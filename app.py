import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- CSS ปรับแต่งสี (คงเดิมตาม Master Code) ---
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

# 2. รายชื่อและข้อมูลพื้นฐาน (คงเดิม)
DEPT_COLORS = {"Distri-Pro": "#3498db", "Post": "#8e44ad", "Broadcast": "#27ae60", "Residential": "#f39c12", "Cinema": "#e74c3c", "ENG-Center": "#2c3e50"}
SALES_LIST = ["None", "CB : Chanunkarn", "AW : Apasri", "TH : Thanyhathorn"]
ENG_LIST = ["None", "CK : Chatchai", "BS : Boonchob", "PU : Pankrich", "MS : Maytha", "KC : Kiattisak", "DR : Danuphop", "SB : Sarawut", "KL : Kongphop", "DS : Decha", "PT : Patjitra", "WS : Worawut", "RO : Ronnarit", "NI : Nutwarot", "SK : Sirisak", "KI : Kathathep", "CA : Chatchawan", "NM : Nithithorn", "PA : Phaisan", "CN : Chainarong", "PH : Parawee", "TC : Totsapol", "WO : Watcharakorn", "VP : Veeraphat", "MK : Monrak", "PL : Preecha", "NC : Nattipong"]

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

def save_data(df_to_save): df_to_save.to_csv(DATA_FILE, index=False)
df = load_data()

if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# --- 3. หน้าปก ---
st.image("https://squarespace-cdn.com", use_container_width=True)

# 4. กราฟและรายละเอียด
if not df.empty:
    st.subheader("🔍 ค้นหาและตัวกรอง")
    f1, f2, f3 = st.columns(3)
    search = f1.text_input("🔎 ค้นหาชื่องาน", placeholder="พิมพ์เพื่อค้นหา...")
    f_dept = f2.multiselect("🏢 แผนก", options=df["Dept"].unique(), default=df["Dept"].unique())
    f_pstat = f3.multiselect("🚨 P-Status", options=["P0", "P1", "P2", "P3"], default=["P0", "P1", "P2", "P3"])
    filtered_df = df[(df["Activity"].str.contains(search, case=False, na=False)) & (df["Dept"].isin(f_dept)) & (df["Project Status"].isin(f_pstat))]

    st.markdown("---")
    st.subheader(f"📄 รายละเอียดแผนงาน ({len(filtered_df)} รายการ)")
    
    for index, row in filtered_df.iterrows():
        # --- ปรับหัวข้อ: เพิ่มตัวเลข % เข้าไปใน Tab สีขาวเลย ---
        header_label = f"📌 [{row['Project Status']}] {row['Dept']} | {row['Progress']}% | S: {row['Sales PIC']} E: {row['Eng PIC']} - {row['Activity'][:40]}..."
        
        with st.expander(header_label):
            ca, cb, cc = st.columns([2.5, 1, 1])
            with ca:
                # --- ปรับรายละเอียด: โชว์กิจกรรมแบบละเอียดแทน Bar ---
                st.markdown("##### 📋 รายละเอียดกิจกรรม (Full Activity)")
                st.info(row['Activity']) # ใช้กล่อง Info เพื่อให้อ่านง่ายขึ้น
            with cb:
                st.write(f"**สถานะ:** {row['Status']}")
                st.write(f"**ความคืบหน้า:** {row['Progress']}%")
                if st.button(f"✏️ แก้ไข", key=f"ed_{index}"):
                    st.session_state.edit_index = index; st.session_state.edit_mode = True; st.rerun()
            with cc:
                st.write(f"**Timeline:**")
                st.caption(f"{row['Start Date']} ถึง {row['End Date']}")
                if st.button(f"🗑️ ลบ", key=f"dl_{index}"):
                    df = df.drop(index); save_data(df); st.rerun()

    # กราฟสรุปด้านล่าง
    st.markdown("---")
    cg1, cg2 = st.columns(2)
    with cg1:
        fig = px.timeline(filtered_df, x_start="Start Date", x_end="End Date", y="Activity", color="Dept", text="Progress", color_discrete_map=DEPT_COLORS)
        fig.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with cg2:
        fig_p = px.pie(filtered_df, names="Dept", hole=0.4, color="Dept", color_discrete_map=DEPT_COLORS)
        fig_p.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p, use_container_width=True)

