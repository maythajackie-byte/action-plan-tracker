import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- Master CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b5345; color: white; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: white !important; }
    [data-testid="stMetric"] { background-color: #ffffff !important; padding: 20px; border-radius: 12px; border-left: 8px solid #0b5345; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    
    /* กล่องรายละเอียดสีขาว + ตัวหนังสือดำ */
    div[data-testid="stExpander"] { background-color: white !important; border-radius: 12px !important; border: 1px solid #ddd !important; margin-bottom: 10px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] label { color: #1a1a1a !important; }
    div[data-testid="stExpander"] b { color: #0b5345 !important; }
    
    /* สไตล์สำหรับโซนงานด่วน (สีแดง) */
    .urgent-box { background-color: #f8d7da; border: 2px solid #dc3545; padding: 15px; border-radius: 10px; color: #721c24; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ข้อมูลพื้นฐาน
DEPT_COLORS = {"Distri-Pro": "#3498db", "Post": "#8e44ad", "Broadcast": "#27ae60", "Residential": "#f39c12", "Cinema": "#e74c3c", "ENG-Center": "#2c3e50"}
DEPT_ICONS = {"Distri-Pro": "🔵", "Post": "🟣", "Broadcast": "🟢", "Residential": "🟠", "Cinema": "🔴", "ENG-Center": "⚫"}
SALES_LIST = ["None", "CB : Chanunkarn", "AW : Apasri", "TH : Thanyhathorn"]
ENG_LIST = ["None", "CK : Chatchai", "BS : Boonchob", "PU : Pankrich", "MS : Maytha", "KC : Kiattisak", "DR : Danuphop", "SB : Sarawut", "KL : Kongphop", "DS : Decha", "PT : Patjitra", "WS : Worawut", "RO : Ronnarit", "NI : Nutwarot", "SK : Sirisak", "KI : Kathathep", "CA : Chatchawan", "NM : Nithithorn", "PA : Phaisan", "CN : Chainarong", "PH : Parawee", "TC : Totsapol", "WO : Watcharakorn", "VP : Veeraphat", "MK : Monrak", "PL : Preecha", "NC : Nattipong"]

# 3. จัดการข้อมูล (Safe Load)
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

# --- 5. 🚨 ไฮไลท์งานด่วน (สีแดงเด่นชัด) ---
if not df.empty:
    today = datetime.now().date()
    near_deadline = today + timedelta(days=7) # ใกล้ Deadline ใน 7 วัน
    
    # ดึงงาน P0 หรือ งานที่ใกล้ครบกำหนด
    urgent_df = df[(df['Project Status'] == 'P0') | (df['End Date'] <= near_deadline)]
    # กรองเฉพาะงานที่ยังไม่เสร็จ (Progress < 100)
    urgent_df = urgent_df[pd.to_numeric(urgent_df['Progress'], errors='coerce') < 100]

    if not urgent_df.empty:
        st.error(f"### 🚨 งานด่วนพิเศษ & ใกล้กำหนดส่ง ({len(urgent_df)} รายการ)")
        cols_urgent = st.columns(len(urgent_df) if len(urgent_df) <= 3 else 3)
        for i, (idx, row) in enumerate(urgent_df.head(3).iterrows()):
            with cols_urgent[i % 3]:
                st.markdown(f"""
                <div class="urgent-box">
                    <b>{row['Dept']}</b><br>
                    {row['Activity'][:50]}...<br>
                    📅 Deadline: {row['End Date']}<br>
                    🔥 Status: {row['Project Status']}
                </div>
                """, unsafe_allow_html=True)
        if len(urgent_df) > 3:
            st.caption(f"และยังมีงานด่วนอีก {len(urgent_df)-3} รายการด้านล่าง...")

# --- 6. Metrics & Graphs ---
if not df.empty:
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("📊 จำนวนงานทั้งหมด", f"{len(df)} รายการ")
    avg_p = pd.to_numeric(df['Progress'], errors='coerce').mean()
    m2.metric("📈 ความคืบหน้าเฉลี่ย", f"{avg_p:.1f}%")
    m3.metric("🚨 งาน P0 ทั้งหมด", f"{len(df[df['Project Status'] == 'P0'])} รายการ")
    
    cg1, cg2 = st.columns(2)
    with cg1:
        fig = px.timeline(df, x_start="Start Date", x_end="End Date", y="Activity", color="Dept", text="Progress", color_discrete_map=DEPT_COLORS)
        fig.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_yaxes(tickfont=dict(color='white')); fig.update_xaxes(tickfont=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    with cg2:
        fig_p = px.pie(df, names="Dept", hole=0.4, color="Dept", color_discrete_map=DEPT_COLORS)
        fig_p.update_layout(font=dict(color="white"), legend_font_color="white", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_p, use_container_width=True)

# --- 7. ระบบ Filter (ล็อคให้กลับมาถาวร) ---
st.markdown("---")
st.subheader("🔍 ตัวกรองข้อมูล (Filters)")
f_row1 = st.columns([2, 1])
search = f_row1[0].text_input("🔎 ค้นหาชื่องาน", placeholder="พิมพ์เพื่อค้นหา...")
f_dept = f_row1[1].multiselect("🏢 แผนก", options=df["Dept"].unique() if not df.empty else [])

f_row2 = st.columns(3)
f_pstat = f_row2[0].multiselect("🚨 P-Status", options=["P0", "P1", "P2", "P3"])
f_sales = f_row2[1].multiselect("👤 Sales", options=df["Sales PIC"].unique() if not df.empty else [])
f_eng = f_row2[2].multiselect("🛠 Engineer", options=df["Eng PIC"].unique() if not df.empty else [])

# ตรรกะ Filter (ถ้าไม่เลือก = ดูทั้งหมด)
d_crit = f_dept if f_dept else df["Dept"].unique() if not df.empty else []
p_crit = f_pstat if f_pstat else ["P0", "P1", "P2", "P3"]
s_crit = f_sales if f_sales else df["Sales PIC"].unique() if not df.empty else []
e_crit = f_eng if f_eng else df["Eng PIC"].unique() if not df.empty else []

if not df.empty:
    filtered_df = df[
        (df["Activity"].astype(str).str.contains(search, case=False, na=False)) &
        (df["Dept"].isin(d_crit)) &
        (df["Project Status"].isin(p_crit)) &
        (df["Sales PIC"].isin(s_crit)) &
        (df["Eng PIC"].isin(e_crit))
    ]
else:
    filtered_df = df

# --- 8. Sidebar (Auto-Progress) ---
with st.sidebar:
    if st.session_state.edit_mode:
        if st.button("⬅️ Back to Add Mode", use_container_width=True):
            st.session_state.edit_mode = False; st.session_state.edit_index = None; st.rerun()
    st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    dv = {"Status": "Planning", "Dept": "Distri-Pro", "Activity": "", "Sales PIC": "None", "Eng PIC": "None", "Priority": "Medium", "Project Status": "P1", "Start Date": datetime.now().date(), "End Date": datetime.now().date(), "Progress": 0}
    if st.session_state.edit_mode and st.session_state.edit_index is not None:
        try:
            row_edit = df.iloc[st.session_state.edit_index]; [dv.update({k: row_edit[k]}) for k in dv if k in row_edit]
        except: st.session_state.edit_mode = False

    s_opts = ["Planning", "In Progress", "Completed", "Delayed"]
    f_status = st.selectbox("Status", s_opts, index=s_opts.index(str(dv["Status"])) if str(dv["Status"]) in s_opts else 0)
    auto_map = {"Planning": 0, "In Progress": 50, "Completed": 100, "Delayed": 25}
    default_prog = int(dv["Progress"]) if st.session_state.edit_mode and f_status == dv["Status"] else auto_map.get(f_status, 0)
    f_progress = st.number_input("ความคืบหน้า (%)", min_value=0, max_value=100, value=default_prog)

    with st.form("action_form", clear_on_submit=True):
        f_dept_in = st.selectbox("Department", list(DEPT_COLORS.keys()), index=list(DEPT_COLORS.keys()).index(str(dv["Dept"])) if str(dv["Dept"]) in DEPT_COLORS else 0)
        f_activity_in = st.text_area("Action Plan & Activity", value=str(dv["Activity"]))
        c1, c2 = st.columns(2)
        f_s_pic = c1.selectbox("Sales PIC", SALES_LIST, index=SALES_LIST.index(str(dv["Sales PIC"])) if str(dv["Sales PIC"]) in SALES_LIST else 0)
        f_e_pic = c2.selectbox("Engineer PIC", ENG_LIST, index=ENG_LIST.index(str(dv["Eng PIC"])) if str(dv["Eng PIC"]) in ENG_LIST else 0)
        c3, c4 = st.columns(2)
        f_prio = c3.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(str(dv["Priority"])) if str(dv["Priority"]) in ["High", "Medium", "Low"] else 1)
        f_pstat_in = c4.selectbox("Project Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(str(dv["Project Status"])) if str(dv["Project Status"]) in ["P0", "P1", "P2", "P3"] else 1)
        c5, c6 = st.columns(2)
        f_start = c5.date_input("Start Date", value=dv["Start Date"])
        f_end = c6.date_input("End Date", value=dv["End Date"])
        if st.form_submit_button("💾 บันทึกข้อมูล", use_container_width=True):
            new_row = {"Dept": f_dept_in, "Activity": f_activity_in, "Sales PIC": f_s_pic, "Eng PIC": f_e_pic, "Status": f_status, "Progress": f_progress, "Start Date": f_start, "End Date": f_end, "Priority": f_prio, "Project Status": f_pstat_in}
            if st.session_state.edit_mode: df.iloc[st.session_state.edit_index] = new_row; st.session_state.edit_mode = False; st.session_state.edit_index = None
            else: df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df); st.rerun()

# --- 9. รายละเอียดแผนงาน ---
if not filtered_df.empty:
    st.subheader(f"📄 รายละเอียดแผนงาน ({len(filtered_df)} รายการ)")
    for index, row in filtered_df.iterrows():
        color = DEPT_COLORS.get(row['Dept'], "#ddd")
        icon = DEPT_ICONS.get(row['Dept'], "⚪")
        header_label = f"{icon} [{row['Project Status']}] {row['Dept']} | {row['Progress']}% | S: {row['Sales PIC']} E: {row['Eng PIC']} - {row['Activity'][:40]}..."
        
        with st.container():
            st.markdown(f"<style>div[data-testid='stExpander']:nth-of-type({index+5}) {{ border-left: 10px solid {color} !important; }}</style>", unsafe_allow_html=True)
            with st.expander(header_label):
                ca, cb, cc = st.columns([2.5, 1.2, 1.2])
                with ca:
                    st.markdown(f"**📋 รายละเอียดกิจกรรม:**")
                    st.info(row['Activity'])
                with cb:
                    st.markdown(f"**สถานะ:** {row['Status']}")
                    st.markdown(f"**ความคืบหน้า:** {row['Progress']}%")
                    if st.button(f"✏️ แก้ไข", key=f"ed_{index}"):
                        actual_idx = df.index[df['Activity'] == row['Activity']].tolist()[0]
                        st.session_state.edit_index = actual_idx; st.session_state.edit_mode = True; st.rerun()
                with cc:
                    st.markdown(f"**Timeline:**")
                    st.markdown(f"{row['Start Date']} ถึง {row['End Date']}")
                    if st.button(f"🗑️ ลบรายการ", key=f"dl_{index}"):
                        actual_idx = df.index[df['Activity'] == row['Activity']].tolist()[0]
                        df = df.drop(actual_idx); save_data(df); st.rerun()
else:
    st.info("ไม่พบข้อมูลที่ตรงกับตัวกรองครับ")
