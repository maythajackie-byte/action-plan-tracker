import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ตั้งค่าหน้าจอ Web App เป็นแนวกว้าง
st.set_page_config(page_title="Engineering Master Scheduler 2026", layout="wide")

st.title("📊 Engineering Master Scheduler Dashboard (พ.ศ. 2569)")
st.markdown("### ระบบบริหารตารางงานและกะทำงานรายสัปดาห์ (Day / Mid / Night)")

# --- 1. เตรียมข้อมูลพื้นฐาน (Master Data) ---
TEAMS = [
    "Production Team",
    "Cinema Engineer",
    "Pro-AV Engineer",
    "Post Production Engineer",
    "Broadcast Engineer",
    "Residential Engineer"
]

TASK_CATEGORIES = [
    "Maintenance (Bangkok)", "Maintenance (Outside Bangkok)", "Maintenance (Oversea)",
    "Service (Bangkok)", "Service (Outside Bangkok)", "Service (Oversea)",
    "Project (Bangkok)", "Project (Outside Bangkok)", "Project (Oversea)",
    "Training (In-house)", "Training (Outside)",
    "Production (Project)", "Production (Other)",
    "Event/Show", "ลาพักร้อน (VL)", "ลากิจ (PL)", "ลาป่วย (SL)", "ลาไม่รับค่าจ้าง (LVP)"
]

STAGE_COLORS = {
    "P0": "#F1C40F",   # เหลือง: Pitch Project / Brainstorm
    "P1": "#E67E22",   # ส้ม: Build up / Present / Make it WIN
    "P2": "#3498DB",   # ฟ้า: Win project Installation
    "P3": "#2ECC71",   # เขียว: After sales service / MA/MT
    "PL": "#95A5A6",   # เทา: Personal Leave (ลากิจ)
    "VL": "#9B59B6",   # ม่วง: Vacation Leave (ลาพักร้อน)
    "SL": "#E74C3C",   # แดง: Sick Leave (ลาป่วย)
    "LVP": "#34495E"   # น้ำเงินเข้ม: Leave Without Pay (ลาไม่รับค่าจ้าง)
}

# --- 2. ใช้ st.session_state เป็นฐานข้อมูลในหน้าเว็บเพื่อให้บันทึกข้อมูลได้จริง ---
if "schedule_data" not in st.session_state:
    # ข้อมูลเริ่มต้นระบบ
    initial_data = [
        {
            "ทีม": "Cinema Engineer", "ชื่อพนักงาน": "วิชาญ (Chan)", "กะทำงาน": "Day",
            "หมวดหมู่งาน": "Project (Bangkok)", "Stage": "P2", "รายละเอียดงาน": "ติดตั้งระบบภาพและเสียง SFW Hall 15",
            "วันที่เริ่ม": datetime(2026, 5, 18, 8, 0), "วันที่สิ้นสุด": datetime(2026, 5, 20, 17, 0), "ความคืบหน้า": 65, "Deadline": "2026-05-22"
        },
        {
            "ทีม": "Cinema Engineer", "ชื่อพนักงาน": "วิชาญ (Chan)", "กะทำงาน": "Night",
            "หมวดหมู่งาน": "Service (Bangkok)", "Stage": "P3", "รายละเอียดงาน": "Standby แก้ไขระบบด่วนหลังโรงภาพยนตร์ปิดทำการ",
            "วันที่เริ่ม": datetime(2026, 5, 18, 23, 0), "วันที่สิ้นสุด": datetime(2026, 5, 19, 7, 0), "ความคืบหน้า": 100, "Deadline": "2026-05-19"
        },
        {
            "ทีม": "Pro-AV Engineer", "ชื่อพนักงาน": "ฉัตรชัย (Dy)", "กะทำงาน": "Day",
            "หมวดหมู่งาน": "Maintenance (Outside Bangkok)", "Stage": "P3", "รายละเอียดงาน": "PM ระบบสัญญานและตู้ Rack สาขาพัทยา",
            "วันที่เริ่ม": datetime(2026, 5, 19, 8, 0), "วันที่สิ้นสุด": datetime(2026, 5, 21, 17, 0), "ความคืบหน้า": 40, "Deadline": "2026-05-21"
        }
    ]
    st.session_state.schedule_data = pd.DataFrame(initial_data)

