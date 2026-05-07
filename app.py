import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan Management", layout="wide")

# ธีมสีเขียวและการจัด Layout
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b5345; color: white; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: white !important; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #0b5345; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. รายชื่อพนักงานทั้งหมด (รวมรายชื่อ Sales ใหม่ 3 ท่านด้านบนสุด)
PIC_LIST = [
    "CB : Chanunkarn", "AW : Apasri", "TH : Thanyhathorn", # เพิ่ม Sales ใหม่
    "CK : Chatchai", "BS : Boonchob", "PU : Pankrich", "MS : Maytha", 
    "KC : Kiattisak", "DR : Danuphop", "SB : Sarawut", "KL : Kongphop",
    "DS : Decha", "PT : Patjitra", "WS : Worawut", "RO : Ronnarit",
    "NI : Nutwarot", "SK : Sirisak", "KI : Kathathep", "CA : Chatchawan",
    "NM : Nithithorn", "PA : Phaisan", "CN : Chainarong", "PH : Parawee",
    "TC : Totsapol", "WO : Watcharakorn", "VP : Veeraphat", "MK : Monrak",
    "PL : Preecha", "NC : Nattipong"
]

# 3. จัดการฐานข้อมูล
DATA_FILE = "action_plan_2026.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # ตรวจสอบและแปลงรูปแบบวันที่
        if 'Start Date' in df.columns:
            df['Start Date'] = pd.to_datetime(df['Start Date']).dt.date
        if 'End Date' in df.columns:
            df['End Date'] = pd.to_datetime(df['End Date']).dt.date
        return df
    return pd.DataFrame(columns=["Dept", "Activity", "Target", "PIC", "Support", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --- ส่วนของการจัดการ Session State สำหรับการแก้ไข ---
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

# --- 4. Sidebar (Input & Edit Form) ---
with st.sidebar:
    st.header("📝 " + ("แก้ไขแผนงาน" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    
    # ดึงค่าเดิมมาใส่ถ้าอยู่ในโหมดแก้ไข
    default_vals = df.iloc[st.session_state.edit_index] if st.session_state.edit_mode else None
    
    with st.form("action_form", clear_on_submit=True):
        dept = st.selectbox("Department", ["Distri-Pro", "Post", "Broadcast", "Residential", "Cinema", "ENG-Center"], 
                            index=["Distri-Pro", "Post", "Broadcast", "Residential", "Cinema", "ENG-Center"].index(default_vals['Dept']) if default_vals is not None else 0)
        
        activity = st.text_area("Activity", value=default_vals['Activity'] if default_vals is not None else "")
        
        # แสดงรายชื่อพนักงานที่มีรายชื่อ Sales ใหม่รวมอยู่ด้วย
        pic = st.selectbox("PIC (ผู้รับผิดชอบ)", PIC_LIST, 
                           index=PIC_LIST.index(default_vals['PIC']) if default_vals is not None and default_vals['PIC'] in PIC_LIST else 0)
        
        col_s1, col_s2 = st.columns(2)
        priority = col_s1.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(default_vals['Priority']) if default_vals is not None else 0)
        p_status = col_s2.selectbox("P-Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(default_vals['Project Status']) if default_vals is not None else 0)
        
        progress = st.slider("Progress (%)", 0, 100, int(default_vals['Progress']) if default_vals is not None else 0)
        
        status = st.selectbox("Status", ["Planning", "In Progress", "Completed", "Delayed"], 
                              index=["Planning", "In Progress", "Completed", "Delayed"].index(default_vals['Status']) if default_vals is not None else 0)
        
        submitted = st.form_submit_button("บันทึกการแก้ไข" if st.session_state.edit_mode else "เพิ่มแผนงาน")
        
        if submitted:
            new_data = {
                "Dept": dept, "Activity": activity, "Target": default_vals['Target'] if default_vals is not None else "-",
                "PIC": pic, "Support": default_vals['Support'] if default_vals is not None else "-",
                "Status": status, "Progress": progress, 
                "Start Date": default_vals['Start Date'] if default_vals is not None else pd.Timestamp.now().date(),
                "End Date": default_vals['End Date'] if default_vals is not None else pd.Timestamp.now().date(),
                "Priority": priority, "Project Status": p_status
            }
            
            if st.session_state.edit_mode:
                df.iloc[st.session_state.edit_index] = new_data
                st.session_state.edit_mode = False
            else:
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            
            save_data(df)
            st.success("บันทึกสำเร็จ!")
            st.rerun()

    if st.session_state.edit_mode:
        if st.button("ยกเลิกการแก้ไข"):
            st.session_state.edit_mode = False
            st.rerun()

# --- 5. Dashboard Main Content ---
st.title("🚀 Action Plan Tracker")

if not df.empty:
    st.subheader("📄 Detailed Action Plan Table")
    for index, row in df.iterrows():
        with st.expander(f"[{row['Project Status']}] {row['Dept']} - {row['PIC']} : {row['Activity'][:40]}..."):
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.write(f"**Activity:** {row['Activity']}")
                st.caption(f"PIC: {row['PIC']} | Progress: {row['Progress']}% | Status: {row['Status']}")
            with c2:
                if st.button(f"✏️ แก้ไข", key=f"edit_{index}"):
                    st.session_state.edit_index = index
                    st.session_state.edit_mode = True
                    st.rerun()
            with c3:
                if st.button(f"🗑️ ลบ", key=f"del_{index}"):
                    df = df.drop(index)
                    save_data(df)
                    st.rerun()
else:
    st.info("ยังไม่มีข้อมูลแผนงาน กรุณากรอกข้อมูลที่แถบด้านซ้ายมือครับ")
