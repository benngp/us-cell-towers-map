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

    # Rename to match what we need for mapping
    df = df.rename(columns={
        "latitude_decimal": "lat",
        "longitude_decimal": "lon",
        "call_sign": "Call Sign",
        "call_sign_licensee_name": "Licensee"
    })

    # Drop rows without valid coordinates
    df = df.dropna(subset=["lat", "lon"])
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)

    return df

df = load_data()

st.write(f"Showing **{len(df)}** tower records")

# Optional filter by Licensee
licensee_filter = st.text_input("Filter by Licensee (company name):")
if licensee_filter:
    df = df[df["Licensee"].str.contains(licensee_filter, case=False, na=False)]

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
            get_position='[lon, lat]',
            get_radius=1000,
            get_fill_color=[0, 100, 255, 100],
            pickable=True,
        )
    ],
))

# Optional table
with st.expander("🔎 Raw Data Table"):
    st.dataframe(df)
