# smart_accounting_ui.py
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="النظام المحاسبي الذكي",
    layout="wide",
    page_icon="💰"
)

# -------------------------
# واجهة التطبيق الرئيسية
# -------------------------
st.title("💼 النظام المحاسبي الذكي")
st.markdown(
    "مرحبًا بك في النظام المحاسبي الذكي. يمكنك إدارة الفواتير، المخزون، والقيود المالية بسهولة."
)

# -----------------------------------
# قاعدة بيانات مؤقتة (للاستخدام الأولي)
# -----------------------------------
people_db = []
inventory = []
journal_entries = []

# -------------------------
# تبويبات التطبيق
# -------------------------
tabs = st.tabs(["🏢 الأشخاص/المؤسسات", "📦 المخزون", "العملات ","📝 القيد المحاسبي", "📊 التقارير"])

# -------------------------
# 1️⃣ إدارة الأشخاص والمؤسسات
# -------------------------
with tabs[0]:
    st.header("🏢 إدارة الأشخاص والمؤسسات")
    with st.form("person_form"):
        name = st.text_input("الاسم")
        role = st.text_input("الصفة / الدور")
        phone = st.text_input("رقم الهاتف")
        email = st.text_input("البريد الإلكتروني")
        hi = st.text_input("العنوان")
        
        submit_person = st.form_submit_button("إضافة شخص/مؤسسة")
        if submit_person:
            person = {
                "الاسم": name,
                "الصفة": role,
                "الهاتف": phone,
                "البريد": email,
                "العنوان":hi,
            }
            people_db.append(person)
            st.success(f"تم إضافة: {name}")

    if people_db:
        st.subheader("قائمة الأشخاص/المؤسسات")
        df_people = pd.DataFrame(people_db)
        st.dataframe(df_people, use_container_width=True)

# -------------------------
# 2️⃣ إدارة الأصناف والمخزون
# -------------------------
with tabs[1]:
    st.header("📦 إدارة الأصناف والمخزون")
    with st.form("inventory_form"):
        item_name = st.text_input("اسم الصنف")
        item_type = st.text_input("نوع الصنف")
        item_price = st.number_input("سعر الوحدة", min_value=0.0, format="%.2f")
        item_quantity = st.number_input("الكمية المتوفرة", min_value=0, step=1)
        reorder_point = st.number_input("نقطة إعادة الطلب", min_value=0, step=1)
        submit_item = st.form_submit_button("إضافة صنف")
        if submit_item:
            item = {
                "الاسم": item_name,
                "النوع": item_type,
                "السعر": item_price,
                "الكمية": item_quantity,
                "نقطة إعادة الطلب": reorder_point
            }
            inventory.append(item)
            st.success(f"تم إضافة الصنف: {item_name}")

    if inventory:
        st.subheader("المخزون الحالي")
        df_inventory = pd.DataFrame(inventory)
        # تمييز المخزون المنخفض
        def highlight_reorder(row):
            return ['background-color: #ffcccc' if row["الكمية"] <= row["نقطة إعادة الطلب"] else '' for _ in row]

        st.dataframe(df_inventory.style.apply(highlight_reorder, axis=1), use_container_width=True)

# -------------------------
# 3️⃣ إدخال القيد المحاسبي
# -------------------------
with tabs[2]:
    st.header("📝 إدخال قيد محاسبي")
    with st.form("journal_form"):
        entry_date = st.date_input("التاريخ", date.today())
        entry_description = st.text_input("الوصف")
        entry_amount = st.number_input("المبلغ", min_value=0.0, format="%.2f")
        entry_account = st.selectbox("الحساب", ["النقدية", "البنك", "المبيعات", "المشتريات"])
        submit_journal = st.form_submit_button("إضافة القيد")
        if submit_journal:
            entry = {
                "التاريخ": entry_date,
                "الوصف": entry_description,
                "المبلغ": entry_amount,
                "الحساب": entry_account
            }
            journal_entries.append(entry)
            st.success(f"تم إضافة القيد: {entry_description} بمبلغ {entry_amount}")

    if journal_entries:
        st.subheader("القيود المحاسبية")
        df_journal = pd.DataFrame(journal_entries)
        st.dataframe(df_journal, use_container_width=True)

# -------------------------
# 4️⃣ التقارير المالية
# -------------------------
with tabs[3]:
    st.header("📊 التقارير المالية")
    if journal_entries:
        st.subheader("ملخص الحسابات")
        df_journal = pd.DataFrame(journal_entries)
        accounts_summary = df_journal.groupby("الحساب")["المبلغ"].sum().reset_index()
        st.dataframe(accounts_summary, use_container_width=True)
    else:
        st.info("لا توجد قيود محاسبية لعرض التقرير.")






