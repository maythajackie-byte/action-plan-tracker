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
    div[data-testid="stExpander"] { background-color: white !important; border: 1px solid #0b5345 !important; border-radius: 12px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] label { color: #1a1a1a !important; }
    div[data-testid="stExpander"] b { color: #0b5345 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. ข้อมูลพื้นฐาน
DEPT_COLORS = {"Distri-Pro": "#3498db", "Post": "#8e44ad", "Broadcast": "#27ae60", "Residential": "#f39c12", "Cinema": "#e74c3c", "ENG-Center": "#2c3e50"}
SALES_LIST = ["None", "CB : Chanunkarn", "AW : Apasri", "TH : Thanyhathorn"]
ENG_LIST = ["None", "CK : Chatchai", "BS : Boonchob", "PU : Pankrich", "MS : Maytha", "KC : Kiattisak", "DR : Danuphop", "SB : Sarawut", "KL : Kongphop", "DS : Decha", "PT : Patjitra", "WS : Worawut", "RO : Ronnarit", "NI : Nutwarot", "SK : Sirisak", "KI : Kathathep", "CA : Chatchawan", "NM : Nithithorn", "PA : Phaisan", "CN : Chainarong", "PH : Parawee", "TC : Totsapol", "WO : Watcharakorn", "VP : Veeraphat", "MK : Monrak", "PL : Preecha", "NC : Nattipong"]

# 3. จัดการข้อมูล (Safe Mode)
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
        except:
            return pd.DataFrame(columns=["Dept", "Activity", "Sales PIC", "Eng PIC", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])
    return pd.DataFrame(columns=["Dept", "Activity", "Sales PIC", "Eng PIC", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])

def save_data(df_to_save):
    df_to_save.to_csv(DATA_FILE, index=False)

df = load_data()

# จัดการโหมดแก้ไข
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# --- 4. ส่วนหัวของหน้าเว็บ (หน้าปก และ Title) ---
st.image("https://www.conferoinc.com/wp-content/uploads/2022/06/Action-Plans.png", use_container_width=20)

c_t1, c_t2 = st.columns([0.1, 0.9])
with c_t1: st.image("https://flaticon.com", width=70)
with c_t2: st.title("2026 Follow up & Action Plan")

# 5. ส่วนสรุปภาพรวม (Metrics & Graphs)
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

# 6. Sidebar (แก้ไขจุดที่ Error และปุ่มบันทึก)
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
        
        # แก้ไขจุดที่เกิด AttributeError: ใช้ col[0] และ col[1]
        c_p = st.columns(2)
        sales_val = str(dv["Sales PIC"])
        f_sales = c_p[0].selectbox("Sales PIC", SALES_LIST, index=SALES_LIST.index(sales_val) if sales_val in SALES_LIST else 0)
        eng_val = str(dv["Eng PIC"])
        f_eng = c_p[1].selectbox("Engineer PIC", ENG_LIST, index=ENG_LIST.index(eng_val) if eng_val in ENG_LIST else 0)
        
        c_i = st.columns(2)
        prio_list = ["High", "Medium", "Low"]
        f_priority = c_i[0].selectbox("Priority", prio_list, index=prio_list.index(str(dv["Priority"])) if str(dv["Priority"]) in prio_list else 1)
        ps_list = ["P0", "P1", "P2", "P3"]
        f_pstat = c_i[1].selectbox("Project Status", ps_list, index=ps_list.index(str(dv["Project Status"])) if str(dv["Project Status"]) in ps_list else 1)
        
        c_d = st.columns(2)
        f_start = c_d[0].date_input("Start Date", value=dv["Start Date"])
        f_end = c_d[1].date_input("End Date", value=dv["End Date"])

        # ปุ่มบันทึก (ต้องอยู่ภายในบล็อก with st.form)
        submitted = st.form_submit_button("💾 บันทึกข้อมูล", use_container_width=True)
        
        if submitted:
            auto_map = {"Planning": 0, "In Progress": 50, "Completed": 100, "Delayed": 25}
            final_prog = dv['Progress'] if st.session_state.edit_mode else auto_map.get(f_status, 0)
            new_row = {"Dept": f_dept, "Activity": f_activity, "Sales PIC": f_sales, "Eng PIC": f_eng, "Status": f_status, "Progress": final_prog, "Start Date": f_start, "End Date": f_end, "Priority": f_priority, "Project Status": f_pstat}
            if st.session_state.edit_mode:
                df.iloc[st.session_state.edit_index] = new_row
                st.session_state.edit_mode = False
                st.session_state.edit_index = None
            else:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.rerun()

# 7. รายละเอียดแผนงาน
if not df.empty:
    st.subheader(f"📄 รายละเอียดแผนงาน ({len(df)} รายการ)")
    for index, row in df.iterrows():
        header_label = f"📌 [{row['Project Status']}] {row['Dept']} | {row['Progress']}% | S: {row['Sales PIC']} E: {row['Eng PIC']} - {row['Activity'][:40]}..."
        with st.expander(header_label):
            ca, cb, cc = st.columns([2.5, 1.2, 1.2])
            with ca:
                st.markdown("##### 📋 รายละเอียดกิจกรรม")
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
