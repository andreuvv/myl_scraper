import os
import random
import json
import time
import logging
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from utils import fix_empty_cards
import requests

BASE_URL = "https://tor.myl.cl"

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def set_edition(edition):
    global EDITION, CARDS_PAGE, log_filename
    EDITION = edition
    CARDS_PAGE = f"{BASE_URL}/cartas/{EDITION}"
    os.makedirs("scraping_logs", exist_ok=True)
    log_filename = os.path.join("scraping_logs", f"scraping_{EDITION}_errors.log")
    logging.basicConfig(filename=log_filename, level=logging.WARNING, 
                        format="%(asctime)s - %(levelname)s - %(message)s")
    
def download_image(url, folder, filename):
    """
    Descarga una imagen desde una URL y la guarda en una carpeta específica.

    Args:
        url (str): La URL de la imagen.
        folder (str): La carpeta donde se guardará la imagen.
        filename (str): El nombre del archivo de la imagen.
    """
    response = requests.get(url)
    if response.status_code == 200:
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, filename), 'wb') as f:
            f.write(response.content)
    else:
        logging.warning(f"Error al descargar imagen desde {url}")

def get_card_links():
    driver.get(CARDS_PAGE)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    card_elements = soup.find_all("a", class_="ng-scope")

    links = [card["href"] if card["href"].startswith("http") else BASE_URL + card["href"] for card in card_elements if "href" in card.attrs]
    return links

def start_and_or_retry_scraping(card_url, retries=5):
    for attempt in range(retries):
        try:
            return scrape_card_details(card_url)
        except Exception as e:
            logging.warning(f"Attempt {attempt+1} failed for {card_url}")
            time.sleep(2)
    return {"name": card_url}

def scrape_card_details(card_url):
    driver.get(card_url)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "cardinfo")))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    except TimeoutException:
        logging.warning(f"Timeout waiting for card details on {card_url}")
        return {"name": card_url} 

    card_info = {
        "name": card_url,
        "image_path": None,
        "rarity": None,
        "type": None,
        "race": None,
        "attack": None,
        "cost": None,
        "ability": None
    }

    try:
        name_div = driver.find_element(By.CLASS_NAME, 'content-title')
        name = name_div.text.split('/')[-1].strip()
    except:
        name = card_url
        logging.warning(f"Name extraction failed on {card_url}")

    try:
        img_div = driver.find_element(By.CLASS_NAME, "lazyimg")
        image_url = img_div.get_attribute("back-img")
    except:
        image_url = None
        logging.warning(f"Image extraction failed on {card_url}")

    try:
        card_info_divs = driver.find_elements(By.CLASS_NAME, "cardinfo")
        card_info = None
        for div in card_info_divs:
            if div.is_displayed():
                card_info = div
                break

        if card_info:
            details = card_info.find_elements(By.TAG_NAME, "div")
            card_attributes = {}
            for detail in details:
                try:
                    key = detail.find_element(By.TAG_NAME, "span").text.strip()
                    value = detail.text.replace(key, "").strip()
                    card_attributes[key] = value
                except:
                    continue

            try:
                attack = int(card_attributes.get("Fuerza")) if "Fuerza" in card_attributes else None
            except (TypeError, ValueError):
                attack = None

            try:
                cost = int(card_attributes.get("Coste")) if "Coste" in card_attributes else None
            except (TypeError, ValueError):
                cost = None
            race = card_attributes.get("Raza")
            type_ = card_attributes.get("Tipo")
            rarity = card_attributes.get("Rareza")
        else:
            attack = cost = race = type_ = rarity = None
            logging.warning(f"Card info extraction failed on {card_url}")

    except:
        attack = cost = race = type_ = rarity = None
        logging.warning(f"Card attributes extraction failed on {card_url}")

    try:
        ability_text = driver.find_element(By.CLASS_NAME, "cardability").text.strip()
        ability = ability_text.replace("Habilidad:\n", "").strip()
    except:
        ability = None
        logging.warning(f"Ability extraction failed on {card_url}")

    if not name:
        name = card_url

    return {
        "name": name,
        "image_path": image_url,
        "rarity": rarity,
        "type": type_,
        "race": race,
        "attack": attack,
        "cost": cost,
        "ability": ability
    }

def scrape_edition(format_name, edition, save_images):
    print(f"Extrayendo edición: {edition}")
    start_time = time.time()
    print("Consiguiendo links de las cartas...")
    card_links = get_card_links()
    
    print(f"Se encontraron {len(card_links)} cartas. Extrayendo los detalles...")

    cards_data = []
    for index, link in enumerate(card_links):
        print(f"Extrayendo carta {index + 1}/{len(card_links)}: {link}")
        card_info = start_and_or_retry_scraping(link)
        if card_info:
            if card_info["name"] == link:
                logging.warning(f"Falló la extracción de la información de la carta {link}, URL quedó en el campo de nombre.")
                cards_data.append(card_info)
                print(card_info)
                print(f"\033[91mFalló la extracción de la información de la carta {link}, URL quedó en el campo de nombre.\033[0m")
            else:
                cards_data.append(card_info)
                print(card_info)
                print(f"\033[92m✓ Extracción de la información de la carta {index + 1}/{len(card_links)} exitoso\033[0m")
                if save_images and card_info.get("image_path"):
                    image_folder = os.path.join("images", format_name, edition)
                    sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', card_info['name'])
                    image_filename = f"{sanitized_name.replace(' ', '_')}.jpg"
                    download_image(card_info["image_path"], image_folder, image_filename)
        else:
            logging.warning(f"Saltando carta {link} debido a extracción fallida.")
            print(f"\033[91mSaltando carta {link} debido a extracción fallida.\033[0m")

        time.sleep(random.uniform(1.5, 3))

    os.makedirs(os.path.join("scraped_cards", format_name), exist_ok=True)
    json_filename = os.path.join("scraped_cards", format_name, f"cards_{edition}.json")
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(cards_data, f, indent=4, ensure_ascii=False)

    fix_empty_cards(json_filename, start_and_or_retry_scraping)

    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_time_formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    print(f"Extracción completada, información guardada en '{json_filename}'.")
    print(f"Tiempo total transcurrido: {elapsed_time_formatted}")