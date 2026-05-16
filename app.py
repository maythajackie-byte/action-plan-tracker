import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, time

# ตั้งค่าหน้าจอ Web App เป็นแนวกว้างแบบ Enterprise Layout
st.set_page_config(page_title="Engineering Master Scheduler 3.0", layout="wide")

st.title("📊 Engineering Master Scheduler Dashboard 3.0")
st.markdown("### ระบบบริหารงานรายบุคคลและปฏิทินภาพรวม")

# --- 1. ข้อมูลโครงสร้างหลัก (Master Data) ---
TEAMS = [
    "Production Team", "Cinema Engineer", "Pro-AV Engineer", 
    "Post Production Engineer", "Broadcast Engineer", "Center Engineer", "Residential Engineer"
]
PROJECT_STAGES = ["P0: Pitch/Brainstorm", "P1: Build up/Present", "P2: Installation", "P3: After Sales/Service/MA"]
LEAVE_CODES = ["PL: ลากิจ", "VL: ลาพักร้อน", "SL: ลาป่วย", "LVP: ลาไม่รับค่าจ้าง"]

STAGE_COLORS = {
    "P0": "#F1C40F", "P1": "#E67E22", "P2": "#3498DB", "P3": "#2ECC71",
    "PL": "#95A5A6", "VL": "#9B59B6", "SL": "#E74C3C", "LVP": "#34495E"
}

