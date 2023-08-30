import plotly.express as px
import pandas as pd
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
# ----------------------------------------------------------------------------------------------------------------------


def scatter_plot(df, x, y):
    """ Grafico de dispercción """

    fig = px.scatter(df, x=df[x], y=df[y], title='Gráfico: número y tamaño de Hab. vs. precio de casa')

    return fig


def bar_plot(df, x, y, title):
    """ Grafico de barras """

    fig = px.bar(df, x=df[x], y=df[y], title=title)
    # Crear el gráfico de barras con Plotly

    return fig


def mapbox_plot(df, x, y):
    """Grafico para ver ubicaciones de mapas"""

    # Inicializar el geocodificador de Google Maps
    geolocator = GoogleV3(api_key='AIzaSyC7F7dTzE8dzP8R4yDKMJuyB79bwNTUUq0')

    # Obtener las coordenadas geográficas para cada ubicación
    df['Coordenadas'] = df[x].apply(lambda location: get_coordinates(geolocator, location))
    df[['Latitud', 'Longitud']] = pd.DataFrame(df['Coordenadas'].tolist(), index=df.index)

    # Crear un gráfico de dispersión en un mapa utilizando scatter_mapbox
    fig = px.scatter_mapbox(df, lat='Latitud', lon='Longitud', size=df[y],
                            title='Gráfico de Precio vs. Ubicación en un Mapa',
                            mapbox_style="carto-positron", zoom=12)

    return fig


def get_coordinates(geolocator, location):
    try:
        result = geolocator.geocode(location)
        if result is not None:
            return (result.latitude, result.longitude)
        else:
            return None
    except GeocoderTimedOut:
        return None



def box_plot(df, x):

    """ Grafico de bigotes """
    fig = px.box(df, y=df[x], title='Gráfico: Precios de casas')

    return fig
