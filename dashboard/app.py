import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.set_page_config(
    page_title="E-commerce User Growth Analytics",
    layout="wide"
)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


rfm = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "rfm_customer_segments.csv"
    )
)

customers = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "data",
        "raw",
        "olist_customers_dataset.csv"
    )
)


customer_state = customers[
    [
        "customer_unique_id",
        "customer_state"
    ]
]


rfm = rfm.merge(
    customer_state,
    on="customer_unique_id",
    how="left"
)
orders = pd.read_csv(
    os.path.join(
        BASE_DIR,
        "data",
        "raw",
        "olist_orders_dataset.csv"
    )
)
st.title(
    "🛒 E-commerce User Growth Analytics Dashboard"
)
st.markdown(
"""
### Project Overview

This dashboard analyzes customer behavior,
purchase patterns and user value segmentation
using RFM analysis.

**Techniques:**
- Customer Behavior Analysis
- Order Growth Analysis
- RFM Customer Segmentation
- Customer Retention Insights

"""
)
# KPI

total_customers = customers["customer_unique_id"].nunique()

total_orders = orders.shape[0]


col1, col2, col3 = st.columns(3)
avg_orders = (
    total_orders /
    total_customers
)

with col1:
    st.metric(
        "Total Customers",
        total_customers
    )


with col2:
    st.metric(
        "Total Orders",
        total_orders
    )
    # Monthly Order Growth Analysis

with col3:
    st.metric(
        "Avg Orders per Customer",
        round(avg_orders,2)
    )

st.subheader(
    "📈 Monthly Order Growth Trend"
)


orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)


orders["order_month"] = (
    orders["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)


monthly_orders = (
    orders
    .groupby("order_month")
    .size()
    .reset_index(name="orders")
)


fig = px.line(
    monthly_orders,
    x="order_month",
    y="orders",
    markers=True,
    title="Monthly Order Growth Trend"
)


fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Orders"
)


st.plotly_chart(
    fig,
    use_container_width=True
)
# Customer Segment Filter

st.sidebar.header(
    "Customer Filter"
)
state_options = [
    "All"
] + sorted(
    rfm["customer_state"]
    .dropna()
    .unique()
)


selected_state = st.sidebar.selectbox(
    "Select Customer State",
    state_options
)
segment_options = [
    "All"
] + list(
    rfm["Customer_Segment"].unique()
)


selected_segment = st.sidebar.selectbox(
    "Select Customer Segment",
    segment_options
)

filtered_rfm = rfm.copy()


if selected_segment != "All":
    filtered_rfm = filtered_rfm[
        filtered_rfm["Customer_Segment"]
        == selected_segment
    ]


if selected_state != "All":
    filtered_rfm = filtered_rfm[
        filtered_rfm["customer_state"]
        == selected_state
    ]
# Customer Segmentation Analysis

st.subheader(
    "👥 Customer Segmentation Analysis"
)

# Customer Segment Distribution

segment_count = (
    filtered_rfm["Customer_Segment"]
    .value_counts()
    .reset_index()
)


segment_count.columns = [
    "Customer_Segment",
    "Count"
]


segment_count["Percentage"] = (
    segment_count["Count"]
    /
    segment_count["Count"].sum()
    *
    100
)


fig = px.bar(
    segment_count,
    x="Customer_Segment",
    y="Count",
    text="Percentage",
    title="Customer Segment Distribution",
    labels={
        "Customer_Segment": "Customer Segment",
        "Count": "Number of Customers"
    }
)


fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)


st.plotly_chart(
    fig,
    use_container_width=True
)
# RFM KPI Analysis
# RFM Customer Value Scatter Plot

st.subheader(
    "💎 Customer Value Analysis"
)
st.caption(
"""
Customer Segments:
🏆 Champions - High value customers
❤️ Loyal Customers - Regular buyers
⚠️ At Risk - Potential churn customers
💤 Lost Customers - Inactive customers
"""
)

rfm_scatter = filtered_rfm.copy()


fig = px.scatter(
    rfm_scatter,
    x="Frequency",
    y="Monetary",
    color="Customer_Segment",
    hover_data=[
        "Recency",
        "Frequency",
        "Monetary"
    ],
    title="RFM Customer Value Distribution",
    labels={
        "Frequency": "Purchase Frequency",
        "Monetary": "Customer Spending"
    }
)


st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader(
    "📊 RFM Customer Value Overview"
)

champions = len(
    filtered_rfm[filtered_rfm["Customer_Segment"] == "Champions"]
)

at_risk = len(
    filtered_rfm[filtered_rfm["Customer_Segment"] == "At Risk"]
)

loyal = len(
    filtered_rfm[filtered_rfm["Customer_Segment"] == "Loyal Customers"]
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total RFM Customers",
        len(filtered_rfm)
    )

with col2:
    st.metric(
        "Champions",
        champions
    )

with col3:
    st.metric(
        "At Risk Customers",
        at_risk
    )
    # Business Insights

st.subheader(
    "💡 Business Insights & Recommendations"
)

st.markdown(
"""
### 🏆 Champions Customers
- Maintain relationship with VIP benefits
- Provide exclusive promotions
- Encourage repeat purchases


### ❤️ Loyal Customers
- Increase engagement through loyalty programs
- Recommend related products


### ⚠️ At Risk Customers
- Launch retention campaigns
- Provide personalized discounts


### 💤 Lost Customers
- Analyze churn reasons
- Evaluate reactivation cost

"""
)