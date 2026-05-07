import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. ตั้งค่าหน้าเว็บและธีมสีเขียว
st.set_page_config(page_title="Company Action Plan 2026", layout="wide")

# Custom CSS เพื่อปรับสีให้เหมือนในภาพ (โทนเขียวเข้มและเหลืองทอง)
st.markdown("""
    <style>
    .main { background-color: #f5f7f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #0b5345; shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .stButton>button { background-color: #0b5345; color: white; border-radius: 5px; }
    h1, h2, h3 { color: #0b5345; font-family: 'Sarabun', sans-serif; }
    div[data-testid="stExpander"] { border: 1px solid #0b5345; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. ฟังก์ชันจัดการข้อมูล
DATA_FILE = "action_plan_2026.csv"

def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        df['Start Date'] = pd.to_datetime(df['Start Date'])
        df['End Date'] = pd.to_datetime(df['End Date'])
        return df
    except:
        return pd.DataFrame(columns=["Dept", "Activity", "Target", "PIC", "Support", "Status", "Progress", "Start Date", "End Date"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# 3. ส่วนหัวข้อ (Header)
st.title("📋 2026 Follow up & Action Plan")
st.subheader("Project Dashboard")

# 4. ส่วนการกรอกข้อมูล (Sidebar) - ปรับตามหัวข้อในภาพ
with st.sidebar:
    st.image("https://flaticon.com", width=100)
    st.header("📋 เพิ่มแผนงานใหม่")
    with st.form("action_form", clear_on_submit=True):
        dept = st.selectbox("Department", ["BCP-ENG", "Sales", "Marketing", "HR"])
        activity = st.text_area("Action Plan & Activity")
        target = st.text_area("Target / Objective")
        pic = st.text_input("PIC (ผู้รับผิดชอบ)")
        support = st.text_input("Support Needed")
        
        col_in1, col_in2 = st.columns(2)
        start_date = col_in1.date_input("Start Date")
        end_date = col_in2.date_input("End Date")
        
        status = st.selectbox("Status", ["Planning", "In Progress", "Completed", "Delayed"])
        progress = st.slider("Progress (%)", 0, 100, 0)
        
        submitted = st.form_submit_button("บันทึกแผนงาน")
        if submitted and activity:
            new_row = {"Dept": dept, "Activity": activity, "Target": target, "PIC": pic, 
                       "Support": support, "Status": status, "Progress": progress,
                       "Start Date": start_date, "End Date": end_date}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success("บันทึกข้อมูลเรียบร้อย!")

# 5. ส่วนแสดงผลกราฟ (Visuals)
if not df.empty:
    # คำนวณ Metric
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("งานทั้งหมด", len(df))
    m2.metric("ความคืบหน้าเฉลี่ย", f"{df['Progress'].mean():.1f}%")
    m3.metric("เสร็จสิ้น", len(df[df['Status']=='Completed']))
    m4.metric("กำลังดำเนินการ", len(df[df['Status']=='In Progress']))

    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # กราฟความคืบหน้า (Gantt Chart แบบย่อย)
        st.subheader("📈 Timeline & Progress")
        fig = px.timeline(df, x_start="Start Date", x_end="End Date", y="Activity", 
                          color="Progress", text="Progress",
                          color_continuous_scale='Greens', title="แผนการดำเนินงานรายไตรมาส")
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # กราฟเส้นความคืบหน้า (Trend Line)
        st.subheader("📉 Overall Progress Trend")
        # จำลองข้อมูล Trend (ในอนาคตสามารถปรับตามวันที่บันทึกจริงได้)
        trend_data = df.sort_values("End Date")
        fig_line = px.line(trend_data, x="End Date", y="Progress", markers=True,
                           line_shape="spline", color_discrete_sequence=['#1D8348'])
        st.plotly_chart(fig_line, use_container_width=True)

    # 6. ส่วนรายละเอียดงาน (คล้ายตารางในรูปภาพ)
    st.markdown("---")
    st.subheader("📄 Detailed Action Plan Table")
    
    # ปรับแต่งตารางให้ดูง่าย
    for index, row in df.iterrows():
        with st.expander(f"📌 {row['Dept']} : {row['Activity'][:50]}... (Progress: {row['Progress']}%)"):
            c1, c2, c3 = st.columns([1, 2, 1])
            with c1:
                st.write(f"**PIC:** {row['PIC']}")
                st.write(f"**Status:** {row['Status']}")
            with c2:
                st.write(f"**Target:** {row['Target']}")
                st.write(f"**Support Needed:** {row['Support']}")
            with c3:
                st.write(f"**Timeline:** {row['Start Date'].strftime('%d %b')} - {row['End Date'].strftime('%d %b %Y')}")
                if st.button(f"ลบงานที่ {index+1}", key=f"del_{index}"):
                    df = df.drop(index)
                    save_data(df)
                    st.rerun()

    # ปุ่มดาวน์โหลด
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Download Action Plan (CSV)", csv, "action_plan_2026.csv", "text/csv")

else:
    st.info("เริ่มสร้างแผนงานแรกของคุณที่แถบด้านซ้ายมือได้เลยครับ")
