# Libraries
import ast
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------------------------------------------------
# creo DataFrame para guardar datos scrapeados
df = pd.DataFrame(columns=["Precio_Casa", "Ubicacion", "Tamaño", "Habitaciones"])
# ----------------------------------------------------------------------------------------------------------------------
# Url a scrapear para buscar datos
base_url = "https://listado.mercadolibre.com.co/inmuebles/antioquia/medellin/casas-en-venta-medell%C3%ADn"
max_pages = 42
# Lista para guardar los enlaces a las páginas de detalles
house_links = []

# For para obtener los datos de múltiples páginas
for page_num in range(1, max_pages + 1):  # entre 1 - 43
    # TODO: No está accediendo a ,a url inicial, arreglas eso ...
    cantidad_li_pag = 48 * page_num  # Aumentar la cantidad en cada iteración
    url_to_scrap = f"{base_url}_Desde_{cantidad_li_pag + 1}_NoIndex_True"

    response = rq.get(url_to_scrap)
    soup = BeautifulSoup(response.content, "html.parser")
    all_house_li = soup.find_all("li", class_="ui-search-layout__item")

    for house in all_house_li:

        # Obtener el precio
        price = house.find(class_="andes-money-amount__fraction").text
        price = float("".join(price.split(".")))

        # Obtener ubicación
        city_element = house.find(class_="ui-search-item__group__element ui-search-item__location shops__"
                                         "items-group-details")
        ubicacion = city_element.text.strip() if city_element else "Ubicación no disponible"

        # Obtener todos los elementos <li> dentro de la lista
        li_elements = soup.find('ul', class_='ui-search-card-attributes').find_all('li')

        # Obtener los valores de los elementos <li>
        size = li_elements[0].get_text()
        bedrooms = li_elements[1].get_text()

        # --------------------------------------------------------------------------------------------------------------
        # Inserto en el DataFrame inicial
        df.loc[len(df)] = [price, ubicacion, size, bedrooms]
        # Guardar el DataFrame en un archivo CSV
        df.to_csv('../data/datos_casas.csv')
