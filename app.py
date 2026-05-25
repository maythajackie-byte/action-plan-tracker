import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from streamlit_calendar import calendar

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="Workload Tracker", layout="wide")

# ฐานข้อมูลเริ่มต้น
if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame(columns=["ชื่อพนักงาน", "ทีม", "ชื่องาน", "Status", "เริ่ม", "สิ้นสุด", "รายละเอียด"])

# หน้าเว็บ
st.title("📋 Engineer Workload & Schedule Tracker")

# ระบบ Tab
tab1, tab2, tab3 = st.tabs(["📝 Jobs & Forms", "📅 Timeline", "⚙️ Settings"])

with tab1:
    st.subheader("➕ เพิ่มงานใหม่")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        emp = col1.text_input("ชื่อพนักงาน:")
        job = col2.text_input("ชื่องาน:")
        s_d = st.date_input("เริ่ม:")
        e_d = st.date_input("สิ้นสุด:")
        stage = st.selectbox("Stage:", ["P0", "P1", "P2", "P3"])
        desc = st.text_area("รายละเอียด:")
        if st.form_submit_button("บันทึก"):
            new_row = pd.DataFrame([{"ชื่อพนักงาน": emp, "ชื่องาน": job, "Status": stage, "เริ่ม": pd.to_datetime(s_d), "สิ้นสุด": pd.to_datetime(e_d), "รายละเอียด": desc}])
            st.session_state.tasks = pd.concat([st.session_state.tasks, new_row], ignore_index=True)
            st.rerun()

with tab2:
    st.subheader("📅 ปฏิทิน")
    if not st.session_state.tasks.empty:
        events = []
        for _, row in st.session_state.tasks.iterrows():
            events.append({
                "title": f"[{row['Status']}] {row['ชื่อพนักงาน']} - {row['ชื่องาน']}",
                "start": row["เริ่ม"].strftime("%Y-%m-%d"),
                "end": row["สิ้นสุด"].strftime("%Y-%m-%d"),
                "backgroundColor": "#3498db"
            })
        calendar(events=events, options={"initialView": "dayGridMonth"})

with tab3:
    st.subheader("🗑️ จัดการข้อมูล")
    st.data_editor(st.session_state.tasks, use_container_width=True)
    if st.button("ล้างข้อมูลทั้งหมด"):
        st.session_state.tasks = pd.DataFrame(columns=["ชื่อพนักงาน", "ทีม", "ชื่องาน", "Status", "เริ่ม", "สิ้นสุด", "รายละเอียด"])
        st.rerun()
