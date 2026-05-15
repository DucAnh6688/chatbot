# FLC mất điện - Portfolio & Stock Assistant

A professional multi-page Streamlit application showcasing an AI-powered financial assistant integrated with NVIDIA NIM, Google AI Studio (Gemini), and real-time Vietnamese stock market data.

## 🚀 Features

### 1. Portfolio (Home)
- Modern glassmorphism UI.
- Professional bio and skill set highlights.
- Seamless navigation to sub-projects.

### 2. AI Stock Assistant
- **Real-time Data:** Fetches OHLCV data for the Vietnamese stock market using `vnstock`.
- **Technical Charts:** Interactive Plotly candlestick charts with SMA 20, SMA 50, and RSI (14).
- **AI Analysis:** Automated technical interpretation using **NVIDIA NIM (Llama 3.1)**, **Google AI Studio (Gemini)**, or **OpenAI**.
- **Financial Chatbot:** Context-aware assistant for market inquiries.
- **Data Export:** Download analyzed stock data in CSV format.

## 🛠️ Tech Stack
- **Frontend:** Streamlit, CSS (Custom Glassmorphism).
- **LLM Integration:** NVIDIA NIM, Google AI Studio (Gemini), OpenAI API.
- **Data & Visualization:** vnstock, Pandas, Plotly.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/grafity-ai.git
   cd grafity-ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## 🔑 Configuration
You will need at least one of the following API Keys to use the AI features:
- **NVIDIA API Key** (from [build.nvidia.com](https://build.nvidia.com))
- **Google AI Studio API Key** (from [aistudio.google.com](https://aistudio.google.com))
- **OpenAI API Key** (from [platform.openai.com](https://platform.openai.com))

---
© 2024 FLC mất điện
