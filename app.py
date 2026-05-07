import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- CSS ปรับแต่งสี (ตัวหนังสือดำเข้มในกล่องขาว) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b5345; color: white; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: white !important; }
    [data-testid="stMetric"] { background-color: #ffffff !important; padding: 20px; border-radius: 12px; border-left: 8px solid #0b5345; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    [data-testid="stMetricLabel"] { color: #0b5345 !important; font-size: 1.1rem !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-weight: bold !important; }
    
    /* กล่องรายละเอียดสีขาว */
    div[data-testid="stExpander"] { background-color: white !important; border: 1px solid #0b5345 !important; border-radius: 12px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] label {
        color: #1a1a1a !important; 
    }
    div[data-testid="stExpander"] b { color: #0b5345 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. ข้อมูลพนักงานและแผนก
DEPT_COLORS = {"Distri-Pro": "#3498db", "Post": "#8e44ad", "Broadcast": "#27ae60", "Residential": "#f39c12", "Cinema": "#e74c3c", "ENG-Center": "#2c3e50"}
SALES_LIST = ["None", "CB : Chanunkarn", "AW : Apasri", "TH : Thanyhathorn"]
ENG_LIST = ["None", "CK : Chatchai", "BS : Boonchob", "PU : Pankrich", "MS : Maytha", "KC : Kiattisak", "DR : Danuphop", "SB : Sarawut", "KL : Kongphop", "DS : Decha", "PT : Patjitra", "WS : Worawut", "RO : Ronnarit", "NI : Nutwarot", "SK : Sirisak", "KI : Kathathep", "CA : Chatchawan", "NM : Nithithorn", "PA : Phaisan", "CN : Chainarong", "PH : Parawee", "TC : Totsapol", "WO : Watcharakorn", "VP : Veeraphat", "MK : Monrak", "PL : Preecha", "NC : Nattipong"]

# 3. จัดการข้อมูล (Safe Load)
DATA_FILE = "action_plan_2026.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df_loaded = pd.read_csv(DATA_FILE)
            cols = ["Sales PIC", "Eng PIC", "Priority", "Project Status", "Dept", "Activity", "Progress", "Status", "Start Date", "End Date"]
            for col in cols:
                if col not in df_loaded.columns: df_loaded[col] = "None"
            df_loaded['Start Date'] = pd.to_datetime(df_loaded['Start Date'], errors='coerce').dt.date
            df_loaded['End Date'] = pd.to_datetime(df_loaded['End Date'], errors='coerce').dt.date
            return df_loaded.fillna("None")
        except: pass
    return pd.DataFrame(columns=["Dept", "Activity", "Sales PIC", "Eng PIC", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])

def save_data(df_to_save):
    df_to_save.to_csv(DATA_FILE, index=False)

df = load_data()

# Session State สำหรับโหมดแก้ไข
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# --- 4. ส่วนหน้าปกและ Title (Top Section) ---
st.image("https://squarespace-cdn.com", use_container_width=True)

col_title1, col_title2 = st.columns([0.1, 0.9])
with col_title1:
    st.image("https://flaticon.com", width=70)
with col_title2:
    st.title("2026 Follow up & Action Plan")

# 5. สรุปภาพรวม (Metrics & Graphs)
if not df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("📊 จำนวนงานทั้งหมด", f"{len(df)} รายการ")
    avg_prog = pd.to_numeric(df['Progress'], errors='coerce').mean()
    m2.metric("📈 ความคืบหน้าเฉลี่ย", f"{avg_prog:.1f}%")
    m3.metric("🚨 งานด่วนพิเศษ (P0)", f"{len(df[df['Project Status'] == 'P0'])} รายการ")
    
    st.markdown("---")
    
    cg1, cg2 = st.columns(2)
    with cg1:
        st.subheader("📈 Timeline")
        fig = px.timeline(df, x_start="Start Date", x_end="End Date", y="Activity", color="Dept", text="Progress", color_discrete_map=DEPT_COLORS)
        fig.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_yaxes(tickfont=dict(color='white'))
        fig.update_xaxes(tickfont=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    with cg2:
        st.subheader("📊 สัดส่วนงานรายแผนก")
        fig_p = px.pie(df, names="Dept", hole=0.4, color="Dept", color_discrete_map=DEPT_COLORS)
        fig_p.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p, use_container_width=True)

st.markdown("---")

# 6. Sidebar (Input Form - แก้ Error และปุ่มบันทึก)
with st.sidebar:
    if st.session_state.edit_mode:
        if st.button("⬅️ Back to Add Mode", use_container_width=True):
            st.session_state.edit_mode = False; st.session_state.edit_index = None; st.rerun()
            
    st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    
    # ค่าเริ่มต้นแบบปลอดภัย
    dv = {"Status": "Planning", "Dept": "Distri-Pro", "Activity": "", "Sales PIC": "None", "Eng PIC": "None", "Priority": "Medium", "Project Status": "P1", "Start Date": datetime.now().date(), "End Date": datetime.now().date(), "Progress": 0}
    
    if st.session_state.edit_mode and st.session_state.edit_index is not None:
        try:
            row = df.iloc[st.session_state.edit_index]
            for k in dv:
                if k in row: dv[k] = row[k]
        except: st.session_state.edit_mode = False

    with st.form("action_form"):
        s_opts = ["Planning", "In Progress", "Completed", "Delayed"]
        f_status = st.selectbox("Status", s_opts, index=s_opts.index(str(dv["Status"])) if str(dv["Status"]) in s_opts else 0)
        
        d_opts = list(DEPT_COLORS.keys())
        f_dept = st.selectbox("Department", d_opts, index=d_opts.index(str(dv["Dept"])) if str(dv["Dept"]) in d_opts else 0)
        
        f_activity = st.text_area("Action Plan & Activity", value=str(dv["Activity"]))
        
        c_p = st.columns(2)
        f_sales = c_p.selectbox("Sales PIC", SALES_LIST, index=SALES_LIST.index(str(dv["Sales PIC"])) if str(dv["Sales PIC"]) in SALES_LIST else 0)
        f_eng = c_p.selectbox("Engineer PIC", ENG_LIST, index=ENG_LIST.index(str(dv["Eng PIC"])) if str(dv["Eng PIC"]) in ENG_LIST else 0)
        
        c_i = st.columns(2)
        f_priority = c_i.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(str(dv["Priority"])) if str(dv["Priority"]) in ["High", "Medium", "Low"] else 1)
        f_pstat = c_i.selectbox("Project Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(str(dv["Project Status"])) if str(dv["Project Status"]) in ["P0", "P1", "P2", "P3"] else 1)
        
        c_d = st.columns(2)
        f_start = c_d.date_input("Start Date", value=dv["Start Date"])
        f_end = c_d.date_input("End Date", value=dv["End Date"])

        # ปุ่มบันทึก (ต้องอยู่ภายใน st.form)
        if st.form_submit_button("💾 บันทึกข้อมูล", use_container_width=True):
            auto_map = {"Planning": 0, "In Progress": 50, "Completed": 100, "Delayed": 25}
            final_prog = dv['Progress'] if st.session_state.edit_mode else auto_map.get(f_status, 0)
            new_row = {"Dept": f_dept, "Activity": f_activity, "Sales PIC": f_sales, "Eng PIC": f_eng, "Status": f_status, "Progress": final_prog, "Start Date": f_start, "End Date": f_end, "Priority": f_priority, "Project Status": f_pstat}
            if st.session_state.edit_mode:
                df.iloc[st.session_state.edit_index] = new_row