# --- 2. ระบบฐานข้อมูลชั่วคราว (Session State) ---
# ฐานข้อมูลรายชื่อพนักงาน
if "employee_roster" not in st.session_state:
    st.session_state.employee_roster = pd.DataFrame([
        {"ชื่อพนักงาน": "ฉัตรชัย (Dy)", "ทีม": "Pro-AV Engineer"},
        {"ชื่อพนักงาน": "วรวุฒิ (Wut)", "ทีม": "Pro-AV Engineer"}
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

# ฐานข้อมูลตารางงานและการลา
if "task_schedule" not in st.session_state:
    init_tasks = [
        {"ชื่อพนักงาน": "วิชาญ (Chan)", "ทีม": "Cinema Engineer", "กะ": "Day", "ประเภท": "งาน", "Status": "P2", "รายละเอียด": "ติดตั้งระบบภาพและเสียง SFW", "เริ่ม": "2026-05-18 08:00", "สิ้นสุด": "2026-05-20 17:00"},
        {"ชื่อพนักงาน": "ฉัตรชัย (Dy)", "ทีม": "Pro-AV Engineer", "กะ": "Day", "ประเภท": "การลา", "Status": "VL", "รายละเอียด": "ลาพักร้อนประจำปี", "เริ่ม": "2026-05-19 08:00", "สิ้นสุด": "2026-05-21 17:00"},
        {"ชื่อพนักงาน": "กัลยกร (Namfon)", "ทีม": "Production Team", "กะ": "Mid", "ประเภท": "งาน", "Status": "P0", "รายละเอียด": "Brainstorm Stage โครงการใหม่", "เริ่ม": "2026-05-18 15:00", "สิ้นสุด": "2026-05-18 23:00"}
    ]
    df_tasks = pd.DataFrame(init_tasks)
    df_tasks["เริ่ม"] = pd.to_datetime(df_tasks["เริ่ม"])
    df_tasks["สิ้นสุด"] = pd.to_datetime(df_tasks["สิ้นสุด"])
    st.session_state.task_schedule = df_tasks

# --- 3. ส่วนแรก: ฟอร์มกรอกข้อมูลพนักงานใหม่ (หน้าแรก/ส่วนบน) ---
st.markdown("---")
with st.expander("👤 ขั้นตอนที่ 1: กรอกข้อมูลลงทะเบียนพนักงาน", expanded=st.session_state.employee_roster.empty):
    with st.form("employee_form", clear_on_submit=True):
        st.subheader("📝 ฟอร์มลงทะเบียนพนักงาน")
        c1, c2 = st.columns(2)
        with c1:
            new_name = st.text_input("ชื่อ-นามสกุลพนักงาน (พร้อมชื่อเล่น):", placeholder="เช่น สมชาย (Joe)")
        with c2:
            new_team = st.selectbox("เลือกทีมสังกัด:", TEAMS)
        
        if st.form_submit_button("➕ บันทึกรายชื่อพนักงาน"):
            if new_name.strip() == "":
                st.error("❌ กรุณากรอกชื่อพนักงานก่อนกดบันทึก")
            else:
                new_emp = {"ชื่อพนักงาน": new_name, "ทีม": new_team}
                st.session_state.employee_roster = pd.concat([st.session_state.employee_roster, pd.DataFrame([new_emp])], ignore_index=True)
                st.success(f"✔️ เพิ่มคุณ {new_name} เข้าสู่ระบบเรียบร้อย! รายชื่อจะปรากฏที่แถบด้านซ้าย")
                st.rerun()

# --- 4. แถบด้านซ้าย (Sidebar) แสดงรายชื่อพนักงานและตัวกรอง ---
st.sidebar.header("👥 รายชื่อพนักงานในระบบ")
if not st.session_state.employee_roster.empty:
    # ผู้ใช้คลิกเลือกชื่อจากตรงนี้เพื่อไปจัดงาน
    selected_employee = st.sidebar.radio(
        "👉 คลิกเลือกชื่อพนักงานเพื่อวางงาน:",
        options=st.session_state.employee_roster["ชื่อพนักงาน"].unique()
    )
    # ดึงชื่อทีมของพนักงานที่เลือกมาโดยอัตโนมัติ
    selected_team = st.session_state.employee_roster[st.session_state.employee_roster["ชื่อพนักงาน"] == selected_employee]["ทีม"].values[0]
    st.sidebar.info(f"พนักงานที่เลือก: {selected_employee}\nสังกัด: {selected_team}")
else:
    st.sidebar.warning("ยังไม่มีพนักงานในระบบ")
    selected_employee = None

# --- 5. ส่วนที่สอง: ฟอร์มวางงานตามแผนงาน (อิงจากการคลิกเลือกชื่อพนักงานซ้ายมือ) ---
if selected_employee:
    st.subheader(f"📅 ขั้นตอนที่ 2: วางแผนงานและการลาสำหรับ [ {selected_employee} ]")
    with st.form("task_assignment_form", clear_on_submit=True):
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            shift = st.selectbox("กะเวลาการทำงาน:", ["Day", "Mid", "Night"])
            entry_type = st.radio("ประเภทแผนงาน:", ["งาน (Project Work)", "การลา (Leave)"], horizontal=True)
        
        with col_t2:
            if "งาน" in entry_type:
                status_code = st.selectbox("เลือก Stage งาน:", PROJECT_STAGES).split(":")[0]
                task_cat = "งาน"
            else:
                status_code = st.selectbox("เลือกรหัสการลา:", LEAVE_CODES).split(":")[0]
                task_cat = "การลา"
            task_detail = st.text_area("รายละเอียดเนื้อข่าวงา/เหตุผลการลา:")
            
        with col_t3:
            start_date = st.date_input("วันที่เริ่มต้น:", date(2026, 5, 18))
            start_time = st.time_input("เวลาเริ่มต้น:", time(8, 0))
            end_date = st.date_input("วันที่สิ้นสุด:", date(2026, 5, 18))
            end_time = st.time_input("เวลาสิ้นสุด:", time(17, 0))
            
        if st.form_submit_button("💾 บันทึกแผนงานลงปฏิทินภาพรวม"):
            if task_detail.strip() == "":
                st.error("❌ กรุณากรอกรายละเอียดงานหรือเหตุผลการลา")
            else:
                new_task = {
                    "ชื่อพนักงาน": selected_employee,
                    "ทีม": selected_team,
                    "กะ": shift,
                    "ประเภท": task_cat,
                    "Status": status_code,
                    "รายละเอียด": task_detail,
                    "เริ่ม": datetime.combine(start_date, start_time),
                    "สิ้นสุด": datetime.combine(end_date, end_time)
                }
                st.session_state.task_schedule = pd.concat([st.session_state.task_schedule, pd.DataFrame([new_task])], ignore_index=True)
                st.success(f"✔️ บันทึกตารางงานของ {selected_employee} เรียบร้อยแล้ว!")
                st.rerun()

st.divider()

# --- 6. ส่วนล่าง: ปฏิทินและ Gantt Chart ภาพรวมทั้งเดือน อัปเดตอัตโนมัติ ---
st.subheader("🗓️ ขั้นตอนที่ 3: ปฏิทินและตารางวิเคราะห์ภาพรวมรายเดือน (Holistic Overview)")

current_schedule = st.session_state.task_schedule

if not current_schedule.empty:
    # ปรับแต่งคอลัมน์ชื่อแกน Y ให้เห็นชื่อพนักงานและทีมคู่กันชิดซ้าย
    current_schedule["Y_Label"] = current_schedule["ชื่อพนักงาน"] + " (" + current_schedule["ทีม"] + ")"
    
    # 6.1 แผนภาพ Gantt Chart แสดงกะเวลา
    fig_gantt = px.timeline(
        current_schedule, x_start="เริ่ม", x_end="สิ้นสุด", y="Y_Label", color="Status",
        color_discrete_map=STAGE_COLORS, hover_data=["รายละเอียด", "กะ"],
        title="แถบระยะเวลาทำงานและการลาแบ่งตามกะ (Day / Mid / Night)"
    )
    fig_gantt.update_yaxes(autorange="reversed", title="")
    fig_gantt.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig_gantt, use_container_width=True)
    
    # 6.2 ปฏิทินภาพรวมรายวันในเดือนนั้นๆ (Monthly Calendar Heatmap Style)
    st.markdown("#### 📅 ตารางสัญญานภาพรวมรายวันประจำเดือน (Monthly Availability Matrix)")
    current_schedule['วันที่'] = current_schedule['เริ่ม'].dt.date
    
    # สร้างตาราง Pivot สรุปภาพรวม
    cal_pivot = current_schedule.pivot_table(index='Y_Label', columns='วันที่', values='Status', aggfunc='first')
    
    # แปลงรหัสตัวอักษรเป็นตัวเลขเพื่อวาด Heatmap
    status_to_num = {k: i for i, k in enumerate(STAGE_COLORS.keys())}
    numeric_pivot = cal_pivot.replace(status_to_num)
    
    fig_cal = go.Figure(data=go.Heatmap(
        z=numeric_pivot.values,
        x=numeric_pivot.columns,
        y=numeric_pivot.index,
        colorscale=[[i/len(STAGE_COLORS), col] for i, col in enumerate(STAGE_COLORS.values())],
        showscale=False, xgap=3, ygap=3
    ))
    fig_cal.update_layout(height=250, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_cal, use_container_width=True)

    # 6.3 ตารางแก้ไข/ลบ ข้อมูลดิบด้านล่างสุด
    st.markdown("#### 🛠️ เครื่องมือแก้ไขหรือลบแผนงานในฐานข้อมูล")
    edited_df = st.data_editor(
        current_schedule[["ชื่อพนักงาน", "ทีม", "กะ", "ประเภท", "Status", "เริ่ม", "สิ้นสุด", "รายละเอียด"]],
        use_container_width=True, num_rows="dynamic", key="calendar_editor"
    )
    if st.button("💾 ยืนยันการอัปเดตข้อมูลปฏิทินทั้งหมด", type="primary"):
        # แปลงเวลากลับเป็น datetime เผื่อมีการแก้ไขในตารางดนตรี
        edited_df["เริ่ม"] = pd.to_datetime(edited_df["เริ่ม"])
        edited_df["สิ้นสุด"] = pd.to_datetime(edited_df["สิ้นสุด"])
        st.session_state.task_schedule = edited_df
        st.success("อัปเดตระบบปฏิทินเรียบร้อย!")
        st.rerun()
else:
    st.info("💡 ระบบกำลังรอข้อมูล กรุณาลงทะเบียนพนักงานและใส่แผนงานก่อนระบบจึงจะแสดงปฏิทินภาพรวมได้ครับ")
