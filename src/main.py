import os
from scraper import get_card_links, retry_scraping, set_edition
from utils import fix_empty_cards
from enums import FxEditions, PbEditions, PeEditions, SbEditions, ImperioEditions
import random
import json
import time
import logging

def select_format():
    formats = {
        1: ("Primera Era", PeEditions),
        2: ("Primer Bloque", PbEditions),
        3: ("Segundo Bloque", SbEditions),
        4: ("Furia Extendido", FxEditions),
        5: ("Imperio", ImperioEditions)
    }
    
    print("Please select a format:")
    for i, (name, _) in formats.items():
        print(f"{i}. {name}")

    choice = int(input("Enter the number of the format: "))
    selected_format = formats[choice][1]
    return selected_format

def select_edition(format_enum):
    print("Please select an edition:")
    for i, edition in enumerate(format_enum, 1):
        print(f"{i}. {edition.name}")

    choice = int(input("Enter the number of the edition: "))
    selected_edition = list(format_enum)[choice - 1]
    set_edition(selected_edition.value)
    return selected_edition.value

def main():
    format_enum = select_format()
    edition = select_edition(format_enum)
    start_time = time.time()
    print("Fetching card links...")
    card_links = get_card_links()
    
    print(f"Found {len(card_links)} cards. Scraping details...")

    cards_data = []
    for index, link in enumerate(card_links):
        print(f"Scraping {index + 1}/{len(card_links)}: {link}")
        card_info = retry_scraping(link)
        if card_info:
            if card_info["name"] == link:
                logging.warning(f"Card scraping failed for {link}, only URL in the name field.")
                cards_data.append(card_info)
                print(card_info)
                print(f"\033[91mCard scraping failed for {link}, only URL in the name field.\033[0m")
            else:
                cards_data.append(card_info)
                print(card_info)
                print(f"\033[92m✓ Successfully scraped card {index + 1}/{len(card_links)}\033[0m")
        else:
            logging.warning(f"Skipping {link} due to failed scraping.")
            print(f"\033[91mSkipping {link} due to failed scraping\033[0m")

        time.sleep(random.uniform(1.5, 3))

    os.makedirs("scrapped_cards", exist_ok=True)
    json_filename = os.path.join("scrapped_cards", f"cards_{edition}.json")
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(cards_data, f, indent=4, ensure_ascii=False)

    fix_empty_cards(json_filename)

    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_time_formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    print(f"Scraping complete! Data saved to '{json_filename}'.")
    print(f"Total time taken: {elapsed_time_formatted}")

if __name__ == "__main__":
    main()