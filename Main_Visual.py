# Libraries
import streamlit as st
import plotly.express as px
import pandas as pd

# Internal Functions
from Funtions import DataConverter
from modelo.modelo_regresion import y_test, y_pred, mse, r2
from plotly_functions import scatter_plot, bar_plot, mapbox_plot, box_plot, correlation_matrix
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

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig, width=1000)

# grafico disperción
fig = scatter_plot(df, 'Tamaño', 'Precio_Casa', 'Gráfico: número y tamaño de Hab. vs. precio de casa')

with col2:
    st.plotly_chart(fig, width=600)

# Gráfico de bigotes
fig = box_plot(df, 'Precio_Casa')
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig, width=600)

# ---------------------------------------------- Coorelación Mapa ------------------------------------------------------
# df_coorelacion = df['Precio_Casa']
numeric_df = df.select_dtypes(include=['number'])
df_correlation = numeric_df.corr()
fig = correlation_matrix(df_correlation, 'Mapa de Correlación')

with col2:
    st.plotly_chart(fig, width=800)

# -------------------------------------------------------- Mapa --------------------------------------------------------

with st.spinner('Cargando el MAPA ----- '):
    # Gráfico de mapas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('Aqui va el mapa')
#     fig = mapbox_plot(df, x='Ubicacion', y='Precio_Casa')

#         st.plotly_chart(fig, width=600, text_align='center')
#     st.markdown("""---""")

# -------------------------------------------------------- Modelo ------------------------------------------------------
with st.spinner('Cargando el módelo'):
    with col2:
        st.title('Modelo de Regreción  Lineal')
        st.markdown('Variables en cuenta: Precios de casa, habitaciones_casa, Tamaño de casa')
        fig = px.scatter(x=y_test, y=y_pred, labels={'x': 'Valores Reales', 'y': 'Predicciones'},
                         title='Valores Reales vs. Predicciones')

        # fig = scatter_plot(modelo, y_pred, 'Valores Reales vs. Predicciones')

        st.plotly_chart(fig, width=600, text_align='center')

        # Imprimir las métricas de evaluación
        st.write(f'Mean Squared Error (MSE): {mse:.2f}')
        st.write(f'Coefficient of Determination (R²): {r2*100:.2f} %')

# ----------------------------------------------------------------------------------------------------------------------
st.sidebar.header("Acerca de la App")
st.sidebar.write("Ingeniería de sistemes 2023")
st.sidebar.write("nicolass.gutierrezc@unac.edu.co")
st.sidebar.markdown("**Creado el:** 29/08/2023")
