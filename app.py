import streamlit as st
import pandas as pd

# 1. การตั้งค่าหน้า Dashboard
st.set_page_config(layout="wide")
st.title("📋 Engineer Workload & Schedule Tracker")

# 2. จำลองฐานข้อมูล (แนะนำ: ให้เชื่อมต่อ Google Sheets ในอนาคตเพื่อบันทึกถาวร)
if "jobs" not in st.session_state:
    st.session_state.jobs = pd.DataFrame(columns=["Customer", "Job Name", "PIC", "Status", "Start", "End"])

# 3. จัดการ Tabs (ระบบนำทาง)
tab1, tab2, tab3 = st.tabs(["📋 Jobs Table", "📅 Gantt Timeline", "⚙️ Manage"])

with tab1:
    st.subheader("รายการงานทั้งหมด")
    st.data_editor(st.session_state.jobs, use_container_width=True, num_rows="dynamic")

with tab2:
    st.subheader("📅 ไทม์ไลน์งาน")
    if not st.session_state.jobs.empty:
        # แสดง Timeline Chart
        fig = st.bar_chart(st.session_state.jobs, x="Job Name", y=["Start", "End"])
    else:
        st.info("ยังไม่มีข้อมูลงาน")

with tab3:
    st.subheader("➕ เพิ่ม/แก้ไขข้อมูลงาน")
    with st.form("add_job"):
        cust = st.text_input("Customer")
        job = st.text_input("Job Name")
        pic = st.text_input("PIC")
        status = st.selectbox("Status", ["On-going", "Complete", "Pending"])
        s_date = st.date_input("Start Date")
        e_date = st.date_input("End Date")
        if st.form_submit_button("บันทึกงาน"):
            new_job = pd.DataFrame([{"Customer": cust, "Job Name": job, "PIC": pic, "Status": status, "Start": s_date, "End": e_date}])
            st.session_state.jobs = pd.concat([st.session_state.jobs, new_job], ignore_index=True)
            st.rerun()

# 4. ปุ่ม Export (ส่วนนี้ทำงานได้ใน Streamlit)
if st.button("📥 Download Excel"):
    output = io.BytesIO()
    st.session_state.jobs.to_excel(output, index=False)
    st.download_button("คลิกเพื่อโหลด", data=output.getvalue(), file_name="Workload.xlsx")
