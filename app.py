import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- Master CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b5345; color: white; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: white !important; }
    [data-testid="stMetric"] { background-color: #ffffff !important; padding: 20px; border-radius: 12px; border-left: 8px solid #0b5345; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    [data-testid="stMetricLabel"] { color: #0b5345 !important; font-size: 1.1rem !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-weight: bold !important; }
    
    /* สไตล์สำหรับ Expander ทั่วไป */
    div[data-testid="stExpander"] { background-color: white !important; border-radius: 12px !important; border: 1px solid #ddd !important; margin-bottom: 10px !important; }
    div[data-testid="stExpander"] p { color: #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. ข้อมูลพื้นฐานและสี
DEPT_COLORS = {
    "Distri-Pro": "#3498db", # สีฟ้า
    "Post": "#8e44ad",       # สีม่วง
    "Broadcast": "#27ae60",  # สีเขียว
    "Residential": "#f39c12",
    "Cinema": "#e74c3c",
    "ENG-Center": "#2c3e50"
}

# ไอคอนสำหรับแสดงหน้าหัวข้อเพื่อเพิ่มความชัดเจน
DEPT_ICONS = {"Distri-Pro": "🔵", "Post": "🟣", "Broadcast": "🟢", "Residential": "🟠", "Cinema": "🔴", "ENG-Center": "⚫"}

SALES_LIST = ["None", "CB : Chanunkarn", "AW : Apasri", "TH : Thanyhathorn"]
ENG_LIST = ["None", "CK : Chatchai", "BS : Boonchob", "PU : Pankrich", "MS : Maytha", "KC : Kiattisak", "DR : Danuphop", "SB : Sarawut", "KL : Kongphop", "DS : Decha", "PT : Patjitra", "WS : Worawut", "RO : Ronnarit", "NI : Nutwarot", "SK : Sirisak", "KI : Kathathep", "CA : Chatchawan", "NM : Nithithorn", "PA : Phaisan", "CN : Chainarong", "PH : Parawee", "TC : Totsapol", "WO : Watcharakorn", "VP : Veeraphat", "MK : Monrak", "PL : Preecha", "NC : Nattipong"]

# 3. จัดการข้อมูล
DATA_FILE = "action_plan_2026.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df_l = pd.read_csv(DATA_FILE)
            cols = ["Sales PIC", "Eng PIC", "Priority", "Project Status", "Dept", "Activity", "Progress", "Status", "Start Date", "End Date"]
            for c in cols:
                if c not in df_l.columns: df_l[c] = "None"
            df_l['Start Date'] = pd.to_datetime(df_l['Start Date'], errors='coerce').dt.date
            df_l['End Date'] = pd.to_datetime(df_l['End Date'], errors='coerce').dt.date
            return df_l.fillna("None")
        except: pass
    return pd.DataFrame(columns=["Dept", "Activity", "Sales PIC", "Eng PIC", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])

def save_data(df_s): df_s.to_csv(DATA_FILE, index=False)

df = load_data()
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# --- 4. ส่วนบนสุด (Banner & Title) ---
st.image("https://www.nimblework.com/wp-content/uploads/2024/05/Action-plan.png", use_container_width=50)
st.title("📋 2026 Follow up & Action Plan")
st.write("### Project Dashboard | Engineer Center")

# 5. Metrics & Graphs
if not df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("📊 จำนวนงานทั้งหมด", f"{len(df)} รายการ")
    avg_p = pd.to_numeric(df['Progress'], errors='coerce').mean()
    m2.metric("📈 ความคืบหน้าเฉลี่ย", f"{avg_p:.1f}%")
    m3.metric("🚨 งานด่วนพิเศษ (P0)", f"{len(df[df['Project Status'] == 'P0'])} รายการ")
    st.markdown("---")
    cg1, cg2 = st.columns(2)
    with cg1:
        st.subheader("📈 Timeline")
        fig = px.timeline(df, x_start="Start Date", x_end="End Date", y="Activity", color="Dept", text="Progress", color_discrete_map=DEPT_COLORS)
        fig.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_yaxes(tickfont=dict(color='white')); fig.update_xaxes(tickfont=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    with cg2:
        st.subheader("📊 สัดส่วนงานรายแผนก")
        fig_p = px.pie(df, names="Dept", hole=0.4, color="Dept", color_discrete_map=DEPT_COLORS)
        fig_p.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p, use_container_width=True)

st.markdown("---")

# --- 6. Sidebar (Auto-Progress Real-time) ---
with st.sidebar:
    if st.session_state.edit_mode:
        if st.button("⬅️ Back to Add Mode", use_container_width=True):
            st.session_state.edit_mode = False; st.session_state.edit_index = None; st.rerun()
    st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    dv = {"Status": "Planning", "Dept": "Distri-Pro", "Activity": "", "Sales PIC": "None", "Eng PIC": "None", "Priority": "Medium", "Project Status": "P1", "Start Date": datetime.now().date(), "End Date": datetime.now().date(), "Progress": 0}
    if st.session_state.edit_mode and st.session_state.edit_index is not None:
        try:
            row = df.iloc[st.session_state.edit_index]; [dv.update({k: row[k]}) for k in dv if k in row]
        except: st.session_state.edit_mode = False

    s_opts = ["Planning", "In Progress", "Completed", "Delayed"]
    f_status = st.selectbox("Status (สถานะ)", s_opts, index=s_opts.index(str(dv["Status"])) if str(dv["Status"]) in s_opts else 0)
    auto_map = {"Planning": 0, "In Progress": 50, "Completed": 100, "Delayed": 25}
    default_prog = int(dv["Progress"]) if st.session_state.edit_mode and f_status == dv["Status"] else auto_map.get(f_status, 0)
    f_progress = st.number_input("ความคืบหน้า (%)", min_value=0, max_value=100, value=default_prog)

    with st.form("action_form", clear_on_submit=True):
        f_dept = st.selectbox("Department", list(DEPT_COLORS.keys()), index=list(DEPT_COLORS.keys()).index(str(dv["Dept"])) if str(dv["Dept"]) in DEPT_COLORS else 0)
        f_activity = st.text_area("Action Plan & Activity", value=str(dv["Activity"]))
        c1, c2 = st.columns(2)
        f_sales = c1.selectbox("Sales PIC", SALES_LIST, index=SALES_LIST.index(str(dv["Sales PIC"])) if str(dv["Sales PIC"]) in SALES_LIST else 0)
        f_eng = c2.selectbox("Engineer PIC", ENG_LIST, index=ENG_LIST.index(str(dv["Eng PIC"])) if str(dv["Eng PIC"]) in ENG_LIST else 0)
        c3, c4 = st.columns(2)
        f_prio = c3.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(str(dv["Priority"])) if str(dv["Priority"]) in ["High", "Medium", "Low"] else 1)
        f_ps = c4.selectbox("Project Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(str(dv["Project Status"])) if str(dv["Project Status"]) in ["P0", "P1", "P2", "P3"] else 1)
        c5, c6 = st.columns(2)
        f_start = c5.date_input("Start Date", value=dv["Start Date"])
        f_end = c6.date_input("End Date", value=dv["End Date"])
        if st.form_submit_button("💾 บันทึกข้อมูล", use_container_width=True):
            new_row = {"Dept": f_dept, "Activity": f_activity, "Sales PIC": f_sales, "Eng PIC": f_eng, "Status": f_status, "Progress": f_progress, "Start Date": f_start, "End Date": f_end, "Priority": f_prio, "Project Status": f_ps}
            if st.session_state.edit_mode: df.iloc[st.session_state.edit_index] = new_row; st.session_state.edit_mode = False; st.session_state.edit_index = None
            else: df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df); st.rerun()

# --- 7. รายละเอียดแผนงาน (Color Coded Expander) ---
if not df.empty:
    st.subheader(f"📄 รายละเอียดแผนงาน ({len(df)} รายการ)")
    for index, row in df.iterrows():
        # กำหนดไอคอนและสีตามแผนก
        icon = DEPT_ICONS.get(row['Dept'], "⚪")
        color = DEPT_COLORS.get(row['Dept'], "#ddd")
        
        # หัวข้อที่มีไอคอนแผนก
        header_label = f"{icon} [{row['Project Status']}] {row['Dept']} | {row['Progress']}% | S: {row['Sales PIC']} E: {row['Eng PIC']} - {row['Activity'][:40]}..."
        
        # ใช้ container เพื่อใส่เส้นสีด้านซ้าย (Border Left)
        with st.container():
            # ฉีด CSS เฉพาะกิจสำหรับ Expander นี้
            st.markdown(f"""
                <style>
                div[data-testid="stExpander"]:nth-of-type({index+1}) {{
                    border-left: 10px solid {color} !important;
                }}
                </style>
                """, unsafe_allow_html=True)
            
            with st.expander(header_label):
                ca, cb, cc = st.columns([2.5, 1.2, 1.2])
                with ca:
                    st.markdown(f"##### 📋 รายละเอียดกิจกรรม")
                    st.info(row['Activity'])
                with cb:
                    st.write(f"**สถานะ:** {row['Status']}")
                    st.write(f"**ความคืบหน้า:** {row['Progress']}%")
                    if st.button(f"✏️ แก้ไข", key=f"ed_{index}"):
                        st.session_state.edit_index = index; st.session_state.edit_mode = True; st.rerun()
                with cc:
                    st.write(f"**Timeline:**")
                    st.caption(f"{row['Start Date']} ถึง {row['End Date']}")
                    if st.button(f"🗑️ ลบรายการ", key=f"dl_{index}"):
                        df = df.drop(index); save_data(df); st.rerun()
else:
    st.info("กรุณากรอกข้อมูลที่ Sidebar ครับ")
