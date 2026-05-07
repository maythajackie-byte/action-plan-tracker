import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- Master CSS (ตัวหนังสือดำในกล่องขาว, กราฟตัวหนังสือขาว) ---
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

def save_data(df_s): df_to_save = df_s.copy(); df_to_save.to_csv(DATA_FILE, index=False)

df = load_data()
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# --- 4. ส่วนบนสุด (Banner & Title) ---
st.image("https://www.nimblework.com/wp-content/uploads/2024/05/Action-plan.png", use_container_width=50)
st.title("📋 2026 Follow up & Action Plan")
st.write("### Project Dashboard | Engineer Center")

# --- 5. ระบบ Filter ปรับปรุงใหม่ (อัจฉริยะขึ้น) ---
if not df.empty:
    st.markdown("---")
    st.subheader("🔍 ค้นหาและตัวกรองข้อมูล (Filters)")
    
    row1_c1, row1_c2 = st.columns([2, 1])
    search = row1_c1.text_input("🔎 ค้นหาชื่องาน", placeholder="พิมพ์คำค้นหาที่นี่...")
    f_dept = row1_c2.multiselect("🏢 แผนก", options=df["Dept"].unique(), default=df["Dept"].unique())
    
    row2_c1, row2_c2, row2_c3 = st.columns(3)
    f_pstat = row2_c1.multiselect("🚨 P-Status", options=["P0", "P1", "P2", "P3"], default=["P0", "P1", "P2", "P3"])
    f_sales = row2_c2.multiselect("👤 Sales PIC", options=df["Sales PIC"].unique(), default=df["Sales PIC"].unique())
    f_eng = row2_c3.multiselect("🛠 Engineer PIC", options=df["Eng PIC"].unique(), default=df["Eng PIC"].unique())

    # --- ตรรกะใหม่: ถ้าช่องว่าง ให้ถือว่าเลือกทั้งหมด (ป้องกันหน้าจอขาว) ---
    dept_criteria = f_dept if f_dept else df["Dept"].unique()
    pstat_criteria = f_pstat if f_pstat else ["P0", "P1", "P2", "P3"]
    sales_criteria = f_sales if f_sales else df["Sales PIC"].unique()
    eng_criteria = f_eng if f_eng else df["Eng PIC"].unique()

    # ประมวลผล Filter ด้วยตรรกะใหม่
    filtered_df = df[
        (df["Activity"].astype(str).str.contains(search, case=False, na=False)) &
        (df["Dept"].isin(dept_criteria)) &
        (df["Project Status"].isin(pstat_criteria)) &
        (df["Sales PIC"].isin(sales_criteria)) &
        (df["Eng PIC"].isin(eng_criteria))
    ]
else:
    filtered_df = df

# --- 6. สรุปภาพรวม (Metrics & Graphs) ---
if not filtered_df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("📊 จำนวนงานที่พบ", f"{len(filtered_df)} รายการ")
    avg_p = pd.to_numeric(filtered_df['Progress'], errors='coerce').mean()
    m2.metric("📈 ความคืบหน้าเฉลี่ย", f"{avg_p:.1f}%")
    m3.metric("🚨 งาน P0", f"{len(filtered_df[filtered_df['Project Status'] == 'P0'])} รายการ")
    
    st.markdown("---")
    cg1, cg2 = st.columns(2)
    with cg1:
        fig = px.timeline(filtered_df, x_start="Start Date", x_end="End Date", y="Activity", color="Dept", text="Progress", color_discrete_map=DEPT_COLORS)
        fig.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_yaxes(tickfont=dict(color='white'))
        fig.update_xaxes(tickfont=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    with cg2:
        fig_p = px.pie(filtered_df, names="Dept", hole=0.4, color="Dept", color_discrete_map=DEPT_COLORS)
        fig_p.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p, use_container_width=True)

st.markdown("---")

