import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. การตั้งค่าหน้าจอให้กว้างเพื่อรองรับ Dashboard
st.set_page_config(page_title="Engineering Scheduler UI", layout="wide")

# 2. ปรับแต่ง CSS เพื่อให้ได้ Look & Feel เหมือนในภาพ
st.markdown("""
<style>
    /* สีพื้นหลัง Dashboard */
    .stApp { background-color: #f0f2f6; }
    
    /* สไตล์กล่องข้อมูล (Cards) */
    .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
    
    /* หัวข้อหลัก */
    .main-title { color: #2c3e50; font-weight: bold; border-left: 5px solid #f5a623; padding-left: 15px; }
    
    /* ปรับแต่งตาราง */
    div[data-testid="stDataFrame"] { background: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. ส่วน Header
st.markdown('<h1 class="main-title">📊 Engineering Master Scheduler 3.0</h1>', unsafe_allow_html=True)
st.write("---")

# 4. Mockup Data (แทนที่ส่วนนี้ด้วยการโหลดจากไฟล์จริงหรือ DB ของคุณ)
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "พนักงาน": ["คุณ A", "คุณ B", "คุณ C"],
        "สถานะ": ["P2", "P3", "P1"],
        "รายละเอียด": ["โครงการ A", "โครงการ B", "โครงการ C"]
    })

# 5. สร้างส่วนประกอบตามภาพตัวอย่าง
# ส่วนที่ 1: สรุปผล (KPIs หรือ Status)
col1, col2, col3, col4 = st.columns(4)
col1.metric("งานคงค้าง (P2)", "12", "+2")
col2.metric("งานเสร็จสิ้น (P3)", "45", "+5")
col3.metric("อยู่ระหว่างรอ", "8", "-1")
col4.metric("วิศวกรว่าง", "3", "0")

# ส่วนที่ 2: ตารางข้อมูลหลัก
st.markdown('<div class="card"><h3>📋 รายชื่อพนักงานและตารางงานปัจจุบัน</h3>', unsafe_allow_html=True)
edited_df = st.data_editor(st.session_state.data, use_container_width=True, num_rows="dynamic")
st.markdown('</div>', unsafe_allow_html=True)

# ส่วนที่ 3: กราฟ Heatmap (เหมือนในภาพที่คุณต้องการ)
st.markdown('<div class="card"><h3>📅 ปฏิทินงานรายบุคคล (Heatmap)</h3>', unsafe_allow_html=True)
# สร้าง Dummy Heatmap
fig = go.Figure(data=go.Heatmap(
    z=[[1, 20, 30], [20, 1, 60], [30, 60, 1]],
    colorscale='Viridis'
))
fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ส่วนที่ 4: Sidebar สำหรับตั้งค่า
with st.sidebar:
    st.title("⚙️ ตั้งค่าโครงการ")
    st.selectbox("เลือกทีม", ["Team A", "Team B", "Team C"])
    st.date_input("เลือกช่วงเวลา")
    if st.button("🔄 อัปเดตข้อมูล"):
        st.rerun()
