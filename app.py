import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from streamlit_calendar import calendar
import io

# ตั้งค่าการแสดงผลหน้าจอแบบแนวกว้าง (Enterprise Layout)
st.set_page_config(page_title="Engineering Master Scheduler 6.2", layout="wide")

st.title("📊 Engineering Master Scheduler Dashboard 6.2")
st.markdown("### ระบบบริหารแผนงานประจำปี และ Interactive Calendar")

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
    "Event/Show", "R&D", "Others"
]

PROJECT_STAGES = ["P0:", "P1:", "P2:", "P3:", "Others"]
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
       
        {"ชื่อพนักงาน": "บาตท์ โฮ  (Bart)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "วิชาญ  (Chan)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "กิตติศักดิ์   (Tu)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "อิทธิรัตน์  (Koh)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "เอกวุฒิ  (Tum)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "อภิชาติ  (Tum)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "ยศิธร  (Van)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "ศิวัช   (Champ)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "ณัฐพล  (Nui)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "ชาติสยาม (ญนนท)", "ทีม": "Cinema Engineer"},
        {"ชื่อพนักงาน": "ณัฐดุสิต  (Mint)", "ทีม": "Cinema Engineer"}, 
        {"ชื่อพนักงาน": "คเชนทร์   (Tae)", "ทีม": "Cinema Engineer"},

        {"ชื่อพนักงาน": "นิรุตต์ (Rut)", "ทีม": "Cinema Engineer"},

        {"ชื่อพนักงาน": "อดิเรก   (Rek)", "ทีม": "Production Team"},
        {"ชื่อพนักงาน": "วรทัศน์   (Awun)", "ทีม": "Production Team"},
        {"ชื่อพนักงาน": "ชำนาญ   (Pui)", "ทีม": "Production Team"},
        {"ชื่อพนักงาน": "ซอ ยาว (Saw Yawr)", "ทีม": "Production Team"},
        {"ชื่อพนักงาน": "ยุรนันทน์ (Bird)", "ทีม": "Production Team"},
        {"ชื่อพนักงาน": "ณรงค์ฤทธิ์ (Rit)", "ทีม": "Production Team"},
        {"ชื่อพนักงาน": "ทักษ์ดนัย (Nai)", "ทีม": "Production Team"},
        {"ชื่อพนักงาน": "พีระศักดิ์ (Foam)", "ทีม": "Production Team"},       
        {"ชื่อพนักงาน": "ชัยวุฒิ (Pump)", "ทีม": "Production Team"},         

    ])

if "task_schedule" not in st.session_state:
    init_tasks = [
        #{"ชื่อพนักงาน": "วิชาญ (Chan)", "ทีม": "Cinema Engineer", "กะ": "Day", "ประเภท": "แผนงาน", "Status": "P2", "หมวดหมู่": "Project (Bangkok)", "ชื่องาน": "ติดตั้งระบบภาพ", "รายละเอียด": "ติดตั้งระบบภาพ SFW Hall 15", "เริ่ม": "2026-05-18 09:00", "สิ้นสุด": "2026-05-20 18:00"},
        {"ชื่อพนักงาน": "คุณทดสอบ (Test)", "ทีม": "Pro-AV Engineer", "กะ": "Day", "ประเภท": "การลา", "Status": "VL", "หมวดหมู่": "ลาพักร้อน", "ชื่องาน": "แจ้งลาพักร้อน", "รายละเอียด": "พักร้อนประจำปี", "เริ่ม": "2026-05-13 09:00", "สิ้นสุด": "2026-05-15 18:00"},
        #{"ชื่อพนักงาน": "กัลยกร (Namfon)", "ทีม": "Production Team", "กะ": "Mid", "ประเภท": "แผนงาน", "Status": "P0", "หมวดหมู่": "Production (Project)", "ชื่องาน": "Brainstorm Stage", "รายละเอียด": "ประชุมทีมโปรเจกต์ใหม่", "เริ่ม": "2026-05-18 15:00", "สิ้นสุด": "2026-05-18 23:00"}
    ]
    df_tasks = pd.DataFrame(init_tasks)
    df_tasks["เริ่ม"] = pd.to_datetime(df_tasks["เริ่ม"])
    df_tasks["สิ้นสุด"] = pd.to_datetime(df_tasks["สิ้นสุด"])
    st.session_state.task_schedule = df_tasks


