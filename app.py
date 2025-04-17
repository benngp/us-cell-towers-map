import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="US Cell Towers", layout="wide")

st.title("📡 US Cell Towers Map")

DATA_URL = "https://opendata.fcc.gov/api/views/eers-7wdv/rows.csv?accessType=DOWNLOAD"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df = df[["Registration Number", "Latitude", "Longitude", "Structure Type", "Owner Name"]]
    df.dropna(subset=["Latitude", "Longitude"], inplace=True)
    return df

df = load_data()

# Optional filter
owner_filter = st.text_input("Filter by Owner (e.g. Verizon, T-Mobile):")

if owner_filter:
    df = df[df["Owner Name"].str.contains(owner_filter, case=False, na=False)]

# Show map
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=39.5,
        longitude=-98.35,
        zoom=3.5,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position='[Longitude, Latitude]',
            get_radius=1000,
            get_fill_color=[255, 0, 0, 80],
            pickable=True,
        ),
    ],
))# us-cell-towers-map
