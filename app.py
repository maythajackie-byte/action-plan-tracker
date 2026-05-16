import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, time, timedelta
import calendar

# ตั้งค่าการแสดงผลแนวกว้าง (Enterprise Layout)
st.set_page_config(page_title="Engineering Master Scheduler 5.2", layout="wide")

st.title("📊 Engineering Master Scheduler Dashboard 5.2")
st.markdown("### ระบบบริหารแผนงานประจำปี พ.ศ. 2569")

# --- [ข้อมูลโครงสร้างหลัก - Master Data] ---
TEAMS = [
    "Production Team", "Cinema Engineer", "Pro-AV Engineer", 
    "Post Production Engineer", "Broadcast Engineer", "Residential Engineer", "Center Engineer"
]

TASK_CATEGORIES = [
    "Maintenance (Bangkok)", "Maintenance (Outside Bangkok)", "Maintenance (Oversea)",
    "Service (Bangkok)", "Service (Outside Bangkok)", "Service (Oversea)",
    "Project (Bangkok)", "Project (Outside Bangkok)", "Project (Oversea)",
    "Training (In-house)", "Training (Outside)",
    "Production (Project)", "Production (Other)",
    "Event/Show", "Others"
]

PROJECT_STAGES = ["P0: Pitch/Brainstorm", "P1: Build up/Present", "P2: Installation", "P3: After Sales/Service/MA"]
LEAVE_OPTIONS = ["PL: ลากิจ (Personal Leave)", "VL: ลาพักร้อน (Vacation Leave)", "SL: ลาป่วย (Sick Leave)", "LVP: ลาไม่รับค่าจ้าง (Leave Without Pay)"]

STAGE_COLORS = {
    "P0": "#F1C40F", "P1": "#E67E22", "P2": "#3498DB", "P3": "#2ECC71",
    "PL": "#95A5A6", "VL": "#9B59B6", "SL": "#E74C3C", "LVP": "#34495E"
}

# --- [ระบบฐานข้อมูลชั่วคราว - Session State] ---
if "employee_roster" not in st.session_state:
    st.session_state.employee_roster = pd.DataFrame([
        {"ชื่อพนักงาน": "ฉัตรชัย (Dy)", "ทีม": "Pro-AV Engineer"},
        {"ชื่อพนักงาน": "วรวุฒิ (Wut)", "ทีม": "Pro-AV Engineer"},
        {"ชื่อพนักงาน": "รณฤทธิ์ (Bank)", "ทีม": "Pro-AV Engineer"},
        {"ชื่อพนักงาน": "ปารวี (Vee)", "ทีม": "Pro-AV Engineer"},
        {"ชื่อพนักงาน": "วัชรากร (Golf)", "ทีม": "Pro-AV Engineer"},
        
        {"ชื่อพนักงาน": "เกียรติศักดิ์ (Tle)", "ทีม": "Post Production Engineer"},
        {"ชื่อพนักงาน": "ชัยณรงค์ (Keng)", "ทีม": "Post Production Engineer"},
        {"ชื่อพนักงาน": "ณัฐวรท (Boss)", "ทีม": "Post Production Engineer"}, 
        
        {"ชื่อพนักงาน": "บุญชอบ (Chob)", "ทีม": "Broadcast Engineer"},
        {"ชื่อพนักงาน": "ปานกริช (Dan)", "ทีม": "Broadcast Engineer"},
        {"ชื่อพนักงาน": "เดชา (De)", "ทีม": "Broadcast Engineer"},
        {"ชื่อพนักงาน": "ภัทรจิตรา (Nook)", "ทีม": "Broadcast Engineer"},
        
        {"ชื่อพนักงาน": "เมธา (Jack)", "ทีม": "Center Engineer"},
        {"ชื่อพนักงาน": "ดนุภพ (Pai)", "ทีม": "Center Engineer"},
        {"ชื่อพนักงาน": "สราวุธ (No)", "ทีม": "Center Engineer"},
        {"ชื่อพนักงาน": "คทาเทพ  (์James)", "ทีม": "Center Engineer"},
        {"ชื่อพนักงาน": "มลรัก (Aeh)", "ทีม": "Center Engineer"},
        {"ชื่อพนักงาน": "ศิริศักดิ์ (Oh)", "ทีม": "Center Engineer"},
        {"ชื่อพนักงาน": "ชัชวาลย์ (Diew)", "ทีม": "Center Engineer"},
        {"ชื่อพนักงาน": "นิติธร (Fluke)", "ทีม": "Center Engineer"},
        {"ชื่อพนักงาน": "ทศพล (Tri)", "ทีม": "Center Engineer"},
        {"ชื่อพนักงาน": "ปรีชา (Aek)", "ทีม": "Center Engineer"},
        {"ชื่อพนักงาน": "ไพศาล (Mua)", "ทีม": "Center Engineer"},
        
        {"ชื่อพนักงาน": "ณัฐติพงษ์ (Tle)", "ทีม": "Residential Engineer"},
        {"ชื่อพนักงาน": "วีรภัทร (Arm)", "ทีม": "Residential Engineer"},
    ])

