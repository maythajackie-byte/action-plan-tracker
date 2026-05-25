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

# นำโทนสีจากไฟล์ HTML ต้นฉบับของคุณมาปรับใช้
st.markdown("""
<style>
    /* ปรับแต่งสีพื้นหลังหลักและตัวอักษร */
    .stApp { background-color: #f4f6f9; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Segoe UI', sans-serif; }
    
    /* ตกแต่งกล่อง Expander ให้ดูเป็น Card มากขึ้น */
    .streamlit-expanderHeader { background-color: #ffffff; border-radius: 8px; font-weight: bold; color: #f5a623; }
    
    /* สไตล์สำหรับการ์ดข้อมูลช่าง (Engineer Capacity Cards) */
    .eng-card { background-color: #ffffff; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.08); border-top: 4px solid #3498db; margin-bottom: 15px; }
    .eng-name { font-size: 16px; font-weight: bold; color: #2c3e50; }
    .eng-stat { font-size: 13px; color: #7f8c8d; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

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
    st.session_state.task_schedule = df_t

# ดึงข้อมูลมาใช้งาน
roster_df = st.session_state.employee_roster
current_data = st.session_state.task_schedule

# ---------------------------------------------------------------------
# แท็บ 3: ข้อมูลช่างและประสิทธิภาพ (Capacity & Workload)
# ---------------------------------------------------------------------
with tab3:
    st.markdown("### 👷 Engineer Workload Overview")
    st.caption("สรุปปริมาณงานและการลาของช่างแต่ละท่าน (คล้ายดีไซน์ HTML)")
    
    # สร้างการ์ดแสดงข้อมูลของช่างแต่ละคนโดยใช้ st.columns
    cols = st.columns(4)
    for i, emp in enumerate(st.session_state.employee_roster["ชื่อพนักงาน"].unique()):
        
        # คำนวณจำนวนงานและการลา (บรรทัดนี้ต้องยาวจนสุด)
        emp_jobs = current_data[(current_data["ชื่อพนักงาน"] == emp) & (current_data["ประเภท"] == "แผนงาน")]
        emp_leaves = current_data[(current_data["ชื่อพนักงาน"] == emp) & (current_data["ประเภท"] == "การลา")]
        
        job_count = len(emp_jobs)
        leave_count = len(emp_leaves)
        
        with cols[i % 4]: # จัดเรียงใส่คอลัมน์
            # ใช้ HTML เพื่อเลียนแบบกล่องการ์ดสวยๆ
            st.markdown(f"""
            <div class="eng-card">
                <div class="eng-name">{emp}</div>
                <div class="eng-stat">💼 งานทั้งหมด: <b>{job_count} Jobs</b></div>
                <div class="eng-stat">🏖️ ลาหยุด: <b>{leave_count} ครั้ง</b></div>
            </div>
            "", unsafe_allow_html=True)

# =====================================================================
# 📑 ส่วนที่ 4: การสร้างระบบนำทาง (Tabs Layout)
# =====================================================================
# แบ่งหน้าเว็บเป็น 4 แท็บหลักเหมือนใน HTML ของคุณ
tab1, tab2, tab3, tab4 = st.tabs(["📝 Jobs & Forms (จัดการงาน)", "📅 Timeline (ปฏิทิน)", "📊 Capacity (ข้อมูลช่าง)", "⚙️ Settings (ตั้งค่า & Export)"])

