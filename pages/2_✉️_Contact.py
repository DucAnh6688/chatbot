import streamlit as st
import os

st.set_page_config(page_title="Liên hệ | FLC mất điện", page_icon="✉️", layout="wide")

def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# --- Header ---
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1.5rem;">
    <h1>✉️ Liên hệ</h1>
    <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto;">
        Bạn có câu hỏi hoặc muốn hợp tác? Hãy gửi tin nhắn!
    </p>
</div>
""", unsafe_allow_html=True)

# --- Form ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    with st.form("contact_form"):
        name = st.text_input("Tên của bạn")
        email = st.text_input("Email")
        subject = st.selectbox("Chủ đề", ["Hợp tác dự án", "Hỏi đáp kỹ thuật", "Phản hồi sản phẩm", "Khác"])
        message = st.text_area("Nội dung tin nhắn", height=150)
        submit = st.form_submit_button("Gửi tin nhắn →", use_container_width=True)
        
        if submit:
            if name and email and message:
                st.success(f"Cảm ơn **{name}**! Tin nhắn của bạn đã được ghi nhận. Đây là form demo — trong ứng dụng thực, email sẽ được gửi tự động.")
            else:
                st.warning("Vui lòng điền đầy đủ thông tin.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Contact Links ---
st.markdown("---")

st.markdown("""
<div class="section-header">
    <h2>🔗 Kết nối khác</h2>
</div>
""", unsafe_allow_html=True)

link_col1, link_col2, link_col3 = st.columns(3)

with link_col1:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:2rem; margin-bottom:0.5rem;">📧</div>
        <p style="font-weight:500; color:var(--text-primary);">Email</p>
        <a href="mailto:contact@grafity.ai">contact@grafity.ai</a>
    </div>
    """, unsafe_allow_html=True)

with link_col2:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🔗</div>
        <p style="font-weight:500; color:var(--text-primary);">LinkedIn</p>
        <a href="https://linkedin.com" target="_blank">linkedin.com/in/grafity</a>
    </div>
    """, unsafe_allow_html=True)

with link_col3:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:2rem; margin-bottom:0.5rem;">💻</div>
        <p style="font-weight:500; color:var(--text-primary);">GitHub</p>
        <a href="https://github.com" target="_blank">github.com/grafity</a>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="footer">
    © 2024 FLC mất điện — Thiết kế với Streamlit & ❤️
</div>
""", unsafe_allow_html=True)