if "task_schedule" not in st.session_state:
    init_tasks = [
        {"ชื่อพนักงาน": "วิชาญ (Chan)", "ทีม": "Cinema Engineer", "กะ": "Day", "ประเภท": "แผนงาน", "Status": "P2", "หมวดหมู่": "Project (Bangkok)", "รายละเอียด": "ติดตั้งระบบภาพ SFW Hall 15", "เริ่ม": "2026-05-18 09:00", "สิ้นสุด": "2026-05-20 18:00"},
        {"ชื่อพนักงาน": "ฉัตรชัย (Dy)", "ทีม": "Broadcast Engineer", "กะ": "Day", "ประเภท": "การลา", "Status": "VL", "หมวดหมู่": "ลาพักร้อน", "รายละเอียด": "พักร้อนประจำปี", "เริ่ม": "2026-05-17 09:00", "สิ้นสุด": "2026-05-17 18:00"},
        {"ชื่อพนักงาน": "กัลยกร (Namfon)", "ทีม": "Production Team", "กะ": "Mid", "ประเภท": "แผนงาน", "Status": "P0", "หมวดหมู่": "Production (Project)", "รายละเอียด": "Brainstorm Stage โครงการใหม่", "เริ่ม": "2026-05-18 15:00", "สิ้นสุด": "2026-05-18 23:00"}
    ]
    df_tasks = pd.DataFrame(init_tasks)
    df_tasks["เริ่ม"] = pd.to_datetime(df_tasks["เริ่ม"])
    df_tasks["สิ้นสุด"] = pd.to_datetime(df_tasks["สิ้นสุด"])
    st.session_state.task_schedule = df_tasks