# ---------------------------------------------------------------------
# แท็บ 1: จัดการงานและการลา (Forms & Jobs Data)
# ---------------------------------------------------------------------
with tab1:
    st.markdown("### ➕ เพิ่มงานหรือการลาใหม่ (Add Job / Leave)")
    
    # เลือกพนักงาน
    roster_df["Display_Label"] = roster_df["ชื่อพนักงาน"] + " : " + roster_df["ทีม"]
    selected_label = st.selectbox("👉 เลือกรายชื่อพนักงาน:", roster_df["Display_Label"].unique())
    current_emp_name = roster_df[roster_df["Display_Label"] == selected_label]["ชื่อพนักงาน"].values[0]
    current_emp_team = roster_df[roster_df["Display_Label"] == selected_label]["ทีม"].values[0]

    entry_type = st.radio("ประเภทการบันทึก:", ["💼 วางแผนงาน (Work Plan)", "🏖️ แจ้งลา (Leave)"], horizontal=True)

    with st.form("add_job_form", clear_on_submit=True):
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            shift_choice = st.selectbox("กะเวลา (Shift):", ["Day", "Mid", "Night"])
            task_title = st.text_input("ชื่องาน / หัวข้อการแจ้งลา:")
            if "วางแผนงาน" in entry_type:
                task_detail = st.text_area("Scope / รายละเอียดงาน:")
                record_cat = "แผนงาน"
            else:
                record_cat = "การลา"
                
        with f_col2:
            if "วางแผนงาน" in entry_type:
                status_code = st.selectbox("Phase (Stage):", PROJECT_STAGES).split(":")[0]
                work_cat = st.selectbox("ประเภทพื้นที่งาน:", TASK_CATEGORIES)
            else:
                status_code = st.selectbox("ประเภทการลา:", LEAVE_OPTIONS).split(":")[0]
                task_detail = st.text_area("เหตุผลการลา:")
                work_cat = "การลาหยุดพักผ่อน"
                
        with f_col3:
            start_d = st.date_input("Start Date:", date(2026, 5, 18))
            start_t = st.time_input("Start Time:", time(9, 0), step=1800)
            end_d = st.date_input("End Date:", date(2026, 5, 18))
            end_t = st.time_input("End Time:", time(18, 0), step=1800)
            
        if st.form_submit_button("💾 บันทึกลงระบบ"):
            if task_detail.strip() == "" or task_title.strip() == "":
                st.error("❌ กรุณากรอกชื่องานและรายละเอียดข้อมูลให้ครบถ้วน")
            else:
                new_record = {
                    "ชื่อพนักงาน": current_emp_name, "ทีม": current_emp_team, "กะ": shift_choice,
                    "ประเภท": record_cat, "Status": status_code, "หมวดหมู่": work_cat,
                    "ชื่องาน": task_title, "รายละเอียด": task_detail,
                    "เริ่ม": datetime.combine(start_d, start_t), "สิ้นสุด": datetime.combine(end_d, end_t)
                }
                st.session_state.task_schedule = pd.concat([st.session_state.task_schedule, pd.DataFrame([new_record])], ignore_index=True)
                st.success("บันทึกสำเร็จ!")
                st.rerun()

    st.markdown("---")
    st.markdown("### 📋 ตารางงานทั้งหมด (Jobs Data)")
    st.dataframe(current_data, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------
# แท็บ 2: ปฏิทินและไทม์ไลน์ (Timeline View)
# ---------------------------------------------------------------------
with tab2:
    st.markdown("### 📅 ปฏิทินรวมพนักงานทั้งหมด (All Staff Timeline)")
    
    cal_options = {
        "initialView": "dayGridMonth",
        "initialDate": "2026-05-01",
        "firstDay": 0, "displayEventTime": False,
        "headerToolbar": {"left": "today prev,next", "center": "title", "right": "dayGridMonth,timeGridWeek"}
    }
    
    if not current_data.empty:
        all_events = get_calendar_events(current_data)
        cal_res = calendar(events=all_events, options=cal_options, key="main_cal")
        
        # กล่องแสดงรายละเอียดเมื่อคลิกแถบงานในปฏิทิน
        if cal_res.get("eventClick"):
            ev = cal_res["eventClick"]["event"]
            prp = ev.get("extendedProps", {})
            st.info(f"**ชื่องาน:** {ev.get('title')}\n\n**พนักงาน:** {prp.get('empName')} | **เวลา:** {prp.get('timeStr')}\n\n**รายละเอียด:** {prp.get('details')}")
            
        st.markdown("---")
        st.markdown(f"### 🔍 Gantt Chart ของ: {current_emp_name}")
        p_data = current_data[current_data["ชื่อพนักงาน"] == current_emp_name]
        if not p_data.empty:
            fig = px.timeline(p_data, x_start="เริ่ม", x_end="สิ้นสุด", y="ชื่องาน", color="Status", color_discrete_map=STAGE_COLORS)
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("ยังไม่มีงานในระบบสำหรับพนักงานท่านนี้")

# ---------------------------------------------------------------------
# แท็บ 3: ข้อมูลช่างและประสิทธิภาพ (Capacity & Workload)
# ---------------------------------------------------------------------
with tab3:
    st.markdown("### 👷 Engineer Workload Overview")
    st.caption("สรุปปริมาณงานและการลาของช่างแต่ละท่าน (คล้ายดีไซน์ HTML)")
    
    # สร้างการ์ดแสดงข้อมูลของช่างแต่ละคนโดยใช้ st.columns
    cols = st.columns(4)
    for i, emp in enumerate(st.session_state.employee_roster["ชื่อพนักงาน"].unique()):
        # คำนวณจำนวนงานและการลา
        emp_jobs = current_data[(current_data["ชื่อพนักงาน"] == emp) & (current_data
