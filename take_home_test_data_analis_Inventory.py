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

def map_product_group(cat):
    if cat in ["Outerwear & Coats", "Fashion Hoodies & Sweatshirts"]:
        return "Sweaters"
    elif cat in ["Active", "Shorts"]:
        return "Tops & Tees"
    elif cat in ["Pants & Capris", "Jeans"]:
        return "Pants"
    elif cat in ["Suits", "Blazers & Jackets", "Jumpsuits & Rompers"]:
        return "Suits & Sport Coats"
    else:
        return cat

df["product_group"] = df["product_category"].apply(map_product_group)

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
fig1 = px.line(rev_year, x='year', y='revenue', markers=True, title="Revenue Trend by Year")
st.plotly_chart(fig1, use_container_width=True)

# =====================
# Revenue by Product Category
# =====================

check_rev_group = (
    df[df["sold_flag"] == 1]
    .groupby("product_group")["product_retail_price"]
    .sum()
    .reset_index()
    .sort_values("product_retail_price", ascending=False)
    .head(10)
)

fig2 = px.bar(
    check_rev_group,
    x="product_group",
    y="product_retail_price",
    title="Revenue by Product Category",
    text_auto=".2s"
)
st.plotly_chart(fig2, use_container_width=True)


# =====================
# Revenue by Product Name
# =====================
rev_prod = sold_df.groupby('product_name')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
fig3 = px.bar(rev_prod, x='revenue', y='product_name', orientation='h', title="Revenue by Product Name")
st.plotly_chart(fig3, use_container_width=True)

# =====================
# Brand Performance Table
# =====================
brand_perf = sold_df.groupby('product_brand').agg(
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





