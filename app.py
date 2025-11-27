import streamlit as st
import os
from groq import Groq
import json
import pandas as pd
import time
import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DidYouThough? | Accountability Engine",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENHANCED CUSTOM CSS WITH ANIMATIONS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-primary: #030712;
        --bg-secondary: #0f172a;
        --bg-card: rgba(15, 23, 42, 0.6);
        --border-subtle: rgba(148, 163, 184, 0.1);
        --border-glow: rgba(99, 102, 241, 0.4);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-primary: #6366f1;
        --accent-secondary: #8b5cf6;
        --accent-cyan: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }

    /* Animated background */
    .stApp {
        background: var(--bg-primary);
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(99, 102, 241, 0.15), transparent),
            radial-gradient(ellipse 60% 40% at 100% 0%, rgba(139, 92, 246, 0.1), transparent),
            radial-gradient(ellipse 50% 30% at 0% 100%, rgba(6, 182, 212, 0.08), transparent);
    }

    /* Typography */
    h1, h2, h3, h4 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }
    h1 { font-size: 2rem !important; }
    h2 { font-size: 1.5rem !important; }
    h3 { font-size: 1.15rem !important; }
    p, label, .stMarkdown { color: var(--text-secondary) !important; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
        border-right: 1px solid var(--border-subtle);
    }
    [data-testid="stSidebar"] .stMarkdown h2 {
        background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.3rem !important;
    }

    /* === HERO SECTION === */
    .hero-container {
        position: relative;
        border-radius: 24px;
        padding: 32px 36px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.05) 50%, rgba(6, 182, 212, 0.03) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(20px);
        box-shadow: 
            0 0 0 1px rgba(255,255,255,0.03) inset,
            0 25px 50px -12px rgba(0, 0, 0, 0.5),
            0 0 100px -20px rgba(99, 102, 241, 0.3);
        margin-bottom: 2rem;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.5), rgba(139, 92, 246, 0.5), transparent);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        font-size: 0.75rem;
        font-weight: 500;
        color: #a5b4fc;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .hero-badge .pulse {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--success);
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    .hero-title {
        font-size: 2.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 50%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--text-secondary);
        max-width: 520px;
        line-height: 1.6;
    }
    .hero-subtitle strong {
        color: var(--text-primary);
        font-weight: 600;
    }

    /* === GLASSMORPHISM CARDS === */
    .glass-card {
        background: rgba(15, 23, 42, 0.5);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        padding: 24px;
        box-shadow: 
            0 0 0 1px rgba(255,255,255,0.02) inset,
            0 20px 40px -15px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 
            0 0 0 1px rgba(255,255,255,0.05) inset,
            0 25px 50px -15px rgba(0, 0, 0, 0.5),
            0 0 40px -10px rgba(99, 102, 241, 0.2);
        transform: translateY(-2px);
    }
    .glass-card-glow {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.25);
        padding: 28px;
        box-shadow: 
            0 0 0 1px rgba(255,255,255,0.03) inset,
            0 25px 50px -12px rgba(0, 0, 0, 0.5),
            0 0 60px -15px rgba(99, 102, 241, 0.25);
    }

    /* === METRIC CARDS === */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 20px 18px;
        box-shadow: 
            0 0 0 1px rgba(255,255,255,0.03) inset,
            0 15px 35px -10px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-3px);
        box-shadow: 
            0 0 0 1px rgba(255,255,255,0.05) inset,
            0 20px 40px -10px rgba(0, 0, 0, 0.5),
            0 0 30px -5px rgba(99, 102, 241, 0.3);
    }
    div[data-testid="metric-container"] label {
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-muted) !important;
        font-weight: 600;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* === INPUTS === */
    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.15) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        backdrop-filter: blur(8px);
        transition: all 0.2s ease;
    }
    .stTextInput input:focus,
    .stSelectbox div[data-baseweb="select"] > div:focus-within,
    .stTextArea textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15), 0 0 20px -5px rgba(99, 102, 241, 0.3) !important;
    }

    /* === BUTTONS === */
    .stButton > button {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
        color: #e0e7ff;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6rem 1.4rem;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 0.9rem;
        letter-spacing: 0.01em;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.35) 0%, rgba(139, 92, 246, 0.25) 100%);
        border-color: rgba(99, 102, 241, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.4);
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: 1px solid rgba(255,255,255,0.15);
        color: #ffffff;
        box-shadow: 0 8px 25px -8px rgba(99, 102, 241, 0.5);
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
        box-shadow: 0 12px 35px -8px rgba(99, 102, 241, 0.6);
    }

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.5);
        backdrop-filter: blur(12px);
        padding: 8px;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 12px 20px;
        background: transparent;
        border: none;
        color: var(--text-muted);
        font-weight: 500;
        border-radius: 10px;
        transition: all 0.2s ease;
        font-size: 0.9rem;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-secondary);
        background: rgba(99, 102, 241, 0.1);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.15) 100%) !important;
        color: #e0e7ff !important;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 4px 15px -5px rgba(99, 102, 241, 0.3);
    }

    /* === DATAFRAME === */
    .stDataFrame {
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        overflow: hidden;
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
    }

    /* === EXPANDERS === */
    .streamlit-expanderHeader {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(12px);
        border-radius: 12px !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        color: var(--text-primary) !important;
        font-weight: 500;
        padding: 16px 20px !important;
        transition: all 0.2s ease;
    }
    .streamlit-expanderHeader:hover {
        border-color: rgba(99, 102, 241, 0.3) !important;
        background: rgba(99, 102, 241, 0.1) !important;
    }
    .streamlit-expanderContent {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-top: none;
        border-bottom-left-radius: 12px;
        border-bottom-right-radius: 12px;
        padding: 20px 24px;
    }

    /* === TASK COMPLETION ANIMATION === */
    @keyframes taskComplete {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    @keyframes checkmark {
        0% { stroke-dashoffset: 100; }
        100% { stroke-dashoffset: 0; }
    }
    @keyframes confetti {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-100px) rotate(720deg); opacity: 0; }
    }
    .task-complete-animation {
        animation: taskComplete 0.5s ease-out;
    }
    .completion-banner {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 16px;
        padding: 20px 24px;
        display: flex;
        align-items: center;
        gap: 16px;
        animation: taskComplete 0.5s ease-out;
        box-shadow: 0 0 40px -10px rgba(16, 185, 129, 0.4);
    }
    .completion-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
    }
    .completion-text {
        flex: 1;
    }
    .completion-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #34d399;
        margin-bottom: 4px;
    }
    .completion-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
    }

    /* === SECTION HEADERS === */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }
    .section-icon {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    .section-subtitle {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin: 0;
    }

    /* === CHECKBOX STYLING === */
    .stCheckbox {
        transition: all 0.2s ease;
    }
    .stCheckbox:hover {
        transform: scale(1.02);
    }
    .stCheckbox label {
        padding: 12px 16px;
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 10px;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stCheckbox label:hover {
        border-color: rgba(99, 102, 241, 0.3);
        background: rgba(99, 102, 241, 0.05);
    }

    /* === SUCCESS/ERROR MESSAGES === */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px !important;
    }
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
    }
    .stInfo {
        background: rgba(99, 102, 241, 0.1) !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 12px !important;
    }
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
    }

    /* === PERSON CARD === */
    .person-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(15, 23, 42, 0.6) 100%);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 28px;
        box-shadow: 0 20px 50px -15px rgba(0, 0, 0, 0.4);
    }
    .person-name {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    /* === PROGRESS RING === */
    .progress-ring {
        position: relative;
        width: 120px;
        height: 120px;
    }
    .progress-ring-circle {
        transform: rotate(-90deg);
        transform-origin: 50% 50%;
    }
    .progress-ring-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 1.5rem;
        font-weight: 700;
        color: #fff;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Plotly chart container */
    .js-plotly-plot {
        border-radius: 16px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'db_tasks' not in st.session_state:
    st.session_state.db_tasks = pd.DataFrame(columns=[
        'Task ID', 'Description', 'Owner', 'Due Date', 'Priority',
        'Initiative', 'Status', 'Source Meeting', 'Created'
    ])

if 'db_meetings' not in st.session_state:
    st.session_state.db_meetings = []

if 'just_completed' not in st.session_state:
    st.session_state.just_completed = None

if 'completion_count' not in st.session_state:
    st.session_state.completion_count = 0

# --- CHART FUNCTIONS ---
def create_workload_chart(df):
    """Create animated donut chart for workload distribution"""
    owner_counts = df['Owner'].value_counts().reset_index()
    owner_counts.columns = ['Owner', 'Tasks']
    
    colors = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#ec4899']
    
    fig = go.Figure(data=[go.Pie(
        labels=owner_counts['Owner'],
        values=owner_counts['Tasks'],
        hole=0.65,
        marker=dict(colors=colors[:len(owner_counts)]),
        textinfo='label+value',
        textposition='outside',
        textfont=dict(size=12, color='#94a3b8'),
        hovertemplate="<b>%{label}</b><br>Tasks: %{value}<br>%{percent}<extra></extra>",
        pull=[0.02] * len(owner_counts)
    )])
    
    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=20, r=20),
        height=300,
        annotations=[dict(
            text=f'<b>{len(df)}</b><br>Tasks',
            x=0.5, y=0.5,
            font=dict(size=20, color='#f8fafc'),
            showarrow=False
        )]
    )
    
    return fig

