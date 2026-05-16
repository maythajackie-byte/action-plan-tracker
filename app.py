import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, time

# ตั้งค่าการแสดงผลแบบแนวกว้าง
st.set_page_config(page_title="Engineering Master Scheduler 4.0", layout="wide")

st.title("📊 Engineering Master Scheduler Dashboard 4.0")
st.markdown("### ระบบบริหารแผนงานประจำปี พ.ศ. 2569")

# --- 1. ข้อมูลโครงสร้างหลัก (Master Data) ---
TEAMS = [
    "Production Team", "Cinema Engineer", "Pro-AV Engineer", 
    "Post Production Engineer", "Broadcast Engineer", "Residential Engineer"
]

# หมวดหมู่งานหลักแยกพื้นที่ตามข้อกำหนดของคุณ
TASK_CATEGORIES = [
    "Maintenance (Bangkok)", "Maintenance (Outside Bangkok)", "Maintenance (Oversea)",
    "Service (Bangkok)", "Service (Outside Bangkok)", "Service (Oversea)",
    "Project (Bangkok)", "Project (Outside Bangkok)", "Project (Oversea)",
    "Training (In-house)", "Training (Outside)",
    "Production (Project)", "Production (Other)",
    "Event/Show"
]

PROJECT_STAGES = ["P0: Pitch/Brainstorm", "P1: Build up/Present", "P2: Installation", "P3: After Sales/Service/MA"]
LEAVE_OPTIONS = ["PL: ลากิจ (Personal Leave)", "VL: ลาพักร้อน (Vacation Leave)", "SL: ลาป่วย (Sick Leave)", "LVP: ลาไม่รับค่าจ้าง (Leave Without Pay)"]

# โค้ดสีมาตรฐานของระบบสเกดดูล
STAGE_COLORS = {
    "P0": "#F1C40F", "P1": "#E67E22", "P2": "#3498DB", "P3": "#2ECC71",
    "PL": "#95A5A6", "VL": "#9B59B6", "SL": "#E74C3C", "LVP": "#34495E"
}

# --- 2. การจัดเตรียมฐานข้อมูลเบื้องต้น (Initial Session State) ---
# ขั้นตอนที่ 1: ใส่รายชื่อและสังกัดพนักงานลงในโค้ดโดยตรงบางส่วน
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

# ใส่แผนงานเริ่มต้นบางส่วนเพื่อให้ปฏิทินแสดงผลแถบสีสวยงาม
if "task_schedule" not in st.session_state:
    init_tasks = [
        {"ชื่อพนักงาน": "วิชาญ (Chan)", "ทีม": "Cinema Engineer", "กะ": "Day", "ประเภท": "แผนงาน", "Status": "P2", "หมวดหมู่": "Project (Bangkok)", "รายละเอียด": "ติดตั้งระบบภาพ SFW Hall 15", "เริ่ม": "2026-05-18 08:00", "สิ้นสุด": "2026-05-20 17:00"},
        {"ชื่อพนักงาน": "ฉัตรชัย (Dy)", "ทีม": "Broadcast Engineer", "กะ": "Day", "ประเภท": "การลา", "Status": "VL", "หมวดหมู่": "ลาพักร้อน", "รายละเอียด": "พักร้อนประจำปี", "เริ่ม": "2026-05-19 08:00", "สิ้นสุด": "2026-05-21 17:00"},
        {"ชื่อพนักงาน": "กัลยกร (Namfon)", "ทีม": "Production Team", "กะ": "Mid", "ประเภท": "แผนงาน", "Status": "P0", "หมวดหมู่": "Production (Project)", "รายละเอียด": "Brainstorm Stage โครงการใหม่", "เริ่ม": "2026-05-18 15:00", "สิ้นสุด": "2026-05-18 23:00"},
        {"ชื่อพนักงาน": "หทัยชนก (Liew)", "ทีม": "Cinema Engineer", "กะ": "Night", "ประเภท": "แผนงาน", "Status": "P1", "หมวดหมู่": "Event/Show", "รายละเอียด": "Setup งาน Architect'26", "เริ่ม": "2026-05-21 22:00", "สิ้นสุด": "2026-05-22 06:00"}
    ]
    df_tasks = pd.DataFrame(init_tasks)
    df_tasks["เริ่ม"] = pd.to_datetime(df_tasks["เริ่ม"])
    df_tasks["สิ้นสุด"] = pd.to_datetime(df_tasks["สิ้นสุด"])
    st.session_state.task_schedule = df_tasks

