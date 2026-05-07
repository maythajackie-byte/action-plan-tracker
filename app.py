import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- ปรับแต่ง CSS ให้เห็นชื่อหัวข้อและตัวเลขชัดเจน ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b5345; color: white; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: white !important; }
    
    /* ปรับแต่งกล่อง Metric */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #0b5345;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    /* สีของชื่อหัวข้อ (Label) */
    [data-testid="stMetricLabel"] {
        color: #0b5345 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    /* สีของตัวเลขสรุป (Value) */
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. จัดการข้อมูล (ดึงข้อมูลเหมือนเดิม)
DATA_FILE = "action_plan_2026.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        if 'Start Date' in df.columns: df['Start Date'] = pd.to_datetime(df['Start Date']).dt.date
        if 'End Date' in df.columns: df['End Date'] = pd.to_datetime(df['End Date']).dt.date
        return df
    return pd.DataFrame(columns=["Dept", "Activity", "Sales PIC", "Eng PIC", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])

df = load_data()

# 3. ส่วนหัวข้อ
st.title("📋 2026 Follow up & Action Plan")
st.markdown("---")

# 4. ส่วนแสดง Metrics พร้อมคำอธิบายภาษาไทย
if not df.empty:
    col_m1, col_m2, col_m3 = st.columns(3)
    
    # กล่องที่ 1: จำนวนงานทั้งหมด
    col_m1.metric(label="📊 จำนวนงานทั้งหมด (Tasks)", value=f"{len(df)} รายการ")
    
    # กล่องที่ 2: ความคืบหน้าเฉลี่ย
    avg_prog = df["Progress"].mean()
    col_m2.metric(label="📈 ความคืบหน้าเฉลี่ย (Overall)", value=f"{avg_prog:.1f}%")
    
    # กล่องที่ 3: จำนวนงานด่วนที่สุด (P0)
    p0_count = len(df[df['Project Status'] == 'P0'])
    col_m3.metric(label="🚨 งานด่วนพิเศษ (P0 Status)", value=f"{p0_count} รายการ")

    st.markdown("---")
# (ส่วนที่เหลือของโค้ด เช่น Sidebar และตารางรายละเอียด ให้ใช้ของเดิมที่ผมเคยให้ไว้ได้เลยครับ)
