import os
from scraper import get_card_links, retry_scraping, download_image, set_edition
from utils import fix_empty_cards
from input_helpers import select_format, select_edition
import random
import json
import time
import logging
import re

def scrape_edition(format_name, edition, save_images):
    print(f"Extrayendo edición: {edition}")
    start_time = time.time()
    print("Consiguiendo links de las cartas...")
    card_links = get_card_links()
    
    print(f"Se encontraron {len(card_links)} cartas. Extrayendo los detalles...")

    cards_data = []
    for index, link in enumerate(card_links):
        print(f"Extrayendo carta {index + 1}/{len(card_links)}: {link}")
        card_info = retry_scraping(link)
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

    fix_empty_cards(json_filename)

    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_time_formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    print(f"Extracción completada, información guardada en '{json_filename}'.")
    print(f"Tiempo total transcurrido: {elapsed_time_formatted}")

def main():
    format_enum = select_format()
    format_name = format_enum.__name__
    scrape_full_format = input("¿Quieres extraer todo el formato? (y/n): ").strip().lower() == 'y'
    save_images = input("¿Quieres guardar las imágenes de las cartas? (y/n): ").strip().lower() == 'y'

    if scrape_full_format:
        for edition in format_enum:
            set_edition(edition.value)
            scrape_edition(format_name, edition.value, save_images)
    else:
        edition = select_edition(format_enum)
        scrape_edition(format_name, edition, save_images)

if __name__ == "__main__":
    main()