# ตัวแปรควบคุมการ เปิด/ปิด ของกล่องฟอร์มกรอกข้อมูล
if "show_form" not in st.session_state:
    st.session_state.show_form = False

# --- 3. ส่วนปุ่มควบคุมด้านบน (Top Action Bar) ---
col_btn1, col_btn2, col_spacer = st.columns([1.5, 1.5, 5])
with col_btn1:
    if st.button("➕ กรอกข้อมูลรายบุคคล (Manual Entry)", use_container_width=True):
        st.session_state.show_form = not st.session_state.show_form  # สลับสถานะเปิด/ปิดฟอร์ม

with col_btn2:
    st.button("📁 อัปโหลดแผนงาน (Excel Import)", use_container_width=True)

# --- 4. แสดงผลฟอร์มกรอกข้อมูลเมื่อผู้ใช้งานกดปุ่ม ---
if st.session_state.show_form:
    st.markdown("---")
    with st.form("manual_entry_form", clear_on_submit=True):
        st.subheader("📝 ฟอร์มเพิ่มข้อมูลการทำงาน / การลา รายบุคคล")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            form_team = st.selectbox("เลือกทีม:", TEAMS)
            form_name = st.text_input("ชื่อพนักงาน:", placeholder="เช่น วิชาญ (Chan)")
        with c2:
            form_shift = st.selectbox("กะทำงานของวันนั้น:", ["Day", "Mid", "Night"])
            form_stage = st.selectbox("Stage งาน / โค้ดการลา:", list(STAGE_COLORS.keys()))
        with c3:
            form_cat = st.selectbox("หมวดหมู่งาน:", TASK_CATEGORIES)
            form_progress = st.slider("ความคืบหน้า (%)", 0, 100, 0)
        with c4:
            form_deadline = st.date_input("กำหนดส่ง (Deadline):", datetime(2026, 5, 22))
            
        c5, c6 = st.columns(2)
        with c5:
            form_start = st.date_input("วันที่เริ่มงาน:", datetime(2026, 5, 18))
            form_start_time = st.time_input("เวลาเริ่มงาน:", datetime(2026, 5, 18, 8, 0).time())
        with c6:
            form_end = st.date_input("วันที่สิ้นสุดงาน:", datetime(2026, 5, 18))
            form_end_time = st.time_input("เวลาสิ้นสุดงาน:", datetime(2026, 5, 18, 17, 0).time())
            
        form_detail = st.text_area("รายละเอียดเนื้อข่าวงาและรายละเอียดเพิ่มเติม:", placeholder="พิมพ์ข้อมูลงาน เช่น ติดตั้งตู้คอนโซล...")
        
        submit_button = st.form_submit_button("💾 บันทึกข้อมูลลงตารางระบบ", use_container_width=True)
        
        if submit_button:
            if form_name.strip() == "" or form_detail.strip() == "":
                st.error("❌ กรุณากรอกชื่อพนักงานและรายละเอียดงานให้เรียบร้อยก่อนบันทึก")
            else:
                # รวมวันที่และเวลาเข้าด้วยกัน
                start_dt = datetime.combine(form_start, form_start_time)
                end_dt = datetime.combine(form_end, form_end_time)
                
                # ประกอบข้อมูลบรรทัดใหม่
                new_row = {
                    "ทีม": form_team,
                    "ชื่อพนักงาน": form_name,
                    "กะทำงาน": form_shift,
                    "หมวดหมู่งาน": form_cat,
                    "Stage": form_stage,
                    "รายละเอียดงาน": form_detail,
                    "วันที่เริ่ม": start_dt,
                    "วันที่สิ้นสุด": end_dt,
                    "ความคืบหน้า": form_progress,
                    "Deadline": str(form_deadline)
                }
                
                # บันทึกข้อมูลเพิ่มเข้าไปในฐานข้อมูลจำลองบนหน้าเว็บ
                st.session_state.schedule_data = pd.concat([st.session_state.schedule_data, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"✔️ บันทึกข้อมูลของคุณ {form_name} ลงระบบเรียบร้อยแล้ว!")
                st.session_state.show_form = False  # ปิดฟอร์มลงไปหลังจากบันทึกเสร็จ
                st.rerun()  # สั่งให้รีเฟรชหน้าจอเพื่อแสดงผลข้อมูลใหม่ทันที

st.divider()

# --- 5. เมนูกรองข้อมูลแถบข้าง (Sidebar Filters) ---
st.sidebar.header("🛠 ตัวกรองข้อมูลผู้บริหาร")
selected_teams = st.sidebar.multiselect("เลือกทีมงาน:", options=TEAMS, default=TEAMS)
selected_stages = st.sidebar.multiselect("เลือก Stage / สถานะการลา:", options=list(STAGE_COLORS.keys()), default=list(STAGE_COLORS.keys()))

# เรียกใช้ข้อมูลปัจจุบันจากฐานข้อมูลจำลองในระบบ
df = st.session_state.schedule_data

# กรองข้อมูลตามเงื่อนไขที่เลือกบน Sidebar
filtered_df = df[(df["ทีม"].isin(selected_teams)) & (df["Stage"].isin(selected_stages))]

# --- 6. การแสดงผลตาราง Gantt Chart ---
if not filtered_df.empty:
    st.subheader("📅 ตารางวิเคราะห์งานและกะเวลา (Gantt Chart Views)")
    
    filtered_df["แกน Y (กลุ่มทำงาน)"] = "📌 " + filtered_df["ทีม"] + " | " + filtered_df["ชื่อพนักงาน"] + " (" + filtered_df["กะทำงาน"] + ")"
    
    fig = px.timeline(
        filtered_df,
        x_start="วันที่เริ่ม",
        x_end="วันที่สิ้นสุด",
        y="แกน Y (กลุ่มทำงาน)",
        color="Stage",
        color_discrete_map=STAGE_COLORS,
        hover_data={"หมวดหมู่งาน": True, "รายละเอียดงาน": True, "ความคืบหน้า": True, "Deadline": True},
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=450,
        font=dict(family="Tahoma, sans-serif", size=13),
        xaxis=dict(title="วันและเวลาปฏิบัติงาน (Day / Mid / Night)")
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- 7. ตารางแสดงผลข้อมูลเชิงลึกแบบ Matrix รายบุคคล ---
    st.subheader("📋 ตารางสรุปรายละเอียดงานและการลาประจำสัปดาห์ (Matrix Operational View)")
    
    matrix_display = filtered_df[[
        "ทีม", "ชื่อพนักงาน", "กะทำงาน", "Stage", "หมวดหมู่งาน", "รายละเอียดงาน", "ความคืบหน้า", "Deadline"
    ]].copy()
    
    matrix_display["ความคืบหน้า (%)"] = matrix_display["ความคืบหน้า"].apply(lambda x: f"{x}%")
    matrix_display = matrix_display.drop(columns=["ความคืบหน้า"])
    
    st.dataframe(
        matrix_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Stage": st.column_config.TextColumn("Stage / โค้ดลา"),
            "ความคืบหน้า (%)": st.column_config.TextColumn("ความคืบหน้า"),
            "Deadline": st.column_config.TextColumn("กำหนดส่ง (Deadline)")
        }
    )
else:
    st.warning("ไม่พบข้อมูลที่ตรงกับเงื่อนไขการกรอง โปรดเลือกทีมงานหรือสถานะใหม่อีกครั้งที่แถบเมนูด้านซ้าย")
