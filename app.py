import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from streamlit_calendar import calendar
import plotly.express as px
import io

# =====================================================================
# 📦 ส่วนที่ 1: ตั้งค่าระบบหลัก & CSS ตกแต่งหน้าตา (Configuration & Styling)
# =====================================================================
st.set_page_config(page_title="Engineer Workload Tracker", layout="wide", page_icon="📋")

# ปรับสีพื้นหลังและสไตล์แบบยั่งยืน (ไม่ใช้ Triple Quotes เพื่อป้องกัน Error)
css = "<style>"
css += ".stApp { background-color: #f4f6f9; }"
css += "h1, h2, h3 { color: #2c3e50; font-family: sans-serif; }"
css += ".eng-card { background-color: #ffffff; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.08); border-top: 4px solid #3498db; margin-bottom: 15px; }"
css += ".eng-name { font-size: 16px; font-weight: bold; color: #2c3e50; }"
css += ".eng-stat { font-size: 13px; color: #7f8c8d; margin-top: 5px; }"
css += "</style>"
st.markdown(css, unsafe_allow_html=True)

st.title("📋 Engineer Workload & Schedule Tracker")
st.markdown("ระบบบริหารแผนงานประจำปี (สไตล์ Dashboard)")

# =====================================================================
# 🗄️ ส่วนที่ 2: ข้อมูลโครงสร้าง (Master Data)
# =====================================================================
TEAMS = ["Production Team", "Cinema Engineer", "Pro-AV Engineer", "Post Production Engineer", "Broadcast Engineer", "Residential Engineer"]
TASK_CATEGORIES = ["Maintenance (Bangkok)", "Maintenance (Outside)", "Service (Bangkok)", "Project (Bangkok)", "Training", "Event/Show"]
PROJECT_STAGES = ["P0: Pitch", "P1: Build up", "P2: Installation", "P3: After Sales"]
LEAVE_OPTIONS = ["PL: ลากิจ", "VL: ลาพักร้อน", "SL: ลาป่วย", "LVP: ลาไม่รับค่าจ้าง"]
STAGE_COLORS = {"P0": "#F1C40F", "P1": "#E67E22", "P2": "#3498DB", "P3": "#2ECC71", "PL": "#95A5A6", "VL": "#9B59B6", "SL": "#E74C3C", "LVP": "#34495E"}

if "employee_roster" not in st.session_state:
    st.session_state.employee_roster = pd.DataFrame([{"ชื่อพนักงาน": "วิชาญ (Chan)", "ทีม": "Cinema Engineer"}])

if "task_schedule" not in st.session_state:
    st.session_state.task_schedule = pd.DataFrame(columns=["ชื่อพนักงาน", "ทีม", "กะ", "ประเภท", "Status", "หมวดหมู่", "ชื่องาน", "รายละเอียด", "เริ่ม", "สิ้นสุด"])

# =====================================================================
# 📑 ส่วนที่ 3: ระบบนำทาง (Tabs)
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs(["📝 Jobs & Forms", "📅 Timeline", "📊 Capacity", "⚙️ Settings"])

with tab1:
    st.subheader("➕ เพิ่มงานหรือการลา")
    roster = st.session_state.employee_roster
    roster["Label"] = roster["ชื่อพนักงาน"] + " : " + roster["ทีม"]
    sel = st.selectbox("เลือกพนักงาน:", roster["Label"].unique())
    emp = roster[roster["Label"] == sel]["ชื่อพนักงาน"].iloc[0]
    team = roster[roster["Label"] == sel]["ทีม"].iloc[0]
    
    with st.form("add_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            shift = st.selectbox("กะ:", ["Day", "Mid", "Night"])
            job_name = st.text_input("ชื่องาน:")
        with c2:
            stage = st.selectbox("Stage/ประเภท:", PROJECT_STAGES + LEAVE_OPTIONS)
            detail = st.text_area("รายละเอียด:")
        with c3:
            s_d = st.date_input("เริ่ม:", date.today())
            e_d = st.date_input("สิ้นสุด:", date.today())
            if st.form_submit_button("บันทึก"):
                st.session_state.task_schedule = pd.concat([st.session_state.task_schedule, pd.DataFrame([{
                    "ชื่อพนักงาน": emp, "ทีม": team, "กะ": shift, "ประเภท": "งาน",
                    "Status": stage.split(":")[0], "ชื่องาน": job_name, "รายละเอียด": detail,
                    "เริ่ม": pd.to_datetime(s_d), "สิ้นสุด": pd.to_datetime(e_d)
                }])], ignore_index=True)
                st.rerun()

with tab2:
    st.subheader("📅 ปฏิทินงาน")
    df = st.session_state.task_schedule
    if not df.empty:
        events = []
        for _, row in df.iterrows():
            events.append({
                "title": f"[{row['Status']}] {row['ชื่องาน']}",
                "start": row["เริ่ม"].strftime("%Y-%m-%d"),
                "end": row["สิ้นสุด"].strftime("%Y-%m-%d"),
                "backgroundColor": STAGE_COLORS.get(row["Status"], "#333")
            })
        calendar(events=events, options={"initialView": "dayGridMonth"})

with tab3:
    st.subheader("📊 ข้อมูลภาพรวมช่าง")
    cols = st.columns(4)
    for i, emp in enumerate(st.session_state.employee_roster["ชื่อพนักงาน"].unique()):
        count = len(st.session_state.task_schedule[st.session_state.task_schedule["ชื่อพนักงาน"] == emp])
        with cols[i % 4]:
            st.markdown(f'<div class="eng-card"><div class="eng-name">{emp}</div><div class="eng-stat">งานรวม: {count}</div></div>', unsafe_allow_html=True)

with tab4:
    st.subheader("⚙️ ตั้งค่า")
    if st.button("Download Excel"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            st.session_state.task_schedule.to_excel(writer)
        st.download_button("โหลดไฟล์", buffer, "data.xlsx")
