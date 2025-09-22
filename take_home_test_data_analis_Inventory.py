import streamlit as st
import pandas as pd

df = pd.read_parquet("inventory_clean.parquet")
st.write(df.head())





