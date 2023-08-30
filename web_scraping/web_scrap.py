# Libraries
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------------------------------------------------
# creo DataFrame para guardar datos scrapeados
df = pd.DataFrame(columns=["Tipo_Vivienda", "Precio_Casa", "Ubicacion", "Tamaño", "Habitaciones"])
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
        ubicacion = house.find(class_="ui-search-item__location-label").text

        # Obtener todos los elementos <li> dentro de la lista
        li_container = house.find('ul', class_='ui-search-card-attributes ui-search-item__group__element ui-search-'
                                                'item__attributes-grid shops__items-group-details')

        # Verificar si se encontró el contenedor de elementos <li>
        if li_container:
            li_elements = li_container.find_all('li')

            # Verificar si hay al menos dos elementos en la lista
            if len(li_elements) >= 2:
                size = li_elements[0].get_text()
                bedrooms = li_elements[1].get_text()
                print(size + ' - ' + bedrooms)
            else:
                print("No hay suficientes elementos en la lista")
        else:
            print("No se encontraron elementos <li> en la lista")

        tipo_vivienda = house.find(
        class_="ui-search-item__group__element ui-search-item__subtitle-grid shops__items-group-details").text

        # --------------------------------------------------------------------------------------------------------------
        # Inserto en el DataFrame inicial
        df.loc[len(df)] = [tipo_vivienda, price, ubicacion, size, bedrooms]
        # Guardar el DataFrame en un archivo CSV
        df.to_csv('datos_casas2.csv')
