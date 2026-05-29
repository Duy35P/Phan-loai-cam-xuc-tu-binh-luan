# MÔ TẢ CẤU TRÚC VÀ CHỨC NĂNG CHI TIẾT DỰ ÁN

## HỆ THỐNG PHÂN TÍCH CẢM XÚC BÌNH LUẬN THƯƠNG MẠI ĐIỆN TỬ

**Đồ án Khai thác Dữ liệu — Thương mại Điện tử Việt Nam**

---

## 1. TỔNG QUAN DỰ ÁN

### 1.1. Mục tiêu
Xây dựng hệ thống ứng dụng web phân tích cảm xúc (Sentiment Analysis) từ bình luận khách hàng trên các sàn thương mại điện tử Việt Nam. Hệ thống sử dụng mô hình AI (PhoBERT và Naive Bayes) để tự động phân loại bình luận thành 3 nhãn: **Tích cực (POS)**, **Trung tính (NEU)**, **Tiêu cực (NEG)**.

### 1.2. Công nghệ sử dụng
| Thành phần           | Công nghệ                                           |
|----------------------|------------------------------------------------------|
| Framework web        | Streamlit                                            |
| Ngôn ngữ             | Python 3.x                                           |
| Mô hình Deep Learning| PhoBERT (vinai/phobert-base, fine-tuned)             |
| Mô hình Baseline     | Naive Bayes (scikit-learn Pipeline)                  |
| Tokenizer tiếng Việt | PyVi (ViTokenizer)                                   |
| Transformer          | HuggingFace Transformers + PyTorch                   |
| Biểu đồ              | Plotly (plotly.express, plotly.graph_objects)         |
| Database             | SQLite3 (lưu lịch sử phân tích)                     |
| Xuất báo cáo         | Pandas, OpenPyXL (Excel có format màu)               |
| Giao diện            | Custom CSS (dark mode, gradient, animations)         |

### 1.3. Dataset
- **Nguồn**: Vietnamese Sentiment Analyst (Kaggle — linhlpv)
- **Kích thước**: 31,460 bình luận thương mại điện tử
- **Nhãn**: Tích cực (POS) / Tiêu cực (NEG) / Trung tính (NEU)

### 1.4. Kết quả mô hình

| Mô hình              | Accuracy   | Đặc điểm                                    |
|-----------------------|------------|----------------------------------------------|
| Naive Bayes           | 76.12%     | Nhanh, nhẹ — phù hợp phân tích hàng loạt    |
| Logistic Regression   | 72.86%     | Ổn định, dễ giải thích                       |
| SVM Linear            | 75.16%     | Mạnh với dữ liệu text                       |
| **PhoBERT (best)**    | **78.51%** | **Chính xác nhất** — Transformer cho tiếng Việt |

---

## 2. CẤU TRÚC THƯ MỤC DỰ ÁN

```
project/
├── .streamlit/
│   └── config.toml              # Cấu hình giao diện Streamlit (theme, server)
├── app.py                       # File chính — Trang Home của ứng dụng
├── core/                        # Module xử lý nghiệp vụ chính
│   ├── __init__.py              # Khai báo package core
│   ├── database.py              # Quản lý database SQLite (lịch sử phân tích)
│   ├── models.py                # Quản lý model AI và prediction
│   └── preprocessing.py         # Tiền xử lý văn bản tiếng Việt
├── data/
│   └── history.db               # Database SQLite lưu lịch sử phân tích
├── models/                      # Thư mục chứa model đã huấn luyện
│   ├── best_baseline.pkl        # Model Naive Bayes (scikit-learn Pipeline)
│   └── phobert_best/            # Model PhoBERT fine-tuned
│       ├── config.json           # Cấu hình mô hình
│       ├── model.safetensors     # Trọng số mô hình (~540MB)
│       ├── tokenizer_config.json # Cấu hình tokenizer
│       ├── vocab.txt             # Từ vựng
│       ├── bpe.codes             # BPE encoding
│       └── added_tokens.json     # Token bổ sung
├── pages/                       # Các trang con của Streamlit (multi-page app)
│   ├── 1_📊_Dashboard.py       # Trang Dashboard thống kê tổng quan
│   ├── 2_💬_Phan_Tich.py       # Trang phân tích cảm xúc đơn lẻ
│   ├── 3_📁_Upload_File.py     # Trang upload file và phân tích hàng loạt
│   └── 4_📜_Lich_Su.py         # Trang quản lý lịch sử phân tích
├── utils/                       # Module tiện ích
│   ├── __init__.py              # Khai báo package utils
│   ├── charts.py                # Hàm vẽ biểu đồ Plotly
│   └── export.py                # Hàm xuất báo cáo CSV/Excel
├── doankpdl.ipynb               # Jupyter Notebook huấn luyện mô hình
└── readme.txt                   # Hướng dẫn cài đặt và chạy project
```

