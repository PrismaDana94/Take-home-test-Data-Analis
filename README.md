# Take-home Test – Sales & Profit Performance Dashboard

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-brightgreen)](https://onky-pradana-take-home-test-inventory.streamlit.app/)

## Project Overview

Proyek ini berfokus pada pembuatan **dashboard interaktif dengan Streamlit** untuk menganalisis **performa penjualan, profit, dan inventory** pada data retail.
Dashboard ini membantu mengidentifikasi **produk, kategori, dan brand unggulan**, serta mendeteksi **ketidakefisienan stok (overstock vs sold items)** untuk mendukung pengambilan keputusan bisnis berbasis data.

---

## Dataset

Dataset yang digunakan merupakan **inventory retail data** yang telah dibersihkan dan disimpan dalam format Parquet.

Dataset yang digunakan diambil langsung dari repo ini:  
[`inventory_clean.parquet`](./inventory_clean.parquet)

Beberapa kolom penting:
- `sold_at` → tanggal produk terjual  
- `product_retail_price` → harga jual produk  
- `cost` → biaya produk  
- `product_category` → kategori produk  
- `product_brand` → brand produk  

---

## 🚀 Dashboard Workflow
1. **Data Loading** → membaca dataset inventory.  
2. **Data Preparation** → perhitungan revenue, profit, sold items, dan inventory on hand.  
3. **EDA** → analisis tren revenue, kategori, produk, dan brand.  
4. **Visualization** → KPI cards, line chart, bar chart, dan tabel performa brand.  
5. **Insights & Recommendations** → ringkasan temuan utama dan rekomendasi bisnis.

---

## 📈 Dashboard Features
- **KPI Cards** – Total Revenue, Total Profit, Sold Items, Inventory On Hand  
- **Revenue Trend** – tren revenue tahunan  
- **Top Categories & Products** – analisis kontribusi revenue  
- **Brand Performance Table** – revenue, profit, dan profit margin  
- **Insights & Recommendations** – ringkasan hasil analisis  

🔗 **Live App** → https://onky-pradana-take-home-test-inventory.streamlit.app/

---

## 🛠️ Tech Stack
- Python (Pandas)  
- Streamlit – dashboard interaktif  
- Plotly – visualisasi data  
- GitHub – version control & deployment  

---

## 📌 Key Insights
- ±64% inventory belum terjual → indikasi **overstock**.  
- Revenue 2024 turun signifikan dibanding 2023.  
- Kategori dengan revenue tertinggi: **Outerwear & Coats, Jeans, Sweaters**.  
- Brand dengan profit margin tertinggi: **Tommy Hilfiger, The North Face, Columbia**.

---

## 📂 Main Files
- `inventory_clean.parquet` – dataset inventory  
- `take_home_test_data_analis_Inventory.py` – Streamlit dashboard  
- `requirements.txt` – dependencies  

---

## 📬 Author
👤 **Onky Prisma Pradana**  
- 💼 LinkedIn: https://www.linkedin.com/in/prisma-dana/  
- 🐙 GitHub: https://github.com/PrismaDana94  

---

✨ Feel free to fork & explore this repo!  
Jika ada pertanyaan atau saran, silakan open issue di repo ini.
