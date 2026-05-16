import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date

# 1. Page Configuration
st.set_page_config(page_title="Engineering Master Scheduler 2.0", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #262730; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1a1c24; border-radius: 5px 5px 0 0; padding: 10px 20px; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Engineering Master Scheduler Dashboard 2.0")

# 2. Master Data
TEAMS = ["Production Team", "Cinema Engineer", "Pro-AV Engineer", "Post Production Engineer", "Broadcast Engineer", "Residential Engineer"]
PROJECT_STAGES = ["P0: Pitch/Brainstorm", "P1: Build up/Present", "P2: Installation", "P3: After Sales/MA"]
LEAVE_CODES = ["PL: ลากิจ", "VL: ลาพักร้อน", "SL: ลาป่วย", "LVP: ลาไม่รับค่าจ้าง"]

STAGE_COLORS = {
    "P0": "#F1C40F", "P1": "#E67E22", "P2": "#3498DB", "P3": "#2ECC71",
    "PL": "#95A5A6", "VL": "#9B59B6", "SL": "#E74C3C", "LVP": "#34495E"
}

# 3. Session State Data
if "schedule_df" not in st.session_state:
    # Initial Mock Data
    init_data = [
        {"ทีม": "Cinema Engineer", "พนักงาน": "วิชาญ (Chan)", "กะ": "Day", "Category": "งาน", "Status": "P2", "รายละเอียด": "Install Projector SFW", "เริ่ม": "2026-05-18 08:00", "สิ้นสุด": "2026-05-20 17:00"},
        {"ทีม": "Pro-AV Engineer", "พนักงาน": "ฉัตรชัย (Dy)", "กะ": "Day", "Category": "การลา", "Status": "VL", "รายละเอียด": "พักร้อนประจำปี", "เริ่ม": "2026-05-19 08:00", "สิ้นสุด": "2026-05-21 17:00"},
        {"ทีม": "Production Team", "พนักงาน": "กัลยกร (Namfon)", "กะ": "Mid", "Category": "งาน", "Status": "P0", "รายละเอียด": "Brainstorm Stage", "เริ่ม": "2026-05-18 15:00", "สิ้นสุด": "2026-05-18 23:00"}
    ]
    df = pd.DataFrame(init_data)
    df["เริ่ม"] = pd.to_datetime(df["เริ่ม"])
    df["สิ้นสุด"] = pd.to_datetime(df["สิ้นสุด"])
    st.session_state.schedule_df = df

if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False

# 4. Top Controls
c1, c2, _ = st.columns([1.5, 1.5, 5])
with c1:
    if st.button("➕ กรอกข้อมูลรายบุคคล (Manual Entry)"):
        st.session_state.show_add_form = not st.session_state.show_add_form
with c2:
    st.button("📁 อัปโหลดแผนงาน (Excel Import)")

# 5. Manual Entry Form
if st.session_state.show_add_form:
    with st.expander("📝 แบบฟอร์มบันทึกข้อมูลใหม่", expanded=True):
        with st.form("input_form", clear_on_submit=True):
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                team = st.selectbox("เลือกทีม:", TEAMS)
                name = st.text_input("ชื่อพนักงาน:", placeholder="ระบุชื่อ-นามสกุล")
                shift = st.selectbox("กะการทำงาน:", ["Day", "Mid", "Night"])
            with f_col2:
                entry_type = st.radio("ประเภทข้อมูล:", ["งาน (Project Work)", "การลา (Leave)"], horizontal=True)
                if "งาน" in entry_type:
                    status = st.selectbox("Stage งาน:", PROJECT_STAGES).split(":")[0]
                    cat = "งาน"
                else:
                    status = st.selectbox("รหัสการลา:", LEAVE_CODES).split(":")[0]
                    cat = "การลา"
                detail = st.text_area("รายละเอียดงาน/เหตุผลการลา:")
            with f_col3:
                d_start = st.date_input("วันที่เริ่ม:", date(2026, 5, 18))
                t_start = st.time_input("เวลาเริ่ม:", datetime.strptime("08:00", "%H:%M").time())
                d_end = st.date_input("วันที่สิ้นสุด:", date(2026, 5, 18))
                t_end = st.time_input("เวลาสิ้นสุด:", datetime.strptime("17:00", "%H:%M").time())
            
            if st.form_submit_button("บันทึกลงระบบ"):
                new_row = {
                    "ทีม": team, "พนักงาน": name, "กะ": shift, "Category": cat, "Status": status,
                    "รายละเอียด": detail, "เริ่ม": datetime.combine(d_start, t_start), "เริ่ม": datetime.combine(d_end, t_end)
                }
                st.session_state.schedule_df = pd.concat([st.session_state.schedule_df, pd.DataFrame([new_row])], ignore_index=True)
                st.success("บันทึกข้อมูลเรียบร้อย!")
                st.rerun()

st.divider()

# 6. Sidebar Filters (Separated)
st.sidebar.header("📋 ตัวกรองข้อมูล")
f_team = st.sidebar.multiselect("กรองตามทีม:", TEAMS, default=TEAMS)
f_stage = st.sidebar.multiselect("กรองตาม Stage งาน:", ["P0", "P1", "P2", "P3"], default=["P0", "P1", "P2", "P3"])
f_leave = st.sidebar.multiselect("กรองตามรหัสการลา:", ["PL", "VL", "SL", "LVP"], default=["PL", "VL", "SL", "LVP"])

# Filter Logic
all_status_filters = f_stage + f_leave
main_df = st.session_state.schedule_df
filtered_df = main_df[(main_df["ทีม"].isin(f_team)) & (main_df["Status"].isin(all_status_filters))]

# 7. Visualization: Gantt Chart (Names on Left)
st.subheader("📅 ตาราง Gantt Chart รายสัปดาห์ (ชื่อพนักงานชิดซ้าย)")
if not filtered_df.empty:
    # Format Y-axis to show Name | Team
    filtered_df["Y_Label"] = filtered_df["พนักงาน"] + " (" + filtered_df["ทีม"] + ")"
    
    fig = px.timeline(
        filtered_df, x_start="เริ่ม", x_end="สิ้นสุด", y="Y_Label", color="Status",
        color_discrete_map=STAGE_COLORS, hover_data=["รายละเอียด", "กะ"]
    )
    fig.update_yaxes(autorange="reversed", title="")
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("โปรดเลือกข้อมูลเพื่อแสดงผล")

# 8. Visualization: Monthly Overview (Calendar Style Heatmap)
st.subheader("🗓️ ภาพรวมรายเดือน (Monthly Availability Overview)")
if not filtered_df.empty:
    # Create a simple day-by-day heatmap
    filtered_df['Day'] = filtered_df['เริ่ม'].dt.date
    cal_data = filtered_df.pivot_table(index='Y_Label', columns='Day', values='Status', aggfunc='first')
    
    # We'll use Plotly Heatmap for a better visual
    # Map status to numbers for heatmap
    status_map = {s: i for i, s in enumerate(STAGE_COLORS.keys())}
    numeric_cal = cal_data.replace(status_map)
    
    fig_cal = go.Figure(data=go.Heatmap(
        z=numeric_cal.values,
        x=numeric_cal.columns,
        y=numeric_cal.index,
        colorscale=[[i/len(STAGE_COLORS), color] for i, color in enumerate(STAGE_COLORS.values())],
        showscale=False,
        xgap=2, ygap=2
    ))
    fig_cal.update_layout(height=300, margin=dict(l=20, r=20, t=10, b=10))
    st.plotly_chart(fig_cal, use_container_width=True)

# 9. Matrix Table View (Editable)
st.subheader("📋 จัดการฐานข้อมูล (แก้ไข หรือ ลบข้อมูล)")
st.info("💡 **วิธีลบข้อมูล:** ให้คลิกเลือกที่กล่องสี่เหลี่ยมด้านซ้ายสุดของแถวที่ต้องการลบ แล้วกดปุ่ม **Delete** (หรือ Backspace) บนคีย์บอร์ด")

# เปลี่ยนจาก st.dataframe เป็น st.data_editor เพื่อให้แก้ไขบนเว็บได้
edited_df = st.data_editor(
    st.session_state.schedule_df, 
    use_container_width=True,
    num_rows="dynamic",  # คำสั่งนี้คือหัวใจสำคัญที่เปิดให้ลบแถวทิ้งได้
    key="master_editor"
)

# ปุ่มกดบันทึกหลังจากลบหรือแก้ไขข้อมูลเสร็จ
if st.button("💾 ยืนยันการแก้ไข/ลบข้อมูล (อัปเดตเข้ากราฟ)", type="primary"):
    st.session_state.schedule_df = edited_df
    st.rerun()
