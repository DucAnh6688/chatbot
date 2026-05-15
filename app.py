import streamlit as st
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FLC mất điện | Portfolio",
    page_icon="🚀",
    layout="wide",
)

# --- LOAD CUSTOM CSS ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# --- HERO SECTION ---
st.markdown("""
<div class="hero-container animate-in">
    <h1>FLC mất điện</h1>
    <p class="hero-subtitle">
        Xây dựng giải pháp thông minh tại giao điểm giữa <strong>Tài chính</strong> 
        và <strong>Trí tuệ nhân tạo</strong>. Chuyên về tích hợp LLM, NVIDIA NIM 
        và tự động hóa phân tích kỹ thuật.
    </p>
    <div class="hero-links">
        <a href="https://linkedin.com" target="_blank">🔗 LinkedIn</a>
        <a href="https://github.com" target="_blank">💻 GitHub</a>
        <a href="mailto:contact@grafity.ai">📧 Email</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- PROJECTS ---
st.markdown("""
<div class="section-header">
    <h2>🛠️ Dự án</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="glass-card animate-in">
        <h3>📈 AI Stock Assistant</h3>
        <p>Chatbot phân tích chứng khoán Việt Nam tích hợp AI.</p>
        <div style="margin: 0.8rem 0;">
            <span class="badge">Streamlit</span>
            <span class="badge">Gemini</span>
            <span class="badge">vnstock</span>
            <span class="badge">Plotly</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted);">
            Hỗ trợ đa nhà cung cấp LLM, biểu đồ kỹ thuật, 
            chỉ báo SMA/RSI/MACD và phân tích AI tự động.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Khám phá Stock Assistant →", use_container_width=True, key="btn_stock"):
        st.switch_page("pages/1_📈_Stock_Assistant.py")

with col2:
    st.markdown("""
    <div class="glass-card animate-in" style="animation-delay: 0.1s;">
        <h3>🧬 Dự án AI tiếp theo</h3>
        <p>Đang phát triển dự án mới về Computer Vision & Predictive Modeling.</p>
        <div style="margin: 0.8rem 0;">
            <span class="badge">Computer Vision</span>
            <span class="badge">Deep Learning</span>
            <span class="badge">R&D</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted);">
            Trạng thái: Nghiên cứu & Phát triển<br>
            Dự kiến ra mắt: Q3 2026
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.button("Sắp ra mắt", disabled=True, use_container_width=True, key="btn_future")

# --- SKILLS ---
st.markdown("""
<div class="section-header">
    <h2>⚡ Kỹ năng & Công cụ</h2>
</div>
""", unsafe_allow_html=True)

skills = [
    "Python", "Streamlit", "NVIDIA NIM", "OpenAI API", 
    "Google Gemini", "Pandas & NumPy", "Plotly & Matplotlib", 
    "Technical Analysis", "SQL", "LangChain"
]

badges_html = "".join([f'<span class="badge">{s}</span>' for s in skills])
st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:0.3rem;">{badges_html}</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    © 2024 FLC mất điện — Thiết kế với Streamlit & ❤️
</div>
""", unsafe_allow_html=True)
