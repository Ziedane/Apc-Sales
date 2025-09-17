import streamlit as st
import pandas as pd

# تحميل البيانات
df = pd.read_csv("sales.csv")

# عنوان الصفحة
st.title("📊 تقرير المبيعات اليومية")

# عرض البيانات
st.dataframe(df)