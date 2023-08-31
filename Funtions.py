# Libraries
import pandas as pd
from sklearn.preprocessing import StandardScaler
# ----------------------------------------------------------------------------------------------------------------------


class DataConverter:

    def convert_data(self, df):

        """ Función de conversión de datos"""

        # Crear objeto StandardScaler
        scaler = StandardScaler()

        # Convertir la columna 'Precio_Casa' en una matriz 2D
        precio_casa_2d = df[['Precio_Casa']]

        # Aplicar la estandarización
        df['precios_estandarizados'] = scaler.fit_transform(precio_casa_2d)

        # Convertir Tamaño a entero y dejar los números
        df['Tamaño'] = df['Tamaño'].str.extract(r'(\d+)').astype(int)

        # Extraer el número utilizando str.extract y una expresión regular y convertir la columna a números enteros
        df['Habitaciones'] = df['Habitaciones'].str.extract(r'(\d+)').astype(int)

        # Definir los límites de los intervalos para las categorías de habitaciones
        bins = [0, 1, 2, 3, 4, 5, float('inf')]

        # Etiquetas para las categorías de habitaciones
        labels = ['1 habitación', '2 habitaciones', '3 habitaciones', '4 habitaciones', '5 habitaciones',
                  '6 o más habitaciones']

        # Agregar una nueva columna categórica al DataFrame para las habitaciones
        df['habitaciones_categoricas'] = pd.cut(df['Habitaciones'], bins=bins, labels=labels)

        df = df.loc[df['Tamaño'] >= 40]

        # Filtrar y eliminar las filas con palabras clave en la columna "tipo", me aseguro que solo sean ventas
        palabras_clave = ['arriendo', 'Finca', 'Apartamento']
        df = df[~df['Tipo_Vivienda'].str.contains('|'.join(palabras_clave))]

        return df
