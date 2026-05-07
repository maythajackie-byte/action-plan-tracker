import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Company Action Plan 2026", layout="wide")

# --- ปรับแต่ง CSS ให้สวยงามและอ่านง่าย ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b5345; color: white; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: white !important; }
    
    /* ปรับแต่งกล่อง Metric (3 กรอบขาว) */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #0b5345;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    [data-testid="stMetricLabel"] { color: #0b5345 !important; font-size: 1.1rem !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-weight: bold !important; }
    
    /* ปรับแต่งปุ่มและ Expander */
    .stButton>button { border-radius: 5px; width: 100%; }
    div[data-testid="stExpander"] { border: 1px solid #0b5345; border-radius: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. รายชื่อพนักงาน
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
        for col in ["Sales PIC", "Eng PIC", "Priority", "Project Status"]:
            if col not in df.columns: df[col] = "None"
        df['Start Date'] = pd.to_datetime(df['Start Date']).dt.date
        df['End Date'] = pd.to_datetime(df['End Date']).dt.date
        return df
    return pd.DataFrame(columns=["Dept", "Activity", "Target", "Sales PIC", "Eng PIC", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# Session State สำหรับการแก้ไข
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# 4. ส่วนหัวข้อ (Title & Logo)
c_title1, c_title2 = st.columns([0.1, 0.9])
with c_title1:
    st.image("https://flaticon.com", width=70)
with c_title2:
    st.title("2026 Follow up & Action Plan")

# 5. ส่วนแสดง Metrics (3 กรอบขาวพร้อมชื่อหัวข้อ)
if not df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric(label="📊 จำนวนงานทั้งหมด", value=f"{len(df)} รายการ")
    m2.metric(label="📈 ความคืบหน้าเฉลี่ย", value=f"{df['Progress'].mean():.1f}%")
    m3.metric(label="🚨 งานด่วนพิเศษ (P0)", value=f"{len(df[df['Project Status'] == 'P0'])} รายการ")

st.markdown("---")

# 6. Sidebar (Input Form)
with st.sidebar:
    st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    val = df.iloc[st.session_state.edit_index] if st.session_state.edit_mode else None
    
    with st.form("action_form", clear_on_submit=True):
        dept = st.selectbox("Department", ["Distri-Pro", "Post", "Broadcast", "Residential", "Cinema", "ENG-Center"],
                            index=["Distri-Pro", "Post", "Broadcast", "Residential", "Cinema", "ENG-Center"].index(val['Dept']) if val is not None else 0)
        activity = st.text_area("Action Plan & Activity", value=val['Activity'] if val is not None else "")
        
        col_pic1, col_pic2 = st.columns(2)
        sales_p = col_pic1.selectbox("Sales PIC", SALES_LIST, index=SALES_LIST.index(val['Sales PIC']) if val is not None else 0)
        eng_p = col_pic2.selectbox("Engineer PIC", ENG_LIST, index=ENG_LIST.index(val['Eng PIC']) if val is not None else 0)
        
        col_s1, col_s2 = st.columns(2)
        priority = col_s1.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(val['Priority']) if val is not None else 1)
        p_status = col_s2.selectbox("Project Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(val['Project Status']) if val is not None else 1)
        
        col_d1, col_d2 = st.columns(2)
        start_d = col_d1.date_input("Start Date", value=val['Start Date'] if val is not None else datetime.now().date())
        end_d = col_d2.date_input("End Date", value=val['End Date'] if val is not None else datetime.now().date())
        
        status = st.selectbox("Status", ["Planning", "In Progress", "Completed", "Delayed"], index=["Planning", "In Progress", "Completed", "Delayed"].index(val['Status']) if val is not None else 0)
        progress = st.slider("Progress (%)", 0, 100, int(val['Progress']) if val is not None else 0)
        
        if st.form_submit_button("💾 บันทึกข้อมูล"):
            new_row = {"Dept": dept, "Activity": activity, "Sales PIC": sales_p, "Eng PIC": eng_p, "Status": status, "Progress": progress, 
                       "Start Date": start_d, "End Date": end_d, "Priority": priority, "Project Status": p_status}
            if st.session_state.edit_mode:
                df.iloc[st.session_state.edit_index] = new_row
                st.session_state.edit_mode = False
            else:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.rerun()

# 7. กราฟสรุป (Visuals)
if not df.empty:
    col_g1, col_g2 = st.columns([2, 1])
    with col_g1:
        st.subheader("📈 Timeline & Progress")
        fig = px.timeline(df, x_start="Start Date", x_end="End Date", y="Activity", color="Project Status", text="Progress",
                          color_discrete_map={"P0":"#e74c3c", "P1":"#e67e22", "P2":"#3498db", "P3":"#2ecc71"})
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    with col_g2:
        st.subheader("📊 สัดส่วนตามแผนก")
        fig_pie = px.pie(df, names="Dept", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("📄 รายละเอียดแผนงาน")
    for index, row in df.iterrows():
        with st.expander(f"📌 [{row['Project Status']}] {row['Dept']} | S: {row['Sales PIC']} E: {row['Eng PIC']} - {row['Activity'][:30]}..."):
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.write(f"**Activity:** {row['Activity']}")
            with c2:
                st.write(f"**Progress:** {row['Progress']}%")
                if st.button(f"✏️ แก้ไข", key=f"ed_{index}"):
                    st.session_state.edit_index = index
                    st.session_state.edit_mode = True
                    st.rerun()
            with c3:
                if st.button(f"🗑️ ลบ", key=f"dl_{index}"):
                    df = df.drop(index); save_data(df); st.rerun()
