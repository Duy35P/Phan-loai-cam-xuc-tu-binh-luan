import streamlit as st
import pandas as pd
from core.database import get_all_sessions, get_session_results, get_session_by_id, delete_session
from core.models import LABEL_MAP, EMOJI_MAP
from utils.charts import create_pie_chart, create_session_comparison
from utils.export import export_to_csv, export_to_excel

st.set_page_config(page_title="Lịch sử — Phân tích Cảm xúc", page_icon="📜", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem; border-radius: 14px; margin-bottom: 1.5rem;
    }
    .page-header h2 { color: white; margin: 0; font-weight: 700; }
    .page-header p { color: rgba(255,255,255,0.8); margin: 0.3rem 0 0 0; font-size: 0.9rem; }
    .session-card {
        background: linear-gradient(145deg, #1e1e2e, #252540);
        border: 1px solid rgba(139,92,246,0.15); border-radius: 12px;
        padding: 1.2rem; margin-bottom: 0.8rem;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>📜 Lịch sử Phân tích</h2>
    <p>Xem lại, so sánh và quản lý các phiên phân tích đã lưu</p>
</div>
""", unsafe_allow_html=True)

sessions = get_all_sessions()

if not sessions:
    st.info("📭 Chưa có lịch sử phân tích nào. Hãy thực hiện phân tích và lưu kết quả trước!")
    st.stop()

# ==================== DANH SÁCH PHIÊN ====================
st.markdown(f"### 📋 Danh sách ({len(sessions)} phiên)")

sessions_df = pd.DataFrame([{
    'ID': s['id'],
    'Tên': s['name'][:50],
    'Nguồn': {'upload': '📁 Upload', 'shopee': '🛒 Shopee', 'manual': '💬 Thủ công'}.get(s['source'], s['source']),
    'Model': s['model_used'],
    'Tổng': s['total_comments'],
    '✅': s['positive_count'],
    '😐': s['neutral_count'],
    '❌': s['negative_count'],
    'Thời gian': s['created_at']
} for s in sessions])

st.dataframe(sessions_df, use_container_width=True, hide_index=True)

# ==================== XEM CHI TIẾT ====================
st.divider()
st.markdown("### 🔍 Xem chi tiết phiên")

session_ids = [s['id'] for s in sessions]
session_names = [f"#{s['id']} — {s['name'][:40]}" for s in sessions]
selected_idx = st.selectbox("Chọn phiên:", range(len(session_names)), format_func=lambda i: session_names[i])
selected_id = session_ids[selected_idx]

session = get_session_by_id(selected_id)
results_raw = get_session_results(selected_id)

if session and results_raw:
    # Summary
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Tổng bình luận", session['total_comments'])
    with c2:
        st.metric("✅ Tích cực", session['positive_count'])
    with c3:
        st.metric("😐 Trung tính", session['neutral_count'])
    with c4:
        st.metric("❌ Tiêu cực", session['negative_count'])

    # Chart
    st.plotly_chart(create_pie_chart(
        session['positive_count'], session['neutral_count'], session['negative_count'],
        title=f"Phiên #{selected_id}"
    ), use_container_width=True)

    # Detail table
    detail_df = pd.DataFrame([{
        'Bình luận': r['comment_text'],
        'Kết quả': r['label_name'],
        'Độ tin cậy': f"{r['confidence']:.1%}"
    } for r in results_raw])
    st.dataframe(detail_df, use_container_width=True, hide_index=True)

    # Export
    export_results = [{
        'text': r['comment_text'], 'pred': r['predicted_label'],
        'label': r['label_name'], 'emoji': EMOJI_MAP.get(r['predicted_label'], ''),
        'probs': [0, 0, 0], 'confidence': r['confidence']
    } for r in results_raw]

    c_csv, c_xl = st.columns(2)
    with c_csv:
        st.download_button("📥 CSV", export_to_csv(export_results), f"history_{selected_id}.csv", "text/csv", use_container_width=True)
    with c_xl:
        st.download_button("📥 Excel", export_to_excel(export_results), f"history_{selected_id}.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

# ==================== SO SÁNH ====================
if len(sessions) >= 2:
    st.divider()
    st.markdown("### 📈 So sánh phiên")
    compare_indices = st.multiselect(
        "Chọn phiên để so sánh:",
        range(len(session_names)), format_func=lambda i: session_names[i],
        default=[0, 1] if len(sessions) >= 2 else [0]
    )
    if len(compare_indices) >= 2:
        compare_sessions = [sessions[i] for i in compare_indices]
        fig = create_session_comparison(compare_sessions)
        st.plotly_chart(fig, use_container_width=True)

# ==================== XÓA ====================
st.divider()
st.markdown("### 🗑️ Xóa phiên")
del_idx = st.selectbox("Chọn phiên cần xóa:", range(len(session_names)), format_func=lambda i: session_names[i], key="del_select")
del_id = session_ids[del_idx]
if st.button("🗑️ Xóa phiên này", type="secondary"):
    delete_session(del_id)
    st.success(f"✅ Đã xóa phiên #{del_id}")
    st.rerun()
