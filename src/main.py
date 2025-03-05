import os
from scraper import get_card_links, retry_scraping, download_image
from utils import fix_empty_cards
from input_helpers import select_format, select_edition
import random
import json
import time
import logging

def main():
    format_enum = select_format()
    edition = select_edition(format_enum)
    save_images = input("¿Quieres guardar las imágenes de las cartas? (y/n): ").strip().lower() == 'y'
    start_time = time.time()
    print("Consiguiendo links de las cartas...")
    card_links = get_card_links()
    
    print(f"Se encontraron {len(card_links)} cartas. Extrayendo los detalles...")

    cards_data = []
    for index, link in enumerate(card_links):
        print(f"Scraping {index + 1}/{len(card_links)}: {link}")
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
                    download_image(card_info["image_path"], f"images_{edition}", f"{card_info['name']}.jpg")
        else:
            logging.warning(f"Saltando carta {link} debido a extracción fallida.")
            print(f"\033[91mSaltando carta {link} debido a extracción fallida.\033[0m")

        time.sleep(random.uniform(1.5, 3))

    os.makedirs("scraped_cards", exist_ok=True)
    json_filename = os.path.join("scraped_cards", f"cards_{edition}.json")
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

if __name__ == "__main__":
    main()