# Libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


# ----------------------------------------------------------------------------------------------------------------------


def conversion_data(df):
    # Extraer los números y convertir a m²
    df['tamaño_casa'] = df['tamaño_casa'].str.extract('(\d+)').astype(float)

    # Calcular la media
    media = np.mean(df['Precio_Casa'])  # y la desviación estándar
    desviacion_estandar = np.std(df['Precio_Casa'])

    # Estandarización: restar la media y dividir por la desviación estándar
    df['Precio_Casa'] = (df['Precio_Casa'] - media) / desviacion_estandar

    # Definir los límites de los intervalos para las categorías
    bins = [0, 1, 2, 3, 4, 5, 10]

    # Etiquetas para las categorías
    labels = ['1 habitación', '2 habitaciones', '3 habitaciones', '4 habitaciones', '5 habitaciones',
              '6 o más habitaciones']

    # Agregar una nueva columna categórica al DataFrame
    df['habitaciones_categoricas'] = pd.cut(df['habitaciones_casa'], bins=bins, labels=labels)
    # pd.cut() se usa para convertir la variable numérica en una variable categórica

    return df
