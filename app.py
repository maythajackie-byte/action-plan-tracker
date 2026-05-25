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

# เลี่ยงการใช้ Triple Quotes (""") เพื่อป้องกัน Error ตอนก็อปปี้วาง
css_code = (
    "<style>"
    ".stApp { background-color: #f4f6f9; }"
    "h1, h2, h3 { color: #2c3e50; font-family: 'Segoe UI', sans-serif; }"
    ".streamlit-expanderHeader { background-color: #ffffff; border-radius: 8px; font-weight: bold; color: #f5a623; }"
    ".eng-card { background-color: #ffffff; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.08); border-top: 4px solid #3498db; margin-bottom: 15px; }"
    ".eng-name { font-size: 16px; font-weight: bold; color: #2c3e50; }"
    ".eng-stat { font-size: 13px; color: #7f8c8d; margin-top: 5px; }"
    "</style>"
)
st.markdown(css_code, unsafe_allow_html=True)

st.title("📋 Engineer Workload & Schedule Tracker")
st.markdown("ระบบบริหารแผนงานประจำปี (สไตล์ Dashboard)")

# =====================================================================
# 🗄️ ส่วนที่ 2: ตั้งค่าข้อมูลโครงสร้าง & ฐานข้อมูล (Master Data & State)
# =====================================================================
TEAMS = ["Production Team", "Cinema Engineer", "Pro-AV Engineer", "Post Production Engineer", "Broadcast Engineer", "Residential Engineer"]
TASK_CATEGORIES = ["Maintenance (Bangkok)", "Maintenance (Outside Bangkok)", "Service (Bangkok)", "Service (Outside)", "Project (Bangkok)", "Project (Outside)", "Training", "Event/Show"]
PROJECT_STAGES = ["P0: Pitch/Brainstorm", "P1: Build up/Present", "P2: Installation", "P3: After Sales/Service/MA"]
LEAVE_OPTIONS = ["PL: ลากิจ (Personal Leave)", "VL: ลาพักร้อน (Vacation Leave)", "SL: ลาป่วย (Sick Leave)", "LVP: ลาไม่รับค่าจ้าง"]

STAGE_COLORS = {"P0": "#F1C40F", "P1": "#E67E22", "P2": "#3498DB", "P3": "#2ECC71", "PL": "#95A5A6", "VL": "#9B59B6", "SL": "#E74C3C", "LVP": "#34495E"}

if "employee_roster" not in st.session_state:
    st.session_state.employee_roster = pd.DataFrame([
        {"ชื่อพนักงาน": "วิชาญ (Chan)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "ฉัตรชัย (Dy)", "ทีม": "Broadcast Engineer"},
        {"ชื่อพนักงาน": "กัลยกร (Namfon)", "ทีม": "Production Team"},
        {"ชื่อพนักงาน": "เอกวุฒิ (Tum)", "ทีม": "Residential Engineer"}
    ])

if "task_schedule" not in st.session_state:
    init_tasks = [
        {"ชื่อพนักงาน": "วิชาญ (Chan)", "ทีม": "Cinema Engineer", "กะ": "Day", "ประเภท": "แผนงาน", "Status": "P2", "หมวดหมู่": "Project (Bangkok)", "ชื่องาน": "ติดตั้งระบบภาพ", "รายละเอียด": "SFW Hall 15", "เริ่ม": "2026-05-18 09:00", "สิ้นสุด": "2026-05-20 18:00"},
        {"ชื่อพนักงาน": "ฉัตรชัย (Dy)", "ทีม": "Broadcast Engineer", "กะ": "Day", "ประเภท": "การลา", "Status": "VL", "หมวดหมู่": "การลา", "ชื่องาน": "ลาพักร้อน", "รายละเอียด": "พักร้อนประจำปี", "เริ่ม": "2026-05-13 09:00", "สิ้นสุด": "2026-05-15 18:00"}
    ]
    df_t = pd.DataFrame(init_tasks)
    df_t["เริ่ม"] = pd.to_datetime(df_t["เริ่ม"])
    df_t["สิ้นสุด"] = pd.to_datetime(df_t["สิ้นสุด"])
    st.session_state
