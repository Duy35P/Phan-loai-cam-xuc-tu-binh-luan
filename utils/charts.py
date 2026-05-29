"""
Module vẽ biểu đồ Plotly cho dashboard phân tích cảm xúc.
Theme nhất quán: dark mode, gradient colors.
"""

import plotly.express as px
import plotly.graph_objects as go
from collections import Counter


# ==================== COLOR SCHEME ====================
SENTIMENT_COLORS = {
    'TÍCH CỰC': '#22c55e',
    'TRUNG TÍNH': '#f59e0b',
    'TIÊU CỰC': '#ef4444'
}

PLOTLY_TEMPLATE = 'plotly_dark'


def create_pie_chart(positive, neutral, negative, title="Tỷ lệ Cảm xúc"):
    """Biểu đồ tròn tỷ lệ cảm xúc."""
    labels = ['Tích cực', 'Trung tính', 'Tiêu cực']
    values = [positive, neutral, negative]
    colors = ['#22c55e', '#f59e0b', '#ef4444']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=colors, line=dict(color='#1e1e2e', width=2)),
        textinfo='label+percent',
        textfont=dict(size=13, color='white'),
        hovertemplate='%{label}: %{value} bình luận<br>(%{percent})<extra></extra>'
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white')),
        template=PLOTLY_TEMPLATE,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(font=dict(color='white', size=12)),
        height=400,
        margin=dict(t=60, b=30, l=30, r=30)
    )

    return fig


def create_bar_chart(results, title="Phân bố Cảm xúc"):
    """Biểu đồ cột phân bố cảm xúc."""
    counts = Counter([r['label'] for r in results])
    labels = ['TIÊU CỰC', 'TRUNG TÍNH', 'TÍCH CỰC']
    values = [counts.get(l, 0) for l in labels]
    colors = ['#ef4444', '#f59e0b', '#22c55e']

    fig = go.Figure(data=[go.Bar(
        x=['Tiêu cực', 'Trung tính', 'Tích cực'],
        y=values,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=values,
        textposition='auto',
        textfont=dict(size=14, color='white'),
        hovertemplate='%{x}: %{y} bình luận<extra></extra>'
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white')),
        template=PLOTLY_TEMPLATE,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='', tickfont=dict(color='white', size=13)),
        yaxis=dict(
            title=dict(text='Số bình luận', font=dict(color='white')),
            tickfont=dict(color='white')
        ),
        height=400,
        margin=dict(t=60, b=40, l=50, r=30)
    )

    return fig


def create_confidence_histogram(results, title="Phân bố Độ tin cậy"):
    """Biểu đồ histogram độ tin cậy."""
    confidences = [r['confidence'] for r in results]

    fig = go.Figure(data=[go.Histogram(
        x=confidences,
        nbinsx=20,
        marker=dict(
            color='#8b5cf6',
            line=dict(color='rgba(255,255,255,0.3)', width=1)
        ),
        hovertemplate='Độ tin cậy: %{x:.1%}<br>Số lượng: %{y}<extra></extra>'
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white')),
        template=PLOTLY_TEMPLATE,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title=dict(text='Độ tin cậy', font=dict(color='white')),
            tickformat='.0%',
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            title=dict(text='Số bình luận', font=dict(color='white')),
            tickfont=dict(color='white')
        ),
        height=350,
        margin=dict(t=60, b=50, l=50, r=30)
    )

    return fig


def create_session_comparison(sessions, title="So sánh Phiên phân tích"):
    """Biểu đồ cột nhóm so sánh giữa các phiên."""
    if not sessions:
        return go.Figure()

    names = [s['name'][:20] for s in sessions]
    pos = [s['positive_count'] for s in sessions]
    neu = [s['neutral_count'] for s in sessions]
    neg = [s['negative_count'] for s in sessions]

    fig = go.Figure(data=[
        go.Bar(name='Tích cực', x=names, y=pos, marker_color='#22c55e'),
        go.Bar(name='Trung tính', x=names, y=neu, marker_color='#f59e0b'),
        go.Bar(name='Tiêu cực', x=names, y=neg, marker_color='#ef4444'),
    ])

    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white')),
        barmode='group',
        template=PLOTLY_TEMPLATE,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(font=dict(color='white', size=12)),
        xaxis=dict(tickfont=dict(color='white')),
        yaxis=dict(
            title=dict(text='Số bình luận', font=dict(color='white')),
            tickfont=dict(color='white')
        ),
        height=400,
        margin=dict(t=60, b=50, l=50, r=30)
    )

    return fig


def create_prob_bar_chart(probs, title="Xác suất từng nhãn"):
    """Biểu đồ xác suất cho phân tích đơn lẻ."""
    labels = ['Tiêu cực', 'Trung tính', 'Tích cực']
    colors = ['#ef4444', '#f59e0b', '#22c55e']

    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=probs,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.2)', width=1)
        ),
        text=[f'{p:.1%}' for p in probs],
        textposition='auto',
        textfont=dict(size=14, color='white'),
        hovertemplate='%{x}: %{y:.2%}<extra></extra>'
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='white')),
        template=PLOTLY_TEMPLATE,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='white', size=13)),
        yaxis=dict(
            title=dict(text='Xác suất', font=dict(color='white')),
            tickformat='.0%',
            tickfont=dict(color='white'),
            range=[0, 1]
        ),
        height=300,
        margin=dict(t=50, b=40, l=50, r=30)
    )

    return fig
