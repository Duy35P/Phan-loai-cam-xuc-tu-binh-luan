"""
Module quản lý model và prediction.
Hỗ trợ: PhoBERT (fine-tuned), Naive Bayes (baseline), và batch prediction.
"""

import os
import torch
import joblib
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from core.preprocessing import preprocess

# ==================== CONSTANTS ====================
LABEL_MAP = {0: "TIÊU CỰC", 1: "TRUNG TÍNH", 2: "TÍCH CỰC"}
EMOJI_MAP = {0: "❌", 1: "😐", 2: "✅"}
COLOR_MAP = {0: "#ef4444", 1: "#f59e0b", 2: "#22c55e"}
LABEL_EN = {0: "Negative", 1: "Neutral", 2: "Positive"}

# ===== CẤU HÌNH HUGGINGFACE =====
# 👉 SAU KHI UPLOAD MODEL, HÃY CẬP NHẬT DÒNG NÀY:
#    Ví dụ: HUGGINGFACE_REPO_ID = "username/phobert-sentiment-vietnamese"
HUGGINGFACE_REPO_ID = "YUd35P/phobert-sentiment-vietnamese"

LOCAL_MODEL_PATH = './models/phobert_best'


# ==================== LOAD MODELS ====================
@st.cache_resource
def load_phobert():
    """Load PhoBERT model và tokenizer (cached).
    
    Nếu model chưa có local (chưa tải hoặc đã bị gitignore),
    sẽ tự động tải từ HuggingFace Hub.
    """
    model_file = os.path.join(LOCAL_MODEL_PATH, 'model.safetensors')
    pytorch_file = os.path.join(LOCAL_MODEL_PATH, 'pytorch_model.bin')
    
    if os.path.exists(model_file) or os.path.exists(pytorch_file):
        # Load từ local
        source = LOCAL_MODEL_PATH
    else:
        # Tải từ HuggingFace Hub
        st.info(f"⏬ Đang tải model PhoBERT từ HuggingFace ({HUGGINGFACE_REPO_ID})... Chỉ cần tải 1 lần.")
        source = HUGGINGFACE_REPO_ID
    
    tokenizer = AutoTokenizer.from_pretrained(source)
    model = AutoModelForSequenceClassification.from_pretrained(source)
    model.eval()
    return tokenizer, model


@st.cache_resource
def load_baseline():
    """Load baseline model (Naive Bayes pipeline, cached)."""
    return joblib.load('./models/best_baseline.pkl')


# ==================== PREDICTION ====================
def predict_phobert(text, tokenizer, model):
    """Dự đoán cảm xúc bằng PhoBERT. Trả về (label_id, probabilities)."""
    enc = tokenizer(text, return_tensors='pt',
                    max_length=128, truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**enc).logits
    probs = torch.softmax(logits, dim=1)[0].tolist()
    pred = int(torch.argmax(logits, dim=1))
    return pred, probs


def predict_baseline(text, model):
    """Dự đoán cảm xúc bằng Naive Bayes. Trả về (label_id, probabilities)."""
    cleaned = preprocess(text)
    pred = int(model.predict([cleaned])[0])
    try:
        probs = model.predict_proba([cleaned])[0].tolist()
    except Exception:
        probs = [0.0, 0.0, 0.0]
        probs[pred] = 1.0
    return pred, probs


def predict_batch(texts, model_choice="PhoBERT"):
    """
    Phân tích hàng loạt. Trả về list[dict] với keys:
    - text: bình luận gốc
    - pred: label_id (0/1/2)
    - label: tên nhãn
    - emoji: emoji tương ứng
    - probs: [neg, neu, pos]
    - confidence: max(probs)
    """
    results = []

    if model_choice == "PhoBERT":
        tokenizer, model = load_phobert()
        for text in texts:
            pred, probs = predict_phobert(text, tokenizer, model)
            results.append({
                'text': text,
                'pred': pred,
                'label': LABEL_MAP[pred],
                'emoji': EMOJI_MAP[pred],
                'probs': probs,
                'confidence': max(probs)
            })
    else:
        model = load_baseline()
        for text in texts:
            pred, probs = predict_baseline(text, model)
            results.append({
                'text': text,
                'pred': pred,
                'label': LABEL_MAP[pred],
                'emoji': EMOJI_MAP[pred],
                'probs': probs,
                'confidence': max(probs)
            })

    return results
