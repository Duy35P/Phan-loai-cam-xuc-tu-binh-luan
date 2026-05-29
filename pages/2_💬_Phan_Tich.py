import streamlit as st
from core.models import (
    load_phobert, load_baseline,
    predict_phobert, predict_baseline,
    LABEL_MAP, EMOJI_MAP, COLOR_MAP
)
from core.database import save_session
from utils.charts import create_prob_bar_chart

st.set_page_config(page_title="Phân tích Cảm xúc", page_icon="💬", layout="centered")

# ==================== CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }

    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
    }
    .page-header h2 { color: white; margin: 0; font-weight: 700; }
    .page-header p { color: rgba(255,255,255,0.8); margin: 0.3rem 0 0 0; font-size: 0.9rem; }

    .result-card {
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    .result-positive {
        background: linear-gradient(145deg, rgba(34,197,94,0.15), rgba(34,197,94,0.05));
        border: 1px solid rgba(34,197,94,0.3);
    }
    .result-negative {
        background: linear-gradient(145deg, rgba(239,68,68,0.15), rgba(239,68,68,0.05));
        border: 1px solid rgba(239,68,68,0.3);
    }
    .result-neutral {
        background: linear-gradient(145deg, rgba(245,158,11,0.15), rgba(245,158,11,0.05));
        border: 1px solid rgba(245,158,11,0.3);
    }
    .result-emoji { font-size: 3rem; }
    .result-label { font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0; }
    .result-conf { font-size: 1rem; color: #94a3b8; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="page-header">
    <h2>💬 Phân tích Cảm xúc</h2>
    <p>Nhập bình luận để nhận kết quả phân tích tức thì</p>
</div>
""", unsafe_allow_html=True)

# ==================== CHỌN MODEL ====================
model_choice = st.radio(
    "🤖 Chọn mô hình:",
    ["PhoBERT (Chính xác hơn)", "Naive Bayes (Nhanh hơn)"],
    horizontal=True
)

# ==================== NHẬP BÌNH LUẬN ====================
user_input = st.text_area(
    "📝 Nhập bình luận khách hàng:",
    height=120,
    placeholder="Ví dụ: Sản phẩm đẹp, giao hàng nhanh, đóng gói cẩn thận..."
)

col1, col2 = st.columns([1, 3])
with col1:
    analyze_btn = st.button("🔍 Phân tích", type="primary", use_container_width=True)

# ==================== KẾT QUẢ ====================
if analyze_btn and user_input.strip():
    with st.spinner("🔄 Đang phân tích..."):
        if "PhoBERT" in model_choice:
            tokenizer, model = load_phobert()
            pred, probs = predict_phobert(user_input, tokenizer, model)
        else:
            model = load_baseline()
            pred, probs = predict_baseline(user_input, model)

    st.divider()

    # Kết quả chính
    emoji = EMOJI_MAP[pred]
    label = LABEL_MAP[pred]
    conf = max(probs)
    color = COLOR_MAP[pred]

    css_class = {0: 'result-negative', 1: 'result-neutral', 2: 'result-positive'}[pred]
    st.markdown(f"""
    <div class="result-card {css_class}">
        <div class="result-emoji">{emoji}</div>
        <div class="result-label" style="color: {color};">{label}</div>
        <div class="result-conf">Độ tin cậy: {conf:.1%}</div>
    </div>
    """, unsafe_allow_html=True)

    # Biểu đồ xác suất
    fig = create_prob_bar_chart(probs)
    st.plotly_chart(fig, use_container_width=True)

    # Giải thích
    with st.expander("💡 Giải thích kết quả", expanded=False):
        st.markdown(f"""
        **Bình luận:** "{user_input}"

        **Phân tích chi tiết:**
        - ❌ Tiêu cực: **{probs[0]:.1%}**
        - 😐 Trung tính: **{probs[1]:.1%}**
        - ✅ Tích cực: **{probs[2]:.1%}**

        **Kết luận:** Mô hình dự đoán bình luận này mang cảm xúc **{label}** với độ tin cậy **{conf:.1%}**.
        """)

    # Nút lưu
    st.divider()
    if st.button("💾 Lưu kết quả vào lịch sử", use_container_width=True):
        model_name = "PhoBERT" if "PhoBERT" in model_choice else "Naive Bayes"
        result = [{
            'text': user_input,
            'pred': pred,
            'label': label,
            'emoji': emoji,
            'probs': probs,
            'confidence': conf
        }]
        save_session(
            name=f"Phân tích đơn: {user_input[:50]}...",
            source="manual",
            model_used=model_name,
            results=result
        )
        st.success("✅ Đã lưu vào lịch sử!")

elif analyze_btn:
    st.warning("⚠️ Vui lòng nhập bình luận!")
