import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Action Plan 2026", layout="wide")

# --- ปรับแต่ง CSS ใหม่ (เน้นความชัดเจนของกล่อง Dropdown/Expander) ---
st.markdown("""
    <style>
    /* พื้นหลังหลัก */
    .main { background-color: #f0f2f6; }
    
    /* กล่องรายการ (Expander) */
    div[data-testid="stExpander"] {
        background-color: white !important;
        border: 1px solid #0b5345 !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    /* ตัวหนังสือในหัวข้อ Expander */
    div[data-testid="stExpander"] p {
        color: #0b5345 !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }

    /* ปรับแต่งปุ่มภายในกล่อง */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    
    /* สีปุ่มแก้ไข */
    div[key^="ed_"] button {
        background-color: #f1c40f !important;
        color: #0b5345 !important;
        border: none !important;
    }
    
    /* สีปุ่มลบ */
    div[key^="dl_"] button {
        background-color: #e74c3c !important;
        color: white !important;
        border: none !important;
    }

    /* Metric Boxes */
    [data-testid="stMetric"] {
        background-color: white !important;
        border-left: 8px solid #0b5345 !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2-5. (ส่วนของข้อมูล รายชื่อ และ Sidebar ใช้เหมือนเดิม)
# ... (ผมละไว้เพื่อความกระชับ แต่ในไฟล์จริงให้คงไว้ตามเดิมนะครับ) ...

# 6. ส่วนแสดงผล (Detailed Action Plan Table)
if not df.empty:
    st.markdown("---")
    st.subheader("📄 รายละเอียดแผนงาน (คลิกเพื่อดูรายละเอียดและแก้ไข)")
    for index, row in df.iterrows():
        # สร้างป้ายกำกับสถานะ (Tag)
        p_status = row['Project Status']
        dept = row['Dept']
        
        # หัวข้อที่แสดงบนกล่อง
        header_text = f"📌 [{p_status}] {dept} | S: {row['Sales PIC']} | E: {row['Eng PIC']} - {row['Activity'][:40]}..."
        
        with st.expander(header_text):
            col_a, col_b, col_c = st.columns([2, 1, 1])
            with col_a:
                st.write(f"**กิจกรรม:** {row['Activity']}")
                st.write(f"**สถานะ:** {row['Status']} ({row['Progress']}%)")
            with col_b:
                if st.button(f"✏️ แก้ไขข้อมูล", key=f"ed_{index}"):
                    st.session_state.edit_index = index
                    st.session_state.edit_mode = True
                    st.rerun()
            with col_c:
                if st.button(f"🗑️ ลบรายการ", key=f"dl_{index}"):
                    df = df.drop(index)
                    save_data(df)
                    st.rerun()
