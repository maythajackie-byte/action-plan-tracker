import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- ปรับแต่ง CSS (คงเดิมตาม Master Code) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b5345; color: white; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: white !important; }
    [data-testid="stMetric"] { background-color: #ffffff !important; padding: 20px; border-radius: 12px; border-left: 8px solid #0b5345; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    [data-testid="stMetricLabel"] { color: #0b5345 !important; font-size: 1.1rem !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #1a1a1a !important; font-weight: bold !important; }
    div[data-testid="stExpander"] { background-color: white !important; border: 1px solid #0b5345 !important; border-radius: 12px !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important; }
    div[data-testid="stExpander"] p { color: #0b5345 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. กำหนดสีประจำแผนกตามรูปภาพ (Color Map) ---
DEPT_COLORS = {
    "Distri-Pro": "#3498db",    # สีฟ้า
    "Post": "#8e44ad",          # สีม่วง
    "Broadcast": "#27ae60",     # สีเขียว
    "Residential": "#f39c12",   # สีส้ม (เผื่อไว้)
    "Cinema": "#e74c3c",        # สีแดง (เผื่อไว้)
    "ENG-Center": "#2c3e50"     # สีเทาเข้ม (เผื่อไว้)
}

# รายชื่อพนักงาน (คงเดิม)
SALES_LIST = ["None", "CB : Chanunkarn", "AW : Apasri", "TH : Thanyhathorn"]
ENG_LIST = ["None", "CK : Chatchai", "BS : Boonchob", "PU : Pankrich", "MS : Maytha", "KC : Kiattisak", "DR : Danuphop", "SB : Sarawut", "KL : Kongphop", "DS : Decha", "PT : Patjitra", "WS : Worawut", "RO : Ronnarit", "NI : Nutwarot", "SK : Sirisak", "KI : Kathathep", "CA : Chatchawan", "NM : Nithithorn", "PA : Phaisan", "CN : Chainarong", "PH : Parawee", "TC : Totsapol", "WO : Watcharakorn", "VP : Veeraphat", "MK : Monrak", "PL : Preecha", "NC : Nattipong"]

# 3. จัดการข้อมูล
DATA_FILE = "action_plan_2026.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df_loaded = pd.read_csv(DATA_FILE)
        for col in ["Sales PIC", "Eng PIC", "Priority", "Project Status", "Dept", "Activity", "Progress", "Status", "Start Date", "End Date"]:
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

# 4. ส่วนหัวข้อ
c1, c2 = st.columns([0.1, 0.9])
with c1: st.image("https://flaticon.com", width=70)
with c2: st.title("2026 Follow up & Action Plan")

# 5. Metrics (คงเดิม)
if not df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("📊 จำนวนงานทั้งหมด", f"{len(df)} รายการ")
    m2.metric("📈 ความคืบหน้าเฉลี่ย", f"{df['Progress'].mean():.1f}%")
    m3.metric("🚨 งานด่วนพิเศษ (P0)", f"{len(df[df['Project Status'] == 'P0'])} รายการ")

st.markdown("---")

# 6. Sidebar (Input Form - คงเดิม)
with st.sidebar:
    st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    val = df.iloc[st.session_state.edit_index] if st.session_state.edit_mode else None
    with st.form("action_form", clear_on_submit=True):
        dept = st.selectbox("Department", list(DEPT_COLORS.keys()), index=list(DEPT_COLORS.keys()).index(val['Dept']) if val is not None else 0)
        activity = st.text_area("Action Plan & Activity", value=val['Activity'] if val is not None else "")
        c_p1, c_p2 = st.columns(2)
        sales_p = c_p1.selectbox("Sales PIC", SALES_LIST, index=SALES_LIST.index(val['Sales PIC']) if val is not None else 0)
        eng_p = c_p2.selectbox("Engineer PIC", ENG_LIST, index=ENG_LIST.index(val['Eng PIC']) if val is not None else 0)
        c_s1, c_s2 = st.columns(2)
        priority = c_s1.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(val['Priority']) if val is not None else 1)
        p_status = c_s2.selectbox("Project Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(val['Project Status']) if val is not None else 1)
        c_d1, c_d2 = st.columns(2)
        start_d = c_d1.date_input("Start Date", value=val['Start Date'] if val is not None else datetime.now().date())
        end_d = c_d2.date_input("End Date", value=val['End Date'] if val is not None else datetime.now().date())
        status = st.selectbox("Status", ["Planning", "In Progress", "Completed", "Delayed"], index=["Planning", "In Progress", "Completed", "Delayed"].index(val['Status']) if val is not None else 0)
        progress = st.slider("Progress (%)", 0, 100, int(val['Progress']) if val is not None else 0)
        if st.form_submit_button("💾 บันทึกข้อมูล"):
            new_row = {"Dept": dept, "Activity": activity, "Sales PIC": sales_p, "Eng PIC": eng_p, "Status": status, "Progress": progress, "Start Date": start_d, "End Date": end_d, "Priority": priority, "Project Status": p_status}
            if st.session_state.edit_mode: df.iloc[st.session_state.edit_index] = new_row; st.session_state.edit_mode = False
            else: df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df); st.rerun()

# 7. กราฟ (เน้นการใช้สีตามแผนกที่กำหนด)
if not df.empty:
    col_g1, col_g2 = st.columns()
    with col_g1:
        st.subheader("📈 Timeline (แยกตามแผนก)")
        # เปลี่ยน color เป็น Dept เพื่อให้เห็นสีตามที่เลือก
        fig = px.timeline(df, x_start="Start Date", x_end="End Date", y="Activity", 
                          color="Dept", text="Progress", 
                          color_discrete_map=DEPT_COLORS) # ใช้สีที่เรากำหนดไว้
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    with col_g2:
        st.subheader("📊 สัดส่วนตามแผนก")
        # ใช้สีที่เรากำหนดไว้ในกราฟวงกลมด้วย
        st.plotly_chart(px.pie(df, names="Dept", hole=0.4, color="Dept", color_discrete_map=DEPT_COLORS), use_container_width=True)

    st.markdown("---")
    st.subheader("📄 รายละเอียดแผนงาน")
    for index, row in df.iterrows():
        # กำหนดสีขอบของ Expander ตามสีแผนก
        d_color = DEPT_COLORS.get(row['Dept'], "#0b5345")
        with st.expander(f"📌 [{row['Project Status']}] {row['Dept']} | S: {row['Sales PIC']} E: {row['Eng PIC']} - {row['Activity'][:40]}..."):
            ca, cb, cc = st.columns()
            with ca: st.write(f"**กิจกรรม:** {row['Activity']}")
            with cb:
                st.write(f"**Progress:** {row['Progress']}%")
                if st.button(f"✏️ แก้ไข", key=f"ed_{index}"):
                    st.session_state.edit_index = index
                    st.session_state.edit_mode = True; st.rerun()
            with cc:
                st.write(f"**Status:** {row['Status']}")
                if st.button(f"🗑️ ลบ", key=f"dl_{index}"):
                    df = df.drop(index); save_data(df); st.rerun()
else:
    st.info("กรุณากรอกข้อมูลที่ Sidebar ครับ")