# --- 3. แถบเครื่องมือและรายชื่อพนักงานด้านซ้ายมือ (Sidebar Layout) ---
st.sidebar.header("👥 รายชื่อพนักงานและสังกัด")

# ปรับให้ต่อท้ายด้วย : ชื่อทีม เพื่อระบุสังกัดในการเลือก
roster_df = st.session_state.employee_roster
roster_df["Display_Label"] = roster_df["ชื่อพนักงาน"] + " : " + roster_df["ทีม"]

selected_label = st.sidebar.radio(
    "👉 คลิกเลือกชื่อพนักงานเพื่อจัดการงาน:",
    options=roster_df["Display_Label"].unique()
)

# ดึงข้อมูลพนักงานและทีมปัจจุบันแยกออกมาใช้งานต่อ
current_emp_name = roster_df[roster_df["Display_Label"] == selected_label]["ชื่อพนักงาน"].values[0]
current_emp_team = roster_df[roster_df["Display_Label"] == selected_label]["ทีม"].values[0]

# ฟอร์มเพิ่มพนักงานใหม่เพิ่มเติมภายหลัง
with st.sidebar.expander("➕ เพิ่มรายชื่อพนักงานใหม่"):
    with st.form("add_employee_form", clear_on_submit=True):
        add_name = st.text_input("ชื่อพนักงาน:")
        add_team = st.selectbox("เลือกทีม:", TEAMS)
        if st.form_submit_button("บันทึกรายชื่อ"):
            if add_name.strip() != "":
                new_emp = {"ชื่อพนักงาน": add_name, "ทีม": add_team}
                st.session_state.employee_roster = pd.concat([st.session_state.employee_roster, pd.DataFrame([new_emp])], ignore_index=True)
                st.success("เพิ่มรายชื่อสำเร็จ!")
                st.rerun()

# --- 4. ขั้นตอนที่ 2: ฟอร์มจัดการตารางงานและการลา (แยกประเภทชัดเจน) ---
st.subheader(f"🛠️ จัดการแผนงานและการลาของ [ {current_emp_name} ]")
with st.form("assignment_form", clear_on_submit=True):
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        shift_choice = st.selectbox("กะเวลาการทำงาน:", ["Day", "Mid", "Night"])
        entry_type = st.radio("เลือกประเภทการบันทึก:", ["วางแผนงาน (Work Plan)", "บันทึกการลา (Leave)"], horizontal=True)
        
    with col_f2:
        # เงื่อนไขเปลี่ยนตัวเลือกตามประเภทที่คลิกเลือก
        if "วางแผนงาน" in entry_type:
            status_code = st.selectbox("เลือกระดับ Stage งาน:", PROJECT_STAGES).split(":")[0]
            work_cat = st.selectbox("หมวดหมู่งานตามพื้นที่:", TASK_CATEGORIES)
            record_cat = "แผนงาน"
        else:
            status_code = st.selectbox("เลือกประเภทโค้ดการลา:", LEAVE_OPTIONS).split(":")[0]
            work_cat = "การลาหยุดพักผ่อน"
            record_cat = "การลา"
            
        task_detail = st.text_area("รายละเอียดเนื้อหางานหรือเหตุผลการลา:")
        
    with col_f3:
        start_d = st.date_input("วันที่เริ่มต้น:", date(2026, 5, 18))
        start_t = st.time_input("เวลาเริ่มต้น:", time(8, 0))
        end_d = st.date_input("วันที่สิ้นสุด:", date(2026, 5, 18))
        end_t = st.time_input("เวลาสิ้นสุด:", time(17, 0))
        
    if st.form_submit_button("💾 บันทึกตารางงานเข้าปฏิทินกลาง"):
        if task_detail.strip() == "":
            st.error("❌ กรุณากรอกรายละเอียดเนื้อหางานหรือเหตุผล")
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
            st.success("บันทึกข้อมูลเรียบร้อย!")
            st.rerun()

