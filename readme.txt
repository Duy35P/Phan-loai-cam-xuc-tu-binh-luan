HƯỚNG DẪN CHẠY PROJECT

Yêu cầu:
- Python 3.x
- Các thư viện: streamlit, torch, transformers, pyvi, joblib, pandas, scikit-learn

(NẾU THIẾU MÔI TRƯỜNG HOAC75 THƯ VIỆN)
- CHẠY CÁC LỆNH SAU TRONG POWERSHELL
Set-Location "D:\DAIHOC\NAM 3 - HK2\KTDL\project"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install streamlit torch transformers pyvi joblib pandas scikit-learn requests plotly openpyxl
.\.venv\Scripts\streamlit.exe run app.py

CHẠY PROJECT
Các bước (Windows):
1. Mở terminal tại thư mục project.
2. (Tùy chọn) Tạo môi trường ảo:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
3. Cài thư viện:
   pip install streamlit torch transformers pyvi joblib pandas scikit-learn
4. Chạy ứng dụng:
   .\.venv\Scripts\streamlit.exe run app.py
   (hoặc nếu đã cài global) streamlit run app.py

GIẢI THÍCH CẤU TRÚC FILE

- app.py
  Ứng dụng Streamlit cho bài toán phân tích cảm xúc bình luận.
  Cho phép chọn 2 mô hình (PhoBERT hoặc Naive Bayes), tiền xử lý dữ liệu,
  hiển thị kết quả và biểu đồ xác suất.

- models\
  Thư mục chứa các model đã huấn luyện.

  - best_baseline.pkl
    Model baseline (scikit-learn) dùng cho lựa chọn "Naive Bayes (Nhanh hơn)".

  - phobert_best\
    Các file của mô hình PhoBERT (HuggingFace) đã fine-tune:
    + config.json: cấu hình mô hình
    + model.safetensors: trọng số mô hình
    + tokenizer_config.json: cấu hình tokenizer
    + vocab.txt, bpe.codes, added_tokens.json: tài nguyên tokenizer

- .venv\
  Môi trường ảo Python (nếu đã tạo).

- readme.txt
  Tài liệu hướng dẫn chạy project và mô tả cấu trúc file.

