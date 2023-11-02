# Libraries
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
#  Casas
# Página para scrapear datos de las motos
base_url = "https://listado.mercadolibre.com.co/casas-en-venta-medellin#D[A:casas%20en%20venta%20medellin]"

# Lista para almacenar los datos
casas = []

# Página inicial y final
current_page = 1
max_pages = 41

while current_page <= max_pages:

    # Construir la URL de la página actual
    url = f"{base_url}_Desde_{(current_page - 1) * 41 + 1}"

    # Realizar la solicitud HTTP
    response = rq.get(base_url)

    # Utilizar BeautifulSoup para analizar el contenido HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrar todas las tarjetas de anuncio de motos
    casa_cards = soup.find_all("div", class_="ui-search-result__content-wrapper")

    # Si no se encuentran tarjetas de anuncio, se asume que no hay más resultados
    if not casa_cards:
        break

    # Iterar a través de las tarjetas y extraer los datos
    for card in casa_cards:
        precio = card.find("span", class_="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript").text.strip()
        atributos = card.find("ul", class_="ui-search-card-attributes ui-search-item__attributes-grid")
        habitaciones = atributos.find("li", class_="ui-search-card-attributes__attribute").text.strip()
        banos = atributos.find_all("li", class_="ui-search-card-attributes__attribute")[1].text.strip()
        tamano = atributos.find_all("li", class_="ui-search-card-attributes__attribute")[2].text.strip() if len(atributos.find_all("li", class_="ui-search-card-attributes__attribute")) >= 3 else ""
        ubicacion = card.find("span", class_="ui-search-item__location-label").text.strip()

        # Agregar los datos de la casa a la lista
        casas.append([precio, habitaciones, banos, tamano, ubicacion])
    # Avanzar a la siguiente página
    current_page += 1

# Crear un DataFrame de Pandas con los datos
df = pd.DataFrame(casas, columns=["Precio", "Habitaciones", "Baños", "Tamaño", "Ubicación"])

# Guardar los datos en un archivo CSV
df.to_csv('datos_casas_v2.csv', index=False)