def create_priority_chart(df):
    """Create animated bar chart for priority distribution"""
    priority_order = ['High', 'Med', 'Low']
    priority_colors = {'High': '#ef4444', 'Med': '#f59e0b', 'Low': '#10b981'}
    
    priority_counts = df['Priority'].value_counts().reindex(priority_order, fill_value=0)
    
    fig = go.Figure(data=[go.Bar(
        x=priority_counts.index,
        y=priority_counts.values,
        marker=dict(
            color=[priority_colors.get(p, '#6366f1') for p in priority_counts.index],
            line=dict(width=0),
            cornerradius=8
        ),
        text=priority_counts.values,
        textposition='outside',
        textfont=dict(size=14, color='#f8fafc'),
        hovertemplate="<b>%{x}</b><br>Tasks: %{y}<extra></extra>"
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=40, l=40, r=40),
        height=250,
        xaxis=dict(
            showgrid=False,
            showline=False,
            tickfont=dict(color='#94a3b8', size=12),
            title=None
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            showline=False,
            tickfont=dict(color='#64748b', size=11),
            title=None
        ),
        bargap=0.4
    )
    
    return fig

def create_initiative_chart(df):
    """Create horizontal bar chart for initiatives"""
    init_counts = df['Initiative'].value_counts().head(6)
    
    fig = go.Figure(data=[go.Bar(
        y=init_counts.index,
        x=init_counts.values,
        orientation='h',
        marker=dict(
            color='#6366f1',
            line=dict(width=0),
            cornerradius=6
        ),
        text=init_counts.values,
        textposition='outside',
        textfont=dict(size=12, color='#f8fafc'),
        hovertemplate="<b>%{y}</b><br>Tasks: %{x}<extra></extra>"
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=20, r=60),
        height=220,
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            showline=False,
            tickfont=dict(color='#64748b', size=11),
            title=None
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            tickfont=dict(color='#94a3b8', size=11),
            title=None,
            autorange='reversed'
        ),
        bargap=0.35
    )
    
    return fig

def create_timeline_chart(df):
    """Create timeline/area chart for tasks over time"""
    if 'Created' not in df.columns or df['Created'].isna().all():
        return None
    
    df_copy = df.copy()
    df_copy['Created'] = pd.to_datetime(df_copy['Created'])
    daily_counts = df_copy.groupby(df_copy['Created'].dt.date).size().reset_index()
    daily_counts.columns = ['Date', 'Tasks']
    daily_counts['Cumulative'] = daily_counts['Tasks'].cumsum()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_counts['Date'],
        y=daily_counts['Cumulative'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#6366f1', width=3),
        fillcolor='rgba(99, 102, 241, 0.2)',
        hovertemplate="<b>%{x}</b><br>Total Tasks: %{y}<extra></extra>"
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=40, l=40, r=20),
        height=200,
        xaxis=dict(
            showgrid=False,
            showline=False,
            tickfont=dict(color='#64748b', size=10),
            title=None
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            showline=False,
            tickfont=dict(color='#64748b', size=10),
            title=None
        )
    )
    
    return fig