# --- 7. Sidebar (Input Form) ---
with st.sidebar:
    if st.session_state.edit_mode:
        if st.button("⬅️ Back to Add Mode", use_container_width=True):
            st.session_state.edit_mode = False; st.session_state.edit_index = None; st.rerun()
    st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    dv = {"Status": "Planning", "Dept": "Distri-Pro", "Activity": "", "Sales PIC": "None", "Eng PIC": "None", "Priority": "Medium", "Project Status": "P1", "Start Date": datetime.now().date(), "End Date": datetime.now().date(), "Progress": 0}
    if st.session_state.edit_mode and st.session_state.edit_index is not None:
        try:
            row_data = df.iloc[st.session_state.edit_index]
            for k in dv:
                if k in row_data: dv[k] = row_data[k]
        except: st.session_state.edit_mode = False

    with st.form("action_form"):
        s_opts = ["Planning", "In Progress", "Completed", "Delayed"]
        f_status = st.selectbox("Status", s_opts, index=s_opts.index(str(dv["Status"])) if str(dv["Status"]) in s_opts else 0)
        f_dept = st.selectbox("Department", list(DEPT_COLORS.keys()), index=list(DEPT_COLORS.keys()).index(str(dv["Dept"])) if str(dv["Dept"]) in DEPT_COLORS else 0)
        f_activity = st.text_area("Action Plan & Activity", value=str(dv["Activity"]))
        cp = st.columns(2)
        f_sales_val = cp[0].selectbox("Sales PIC", SALES_LIST, index=SALES_LIST.index(str(dv["Sales PIC"])) if str(dv["Sales PIC"]) in SALES_LIST else 0)
        f_eng_val = cp[1].selectbox("Engineer PIC", ENG_LIST, index=ENG_LIST.index(str(dv["Eng PIC"])) if str(dv["Eng PIC"]) in ENG_LIST else 0)
        ci = st.columns(2)
        f_priority = ci[0].selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(str(dv["Priority"])) if str(dv["Priority"]) in ["High", "Medium", "Low"] else 1)
        f_pstat = ci[1].selectbox("Project Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(str(dv["Project Status"])) if str(dv["Project Status"]) in ["P0", "P1", "P2", "P3"] else 1)
        cd = st.columns(2)
        f_start = cd[0].date_input("Start Date", value=dv["Start Date"])
        f_end = cd[1].date_input("End Date", value=dv["End Date"])
        if st.form_submit_button("💾 บันทึกข้อมูล", use_container_width=True):
            auto_map = {"Planning": 0, "In Progress": 50, "Completed": 100, "Delayed": 25}
            final_prog = dv['Progress'] if st.session_state.edit_mode else auto_map.get(f_status, 0)
            new_row = {"Dept": f_dept, "Activity": f_activity, "Sales PIC": f_sales_val, "Eng PIC": f_eng_val, "Status": f_status, "Progress": final_prog, "Start Date": f_start, "End Date": f_end, "Priority": f_priority, "Project Status": f_pstat}
            if st.session_state.edit_mode: df.iloc[st.session_state.edit_index] = new_row; st.session_state.edit_mode = False
            else: df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df); st.rerun()

# --- 8. รายละเอียดแผนงาน (Bottom) ---
if not filtered_df.empty:
    st.subheader(f"📄 รายละเอียดแผนงาน ({len(filtered_df)} รายการที่กรอง)")
    for index, row in filtered_df.iterrows():
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
                    # ค้นหา index จริงใน df หลัก
                    actual_idx = df.index[df['Activity'] == row['Activity']].tolist()[0]
                    st.session_state.edit_index = actual_idx; st.session_state.edit_mode = True; st.rerun()
            with cc:
                st.write(f"**Timeline:**")
                st.caption(f"{row['Start Date']} ถึง {row['End Date']}")
                if st.button(f"🗑️ ลบรายการ", key=f"dl_{index}"):
                    actual_idx = df.index[df['Activity'] == row['Activity']].tolist()[0]
                    df = df.drop(actual_idx); save_data(df); st.rerun()
else:
    st.info("ไม่พบข้อมูลที่ตรงกับตัวกรองของคุณ")
