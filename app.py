import streamlit as st
import pandas as pd
import requests
import pydeck as pdk

st.set_page_config(page_title="FCC Cell Towers", layout="wide")
st.title("📡 FCC Cell Towers Map")

@st.cache_data
def load_data():
    url = "https://opendata.fcc.gov/resource/h7da-s4u2.json?$limit=1000"
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)

    # Rename and clean
    df = df.rename(columns={
        "latitude": "lat",
        "longitude": "lon",
        "company": "Company",
        "market": "Market",
        "channel": "Channel",
        "callsign": "Callsign"
    })

    df = df[["lat", "lon", "Company", "Market", "Channel", "Callsign"]]
    df = df.dropna(subset=["lat", "lon"])
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)
    return df

df = load_data()

# Optional company filter
company_filter = st.text_input("Filter by Company (e.g. AT&T, Verizon):")
if company_filter:
    df = df[df["Company"].str.contains(company_filter, case=False, na=False)]

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
            get_position='[lon, lat]',
            get_radius=1000,
            get_fill_color=[0, 100, 255, 100],
            pickable=True,
        )
    ],
))

# Optional table preview
with st.expander("See Raw Data Table"):
    st.dataframe(df)
