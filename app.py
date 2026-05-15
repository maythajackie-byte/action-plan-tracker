import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- Master CSS ปรับปรุงสีตัวหนังสือในกล่องสรุป ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b5345; color: white; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: white !important; }
    
    /* สไตล์ Tabs ใน Sidebar */
    div[data-testid="stTabs"] button { color: #1a1a1a; font-weight: 600; }
    div[data-testid="stTabs"] button[aria-selected="true"] { color: #0b5345 !important; border-bottom-color: #0b5345 !important; }

    /* กล่องสรุปภาพรวม (Metrics) */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #0b5345;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    [data-testid="stMetricLabel"] {
        color: #0b5345 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }

    /* กล่องรายละเอียดสีขาว + ตัวหนังสือดำ */
    div[data-testid="stExpander"] { background-color: white !important; border-radius: 12px !important; border: 1px solid #ddd !important; margin-bottom: 10px !important; }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] span, div[data-testid="stExpander"] label, div[data-testid="stExpander"] div { color: #1a1a1a !important; }
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
MA_EXCEL_FILE = "ma_plan_data.xlsx" # ไฟล์สำหรับเก็บข้อมูล MA/MT แบบ Excel

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

def load_ma_data():
    if os.path.exists(MA_EXCEL_FILE):
        try:
            return pd.read_excel(MA_EXCEL_FILE, engine='openpyxl').fillna("-")
        except: pass
    # โครงสร้างตาราง Default ถ้ายังไม่มีไฟล์
    return pd.DataFrame(columns=["Project / Customer", "Category", "Last MA", "Next MA", "Status"])

def save_data(df_s): df_s.to_csv(DATA_FILE, index=False) # แก้ไขจาก to_exel เป็น to_csv ให้ถูกต้อง
def save_ma_data(df_m): df_m.to_excel(MA_EXCEL_FILE, index=False, engine='openpyxl')

df = load_data()
df_ma = load_ma_data()

if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# --- 4. ส่วนบนสุด (Banner & Title) ---
st.image("https://www.nimblework.com/wp-content/uploads/2024/05/Action-plan.png", use_container_width=50)
st.title("📋 2026 Follow up & Action Plan")
st.write("### Project Dashboard | Engineer Center")

# --- 5. 🚨 ไฮไลท์งานด่วน ---
if not df.empty:
    today = datetime.now().date()
    near_deadline = today + timedelta(days=7)
    urgent_df = df[(df['Project Status'] == 'P0') | (df['End Date'] <= near_deadline)]
    urgent_df = urgent_df[pd.to_numeric(urgent_df['Progress'], errors='coerce') < 100]

    if not urgent_df.empty:
        st.error(f"### 🚨 งานด่วนพิเศษ & ใกล้กำหนดส่ง ({len(urgent_df)} รายการ)")
        cols_u = st.columns(3)
        for i, (idx, row) in enumerate(urgent_df.head(3).iterrows()):
            with cols_u[i % 3]:
                st.markdown(f"""<div class="urgent-box"><b>{row['Dept']}</b><br>{row['Activity'][:50]}...<br>📅 Deadline: {row['End Date']}</div>""", unsafe_allow_html=True)

# --- 6. สรุปภาพรวม (Metrics & Graphs) ---
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


# --- 6.5 ตาราง MA/MT ดึงข้อมูลจาก Excel อัตโนมัติ ---
st.markdown("---")
st.subheader("🛠️ MA & MT Tracking Plan (2024-2025)")

if df_ma.empty:
    st.info("ยังไม่มีข้อมูล MA/MT กรุณาอัปโหลดไฟล์ Excel ที่แถบเมนูด้านซ้ายมือครับ (ต้องมีหัว Column: Project / Customer, Category, Last MA, Next MA, Status)")
else:
    # สร้าง HTML Table แบบไดนามิกจาก DataFrame
    ma_html = """<div style="background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #ddd; margin-bottom: 20px;">
    <p style="color: #444; font-size: 16px;">ระบบบริหารจัดการและติดตามแผนการบำรุงรักษาระบบ (Maintenance Agreement) ของลูกค้าอย่างต่อเนื่อง</p>
    <table style="width:100%; border-collapse: collapse; text-align: left; font-family: sans-serif; margin-top: 15px;">
    <tr style="background-color: #0b5345; color: white;">
    <th style="padding: 12px; border-bottom: 2px solid #ddd;">Project / Customer</th>
    <th style="padding: 12px; border-bottom: 2px solid #ddd;">Category</th>
    <th style="padding: 12px; border-bottom: 2px solid #ddd;">Last MA</th>
    <th style="padding: 12px; border-bottom: 2px solid #ddd;">Next MA</th>
    <th style="padding: 12px; border-bottom: 2px solid #ddd; text-align: center;">Status</th>
    </tr>"""

    for _, row in df_ma.iterrows():
        # ป้องกันค่า NaN
        status = str(row.get('Status', '-')).strip()
        category = str(row.get('Category', '-'))
        next_ma = str(row.get('Next MA', '-'))
        
        # จัดสีตามข้อความ
        next_ma_style = "color: #dc3545; font-weight: bold;" if next_ma.lower() == "run out" else "color: #1a1a1a;"
        badge_bg = "#28a745" if status.lower() == "done" else "#ffc107" if status.lower() == "pending" else "#dc3545"
        badge_color = "white" if status.lower() in ["done", "run out"] else "black"
        cat_color = "#e74c3c" if "MA" in category else "#3498db"

        ma_html += f"""
        <tr style="border-bottom: 1px solid #eee;">
        <td style="padding: 12px; color: #1a1a1a;">{row.get('Project / Customer', '-')}</td>
        <td style="padding: 12px;"><span style="color: {cat_color}; font-weight: bold;">{category}</span></td>
        <td style="padding: 12px; color: #1a1a1a;">{row.get('Last MA', '-')}</td>
        <td style="padding: 12px; {next_ma_style}">{next_ma}</td>
        <td style="padding: 12px; text-align: center;">
            <span style="background-color: {badge_bg}; color: {badge_color}; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600;">{status}</span>
        </td>
        </tr>"""
    
    ma_html += "</table></div>"
    st.markdown(ma_html, unsafe_allow_html=True)


# --- 7. ระบบ Filter ---
st.markdown("---")
st.subheader("🔍 ตัวกรองข้อมูล (Filters)")
f_c1, f_c2 = st.columns([2, 2])
search = f_c1.text_input("🔎 ค้นหาชื่องาน", placeholder="พิมพ์เพื่อค้นหา...")
f_dept = f_c2.multiselect("🏢 แผนก", options=df["Dept"].unique() if not df.empty else [])

f_c3, f_c4, f_c5 = st.columns(3)
f_pstat = f_c3.multiselect("⏳ Project Status", options=["P0", "P1", "P2", "P3"])
f_sales = f_c4.multiselect("👤 Sales", options=df["Sales PIC"].unique() if not df.empty else [])
f_eng = f_c5.multiselect("🛠 Engineer", options=df["Eng PIC"].unique() if not df.empty else [])

d_crit = f_dept if f_dept else df["Dept"].unique() if not df.empty else []
p_crit = f_pstat if f_pstat else ["P0", "P1", "P2", "P3"]
s_crit = f_sales if f_sales else df["Sales PIC"].unique() if not df.empty else []
e_crit = f_eng if f_eng else df["Eng PIC"].unique() if not df.empty else []

if not df.empty:
    filtered_df = df[(df["Activity"].astype(str).str.contains(search, case=False, na=False)) & (df["Dept"].isin(d_crit)) & (df["Project Status"].isin(p_crit)) & (df["Sales PIC"].isin(s_crit)) & (df["Eng PIC"].isin(e_crit))]
else:
    filtered_df = df


# --- 8. Sidebar แบบมี Tabs ---
with st.sidebar:
    tab_action, tab_upload = st.tabs(["📝 Action Plan", "📁 อัปโหลด MA Excel"])
    
    # -------- Tab 1: จัดการ Action Plan --------
    with tab_action:
        if st.session_state.edit_mode:
            if st.button("⬅️ Back to Add Mode", use_container_width=True):
                st.session_state.edit_mode = False; st.session_state.edit_index = None; st.rerun()
        st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
        dv = {"Status": "Planning", "Dept": "Distri-Pro", "Activity": "", "Sales PIC": "None", "Eng PIC": "None", "Priority": "Medium", "Project Status": "P1", "Start Date": datetime.now().date(), "End Date": datetime.now().date(), "Progress": 0}
        if st.session_state.edit_mode and st.session_state.edit_index is not None:
            try:
                row_e = df.iloc[st.session_state.edit_index if isinstance(st.session_state.edit_index, int) else st.session_state.edit_index[0]]
                for k in dv: dv[k] = row_e[k] if k in row_e else dv[k]
            except: st.session_state.edit_mode = False

        f_status = st.selectbox("Status", ["Planning", "In Progress", "Completed", "Delayed"], index=["Planning", "In Progress", "Completed", "Delayed"].index(str(dv["Status"])) if str(dv["Status"]) in ["Planning", "In Progress", "Completed", "Delayed"] else 0)
        auto_m = {"Planning": 0, "In Progress": 50, "Completed": 100, "Delayed": 25}
        f_progress = st.number_input("ความคืบหน้า (%)", 0, 100, int(dv["Progress"]) if st.session_state.edit_mode and f_status == dv["Status"] else auto_m.get(f_status, 0))

        with st.form("action_form", clear_on_submit=True):
            f_dept_in = st.selectbox("Department", list(DEPT_COLORS.keys()), index=list(DEPT_COLORS.keys()).index(str(dv["Dept"])) if str(dv["Dept"]) in DEPT_COLORS else 0)
            f_act = st.text_area("Activity", value=str(dv["Activity"]))
            c1, c2 = st.columns(2)
            f_s = c1.selectbox("Sales PIC", SALES_LIST, index=SALES_LIST.index(str(dv["Sales PIC"])) if str(dv["Sales PIC"]) in SALES_LIST else 0)
            f_e = c2.selectbox("Eng PIC", ENG_LIST, index=ENG_LIST.index(str(dv["Eng PIC"])) if str(dv["Eng PIC"]) in ENG_LIST else 0)
            c3, c4 = st.columns(2)
            f_prio = c3.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(str(dv["Priority"])) if str(dv["Priority"]) in ["High", "Medium", "Low"] else 1)
            f_ps = c4.selectbox("P-Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(str(dv["Project Status"])) if str(dv["Project Status"]) in ["P0", "P1", "P2", "P3"] else 1)
            c5, c6 = st.columns(2)
            f_start, f_end = c5.date_input("Start", dv["Start Date"]), c6.date_input("End", dv["End Date"])
            
            if st.form_submit_button("💾 บันทึกข้อมูล", use_container_width=True):
                new_r = {"Dept": f_dept_in, "Activity": f_act, "Sales PIC": f_s, "Eng PIC": f_e, "Status": f_status, "Progress": f_progress, "Start Date": f_start, "End Date": f_end, "Priority": f_prio, "Project Status": f_ps}
                if st.session_state.edit_mode:
                    idx = st.session_state.edit_index if isinstance(st.session_state.edit_index, int) else st.session_state.edit_index[0]
                    df.iloc[idx] = new_r
                else: df = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
                save_data(df); st.rerun()

    # -------- Tab 2: อัปโหลดไฟล์ Excel --------
    with tab_upload:
        st.header("📁 อัปโหลดข้อมูล MA/MT")
        st.write("รองรับไฟล์ .xlsx ที่มีหัวข้อคอลัมน์ดังนี้:\n- Project / Customer\n- Category\n- Last MA\n- Next MA\n- Status")
        uploaded_file = st.file_uploader("ลากไฟล์ Excel มาวางที่นี่", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                new_ma_df = pd.read_excel(uploaded_file, engine='openpyxl')
                st.success("อ่านไฟล์สำเร็จ!")
                if st.button("💾 บันทึกเข้าสู่ระบบตาราง", use_container_width=True):
                    save_ma_data(new_ma_df)
                    st.rerun()
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")


# --- 9. รายละเอียดแผนงาน ---
if not filtered_df.empty:
    st.subheader(f"📄 รายละเอียดแผนงาน ({len(filtered_df)} รายการ)")
    for index, row in filtered_df.iterrows():
        color = DEPT_COLORS.get(row['Dept'], "#ddd")
        icon = DEPT_ICONS.get(row['Dept'], "⚪")
        header = f"{icon} [{row['Project Status']}] {row['Dept']} | {row['Progress']}% | S: {row['Sales PIC']} E: {row['Eng PIC']} - {row['Activity'][:40]}..."
        with st.container():
            st.markdown(f"<style>div[data-testid='stExpander']:nth-of-type({index+5}) {{ border-left: 10px solid {color} !important; }}</style>", unsafe_allow_html=True)
            with st.expander(header):
                ca, cb, cc = st.columns([2.5, 1.2, 1.2])
                with ca: st.markdown(f"**📋 รายละเอียด:**"); st.info(row['Activity'])
                with cb:
                    st.write(f"**สถานะ:** {row['Status']}"); st.write(f"**ความคืบหน้า:** {row['Progress']}%")
                    if st.button(f"✏️ แก้ไข", key=f"ed_{index}"):
                        st.session_state.edit_index = df.index[df['Activity'] == row['Activity']].tolist(); st.session_state.edit_mode = True; st.rerun()
                with cc:
                    st.write(f"**Timeline:**\n{row['Start Date']} ถึง {row['End Date']}")
                    if st.button(f"🗑️ ลบ", key=f"dl_{index}"):
                        df = df.drop(df.index[df['Activity'] == row['Activity']].tolist()); save_data(df); st.rerun()
else: st.info("ไม่พบข้อมูลที่ตรงกับตัวกรองครับ")
