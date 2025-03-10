from scraper import set_edition, scrape_edition
from input_helpers import select_format, select_edition

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