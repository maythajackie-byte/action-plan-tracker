import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date

# 1. Page Configuration
st.set_page_config(page_title="Engineering Master Scheduler 2.0", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #262730; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1a1c24; border-radius: 5px 5px 0 0; padding: 10px 20px; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Engineering Master Scheduler Dashboard 2.0")

# 2. Master Data
TEAMS = ["Production Team", "Cinema Engineer", "Pro-AV Engineer", "Post Production Engineer", "Broadcast Engineer", "Residential Engineer"]
PROJECT_STAGES = ["P0: Pitch/Brainstorm", "P1: Build up/Present", "P2: Installation", "P3: After Sales/MA"]
LEAVE_CODES = ["PL: ลากิจ", "VL: ลาพักร้อน", "SL: ลาป่วย", "LVP: ลาไม่รับค่าจ้าง"]

STAGE_COLORS = {
    "P0": "#F1C40F", "P1": "#E67E22", "P2": "#3498DB", "P3": "#2ECC71",
    "PL": "#95A5A6", "VL": "#9B59B6", "SL": "#E74C3C", "LVP": "#34495E"
}

# 3. Session State Data
if "schedule_df" not in st.session_state:
    # Initial Mock Data
    init_data = [
        {"ทีม": "Cinema Engineer", "พนักงาน": "วิชาญ (Chan)", "กะ": "Day", "Category": "งาน", "Status": "P2", "รายละเอียด": "Install Projector SFW", "เริ่ม": "2026-05-18 08:00", "สิ้นสุด": "2026-05-20 17:00"},
        {"ทีม": "Pro-AV Engineer", "พนักงาน": "ฉัตรชัย (Dy)", "กะ": "Day", "Category": "การลา", "Status": "VL", "รายละเอียด": "พักร้อนประจำปี", "เริ่ม": "2026-05-19 08:00", "สิ้นสุด": "2026-05-21 17:00"},
        {"ทีม": "Production Team", "พนักงาน": "กัลยกร (Namfon)", "กะ": "Mid", "Category": "งาน", "Status": "P0", "รายละเอียด": "Brainstorm Stage", "เริ่ม": "2026-05-18 15:
