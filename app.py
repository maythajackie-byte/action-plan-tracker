import streamlit as st
import pandas as pd
from datetime import datetime, date

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="Engineer Workload Tracker", layout="wide")

# CSS ตกแต่งให้เหมือนต้นฉบับ (สีเหลืองส้มและโครงสร้าง)
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .header { background: #f5a623; padding: 1rem; color: white; border-radius: 10px; margin-bottom: 20px; }
    .eng-card { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# ส่วน Header เหมือนภาพต้นฉบับ
st.markdown('<div class="header"><h1>📋 Engineer Workload Tracker</h1></div>', unsafe_allow_html=True)

# ฐานข้อมูล (แนะนำให้เชื่อมต่อ Google Sheets ในขั้นตอนถัดไปเพื่อบันทึกถาวร)
if "jobs" not in st.session_state:
    st.session_state.jobs = pd.DataFrame(columns=["Customer", "Job Name", "Phase", "Status", "Start", "End"])

# Tabs เหมือนในภาพ
tab1, tab2, tab3, tab4 = st.tabs(["📋 Jobs & Forms", "📅 Timeline", "📊 Capacity", "📈 Report"])

with tab1:
    st.subheader("➕ เพิ่มงานหรือการลาใหม่")
    with st.form("job_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        cust = c1.text_input("Customer")
        job = c2.text_input("Job / Project Name")
        phase = c3.selectbox("Phase", ["P0", "P1", "P2", "P3"])
        
        s_date = c1.date_input("Start Date")
        e_date = c2.date_input("End Date")
        status = c3.selectbox("Status", ["On-going", "Complete", "Pending"])
        
        if st.form_submit_button("💾 บันทึก"):
            new_row = pd.DataFrame([{"Customer": cust, "Job Name": job, "Phase": phase, "Status": status, "Start": s_date, "End": e_date}])
            st.session_state.jobs = pd.concat([st.session_state.jobs, new_row], ignore_index=True)
            st.rerun()
            
    st.dataframe(st.session_state.jobs, use_container_width=True)

with tab2:
    st.subheader("📅 Timeline")
    # ใส่ระบบปฏิทินที่นี่

with tab3:
    st.subheader("📊 Capacity")
    # ใส่ตารางสรุปงานช่างที่นี่

with tab4:
    st.subheader("📈 Report")
    # ใส่ Report ที่นี่
