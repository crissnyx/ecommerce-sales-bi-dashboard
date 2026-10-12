import base64
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="E-Commerce BI Dashboard",
    page_icon="📊",
    layout="wide"
)

# 2. Load Data with Robust Column Mapping
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_sales_data.csv")
    
    # Clean column names (strip whitespace)
    df.columns = df.columns.str.strip()
    
    # Map common variations to standard names
    col_mapping = {}
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ['date', 'order date', 'fecha']:
            col_mapping[col] = 'Date'
        elif col_lower in ['region', 'región', 'location']:
            col_mapping[col] = 'Region'
        elif col_lower in ['category', 'categoria', 'categoría', 'product category']:
            col_mapping[col] = 'Category'
        elif col_lower in ['total sales', 'sales', 'revenue', 'ventas', 'amount']:
            col_mapping[col] = 'Total Sales'
        elif col_lower in ['units sold', 'units', 'quantity', 'unidades']:
            col_mapping[col] = 'Units Sold'
        elif col_lower in ['sales channel', 'channel', 'canal']:
            col_mapping[col] = 'Sales Channel'
        elif col_lower in ['cost', 'costo']:
            col_mapping[col] = 'Cost'
            
    df = df.rename(columns=col_mapping)
    
    # Ensure Date column exists and is datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    else:
        df['Date'] = pd.date_range(start='2025-01-01', periods=len(df), freq='D')
        
    # Ensure Sales and Units exist
    if 'Total Sales' not in df.columns:
        df['Total Sales'] = 100.0
    if 'Units Sold' not in df.columns:
        df['Units Sold'] = 1
        
    # Calculate Profit
    if 'Profit' not in df.columns and 'Cost' in df.columns:
        df['Profit'] = df['Total Sales'] - df['Cost']
    elif 'Profit' not in df.columns:
        df['Profit'] = df['Total Sales'] * 0.25
        
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("🔍 Filter Sales Data")

min_date = df['Date'].min().date() if not df['Date'].isna().all() else pd.to_datetime('2025-01-01').date()
max_date = df['Date'].max().date() if not df['Date'].isna().all() else pd.to_datetime('2025-12-31').date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

regions = ["All"] + sorted(df['Region'].dropna().unique().tolist()) if 'Region' in df.columns else ["All"]
selected_region = st.sidebar.selectbox("Select Region", regions)

categories = ["All"] + sorted(df['Category'].dropna().unique().tolist()) if 'Category' in df.columns else ["All"]
selected_category = st.sidebar.selectbox("Select Category", categories)

channels = ["All"] + sorted(df['Sales Channel'].dropna().unique().tolist()) if 'Sales Channel' in df.columns else ["All"]
selected_channel = st.sidebar.selectbox("Select Sales Channel", channels)

# Filter Logic
filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['Date'].dt.date >= start_date) & 
        (filtered_df['Date'].dt.date <= end_date)
    ]

if selected_region != "All" and 'Region' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

if selected_category != "All" and 'Category' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

if selected_channel != "All" and 'Sales Channel' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Sales Channel'] == selected_channel]

# 4. Header & Overview
st.title("📊 E-Commerce Business Intelligence Dashboard")
st.markdown("Interactive analytics tracking revenue, sales channels, and profit margins.")

total_revenue = filtered_df['Total Sales'].sum()
total_units = filtered_df['Units Sold'].sum()
avg_order_value = filtered_df['Total Sales'].mean() if len(filtered_df) > 0 else 0
total_profit = filtered_df['Profit'].sum() if 'Profit' in filtered_df.columns else 0
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Units Sold", f"{total_units:,}")
col3.metric("Avg Order Value (AOV)", f"${avg_order_value:,.2f}")
col4.metric("Profit Margin", f"{profit_margin:.1f}%")

st.markdown("---")

# 5. Visualizations
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("📈 Revenue Trend Over Time")
    daily_sales = filtered_df.groupby('Date')['Total Sales'].sum().reset_index()
    fig_trend = px.line(
        daily_sales, x='Date', y='Total Sales',
        labels={'Total Sales': 'Revenue ($)', 'Date': 'Date'},
        template="plotly_white"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with row1_col2:
    st.subheader("🗺️ Revenue by Region")
    if 'Region' in filtered_df.columns:
        region_sales = filtered_df.groupby('Region')['Total Sales'].sum().reset_index()
        fig_region = px.bar(
            region_sales, x='Region', y='Total Sales',
            color='Region',
            labels={'Total Sales': 'Revenue ($)'},
            template="plotly_white"
        )
        st.plotly_chart(fig_region, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("📦 Revenue by Product Category")
    if 'Category' in filtered_df.columns:
        cat_sales = filtered_df.groupby('Category')['Total Sales'].sum().reset_index()
        fig_cat = px.pie(
            cat_sales, values='Total Sales', names='Category',
            hole=0.4
        )
        st.plotly_chart(fig_cat, use_container_width=True)

with row2_col2:
    st.subheader("🛍️ Sales by Channel")
    if 'Sales Channel' in filtered_df.columns:
        channel_sales = filtered_df.groupby('Sales Channel')['Total Sales'].sum().reset_index()
        fig_channel = px.bar(
            channel_sales, x='Sales Channel', y='Total Sales',
            color='Sales Channel',
            labels={'Total Sales': 'Revenue ($)'},
            template="plotly_white"
        )
        st.plotly_chart(fig_channel, use_container_width=True)

st.markdown("---")

# 6. Raw Data View & Export Feature
st.subheader("📋 Transactional Data")
col_data, col_download = st.columns([3, 1])

with col_download:
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Data (CSV)",
        data=csv_data,
        file_name="filtered_ecommerce_sales.csv",
        mime="text/csv",
        use_container_width=True
    )

st.dataframe(filtered_df, use_container_width=True)

# 7. Executive Presentation Slides (Using 01.png to 04.png)
st.markdown("---")
st.header("📊 Executive Project Presentation")
st.markdown("Explore the key strategic insights, system architecture, and real-time business metrics below:")

c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    st.subheader("1. Project Overview")
    try:
        st.image("01.png", use_container_width=True)
    except Exception:
        st.warning("Image '01.png' not found in repository.")
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("2. Strategic Challenge & BI Solution")
    try:
        st.image("02.png", use_container_width=True)
    except Exception:
        st.warning("Image '02.png' not found in repository.")
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("3. Technical Architecture & Pillars")
    try:
        st.image("03.png", use_container_width=True)
    except Exception:
        st.warning("Image '03.png' not found in repository.")
    st.markdown("<br>", unsafe_allow_html=True)