# =========================================================
# 👤 ขั้นตอนที่ 1: ลงทะเบียนรายชื่อพนักงานใหม่
# =========================================================
with st.expander("👤 ลงทะเบียนรายชื่อพนักงานใหม่", expanded=False):
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

# =========================================================
# 👥 แถบเครื่องมือแสดงรายชื่อพนักงานด้านซ้ายมือ (Sidebar)
# =========================================================
st.sidebar.header("👥 รายชื่อพนักงาน")
roster_df = st.session_state.employee_roster
roster_df["Display_Label"] = roster_df["ชื่อพนักงาน"] + " : " + roster_df["ทีม"]

selected_label = st.sidebar.radio(
    "👉 คลิกเลือกชื่อพนักงานเพื่อจัดการงาน:",
    options=roster_df["Display_Label"].unique()
)

current_emp_name = roster_df[roster_df["Display_Label"] == selected_label]["ชื่อพนักงาน"].values[0]
current_emp_team = roster_df[roster_df["Display_Label"] == selected_label]["ทีม"].values[0]

# =========================================================
# 🛠️ ขั้นตอนที่ 2: จัดการตารางงานและการลา
# =========================================================
st.subheader(f"🛠️ จัดการตารางเวลาของ [ {current_emp_name} ]")

entry_type = st.radio(
    "เลือกระบบที่ต้องการบันทึกข้อมูล:", 
    ["💼 วางแผนงาน (Work Plan)", "🏖️ แจ้งลา (Leave)"], 
    horizontal=True
)

with st.form("assignment_form", clear_on_submit=True):
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        shift_choice = st.selectbox("กะเวลาการทำงาน:", ["Day", "Mid", "Night"])
        task_title = st.text_input("ชื่องาน / หัวข้อการแจ้งลา:")
        
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
            status_code = st.selectbox("แจ้งลา:", LEAVE_OPTIONS).split(":")[0]
            task_detail = st.text_area("เหตุผลการลา:")
            work_cat = "การลาหยุดพักผ่อน"
        
    with col_f3:
        start_d = st.date_input("วันที่เริ่มต้น:", date(2026, 5, 18))
        start_t = st.time_input("เวลาเริ่มต้น:", time(9, 0), step=1800)
        end_d = st.date_input("วันที่สิ้นสุด:", date(2026, 5, 18))
        end_t = st.time_input("เวลาสิ้นสุด:", time(18, 0), step=1800)
        
    if st.form_submit_button("💾 บันทึกลงปฏิทิน"):
        if task_detail.strip() == "" or task_title.strip() == "":
            st.error("❌ กรุณากรอกชื่องานและรายละเอียดข้อมูลให้ครบถ้วน")
        else:
            new_record = {
                "ชื่อพนักงาน": current_emp_name,
                "ทีม": current_emp_team,
                "กะ": shift_choice,
                "ประเภท": record_cat,
                "Status": status_code,
                "หมวดหมู่": work_cat,
                "ชื่องาน": task_title,
                "รายละเอียด": task_detail,
                "เริ่ม": datetime.combine(start_d, start_t),
                "สิ้นสุด": datetime.combine(end_d, end_t)
            }
            st.session_state.task_schedule = pd.concat([st.session_state.task_schedule, pd.DataFrame([new_record])], ignore_index=True)
            st.success("บันทึกตารางลงปฏิทินสำเร็จ!")
            st.rerun()

st.divider()

# =========================================================
# ฟังก์ชันแปลงข้อมูลสำหรับการสร้างปฏิทิน
# =========================================================
def df_to_calendar_events(df):
    events = []
    for _, row in df.iterrows():
        task_name = row.get('ชื่องาน', 'ไม่มีชื่องาน')
        title = f"[{row['Status']}] {row['ชื่อพนักงาน']} - {task_name}"
        bg_color = STAGE_COLORS.get(row['Status'], "#333333")
        
        events.append({
            "title": title,
            "start": row["เริ่ม"].strftime("%Y-%m-%dT%H:%M:%S"),
            "end": row["สิ้นสุด"].strftime("%Y-%m-%dT%H:%M:%S"),
            "backgroundColor": bg_color,
            "borderColor": bg_color,
            "extendedProps": {
                "empName": row['ชื่อพนักงาน'],
                "teamName": row['ทีม'],
                "shift": row['กะ'],
                "category": row['หมวดหมู่'],
                "status": row['Status'],
                "taskName": task_name,
                "details": row['รายละเอียด'],
                "timeStr": f"{row['เริ่ม'].strftime('%H:%M')} - {row['สิ้นสุด'].strftime('%H:%M')}"
            }
        })
    return events

