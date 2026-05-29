import streamlit as st
import pandas as pd
from core.database import get_aggregate_stats, get_all_sessions, get_session_results
from core.models import LABEL_MAP, EMOJI_MAP
from utils.charts import (
    create_pie_chart, create_bar_chart, create_confidence_histogram,
    create_session_comparison
)

st.set_page_config(page_title="Dashboard — Phân tích Cảm xúc", page_icon="📊", layout="wide")

# ==================== CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }

    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.8rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
    }
    .dashboard-header h2 {
        color: white; margin: 0; font-weight: 700;
    }
    .dashboard-header p {
        color: rgba(255,255,255,0.8); margin: 0.3rem 0 0 0; font-size: 0.95rem;
    }

    .metric-card {
        background: linear-gradient(145deg, #1e1e2e, #252540);
        border: 1px solid rgba(139, 92, 246, 0.15);
        border-radius: 12px;
        padding: 1.3rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 0.2rem;
    }
    .positive { color: #22c55e; }
    .neutral { color: #f59e0b; }
    .negative { color: #ef4444; }
    .purple { background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="dashboard-header">
    <h2>📊 Dashboard Tổng quan</h2>
    <p>Thống kê từ tất cả phiên phân tích đã lưu</p>
</div>
""", unsafe_allow_html=True)

# ==================== LOAD DATA ====================
stats = get_aggregate_stats()
sessions = get_all_sessions()

if stats['total_comments'] == 0:
    st.info("📭 Chưa có dữ liệu phân tích nào. Hãy thử **💬 Phân Tích**, **📁 Upload File** hoặc **🛒 Shopee** để bắt đầu!")
    st.stop()

# ==================== METRICS ====================
total = stats['total_comments']
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value purple">{stats['total_sessions']}</div>
        <div class="metric-label">Phiên phân tích</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value positive">{stats['total_positive']}</div>
        <div class="metric-label">✅ Tích cực ({stats['total_positive']/total:.0%})</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value neutral">{stats['total_neutral']}</div>
        <div class="metric-label">😐 Trung tính ({stats['total_neutral']/total:.0%})</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value negative">{stats['total_negative']}</div>
        <div class="metric-label">❌ Tiêu cực ({stats['total_negative']/total:.0%})</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== BIỂU ĐỒ ====================
col_left, col_right = st.columns(2)

with col_left:
    fig_pie = create_pie_chart(
        stats['total_positive'], stats['total_neutral'], stats['total_negative'],
        title="Tỷ lệ Cảm xúc Tổng hợp"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    # Tập hợp tất cả kết quả để vẽ biểu đồ cột
    all_results = []
    for session in sessions:
        results = get_session_results(session['id'])
        for r in results:
            all_results.append({
                'text': r['comment_text'],
                'pred': r['predicted_label'],
                'label': r['label_name'],
                'confidence': r['confidence'],
                'probs': [0, 0, 0]
            })

    fig_bar = create_bar_chart(all_results, title="Phân bố Cảm xúc Tổng hợp")
    st.plotly_chart(fig_bar, use_container_width=True)

# ==================== HISTOGRAM ĐỘ TIN CẬY ====================
if all_results:
    fig_hist = create_confidence_histogram(all_results, title="Phân bố Độ tin cậy")
    st.plotly_chart(fig_hist, use_container_width=True)

# ==================== SO SÁNH PHIÊN ====================
if len(sessions) > 1:
    st.markdown("### 📈 So sánh giữa các phiên")
    recent = sessions[:10]  # 10 phiên gần nhất
    fig_comp = create_session_comparison(recent, title="So sánh 10 phiên gần nhất")
    st.plotly_chart(fig_comp, use_container_width=True)

# ==================== BẢNG PHIÊN ====================
st.markdown("### 📋 Danh sách phiên phân tích")
sessions_df = pd.DataFrame([{
    'Tên': s['name'],
    'Nguồn': s['source'],
    'Model': s['model_used'],
    'Tổng': s['total_comments'],
    '✅': s['positive_count'],
    '😐': s['neutral_count'],
    '❌': s['negative_count'],
    'Thời gian': s['created_at']
} for s in sessions])

st.dataframe(sessions_df, use_container_width=True, hide_index=True)
