import streamlit as st

# --- PAGE CONFIGURATION (MUST be the very first Streamlit command) ---
st.set_page_config(
    page_title="FLC mất điện - Stock Chatbot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- All other imports AFTER set_page_config ---
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os

# Safe import for vnstock (may fail on some cloud environments)
try:
    from vnstock import Quote
    VNSTOCK_AVAILABLE = True
except Exception:
    VNSTOCK_AVAILABLE = False

# Safe import for openai
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

# Safe import for dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def get_secret(key, default=""):
    """Get secret from Streamlit Cloud secrets or .env fallback."""
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError, AttributeError):
        return os.getenv(key, default)

# --- LOAD CUSTOM CSS ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# --- SIDEBAR: CONFIGURATION ---
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1rem;">
        <span style="font-size: 2.2rem;">🚀</span>
        <h3 style="margin:0.3rem 0 0; font-size:1.2rem;">FLC mất điện</h3>
        <p style="font-size:0.75rem; color:var(--text-muted); margin:0;">Stock Assistant v2.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- LLM Provider ---
    st.markdown("##### 🤖 Cấu hình AI")
    api_provider = st.selectbox("Nhà cung cấp", ["Google AI Studio", "OpenAI", "NVIDIA NIM", "Local NIM"], label_visibility="collapsed")
    
    if api_provider == "OpenAI":
        api_key = st.text_input("OpenAI API Key", type="password", help="Nhập mã OpenAI API key của bạn.")
        base_url = None
        model_name = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
    elif api_provider == "NVIDIA NIM":
        api_key = st.text_input("NVIDIA API Key", type="password", help="Nhập mã NVIDIA API key từ build.nvidia.com")
        base_url = "https://integrate.api.nvidia.com/v1"
        model_name = st.selectbox("Model NVIDIA", [
            "meta/llama-3.1-405b-instruct",
            "meta/llama-3.1-70b-instruct",
            "nvidia/llama-3.1-nemotron-70b-instruct",
        ])
    elif api_provider == "Google AI Studio":
        default_gemini_key = get_secret("GOOGLE_API_KEY", "")
        api_key = st.text_input("Gemini API Key", value=default_gemini_key, type="password", help="Nhập mã API key từ aistudio.google.com")
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
        model_name = st.selectbox("Model Gemini", ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.5-pro"])
    else:  # Local NIM
        api_key = st.text_input("API Key (nếu có)", value="not-used", type="password")
        base_url = st.text_input("NIM URL", value="http://localhost:8000/v1")
        model_name = st.text_input("Model Name", value="meta/llama-3.1-8b-instruct")

    st.markdown("---")
    
    # --- Market Data ---
    st.markdown("##### 📊 Dữ liệu thị trường")
    ticker = st.text_input("Mã chứng khoán", value="FPT", help="VD: VCB, FPT, VNM, HPG").upper()
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = st.date_input("Khoảng thời gian", [start_date, end_date])
    
    if len(date_range) != 2:
        st.warning("⚠️ Chọn đầy đủ ngày bắt đầu và kết thúc.")

    show_indicators = st.checkbox("Hiển thị chỉ báo kỹ thuật", value=True)

    st.markdown("---")
    
    # Provider info
    provider_urls = {
        "OpenAI": "platform.openai.com",
        "NVIDIA NIM": "build.nvidia.com",
        "Google AI Studio": "aistudio.google.com",
        "Local NIM": "localhost"
    }
    st.caption(f"🔑 Provider: **{api_provider}** • [Lấy key →](https://{provider_urls[api_provider]})")

# --- MAIN INTERFACE ---
st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <h1 style="margin-bottom: 0.2rem;">📈 Stock Assistant</h1>
    <p style="color: var(--text-muted); font-size: 0.9rem;">Phân tích kỹ thuật chứng khoán Việt Nam với AI</p>
</div>
""", unsafe_allow_html=True)

# --- Check vnstock availability ---
if not VNSTOCK_AVAILABLE:
    st.error("⚠️ Thư viện `vnstock` chưa được cài đặt hoặc gặp lỗi khi khởi tạo. Vui lòng kiểm tra lại requirements.txt")

# --- FETCH DATA ---
data_container = st.container()

with data_container:
    if st.button("🔍  Phân tích  " + ticker, use_container_width=True, type="primary"):
        if not VNSTOCK_AVAILABLE:
            st.error("Không thể phân tích vì thư viện vnstock không khả dụng.")
        elif len(date_range) != 2:
            st.error("Vui lòng chọn đầy đủ ngày bắt đầu và kết thúc trước khi lấy dữ liệu.")
        else:
            try:
                with st.spinner(f"Đang tải dữ liệu {ticker}..."):
                    quote = Quote(symbol=ticker)
                    df = quote.history(
                        start=date_range[0].strftime('%Y-%m-%d'),
                        end=date_range[1].strftime('%Y-%m-%d'),
                        interval='1D'
                    )

                if df is not None and not df.empty:
                    # --- Calculate Indicators ---
                    df['SMA20'] = df['close'].rolling(window=20).mean()
                    df['SMA50'] = df['close'].rolling(window=50).mean()

                    # RSI
                    delta_price = df['close'].diff()
                    gain = (delta_price.where(delta_price > 0, 0)).rolling(window=14).mean()
                    loss = (-delta_price.where(delta_price < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    df['RSI'] = 100 - (100 / (1 + rs))

                    # MACD
                    exp1 = df['close'].ewm(span=12, adjust=False).mean()
                    exp2 = df['close'].ewm(span=26, adjust=False).mean()
                    df['MACD'] = exp1 - exp2
                    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
                    df['Hist'] = df['MACD'] - df['Signal']

                    last = df.iloc[-1]
                    prev = df.iloc[-2] if len(df) > 1 else last
                    price_change = last['close'] - prev['close']
                    pct_change = (price_change / prev['close'] * 100) if prev['close'] != 0 else 0

                    # --- Summary Metrics ---
                    rsi_val = last['RSI']
                    rsi_display = f"{rsi_val:.1f}" if pd.notna(rsi_val) else "—"
                    rsi_class = "metric-down" if pd.notna(rsi_val) and rsi_val > 70 else ("metric-up" if pd.notna(rsi_val) and rsi_val < 30 else "")
                    rsi_status = "Quá mua" if pd.notna(rsi_val) and rsi_val > 70 else ("Quá bán" if pd.notna(rsi_val) and rsi_val < 30 else "Trung tính")
                    
                    sma20_display = f"{last['SMA20']:,.1f}" if pd.notna(last['SMA20']) else "—"
                    sma20_delta_class = "metric-up" if pd.notna(last['SMA20']) and last['close'] > last['SMA20'] else ("metric-down" if pd.notna(last['SMA20']) else "metric-neutral")
                    sma20_status = "Trên SMA" if pd.notna(last['SMA20']) and last['close'] > last['SMA20'] else ("Dưới SMA" if pd.notna(last['SMA20']) else "Chưa đủ dữ liệu")
                    
                    price_delta_class = "metric-up" if price_change >= 0 else "metric-down"
                    macd_delta_class = "metric-up" if last['MACD'] > last['Signal'] else "metric-down"
                    macd_status = "Tăng ↑" if last['MACD'] > last['Signal'] else "Giảm ↓"

                    st.markdown(f"""
                    <div class="metric-row">
                        <div class="metric-card">
                            <div class="metric-label">Giá hiện tại</div>
                            <div class="metric-value">{last['close']:,.1f}</div>
                            <div class="metric-delta {price_delta_class}">{price_change:+,.1f} ({pct_change:+.2f}%)</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">RSI (14)</div>
                            <div class="metric-value {rsi_class}">{rsi_display}</div>
                            <div class="metric-delta metric-neutral">{rsi_status}</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">SMA 20</div>
                            <div class="metric-value">{sma20_display}</div>
                            <div class="metric-delta {sma20_delta_class}">{sma20_status}</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">MACD</div>
                            <div class="metric-value">{last['MACD']:.2f}</div>
                            <div class="metric-delta {macd_delta_class}">{macd_status}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # --- Chart ---
                    # Detect the date/time column name
                    time_col = 'time' if 'time' in df.columns else ('date' if 'date' in df.columns else df.columns[0])
                    
                    if show_indicators:
                        fig = make_subplots(
                            rows=3, cols=1, shared_xaxes=True,
                            vertical_spacing=0.04,
                            row_heights=[0.55, 0.22, 0.23],
                            subplot_titles=(f"{ticker} — Biểu đồ nến", "RSI (14)", "MACD")
                        )
                    else:
                        fig = go.Figure()

                    candlestick = go.Candlestick(
                        x=df[time_col], open=df['open'], high=df['high'],
                        low=df['low'], close=df['close'], name="Giá",
                        increasing_line_color='#34d399', decreasing_line_color='#f87171',
                        increasing_fillcolor='#34d399', decreasing_fillcolor='#f87171',
                    )

                    if show_indicators:
                        fig.add_trace(candlestick, row=1, col=1)
                        fig.add_trace(go.Scatter(x=df[time_col], y=df['SMA20'], name='SMA 20', line=dict(color='#38bdf8', width=1.2)), row=1, col=1)
                        fig.add_trace(go.Scatter(x=df[time_col], y=df['SMA50'], name='SMA 50', line=dict(color='#a78bfa', width=1.2)), row=1, col=1)

                        # Volume as bar chart on main
                        fig.add_trace(go.Bar(x=df[time_col], y=df['volume'], name='Volume', marker_color='rgba(56,189,248,0.15)', yaxis='y'), row=1, col=1)

                        # RSI
                        fig.add_trace(go.Scatter(x=df[time_col], y=df['RSI'], name='RSI', line=dict(color='#818cf8', width=1.5)), row=2, col=1)
                        fig.add_hline(y=70, line_dash="dash", line_color="rgba(248,113,113,0.5)", line_width=1, row=2, col=1)
                        fig.add_hline(y=30, line_dash="dash", line_color="rgba(52,211,153,0.5)", line_width=1, row=2, col=1)
                        fig.add_hrect(y0=30, y1=70, fillcolor="rgba(129,140,248,0.04)", line_width=0, row=2, col=1)

                        # MACD
                        colors = ['#34d399' if v >= 0 else '#f87171' for v in df['Hist']]
                        fig.add_trace(go.Bar(x=df[time_col], y=df['Hist'], name='Histogram', marker_color=colors), row=3, col=1)
                        fig.add_trace(go.Scatter(x=df[time_col], y=df['MACD'], name='MACD', line=dict(color='#38bdf8', width=1.2)), row=3, col=1)
                        fig.add_trace(go.Scatter(x=df[time_col], y=df['Signal'], name='Signal', line=dict(color='#fbbf24', width=1.2)), row=3, col=1)
                    else:
                        fig.add_trace(candlestick)

                    fig.update_layout(
                        template="plotly_dark",
                        height=750,
                        margin=dict(l=0, r=10, t=40, b=0),
                        xaxis_rangeslider_visible=False,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(12,14,20,0.8)',
                        font=dict(family="Inter, sans-serif", size=11, color="#94a3b8"),
                        legend=dict(
                            orientation="h", yanchor="bottom", y=1.02,
                            xanchor="right", x=1, bgcolor="rgba(0,0,0,0)",
                            font=dict(size=10)
                        ),
                        hoverlabel=dict(bgcolor="#1e293b", font_size=12, font_family="Inter"),
                    )
                    # Grid styling
                    fig.update_xaxes(gridcolor='rgba(255,255,255,0.04)', showgrid=True)
                    fig.update_yaxes(gridcolor='rgba(255,255,255,0.04)', showgrid=True)

                    st.plotly_chart(fig, use_container_width=True)

                    # --- AI Analysis ---
                    st.markdown("### 🤖 Nhận định từ AI")
                    if not api_key:
                        st.warning("Vui lòng nhập API Key ở thanh bên để nhận phân tích từ AI.")
                    elif not OPENAI_AVAILABLE:
                        st.warning("Thư viện OpenAI chưa được cài đặt.")
                    else:
                        macd_analysis = (
                            "Cắt lên (Tăng)" if last['MACD'] > last['Signal'] and prev['MACD'] <= prev['Signal']
                            else "Cắt xuống (Giảm)" if last['MACD'] < last['Signal'] and prev['MACD'] >= prev['Signal']
                            else "Duy trì xu hướng"
                        )

                        sma20_text = f"{last['SMA20']:.2f}" if pd.notna(last['SMA20']) else "Chưa đủ dữ liệu (cần ≥20 phiên)"
                        sma50_text = f"{last['SMA50']:.2f}" if pd.notna(last['SMA50']) else "Chưa đủ dữ liệu (cần ≥50 phiên)"
                        rsi_text = f"{last['RSI']:.2f}" if pd.notna(last['RSI']) else "Chưa đủ dữ liệu"

                        prompt_analysis = f"""
Phân tích kỹ thuật cho mã {ticker}:
- Giá hiện tại: {last['close']:.2f} VND (Thay đổi: {price_change:+.2f} VND, {pct_change:+.2f}%)
- SMA 20: {sma20_text}
- SMA 50: {sma50_text}
- RSI (14): {rsi_text}
- MACD: {last['MACD']:.2f}, Signal: {last['Signal']:.2f}
- Trạng thái MACD: {macd_analysis}

Dựa trên các chỉ số này, hãy đưa ra nhận định ngắn gọn về xu hướng và gợi ý (Mua/Bán/Theo dõi). Trả lời chuyên nghiệp bằng tiếng Việt.
"""
                        with st.spinner("AI đang phân tích..."):
                            try:
                                client = OpenAI(api_key=api_key, base_url=base_url)
                                response = client.chat.completions.create(
                                    model=model_name,
                                    messages=[
                                        {"role": "system", "content": "Bạn là một chuyên gia phân tích kỹ thuật chứng khoán Việt Nam. Trả lời ngắn gọn, rõ ràng, có cấu trúc."},
                                        {"role": "user", "content": prompt_analysis}
                                    ]
                                )
                                st.markdown(f"""
<div class="glass-card">
{response.choices[0].message.content}
</div>
""", unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Lỗi AI: {e}")

                    # --- Data Table ---
                    with st.expander("📋 Xem dữ liệu chi tiết"):
                        st.dataframe(
                            df.tail(15).style.format({
                                'open': '{:.1f}', 'high': '{:.1f}',
                                'low': '{:.1f}', 'close': '{:.1f}',
                                'volume': '{:,.0f}'
                            }),
                            use_container_width=True
                        )
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Tải dữ liệu CSV",
                            data=csv,
                            file_name=f"{ticker}_data.csv",
                            mime="text/csv",
                        )
                else:
                    st.warning("Không tìm thấy dữ liệu cho mã này.")
            except Exception as e:
                st.error(f"Lỗi: {e}")

# --- CHAT SECTION ---
st.markdown("---")
st.markdown("### 💬 Chat với FLC mất điện")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hỏi thêm về cổ phiếu..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        st.warning("Vui lòng nhập API Key để tiếp tục.")
    elif not OPENAI_AVAILABLE:
        st.warning("Thư viện OpenAI chưa được cài đặt.")
    else:
        try:
            client = OpenAI(api_key=api_key, base_url=base_url)
            context = f"Người dùng đang xem mã {ticker}."
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for response in client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "Bạn là trợ lý tài chính chứng khoán Việt Nam. Trả lời ngắn gọn, chính xác."},
                        {"role": "system", "content": context},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    stream=True,
                ):
                    chunk_delta = response.choices[0].delta.content if hasattr(response.choices[0].delta, 'content') else ""
                    full_response += (chunk_delta or "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Lỗi: {e}")

# --- FOOTER ---
st.markdown("""
<div class="footer">
    © 2024 FLC mất điện — Powered by Gemini, NVIDIA NIM, OpenAI & vnstock
</div>
""", unsafe_allow_html=True)