# =========================================================
# 👤 ขั้นตอนที่ 1: ลงทะเบียนรายชื่อพนักงานใหม่
# =========================================================
st.subheader("👤 ขั้นตอนที่ 1: ลงทะเบียนรายชื่อพนักงานใหม่")
with st.expander("📝 เปิดฟอร์มลงทะเบียนพนักงานใหม่ (ข้อมูลจะไปเพิ่มที่แถบซ้ายมืออัตโนมัติ)", expanded=False):
    with st.form("main_add_employee_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            add_name = st.text_input("ชื่อพนักงาน (เช่น สมชาย (Joe)):")
        with c2:
            add_team = st.selectbox("เลือกทีมสังกัดพนักงาน:", TEAMS)
            
        if st.form_submit_button("➕ บันทึกรายชื่อพนักงานใหม่"):
            if add_name.strip() != "":
                new_emp = {"ชื่อพนักงาน": add_name, "ทีม": add_team}
                st.session_state.employee_roster = pd.concat([st.session_state.employee_roster, pd.DataFrame([new_emp])], ignore_index=True)
                st.success(f"บันทึกรายชื่อคุณ {add_name} สำเร็จ!")
                st.rerun()
            else:
                st.error("กรุณากรอกชื่อพนักงานก่อนกดบันทึก")

st.divider()


# =========================================================
# 👥 แถบเครื่องมือแสดงรายชื่อพนักงานด้านซ้ายมือ (Sidebar)
# =========================================================
st.sidebar.header("👥 รายชื่อพนักงานในระบบ")
roster_df = st.session_state.employee_roster
roster_df["Display_Label"] = roster_df["ชื่อพนักงาน"] + " : " + roster_df["ทีม"]

selected_label = st.sidebar.radio(
    "👉 คลิกเลือกชื่อพนักงานเพื่อวางงาน:",
    options=roster_df["Display_Label"].unique()
)

current_emp_name = roster_df[roster_df["Display_Label"] == selected_label]["ชื่อพนักงาน"].values[0]
current_emp_team = roster_df[roster_df["Display_Label"] == selected_label]["ทีม"].values[0]


# =========================================================
# 🛠️ ขั้นตอนที่ 2: จัดการตารางงานและการลา (แยกประเภทเด็ดขาด)
# =========================================================
st.subheader(f"🛠️ ขั้นตอนที่ 2: จัดการตารางเวลาของ [ {current_emp_name} ]")

entry_type = st.radio(
    "เลือกระบบที่ต้องการบันทึกข้อมูล:", 
    ["💼 วางแผนงาน (Work Plan)", "🏖️ บันทึกการลา (Leave)"], 
    horizontal=True
)

with st.form("assignment_form", clear_on_submit=True):
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        shift_choice = st.selectbox("กะเวลาการทำงาน:", ["Day", "Mid", "Night"])
        
        if "วางแผนงาน" in entry_type:
            task_detail = st.text_area("รายละเอียดเนื้อหางาน:")
            record_cat = "แผนงาน"
        else:
            record_cat = "การลา"
        
    with col_f2:
        if "วางแผนงาน" in entry_type:
            status_code = st.selectbox("เลือกระดับ Stage งาน:", PROJECT_STAGES).split(":")[0]
            work_cat = st.selectbox("หมวดหมู่งานตามพื้นที่ปฏิบัติงาน:", TASK_CATEGORIES)
        else:
            status_code = st.selectbox("แจ้งลา", LEAVE_OPTIONS).split(":")[0]
            task_detail = st.text_area("เหตุผลการลา:")
            work_cat = "การลาหยุดพักผ่อน"
        
    with col_f3:
        start_d = st.date_input("วันที่เริ่มต้น:", date(2026, 5, 18))
        # ปรับค่า Default เป็น 09:00 และสเกลช่วงเวลาทีละ 30 นาที (1800 วินาที)
        start_t = st.time_input("เวลาเริ่มต้น:", time(9, 0), step=1800)
        
        end_d = st.date_input("วันที่สิ้นสุด:", date(2026, 5, 18))
        # ปรับค่า Default เป็น 18:00 และสเกลช่วงเวลาทีละ 30 นาที (1800 วินาที)
        end_t = st.time_input("เวลาสิ้นสุด:", time(18, 0), step=1800)
        
    if st.form_submit_button("💾 บันทึกข้อมูลลงฐานข้อมูลส่วนกลาง"):
        if task_detail.strip() == "":
            st.error("❌ กรุณากรอกรายละเอียดงานหรือเหตุผลก่อนส่งข้อมูล")
        else:
            new_record = {
                "ชื่อพนักงาน": current_emp_name,
                "ทีม": current_emp_team,
                "กะ": shift_choice,
                "ประเภท": record_cat,
                "Status": status_code,
                "หมวดหมู่": work_cat,
                "รายละเอียด": task_detail,
                "เริ่ม": datetime.combine(start_d, start_t),
                "สิ้นสุด": datetime.combine(end_d, end_t)
            }
            st.session_state.task_schedule = pd.concat([st.session_state.task_schedule, pd.DataFrame([new_record])], ignore_index=True)
            st.success("บันทึกตารางลงปฏิทินสำเร็จ!")
            st.rerun()

st.divider()


# =========================================================
# 🗓️ ขั้นตอนที่ 3: ส่วนแสดงผลปฏิทินรายเดือน (Sunday First Grid Layout)
# =========================================================
st.subheader("🗓️ ขั้นตอนที่ 3: ปฏิทินภาพรวมประจำเดือน (Monthly Calendar Grid - เริ่มวันอาทิตย์)")

current_data = st.session_state.task_schedule

if not current_data.empty:
    current_data['วันที่'] = current_data['เริ่ม'].dt.date
    
    # กำหนดปีและเดือนที่ต้องการแสดงผล (ตัวอย่าง: พฤษภาคม 2026)
    target_year = 2026
    target_month = 5
    
    st.markdown(f"#### 📅 เดือนพฤษภาคม พ.ศ. 2569")
    
    # สร้างโครงสร้างปฏิทินโดยกำหนดให้วันแรกของสัปดาห์คือวันอาทิตย์ (firstweekday=6)
    cal = calendar.Calendar(firstweekday=6)
    month_weeks = cal.monthdayscalendar(target_year, target_month)
    
    # สร้างหัวคอลัมน์วันอาทิตย์ - วันเสาร์
    days_headers = ["อาทิตย์ (Sun)", "จันทร์ (Mon)", "อังคาร (Tue)", "พุธ (Wed)", "พฤหัสบดี (Thu)", "ศุกร์ (Fri)", "เสาร์ (Sat)"]
    cols = st.columns(7)
    for idx, header in enumerate(days_headers):
        cols[idx].markdown(f"<div style='text-align:center; font-weight:bold; background-color:#1e293b; padding:10px; border-radius:5px;'>{header}</div>", unsafe_allow_html=True)
        
    # วาดกล่องวันที่แต่ละสัปดาห์ลงในตาราง Grid
    for week in month_weeks:
        week_cols = st.columns(7)
        for day_idx, day_num in enumerate(week):
            if day_num == 0:
                # วันของเดือนอื่นที่คาบเกี่ยวกัน ปล่อยให้เป็นกล่องว่าง
                week_cols[day_idx].markdown("<div style='min-height:120px; background-color:#0e1117; border:1px solid #1e293b; padding:5px;'></div>", unsafe_allow_html=True)
            else:
                current_date_obj = date(target_year, target_month, day_num)
                day_events = current_data[current_data['วันที่'] == current_date_obj]
                
                # ตกแต่งกล่องข้อความวันที่ภายในปฏิทิน
                event_html = ""
                for _, ev in day_events.iterrows():
                    bg_color = STAGE_COLORS.get(ev['Status'], '#333')
                    event_html += f"<div style='background-color:{bg_color}; color:black; font-size:11px; padding:2px 5px; margin-top:3px; border-radius:3px; font-weight:bold;'>{ev['ชื่อพนักงาน']}: {ev['Status']}</div>"
                
                week_cols[day_idx].markdown(
                    f"<div style='min-height:120px; background-color:#1e222b; border:1px solid #38bdf8; padding:5px; border-radius:5px;'>"
                    f"<span style='font-weight:bold; font-size:16px; color:#38bdf8;'>{day_num}</span>"
                    f"{event_html}"
                    f"</div>", 
                    unsafe_allow_html=True
                )
                
    # =========================================================
    # 🔍 แผนภูมิ Gantt Chart เจาะลึกรายบุคคล (แสดงด้านล่างปฏิทิน)
    # =========================================================
    st.markdown("---")
    st.markdown(f"#### 🔍 แผนภูมิ Gantt Chart สรุปตารางงานรายกะเฉพาะบุคคลของ: **{current_emp_name}**")
    personal_data = current_data[current_data["ชื่อพนักงาน"] == current_emp_name]
    
    if not personal_data.empty:
        fig_gantt = px.timeline(
            personal_data, x_start="เริ่ม", x_end="สิ้นสุด", y="กะ", color="Status",
            color_discrete_map=STAGE_COLORS, hover_data=["หมวดหมู่", "รายละเอียด"],
            title=f"แถบเวลาปฏิบัติงานประจำวันแยกกะ (Day / Mid / Night) ของ {current_emp_name}"
        )
        fig_gantt.update_yaxes(autorange="reversed")
        fig_gantt.update_layout(height=230, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_gantt, use_container_width=True)
    else:
        st.info(f"💡 คุณ {current_emp_name} ยังไม่มีประวัติการลงตารางงานหรือการลาในเดือนนี้")

    # 3.3 ตารางแก้ไขข้อมูล
    with st.expander("🛠️ ตารางจัดการแก้ไขหรือลบรายการแผนงานดิบในระบบ"):
        edited_df = st.data_editor(current_data[["ชื่อพนักงาน", "ทีม", "กะ", "ประเภท", "Status", "หมวดหมู่", "เริ่ม", "สิ้นสุด", "รายละเอียด"]], use_container_width=True, num_rows="dynamic")
        if st.button("💾 ยืนยันปรับปรุงข้อมูลปฏิทิน"):
            edited_df["เริ่ม"] = pd.to_datetime(edited_df["เริ่ม"])
            edited_df["สิ้นสุด"] = pd.to_datetime(edited_df["สิ้นสุด"])
            st.session_state.task_schedule = edited_df
            st.success("อัปเดตระบบปฏิทินภาพรวมเรียบร้อย!")
            st.rerun()
else:
    st.info("ระบบกำลังรอข้อมูลเริ่มต้น...")
