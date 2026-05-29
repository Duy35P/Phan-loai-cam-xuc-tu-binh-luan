import streamlit as st

# ==================== CẤU HÌNH ====================
st.set_page_config(
    page_title="Phân tích Cảm xúc Bình luận",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* Gradient header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .main-header p {
        color: rgba(255,255,255,0.85);
        font-size: 1.05rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    /* Feature cards */
    .feature-card {
        background: linear-gradient(145deg, #1e1e2e, #2a2a3e);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 14px;
        padding: 1.8rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .feature-card:hover {
        border-color: rgba(139, 92, 246, 0.5);
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.15);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
    }
    .feature-title {
        color: #e2e8f0;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* Stats */
    .stat-card {
        background: linear-gradient(145deg, #1e1e2e, #252540);
        border: 1px solid rgba(139, 92, 246, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }

    /* Model info table */
    .model-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
    }
    .model-table th {
        background: rgba(139, 92, 246, 0.2);
        color: #e2e8f0;
        padding: 0.8rem 1rem;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid rgba(139, 92, 246, 0.3);
    }
    .model-table td {
        padding: 0.7rem 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: #cbd5e1;
    }
    .model-table tr:hover td {
        background: rgba(139, 92, 246, 0.05);
    }

    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Animate */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="main-header animate-in">
    <h1>🛍️ Hệ thống Phân tích Cảm xúc Bình luận</h1>
    <p>Công cụ AI phân tích cảm xúc khách hàng từ bình luận thương mại điện tử</p>
</div>
""", unsafe_allow_html=True)

# ==================== THỐNG KÊ NHANH ====================
from core.database import get_aggregate_stats

stats = get_aggregate_stats()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="stat-card animate-in">
        <div class="stat-number">{stats['total_sessions']}</div>
        <div class="stat-label">Phiên phân tích</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-card animate-in">
        <div class="stat-number">{stats['total_comments']:,}</div>
        <div class="stat-label">Bình luận đã phân tích</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    total = stats['total_comments']
    pos_rate = f"{stats['total_positive']/total:.0%}" if total > 0 else "—"
    st.markdown(f"""
    <div class="stat-card animate-in">
        <div class="stat-number">{pos_rate}</div>
        <div class="stat-label">Tỷ lệ tích cực</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    neg_rate = f"{stats['total_negative']/total:.0%}" if total > 0 else "—"
    st.markdown(f"""
    <div class="stat-card animate-in">
        <div class="stat-number">{neg_rate}</div>
        <div class="stat-label">Tỷ lệ tiêu cực</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== TÍNH NĂNG ====================
st.markdown("### 🚀 Tính năng chính")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card animate-in">
        <div class="feature-icon">💬</div>
        <div class="feature-title">Phân tích Đơn lẻ</div>
        <div class="feature-desc">Nhập bình luận và nhận kết quả phân tích cảm xúc ngay lập tức với độ tin cậy chi tiết.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card animate-in">
        <div class="feature-icon">🛒</div>
        <div class="feature-title">Crawl Shopee</div>
        <div class="feature-desc">Tự động thu thập và phân tích bình luận từ link sản phẩm Shopee.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card animate-in">
        <div class="feature-icon">📁</div>
        <div class="feature-title">Upload File</div>
        <div class="feature-desc">Upload file CSV/Excel chứa bình luận để phân tích hàng loạt với biểu đồ trực quan.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card animate-in">
        <div class="feature-icon">📜</div>
        <div class="feature-title">Lịch sử</div>
        <div class="feature-desc">Lưu trữ và xem lại lịch sử phân tích. So sánh kết quả giữa các phiên.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card animate-in">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Dashboard</div>
        <div class="feature-desc">Biểu đồ tổng quan: pie chart, bar chart, word cloud — theo dõi xu hướng cảm xúc.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card animate-in">
        <div class="feature-icon">📥</div>
        <div class="feature-title">Xuất Báo cáo</div>
        <div class="feature-desc">Xuất kết quả ra CSV/Excel có format màu sắc theo cảm xúc.</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== THÔNG TIN MODEL ====================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🤖 Mô hình AI")

st.markdown("""
<table class="model-table">
    <tr>
        <th>Mô hình</th>
        <th>Accuracy</th>
        <th>Đặc điểm</th>
    </tr>
    <tr>
        <td>⚡ Naive Bayes</td>
        <td>76.12%</td>
        <td>Nhanh, nhẹ — phù hợp phân tích hàng loạt</td>
    </tr>
    <tr>
        <td>📊 Logistic Regression</td>
        <td>72.86%</td>
        <td>Ổn định, dễ giải thích</td>
    </tr>
    <tr>
        <td>🔧 SVM Linear</td>
        <td>75.16%</td>
        <td>Mạnh với dữ liệu text</td>
    </tr>
    <tr>
        <td>🏆 <strong>PhoBERT</strong></td>
        <td><strong>78.51%</strong></td>
        <td><strong>Chính xác nhất</strong> — Transformer cho tiếng Việt</td>
    </tr>
</table>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== HƯỚNG DẪN ====================
with st.expander("📖 Hướng dẫn sử dụng", expanded=False):
    st.markdown("""
    #### Bắt đầu nhanh

    1. **Phân tích đơn lẻ**: Chọn trang **💬 Phân Tích** ở sidebar → nhập bình luận → nhấn "Phân tích"
    2. **Phân tích file**: Chọn trang **📁 Upload File** → upload CSV/Excel → chọn cột bình luận → phân tích hàng loạt
    3. **Crawl Shopee**: Chọn trang **🛒 Shopee** → dán link sản phẩm → thu thập & phân tích tự động
    4. **Xem Dashboard**: Chọn trang **📊 Dashboard** để xem biểu đồ tổng quan từ lịch sử phân tích
    5. **Lịch sử**: Chọn trang **📜 Lịch Sử** để xem lại các phiên phân tích đã lưu

    #### Về Dataset
    - **Nguồn**: Vietnamese Sentiment Analyst (Kaggle — linhlpv)
    - **Kích thước**: 31,460 bình luận thương mại điện tử
    - **Nhãn**: Tích cực (POS) / Tiêu cực (NEG) / Trung tính (NEU)
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 0.85rem;'>"
    "Đồ án Khai thác Dữ liệu — Thương mại Điện tử Việt Nam &nbsp;|&nbsp; "
    "Powered by PhoBERT & Streamlit"
    "</div>",
    unsafe_allow_html=True
)