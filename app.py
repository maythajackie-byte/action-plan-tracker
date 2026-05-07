pythonimport streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan Tracker AI", layout="wide")

# ไฟล์สำหรับเก็บข้อมูล
DATA_FILE = "action_plan_data.csv"

# ฟังก์ชันโหลดข้อมูล
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Job Name", "Category", "Status", "Progress", "Deadline"])

# ฟังก์ชันบันทึกข้อมูล
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# โหลดข้อมูลปัจจุบัน
df = load_data()

st.title("🚀 Action Plan & Performance Dashboard")
st.markdown("---")

# --- ส่วนที่ 1: การกรอกข้อมูล (Input Section) ---
with st.sidebar:
    st.header("➕ เพิ่ม/แก้ไขแผนงาน")
    with st.form("input_form", clear_on_submit=True):
        job_name = st.text_input("ชื่องาน / โปรเจกต์")
        category = st.selectbox("หมวดหมู่", ["ประเมินทีม", "PIP", "วางแผนกลยุทธ์", "อื่นๆ"])
        status = st.selectbox("สถานะ", ["Not Started", "In Progress", "Stuck", "Completed"])
        progress = st.slider("ความคืบหน้า (%)", 0, 100, 50)
        deadline = st.date_input("วันครบกำหนด")
        
        submit_button = st.form_submit_button(label="บันทึกข้อมูล")

    if submit_button and job_name:
        new_data = pd.DataFrame([[job_name, category, status, progress, deadline]], 
                                columns=["Job Name", "Category", "Status", "Progress", "Deadline"])
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success("บันทึกเรียบร้อย!")

# --- ส่วนที่ 2: สรุปผลตัวเลข (Metric Section) ---
if not df.empty:
    col1, col2, col3 = st.columns(3)
    avg_progress = df["Progress"].mean()
    total_tasks = len(df)
    completed_tasks = len(df[df["Status"] == "Completed"])

    col1.metric("งานทั้งหมด", f"{total_tasks} รายการ")
    col2.metric("ความคืบหน้าเฉลี่ย", f"{avg_progress:.1f}%")
    col3.metric("เสร็จสมบูรณ์", f"{completed_tasks} รายการ")

    st.markdown("---")

    # --- ส่วนที่ 3: กราฟแสดงผล (Visualization Section) ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📊 ความคืบหน้ารายงาน")
        fig_bar = px.bar(df, x="Job Name", y="Progress", color="Status", 
                         text="Progress", range_y=[0,100],
                         color_discrete_map={"Completed":"#2ecc71", "In Progress":"#f1c40f", "Stuck":"#e74c3c", "Not Started":"#95a5a6"})
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("📋 สัดส่วนสถานะงาน")
        fig_pie = px.pie(df, names="Status", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- ส่วนที่ 4: ตารางข้อมูล (Data Table) ---
    st.subheader("🔍 รายละเอียดงานทั้งหมด")
    st.dataframe(df, use_container_width=True)
    
    # ปุ่มดาวน์โหลดข้อมูล
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 ดาวน์โหลดข้อมูลเป็น CSV (Excel)", csv, "action_plan.csv", "text/csv")
else:
    st.info("ยังไม่มีข้อมูล กรุณากรอกข้อมูลที่แถบด้านซ้ายมือครับ")
