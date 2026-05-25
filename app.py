import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. ตั้งค่าหน้าจอ
st.set_page_config(page_title="Engineering Master Scheduler 3.0", layout="wide")

# 2. ปรับสีพื้นหลังและตัวหนังสือ (CSS Dashboard Theme)
st.markdown("""
<style>
    /* พื้นหลังสีเทาเข้มแบบในภาพ */
    .stApp { background-color: #f0f2f6; }
    
    /* ปรับแต่งสีข้อความและหัวข้อให้เด่น */
    h1, h2, h3 { color: #2c3e50; }
    
    /* กล่องข้อมูล (Cards) */
    .dashboard-card { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        margin-bottom: 20px;
    }
    
    /* สีแถบเน้น */
    .accent-bar { border-left: 5px solid #f5a623; padding-left: 15px; }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar (แถบด้านข้าง)
with st.sidebar:
    st.markdown("## ⚙️ ตั้งค่าโครงการ")
    st.selectbox("เลือกทีม", ["Team A", "Team B", "Team C"])
    st.date_input("เลือกช่วงเวลา")
    st.button("🔄 อัปเดตข้อมูล")

# 4. Main Content (Dashboard ตามภาพ)
st.markdown('<h1 class="accent-bar">Engineering Master Scheduler 3.0</h1>', unsafe_allow_html=True)

# Metric Boxes
c1, c2, c3, c4 = st.columns(4)
c1.metric("งานคงค้าง (P2)", "12", "+2")
c2.metric("งานเสร็จสิ้น (P3)", "45", "+5")
c3.metric("อยู่ระหว่างรอ", "8", "-1")
c4.metric("วิศวกรว่าง", "3", "0")

# ตารางข้อมูล
st.markdown('<div class="dashboard-card"><h3>📋 รายชื่อพนักงานและตารางงานปัจจุบัน</h3>', unsafe_allow_html=True)
data = pd.DataFrame({
    "พนักงาน": ["คุณ A", "คุณ B", "คุณ C"],
    "สถานะ": ["P2", "P3", "P1"],
    "รายละเอียด": ["โครงการ A", "โครงการ B", "โครงการ C"]
})
st.table(data)
st.markdown('</div>', unsafe_allow_html=True)

# Heatmap
st.markdown('<div class="dashboard-card"><h3>📅 ปฏิทินงานรายบุคคล (Heatmap)</h3>', unsafe_allow_html=True)
fig = go.Figure(data=go.Heatmap(
    z=[[1, 20, 30], [20, 1, 60], [30, 60, 1]],
    colorscale='Viridis'
))
fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
