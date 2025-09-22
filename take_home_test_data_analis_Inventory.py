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
fig1 = px.line(rev_year, x='year', y='revenue', markers=True, title="Revenue Trend by Year")
st.plotly_chart(fig1, use_container_width=True)

# 1) Total revenue keseluruhan
print("TOTAL revenue (sold_df):", sold_df['revenue'].sum())

# 2) Revenue per category (top 20, tanpa head cut)
rev_cat_all = sold_df.groupby('product_category', dropna=False)['revenue'].sum().reset_index()
rev_cat_all = rev_cat_all.sort_values('revenue', ascending=False)
print(rev_cat_all.head(20))

# 3) Cek jumlah baris, duplicates, nulls
print("rows:", len(sold_df))
print("nulls in revenue:", sold_df['revenue'].isna().sum())
print("nulls in category:", sold_df['product_category'].isna().sum())

# 4) Cek apakah revenue dihitung price * qty vs kolom revenue
if all(col in sold_df.columns for col in ['price','quantity']):
    calc_sum = (sold_df['price'] * sold_df['quantity']).sum()
    print("SUM(price*quantity):", calc_sum)
    print("SUM(revenue):", sold_df['revenue'].sum())
else:
    print("Kolom price/quantity tidak ada — lewati cek ini.")

# 5) Normalisasi nama kategori (whitespace/case)
cats = sold_df['product_category'].astype(str).str.strip().str.lower().value_counts().head(50)
print("Top categories (normalized):")
print(cats)

# 6) Bandingkan dengan file yang dipakai Power BI (jika kamu punya path)
# df_powerbi = pd.read_csv('powerbi_export.csv')  # contoh; load file yang sama seperti di Power BI
# print(df_powerbi.groupby('product_category')['revenue'].sum().sort_values(ascending=False).head(20))

# 7) Cari baris yang mungkin double counted (contoh sederhana)
dup_keys = ['order_id','transaction_id']  # ganti sesuai kolom unik di datasetmu
for k in dup_keys:
    if k in sold_df.columns:
        dups = sold_df.duplicated(subset=[k], keep=False).sum()
        print(f"duplicates by {k}:", dups)
# =====================
# Revenue by Product Name (Top 10)
# =====================
rev_prod = sold_df.groupby('product_name')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(10)
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