# 5. Metrics
if not df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("📊 จำนวนงานทั้งหมด", f"{len(df)} รายการ")
    m2.metric("📈 ความคืบหน้าเฉลี่ย", f"{df['Progress'].mean():.1f}%")
    m3.metric("🚨 งานด่วนพิเศษ (P0)", f"{len(df[df['Project Status'] == 'P0'])} รายการ")

st.markdown("---")

# 6. Sidebar (นำ Progress Slider ออก และใช้ระบบ Auto)
with st.sidebar:
    if st.session_state.edit_mode:
        if st.button("⬅️ Back to Add Mode", use_container_width=True):
            st.session_state.edit_mode = False; st.session_state.edit_index = None; st.rerun()
            
    st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    val = df.iloc[st.session_state.edit_index] if st.session_state.edit_mode and st.session_state.edit_index is not None else None

    with st.form("action_form", clear_on_submit=True):
        # 1. เลือก Status (Auto-link กับ Progress)
        status_options = ["Planning", "In Progress", "Completed", "Delayed"]
        status = st.selectbox("Status", status_options, index=status_options.index(val['Status']) if val is not None else 0)
        
        # คำนวณเปอร์เซ็นต์อัตโนมัติเบื้องหลัง
        auto_map = {"Planning": 0, "In Progress": 50, "Completed": 100, "Delayed": 25}
        progress_val = auto_map.get(status, 0)
        if val is not None: progress_val = val['Progress'] # ถ้าแก้ ให้ยึดค่าเดิมไว้ก่อน

        dept_list = list(DEPT_COLORS.keys())
        dept = st.selectbox("Department", dept_list, index=dept_list.index(val['Dept']) if val is not None else 0)
        
        activity = st.text_area("Action Plan & Activity", value=val['Activity'] if val is not None else "")
        
        c_pic = st.columns(2)
        sales_p = c_pic[0].selectbox("Sales PIC", SALES_LIST, index=SALES_LIST.index(val['Sales PIC']) if val is not None else 0)
        eng_p = c_pic[1].selectbox("Engineer PIC", ENG_LIST, index=ENG_LIST.index(val['Eng PIC']) if val is not None else 0)
        
        c_info = st.columns(2)
        priority = c_info[0].selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(val['Priority']) if val is not None else 1)
        p_status = c_info[1].selectbox("Project Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(val['Project Status']) if val is not None else 1)
        
        c_date = st.columns(2)
        start_d = c_date[0].date_input("Start Date", value=val['Start Date'] if val is not None else datetime.now().date())
        end_d = c_date[1].date_input("End Date", value=val['End Date'] if val is not None else datetime.now().date())

        if st.form_submit_button("💾 บันทึกข้อมูล"):
            # ใช้ค่า Progress ที่คำนวณอัตโนมัติจากสถานะ หากเป็นการเพิ่มใหม่
            final_progress = progress_val if val is not None else auto_map.get(status, 0)
            new_row = {"Dept": dept, "Activity": activity, "Sales PIC": sales_p, "Eng PIC": eng_p, "Status": status, "Progress": final_progress, "Start Date": start_d, "End Date": end_d, "Priority": priority, "Project Status": p_status}
            if st.session_state.edit_mode:
                df.iloc[st.session_state.edit_index] = new_row
                st.session_state.edit_mode = False
            else:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df); st.rerun()

else:
    st.info("กรุณากรอกข้อมูลที่ Sidebar ครับ")
