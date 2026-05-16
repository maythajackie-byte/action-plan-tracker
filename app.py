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
    "Event/Show"
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

# --- 2. สร้างข้อมูลจำลองตามโครงสร้างที่คุณกำหนด ---
@st.cache_data
def get_mock_schedule():
    # จำลองข้อมูลงานสอดคล้องกับกะและสถานะต่างๆ ในช่วงกลางเดือนพฤษภาคม พ.ศ. 2569
    data = [
        {
            "ทีม": "Cinema Engineer", "ชื่อพนักงาน": "วิชาญ (Chan)", "กะทำงาน": "Day",
            "หมวดหมู่งาน": "Project (Bangkok)", "Stage": "P2", "รายละเอียดงาน": "ติดตั้งระบบภาพและเสียง SFW Hall 15",
            "วันที่เริ่ม": "2026-05-18 08:00", "วันที่สิ้นสุด": "2026-05-20 17:00", "ความคืบหน้า": 65, "Deadline": "2026-05-22"
        },
        {
            "ทีม": "Cinema Engineer", "ชื่อพนักงาน": "วิชาญ (Chan)", "กะทำงาน": "Night",
            "หมวดหมู่งาน": "Service (Bangkok)", "Stage": "P3", "รายละเอียดงาน": "Standby แก้ไขระบบด่วนหลังโรงภาพยนตร์ปิดทำการ",
            "วันที่เริ่ม": "2026-05-18 23:00", "วันที่สิ้นสุด": "2026-05-19 07:00", "ความคืบหน้า": 100, "Deadline": "2026-05-19"
        },
        {
            "ทีม": "Pro-AV Engineer", "ชื่อพนักงาน": "ฉัตรชัย (Dy)", "กะทำงาน": "Day",
            "หมวดหมู่งาน": "Maintenance (Outside Bangkok)", "Stage": "P3", "รายละเอียดงาน": "PM ระบบสัญญานและตู้ Rack สาขาพัทยา",
            "วันที่เริ่ม": "2026-05-19 08:00", "วันที่สิ้นสุด": "2026-05-21 17:00", "ความคืบหน้า": 40, "Deadline": "2026-05-21"
        },
        {
            "ทีม": "Broadcast Engineer", "ชื่อพนักงาน": "ณัฐดุสิต (Mumin)", "กะทำงาน": "Mid",
            "หมวดหมู่งาน": "Event/Show", "Stage": "P1", "รายละเอียดงาน": "Setup และทดสอบระบบถ่ายทอดสดงานสัมมนาศูนย์สิริกิติ์",
            "วันที่เริ่ม": "2026-05-20 15:00", "วันที่สิ้นสุด": "2026-05-20 23:00", "ความคืบหน้า": 90, "Deadline": "2026-05-20"
        },
        {
            "ทีม": "Production Team", "ชื่อพนักงาน": "กัลยกร (Namfon)", "กะทำงาน": "Day",
            "หมวดหมู่งาน": "Production (Project)", "Stage": "P0", "รายละเอียดงาน": "Brainstorm วางผังระบบห้องคอนโทรลกลางโครงการใหม่",
            "วันที่เริ่ม": "2026-05-18 08:00", "วันที่สิ้นสุด": "2026-05-18 17:00", "ความคืบหน้า": 20, "Deadline": "2026-05-25"
        },
        {
            "ทีม": "Residential Engineer", "ชื่อพนักงาน": "เอกวุฒิ (Tum)", "กะทำงาน": "Day",
            "หมวดหมู่งาน": "ลาพักร้อน", "Stage": "VL", "รายละเอียดงาน": "ลาพักร้อนประจำปี (VL)",
            "วันที่เริ่ม": "2026-05-21 08:00", "วันที่สิ้นสุด": "2026-05-22 17:00", "ความคืบหน้า": 100, "Deadline": "2026-05-22"
        },
        {
            "ทีม": "Post Production Engineer", "ชื่อพนักงาน": "กิตติศักดิ์ (Tu)", "กะทำงาน": "Day",
            "หมวดหมู่งาน": "ลาป่วย", "Stage": "SL", "รายละเอียดงาน": "ลาป่วยเนื่องจากไข้หวัดใหญ่ (SL)",
            "วันที่เริ่ม": "2026-05-18 08:00", "วันที่สิ้นสุด": "2026-05-18 17:00", "ความคืบหน้า": 100, "Deadline": "2026-05-18"
        }
    ]
    df = pd.DataFrame(data)
    df["วันที่เริ่ม"] = pd.to_datetime(df["วันที่เริ่ม"])
    df["วันที่สิ้นสุด"] = pd.to_datetime(df["วันที่สิ้นสุด"])
    return df

