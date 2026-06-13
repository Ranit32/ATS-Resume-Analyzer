"""
Custom CSS for the ATS Resume Checker Streamlit app.
"""

STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── Animated background ── */
.stApp {
    background: #0f0f1a;
    min-height: 100vh;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 55% 45% at 10% 10%, rgba(108,99,255,0.22) 0%, transparent 65%),
        radial-gradient(ellipse 45% 55% at 90% 90%, rgba(139,92,246,0.16) 0%, transparent 65%),
        radial-gradient(ellipse 40% 40% at 80% 10%, rgba(16,185,129,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 35% 35% at 20% 85%, rgba(59,130,246,0.07) 0%, transparent 60%);
    animation: bgOrbs 14s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}
@keyframes bgOrbs {
    0%   { opacity: 1;   transform: scale(1) translateX(0px);   }
    33%  { opacity: 0.8; transform: scale(1.04) translateX(8px); }
    66%  { opacity: 0.9; transform: scale(0.97) translateX(-5px); }
    100% { opacity: 1;   transform: scale(1.02) translateX(4px); }
}

/* Ensure content sits above background */
.stMainBlockContainer {
    position: relative;
    z-index: 1;
}

/* ── App header ── */
.app-header {
    padding: 1.5rem 0 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 1.5rem;
}
.app-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.2rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.app-header p {
    color: #94a3b8;
    font-size: 0.95rem;
    margin: 0;
}

/* ── Step Progress Bar ── */
.step-bar {
    display: flex;
    align-items: center;
    margin: 1.2rem 0 2rem 0;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    flex-shrink: 0;
}
.step-circle {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
    flex-shrink: 0;
    border: 2px solid #2d3748;
    color: #4a5568;
    background: transparent;
    transition: all 0.3s;
}
.step-circle.active {
    background: linear-gradient(135deg, #6c63ff, #8b5cf6);
    border-color: transparent;
    color: white;
    box-shadow: 0 0 18px rgba(108,99,255,0.5);
}
.step-circle.done {
    background: #10b981;
    border-color: #10b981;
    color: white;
}
.step-label {
    font-size: 0.8rem;
    font-weight: 500;
    color: #4a5568;
    white-space: nowrap;
}
.step-label.active { color: #f1f5f9; font-weight: 600; }
.step-label.done   { color: #10b981; }
.step-connector {
    flex: 1;
    height: 2px;
    background: #1e293b;
    margin: 0 0.5rem;
    min-width: 16px;
    border-radius: 2px;
}
.step-connector.done { background: linear-gradient(90deg, #10b981, #059669); }

/* ── Cards (native Streamlit bordered containers) ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(20, 25, 40, 0.85) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 16px !important;
    padding: 1.4rem 1.6rem !important;
    margin-bottom: 0.8rem !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3) !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(108,99,255,0.2) !important;
    transition: border-color 0.3s ease !important;
}

/* ── Card title ── */
.card-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #6c63ff;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(15,15,26,0.8) !important;
    border: 1.5px solid #2d3748 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.18) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #334155 !important;
}

/* ── Hide "Press Enter / Ctrl+Enter to apply" hints ── */
[data-testid="InputInstructions"],
.stTextInput small,
.stTextArea small {
    display: none !important;
}

/* ── Pills (st.pills quick-select chips) ── */
[data-testid="stPills"] {
    margin-top: 0.6rem;
}
[data-testid="stPills"] button {
    background: rgba(108,99,255,0.08) !important;
    border: 1.5px solid rgba(108,99,255,0.25) !important;
    border-radius: 999px !important;
    color: #a78bfa !important;
    font-size: 0.82rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.3rem 0.9rem !important;
    transition: all 0.2s !important;
    white-space: nowrap !important;
}
[data-testid="stPills"] button:hover {
    background: rgba(108,99,255,0.2) !important;
    border-color: #6c63ff !important;
    color: #c4b5fd !important;
    transform: translateY(-1px) !important;
}
[data-testid="stPills"] button[aria-checked="true"],
[data-testid="stPills"] button[aria-pressed="true"],
[data-testid="stPills"] button[data-selected="true"] {
    background: linear-gradient(135deg, #6c63ff, #8b5cf6) !important;
    border-color: transparent !important;
    color: white !important;
    box-shadow: 0 3px 12px rgba(108,99,255,0.4) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(15,15,26,0.6) !important;
    border: 2px dashed #2d3748 !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6c63ff !important;
}

/* ── Primary / Secondary buttons ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #6c63ff, #8b5cf6) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(108,99,255,0.35) !important;
}
.stButton > button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(108,99,255,0.45) !important;
}
.stButton > button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    background: rgba(26,31,46,0.8) !important;
    border: 1.5px solid #2d3748 !important;
    color: #94a3b8 !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #6c63ff !important;
    color: #c4b5fd !important;
}
.stDownloadButton > button {
    background: rgba(16,185,129,0.1) !important;
    border: 1.5px solid rgba(16,185,129,0.35) !important;
    border-radius: 10px !important;
    color: #34d399 !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(16,185,129,0.2) !important;
    transform: translateY(-1px) !important;
}

/* ── Char counter ── */
.char-counter {
    text-align: right;
    font-size: 0.75rem;
    color: #334155;
    margin-top: 0.3rem;
}

/* ── OR divider ── */
.or-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.2rem 0;
    color: #334155;
    font-size: 0.82rem;
    font-style: italic;
}
.or-divider::before, .or-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e293b;
}

/* ── Results: score gauge ── */
.score-gauge-outer {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem 0 0.5rem;
}

/* ── Results: section score rows ── */
.section-score-row { margin: 0.55rem 0; }
.section-score-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    margin-bottom: 0.28rem;
    color: #cbd5e1;
    font-family: 'Inter', sans-serif;
}
.section-score-bar-bg {
    height: 7px;
    background: #1e293b;
    border-radius: 99px;
    overflow: hidden;
}
.section-score-bar-fill {
    height: 100%;
    border-radius: 99px;
}

/* ── Results: keyword tags ── */
.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-top: 0.5rem;
    line-height: 1;
}
.tag {
    padding: 0.22rem 0.7rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    display: inline-block;
}
.tag.match {
    background: rgba(16,185,129,0.14);
    color: #34d399;
    border: 1px solid rgba(16,185,129,0.3);
}
.tag.missing {
    background: rgba(239,68,68,0.12);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.25);
}

/* ── Results: strength items ── */
.strength-item {
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.9rem;
    color: #a7f3d0;
    font-family: 'Inter', sans-serif;
    line-height: 1.5;
}
.strength-icon { color: #10b981; flex-shrink: 0; margin-top: 1px; }

/* ── Results: improvement items ── */
.improvement-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.7rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.88rem;
    color: #cbd5e1;
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
}
.improvement-item:last-child { border-bottom: none; }
.improvement-num {
    min-width: 24px;
    height: 24px;
    border-radius: 50%;
    background: rgba(108,99,255,0.18);
    color: #a78bfa;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
    font-family: 'Inter', sans-serif;
}

/* ── Spinner override ── */
.stSpinner > div { border-top-color: #6c63ff !important; }

/* ── Selectbox / dropdown ── */
.stSelectbox > div > div {
    background: rgba(15,15,26,0.8) !important;
    border-color: #2d3748 !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}

/* ── Success / Error / Warning messages ── */
.stSuccess, [data-testid="stSuccess"] {
    background: rgba(16,185,129,0.1) !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-radius: 10px !important;
    color: #a7f3d0 !important;
}
.stError, [data-testid="stError"] {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: 10px !important;
}
</style>
"""
