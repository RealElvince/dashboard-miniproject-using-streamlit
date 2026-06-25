import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

DATA_PATH = Path("data") / "online_sales_data.csv"

st.set_page_config(
    page_title="Sales Dashboard"
)
st.header("Interactive Sales Dashboard")