---

## 3. MÔ TẢ CHI TIẾT TỪNG FILE

---

### 3.1. `.streamlit/config.toml` — Cấu hình Streamlit

**Chức năng**: Cấu hình theme và server cho ứng dụng Streamlit.

**Nội dung cấu hình**:
- **Theme**: Dark mode với bảng màu tím-xanh
  - `primaryColor`: `#8b5cf6` (tím)
  - `backgroundColor`: `#0e1117` (nền tối)
  - `secondaryBackgroundColor`: `#1e1e2e` (nền phụ)
  - `textColor`: `#e2e8f0` (chữ sáng)
  - `font`: sans serif
- **Server**: `headless = true` (chạy không cần browser tự mở)

---

### 3.2. `app.py` — Trang chủ (Home Page)

**Chức năng**: File entry point của ứng dụng Streamlit. Hiển thị trang chủ với tổng quan hệ thống.

**Chi tiết các thành phần**:

#### a) Cấu hình trang
- Tiêu đề: "Phân tích Cảm xúc Bình luận"
- Icon: 🛍️
- Layout: `wide` (toàn chiều rộng)
- Sidebar: mở rộng mặc định

#### b) Custom CSS
- Import Google Font **Inter** (wght 300–700)
- **Gradient header**: nền gradient tím (#667eea → #764ba2), bo tròn 16px, shadow
- **Feature cards**: nền dark gradient, viền tím mờ, hover effect (nâng lên 3px)
- **Stat cards**: hiển thị số liệu thống kê, chữ số gradient tím
- **Model table**: bảng thông tin model, header tím, hover effect
- **Animation**: fadeInUp keyframe animation
- Ẩn menu mặc định và footer của Streamlit

#### c) Header
- Tiêu đề lớn: "🛍️ Hệ thống Phân tích Cảm xúc Bình luận"
- Mô tả: "Công cụ AI phân tích cảm xúc khách hàng từ bình luận thương mại điện tử"

#### d) Thống kê nhanh (4 thẻ)
Gọi `get_aggregate_stats()` từ `core.database` để lấy dữ liệu:
1. **Phiên phân tích**: tổng số phiên đã lưu
2. **Bình luận đã phân tích**: tổng số bình luận
3. **Tỷ lệ tích cực**: phần trăm bình luận tích cực
4. **Tỷ lệ tiêu cực**: phần trăm bình luận tiêu cực

#### e) Tính năng chính (6 thẻ feature)
Hiển thị 6 tính năng của hệ thống trong grid 3 cột:
1. 💬 **Phân tích Đơn lẻ** — Nhập bình luận, nhận kết quả tức thì
2. 🛒 **Crawl Shopee** — Thu thập bình luận từ link sản phẩm Shopee
3. 📁 **Upload File** — Upload CSV/Excel phân tích hàng loạt
4. 📜 **Lịch sử** — Xem lại lịch sử, so sánh kết quả
5. 📊 **Dashboard** — Biểu đồ tổng quan
6. 📥 **Xuất Báo cáo** — Export CSV/Excel có format màu sắc

#### f) Bảng thông tin mô hình AI
Bảng HTML hiển thị 4 model với accuracy và đặc điểm.

#### g) Hướng dẫn sử dụng
Expander chứa hướng dẫn nhanh 5 bước và thông tin dataset.

#### h) Footer
Dòng chân trang: "Đồ án Khai thác Dữ liệu — Powered by PhoBERT & Streamlit"

---

### 3.3. `core/__init__.py` — Package Core

**Chức năng**: Khai báo package `core`, đánh dấu thư mục `core/` là Python package.

**Nội dung**: Comment mô tả "Core module - chứa logic xử lý chính".

---

### 3.4. `core/preprocessing.py` — Tiền xử lý văn bản

**Chức năng**: Tiền xử lý (preprocessing) văn bản tiếng Việt trước khi đưa vào model phân tích. Được sử dụng bởi model Naive Bayes (baseline).

**Các thành phần chi tiết**:

#### a) STOPWORDS (bộ từ dừng)
Bộ 28 từ dừng tiếng Việt phổ biến: `và, của, là, có, để, trong, với, này, đó, cho, được, một, các, khi, đã, thì, mà, hay, hoặc, nếu, vì, nhưng, tuy, dù, cũng, rất, lắm, quá, hơn, nhất, bị, làm, theo`.

#### b) TEENCODE_MAP (từ điển teencode)
Dictionary chuyển đổi 50+ teencode phổ biến sang tiếng Việt chuẩn:
- `ko/k/kh/khong` → `không`
- `dc/dk/đc` → `được`
- `sp` → `sản phẩm`
- `ship` → `giao hàng`
- `tks/thks/thanks` → `cảm ơn`
- `ok/oke/okie` → `tốt`
- `bth/bt` → `bình thường`
- ... và nhiều từ khác

#### c) EMOJI_SENTIMENT (từ điển emoji → cảm xúc)
Dictionary chuyển emoji thành từ mô tả cảm xúc:
- **Tích cực**: 😍→yêu_thích, ❤️→yêu_thích, 😊→vui, 👍→tốt, 💯→tuyệt_vời...
- **Tiêu cực**: 😡→tức_giận, 👎→tệ, 😢→buồn, 💔→thất_vọng, 🤮→ghê...

#### d) Hàm `replace_teencode(text)`
- **Input**: chuỗi text chứa teencode
- **Output**: chuỗi đã thay thế teencode bằng từ chuẩn
- **Cách hoạt động**: Tách từ → tra dictionary → ghép lại

#### e) Hàm `replace_emoji(text)`
- **Input**: chuỗi text chứa emoji
- **Output**: chuỗi đã thay emoji bằng từ mô tả cảm xúc
- **Cách hoạt động**: Duyệt từng emoji trong dictionary, thay thế trong text

#### f) Hàm `preprocess(text)` — Hàm chính
Pipeline tiền xử lý đầy đủ gồm 6 bước:
1. **Chuyển chữ thường** (`lower()`)
2. **Thay emoji** → từ cảm xúc (gọi `replace_emoji`)
3. **Thay teencode** → từ chuẩn (gọi `replace_teencode`)
4. **Loại bỏ URL** (regex: `http\S+|www\S+`)
5. **Loại bỏ ký tự đặc biệt và số** (regex: `[^\w\s]`, `\d+`)
6. **Tokenize tiếng Việt** bằng `ViTokenizer.tokenize()` (pyvi)
7. **Loại stopwords** và từ có độ dài ≤ 1

---

### 3.5. `core/models.py` — Quản lý mô hình AI

**Chức năng**: Load mô hình đã huấn luyện và thực hiện dự đoán cảm xúc.

**Các thành phần chi tiết**:

#### a) Hằng số mapping
| Hằng số       | Mô tả                                    | Giá trị                                         |
|---------------|-------------------------------------------|--------------------------------------------------|
| `LABEL_MAP`   | Mapping label_id → tên nhãn tiếng Việt    | {0: "TIÊU CỰC", 1: "TRUNG TÍNH", 2: "TÍCH CỰC"} |
| `EMOJI_MAP`   | Mapping label_id → emoji                  | {0: "❌", 1: "😐", 2: "✅"}                      |
| `COLOR_MAP`   | Mapping label_id → mã màu                | {0: "#ef4444", 1: "#f59e0b", 2: "#22c55e"}       |
| `LABEL_EN`    | Mapping label_id → nhãn tiếng Anh         | {0: "Negative", 1: "Neutral", 2: "Positive"}     |

#### b) Hàm `load_phobert()` — Load mô hình PhoBERT
- **Decorator**: `@st.cache_resource` (cache để không load lại)
- **Hành động**: Load tokenizer và model từ `./models/phobert_best/`
- **Thư viện**: `AutoTokenizer`, `AutoModelForSequenceClassification` (HuggingFace)
- **Return**: `(tokenizer, model)` — model ở chế độ `eval()`

#### c) Hàm `load_baseline()` — Load mô hình Naive Bayes
- **Decorator**: `@st.cache_resource` (cache)
- **Hành động**: Load pipeline từ `./models/best_baseline.pkl` bằng `joblib`
- **Return**: scikit-learn Pipeline object

#### d) Hàm `predict_phobert(text, tokenizer, model)`
- **Input**: text gốc (chưa tiền xử lý), tokenizer, model
- **Xử lý**:
  1. Tokenize text (max_length=128, truncation, padding)
  2. Forward pass qua model (với `torch.no_grad()`)
  3. Áp dụng softmax lên logits → probabilities
  4. Lấy argmax → predicted label
- **Return**: `(pred, probs)` — label_id và list 3 xác suất [neg, neu, pos]

#### e) Hàm `predict_baseline(text, model)`
- **Input**: text gốc, baseline model (pipeline)
- **Xử lý**:
  1. Tiền xử lý text bằng `preprocess()` từ `core.preprocessing`
  2. Gọi `model.predict()` → predicted label
  3. Gọi `model.predict_proba()` → probabilities (có try/except)
- **Return**: `(pred, probs)` — tương tự PhoBERT

#### f) Hàm `predict_batch(texts, model_choice="PhoBERT")`
- **Input**: danh sách bình luận, tên model ("PhoBERT" hoặc "Naive Bayes")
- **Xử lý**: Duyệt từng text, gọi hàm predict tương ứng
- **Return**: `list[dict]` với mỗi dict chứa:
  - `text`: bình luận gốc
  - `pred`: label_id (0/1/2)
  - `label`: tên nhãn ("TIÊU CỰC"/"TRUNG TÍNH"/"TÍCH CỰC")
  - `emoji`: emoji tương ứng
  - `probs`: list 3 xác suất [neg, neu, pos]
  - `confidence`: xác suất cao nhất (max(probs))

---

### 3.6. `core/database.py` — Quản lý Database

**Chức năng**: Quản lý database SQLite lưu trữ lịch sử phân tích cảm xúc.

**Database**: `data/history.db`

#### a) Cấu trúc Database

**Bảng `analysis_sessions`** — Lưu thông tin phiên phân tích:

| Cột              | Kiểu      | Mô tả                                          |
|------------------|-----------|-------------------------------------------------|
| id               | INTEGER   | Primary key, auto increment                     |
| name             | TEXT      | Tên phiên (tên file, tên sản phẩm...)           |
| source           | TEXT      | Nguồn dữ liệu (`upload`/`shopee`/`manual`)      |
| model_used       | TEXT      | Model đã dùng (`PhoBERT`/`Naive Bayes`)          |
| total_comments   | INTEGER   | Tổng số bình luận                                |
| positive_count   | INTEGER   | Số bình luận tích cực                            |
| neutral_count    | INTEGER   | Số bình luận trung tính                          |
| negative_count   | INTEGER   | Số bình luận tiêu cực                            |
| created_at       | TIMESTAMP | Thời gian tạo (tự động)                         |

**Bảng `analysis_results`** — Lưu chi tiết kết quả từng bình luận:

| Cột              | Kiểu      | Mô tả                                          |
|------------------|-----------|-------------------------------------------------|
| id               | INTEGER   | Primary key, auto increment                     |
| session_id       | INTEGER   | Foreign key → analysis_sessions(id), ON DELETE CASCADE |
| comment_text     | TEXT      | Nội dung bình luận                               |
| predicted_label  | INTEGER   | Nhãn dự đoán (0/1/2)                            |
| label_name       | TEXT      | Tên nhãn ("TIÊU CỰC"/"TRUNG TÍNH"/"TÍCH CỰC") |
| confidence       | REAL      | Độ tin cậy (0.0 – 1.0)                          |
| probabilities    | TEXT      | JSON array 3 xác suất                            |

#### b) Các hàm chức năng

| Hàm                             | Chức năng                                                  |
|----------------------------------|------------------------------------------------------------|
| `_ensure_dir()`                  | Tạo thư mục `data/` nếu chưa tồn tại                     |
| `get_connection()`               | Tạo kết nối SQLite, sử dụng `row_factory = sqlite3.Row`   |
| `init_db()`                      | Khởi tạo 2 bảng nếu chưa tồn tại (CREATE IF NOT EXISTS)  |
| `save_session(name, source, model_used, results)` | Lưu 1 phiên phân tích (session + results) → return session_id |
| `get_all_sessions()`             | Lấy tất cả phiên, sắp xếp mới nhất trước                 |
| `get_session_results(session_id)`| Lấy chi tiết kết quả của 1 phiên                          |
| `get_session_by_id(session_id)`  | Lấy thông tin 1 phiên theo ID                             |
| `delete_session(session_id)`     | Xóa phiên và tất cả kết quả liên quan                     |
| `get_aggregate_stats()`          | Lấy thống kê tổng hợp (tổng phiên, tổng bình luận, tổng pos/neu/neg) |

---

### 3.7. `utils/__init__.py` — Package Utils

**Chức năng**: Khai báo package `utils`.

**Nội dung**: Comment mô tả "Utils module - tiện ích biểu đồ và xuất báo cáo".

---

### 3.8. `utils/charts.py` — Biểu đồ Plotly

**Chức năng**: Tạo các biểu đồ Plotly để trực quan hóa kết quả phân tích cảm xúc.

**Theme**: Dark mode nhất quán (`plotly_dark`), nền trong suốt.

**Bảng màu cảm xúc**:
- Tích cực: `#22c55e` (xanh lá)
- Trung tính: `#f59e0b` (vàng/cam)
- Tiêu cực: `#ef4444` (đỏ)

#### Danh sách hàm

| Hàm                                                    | Loại biểu đồ            | Mô tả                                                                                |
|---------------------------------------------------------|--------------------------|----------------------------------------------------------------------------------------|
| `create_pie_chart(positive, neutral, negative, title)`  | Donut Chart (Pie, hole=0.45) | Biểu đồ tròn tỷ lệ 3 loại cảm xúc. Hiển thị label + percent. Hover: số lượng + %.   |
| `create_bar_chart(results, title)`                      | Bar Chart                | Biểu đồ cột phân bố cảm xúc. Input: list results → đếm theo label.                   |
| `create_confidence_histogram(results, title)`           | Histogram                | Phân bố độ tin cậy, 20 bins, màu tím #8b5cf6. Trục X format %.                        |
| `create_session_comparison(sessions, title)`            | Grouped Bar Chart        | So sánh giữa nhiều phiên: 3 nhóm cột (pos/neu/neg). Tên phiên cắt 20 ký tự.          |
| `create_prob_bar_chart(probs, title)`                   | Bar Chart                | Biểu đồ xác suất 3 nhãn cho phân tích đơn lẻ. Trục Y: 0–1, format %.                 |

---

### 3.9. `utils/export.py` — Xuất báo cáo

**Chức năng**: Xuất kết quả phân tích ra file CSV/Excel để download.

#### Danh sách hàm

| Hàm                                    | Chức năng                                                                                            |
|-----------------------------------------|------------------------------------------------------------------------------------------------------|
| `results_to_dataframe(results)`         | Chuyển list[dict] kết quả thành Pandas DataFrame. Các cột: Bình luận, Kết quả, Emoji, Độ tin cậy, P(Tiêu cực), P(Trung tính), P(Tích cực). |
| `export_to_csv(results)`               | Xuất ra bytes CSV (encoding utf-8-sig cho Excel mở đúng tiếng Việt).                                |
| `export_to_excel(results, sheet_name)` | Xuất ra bytes Excel (.xlsx) với format nâng cao bằng OpenPyXL.                                       |
| `create_summary_text(results)`          | Tạo text tóm tắt kết quả: tổng, tích cực, trung tính, tiêu cực, độ tin cậy TB.                     |

#### Chi tiết format Excel:
- **Header**: Nền xanh dương (#4472C4), chữ trắng, in đậm, căn giữa
- **Auto-fit column widths**: Tự điều chỉnh chiều rộng cột theo nội dung
- **Color-code cột "Kết quả"**:
  - TÍCH CỰC: nền xanh lá nhạt (#C6EFCE), chữ xanh đậm (#006100)
  - TIÊU CỰC: nền đỏ nhạt (#FFC7CE), chữ đỏ đậm (#9C0006)
  - TRUNG TÍNH: nền vàng nhạt (#FFEB9C), chữ vàng đậm (#9C6500)

---

### 3.10. `pages/1_📊_Dashboard.py` — Trang Dashboard

**Chức năng**: Hiển thị dashboard tổng quan thống kê từ toàn bộ lịch sử phân tích.

**Các thành phần giao diện**:

1. **Header gradient**: "📊 Dashboard Tổng quan"
2. **4 Metric cards**:
   - Số phiên phân tích (tím)
   - Số bình luận tích cực (xanh lá) + tỷ lệ %
   - Số bình luận trung tính (vàng) + tỷ lệ %
   - Số bình luận tiêu cực (đỏ) + tỷ lệ %
3. **Donut Chart**: Tỷ lệ cảm xúc tổng hợp
4. **Bar Chart**: Phân bố cảm xúc tổng hợp (thu thập tất cả results từ mọi phiên)
5. **Histogram**: Phân bố độ tin cậy
6. **Grouped Bar Chart**: So sánh 10 phiên gần nhất (nếu có ≥2 phiên)
7. **Bảng dữ liệu**: Danh sách tất cả phiên (Tên, Nguồn, Model, Tổng, ✅, 😐, ❌, Thời gian)

**Xử lý dữ liệu trống**: Hiển thị thông báo hướng dẫn nếu chưa có dữ liệu.

---

### 3.11. `pages/2_💬_Phan_Tich.py` — Trang Phân tích Đơn lẻ

**Chức năng**: Cho phép người dùng nhập 1 bình luận và nhận kết quả phân tích cảm xúc tức thì.

**Luồng hoạt động**:

1. **Chọn mô hình** (Radio button, ngang):
   - "PhoBERT (Chính xác hơn)"
   - "Naive Bayes (Nhanh hơn)"

2. **Nhập bình luận**: Text area, placeholder gợi ý

3. **Nhấn "🔍 Phân tích"** → spinner "Đang phân tích..."

4. **Hiển thị kết quả**:
   - **Result card**: Emoji lớn + tên nhãn + độ tin cậy. Có 3 style CSS:
     - `result-positive`: nền xanh lá mờ
     - `result-neutral`: nền vàng mờ
     - `result-negative`: nền đỏ mờ
   - **Biểu đồ xác suất**: Bar chart 3 cột (Tiêu cực / Trung tính / Tích cực)
   - **Giải thích chi tiết**: Expander hiển thị % từng nhãn và kết luận

5. **Nút lưu** "💾 Lưu kết quả vào lịch sử":
   - Gọi `save_session()` với source="manual"
   - Tên phiên: "Phân tích đơn: {text[:50]}..."

---

### 3.12. `pages/3_📁_Upload_File.py` — Trang Upload File

**Chức năng**: Upload file CSV/Excel chứa bình luận để phân tích cảm xúc hàng loạt.

**Luồng hoạt động**:

1. **Upload file** (CSV, XLSX, XLS)
2. **Đọc file** → hiển thị thông tin (tên file, số dòng, số cột)
3. **Xem trước** 10 dòng đầu (expander)
4. **Chọn cột** chứa bình luận (selectbox)
5. **Chọn mô hình** (radio button)
6. **Nhấn "🚀 Phân tích hàng loạt"**:
   - Lấy dữ liệu cột, dropna, chuyển string
   - Phân tích theo batch (mỗi batch 10 bình luận)
   - Progress bar hiển thị tiến trình
   - Lưu kết quả vào `st.session_state`

7. **Hiển thị kết quả**:
   - 4 Summary cards: Tổng / Tích cực / Trung tính / Tiêu cực
   - 2 Biểu đồ: Donut chart + Bar chart
   - Bảng chi tiết kết quả (có filter theo nhãn)
   - 3 nút action:
     - 📥 Tải CSV
     - 📥 Tải Excel
     - 💾 Lưu vào lịch sử

---

### 3.13. `pages/4_📜_Lich_Su.py` — Trang Lịch sử

**Chức năng**: Xem lại, so sánh, quản lý và xuất dữ liệu các phiên phân tích đã lưu.

**Các chức năng chính**:

1. **Danh sách phiên**: Bảng DataFrame hiển thị:
   - ID, Tên (cắt 50 ký tự), Nguồn (icon + text), Model, Tổng, ✅, 😐, ❌, Thời gian
   - Nguồn hiển thị: 📁 Upload, 🛒 Shopee, 💬 Thủ công

2. **Xem chi tiết phiên**:
   - Selectbox chọn phiên (hiển thị: "#ID — Tên")
   - 4 Metric: Tổng / Tích cực / Trung tính / Tiêu cực
   - Donut chart cho phiên đã chọn
   - Bảng chi tiết: Bình luận / Kết quả / Độ tin cậy
   - Nút export CSV + Excel

3. **So sánh phiên** (khi ≥2 phiên):
   - Multiselect chọn phiên (mặc định 2 phiên đầu)
   - Grouped bar chart so sánh

4. **Xóa phiên**:
   - Selectbox chọn phiên cần xóa
   - Nút "🗑️ Xóa phiên này" → xóa + rerun trang

---

### 3.14. `models/best_baseline.pkl` — Model Baseline

**Chức năng**: File model Naive Bayes baseline đã huấn luyện (scikit-learn Pipeline), lưu dạng pickle bằng `joblib`.

**Kích thước**: ~1.7 MB

**Sử dụng**: Được load bởi `core/models.py` → `load_baseline()` → `predict_baseline()`

---

### 3.15. `models/phobert_best/` — Model PhoBERT

**Chức năng**: Thư mục chứa mô hình PhoBERT (vinai/phobert-base) đã fine-tune cho bài toán phân loại cảm xúc 3 lớp.

**Các file**:

| File                    | Kích thước  | Mô tả                              |
|-------------------------|-------------|--------------------------------------|
| `config.json`           | ~925 B      | Cấu hình kiến trúc model            |
| `model.safetensors`     | ~540 MB     | Trọng số model (format safetensors)  |
| `tokenizer_config.json` | ~1.2 KB     | Cấu hình tokenizer                  |
| `vocab.txt`             | ~895 KB     | Bộ từ vựng                          |
| `bpe.codes`             | ~1.1 MB     | BPE encoding rules                   |
| `added_tokens.json`     | ~22 B       | Token bổ sung                        |

**Sử dụng**: Được load bởi `core/models.py` → `load_phobert()` → `predict_phobert()`

---

### 3.16. `data/history.db` — Database SQLite

**Chức năng**: Lưu trữ toàn bộ lịch sử phân tích cảm xúc.

**Kích thước**: ~16 KB (tùy thuộc lượng dữ liệu)

**Cấu trúc**: 2 bảng `analysis_sessions` và `analysis_results` (chi tiết tại mục 3.6).

---

### 3.17. `doankpdl.ipynb` — Notebook Huấn luyện

**Chức năng**: Jupyter Notebook chứa code huấn luyện và đánh giá các mô hình phân loại cảm xúc.

**Kích thước**: ~356 KB

---

## 4. SƠ ĐỒ KIẾN TRÚC HỆ THỐNG

```
┌─────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB APP                     │
│                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │   Home   │ │Dashboard │ │ Phân Tích│ │Upload/LS │   │
│  │ (app.py) │ │  (page1) │ │  (page2) │ │(page3/4) │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │
│       │             │            │             │         │
│  ┌────▼─────────────▼────────────▼─────────────▼─────┐  │
│  │              UTILS LAYER                          │  │
│  │  charts.py (Plotly)    export.py (CSV/Excel)      │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          │                               │
│  ┌───────────────────────▼───────────────────────────┐  │
│  │              CORE LAYER                           │  │
│  │  models.py        preprocessing.py   database.py  │  │
│  │  (Load & Predict) (Text cleaning)   (SQLite CRUD) │  │
│  └────┬──────────────────┬──────────────────┬────────┘  │
│       │                  │                  │            │
│  ┌────▼────┐    ┌────────▼────────┐   ┌─────▼──────┐   │
│  │ MODELS  │    │    LIBRARIES    │   │    DATA    │   │
│  │PhoBERT  │    │ PyVi, Torch,   │   │ history.db │   │
│  │Baseline │    │ Transformers   │   │  (SQLite)  │   │
│  └─────────┘    └────────────────┘   └────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 5. LUỒNG XỬ LÝ CHÍNH

### 5.1. Phân tích đơn lẻ
```
Người dùng nhập bình luận
    → Chọn model (PhoBERT / Naive Bayes)
    → [Nếu Naive Bayes]: preprocessing.preprocess(text) → model.predict()
    → [Nếu PhoBERT]: tokenizer.encode(text) → model.forward() → softmax
    → Kết quả: (label, probabilities, confidence)
    → Hiển thị: Result card + Bar chart xác suất
    → [Tùy chọn]: Lưu vào database (lịch sử)
```

### 5.2. Phân tích hàng loạt (Upload File)
```
Upload CSV/Excel
    → Đọc file → Pandas DataFrame
    → Chọn cột bình luận + chọn model
    → predict_batch(texts, model) — xử lý theo batch 10
    → Hiển thị: Summary cards + Pie chart + Bar chart + Bảng chi tiết
    → [Tùy chọn]: Tải CSV/Excel + Lưu vào lịch sử
```

### 5.3. Xem Dashboard
```
Truy cập trang Dashboard
    → get_aggregate_stats() → Thống kê tổng hợp
    → get_all_sessions() → Danh sách phiên
    → get_session_results() → Chi tiết từng phiên
    → Vẽ: Pie chart + Bar chart + Histogram + Session comparison
    → Hiển thị bảng danh sách phiên
```

---

## 6. HƯỚNG DẪN CHẠY PROJECT

### Yêu cầu
- Python 3.x
- Các thư viện: streamlit, torch, transformers, pyvi, joblib, pandas, scikit-learn, plotly, openpyxl, requests

### Cài đặt và chạy (Windows PowerShell)
```powershell
# Di chuyển đến thư mục project
Set-Location "D:\DAIHOC\NAM 3 - HK2\KTDL\project"

# Tạo môi trường ảo (nếu chưa có)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Cài thư viện
pip install --upgrade pip
pip install streamlit torch transformers pyvi joblib pandas scikit-learn requests plotly openpyxl

# Chạy ứng dụng
.\.venv\Scripts\streamlit.exe run app.py
```

---

## 7. CÁC THƯ VIỆN PHỤ THUỘC

| Thư viện       | Phiên bản | Mục đích sử dụng                                |
|----------------|-----------|--------------------------------------------------|
| streamlit      | —         | Framework web application                         |
| torch          | —         | Deep Learning framework (PyTorch)                 |
| transformers   | —         | HuggingFace — load/run PhoBERT                    |
| pyvi           | —         | Tokenizer tiếng Việt (ViTokenizer)                |
| joblib         | —         | Serialize/deserialize model scikit-learn           |
| pandas         | —         | Xử lý dữ liệu bảng (DataFrame)                   |
| scikit-learn   | —         | Machine Learning — Naive Bayes pipeline            |
| plotly         | —         | Vẽ biểu đồ tương tác (Pie, Bar, Histogram)        |
| openpyxl       | —         | Xuất Excel có format (màu sắc, font)              |
| requests       | —         | HTTP requests (crawl dữ liệu)                     |
