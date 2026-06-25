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
     (df["Product Name"]) &
    (df["Region"].isin(selected_regions)) &
    (df["Product Category"].isin(selected_categories)) &
    (df["Payment Method"].isin(selected_payment_methods))
]

# ----------
# KPI Cards
# ----------

total_revenue = filtered_df["Total Revenue"].sum()
total_units = filtered_df["Units Sold"].sum()
total_transactions = filtered_df["Transaction ID"].nunique()
average_order_value = total_revenue / total_transactions if total_transactions > 0 else 0

st.markdown(f"##### Regions selected:{selected_regions} \n Product Categories selected:{selected_categories}.")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue",f"${total_revenue:,.2f}")
col2.metric("Unit Solds",f"{total_units:,.2f}")
col3.metric("Transaction",f"{total_transactions:,}")
col4.metric("Avg. Order Value",f"{average_order_value:,.2f}")

st.divider()

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

#------------------
# Visualizations
#------------------

col5,col6 = st.columns(2)

with col5:
    revenue_by_region = (
        filtered_df.groupby("Region",as_index=False)["Total Revenue"]
        .sum()
        .sort_values("Total Revenue",ascending=False)
    )


    fig_region = px.bar(
        revenue_by_region,
        x="Region",
        y="Total Revenue",
        title="Total Revenue By Region",
        text_auto=".2s"
    )

    st.plotly_chart(fig_region,use_container_width=True)


with col6:
    revenue_by_category = (
        filtered_df.groupby("Product Category", as_index=False)["Total Revenue"]
        .sum()
        .sort_values("Total Revenue", ascending=False)
    )

    fig_category = px.pie(
        revenue_by_category,
        names="Product Category",
        values="Total Revenue",
        title="Revenue Share by Product Category"
    )
    st.plotly_chart(fig_category, use_container_width=True)


# Monthly revenue
monthly_revenue = (
    filtered_df.groupby("Month", as_index=False)["Total Revenue"]
    .sum()
    .sort_values("Month")
)

fig_monthly = px.line(
    monthly_revenue,
    x="Month",
    y="Total Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)
st.plotly_chart(fig_monthly, use_container_width=True)

col7, col8 = st.columns(2)

with col7:
    payment_revenue = (
        filtered_df.groupby("Payment Method", as_index=False)["Total Revenue"]
        .sum()
        .sort_values("Total Revenue", ascending=False)
    )

    fig_payment = px.bar(
        payment_revenue,
        x="Payment Method",
        y="Total Revenue",
        title="Revenue by Payment Method",
        text_auto=".2s"
    )
    st.plotly_chart(fig_payment, use_container_width=True)

with col8:
    top_products = (
        filtered_df.groupby("Product Name", as_index=False)["Total Revenue"]
        .sum()
        .sort_values("Total Revenue", ascending=False)
        .head(10)
    )

    fig_products = px.bar(
        top_products,
        x="Total Revenue",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Revenue",
        text_auto=".2s"
    )
    fig_products.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_products, use_container_width=True)

#-------------
# Data Table
#-------------

st.subheader("Filtered Sales Dataset")
st.dataframe(filtered_df,use_container_width=True)

#-----------------
# Insights
#-----------------

st.subheader("Key Insights")

best_region = revenue_by_region.iloc[0]["Region"]
best_category = revenue_by_category.iloc[0]["Product Category"]
best_payment = payment_revenue.iloc[0]["Payment Method"]
best_product = top_products.iloc[0]["Product Name"]

st.success(
    f"The highest revenue region is {best_region}. "
    f"The best-performing category is {best_category}. "
    f"The most used payment method by revenue is {best_payment}. "
    f"The top product by revenue is {best_product}."
)