def create_status_gauge(open_count, done_count):
    """Create a gauge chart for completion rate"""
    total = open_count + done_count
    completion_rate = (done_count / total * 100) if total > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=completion_rate,
        number=dict(suffix="%", font=dict(size=36, color='#f8fafc')),
        gauge=dict(
            axis=dict(
                range=[0, 100],
                tickwidth=0,
                tickcolor='rgba(0,0,0,0)',
                tickfont=dict(color='#64748b', size=10)
            ),
            bar=dict(color='#10b981', thickness=0.8),
            bgcolor='rgba(148, 163, 184, 0.1)',
            borderwidth=0,
            steps=[
                dict(range=[0, 33], color='rgba(239, 68, 68, 0.2)'),
                dict(range=[33, 66], color='rgba(245, 158, 11, 0.2)'),
                dict(range=[66, 100], color='rgba(16, 185, 129, 0.2)')
            ],
            threshold=dict(
                line=dict(color='#10b981', width=4),
                thickness=0.8,
                value=completion_rate
            )
        )
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=20, l=30, r=30),
        height=180,
        font=dict(color='#f8fafc')
    )
    
    return fig

# --- SIDEBAR & AUTH ---
with st.sidebar:
    st.markdown("## 🔥 DidYouThough?")
    st.caption("v3.0 · Accountability Engine")
    st.markdown("---")

    api_key = None
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ Connected to Groq")
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Get one at console.groq.com"
        )
        if not api_key:
            st.warning("⚠️ API Key required")

    st.markdown("### ⚙️ Model")
    model = st.selectbox(
        "Select model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    
    # Animated stats in sidebar
    open_tasks = len(st.session_state.db_tasks[st.session_state.db_tasks['Status'] == 'Open'])
    done_tasks = len(st.session_state.db_tasks[st.session_state.db_tasks['Status'] == 'Done'])
    total_tasks = len(st.session_state.db_tasks)
    
    if total_tasks > 0:
        st.markdown("### 📈 Progress")
        fig_gauge = create_status_gauge(open_tasks, done_tasks)
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
        st.caption(f"{done_tasks} of {total_tasks} tasks completed")

    st.markdown("---")
    if st.button("🗑️ Clear All Data", use_container_width=True):
        st.session_state.db_tasks = pd.DataFrame(columns=st.session_state.db_tasks.columns)
        st.session_state.db_meetings = []
        st.session_state.just_completed = None
        st.rerun()

# --- LOGIC FUNCTIONS ---
def process_input(content, source_type, meeting_name, client, model):
    system_prompt = """
    You are a skeptical Chief of Staff named 'DidYouThough'. 
    Your goal is to extract tasks, decisions, and risks from meeting notes.
    
    CRITICAL: Return ONLY valid JSON. No markdown formatting.
    Structure:
    {
        "tasks": [
            {"task": "Action description", "owner": "Name", "due_date": "YYYY-MM-DD or 'ASAP'",
             "priority": "High/Med/Low", "initiative": "Project Name"}
        ],
        "decisions": ["Decision 1", "Decision 2"],
        "risks": ["Risk 1"]
    }
    If owner is unknown, use "Unassigned". Infer initiative if missing.
    """

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this {source_type}: {content}"}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        data = json.loads(completion.choices[0].message.content)

        new_tasks = []
        for t in data.get('tasks', []):
            new_tasks.append({
                'Task ID': f"T-{len(st.session_state.db_tasks) + len(new_tasks) + 1:03d}",
                'Description': t['task'],
                'Owner': t['owner'],
                'Due Date': t['due_date'],
                'Priority': t['priority'],
                'Initiative': t['initiative'],
                'Status': 'Open',
                'Source Meeting': meeting_name,
                'Created': datetime.datetime.now()
            })

        if new_tasks:
            new_df = pd.DataFrame(new_tasks)
            st.session_state.db_tasks = pd.concat(
                [st.session_state.db_tasks, new_df],
                ignore_index=True
            )

        st.session_state.db_meetings.append({
            "Date": datetime.date.today(),
            "Name": meeting_name,
            "Type": source_type,
            "Decisions": data.get('decisions', []),
            "Risks": data.get('risks', [])
        })

        return True, len(new_tasks)

    except Exception as e:
        return False, str(e)

def mark_task_complete(task_id):
    """Mark a task as complete with animation trigger"""
    idx = st.session_state.db_tasks[st.session_state.db_tasks['Task ID'] == task_id].index
    if len(idx) > 0:
        st.session_state.db_tasks.loc[idx, 'Status'] = 'Done'
        st.session_state.just_completed = task_id
        st.session_state.completion_count += 1

# --- HERO HEADER ---
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span class="pulse"></span>
        Live accountability layer
    </div>
    <div class="hero-title">DidYouThough?</div>
    <div class="hero-subtitle">
        Turning <strong>procrastinations</strong> into a visible, trackable commitments graph — 
        without adding more tools for people to ignore.
    </div>
</div>
""", unsafe_allow_html=True)

# Show completion animation if just completed a task
if st.session_state.just_completed:
    task_desc = st.session_state.db_tasks[
        st.session_state.db_tasks['Task ID'] == st.session_state.just_completed
    ]['Description'].values
    if len(task_desc) > 0:
        st.markdown(f"""
        <div class="completion-banner">
            <div class="completion-icon">✓</div>
            <div class="completion-text">
                <div class="completion-title">Task Completed! 🎉</div>
                <div class="completion-subtitle">{task_desc[0][:60]}{'...' if len(task_desc[0]) > 60 else ''}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.just_completed = None
        time.sleep(2)
        st.rerun()

# Quick stats row
cols = st.columns(4)
open_count = len(st.session_state.db_tasks[st.session_state.db_tasks['Status'] == 'Open'])
done_count = len(st.session_state.db_tasks[st.session_state.db_tasks['Status'] == 'Done'])
high_count = len(st.session_state.db_tasks[st.session_state.db_tasks['Priority'] == 'High'])
initiative_count = st.session_state.db_tasks['Initiative'].nunique() if not st.session_state.db_tasks.empty else 0
meeting_count = len(st.session_state.db_meetings)

with cols[0]:
    st.metric("Open Tasks", open_count, delta=f"-{done_count} done" if done_count > 0 else None, delta_color="normal")
with cols[1]:
    st.metric("High Priority", high_count)
with cols[2]:
    st.metric("Initiatives", initiative_count)
with cols[3]:
    st.metric("Meetings", meeting_count)

st.markdown("<br>", unsafe_allow_html=True)

# --- MAIN APP LAYOUT ---
tab_capture, tab_dashboard, tab_people, tab_meetings = st.tabs([
    "📥 Capture", "📊 Dashboard", "👥 People", "📅 Meeting Log"
])

# --- TAB 1: CAPTURE ---
with tab_capture:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📥</div>
        <div>
            <div class="section-title">Capture Meeting</div>
            <div class="section-subtitle">Extract commitments from audio or text</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Meeting Details")
        meeting_name = st.text_input(
            "Meeting title",
            value="Weekly Sync",
            placeholder="e.g. Q3 Roadmap Review"
        )
        input_method = st.radio(
            "Source type",
            ["Audio File", "Text / Notes"],
            horizontal=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📄 Content")
        content_to_process = None

        if input_method == "Audio File":
            uploaded_file = st.file_uploader(
                "Upload recording",
                type=["mp3", "m4a", "wav"],
                help="Supports MP3, M4A, and WAV formats"
            )
            if uploaded_file and api_key:
                if st.button("🎧 Transcribe & Analyze", type="primary", use_container_width=True):
                    client = Groq(api_key=api_key)
                    with st.status("🎧 Transcribing audio...", expanded=True) as status:
                        transcription = client.audio.transcriptions.create(
                            file=(uploaded_file.name, uploaded_file.read()),
                            model="whisper-large-v3",
                            response_format="text"
                        )
                        status.update(label="✅ Transcription complete", state="complete", expanded=False)
                    content_to_process = transcription
        else:
            text_input = st.text_area(
                "Paste transcript or raw notes",
                height=150,
                placeholder="Paste your meeting notes, transcript, or raw text here..."
            )
            if st.button("🧠 Analyze Text", type="primary", use_container_width=True):
                content_to_process = text_input
        st.markdown("</div>", unsafe_allow_html=True)

    # Processing Logic
    if content_to_process and api_key:
        client = Groq(api_key=api_key)
        with st.status("🧠 Extracting tasks, decisions & risks...", expanded=True):
            st.write("Parsing commitments with AI...")
            success, result = process_input(content_to_process, input_method, meeting_name, client, model)

            if success:
                st.success(f"✅ Successfully extracted **{result} tasks**!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"❌ Error: {result}")

# --- TAB 2: DASHBOARD ---
with tab_dashboard:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <div>
            <div class="section-title">Dashboard</div>
            <div class="section-subtitle">Team workload and open loops</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.db_tasks.empty:
        st.info("👋 No data yet. Head to **Capture** to process your first meeting.")
    else:
        # Charts row
        chart_cols = st.columns([1, 1, 1])
        
        with chart_cols[0]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("##### 👥 Workload Distribution")
            fig_workload = create_workload_chart(st.session_state.db_tasks)
            st.plotly_chart(fig_workload, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)
        
        with chart_cols[1]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("##### ⚡ Priority Breakdown")
            fig_priority = create_priority_chart(st.session_state.db_tasks)
            st.plotly_chart(fig_priority, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)
        
        with chart_cols[2]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("##### 🎯 By Initiative")
            fig_init = create_initiative_chart(st.session_state.db_tasks)
            st.plotly_chart(fig_init, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Task table with completion
        st.markdown('<div class="glass-card-glow">', unsafe_allow_html=True)
        st.markdown("#### 📋 Task Management")

        col_filter, col_table = st.columns([1, 3], gap="medium")

        with col_filter:
            st.markdown("**Filters**")
            all_initiatives = st.session_state.db_tasks['Initiative'].unique()
            sel_init = st.multiselect("Initiative", all_initiatives, default=list(all_initiatives))

            all_owners = st.session_state.db_tasks['Owner'].unique()
            sel_owner = st.multiselect("Owner", all_owners, default=list(all_owners))
            
            status_filter = st.multiselect("Status", ['Open', 'Done'], default=['Open'])

            filtered_df = st.session_state.db_tasks[
                (st.session_state.db_tasks['Initiative'].isin(sel_init)) &
                (st.session_state.db_tasks['Owner'].isin(sel_owner)) &
                (st.session_state.db_tasks['Status'].isin(status_filter))
            ]

        with col_table:
            # Interactive task list with checkboxes
            for _, row in filtered_df.iterrows():
                col_check, col_desc, col_owner, col_due, col_priority = st.columns([0.5, 4, 1.5, 1, 1])
                
                with col_check:
                    is_done = row['Status'] == 'Done'
                    if st.checkbox("", value=is_done, key=f"task_{row['Task ID']}", label_visibility="collapsed"):
                        if not is_done:
                            mark_task_complete(row['Task ID'])
                            st.rerun()
                
                with col_desc:
                    style = "text-decoration: line-through; color: #64748b;" if row['Status'] == 'Done' else ""
                    st.markdown(f"<span style='{style}'>{row['Description']}</span>", unsafe_allow_html=True)
                
                with col_owner:
                    st.caption(row['Owner'])
                
                with col_due:
                    st.caption(row['Due Date'])
                
                with col_priority:
                    color_map = {'High': '#ef4444', 'Med': '#f59e0b', 'Low': '#10b981'}
                    st.markdown(f"<span style='color: {color_map.get(row['Priority'], '#94a3b8')};'>{row['Priority']}</span>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: PEOPLE ---
with tab_people:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">👥</div>
        <div>
            <div class="section-title">People</div>
            <div class="section-subtitle">Individual accountability view</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.db_tasks.empty:
        st.info("No tasks assigned yet. Process a meeting to see people here.")
    else:
        col_sel, col_view = st.columns([1, 3], gap="large")

        with col_sel:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("**Select Person**")
            owner = st.radio(
                "Team members",
                st.session_state.db_tasks['Owner'].unique(),
                label_visibility="collapsed"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_view:
            person_tasks = st.session_state.db_tasks[st.session_state.db_tasks['Owner'] == owner]
            open_person = len(person_tasks[person_tasks['Status'] == 'Open'])
            done_person = len(person_tasks[person_tasks['Status'] == 'Done'])

            st.markdown(f"""
            <div class="person-card">
                <div class="person-name">{owner}</div>
            </div>
            """, unsafe_allow_html=True)

            # Person stats with gauge
            stat_cols = st.columns([1, 1, 2])
            with stat_cols[0]:
                st.metric("Pending", open_person)
            with stat_cols[1]:
                st.metric("Completed", done_person)
            with stat_cols[2]:
                if open_person + done_person > 0:
                    fig_person_gauge = create_status_gauge(open_person, done_person)
                    st.plotly_chart(fig_person_gauge, use_container_width=True, config={'displayModeBar': False})

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### Task List")
            
            # Interactive checkboxes for person's tasks
            for _, row in person_tasks.iterrows():
                col_check, col_desc, col_due, col_priority = st.columns([0.5, 5, 1.5, 1])
                
                with col_check:
                    is_done = row['Status'] == 'Done'
                    if st.checkbox("", value=is_done, key=f"person_task_{row['Task ID']}", label_visibility="collapsed"):
                        if not is_done:
                            mark_task_complete(row['Task ID'])
                            st.rerun()
                
                with col_desc:
                    style = "text-decoration: line-through; color: #64748b;" if row['Status'] == 'Done' else ""
                    st.markdown(f"<span style='{style}'>{row['Description']}</span>", unsafe_allow_html=True)
                
                with col_due:
                    st.caption(row['Due Date'])
                
                with col_priority:
                    color_map = {'High': '#ef4444', 'Med': '#f59e0b', 'Low': '#10b981'}
                    st.markdown(f"<span style='color: {color_map.get(row['Priority'], '#94a3b8')};'>{row['Priority']}</span>", unsafe_allow_html=True)

            with st.expander("✉️ Generate Follow-up Email"):
                open_tasks = person_tasks[person_tasks['Status'] == 'Open']
                tasks_list = "\n".join(
                    [f"• {row['Description']} (Due: {row['Due Date']})" for _, row in open_tasks.iterrows()]
                )
                email_draft = f"""Subject: Quick check-in on your action items

Hi {owner},

Hope you're doing well! Could you share a quick update on these items from our recent syncs?

{tasks_list}

Let me know if you need any help or if priorities have shifted.

Thanks!"""
                st.text_area("Draft", email_draft, height=220)
            st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: LOG ---
with tab_meetings:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📅</div>
        <div>
            <div class="section-title">Meeting Log</div>
            <div class="section-subtitle">Decisions and risks by meeting</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.db_meetings:
        st.info("No meeting history yet. Process a meeting to start the log.")
    else:
        for m in reversed(st.session_state.db_meetings):
            with st.expander(f"📅 {m['Date']} · **{m['Name']}** ({m['Type']})"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**✅ Decisions Made**")
                    if m['Decisions']:
                        for d in m['Decisions']:
                            st.success(f"✓ {d}")
                    else:
                        st.caption("No decisions recorded.")
                with c2:
                    st.markdown("**⚠️ Risks Identified**")
                    if m['Risks']:
                        for r in m['Risks']:
                            st.error(f"⚠ {r}")
                    else:
                        st.caption("No risks identified.")
