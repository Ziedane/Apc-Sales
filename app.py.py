import streamlit as st
import pandas as pd

# تحميل البيانات
df = pd.read_csv("sales.csv")

# معالجة الأعمدة لو فيها مشاكل أسماء مكررة
df.columns = ["Sales Man", "City", "Sales Target", "Sales", "Sales%", "Customer", "Customer_Actual", "Customer%"]

# عنوان الصفحة
st.set_page_config(page_title="تقرير المبيعات", layout="wide")
st.title("📊 تقرير المبيعات اليومية")

# زر تحميل التقرير
st.download_button(
    label="📥 تحميل التقرير كـ CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name="تقرير_المبيعات.csv",
    mime="text/csv"
)

# مؤشرات عامة
col1, col2, col3 = st.columns(3)
col1.metric("📈 إجمالي المبيعات", f"{df['Sales'].sum():,.0f}")
col2.metric("📉 متوسط المبيعات", f"{df['Sales'].mean():,.0f}")
col3.metric("🔥 أعلى مبيعات", f"{df['Sales'].max():,.0f}")

# فلترة حسب المندوب أو المدينة
salesmen = df["Sales Man"].unique()
cities = df["City"].unique()

with st.sidebar:
    st.header("🎯 فلترة البيانات")
    selected_salesman = st.selectbox("👤 اختر مندوب المبيعات", options=["الكل"] + list(salesmen))
    selected_city = st.selectbox("🏙️ اختر المدينة", options=["الكل"] + list(cities))

# تطبيق الفلتر
filtered_df = df.copy()
if selected_salesman != "الكل":
    filtered_df = filtered_df[filtered_df["Sales Man"] == selected_salesman]
if selected_city != "الكل":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

# تلوين حسب نسبة المبيعات
def highlight_sales(val):
    try:
        val = float(str(val).replace('%', '').replace(',', ''))
        if val >= 40:
            return 'background-color: #d4f4dd'  # أخضر فاتح
        elif val >= 30:
            return 'background-color: #fff3cd'  # أصفر
        else:
            return 'background-color: #f8d7da'  # أحمر فاتح
    except:
        return ''

styled_df = filtered_df.style.applymap(highlight_sales, subset=["Sales%"])

# عرض الجدول
st.subheader("📋 جدول المبيعات")
st.dataframe(styled_df, use_container_width=True)