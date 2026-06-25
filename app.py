import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

DATA_PATH = Path("data") / "online_sales_data.csv"

st.set_page_config(
    page_title="Sales Dashboard"
)
st.header("Interactive Sales Dashboard")


@st.cache_data
def laod_data():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = laod_data()

