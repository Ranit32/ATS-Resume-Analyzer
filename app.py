"""
ATS Resume Checker — Streamlit App
A 4-step wizard to analyze how well your resume matches a job description.
"""
import os

import streamlit as st
from dotenv import load_dotenv

from utils.ats_analyzer import analyze_resume, generate_pdf_report
from utils.resume_parser import extract_resume_text
from utils.styles import STYLES

# ── Load env ───────────────────────────────────────────────────────────────────
load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ATS Resume Checker",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(STYLES, unsafe_allow_html=True)

# ── Session state defaults ─────────────────────────────────────────────────────
defaults = {
    "step": 1,
    "job_role": "",
    "job_description": "",
    "resume_text": "",
    "analysis": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

QUICK_ROLES = [
    "Software Engineer",
    "Data Analyst",
    "Product Manager",
    "UX Designer",
    "Marketing Manager",
]

SECTION_COLORS = {
    "keywords_match":   ("#6c63ff", "#8b5cf6"),
    "skills_alignment": ("#10b981", "#34d399"),
    "experience_match": ("#f59e0b", "#fbbf24"),
    "education_match":  ("#3b82f6", "#60a5fa"),
    "format_structure": ("#ec4899", "#f472b6"),
}


# ── Helpers ────────────────────────────────────────────────────────────────────
def score_color(score: int) -> str:
    if score >= 75:
        return "#10b981"
    elif score >= 50:
        return "#f59e0b"
    return "#ef4444"


def score_gauge_html(score: int) -> str:
    color = score_color(score)
    circumference = 2 * 3.14159 * 54
    dash = circumference * score / 100
    gap = circumference - dash
    label = (
        "Excellent" if score >= 85 else
        "Good"      if score >= 70 else
        "Fair"      if score >= 50 else
        "Needs Work"
    )
    return f"""
<div style="display:flex;flex-direction:column;align-items:center;padding:1.2rem 0;">
  <div style="position:relative;width:160px;height:160px;">
    <svg width="160" height="160" viewBox="0 0 120 120">
      <circle cx="60" cy="60" r="54" fill="none" stroke="#1e293b" stroke-width="10"/>
      <circle cx="60" cy="60" r="54" fill="none" stroke="{color}" stroke-width="10"
        stroke-dasharray="{dash:.1f} {gap:.1f}"
        stroke-dashoffset="{circumference/4:.1f}"
        stroke-linecap="round"/>
    </svg>
    <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                text-align:center;line-height:1.2;">
      <div style="font-size:2.2rem;font-weight:800;color:{color};">{score}</div>
      <div style="font-size:0.65rem;color:#64748b;text-transform:uppercase;
                  letter-spacing:.08em;">/ 100</div>
    </div>
  </div>
  <div style="margin-top:.6rem;font-size:.85rem;font-weight:600;color:{color};">{label}</div>
  <div style="font-size:.75rem;color:#64748b;margin-top:.1rem;">ATS Score</div>
</div>
"""


def section_bar_html(label: str, score: int, colors: tuple) -> str:
    c1, c2 = colors
    color_val = score_color(score)
    return f"""
<div class="section-score-row">
  <div class="section-score-label">
    <span>{label}</span>
    <span style="color:{color_val};font-weight:600;">{score}%</span>
  </div>
  <div class="section-score-bar-bg">
    <div class="section-score-bar-fill"
         style="width:{score}%;background:linear-gradient(90deg,{c1},{c2});"></div>
  </div>
</div>
"""


def render_step_bar(current: int):
    steps = ["Job role", "Job description", "Your resume", "Results"]
    html = '<div class="step-bar">'
    for i, label in enumerate(steps, 1):
        if i < current:
            circle_cls, label_cls, icon = "done", "done", "✓"
        elif i == current:
            circle_cls, label_cls, icon = "active", "active", str(i)
        else:
            circle_cls, label_cls, icon = "", "", str(i)

        html += f"""
        <div class="step-item">
          <div class="step-circle {circle_cls}">{icon}</div>
          <span class="step-label {label_cls}">{label}</span>
        </div>"""

        if i < len(steps):
            conn_cls = "done" if i < current else ""
            html += f'<div class="step-connector {conn_cls}"></div>'

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="app-header">
      <h1>📄 ATS Resume Checker</h1>
      <p>Find out how well your resume matches a job — before you apply.</p>
    </div>
    """, unsafe_allow_html=True)


def card_title(icon: str, text: str):
    st.markdown(
        f'<div class="card-title">{icon} {text}</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — Job Role
# ══════════════════════════════════════════════════════════════════════════════
def step_job_role():
    render_header()
    render_step_bar(1)

    # ── Chip pre-seed: must happen BEFORE st.text_input is instantiated ────────
    # Streamlit forbids writing to a widget's key after the widget renders.
    # Pattern: store chip value in "_chip_pending", consume it here next run.
    if "_chip_pending" in st.session_state:
        st.session_state.role_input = st.session_state.pop("_chip_pending")

    with st.container(border=True):
        card_title("🗂", "JOB ROLE")

        role = st.text_input(
            "Job role",
            placeholder="e.g. Senior Data Scientist",
            label_visibility="collapsed",
            key="role_input",
        )
        st.session_state.job_role = role  # widget is source of truth

        st.markdown('<div style="height:.4rem"></div>', unsafe_allow_html=True)
        cols = st.columns(len(QUICK_ROLES))
        for col, qr in zip(cols, QUICK_ROLES):
            with col:
                if st.button(qr, key=f"chip_{qr}", use_container_width=True):
                    st.session_state._chip_pending = qr
                    st.rerun()

    st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)

    if st.button(
        "Continue →",
        disabled=not st.session_state.job_role.strip(),
        use_container_width=True,
        key="step1_continue",
        type="primary",
    ):
        st.session_state.step = 2
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — Job Description
# ══════════════════════════════════════════════════════════════════════════════
def step_job_description():
    render_header()
    render_step_bar(2)

    with st.container(border=True):
        card_title("📋", "JOB DESCRIPTION")

        jd = st.text_area(
            "Job description",
            value=st.session_state.job_description,
            placeholder="Paste the full job description here — requirements, responsibilities, skills…",
            height=220,
            label_visibility="collapsed",
            key="jd_input",
        )
        st.session_state.job_description = jd

        st.markdown(
            f'<div class="char-counter">{len(jd):,} characters</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)

    col_back, col_cont = st.columns([1, 3])
    with col_back:
        if st.button("← Back", key="step2_back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with col_cont:
        if st.button(
            "Continue →",
            disabled=not jd.strip(),
            key="step2_continue",
            use_container_width=True,
            type="primary",
        ):
            st.session_state.step = 3
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — Resume Upload
# ══════════════════════════════════════════════════════════════════════════════
def step_resume_upload():
    render_header()
    render_step_bar(3)

    with st.container(border=True):
        card_title("⬆", "UPLOAD RESUME")

        uploaded_file = st.file_uploader(
            "Upload resume (PDF or DOCX · max 5 MB)",
            type=["pdf", "docx"],
            label_visibility="collapsed",
            key="file_uploader",
        )

        resume_text_from_file = ""
        if uploaded_file is not None:
            if uploaded_file.size > 5 * 1024 * 1024:
                st.error("❌ File exceeds 5 MB limit. Please upload a smaller file.")
            else:
                with st.spinner("Extracting text from file…"):
                    try:
                        resume_text_from_file = extract_resume_text(uploaded_file)
                        st.success(
                            f"✅ Extracted {len(resume_text_from_file):,} characters "
                            f"from **{uploaded_file.name}**"
                        )
                    except Exception as e:
                        st.error(f"❌ Could not read file: {e}")

        st.markdown(
            '<div class="or-divider">or paste as text</div>',
            unsafe_allow_html=True,
        )

        pasted = st.text_area(
            "Paste resume text",
            value=st.session_state.resume_text if not resume_text_from_file else "",
            placeholder="Paste your resume content here instead…",
            height=180,
            label_visibility="collapsed",
            key="paste_input",
        )

        final_resume = resume_text_from_file or pasted
        st.session_state.resume_text = final_resume

        st.markdown(
            f'<div class="char-counter">{len(final_resume):,} characters</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)

    col_back, col_analyze = st.columns([1, 3])
    with col_back:
        if st.button("← Back", key="step3_back", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    with col_analyze:
        if st.button(
            "🔍 Analyze Resume",
            disabled=not final_resume.strip(),
            key="step3_analyze",
            use_container_width=True,
            type="primary",
        ):
            api_key = os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                st.error(
                    "⚠️ **GEMINI_API_KEY not set.**\n\n"
                    "Create a `.env` file:\n```\nGEMINI_API_KEY=your_key_here\n```"
                )
            else:
                with st.spinner("🤖 Analyzing your resume with Gemini AI…"):
                    try:
                        result = analyze_resume(
                            job_role=st.session_state.job_role,
                            job_description=st.session_state.job_description,
                            resume_text=final_resume,
                        )
                        st.session_state.analysis = result
                        st.session_state.step = 4
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  STEP 4 — Results
# ══════════════════════════════════════════════════════════════════════════════
def step_results():
    render_header()
    render_step_bar(4)

    analysis = st.session_state.analysis
    if not analysis:
        st.error("No analysis results found. Please go back and try again.")
        if st.button("← Start Over"):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()
        return

    overall        = analysis["overall_score"]
    section_scores = analysis["section_scores"]
    matched        = analysis.get("matched_keywords", [])
    missing        = analysis.get("missing_keywords", [])
    improvements   = analysis.get("improvements", [])
    strengths      = analysis.get("strengths", [])
    summary        = analysis.get("summary", "")

    # ── Score gauge + summary ──────────────────────────────────────────────────
    col_gauge, col_summary = st.columns([1, 2])

    with col_gauge:
        with st.container(border=True):
            st.markdown(score_gauge_html(overall), unsafe_allow_html=True)

    with col_summary:
        with st.container(border=True):
            card_title("📊", "EXECUTIVE SUMMARY")
            st.markdown(
                f'<p style="color:#cbd5e1;font-size:.92rem;line-height:1.6;'
                f'margin-bottom:1rem;">{summary}</p>',
                unsafe_allow_html=True,
            )
            section_labels = {
                "keywords_match":   "Keywords Match",
                "skills_alignment": "Skills Alignment",
                "experience_match": "Experience Match",
                "education_match":  "Education Match",
                "format_structure": "Format & Structure",
            }
            bars_html = ""
            for key, label in section_labels.items():
                score  = section_scores.get(key, 0)
                colors = SECTION_COLORS.get(key, ("#6c63ff", "#8b5cf6"))
                bars_html += section_bar_html(label, score, colors)
            st.markdown(bars_html, unsafe_allow_html=True)

    # ── Keywords ───────────────────────────────────────────────────────────────
    col_match, col_miss = st.columns(2)

    with col_match:
        with st.container(border=True):
            st.markdown(
                f'<div class="card-title">✅ Matched Keywords '
                f'<span style="color:#10b981;margin-left:.4rem;">({len(matched)})</span></div>',
                unsafe_allow_html=True,
            )
            if matched:
                tags = "".join(f'<span class="tag match">{kw}</span>' for kw in matched)
                st.markdown(f'<div class="tag-row">{tags}</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<p style="color:#4a5568;font-size:.85rem;">No matched keywords found.</p>',
                    unsafe_allow_html=True,
                )

    with col_miss:
        with st.container(border=True):
            st.markdown(
                f'<div class="card-title">❌ Missing Keywords '
                f'<span style="color:#ef4444;margin-left:.4rem;">({len(missing)})</span></div>',
                unsafe_allow_html=True,
            )
            if missing:
                tags = "".join(f'<span class="tag missing">{kw}</span>' for kw in missing)
                st.markdown(f'<div class="tag-row">{tags}</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<p style="color:#4a5568;font-size:.85rem;">Great — no missing keywords!</p>',
                    unsafe_allow_html=True,
                )

    # ── Strengths ──────────────────────────────────────────────────────────────
    if strengths:
        with st.container(border=True):
            card_title("💪", "STRENGTHS")
            items_html = "".join(
                f'<div class="strength-item">'
                f'<span class="strength-icon">✓</span>{s}</div>'
                for s in strengths
            )
            st.markdown(items_html, unsafe_allow_html=True)

    # ── Improvements ───────────────────────────────────────────────────────────
    with st.container(border=True):
        card_title("🚀", "IMPROVEMENT SUGGESTIONS")
        items_html = "".join(
            f'<div class="improvement-item">'
            f'<div class="improvement-num">{i}</div>'
            f'<div>{tip}</div></div>'
            for i, tip in enumerate(improvements, 1)
        )
        st.markdown(items_html, unsafe_allow_html=True)

    # ── Action buttons ─────────────────────────────────────────────────────────
    st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)
    col_dl, col_restart = st.columns(2)

    with col_dl:
        pdf_bytes = generate_pdf_report(
            job_role=st.session_state.job_role,
            analysis=analysis,
        )
        st.download_button(
            label="⬇ Download PDF Report",
            data=pdf_bytes,
            file_name=f"ats_report_{st.session_state.job_role.replace(' ', '_').lower()}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_report",
        )

    with col_restart:
        if st.button("🔄 Start Over", use_container_width=True, key="restart"):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════
STEPS = {
    1: step_job_role,
    2: step_job_description,
    3: step_resume_upload,
    4: step_results,
}

STEPS[st.session_state.step]()
