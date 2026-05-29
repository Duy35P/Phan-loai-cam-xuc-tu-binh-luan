import streamlit as st
import pandas as pd
from core.models import predict_batch, LABEL_MAP, EMOJI_MAP
from core.database import save_session
from utils.charts import create_pie_chart, create_bar_chart
from utils.export import export_to_csv, export_to_excel, results_to_dataframe

st.set_page_config(page_title="Upload File", page_icon="📁", layout="wide")

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
    .summary-card {
        background: linear-gradient(145deg, #1e1e2e, #252540);
        border: 1px solid rgba(139,92,246,0.15); border-radius: 12px;
        padding: 1.3rem; text-align: center;
    }
    .summary-value { font-size: 1.8rem; font-weight: 700; }
    .summary-label { color: #94a3b8; font-size: 0.85rem; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h2>📁 Upload File & Phân tích Hàng loạt</h2>
    <p>Upload CSV/Excel chứa bình luận → phân tích cảm xúc hàng loạt</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Chọn file CSV hoặc Excel", type=['csv', 'xlsx', 'xls'])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success(f"✅ Đã đọc file: **{uploaded_file.name}** — {len(df)} dòng, {len(df.columns)} cột")
        with st.expander("👀 Xem trước dữ liệu", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)
        text_col = st.selectbox("📌 Chọn cột chứa bình luận:", df.columns.tolist())
        model_choice = st.radio("🤖 Chọn mô hình:", ["PhoBERT (Chính xác hơn)", "Naive Bayes (Nhanh hơn)"], horizontal=True)
        if st.button("🚀 Phân tích hàng loạt", type="primary", use_container_width=True):
            texts = df[text_col].dropna().astype(str).tolist()
            if not texts:
                st.error("❌ Cột được chọn không có dữ liệu!")
                st.stop()
            model_name = "PhoBERT" if "PhoBERT" in model_choice else "Naive Bayes"
            progress = st.progress(0, text="Đang phân tích...")
            results = []
            batch_size = 10
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                batch_results = predict_batch(batch, model_name)
                results.extend(batch_results)
                progress.progress(min(len(results)/len(texts), 1.0), text=f"Đã phân tích {len(results)}/{len(texts)}")
            progress.empty()
            st.success(f"✅ Hoàn thành! Đã phân tích **{len(results)}** bình luận.")
            st.session_state['upload_results'] = results
            st.session_state['upload_filename'] = uploaded_file.name
            st.session_state['upload_model'] = model_name
    except Exception as e:
        st.error(f"❌ Lỗi đọc file: {str(e)}")

if 'upload_results' in st.session_state:
    results = st.session_state['upload_results']
    filename = st.session_state.get('upload_filename', 'File')
    model_name = st.session_state.get('upload_model', 'Unknown')
    st.divider()
    st.markdown("### 📊 Kết quả phân tích")
    total = len(results)
    pos = sum(1 for r in results if r['pred'] == 2)
    neu = sum(1 for r in results if r['pred'] == 1)
    neg = sum(1 for r in results if r['pred'] == 0)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="summary-card"><div class="summary-value" style="color:#8b5cf6">{total}</div><div class="summary-label">Tổng</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="summary-card"><div class="summary-value" style="color:#22c55e">{pos}</div><div class="summary-label">✅ Tích cực</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="summary-card"><div class="summary-value" style="color:#f59e0b">{neu}</div><div class="summary-label">😐 Trung tính</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="summary-card"><div class="summary-value" style="color:#ef4444">{neg}</div><div class="summary-label">❌ Tiêu cực</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        st.plotly_chart(create_pie_chart(pos, neu, neg), use_container_width=True)
    with col_r:
        st.plotly_chart(create_bar_chart(results), use_container_width=True)
    st.markdown("### 📋 Chi tiết kết quả")
    filter_label = st.selectbox("🔍 Lọc:", ["Tất cả", "TÍCH CỰC", "TRUNG TÍNH", "TIÊU CỰC"])
    display = results if filter_label == "Tất cả" else [r for r in results if r['label'] == filter_label]
    st.dataframe(results_to_dataframe(display), use_container_width=True, hide_index=True)
    st.divider()
    c_csv, c_xl, c_save = st.columns(3)
    with c_csv:
        st.download_button("📥 Tải CSV", export_to_csv(results), f"sentiment_{filename}.csv", "text/csv", use_container_width=True)
    with c_xl:
        st.download_button("📥 Tải Excel", export_to_excel(results), f"sentiment_{filename}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with c_save:
        if st.button("💾 Lưu vào lịch sử", use_container_width=True):
            sid = save_session(filename, "upload", model_name, results)
            st.success(f"✅ Đã lưu phiên #{sid}!")
