# Libraries
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Internal Functions
from Funtions import DataConverter

# ----------------------------------------------------------------------------------------------------------------------
# Buscar los datos
df = pd.read_csv('C:/Users/nikog/OneDrive/Documentos/Universidad/10 semestre/Análisis de datos/analisis_unac/data/'
                 'datos_casas.csv')

# Llamada a la función para convertir los datos
df = DataConverter().convert_data(df)
# ----------------------------------------------------------------------------------------------------------------------

# Definir variables independientes (características) y la variable dependiente (precio)
X = df[['Tamaño', 'Habitaciones']]
y = df['Precio_Casa']

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
