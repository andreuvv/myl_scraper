from scraper import retry_scraping
import json

def fix_empty_cards(json_filename):
    """
    Lee el archivo JSON, identifica las cartas con el campo "type" nulo e 
    intenta recuperar la información para esas cartas.
    Actualiza el archivo JSON con la información recuperada.
    
    Args:
        json_filename (str): La ruta al archivo JSON que contiene los datos de las cartas.
    """
    with open(json_filename, "r", encoding="utf-8") as f:
        cards_data = json.load(f)

    fixed_cards_data = []
    for card in cards_data:
        if card["type"] is None:
            print(f"Reintentado la extracción de información de la carta: {card['name']}")
            fixed_card = retry_scraping(card["name"])
            fixed_cards_data.append(fixed_card)
        else:
            fixed_cards_data.append(card)

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(fixed_cards_data, f, indent=4, ensure_ascii=False)
    print(f"Cartas fallidas o vacías corregidas, información actualizada y guarda en '{json_filename}'.")