from scraper import EDITION, get_card_links, retry_scraping
from utils import fix_empty_cards
import random
import json
import time
import logging

def main():
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
                print(f"\033[91mCard scraping failed for {link}, only URL in the name field.\033[0m")
            else:
                cards_data.append(card_info)
                print(f"\033[92m✓ Successfully scraped card {index + 1}/{len(card_links)}\033[0m")
        else:
            logging.warning(f"Skipping {link} due to failed scraping.")
            print(f"\033[91mSkipping {link} due to failed scraping\033[0m")

        time.sleep(random.uniform(1.5, 3))

    json_filename = f"cards_{EDITION}.json"
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