import streamlit as st
import pandas as pd
import plotly.express as px

# =====================
# Judul Aplikasi
# =====================
st.set_page_config(page_title="Sales & Profit Dashboard", layout="wide")
st.title("📊 Sales and Profit Performance Dashboard")
st.markdown("Analisis inventory dan penjualan untuk mendapatkan insight actionable")

# =====================
# Load Data
# =====================
# Pastikan file inventory_clean.parquet ada di repo / path yang sesuai
df = pd.read_parquet("inventory_clean.parquet")

# Konversi kolom tanggal
df['sold_at'] = pd.to_datetime(df['sold_at'], errors='coerce')

# Buat kolom turunan
df['year'] = df['sold_at'].dt.year
df['revenue'] = df['product_retail_price']
df['profit'] = df['product_retail_price'] - df['cost']
df['sold_flag'] = df['sold_at'].notna().astype(int)

# =====================
# KPI Cards
# =====================
total_revenue = df['revenue'].sum()
total_profit = df['profit'].sum()
sold_count = df['sold_flag'].sum()
inventory_on_hand = len(df) - sold_count

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"{total_revenue/1e6:.2f}M")
col2.metric("Total Profit", f"{total_profit/1e6:.2f}M")
col3.metric("Sold Items", f"{sold_count:,}")
col4.metric("Inventory On Hand", f"{inventory_on_hand:,}")

# =====================
# Revenue Trend by Year
# =====================
rev_year = df.groupby('year')['revenue'].sum().reset_index()
fig1 = px.line(rev_year, x='year', y='revenue', markers=True, title="Revenue Trend by Year")
st.plotly_chart(fig1, use_container_width=True)

# =====================
# Revenue by Category
# =====================
rev_cat = df.groupby('product_category')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(10)
fig2 = px.bar(rev_cat, x='revenue', y='product_category', orientation='h', title="Revenue by Product Category")
st.plotly_chart(fig2, use_container_width=True)

# =====================
# Revenue by Product Name (Top 10)
# =====================
rev_prod = df.groupby('product_name')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(10)
fig3 = px.bar(rev_prod, x='revenue', y='product_name', orientation='h', title="Revenue by Product Name")
st.plotly_chart(fig3, use_container_width=True)

# =====================
# Brand Performance Table
# =====================
brand_perf = df.groupby('product_brand').agg(
    Total_Revenue=('revenue','sum'),
    Total_Profit=('profit','sum')
).reset_index()
brand_perf['Profit_Margin'] = (brand_perf['Total_Profit']/brand_perf['Total_Revenue']*100).round(2)

st.subheader("Brand Performance")
st.dataframe(brand_perf.sort_values('Total_Revenue', ascending=False).head(10))

# Insights 
st.subheader("📊 Insights")
st.error("""
- Mayoritas produk **belum terjual** (64%), potensi overstock.  
- **Revenue 2024 turun drastis -89% YoY** dibanding 2023 → indikasi masalah supply chain / demand.  
- **Sweaters, Suits & Sport Coats, Swim** = kontributor revenue terbesar.  
- **Zoot** dominan dari sisi revenue, **Zumba Fitness** unggul di profit margin.  
- Produk cepat laku: **clothing sets, skirts, leggings** (<30 hari).  
- Produk lambat: **suits & jumpsuits** (>30 hari).  
""")

# Recommendations 
st.subheader("✅ Recommendations")
st.success("""
1. **Investigasi Penurunan 2024** → analisis supply chain, demand seasonal, dan pricing strategy.  
2. **Optimalkan Top Sellers** → fokus promosi Sweaters & produk Zoot.  
3. **Perkuat Brand Margin Tinggi** → dorong Zumba Fitness, Zulu, LAX (margin >50%) lewat bundling & campaign.  
4. **Inventory Management Data-Driven** → gunakan reorder point & clearance promo untuk slow-moving items.  
""")





