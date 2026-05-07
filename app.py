import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Company Action Plan 2026", layout="wide")

# --- ปรับแต่งสี Sidebar และองค์ประกอบหน้าเว็บ ---
st.markdown("""
    <style>
    /* ปรับสีพื้นหลังของ Sidebar (ด้านซ้าย) */
    [data-testid="stSidebar"] {
        background-color: #0b5345; /* สีเขียวเข้มตามธีม */
        color: white;
    }
    
    /* ปรับสีตัวหนังสือใน Sidebar ให้เป็นสีขาว */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
        color: white !important;
    }

    /* ปรับแต่งปุ่มใน Sidebar */
    [data-testid="stSidebar"] .stButton>button {
        background-color: #f1c40f; /* สีเหลืองทองให้ตัดกับเขียว */
        color: #0b5345;
        font-weight: bold;
        border-radius: 8px;
    }

    /* ปรับแต่งกล่องเมทริกซ์ด้านบน */
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0b5345;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ฟังก์ชันจัดการข้อมูล (เหมือนเดิม)
DATA_FILE = "action_plan_2026.csv"

def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        df['Start Date'] = pd.to_datetime(df['Start Date'])
        df['End Date'] = pd.to_datetime(df['End Date'])
        return df
    except:
        return pd.DataFrame(columns=["Dept", "Activity", "Target", "PIC", "Support", "Status", "Progress", "Start Date", "End Date", "Priority", "Project Status"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --- 3. ส่วนหัวข้อ (Title & Logo) ---
# สร้าง 2 คอลัมน์สำหรับโลโก้และชื่อเรื่อง
col_title1, col_title2 = st.columns([0.1, 0.9])

with col_title1:
    # ใส่รูปโลโก้ของคุณตรงนี้ (เปลี่ยน URL เป็นรูปที่คุณต้องการได้เลย)
    st.image("https://t4.ftcdn.net/jpg/01/38/23/39/360_F_138233979_Ns6YHS8w4b4jDEvi7oppdU79Fzw9pSY3.jpg", width=700)

with col_title2:
    st.title("2026 Follow up & Action Plan")
    st.write("### Project Dashboard | Engineer Center")

st.markdown("---")

# 4. ส่วนการกรอกข้อมูล (Sidebar)
with st.sidebar:
    st.header("📋 เพิ่มแผนงานใหม่")
    with st.form("action_form", clear_on_submit=True):
        dept = st.selectbox("Department", ["Distri-Pro", "Post", "Broadcast", "Residential", "Cinema", "ENG-Center"])
        activity = st.text_area("Action Plan & Activity")
        target = st.text_area("Target / Objective")
        pic = st.text_input("PIC (ผู้รับผิดชอบ)")
        support = st.text_input("Support Needed")
        
        col_side1, col_side2 = st.columns(2)
        priority = col_side1.selectbox("Priority", ["High", "Medium", "Low"])
        p_status = col_side2.selectbox("Project Status", ["P0", "P1", "P2", "P3"])
        
        col_in1, col_in2 = st.columns(2)
        start_date = col_in1.date_input("Start Date")
        end_date = col_in2.date_input("End Date")
        
        status = st.selectbox("Status", ["Planning", "In Progress", "Completed", "Delayed"])
        progress = st.slider("Progress (%)", 0, 100, 0)
        
        submitted = st.form_submit_button("บันทึกแผนงาน")
        if submitted and activity:
            new_row = {
                "Dept": dept, "Activity": activity, "Target": target, "PIC": pic, 
                "Support": support, "Status": status, "Progress": progress,
                "Start Date": start_date, "End Date": end_date,
                "Priority": priority, "Project Status": p_status
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success("บันทึกข้อมูลเรียบร้อย!")
            st.rerun()

# 5. ส่วนแสดงผลกราฟและตาราง (เหมือนเดิม)
if not df.empty:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("งานทั้งหมด", len(df))
    m2.metric("ความคืบหน้าเฉลี่ย", f"{df['Progress'].mean():.1f}%")
    m3.metric("งานเร่งด่วน (High)", len(df[df['Priority']=='High']))
    m4.metric("สถานะ P0 (Critical)", len(df[df['Project Status']=='P0']))

    st.markdown("---")
    
    col_left, col_right = st.columns([2,1])
    
    with col_left:
        st.subheader("📈 Timeline & Progress")
        fig = px.timeline(df, x_start="Start Date", x_end="End Date", y="Activity", 
                          color="Project Status",
                          hover_data=["Priority", "Progress"],
                          color_discrete_map={"P0": "#e74c3c", "P1": "#f39c12", "P2": "#3498db", "P3": "#2ecc71"})
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("📊 Priority Distribution")
        fig_pie = px.pie(df, names="Priority", hole=0.4, 
                         color="Priority",
                         color_discrete_map={"High": "#e74c3c", "Medium": "#f39c12", "Low": "#2ecc71"})
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("📄 Detailed Action Plan Table")
    
    for index, row in df.iterrows():
        header_label = f"[{row.get('Project Status', 'N/A')}] [{row.get('Priority', 'N/A')}] {row['Dept']} : {row['Activity'][:40]}..."
        with st.expander(header_label):
            c1, c2, c3, c4 = st.columns([1, 1.5, 1.5, 1])
            with c1:
                st.write(f"**PIC:** {row['PIC']}")
                st.write(f"**Status:** {row['Status']}")
            with c2:
                st.write(f"**Priority:** {row.get('Priority', 'N/A')}")
                st.write(f"**Project Status:** {row.get('Project Status', 'N/A')}")
            with c3:
                st.write(f"**Target:** {row['Target']}")
            with c4:
                if st.button("🗑️ ลบ", key=f"del_{index}"):
                    df = df.drop(index)
                    save_data(df)
                    st.rerun()

    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Download CSV", csv, "action_plan_2026.csv", "text/csv")
else:
    st.info("เริ่มสร้างแผนงานแรกของคุณที่แถบด้านซ้ายมือได้เลยครับ")