st.divider()

# --- 5. ขั้นตอนที่ 3: ส่วนแสดงผลปฏิทินรวมรายเดือน (ขึ้นแสดงก่อนอันดับแรกสุด) ---
st.subheader("🗓️ ปฏิทินภาพรวมแผนงานและการลาประจำเดือน (Monthly Matrix)")

current_data = st.session_state.task_schedule

if not current_data.empty:
    current_data["Label_Side"] = current_data["ชื่อพนักงาน"] + " (" + current_data["ทีม"] + ")"
    current_data['วันที่'] = current_data['เริ่ม'].dt.date
    
    # วาดปฏิทิน Matrix รวมก่อนเป็นอันดับแรกตามที่คุณแจ้ง
    cal_pivot = current_data.pivot_table(index='Label_Side', columns='วันที่', values='Status', aggfunc='first')
    status_mapping = {k: i for i, k in enumerate(STAGE_COLORS.keys())}
    numeric_cal = cal_pivot.replace(status_mapping)
    
    fig_matrix = go.Figure(data=go.Heatmap(
        z=numeric_cal.values,
        x=numeric_cal.columns,
        y=numeric_cal.index,
        colorscale=[[i/len(STAGE_COLORS), color] for i, color in enumerate(STAGE_COLORS.values())],
        showscale=False, xgap=4, ygap=4
    ))
    fig_matrix.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_matrix, use_container_width=True)
    
    # --- 6. แผนภูมิ Gantt Chart สรุปงานเจาะลึกเฉพาะบุคคล (แสดงด้านล่างเมื่อมีการคลิกเลือกชื่อ) ---
    st.markdown(f"#### 🔍 แผนภูมิ Gantt Chart ประจำสัปดาห์เฉพาะบุคคลของ: **{current_emp_name}**")
    
    # กรองเอาเฉพาะข้อมูลของคนที่คลิกจากเมนูด้านซ้ายมาวาดกราฟเส้นเวลา
    personal_data = current_data[current_data["ชื่อพนักงาน"] == current_emp_name]
    
    if not personal_data.empty:
        fig_gantt = px.timeline(
            personal_data, x_start="เริ่ม", x_end="สิ้นสุด", y="กะ", color="Status",
            color_discrete_map=STAGE_COLORS, hover_data=["หมวดหมู่", "รายละเอียด"],
            title=f"ตารางงานและกะปฏิบัติงาน (Day / Mid / Night) ของ {current_emp_name}"
        )
        fig_gantt.update_yaxes(autorange="reversed")
        fig_gantt.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_gantt, use_container_width=True)
    else:
        st.info(f"💡 คุณ {current_emp_name} ยังไม่มีตารางงานหรือรายการลาถูกบันทึกในระบบในขณะนี้")
        
    # --- 7. ตารางจัดการแก้ไขข้อมูล ---
    with st.expander("🛠️ ตารางแก้ไขหรือลบรายการดิบในระบบ"):
        edited_df = st.data_editor(current_data[["ชื่อพนักงาน", "ทีม", "กะ", "ประเภท", "Status", "หมวดหมู่", "เริ่ม", "สิ้นสุด", "รายละเอียด"]], use_container_width=True, num_rows="dynamic")
        if st.button("💾 ยืนยันข้อมูลที่มีการเปลี่ยนแปลง"):
            edited_df["เริ่ม"] = pd.to_datetime(edited_df["เริ่ม"])
            edited_df["สิ้นสุด"] = pd.to_datetime(edited_df["สิ้นสุด"])
            st.session_state.task_schedule = edited_df
            st.success("ข้อมูลปฏิทินอัปเดตเรียบร้อยแล้ว!")
            st.rerun()
else:
    st.info("ระบบยังไม่มีข้อมูลแผนงานโปรดใส่ข้อมูลเพื่อทดสอบการใช้งาน")
