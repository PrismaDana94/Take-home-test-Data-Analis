import streamlit as st
import pandas as pd
import plotly.express as px
import gdown
import os
# =====================
# Judul Aplikasi
# =====================
st.set_page_config(page_title="Sales & Profit Dashboard", layout="wide")
st.title("📊 Sales and Profit Performance Dashboard")
st.markdown("Analisis inventory dan penjualan untuk mendapatkan insight actionable")

# =====================
# Load Data
# =====================
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1DBbnyF4AvHJQqj6JdfM3IOoH9lCwaoRj"
    output = "inventory_clean.parquet"
    
    # Download file kalau belum ada di local
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    
    df = pd.read_parquet(output)
    return df

df = load_data()

# =====================
# Data Preparation
# =====================
df['sold_at'] = pd.to_datetime(df['sold_at'], errors='coerce')
df['year'] = df['sold_at'].dt.year
df['revenue'] = df['product_retail_price']
df['profit'] = df['product_retail_price'] - df['cost']
df['sold_flag'] = df['sold_at'].notna().astype(int)

# Dataset hanya produk yang terjual
sold_df = df[df['sold_flag'] == 1].copy()


# =====================
# KPI Cards
# =====================
total_revenue = sold_df['revenue'].sum()
total_profit = sold_df['profit'].sum()
sold_count = sold_df['sold_flag'].sum()
inventory_on_hand = len(df) - sold_count

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"{total_revenue/1e6:.2f}M")
col2.metric("Total Profit", f"{total_profit/1e6:.2f}M")
col3.metric("Sold Items", f"{sold_count:,}")
col4.metric("Inventory On Hand", f"{inventory_on_hand:,}")

# =====================
# Revenue Trend by Year
# =====================
rev_year = sold_df.groupby('year')['revenue'].sum().reset_index()

fig1 = px.line(
    rev_year,
    x='year',
    y='revenue',
    markers=True,
    title="Revenue Trend by Year",
    text='revenue'   
)

# Format angka biar singkat, dan posisikan di atas titik
fig1.update_traces(texttemplate='%{text:.2s}', textposition='top center')

st.plotly_chart(fig1, use_container_width=True)


# =====================
# Revenue by Category
# =====================
rev_cat = (
    sold_df.groupby('product_category')["revenue"]
    .sum()
    .reset_index()
    .sort_values('revenue', ascending=False)
    .head(10)
)

fig2 = px.bar(
    rev_cat,
    x='revenue',
    y='product_category',
    orientation='h',
    title="Top 10 Revenue by Product Category",
    text_auto=".2s"   # <--- angka otomatis di dalam bar
)

st.plotly_chart(fig2, use_container_width=True)



# =====================
# Revenue by Product Name (Top 10)
# =====================
rev_prod = (
    sold_df.groupby('product_name')["product_retail_price"]
    .sum()
    .reset_index()
    .sort_values('product_retail_price', ascending=False)
    .head(10)
)

fig3 = px.bar(
    rev_prod,
    x='product_retail_price',
    y='product_name',
    orientation='h',
    title="Top 10 Revenue by Product Name",
    text_auto=".2s"
)
st.plotly_chart(fig3, use_container_width=True)

# =====================
# Brand Performance Table
# =====================
brand_perf = sold_df.groupby('product_brand').agg(
    Total_Revenue=('revenue','sum'),
    Total_Profit=('profit','sum')
).reset_index()
brand_perf['Profit_Margin'] = (brand_perf['Total_Profit']/brand_perf['Total_Revenue']*100).round(2)

st.subheader("Top 10 Brand Performance")
st.dataframe(brand_perf.sort_values('Total_Revenue', ascending=False).head(10))


# Insights 
st.subheader("📊 Insights")
st.error("""
- Mayoritas produk *belum terjual* (±64%) → potensi overstock.  
- *Revenue 2024 turun -89% YoY* dibanding 2023 → indikasi masalah supply chain atau demand musiman.  
- *Jeans, Outerwear & Coats, Sweaters* = kategori revenue terbesar.  
- *Zoot* dominan di sisi revenue; *Zumba Fitness* unggul di profit margin (>50%).  
- Produk cepat laku: *clothing sets, skirts, leggings* (<30 hari).  
- Produk lambat: *suits & jumpsuits* (>30 hari).  
""")

# Recommendations 
st.subheader("✅ Recommendations")
st.success("""
1. *Pulihkan Revenue 2024* → investigasi supply chain, tren musiman, dan pricing strategy; jalankan kampanye marketing berbasis data.  
2. *Optimalkan Produk Unggulan* → fokus promosi Sweaters & produk Zoot; rancang kampanye musiman.  
3. *Perkuat Brand Margin Tinggi* → dorong Zumba Fitness, Zulu, LAX (margin >50%) lewat bundling & campaign eksklusif.  
4. *Manajemen Inventory Data-Driven* → sesuaikan stok sesuai siklus permintaan, gunakan reorder point & clearance promo


