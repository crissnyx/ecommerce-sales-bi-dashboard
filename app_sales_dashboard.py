import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="E-Commerce Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Modern dark UI styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('ecommerce_sales_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None or df.empty:
    st.error("⚠️ The dataset 'ecommerce_sales_data.csv' was not found. Please run 'generate_sales_data.py' first.")
    st.stop()

# --- HEADER ---
st.title("📊 E-Commerce & Global Sales Business Intelligence Dashboard")
st.markdown("Comprehensive BI solution designed for tracking revenue performance, customer behavior, and product category trends.")
st.markdown("---")

# --- SIDEBAR (FILTERS) ---
st.sidebar.header("🔍 Global Filters")

min_date = df['date'].min().date()
max_date = df['date'].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

categories_list = ['All'] + list(df['category'].unique())
selected_category = st.sidebar.selectbox("Product Category", categories_list)

regions_list = ['All'] + list(df['region'].unique())
selected_region = st.sidebar.selectbox("Sales Region", regions_list)

# Apply filters
df_filtered = df.copy()
if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df_filtered[(df_filtered['date'].dt.date >= start_date) & (df_filtered['date'].dt.date <= end_date)]

if selected_category != 'All':
    df_filtered = df_filtered[df_filtered['category'] == selected_category]

if selected_region != 'All':
    df_filtered = df_filtered[df_filtered['region'] == selected_region]

# --- KPI CALCULATIONS ---
total_revenue = df_filtered['revenue'].sum()
total_units = df_filtered['quantity'].sum()
avg_ticket = df_filtered['revenue'].mean() if len(df_filtered) > 0 else 0
total_transactions = len(df_filtered)

# --- TOP METRIC CARDS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="💰 Total Revenue", value=f"$ {total_revenue:,.2f}")
with col2:
    st.metric(label="📦 Units Sold", value=f"{total_units:,}")
with col3:
    st.metric(label="🛒 Average Order Value", value=f"$ {avg_ticket:,.2f}")
with col4:
    st.metric(label="📋 Transactions", value=f"{total_transactions:,}")

st.markdown("---")

# --- ANALYTICAL CHARTS ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("📈 Historical Revenue Trend")
    if not df_filtered.empty:
        df_temporal = df_filtered.groupby(df_filtered['date'].dt.to_period('M'))['revenue'].sum().reset_index()
        df_temporal['date'] = df_temporal['date'].dt.to_timestamp()
        
        fig_line = px.line(
            df_temporal, 
            x='date', 
            y='revenue', 
            markers=True,
            template='plotly_dark',
            labels={'date': 'Month', 'revenue': 'Total Revenue (USD)'}
        )
        fig_line.update_traces(line_color='#00d2ff', line_width=3)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No data available for the selected range.")

with row1_col2:
    st.subheader("🏆 Top Categories by Revenue")
    if not df_filtered.empty:
        df_cat = df_filtered.groupby('category')['revenue'].sum().reset_index().sort_values(by='revenue', ascending=True)
        
        fig_bar = px.bar(
            df_cat,
            x='revenue',
            y='category',
            orientation='h',
            template='plotly_dark',
            color='revenue',
            color_continuous_scale='blues',
            labels={'revenue': 'Total Revenue (USD)', 'category': ''}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No data available.")

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("🌍 Sales Distribution by Region")
    if not df_filtered.empty:
        df_reg = df_filtered.groupby('region')['revenue'].sum().reset_index()
        fig_pie = px.pie(
            df_reg,
            names='region',
            values='revenue',
            hole=0.4,
            template='plotly_dark'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No data available.")

with row2_col2:
    st.subheader("📋 Recent Transactions Detail")
    if not df_filtered.empty:
        df_table = df_filtered[['date', 'product', 'category', 'quantity', 'revenue', 'region', 'sales_channel']].sort_values(by='date', ascending=False)
        st.dataframe(df_table.head(10), use_container_width=True)
    else:
        st.info("No transactions recorded.")