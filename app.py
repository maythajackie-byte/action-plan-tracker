import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- ปรับแต่ง CSS ---
st.markdown("""
    <style>
    /* ปรับแต่งกล่อง Metric ให้เด่นชัดอ่านง่าย */
    [data-testid="stMetric"] {
        background-color: #ffffff; /* พื้นหลังขาว */
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #0b5345; /* แถบสีเขียวเข้มด้านซ้าย */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* ปรับสีตัวเลข Metric ให้เป็นสีเขียวเข้ม */
    [data-testid="stMetricValue"] {
        color: #0b5345 !important;
        font-weight: bold;
    }
    /* ปรับสีหัวข้อ Metric ให้เป็นสีเทาเข้ม */
    [data-testid="stMetricLabel"] {
        color: #333333 !important;
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. แยกรายชื่อพนักงานตามกลุ่ม
SALES_LIST = ["None", "CB : Chanunkarn", "AW : Apasri", "TH : Thanyhathorn"]

ENG_LIST = [
    "None", "CK : Chatchai", "BS : Boonchob", "PU : Pankrich", "MS : Maytha", 
    "KC : Kiattisak", "DR : Danuphop", "SB : Sarawut", "KL : Kongphop",
    "DS : Decha", "PT : Patjitra", "WS : Worawut", "RO : Ronnarit",
    "NI : Nutwarot", "SK : Sirisak", "KI : Kathathep", "CA : Chatchawan",
    "NM : Nithithorn", "PA : Phaisan", "CN : Chainarong", "PH : Parawee",
    "TC : Totsapol", "WO : Watcharakorn", "VP : Veeraphat", "MK : Monrak",
    "PL : Preecha", "NC : Nattipong"
]

# 3. จัดการข้อมูล
DATA_FILE = "action_plan_2026.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # ตรวจสอบคอลัมน์ (รองรับโครงสร้างใหม่ที่มีทั้ง Sales และ Eng)
        for col in ["Sales PIC", "Eng PIC"]:
            if col not in df.columns: df[col] = "None"
        df['Start Date'] = pd.to_datetime(df['Start Date']).dt.date
        df['End Date'] = pd.to_datetime(df['End Date']).dt.date
        return df
    return pd.DataFrame(columns=["Dept", "Activity", "Target", "Sales PIC", "Eng PIC", "Support", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# Session State สำหรับการแก้ไข
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# 4. Header
st.title("📋 2026 Follow up & Action Plan")
st.markdown("---")

# 5. Sidebar (แยก 2 กล่อง PIC ข้างกัน)
with st.sidebar:
    st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    val = df.iloc[st.session_state.edit_index] if st.session_state.edit_mode else None
    
    with st.form("action_form", clear_on_submit=True):
        dept = st.selectbox("Department", ["Distri-Pro", "Post", "Broadcast", "Residential", "Cinema", "ENG-Center"],
                            index=["Distri-Pro", "Post", "Broadcast", "Residential", "Cinema", "ENG-Center"].index(val['Dept']) if val is not None else 0)
        
        activity = st.text_area("Action Plan & Activity", value=val['Activity'] if val is not None else "")
        
        # --- จุดที่ปรับปรุง: แยก 2 กล่อง PIC ข้างกัน ---
        col_pic1, col_pic2 = st.columns(2)
        sales_pic = col_pic1.selectbox("Sales PIC", SALES_LIST, 
                                       index=SALES_LIST.index(val['Sales PIC']) if val is not None and val['Sales PIC'] in SALES_LIST else 0)
        eng_pic = col_pic2.selectbox("Engineer PIC", ENG_LIST, 
                                     index=ENG_LIST.index(val['Eng PIC']) if val is not None and val['Eng PIC'] in ENG_LIST else 0)
        
        col_s1, col_s2 = st.columns(2)
        priority = col_s1.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(val['Priority']) if val is not None else 1)
        p_status = col_s2.selectbox("Project Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(val['Project Status']) if val is not None else 1)
        
        col_d1, col_d2 = st.columns(2)
        start_date = col_d1.date_input("Start Date", value=val['Start Date'] if val is not None else datetime.now().date())
        end_date = col_d2.date_input("End Date", value=val['End Date'] if val is not None else datetime.now().date())
        
        status = st.selectbox("Status", ["Planning", "In Progress", "Completed", "Delayed"], 
                              index=["Planning", "In Progress", "Completed", "Delayed"].index(val['Status']) if val is not None else 0)
        progress = st.slider("Progress (%)", 0, 100, int(val['Progress']) if val is not None else 0)
        
        if st.form_submit_button("💾 บันทึกข้อมูล"):
            new_data = {
                "Dept": dept, "Activity": activity, "Sales PIC": sales_pic, "Eng PIC": eng_pic,
                "Status": status, "Progress": progress, "Start Date": start_date, "End Date": end_date,
                "Priority": priority, "Project Status": p_status, "Target": val['Target'] if val is not None else "-", "Support": val['Support'] if val is not None else "-"
            }
            if st.session_state.edit_mode:
                df.iloc[st.session_state.edit_index] = new_data
                st.session_state.edit_mode = False
            else:
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            save_data(df)
            st.rerun()

    if st.session_state.edit_mode and st.button("❌ ยกเลิก"):
        st.session_state.edit_mode = False
        st.rerun()

# 6. Main Dashboard Display
if not df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("งานทั้งหมด", len(df))
    m2.metric("เฉลี่ยความคืบหน้า", f"{df['Progress'].mean():.1f}%")
    m3.metric("งานระดับ P0", len(df[df['Project Status'] == 'P0']))

    st.markdown("---")
    st.subheader("📄 รายละเอียดแผนงาน")
    for index, row in df.iterrows():
        # แสดงชื่อทั้ง Sales และ Eng ที่หัวข้อถ้ามีข้อมูล
        pic_display = f"S: {row['Sales PIC']} | E: {row['Eng PIC']}"
        with st.expander(f"📌 [{row['Project Status']}] {row['Dept']} | {pic_display} - {row['Activity'][:30]}..."):
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.write(f"**Activity:** {row['Activity']}")
                st.caption(f"Sales: {row['Sales PIC']} | Engineer: {row['Eng PIC']}")
            with c2:
                st.write(f"**Progress:** {row['Progress']}%")
                if st.button(f"✏️ แก้ไข", key=f"ed_{index}"):
                    st.session_state.edit_index = index
                    st.session_state.edit_mode = True
                    st.rerun()
            with c3:
                st.write(f"**Status:** {row['Status']}")
                if st.button(f"🗑️ ลบ", key=f"dl_{index}"):
                    df = df.drop(index)
                    save_data(df)
                    st.rerun()
else:
    st.info("กรุณากรอกข้อมูลที่ Sidebar ครับ")
