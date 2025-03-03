from scraper import retry_scraping
import json

def fix_empty_cards(json_filename):
    """Read the JSON file, identify cards with type as null, and retry scraping for those cards."""
    with open(json_filename, "r", encoding="utf-8") as f:
        cards_data = json.load(f)

    fixed_cards_data = []
    for card in cards_data:
        if card["type"] is None:
            print(f"Retrying scraping for failed card: {card['name']}")
            fixed_card = retry_scraping(card["name"])
            fixed_cards_data.append(fixed_card)
        else:
            fixed_cards_data.append(card)

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(fixed_cards_data, f, indent=4, ensure_ascii=False)
    print(f"Fixed empty cards and saved updated data to '{json_filename}'.")