import plotly.express as px
import pandas as pd
import folium
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
# ----------------------------------------------------------------------------------------------------------------------


def scatter_plot(df, x, y, title):
    """ Grafico de dispercción """

    fig = px.scatter(x=df[x], y=df[y], title=title)

    fig.update_xaxes(showline=True, linewidth=1, linecolor='white')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='white')

    return fig


def bar_plot(df, x, y, title):
    """ Grafico de barras """

    # Crear el gráfico de barras con Plotly
    fig = px.bar(df, x=df[x], y=df[y], title=title)

    fig.update_xaxes(showline=True, linewidth=1, linecolor='white')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='white')

    return fig


import time
import folium

def mapbox_plot(df, x, y):
    # Crear un mapa centrado en Medellín
    m = folium.Map(location=[6.253041, -75.564574], zoom_start=12)

    # Agregar un marcador fijo en las coordenadas 6.253041, -75.564574
    folium.Marker(
        location=[6.253041, -75.564574],
        popup="Ubicación Fija: Medellín",
        icon=folium.Icon(color="red")  # Puedes personalizar el ícono del marcador
    ).add_to(m)

    # Iterar a través de las filas del DataFrame
    for idx, row in df.iterrows():
        # Obtener las coordenadas (latitud, longitud) desde la columna x
        latitud, longitud = [float(coord.strip()) for coord in row[x].split(',')]

        # Agregar un marcador al mapa
        folium.Marker(
            location=(latitud, longitud),
            popup=f"Coordenadas: {latitud}, {longitud}, Precio: ${row[y]}",
        ).add_to(m)

    return m

def mapbox_plot():
    m = folium.Map(location=[6.253041, -75.564574], zoom_start=12)

    return m



def get_coordinates(geolocator, location):
    try:
        result = geolocator.geocode(location)
        if result is not None:
            return (result.latitude, result.longitude)
        else:
            return None
    except GeocoderTimedOut:
        return None


def box_plot(df, x, title):

    """ Grafico de bigotes """
    fig = px.box(df, y=df[x], title=title)

    fig.update_xaxes(showline=True, linewidth=1, linecolor='white')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='white')

    return fig


def correlation_matrix(df, title):

    """Funcion para crear una matrix de correlacion y ver los datos"""

    fig = px.imshow(df, color_continuous_scale='RdBu', zmin=-1, zmax=1, title=title)
    # Agregar texto a cada celda con los valores de correlación
    for i in range(len(df.columns)):
        for j in range(len(df.columns)):
            fig.add_annotation(
                x=i, y=j,
                text=f"{df.iloc[i, j]:.4f}",
                showarrow=False,
                font=dict(size=20),
                bgcolor='black'
            )

    fig.update_xaxes(showline=True, linewidth=1, linecolor='white')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='white')
    return fig


def histograma(df, x, title):

    fig = px.histogram(df, x='Tamaño', nbins=10, title=title)

    fig.update_xaxes(showline=True, linewidth=1, linecolor='white')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='white')

    return fig
