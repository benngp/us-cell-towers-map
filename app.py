import streamlit as st
import pandas as pd

st.set_page_config(page_title="US Cell Towers (Demo)", layout="wide")
st.title("📡 US Cell Towers Map (Sample Data Demo)")

# Small CSV file that works on Streamlit Cloud
DATA_URL = "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/people/people-100.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df = df[["First Name", "Last Name", "Email"]]
    return df

df = load_data()

st.write("✅ Data Loaded! Here's a preview:")
st.dataframe(df)

# Optional filter by first name
filter_name = st.text_input("Filter by First Name:")

if filter_name:
    filtered_df = df[df["First Name"].str.contains(filter_name, case=False, na=False)]
    st.write(f"Showing results for: **{filter_name}**")
    st.dataframe(filtered_df)
else:
    st.write("Showing full dataset")
