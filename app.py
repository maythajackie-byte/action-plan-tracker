import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Company Action Plan 2026", layout="wide")

# --- ปรับแต่ง CSS (Sidebar เขียวเข้ม + ธีมสี) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b5345; color: white; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label { color: white !important; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #0b5345; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .stButton>button { border-radius: 5px; width: 100%; }
    h1, h2, h3 { color: #0b5345; }
    </style>
    """, unsafe_allow_html=True)

# 2. รายชื่อพนักงานทั้งหมด (รวมรายชื่อ Sales 3 ท่านล่าสุด)
PIC_LIST = [
    "CB : Chanunkarn", "AW : Apasri", "TH : Thanyhathorn", # Sales
    "CK : Chatchai", "BS : Boonchob", "PU : Pankrich", "MS : Maytha", 
    "KC : Kiattisak", "DR : Danuphop", "SB : Sarawut", "KL : Kongphop",
    "DS : Decha", "PT : Patjitra", "WS : Worawut", "RO : Ronnarit",
    "NI : Nutwarot", "SK : Sirisak", "KI : Kathathep", "CA : Chatchawan",
    "NM : Nithithorn", "PA : Phaisan", "CN : Chainarong", "PH : Parawee",
    "TC : Totsapol", "WO : Watcharakorn", "VP : Veeraphat", "MK : Monrak",
    "PL : Preecha", "NC : Nattipong"
]

# 3. ฟังก์ชันจัดการข้อมูล
DATA_FILE = "action_plan_2026.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['Start Date'] = pd.to_datetime(df['Start Date']).dt.date
        df['End Date'] = pd.to_datetime(df['End Date']).dt.date
        # ตรวจสอบคอลัมน์ใหม่ถ้าไม่มีให้เพิ่มเข้าไป
        for col in ["Priority", "Project Status"]:
            if col not in df.columns: df[col] = "Normal"
        return df
    return pd.DataFrame(columns=["Dept", "Activity", "Target", "PIC", "Support", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# จัดการโหมดการแก้ไข
if 'edit_mode' not in st.session_state: st.session_state.edit_mode = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# 4. ส่วนหัวข้อ (Header & Logo)
c_l1, c_l2 = st.columns([0.1, 0.9])
with c_l1:
    # เปลี่ยน URL รูปเป็นรูป Action Plan ของคุณ
    st.image("https://flaticon.com", width=70)
with c_l2:
    st.title("2026 Follow up & Action Plan")
    st.subheader("Project Dashboard | Engineer Center")

# 5. Sidebar (Input & Edit Form)
with st.sidebar:
    st.header("📝 " + ("แก้ไขข้อมูล" if st.session_state.edit_mode else "เพิ่มแผนงานใหม่"))
    
    # ค่าตั้งต้นกรณีแก้ไข
    val = df.iloc[st.session_state.edit_index] if st.session_state.edit_mode else None
    
    with st.form("action_form", clear_on_submit=True):
        dept = st.selectbox("Department", ["Distri-Pro", "Post", "Broadcast", "Residential", "Cinema", "ENG-Center"],
                            index=["Distri-Pro", "Post", "Broadcast", "Residential", "Cinema", "ENG-Center"].index(val['Dept']) if val is not None else 0)
        activity = st.text_area("Action Plan & Activity", value=val['Activity'] if val is not None else "")
        pic = st.selectbox("PIC (ผู้รับผิดชอบ)", PIC_LIST, 
                           index=PIC_LIST.index(val['PIC']) if val is not None and val['PIC'] in PIC_LIST else 0)
        
        col_s1, col_s2 = st.columns(2)
        priority = col_s1.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(val['Priority']) if val is not None else 1)
        p_status = col_s2.selectbox("Project Status", ["P0", "P1", "P2", "P3"], index=["P0", "P1", "P2", "P3"].index(val['Project Status']) if val is not None else 1)
        
        target = st.text_input("Target / Objective", value=val['Target'] if val is not None else "")
        support = st.text_input("Support Needed", value=val['Support'] if val is not None else "")
        
        col_d1, col_d2 = st.columns(2)
        start_date = col_d1.date_input("Start Date", value=val['Start Date'] if val is not None else datetime.now().date())
        end_date = col_d2.date_input("End Date", value=val['End Date'] if val is not None else datetime.now().date())
        
        status = st.selectbox("Status", ["Planning", "In Progress", "Completed", "Delayed"], 
                              index=["Planning", "In Progress", "Completed", "Delayed"].index(val['Status']) if val is not None else 0)
        progress = st.slider("Progress (%)", 0, 100, int(val['Progress']) if val is not None else 0)
        
        submitted = st.form_submit_button("💾 บันทึกข้อมูล")
        if submitted and activity:
            new_data = {
                "Dept": dept, "Activity": activity, "Target": target, "PIC": pic, "Support": support,
                "Status": status, "Progress": progress, "Start Date": start_date, "End Date": end_date,
                "Priority": priority, "Project Status": p_status
            }
            if st.session_state.edit_mode:
                df.iloc[st.session_state.edit_index] = new_data
                st.session_state.edit_mode = False
            else:
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            save_data(df)
            st.success("บันทึกสำเร็จ!")
            st.rerun()

    if st.session_state.edit_mode:
        if st.button("❌ ยกเลิกการแก้ไข"):
            st.session_state.edit_mode = False
            st.rerun()

# 6. ส่วนแสดงผล (Main Dashboard)
if not df.empty:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("งานทั้งหมด", len(df))
    m2.metric("เฉลี่ยความคืบหน้า", f"{df['Progress'].mean():.1f}%")
    m3.metric("สถานะ P0", len(df[df['Project Status'] == 'P0']))
    m4.metric("เสร็จสิ้น", len(df[df['Status'] == 'Completed']))

    st.markdown("---")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📈 Timeline & Progress")
        fig = px.timeline(df, x_start="Start Date", x_end="End Date", y="Activity", color="Project Status", text="Progress",
                          color_discrete_map={"P0":"#e74c3c", "P1":"#e67e22", "P2":"#3498db", "P3":"#2ecc71"})
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        st.subheader("📉 Overall Trend")
        trend_df = df.sort_values("End Date")
        fig_line = px.line(trend_df, x="End Date", y="Progress", markers=True, color_discrete_sequence=['#1D8348'])
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    st.subheader("📄 รายละเอียดแผนงาน")
    for index, row in df.iterrows():
        with st.expander(f"📌 [{row['Project Status']}] {row['Dept']} : {row['PIC']} - {row['Activity'][:40]}..."):
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.write(f"**Activity:** {row['Activity']}")
                st.write(f"**Target:** {row['Target']}")
            with c2:
                st.write(f"**Progress:** {row['Progress']}%")
                if st.button(f"✏️ แก้ไข", key=f"ed_{index}"):
                    st.session_state.edit_index = index
                    st.session_state.edit_mode = True
                    st.rerun()
            with c3:
                st.write(f"**Timeline:** {row['Start Date']} - {row['End Date']}")
                if st.button(f"🗑️ ลบ", key=f"dl_{index}"):
                    df = df.drop(index)
                    save_data(df)
                    st.rerun()

    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Download Data (CSV)", csv, "action_plan_2026.csv", "text/csv")
else:
    st.info("ยังไม่มีข้อมูล กรุณากรอกแผนงานที่แถบด้านซ้ายมือครับ")
