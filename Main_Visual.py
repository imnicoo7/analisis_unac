# Libraries
import streamlit as st
import plotly.express as px
import pandas as pd

# Internal Functions
from Funtions import DataConverter
from modelo.modelo_regresion import y_test, y_pred, mse, r2
from plotly_functions import scatter_plot, bar_plot, mapbox_plot, box_plot
# ----------------------------------------------------------------------------------------------------------------------

# Configuracion para la página
st.set_page_config(page_title='Analisis exploratorio',
                   initial_sidebar_state='collapsed',
                   page_icon='assets/unac.png',
                   layout='wide')
# ----------------------------------------------------------------------------------------------------------------------
# Obtención de data
df = pd.read_csv('data/datos_casas.csv')
# Transformo data para realizarle cambios necesarios
# data_converter = DataConverter()
# Llamada a la función para convertir los datos
df = DataConverter().convert_data(df)
# ----------------------------------------------------------------------------------------------------------------------


st.title("Unac - Analisis")

avg_price_by_room = df.groupby('habitaciones_categoricas')['Precio_Casa'].mean().reset_index()
# Grafico frecuencia habitaciones
fig = bar_plot(avg_price_by_room, 'habitaciones_categoricas', 'Precio_Casa',
               'Distribución de Precios por Categoría de Habitaciones')

st.plotly_chart(fig, width=600)

# grafico disperción
fig = scatter_plot(df, 'Tamaño', 'Precio_Casa')
# fig = px.scatter(df, x=df['habitaciones_casa'], y=df['Precio_Casa'], title='Gráfico de Dispersión')
st.plotly_chart(fig, width=600)

# Gráfico de bigotes
fig = box_plot(df, 'Precio_Casa')
st.plotly_chart(fig, width=600)

# -------------------------------------------------------- Modelo ------------------------------------------------------

with st.spinner('Cargando el MAPA ----- '):
    # Gráfico de mapas
    fig = mapbox_plot(df, x='Ubicacion', y='Precio_Casa')
    st.plotly_chart(fig, width=600, text_align='center')
    st.markdown("""---""")

# -------------------------------------------------------- Modelo ------------------------------------------------------
with st.spinner('Cargando el módelo'):
    st.title('Modelo de Regreción  Lineal')
    st.markdown('Variables en cuenta: Precios de casa, habitaciones_casa, Tamaño de casa')
    fig = px.scatter(x=y_test, y=y_pred, labels={'x': 'Valores Reales', 'y': 'Predicciones'},
                     title='Valores Reales vs. Predicciones')
    st.plotly_chart(fig, width=600, text_align='center')

    # Imprimir las métricas de evaluación
    st.write(f'Mean Squared Error (MSE): {mse:.2f}')
    st.write(f'Coefficient of Determination (R²): {r2*100:.2f} %')

# ----------------------------------------------------------------------------------------------------------------------
st.sidebar.header("Acerca de la App")
st.sidebar.markdown("**Creado por:**")
st.sidebar.write("Nicolas Steven Gutierrez Catiyejo")
st.sidebar.write("nicolass.gutierrezc@unac.edu.co")
st.sidebar.markdown("**Creado el:** 29/08/2023")
