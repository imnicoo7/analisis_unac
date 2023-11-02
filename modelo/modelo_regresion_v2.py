# Libraries
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Internal Functions
from Funtions_v2 import DataConverter_v2

# ----------------------------------------------------------------------------------------------------------------------
# Buscar los datos
# URL del archivo CSV en GitHub (crudo/raw)
csv_url2 = 'https://github.com/imnicoo7/analisis_unac/raw/main/data/datos_casas_v2.csv'

df2 = pd.read_csv(csv_url2)

# Llamada a la función para convertir los datos
df2 = DataConverter_v2().convert_data_2(df2)
# ----------------------------------------------------------------------------------------------------------------------

class Modelo_update:
    def modelo_lineal(self, x, y):

        # Definir variables independientes (características) y la variable dependiente (precio)
        X = df2[x]
        y = df2[y]

        # TODO: Dividir los datos en conjuntos de entrenamiento y prueba (70% para entrenamiento, 30% para prueba)
        X2_train, X2_test, y2_train, y2_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Crear el modelo de regresión lineal
        model = LinearRegression()

        # Entrenar el modelo utilizando los datos de entrenamiento
        model.fit(X2_train, y2_train)

        # Hacer predicciones utilizando los datos de prueba
        y2_pred = model.predict(X2_test)

        # Calcular métricas de evaluación
        mse_2 = mean_squared_error(y2_test, y2_pred)
        r2_2 = r2_score(y2_test, y2_pred)

        # Coef_2icientes y la interseccion
        coef_2 = model.coef_
        interceptor_2 = model.intercept_

        return y2_test, y2_pred, mse_2, r2_2, coef_2, interceptor_2
