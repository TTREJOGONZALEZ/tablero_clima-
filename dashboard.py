
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuracion del tablero
st.set_page_config(
    page_title="Tablero del Clima",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Tablero del Clima")
st.write("Analisis de datos meteorologicos de Queretaro")

# Coordenadas de Queretaro
latitud = 20.5888
longitud = -100.3899

# Consultar la API de Open-Meteo
url = "https://api.open-meteo.com/v1/forecast"

parametros = {
    "latitude": latitud,
    "longitude": longitud,
    "hourly": "temperature_2m,relative_humidity_2m,precipitation",
    "timezone": "America/Mexico_City",
    "forecast_days": 3
}

try:
    respuesta = requests.get(url, params=parametros, timeout=15)
    respuesta.raise_for_status()
    datos = respuesta.json()

    # Convertir los datos a un DataFrame
    df = pd.DataFrame({
        "Fecha": pd.to_datetime(datos["hourly"]["time"]),
        "Temperatura": datos["hourly"]["temperature_2m"],
        "Humedad": datos["hourly"]["relative_humidity_2m"],
        "Precipitacion": datos["hourly"]["precipitation"]
    })

    # Mostrar indicadores
    st.subheader("Resumen meteorologico")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Temperatura promedio",
        f"{df['Temperatura'].mean():.1f} °C"
    )

    col2.metric(
        "Humedad promedio",
        f"{df['Humedad'].mean():.1f} %"
    )

    col3.metric(
        "Precipitacion acumulada",
        f"{df['Precipitacion'].sum():.1f} mm"
    )

    # Tabla de datos
    st.subheader("Datos meteorologicos")
    st.dataframe(df, use_container_width=True)

    # Grafica de temperatura
    st.subheader("Temperatura por hora")

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.lineplot(
        data=df,
        x="Fecha",
        y="Temperatura",
        ax=ax1
    )
    ax1.set_ylabel("Temperatura (°C)")
    ax1.tick_params(axis="x", rotation=45)
    fig1.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

    # Grafica de humedad
    st.subheader("Humedad relativa")

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.lineplot(
        data=df,
        x="Fecha",
        y="Humedad",
        ax=ax2
    )
    ax2.set_ylabel("Humedad (%)")
    ax2.tick_params(axis="x", rotation=45)
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    # Grafica de precipitacion
    st.subheader("Precipitacion por hora")

    fig3, ax3 = plt.subplots(figsize=(10, 4))
    sns.barplot(
        data=df,
        x="Fecha",
        y="Precipitacion",
        color="skyblue",
        ax=ax3
    )
    ax3.set_ylabel("Precipitacion (mm)")
    ax3.set_xticks(range(0, len(df), 6))
    ax3.set_xticklabels(
        df["Fecha"].dt.strftime("%d/%m %H:%M").iloc[::6],
        rotation=45
    )
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

except (requests.RequestException, ValueError, KeyError) as error:
    st.error(f"No se pudieron obtener los datos: {error}")
