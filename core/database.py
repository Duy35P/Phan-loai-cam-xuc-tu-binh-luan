"""
Module quản lý database SQLite cho lịch sử phân tích.
"""

import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'history.db')


def _ensure_dir():
    """Tạo thư mục data/ nếu chưa có."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_connection():
    """Tạo kết nối SQLite."""
    _ensure_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Khởi tạo database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source TEXT NOT NULL,
            model_used TEXT NOT NULL,
            total_comments INTEGER DEFAULT 0,
            positive_count INTEGER DEFAULT 0,
            neutral_count INTEGER DEFAULT 0,
            negative_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            comment_text TEXT NOT NULL,
            predicted_label INTEGER NOT NULL,
            label_name TEXT NOT NULL,
            confidence REAL NOT NULL,
            probabilities TEXT,
            FOREIGN KEY (session_id) REFERENCES analysis_sessions(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


def save_session(name, source, model_used, results):
    """
    Lưu phiên phân tích vào database.

    Args:
        name: tên phiên (ví dụ: tên file, tên sản phẩm)
        source: nguồn dữ liệu ('upload', 'shopee', 'manual')
        model_used: model đã dùng ('PhoBERT' / 'Naive Bayes')
        results: list[dict] từ predict_batch()

    Returns:
        session_id
    """
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    pos = sum(1 for r in results if r['pred'] == 2)
    neu = sum(1 for r in results if r['pred'] == 1)
    neg = sum(1 for r in results if r['pred'] == 0)

    cursor.execute('''
        INSERT INTO analysis_sessions (name, source, model_used, total_comments,
                                        positive_count, neutral_count, negative_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, source, model_used, len(results), pos, neu, neg))

    session_id = cursor.lastrowid

    for r in results:
        cursor.execute('''
            INSERT INTO analysis_results (session_id, comment_text, predicted_label,
                                           label_name, confidence, probabilities)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id, r['text'], r['pred'], r['label'],
              r['confidence'], json.dumps(r['probs'])))

    conn.commit()
    conn.close()
    return session_id


def get_all_sessions():
    """Lấy danh sách tất cả phiên phân tích."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM analysis_sessions ORDER BY created_at DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_session_results(session_id):
    """Lấy chi tiết kết quả của 1 phiên."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM analysis_results WHERE session_id = ? ORDER BY id
    ''', (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_session_by_id(session_id):
    """Lấy thông tin 1 phiên."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM analysis_sessions WHERE id = ?', (session_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_session(session_id):
    """Xóa phiên phân tích."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM analysis_results WHERE session_id = ?', (session_id,))
    cursor.execute('DELETE FROM analysis_sessions WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()


def get_aggregate_stats():
    """Lấy thống kê tổng hợp từ tất cả phiên."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            COUNT(*) as total_sessions,
            COALESCE(SUM(total_comments), 0) as total_comments,
            COALESCE(SUM(positive_count), 0) as total_positive,
            COALESCE(SUM(neutral_count), 0) as total_neutral,
            COALESCE(SUM(negative_count), 0) as total_negative
        FROM analysis_sessions
    ''')
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {
        'total_sessions': 0, 'total_comments': 0,
        'total_positive': 0, 'total_neutral': 0, 'total_negative': 0
    }
