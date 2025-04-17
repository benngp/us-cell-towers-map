import streamlit as st
import pandas as pd
import requests
import pydeck as pdk

st.set_page_config(page_title="US Cell Towers Map", layout="wide")
st.title("📡 US Cell Towers (Live API Sample)")

@st.cache_data
def load_data():
    url = "https://opendata.fcc.gov/resource/eers-7wdv.json?$limit=1000"
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)
    df = df[["owner", "latitude", "longitude", "structure_type", "registration_number"]]
    df = df.dropna(subset=["latitude", "longitude"])
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    return df

df = load_data()

st.write(f"Showing **{len(df)}** registered tower locations (sample)")

# Optional filter by owner
owner_filter = st.text_input("Filter by Owner Name (e.g. Verizon, Crown Castle):")
if owner_filter:
    df = df[df["owner"].str.contains(owner_filter, case=False, na=False)]

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
            get_position='[longitude, latitude]',
            get_radius=1000,
            get_fill_color=[0, 0, 255, 80],
            pickable=True,
        )
    ],
))
