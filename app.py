import streamlit as st
import pandas as pd
import requests
import pydeck as pdk

st.set_page_config(page_title="FCC Cell Towers Map", layout="wide")
st.title("📡 FCC Cell Towers Map")

API_URL = "https://opendata.fcc.gov/resource/h7da-s4u2.json?$limit=1000"

@st.cache_data
def load_data():
    response = requests.get(API_URL)
    data = response.json()
    df = pd.json_normalize(data)
    st.write("Available columns:", df.columns.tolist())  # 🔍 Show all column names for debugging
    return df

df = load_data()

# Only keep rows with valid coordinates
if "latitude" in df.columns and "longitude" in df.columns:
    df = df.dropna(subset=["latitude", "longitude"])
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
else:
    st.error("Latitude/Longitude not available in data.")
    st.stop()

# Optional filter
company_col = "company" if "company" in df.columns else None
if company_col:
    company_filter = st.text_input("Filter by Company:")
    if company_filter:
        df = df[df[company_col].str.contains(company_filter, case=False, na=False)]

# Show map
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=39.5,
        longitude=-98.35,
        zoom=3.5,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position='[longitude, latitude]',
            get_radius=1000,
            get_fill_color=[0, 100, 255, 100],
            pickable=True,
        )
    ],
))

st.write("📄 Data preview:")
st.dataframe(df)
