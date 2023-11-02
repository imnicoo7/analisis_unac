# Libraries
import streamlit as st
import plotly.express as px
import pandas as pd

# Internal Functions
from Funtions import DataConverter
from Funtions_v2 import DataConverter_v2
from modelo.modelo_regresion import Modelo
from modelo.modelo_regresion_v2 import Modelo_update
from plotly_functions import PlotlyFunciones
# ----------------------------------------------------------------------------------------------------------------------

# Configuracion para la página
st.set_page_config(page_title='Analisis Ventas',
                   initial_sidebar_state='collapsed',
                   page_icon='assets/unac.png',
                   layout='wide')
# ----------------------------------------------------------------------------------------------------------------------

# Obtención de data
df = pd.read_csv('data/datos_casas.csv')
df2 = pd.read_csv('data/datos_casas_v2.csv')
# Transformo data para realizarle cambios necesarios
# Llamada a la función para convertir los datos
df =  DataConverter().convert_data(df)
df2 =  DataConverter_v2().convert_data_2(df2)
# ----------------------------------------------------------------------------------------------------------------------

st.title("Modelo de predicción de precios de casas en la ciudad de Medellín para apoyar la toma de decisiones de compra"
         "y venta de propiedad raíz 📈")
# Espacios para
st.markdown("")
st.markdown("")
st.markdown("""---""")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
# ----------------------------------------------------------------------------------------------------------------------
# Instacia a clase de graficas
graficas = PlotlyFunciones()
col1, col2 = st.columns(2)
with col1:
    # Calcular el total de casas por numero de habitacioens
    total_rooms_by_category = df['habitaciones_categoricas'].value_counts().reset_index()
    total_rooms_by_category.columns = ['habitaciones_categoricas', 'Habitaciones']
    total_rooms_by_category = total_rooms_by_category.sort_values(by='habitaciones_categoricas', ascending=True)

    # Graficar el total de habitaciones por categoría
    fig = graficas.bar_plot(total_rooms_by_category, 'habitaciones_categoricas', 'Habitaciones',
                            'Total de casas por la categoría de habitaciones')
    st.plotly_chart(fig, width=400)
    st.markdown("""---""")

with col2:
    fig = graficas.box_plot(df, 'Habitaciones', 'Box-Plot: Habitaciones de casas')
    st.plotly_chart(fig)
    # Gráfico de bigotes
    st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------

with col1:
    fig = graficas.box_plot(df, 'Tamaño', 'Box-Plot: Tamaño de casas')
    st.plotly_chart(fig)
    st.markdown("""---""")

with col2:
    fig = graficas.box_plot(df, 'Precio_Casa', 'Box-Plot: Precios de casas')
    st.plotly_chart(fig)
    st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------

# grafico disperción
with col1:
    fig = graficas.scatter_plot(df, 'Tamaño', 'Precio_Casa', 'Scatter: Tamaño vs. precio de casas', 'Tamaño', 'Precios')
    st.plotly_chart(fig)
    st.markdown("""---""")

# grafico disperción
with col2:
    # Grafico histograma
    fig = graficas.histrogram(df, 'Tamaño', 'Histograma del Tamaño de las Casas')
    st.plotly_chart(fig)
    st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------

with col1:
    fig = graficas.histrogram(df, 'Precio_Casa', 'Histograma de los precios de las casas', )
    st.plotly_chart(fig)
    st.markdown("""---""")

with col2:
    # Histograma precios estandarizados
    fig = graficas.histrogram(df, 'precios_estandarizados', 'Histograma de Valores Estandarizados')
    st.plotly_chart(fig)
    st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------

col1, col2 = st.columns(2)
with col1:
    with st.spinner('Cargando el MAPA ----- :) '):
        mapa = graficas.mapbox_plot()
        st.components.v1.html(mapa._repr_html_(), width=700, height=600)

with col2:
    # Grafico matrix corelación
    df_coor = df[['Precio_Casa', 'Tamaño', 'Habitaciones']]
    numeric_df = df_coor.select_dtypes(include=['number'])
    df_correlation = numeric_df.corr()
    fig = graficas.correlation_matrix(df_correlation, 'Mapa de Correlación')
    st.plotly_chart(fig)
st.markdown("""---""")

# -------------------------------------------------------- Modelo ------------------------------------------------------

# Crear una instancia de la clase Modelo
modelo_instancia = Modelo()
modelo_instancia_2 = Modelo_update()

# Llamar a la función modelo_lineal
y_test, y_pred, mse, r2, coef, interceptor = modelo_instancia.modelo_lineal(['Tamaño', 'Habitaciones'], 'Precio_Casa')
# Llamado al nuevo modelo con la nueva variable 
#  modelo_instancia = Modelo_update()
y2_test, y2_pred, mse_2, r2_2, coef_2, interceptor_2 = modelo_instancia_2.modelo_lineal(['Tamaño', 'Habitaciones', 'Habitaciones'], 'Precio')

st.title('Modelo de Regreción  Lineal')
st.markdown('Variables en cuenta: Precios de casa, habitaciones_casa, Tamaño de casa')
fig = px.scatter(x=y_test, y=y_pred, labels={'x': 'Valores Reales', 'y': 'Predicciones'},
                 title='Valores Reales vs. Predicciones')
st.plotly_chart(fig)

# Imprimir las métricas de evaluación
st.write(f'Mean Squared Error (MSE): {mse:.2f}')
st.write(f'Coefficient of Determination (R²): {r2 * 100:.2f} %')
st.write(f'Coeficiente: {coef} ')
st.write(f'Interceptor: {interceptor} ')

st.title('Nuevo modelo de Regreción  Lineal')
st.markdown("""Nuevo modelo con la nueva variable """)
st.markdown('Variables en cuenta: Precios de casa, habitaciones_casa, Tamaño de casa, Habitaciones')
fig = px.scatter(x=y2_test, y=y2_pred, labels={'x': 'Valores Reales', 'y': 'Predicciones'},
                 title='Valores Reales vs. Predicciones')
st.plotly_chart(fig)

# Imprimir las métricas de evaluación
st.write(f'Mean Squared Error (MSE): {mse_2:.2f}')
st.write(f'Coefficient of Determination (R²): {r2_2 * 100:.2f} %')
st.write(f'Coeficiente: {coef_2} ')
st.write(f'Interceptor: {interceptor_2} ')

st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------
st.sidebar.header("Acerca de la App")
st.sidebar.write("**Creado por:** Estudiantes de ingeniería de sistemas")
st.sidebar.markdown("**Creado el:** 28/08/2023")