# รูปแบบคำสั่งการตั้งค่าการทำงานของหน้าต่างปฏิทิน (ปิดโหมดแจ้งเตือน JavaScript)
calendar_options = {
    "initialView": "dayGridMonth",
    "initialDate": "2026-05-01",
    "firstDay": 0,
    "displayEventTime": False,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek"
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "24:00:00"
}

current_data = st.session_state.task_schedule

# =========================================================
# 🗓️ ส่วนแสดงผลปฏิทินภาพรวม (All Staff)
# =========================================================
st.subheader("🗓️ ขั้นตอนที่ 3: ปฏิทินภาพรวมและแผนภูมิสรุปรายบุคคล")

if not current_data.empty:
    st.markdown("#### 📅 ปฏิทินกลางสำหรับตรวจสอบทรัพยากรพนักงานทั้งหมด (All Staff Calendar)")
    all_events = df_to_calendar_events(current_data)
    
    # วาดปฏิทินหลัก และเก็บค่าการคลิก
    cal_result = calendar(events=all_events, options=calendar_options, key="main_calendar_view")
    
    # สร้างกล่อง Popup รายละเอียดเมื่อมีการคลิกที่แถบงานในปฏิทิน
    if cal_result.get("eventClick"):
        event_data = cal_result["eventClick"]["event"]
        props = event_data.get("extendedProps", {})
        
        with st.container(border=True): 
            st.markdown(f"### 📋 รายละเอียด: {event_data.get('title', 'ไม่มีชื่องาน')}")
            pc1, pc2 = st.columns(2)
            with pc1:
                st.write(f"**👤 พนักงาน:** {props.get('empName', '-')} ({props.get('teamName', '-')})")
                st.write(f"**⏰ เวลาปฏิบัติงาน:** {props.get('timeStr', '-')} [กะ: {props.get('shift', '-')}]")
            with pc2:
                st.write(f"**🏷️ หมวดหมู่:** {props.get('status', '-')} | {props.get('category', '-')}")
            
            st.info(f"**📝 รายละเอียดเนื้อหางาน/เหตุผลการลา:**\n\n{props.get('details', 'ไม่มีรายละเอียดเพิ่มเติม')}")
            
    st.markdown("---")
    
    # =========================================================
    # 🔍 ปฏิทินเฉพาะบุคคล (Personal Calendar)
    # =========================================================
    st.subheader(f"👤 ปฏิทินตารางเวลาเฉพาะบุคคลของ: **{current_emp_name}**")
    personal_data = current_data[current_data["ชื่อพนักงาน"] == current_emp_name]
    
    if not personal_data.empty:
        personal_events = df_to_calendar_events(personal_data)
        calendar(events=personal_events, options=calendar_options, key="personal_calendar_view")
    else:
        st.info(f"💡 คุณ {current_emp_name} ยังไม่มีข้อมูลตารางงานในระบบ")

    # =========================================================
    # 💾 ระบบ Export ข้อมูล, เมนูแก้ไขแบบฟอร์ม, และตารางแก้ไขข้อมูลดิบ
    # =========================================================
    st.markdown("---")
    st.subheader("🛠️ จัดการข้อมูลดิบ นำออกไฟล์ และอัปเดตงาน")
    
    # ส่วนดาวน์โหลดไฟล์
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            current_data.to_excel(writer, index=False, sheet_name='Master_Schedule')
        
        st.download_button(
            label="📥 ดาวน์โหลดตารางข้อมูลเป็น Excel (.xlsx)",
            data=buffer,
            file_name="Engineering_Schedule_2026.xlsx",
            mime="application/vnd.ms-excel",
            type="primary",
            use_container_width=True
        )
    with col_dl2:
        csv = current_data.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 ดาวน์โหลดตารางข้อมูลเป็น CSV",
            data=csv,
            file_name="Engineering_Schedule_2026.csv",
            mime="text/csv",
            use_container_width=True
        )

    # 📝 เมนูฟอร์มแก้ไขข้อมูลภารกิจเดิม
    with st.expander("✏️ เมนูฟอร์มแก้ไขข้อมูลแผนงาน/การลาเดิม"):
        # สร้างรายการตัวเลือกงานดึงจากดัชนีของข้อมูล
        current_data['Edit_Label'] = current_data.index.astype(str) + " : [" + current_data['ชื่อพนักงาน'] + "] " + current_data.get('ชื่องาน', current_data['รายละเอียด']).str.slice(0, 30)
        selected_edit_label = st.selectbox("เลือกรายการงานที่ต้องการปรับปรุงแก้ไข:", current_data['Edit_Label'].unique())
        
        edit_idx = int(selected_edit_label.split(" : ")[0])
        edit_row = current_data.loc[edit_idx]
        
        st.markdown(f"**กำลังแก้ไขรายการของ:** {edit_row['ชื่อพนักงาน']} ({edit_row['ทีม']})")
        
        with st.form("edit_data_form"):
            ec1, ec2, ec3 = st.columns(3)
            with ec1:
                e_title = st.text_input("แก้ไขชื่องาน/หัวข้อการลา:", value=edit_row.get('ชื่องาน', ''))
                e_shift = st.selectbox("แก้ไขกะทำงาน:", ["Day", "Mid", "Night"], index=["Day", "Mid", "Night"].index(edit_row['กะ']))
            with ec2:
                e_status = st.selectbox("แก้ไขโค้ดสถานะ (เช่น P0, P2, VL):", list(STAGE_COLORS.keys()), index=list(STAGE_COLORS.keys()).index(edit_row['Status']))
                e_detail = st.text_area("แก้ไขเนื้อหารายละเอียดงาน/เหตุผล:", value=edit_row['รายละเอียด'])
            with ec3:
                e_start = st.date_input("แก้ไขวันเริ่มต้น:", value=pd.to_datetime(edit_row['เริ่ม']).date())
                e_end = st.date_input("แก้ไขวันสิ้นสุด:", value=pd.to_datetime(edit_row['สิ้นสุด']).date())
            
            if st.form_submit_button("💾 บันทึกการอัปเดตข้อมูลปรับปรุง"):
                st.session_state.task_schedule.at[edit_idx, 'ชื่องาน'] = e_title
                st.session_state.task_schedule.at[edit_idx, 'กะ'] = e_shift
                st.session_state.task_schedule.at[edit_idx, 'Status'] = e_status
                st.session_state.task_schedule.at[edit_idx, 'รายละเอียด'] = e_detail
                st.session_state.task_schedule.at[edit_idx, 'เริ่ม'] = pd.to_datetime(e_start)
                st.session_state.task_schedule.at[edit_idx, 'สิ้นสุด'] = pd.to_datetime(e_end)
                
                st.success("🎉 อัปเดตการแก้ไขข้อมูลไปยังปฏิทินกลางเรียบร้อยแล้ว!")
                st.rerun()

    # ตารางแบบดิบสำหรับลบข้อมูล
    with st.expander("🗑️ ลบหรือแก้ไขรายการโดยตรงจากตารางฐานข้อมูล"):
        st.info("💡 เลือกแถวที่ต้องการและกดปุ่ม Delete บนคีย์บอร์ดเพื่อลบข้อมูล")
        edited_df = st.data_editor(current_data.drop(columns=['Edit_Label']), use_container_width=True, num_rows="dynamic")
        if st.button("💾 ยืนยันการเปลี่ยนแปลงข้อมูลในตาราง"):
            edited_df["เริ่ม"] = pd.to_datetime(edited_df["เริ่ม"])
            edited_df["สิ้นสุด"] = pd.to_datetime(edited_df["สิ้นสุด"])
            st.session_state.task_schedule = edited_df
            st.success("อัปเดตระบบปฏิทินเรียบร้อย!")
            st.rerun()

else:
    st.info("ระบบกำลังรอข้อมูลเริ่มต้น...")
