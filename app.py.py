import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="تقرير المبيعات", layout="wide")
st.title("📊 تقرير المبيعات اليومية")

# تحميل البيانات
try:
    df = pd.read_csv("sales.csv")
except Exception as e:
    st.error(f"❌ خطأ في تحميل الملف: {e}")
    st.stop()

# عرض أسماء الأعمدة للمراجعة
st.write("🧾 الأعمدة الحالية:")
st.write(df.columns.tolist())

# زر تحميل التقرير
st.download_button(
    label="📥 تحميل التقرير كـ CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name="تقرير_المبيعات.csv",
    mime="text/csv"
)

# مؤشرات عامة (لو الأعمدة موجودة)
if "Sales" in df.columns:
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 إجمالي المبيعات", f"{df['Sales'].sum():,.0f}")
    col2.metric("📉 متوسط المبيعات", f"{df['Sales'].mean():,.0f}")
    col3.metric("🔥 أعلى مبيعات", f"{df['Sales'].max():,.0f}")

# فلترة حسب المندوب أو المدينة (لو الأعمدة موجودة)
if "Sales Man" in df.columns and "City" in df.columns:
    with st.sidebar:
        st.header("🎯 فلترة البيانات")
        selected_salesman = st.selectbox("👤 اختر مندوب المبيعات", options=["الكل"] + sorted(df["Sales Man"].dropna().unique()))
        selected_city = st.selectbox("🏙️ اختر المدينة", options=["الكل"] + sorted(df["City"].dropna().unique()))

    filtered_df = df.copy()
    if selected_salesman != "الكل":
        filtered_df = filtered_df[filtered_df["Sales Man"] == selected_salesman]
    if selected_city != "الكل":
        filtered_df = filtered_df[filtered_df["City"] == selected_city]
else:
    filtered_df = df.copy()

# تلوين حسب نسبة المبيعات (لو العمود موجود)
def highlight_sales(val):
    try:
        val = float(str(val).replace('%', '').replace(',', ''))
        if val >= 40:
            return 'background-color: #d4f4dd'
        elif val >= 30:
            return 'background-color: #fff3cd'
        else:
            return 'background-color: #f8d7da'
    except:
        return ''

if "Sales%" in filtered_df.columns:
    styled_df = filtered_df.style.applymap(highlight_sales, subset=["Sales%"])
    st.subheader("📋 جدول المبيعات")
    st.dataframe(styled_df, use_container_width=True)
else:
    st.subheader("📋 جدول المبيعات")
    st.dataframe(filtered_df, use_container_width=True)