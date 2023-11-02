# Libraries
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Internal Functions
from Funtions import DataConverter

# ----------------------------------------------------------------------------------------------------------------------
# Buscar los datos
# URL del archivo CSV en GitHub (crudo/raw)
csv_url = 'https://github.com/imnicoo7/analisis_unac/raw/main/data/datos_casas.csv'

# Cargar el archivo CSV desde la URL
df = pd.read_csv(csv_url)

# Llamada a la función para convertir los datos
df = DataConverter().convert_data(df)
# ----------------------------------------------------------------------------------------------------------------------


class Modelo:

    def modelo_lineal(self, x, y):

        # Definir variables independientes (características) y la variable dependiente (precio)
        X = df[x]
        y = df[y]

        # TODO: Dividir los datos en conjuntos de entrenamiento y prueba (70% para entrenamiento, 30% para prueba)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Crear el modelo de regresión lineal
        model = LinearRegression()

        # Entrenar el modelo utilizando los datos de entrenamiento
        model.fit(X_train, y_train)

        # Hacer predicciones utilizando los datos de prueba
        y_pred = model.predict(X_test)

        # Calcular métricas de evaluación
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Coeficientes y la interseccion
        coef = model.coef_
        interceptor = model.intercept_

        return y_test, y_pred, mse, r2, coef, interceptor
