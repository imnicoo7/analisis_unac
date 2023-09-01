# Libraries
import plotly.express as px
import pandas as pd

from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
# ----------------------------------------------------------------------------------------------------------------------


class PlotlyFunciones:
    def scatter_plot(self, df, x, y, title, x_label, y_label):
        """ Grafico de dispercción """

        fig = px.scatter(x=df[x], y=df[y], title=title, labels={'x': x_label, 'y': y_label})

        fig.update_xaxes(showline=True, linewidth=1, linecolor='white')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='white')

        return fig

    def bar_plot(self, df, x, y, title):
        """ Grafico de barras """

        # Crear el gráfico de barras con Plotly
        fig = px.bar(df, x=df[x], y=df[y], title=title)

        fig.update_xaxes(showline=True, linewidth=1, linecolor='white')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='white')

        return fig

    def mapbox_plot(self, df, x, y):
        """Grafico para ver ubicaciones de mapas"""

        # Inicializar el geocodificador de Google Maps
        geolocator = GoogleV3(api_key='AIzaSyAKS2DZ10Y8CpDqYihAzPlNWsgGNYFRNl0')

        # Obtener las coordenadas geográficas para cada ubicación
        df['Coordenadas'] = df[x].apply(lambda location: self.get_coordinates(geolocator, location))
        df[['Latitud', 'Longitud']] = pd.DataFrame(df['Coordenadas'].tolist(), index=df.index)

        # Crear un gráfico de dispersión en un mapa utilizando scatter_mapbox
        fig = px.scatter_mapbox(df, lat='Latitud', lon='Longitud', size=df[y],
                                title='Gráfico de Precio vs. Ubicación en un Mapa',
                                mapbox_style="carto-positron", zoom=12)

        fig.update_xaxes(showline=True, linewidth=1, linecolor='white')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='white')

        return fig

    def get_coordinates(self, geolocator, location):
        try:
            result = geolocator.geocode(location)
            if result is not None:
                return (result.latitude, result.longitude)
            else:
                return None
        except GeocoderTimedOut:
            return None

    def box_plot(self, df, x, title):

        """ Grafico de bigotes """
        fig = px.box(df, y=df[x], title=title)

        fig.update_xaxes(showline=True, linewidth=1, linecolor='white')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='white')

        return fig

    def correlation_matrix(self, df, title):

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

    def histrogram(self, df, x, title):

        fig = px.histogram(df, x=x, nbins=20, title=title)

        fig.update_xaxes(showline=True, linewidth=1, linecolor='white')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='white')

        return fig
