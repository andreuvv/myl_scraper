# Mitos y Leyendas - Card Scraper

Este proyecto es un scraper web diseñado para extraer detalles de cartas del sitio de tor.myl.cl utilizando Selenium y BeautifulSoup. El scraper recupera enlaces y detalles de cartas, manejando reintentos para solicitudes fallidas y registrando errores.

La intención de este scraper es simplemente la de recopilar información de cartas y sus imagenes de especificos productos y/o ediciones de Mitos y Leyendas para su posterios uso personal.

La información de las cartas se recopila en archivos JSON especificos a la edición o producto.

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

Para configurar el proyecto necesitas tener Python instalado, luego sigue estos pasos:

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

Para ejecutar el scraper, ejecuta el siguiente comando:
```
python src/main.py
```

El script the pedirá seleccionar un formato, luego te preguntará si quieres extraer el formato entero, si les das a si (y), te preguntará si además quieres descargar las imagenes, si pones que si (y), comenzará el proceso de extracción edición por edición del formato, si pones que no (n) a la extracción completa del formato, te preguntará que eligas una edición especifica del formato, después de configuradas las opciones, entrará tor.myl.cl/cartas/****** e iniciará el proceso de extracción, obteniendo enlaces y detalles de cartas, y guardando la información de las cartas en un archivo JSON, dentro de scraped_cards/{formato}/{edicion}, si la opcion de descargar las imagenes fue configurada, las imagenes quedarán guardadas dentro de la carpeta images/{formato}/{edicion}.

## Disclaimer

Este script no está diseñado para su uso malicioso, solo para la obtención de información de cartas que se encuentra de manera pública y gratuita en la web. Su uso indebido puede llegar a ser ilegal y traerá consecuencias para su usuario. El autor no se hace responsable por su uso indebido.

Hay que entender que la pagina de tor.myl.cl es muy inestable y no siempre carga correctamente sus cartas y/o tiene cartas faltantes. A veces habrá que correr el programa varias veces para conseguir correctamente la información de las cartas. Si el programa no puede encontrar una edición en especifico, contactar a la gente de Tor para que agreguen esas cartas y/o ediciones. Tambien a mi, para yo poder agregar esa edición a las opciones si es que lo olvidé o no estaba configurado correctamente.

## Dependencias

El proyecto requiere los siguientes paquetes de Python:

- selenium
- beautifulsoup4
- webdriver-manager

Asegúrate de instalar estos paquetes utilizando el `requirements.txt` proporcionado.

## Registro de Errores

El scraper registra cualquier error encontrado durante el proceso de scraping en un archivo de registro llamado `scrapping_<edition>_errors.log`. Este archivo puede ser utilizado para solucionar problemas con intentos específicos de scraping de cartas.
