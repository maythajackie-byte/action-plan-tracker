import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- CSS ปรับแต่งสี ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b5345; color: white; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: white !important; }
    [data-testid="stMetric"] { background-color: #ffffff !important; padding: 20px; border-radius: 12px; border-left: 8px solid #0b5345; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    [data-testid="stMetricLabel"] { color: #0b5345 !important; font-size: 1.1rem !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-weight: bold !important; }
    div[data-testid="stExpander"] { background-color: white !important; border: 1px solid #0b5345 !important; border-radius: 12px !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important; }
    div[data-testid="stExpander"] p { color: #0b5345 !important; font-weight: bold !important; }
    
    /* ปรับแต่งปุ่ม Back */
    .back-btn { background-color: #f1c40f !important; color: #0b5345 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. กำหนดสีประจำแผนก ---
DEPT_COLORS = {
    "Distri-Pro": "#3498db", "Post": "#8e44ad", "Broadcast": "#27ae60",
    "Residential": "#f39c12", "Cinema": "#e74c3c", "ENG-Center": "#2c3e50"
}

SALES_LIST = ["None", "CB : Chanunkarn", "AW : Apasri", "TH : Thanyhathorn"]
ENG_LIST = ["None", "CK : Chatchai", "BS : Boonchob", "PU : Pankrich", "MS : Maytha", "KC : Kiattisak", "DR : Danuphop", "SB : Sarawut", "KL : Kongphop", "DS : Decha", "PT : Patjitra", "WS : Worawut", "RO : Ronnarit", "NI : Nutwarot", "SK : Sirisak", "KI : Kathathep", "CA : Chatchawan", "NM : Nithithorn", "PA : Phaisan", "CN : Chainarong", "PH : Parawee", "TC : Totsapol", "WO : Watcharakorn", "VP : Veeraphat", "MK : Monrak", "PL : Preecha", "NC : Nattipong"]

# 3. จัดการข้อมูล
DATA_FILE = "action_plan_2026.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df_loaded = pd.read_csv(DATA_FILE)
        cols = ["Sales PIC", "Eng PIC", "Priority", "Project Status", "Dept", "Activity", "Progress", "Status", "Start Date", "End Date"]
        for col in cols:
            if col not in df_loaded.columns: df_loaded[col] = "None"
        df_loaded['Start Date'] = pd.to_datetime(df_loaded['Start Date']).dt.date
        df_loaded['End Date'] = pd.to_datetime(df_loaded['End Date']).dt.date
        return df_loaded
    return pd.DataFrame(columns=["Dept", "Activity", "Sales PIC", "Eng PIC", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])

def save_data(df_to_save):
    df_to_save.to_csv(DATA_FILE, index=False)

df = load_data()

if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# --- 4. ส่วนหน้าปก (Cover Image) ---
st.image("https://images.squarespace-cdn.com/content/v1/6022f791cf4a4d20ccfcd9c4/1720041912442-BKASDM2GXDEANYX4LG4Q/Capture.PNG", use_container_width=1200)

c_t1, c_t2 = st.columns([0.1, 0.9])
with c_t1: st.image("https://flaticon.com", width=70)
with c_t2: st.title("2026 Follow up & Action Plan")

# 5. Metrics
if not df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("📊 จำนวนงานทั้งหมด", f"{len(df)} รายการ")
    m2.metric("📈 ความคืบหน้าเฉลี่ย", f"{df['Progress'].mean():.1f}%")
    m3.metric("🚨 งานด่วนพิเศษ (P0)", f"{len(df[df['Project Status'] == 'P0'])} รายการ")

st.markdown("---")

# 6. Sidebar (Input Form)
with st.sidebar:
    # เพิ่มปุ่ม Back เพื่อย้อนกลับจากการแก้ไข
    if st.session_state.edit_mode:
        if st.button("⬅️ Back to Add Mode", use_container_width=True):
            st.session_state.edit_mode = False
            st.session_state.edit_index = None
            st.rerun()
            
    st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    
    val = None
    if st.session_state.edit_mode and st.session_state.edit_index is not None:
        try:
            val = df.iloc[st.session_state.edit_index[0] if isinstance(st.session_state.edit_index, list) else st.session_state.edit_index]
        except:
            st.session_state.edit_mode = False

    with st.form("action_form", clear_on_submit=True):
        dept_list = list(DEPT_COLORS.keys())
        dept_idx = dept_list.index(val['Dept']) if val is not None and val['Dept'] in dept_list else 0
        dept = st.selectbox("Department", dept_list, index=dept_idx)
        
        activity = st.text_area("Action Plan & Activity", value=val['Activity'] if val is not None else "")
        
        c_p1, c_p2 = st.columns(2)
        s_idx = SALES_LIST.index(val['Sales PIC']) if val is not None and val['Sales PIC'] in SALES_LIST else 0
        sales_p = c_p1.selectbox("Sales PIC", SALES_LIST, index=s_idx)
        e_idx = ENG_LIST.index(val['Eng PIC']) if val is not None and val['Eng PIC'] in ENG_LIST else 0
        eng_p = c_p2.selectbox("Engineer PIC", ENG_LIST, index=e_idx)
        
        c_s1, c_s2 = st.columns(2)
        p_list = ["High", "Medium", "Low"]
        p_idx = p_list.index(val['Priority']) if val is not None and val['Priority'] in p_list else 1
        priority = c_s1.selectbox("Priority", p_list, index=p_idx)
        ps_list = ["P0", "P1", "P2", "P3"]
        ps_idx = ps_list.index(val['Project Status']) if val is not None and val['Project Status'] in ps_list else 1
        p_status = c_s2.selectbox("Project Status", ps_list, index=ps_idx)
        
        c_d1, c_d2 = st.columns(2)
        start_d = c_d1.date_input("Start Date", value=val['Start Date'] if val is not None else datetime.now().date())
        end_d = c_d2.date_input("End Date", value=val['End Date'] if val is not None else datetime.now().date())
        
        st_list = ["Planning", "In Progress", "Completed", "Delayed"]
        st_idx = st_list.index(val['Status']) if val is not None and val['Status'] in st_list else 0
        status = st.selectbox("Status", st_list, index=st_idx)
        progress = st.slider("Progress (%)", 0, 100, int(val['Progress']) if val is not None else 0)
        
        if st.form_submit_button("💾 บันทึกข้อมูล"):
            new_row = {"Dept": dept, "Activity": activity, "Sales PIC": sales_p, "Eng PIC": eng_p, "Status": status, "Progress": progress, "Start Date": start_d, "End Date": end_d, "Priority": priority, "Project Status": p_status}
            if st.session_state.edit_mode:
                idx = st.session_state.edit_index[0] if isinstance(st.session_state.edit_index, list) else st.session_state.edit_index
                df.iloc[idx] = new_row
                st.session_state.edit_mode = False
            else:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df); st.rerun()

# 7. --- ระบบตัวกรอง ---
if not df.empty:
    st.subheader("🔍 ค้นหาและตัวกรอง")
    f1, f2, f3 = st.columns(3)
    search = f1.text_input("🔎 ค้นหาชื่องาน", placeholder="พิมพ์คำค้นหา...")
    f_dept = f2.multiselect("🏢 เลือกแผนก", options=df["Dept"].unique(), default=df["Dept"].unique())
    f_pstat = f3.multiselect("🚨 สถานะ P-Status", options=["P0", "P1", "P2", "P3"], default=["P0", "P1", "P2", "P3"])
    
    filtered_df = df[(df["Activity"].str.contains(search, case=False, na=False)) & (df["Dept"].isin(f_dept)) & (df["Project Status"].isin(f_pstat))]

    # 8. กราฟ (ตัวหนังสือขาว)
    cg1, cg2 = st.columns(2)
    with cg1:
        st.subheader("📈 Timeline (ตามแผนก)")
        fig = px.timeline(filtered_df, x_start="Start Date", x_end="End Date", y="Activity", color="Dept", text="Progress", color_discrete_map=DEPT_COLORS)
        fig.update_yaxes(autorange="reversed", tickfont=dict(color='white'))
        fig.update_xaxes(tickfont=dict(color='white'))
        fig.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with cg2:
        st.subheader("📊 สัดส่วนงาน")
        fig_p = px.pie(filtered_df, names="Dept", hole=0.4, color="Dept", color_discrete_map=DEPT_COLORS)
        fig_p.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p, use_container_width=True)

    st.markdown("---")
    st.subheader(f"📄 รายละเอียดแผนงาน ({len(filtered_df)} รายการ)")
    for index, row in filtered_df.iterrows():
        # ค้นหา index จริงจาก Activity
        real_idx_list = df.index[df['Activity'] == row['Activity']].tolist()
        with st.expander(f"📌 [{row['Project Status']}] {row['Dept']} | S: {row['Sales PIC']} E: {row['Eng PIC']} - {row['Activity'][:40]}..."):
            ca, cb, cc = st.columns(3)
            with ca: st.write(f"**กิจกรรม:** {row['Activity']}")
            with cb:
                st.write(f"**Progress:** {row['Progress']}%")
                if st.button(f"✏️ แก้ไข", key=f"ed_{index}"):
                    st.session_state.edit_index = real_idx_list
                    st.session_state.edit_mode = True; st.rerun()
            with cc:
                st.write(f"**Status:** {row['Status']}")
                if st.button(f"🗑️ ลบ", key=f"dl_{index}"):
                    df = df.drop(real_idx_list); save_data(df); st.rerun()
else:
    st.info("กรุณากรอกข้อมูลที่ Sidebar ครับ")
