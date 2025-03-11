# Mitos y Leyendas - Card Scraper

Este proyecto es un scraper web diseñado para extraer detalles de cartas del sitio tor.myl.cl utilizando Selenium y BeautifulSoup. El scraper recupera enlaces y detalles de cartas, maneja reintentos para solicitudes fallidas y registra errores.

La intención de este scraper es recopilar información de cartas y sus imágenes de productos y/o ediciones específicas de Mitos y Leyendas para su uso personal.

La información de las cartas se recopila en archivos JSON específicos a la edición o producto.

## Estructura del Proyecto

```
myl_scraper
├── scraped_cards
├── scraping_logs
├── images
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── input_helpers.py
│   ├── scraper.py
│   ├── utils.py
│   └── enums.py
├── requirements.txt
└── README.md
```

## Instalación

Para configurar el proyecto, necesitas tener [Python](https://www.python.org/downloads/) instalado. Luego, sigue estos pasos:

1. Clona el repositorio:
   ```
   git clone https://github.com/andreuvv/myl_scraper.git
   cd myl_scraper
   ```

2. Instala las dependencias requeridas:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar el scraper, utiliza el siguiente comando:
```
python src/main.py
```

El script te guiará a través de los siguientes pasos:

1. **Seleccionar un formato**: Se te pedirá que selecciones un formato de cartas.
2. **Extraer todo el formato**: Se te preguntará si deseas extraer todas las ediciones del formato seleccionado. Responde `y` (sí) o `n` (no).
   - Si respondes `y`, se te preguntará si también deseas descargar las imágenes de las cartas. Responde `y` (sí) o `n` (no).
   - Si respondes `n`, se te preguntará si deseas descargar las imágenes de las cartas. Responde `y` (sí) o `n` (no). Luego, se te pedirá que elijas una edición específica del formato.

Después de configurar las opciones, el script accederá a `tor.myl.cl/cartas/{edicion}` e iniciará el proceso de extracción, obteniendo enlaces y detalles de las cartas. La información se guardará en un archivo JSON dentro de `scraped_cards/{formato}/{edicion}`. Si optaste por descargar las imágenes, estas se guardarán en la carpeta `images/{formato}/{edicion}`.

## Disclaimer

Este script está diseñado únicamente para la obtención de información de cartas que se encuentra de manera pública y gratuita en la web. No está destinado para uso malicioso. El uso indebido del script puede ser ilegal y traer consecuencias para el usuario. El autor no se hace responsable por el uso indebido del script.

Es importante tener en cuenta que la página de tor.myl.cl puede ser inestable y no siempre cargar correctamente sus cartas o puede tener cartas faltantes. En ocasiones, será necesario ejecutar el programa varias veces para obtener correctamente la información de las cartas. Si el programa no puede encontrar una edición específica, contacta a la gente de Tor para que agreguen esas cartas o ediciones. También puedes contactarme para agregar esa edición a las opciones si es que lo olvidé o no estaba configurado correctamente.

## Dependencias

El proyecto requiere los siguientes paquetes de Python:

- selenium
- beautifulsoup4
- webdriver-manager

Asegúrate de instalar estos paquetes utilizando el `requirements.txt` proporcionado.

## Registro de Errores

El scraper registra cualquier error encontrado durante el proceso de scraping en un archivo de registro en la ruta `scraping_logs/scraping_<edition>_errors.log`. Este archivo puede ser utilizado para solucionar problemas con intentos específicos de scraping de cartas.