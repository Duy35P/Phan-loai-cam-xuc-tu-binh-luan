"""
Module tiền xử lý văn bản cho phân tích cảm xúc.
Hỗ trợ: chuẩn hóa teencode, xử lý emoji, tokenize tiếng Việt.
"""

import re
from pyvi import ViTokenizer

# ==================== STOPWORDS ====================
STOPWORDS = set([
    'và', 'của', 'là', 'có', 'để', 'trong', 'với', 'này', 'đó',
    'cho', 'được', 'một', 'các', 'khi', 'đã', 'thì', 'mà',
    'hay', 'hoặc', 'nếu', 'vì', 'nhưng', 'tuy', 'dù', 'cũng',
    'rất', 'lắm', 'quá', 'hơn', 'nhất', 'bị', 'làm', 'theo'
])

# ==================== TEENCODE MAP ====================
TEENCODE_MAP = {
    'ko': 'không', 'k': 'không', 'kh': 'không', 'khong': 'không',
    'dc': 'được', 'dk': 'được', 'đc': 'được',
    'ntn': 'như thế nào', 'nc': 'nói chuyện',
    'mn': 'mọi người', 'ng': 'người', 'nv': 'nhân viên',
    'sp': 'sản phẩm', 'ship': 'giao hàng', 'đt': 'điện thoại',
    'tks': 'cảm ơn', 'thks': 'cảm ơn', 'thanks': 'cảm ơn',
    'ok': 'tốt', 'oke': 'tốt', 'okie': 'tốt',
    'fb': 'facebook', 'ig': 'instagram',
    'lun': 'luôn', 'j': 'gì', 'z': 'vậy', 'v': 'vậy',
    'r': 'rồi', 'vs': 'với', 'đg': 'đường', 'hqua': 'hôm qua',
    'hnay': 'hôm nay', 'bth': 'bình thường', 'bt': 'bình thường',
    'cx': 'cũng', 'ms': 'mới', 'mk': 'mình', 'mik': 'mình',
    'tl': 'trả lời', 'rep': 'trả lời', 'sd': 'sử dụng',
    'ghe': 'ghê', 'qua': 'quá', 'wa': 'quá', 'wá': 'quá',
    'nhiu': 'nhiều', 'iu': 'yêu', 'thik': 'thích',
    'trc': 'trước', 'sau': 'sau', 'ntn': 'như thế nào',
    'gd': 'gia đình', 'bn': 'bạn', 'biet': 'biết',
    'lm': 'làm', 'xl': 'xin lỗi', 'sorry': 'xin lỗi',
    'sz': 'size', 'nt': 'nhắn tin', 'dt': 'điện thoại',
    'nch': 'nói chuyện', 'ak': 'à', 'ạ': 'à',
}

# ==================== EMOJI SENTIMENT MAP ====================
EMOJI_SENTIMENT = {
    # Tích cực
    '😍': 'yêu_thích', '❤️': 'yêu_thích', '💕': 'yêu_thích',
    '😊': 'vui', '😁': 'vui', '😄': 'vui', '🥰': 'yêu_thích',
    '👍': 'tốt', '👏': 'tuyệt_vời', '🎉': 'tuyệt_vời',
    '✅': 'tốt', '💯': 'tuyệt_vời', '⭐': 'tốt',
    '🔥': 'tuyệt_vời', '💪': 'tốt',
    # Tiêu cực
    '😡': 'tức_giận', '😤': 'tức_giận', '😠': 'tức_giận',
    '👎': 'tệ', '😢': 'buồn', '😭': 'buồn',
    '💔': 'thất_vọng', '😞': 'thất_vọng', '😔': 'thất_vọng',
    '🤮': 'ghê', '🤢': 'ghê', '❌': 'tệ',
    '😤': 'bực', '🤬': 'tức_giận',
}


def replace_teencode(text):
    """Thay thế teencode bằng từ chuẩn."""
    words = text.split()
    result = []
    for word in words:
        result.append(TEENCODE_MAP.get(word, word))
    return ' '.join(result)


def replace_emoji(text):
    """Thay thế emoji bằng từ mô tả cảm xúc."""
    for emoji, meaning in EMOJI_SENTIMENT.items():
        text = text.replace(emoji, f' {meaning} ')
    return text


def preprocess(text):
    """
    Tiền xử lý text đầy đủ:
    1. Chuyển thường
    2. Thay emoji → từ cảm xúc
    3. Thay teencode
    4. Loại bỏ URL, ký tự đặc biệt, số
    5. Tokenize tiếng Việt (pyvi)
    6. Loại stopwords
    """
    if not isinstance(text, str) or not text.strip():
        return ''

    text = text.lower()
    text = replace_emoji(text)
    text = replace_teencode(text)
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    text = ViTokenizer.tokenize(text)
    tokens = [t for t in text.split() if t not in STOPWORDS and len(t) > 1]
    return ' '.join(tokens)
