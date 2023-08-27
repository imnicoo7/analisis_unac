import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
import re

# ----------------------------------------------------------------------------------------------------------------------
# creo DataFrame para guardar datos scrapeados
df = pd.DataFrame(columns=["imagen_url", 'Titulo_casa', "direccion_casa", "tamaño_casa", "habitaciones_casa",
                           "Precio_Casa"])
# ----------------------------------------------------------------------------------------------------------------------
pattern = r"(\d+)\s*habs\."
# Url a scrapear para buscar datos
base_url = "https://listado.mercadolibre.com.co/casas-en-venta-medell%C3%ADn#D[A:casas%20en%20venta%20medell%C3" \
                "%ADn]"
max_pages = 42  # Por ejemplo, rasparemos hasta 10 páginas

# Loop para raspar los datos de múltiples páginas
for page_num in range(1, max_pages + 1):
    url_to_scrap = f"{base_url}#D[A:casas%20en%20venta%20medell%C3%ADn]_Desde_{(page_num - 1) * 48 + 1}"
    response = rq.get(url_to_scrap)
    soup = BeautifulSoup(response.content, "html.parser")
    all_house_li = soup.find_all("li", class_="ui-search-layout__item")

    for house in all_house_li:

        try:
            # Obtener imagen
            img_url = house.find("img")["data-src"]
            # obtener precio
            price_url = house.find(class_="andes-money-amount__fraction").text
            # lo convierto en float el price
            price_url = float("".join(price_url.split(".")))
            # tamaño de casa
            tamaño_casa_url = house.find(class_="ui-search-card-attributes__attribute").text
            habt_url = house.find(class_="ui-search-card-attributes ui-search-item__group__element shops__items-group"
                                         "-details").text
            # Utilizar expresión regular para obtener el número de habitaciones
            resultado = re.search(pattern, habt_url)
            if resultado:
                num_habs = resultado.group(1)
            else:
                num_habs = "N/A"  # Manejo si no se encuentra el patrón
            title_casa_url = house.find(class_="ui-search-item__title").text
            # direccion casa
            direccion_casa = house.find(class_="ui-search-item__location").text

        except:
            img_url = house.find("img")["src"]
            price_url = house.find(class_="andes-money-amount__fraction").text
            price_url = float("".join(price_url.split(".")))
            tamaño_casa_url = house.find(class_="ui-search-card-attributes__attribute").text
            habt_url = house.find_all(class_="ui-search-card-attributes ui-search-item__group__element "
                                             "shops__items-group-details").text
            
            # Utilizar expresión regular para obtener el número de habitaciones
            resultado = re.search(pattern, habt_url)
            if resultado:
                num_habs = resultado.group(1)
            else:
                num_habs = "N/A"  # Manejo si no se encuentra el patrón
            title_casa_url = house.find(class_="ui-search-item__title").text
            direccion_casa = house.find(class_="ui-search-item__location").text
            
        # ------------------------------------------------------------------------------------------------------------------
        # Insertar datos en el DataFrame
        df.loc[len(df)] = [img_url, title_casa_url, direccion_casa, tamaño_casa_url, num_habs, price_url]
        df.to_csv("Datos_Scrapeados.csv")
