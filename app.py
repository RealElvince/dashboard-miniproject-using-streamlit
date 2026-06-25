import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

DATA_PATH = Path("data") / "online_sales_data.csv"

st.set_page_config(
    page_title="Sales Dashboard"
)
st.header("Interactive Sales Dashboard")
st.write(
    "This dashboard uses the uploaded online sales dataset to analyze revenue, units sold, "
    "product categories, regions, payment methods, and sales trends."
)

@st.cache_data
def laod_data():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = laod_data()

#---------------
# sidebar filers
#---------------

st.sidebar.header("Filter Data")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date,max_date),
    min_value=min_date,
    max_value=max_date
)

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Regions"].unique()),
    default=sorted(df["Regions"].unique())
)

selected_categories = st.sidebar.multiselect(
    "Select Product Category",
    options=sorted(df["Product Category"].unique()),
    default=sorted(df["Product Category"].unique())
)

selected_payment_methods = st.sidebar.multiselect(
    "Select Payment Method",
    options=sorted(df["Payment Method"].unique()),
    default=sorted(df["Payment Method"].unique())
)

# Handle Date Filtering safely

if len(date_range) == 2:
    start_date,end_date = date_range
else:
    start_date, end_date = min_date, max_date


filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date) &
    (df["Region"].isin(selected_regions)) &
    (df["Product Category"].isin(selected_categories)) &
    (df["Payment Method"].isin(selected_payment_methods))
]
