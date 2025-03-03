# Descripción del Proyecto

Este proyecto es un scraper web diseñado para extraer detalles de cartas del sitio de tor.myl.cl utilizando Selenium y BeautifulSoup. El scraper recupera enlaces y detalles de cartas, manejando reintentos para solicitudes fallidas y registrando errores.

La intención de este scraper es simplemente la de recopilar información de cartas y sus imagenes de especificos productos y/o ediciones de Mitos y Leyendas para su posterios uso personal.

La información de las cartas se recopila en archivos JSON especificos a la edición o producto.

## Estructura del Proyecto

```
myl_scrapper
├── src
│   ├── __init__.py
│   ├── main.py
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
   git clone <repository-url>
   cd myl_scrapper
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

Esto iniciará el proceso de scraping, obteniendo enlaces y detalles de cartas, y guardando los resultados en un archivo JSON.

## Dependencias

El proyecto requiere los siguientes paquetes de Python:

- selenium
- beautifulsoup4
- webdriver-manager

Asegúrate de instalar estos paquetes utilizando el `requirements.txt` proporcionado.

## Registro de Errores

El scraper registra cualquier error encontrado durante el proceso de scraping en un archivo de registro llamado `scrapping_<edition>_errors.log`. Este archivo puede ser utilizado para solucionar problemas con intentos específicos de scraping de cartas.
