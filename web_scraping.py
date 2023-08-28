# Libraries
import re
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------------------------------------------------
# creo DataFrame para guardar datos scrapeados
df_links = pd.DataFrame(columns=["Links"])
df = pd.DataFrame(columns=["Precio_Casa", "Tamaño", "Habitaciones", "Baños", "Antiguedad", "Estrato_Social"])


# ----------------------------------------------------------------------------------------------------------------------
pattern = r"(\d+)\s*habs\."
# Url a scrapear para buscar datos
base_url = "https://listado.mercadolibre.com.co/casas-en-venta-medell%C3%ADn#D[A:casas%20en%20venta%20medell%C3" \
                "%ADn]"
max_pages = 42
# Lista para guardar los enlaces a las páginas de detalles
house_links = []

# For para obtener los datos de múltiples páginas
for page_num in range(1, max_pages + 1):
    url_to_scrap = f"{base_url}#D[A:casas%20en%20venta%20medell%C3%ADn]_Desde_{(page_num - 1) * 48 + 1}"
    response = rq.get(url_to_scrap)
    soup = BeautifulSoup(response.content, "html.parser")
    all_house_li = soup.find_all("li", class_="ui-search-layout__item")

    for house in all_house_li:

        # Obtener el enlace a la página de detalles
        house_link = house.find("a", class_="ui-search-item__group__element shops__items-group-details ui-search-link")
        if house_link:
            house_links.append(house_link["href"])

        # obtener tamaño de la casa
        # size_house = house.find(class_="ui-search-card-attributes__attribute").text

# Recorrer los enlaces de las páginas de detalles para obtener más datos
for house_url in house_links:
    response_detail = rq.get(house_url)
    soup_detail = BeautifulSoup(response_detail.content, "html.parser")

    # TODO: REVISAR COMO SCRAPEAR ESE DATO QUE NO TRAE NADA
    x_path = "/html/body/main/div[2]/div[5]/div/div[2]/div[2]/div[2]/section/div[3]/div/div/div/div[1]/div[1]/table/tbody/tr[13]/td/span"
    enlaces = soup_detail.select(x_path)
    print(enlaces)
    # Obtener estrado social
    # social_stratum = soup_detail.find_all("xpath",
    #                                       "/html/body/main/div[2]/div[5]/div/div[2]/div[2]/div[2]/section"
    #                                       "/div[3]/div/div/div/div[1]/div[1]/table/tbody/tr[13]/td/span").text

    # print(social_stratum)
    # if social_stratum:
    #     valor = social_stratum
    #     print(f"Valor: {valor}")
    # else:
    #     print("nada")

    # Obtener precio
    price_house = soup_detail.find(class_="andes-money-amount__fraction").text
    # Convierto a float el precio
    price_house = float("".join(price_house.split(".")))

    # Obtener Habitaciones

    # ----------------------------------------------------------------------------------------------------------
    # Insertar datos en el DataFrame
    # df.loc[len(df)] = [price_house, size_house, bedrooms, bathrooms, antiquity, social_stratum]
    # df.to_csv("data/datos_scrapeados.csv")

# obtener habitación
# habt_url = house.find(class_="ui-search-card-attributes ui-search-item__group__element "
#                              "shops__items-group-details").text

# Utilizar expresión regular para obtener el número de habitaciones
# resultado = re.search(pattern, habt_url)
# if resultado:
#     num_habs = resultado.group(1)
# else:
#     num_habs = "N/A"  # Manejo si no se encuentra el patrón
# # Obtener direccion de la casa
# direccion_casa = house.find(class_="ui-search-item__location").text