df = get_mock_schedule()

# --- 3. ส่วนควบคุมด้านบน (Top Action Bar) ---
col_btn1, col_btn2, col_spacer = st.columns([1.5, 1.5, 5])
with col_btn1:
    st.button("➕ กรอกข้อมูลรายบุคคล (Manual Entry)", use_container_width=True)
with col_btn2:
    st.button("📁 อัปโหลดแผนงาน (Excel Import)", use_container_width=True)

st.divider()

# --- 4. เมนูกรองข้อมูลแถบข้าง (Sidebar Filters) ---
st.sidebar.header("🛠 ตัวกรองข้อมูลผู้บริหาร")
selected_teams = st.sidebar.multiselect("เลือกทีมงาน:", options=TEAMS, default=TEAMS)
selected_stages = st.sidebar.multiselect("เลือก Stage / สถานะการลา:", options=list(STAGE_COLORS.keys()), default=list(STAGE_COLORS.keys()))

# กรองข้อมูล
filtered_df = df[(df["ทีม"].isin(selected_teams)) & (df["Stage"].isin(selected_stages))]

# --- 5. การแสดงผลตาราง Gantt Chart ---
if not filtered_df.empty:
    st.subheader("📅 ตารางวิเคราะห์งานและกะเวลา (Gantt Chart Views)")
    
    # คำนวณปี พ.ศ. สำหรับนำไปแสดงบนแกนเวลาของกราฟ
    filtered_df["แกน Y (กลุ่มทำงาน)"] = "📌 " + filtered_df["ทีม"] + " | " + filtered_df["ชื่อพนักงาน"] + " (" + filtered_df["กะทำงาน"] + ")"
    
    fig = px.timeline(
        filtered_df,
        x_start="วันที่เริ่ม",
        x_end="วันที่สิ้นสุด",
        y="แกน Y (กลุ่มทำงาน)",
        color="Stage",
        color_discrete_map=STAGE_COLORS,
        hover_data={"หมวดหมู่งาน": True, "รายละเอียดงาน": True, "ความคืบหน้า": True, "Deadline": True},
        title="ตารางปฏิบัติงานประจำสัปดาห์ แยกตามกะทำงานและระดับความยาก (พฤษภาคม พ.ศ. 2569)"
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=450,
        font=dict(family="Tahoma, sans-serif", size=13),
        xaxis=dict(title="วันและเวลาปฏิบัติงาน (Day / Mid / Night)")
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- 6. ตารางแสดงผลข้อมูลเชิงลึกแบบ Matrix รายบุคคล ---
    st.subheader("📋 ตารางสรุปรายละเอียดงานและการลาประจำสัปดาห์ (Matrix Operational View)")
    
    # ตกแต่งโครงสร้างข้อมูลสำหรับการอ่านใน Excel/Web Layout
    matrix_display = filtered_df[[
        "ทีม", "ชื่อพนักงาน", "กะทำงาน", "Stage", "หมวดหมู่งาน", "รายละเอียดงาน", "ความคืบหน้า", "Deadline"
    ]].copy()
    
    # เพิ่มฟังก์ชันแสดง Progress Bar สวยๆ ในคอลัมน์เปอร์เซ็นต์ความคืบหน้า
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
