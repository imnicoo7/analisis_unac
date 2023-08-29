# Libraries
import re
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------------------------------------------------
# Url a scrapear para buscar datos
base_url = "https://listado.mercadolibre.com.co/inmuebles/antioquia/medellin/casas-en-venta-medell%C3%ADn"
max_pages = 42
# Lista para guardar los enlaces a las páginas de detalles
house_links = []

# For para obtener los datos de múltiples páginas
for page_num in range(1, max_pages + 1):  # entre 1 - 43

    cantidad_li_pag = 48 * page_num  # Aumentar la cantidad en cada iteración
    url_to_scrap = f"{base_url}_Desde_{cantidad_li_pag + 1}_NoIndex_True"

    response = rq.get(url_to_scrap)
    soup = BeautifulSoup(response.content, "html.parser")
    all_house_li = soup.find_all("li", class_="ui-search-layout__item")

    for house in all_house_li:
        # Obtener el enlace a la página de detalles
        house_link = house.find("a", class_="ui-search-item__group__element shops__items-group-details ui-search-link")
        if house_link:
            link = house_link.get("href")  # Extraer el valor del atributo "href"
            house_links.append(link)

# ----------------------------------------------------------------------------------------------------------------------
# Crear el DataFrame con la columna "Links"
links_house = pd.DataFrame(house_links, columns=['Links'])

# Guardar el DataFrame en un archivo CSV en la carpeta "data"
links_house.to_csv('../data/links_house.csv')
