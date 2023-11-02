# Libraries
import streamlit as st
import plotly.express as px
import pandas as pd

# Internal Functions
from Funtions import DataConverter
from modelo.modelo_regresion import Modelo
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
# Transformo data para realizarle cambios necesarios
# Llamada a la función para convertir los datos
df = DataConverter().convert_data(df)
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

# Llamar a la función modelo_lineal
y_test, y_pred, mse, r2, coef, interceptor = modelo_instancia.modelo_lineal(['Tamaño', 'Habitaciones'], 'Precio_Casa')

st.title('Modelo de Regreción  Lineal')
st.markdown('Variables en cuenta: Precios de casa, habitaciones_casa, Tamaño de casa')
fig = px.scatter(x=y_test, y=y_pred, labels={'x': 'Valores Reales', 'y': 'Predicciones'},
                 title='Valores Reales vs. Predicciones')
st.plotly_chart(fig)

# Imprimir las métricas de evaluación
st.write(f'Mean Squared Error (MSE): {mse:.2f}')
st.write(f'Coefficient of Determination (R²): {r2:.2f} %')
st.write(f'Coeficiente: {coef} ')
st.write(f'Interceptor: {interceptor} ')

st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------
st.sidebar.header("Acerca de la App")
st.sidebar.write("**Creado el:** Estudiantes de ingeniería de sistemes")
st.sidebar.write("")
st.sidebar.markdown("**Creado el:** 28/08/2023")
