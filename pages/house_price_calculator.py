# Libraries
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Internal Functions
from Funtions import DataConverter

# ----------------------------------------------------------------------------------------------------------------------
# Configuracion para la página
st.set_page_config(page_title='Calculator price',
                   initial_sidebar_state='collapsed',
                   page_icon='assets/unac.png',
                   layout='wide')
# ----------------------------------------------------------------------------------------------------------------------
# Obtención de data
df = pd.read_csv('data/datos_casas.csv')
# Transformo data para realizarle cambios necesarios
df = DataConverter().convert_data(df)
# ----------------------------------------------------------------------------------------------------------------------
# Crear el modelo de regresión lineal
model = LinearRegression()
model.fit(df[['Tamaño', 'Habitaciones']], df['Precio_Casa'])
# ----------------------------------------------------------------------------------------------------------------------
# Interfaz de usuario con Streamlit
st.title('Calculadora de precio para tú Casa según carácteristicas 🏠')
st.markdown("")
st.markdown("")
st.markdown("""---""")

st.subheader('Ingrese los detalles de su casa para obtener un consejo sobre el precio.')
nombre = st.text_input("Ingrese su primer nombre por favor")
habitaciones = st.number_input('Número de Habitaciones:', value=2, min_value=1, max_value=10)
tamaño = st.number_input('Tamaño de la Casa (m²):', value=60, min_value=1, max_value=1000)
precio_consejo = model.predict([[tamaño, habitaciones]])
calculo = st.button("Conocer price")
if calculo:
    st.subheader(f"Basado en tús necedidades, el precio sugerido para la casa es: ${precio_consejo[0]:,.2f}. "
                 f"Empiece a ahorrar pues {nombre}")

# ----------------------------------------------------------------------------------------------------------------------
st.sidebar.header("Acerca de la App")
st.sidebar.write("Ingeniería de sistemes 2023")
st.sidebar.write("nicolass.gutierrezc@unac.edu.co")
st.sidebar.markdown("**Creado el:** 29/08/2023")
