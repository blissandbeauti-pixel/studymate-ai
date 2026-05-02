# ============================================
# StudyMate AI - Web Application v6.0
# With Sidebar, Credits, 200 MCQs Support
# ============================================

import streamlit as st
import ollama
import re
import random
from datetime import datetime
from auth import show_auth_page
from database import (
    initialize_database,
    get_user_stats,
    get_user_history,
    get_user_assessments,
    save_mcq_history,
    save_assessment,
    save_suggestion
)
from notes_generator import generate_notes, solve_question
from pdf_generator import generate_pdf
from dotenv import load_dotenv
# Load local .env file first (for development)
load_dotenv()

# ── Load secrets for cloud deployment ──
import os
try:
    os.environ["AI_BACKEND"] = st.secrets.get("AI_BACKEND", "ollama")
    os.environ["GROQ_API_KEY"] = st.secrets.get("GROQ_API_KEY", "")
    os.environ["GROQ_MODEL"] = st.secrets.get("GROQ_MODEL", "llama-3.1-8b-instant")
    os.environ["GEMINI_API_KEY"] = st.secrets.get("GEMINI_API_KEY", "")
    os.environ["APP_URL"] = st.secrets.get("APP_URL", "http://localhost:8501")
except Exception:
    pass

from admin import show_admin_page
from student_features import (
    show_exam_countdown,
    show_progress_charts,
    show_past_papers_student
)
from support_page import show_support_page
from community import show_community_page
from auth import show_change_password
from terms import show_terms_page
from student_features import (
    show_exam_countdown,
    show_progress_charts,
    show_past_papers_student,
    show_admin_notes_student
)

# ============================================
# INITIALIZE DATABASE
# ============================================

initialize_database()

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="StudyMate AI — Pakistani Students",
    page_icon="📚",
    layout="wide"  # Wide layout for sidebar
)

# ============================================
# STYLING
# ============================================

st.markdown("""
<style>
    /* MCQ Card */
    .mcq-card {
        background: white;
        border-radius: 12px;
        padding: 20px 25px;
        margin: 15px 0;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .question-text {
        font-size: 17px;
        font-weight: 600;
        color: #1a1a2e;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    .option {
        font-size: 15px;
        color: #444;
        padding: 6px 10px;
        margin: 3px 0;
        border-radius: 6px;
        background: #f1f3f4;
    }
    .correct-answer {
        font-size: 15px;
        font-weight: 600;
        color: #2e7d32;
        background: #e8f5e9;
        padding: 8px 12px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .explanation {
        font-size: 14px;
        color: #1565c0;
        background: #e3f2fd;
        padding: 8px 12px;
        border-radius: 8px;
        margin-top: 6px;
    }
    .keynote {
        font-size: 14px;
        color: #6a1b9a;
        background: #f3e5f5;
        padding: 8px 12px;
        border-radius: 8px;
        margin-top: 6px;
    }
    .examtip {
        font-size: 14px;
        color: #e65100;
        background: #fff3e0;
        padding: 8px 12px;
        border-radius: 8px;
        margin-top: 6px;
    }
    .info-box {
        background: #e8f4fd;
        border-radius: 10px;
        padding: 15px 20px;
        margin: 10px 0;
        border-left: 4px solid #1976d2;
        line-height: 1.8;
    }
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .history-card {
        background: white;
        border-radius: 10px;
        padding: 15px 20px;
        margin: 8px 0;
        border-left: 4px solid #1976d2;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        line-height: 1.8;
    }
    .tip-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        font-size: 14px;
        line-height: 1.6;
    }
    .credit-box {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
    }
    .warning-box {
        background: #fff8e1;
        border-left: 4px solid #ffc107;
        border-radius: 8px;
        padding: 10px 15px;
        font-size: 13px;
        color: #555;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# STUDY TIPS (Random Daily Tip)
# ============================================

STUDY_TIPS = [
    "📖 Study in 25-min sessions with 5-min breaks (Pomodoro Technique).",
    "✍️ Writing notes by hand improves memory retention by 40%.",
    "🔄 Revise topics within 24 hours of learning to retain 80% more.",
    "❓ Testing yourself is more effective than re-reading notes.",
    "🌙 Sleep consolidates memory — study, then sleep, then review.",
    "🗺️ Create mind maps to connect concepts visually.",
    "📊 For MDCAT: Focus on Biology (38%), Chemistry (30%), Physics (22%).",
    "⚡ For ECAT: Mathematics and Physics carry the highest weightage.",
    "🎯 Attempt past papers in real exam conditions for best preparation.",
    "💧 Stay hydrated — dehydration reduces concentration by 13%.",
    "🏃 Exercise improves brain function — take short walks during breaks.",
    "📱 Put your phone away while studying — it reduces focus significantly.",
    "🔑 Understanding concepts beats memorizing — ask 'why' not just 'what'.",
    "📝 For BSN: Clinical application MCQs are most common in exams.",
    "⏰ Morning study is most effective for analytical subjects like Math.",
]

USEFUL_LINKS = {
    "📄 Past Papers": [
        ("Federal Board Past Papers", "https://fbise.edu.pk"),
        ("PastPapers.pk", "https://www.pastpapers.pk"),
        ("Ilmkidunya Papers", "https://www.ilmkidunya.com/papers"),
    ],
    "📚 Study Resources": [
        ("HEC Digital Library", "https://digitallibrary.hec.gov.pk"),
        ("Virtual University", "https://www.vu.edu.pk"),
        ("Khan Academy", "https://www.khanacademy.org"),
    ],
    "🏥 Medical Entry Tests": [
        ("MDCAT Official (PMC)", "https://www.pmcpakistan.org"),
        ("NUMS Official", "https://www.nums.edu.pk"),
        ("Aga Khan Admissions", "https://www.aku.edu"),
    ],
    "⚙️ Engineering Entry Tests": [
        ("NUST NET Info", "https://admission.nust.edu.pk"),
        ("UET Lahore", "https://www.uet.edu.pk"),
        ("ECAT Preparation", "https://www.ecat.net.pk"),
    ],
    "🏛️ Pakistani Universities": [
        ("HEC University Rankings", "https://www.hec.gov.pk"),
        ("COMSATS University", "https://www.comsats.edu.pk"),
        ("Punjab University", "https://www.pu.edu.pk"),
    ]
}

# ============================================
# DATA
# ============================================

BOARDS = [
    "Federal Board (FBISE)",
    "BISE Lahore", "BISE Rawalpindi", "BISE Gujranwala",
    "BISE Faisalabad", "BISE Multan", "BISE Sahiwal",
    "BISE Sargodha", "BISE DG Khan", "BISE Bahawalpur",
    "BISE Karachi", "BISE Hyderabad", "BISE Sukkur",
    "BISE Peshawar", "BISE Mardan", "BISE Abbottabad",
    "BISE Swat", "BISE Mirpur (AJK)", "BISE Muzaffarabad (AJK)",
    "Other Board"
]

UNIVERSITIES = [
    "General / Any University",
    "── Medical ──",
    "NUMS", "Dow University", "King Edward Medical University (KEMU)",
    "Aga Khan University", "Allama Iqbal Medical College",
    "Rawalpindi Medical University (RMU)", "Army Medical College",
    "── Engineering ──",
    "NUST", "UET Lahore", "UET Peshawar",
    "COMSATS University", "NED University", "PIEAS",
    "── General ──",
    "Punjab University (PU)", "University of Karachi",
    "Quaid-i-Azam University (QAU)", "University of Peshawar",
    "FAST-NUCES", "Bahria University", "Air University",
    "Virtual University (VU)", "Other University"
]

ENTRY_TESTS = [
    "MDCAT (Medical Colleges)", "ECAT (Engineering Colleges)",
    "NUMS Test (Military Medical)", "NET (NUST Entry Test)",
    "Aga Khan Entry Test", "FAST Entry Test (NUCES)",
    "COMSATS Entry Test", "UET Entry Test",
    "NTS Based Test", "Other Entry Test"
]

PROGRAMS = [
    "── Medical / Health ──",
    "BSN Nursing (Generic)", "BSN Nursing (Post RN)",
    "MBBS", "BDS (Dentistry)", "Pharm-D",
    "DPT (Physiotherapy)", "MLT (Medical Lab Technology)",
    "── Engineering ──",
    "DAE Civil Engineering", "DAE Electrical Engineering",
    "DAE Mechanical Engineering", "DAE Computer Information Technology",
    "DAE Electronics", "BE/BSc Civil Engineering",
    "BE/BSc Electrical Engineering", "BE/BSc Mechanical Engineering",
    "BS Computer Science", "BS Software Engineering",
    "── Science ──",
    "FSc Pre-Medical", "FSc Pre-Engineering",
    "BSc Physics", "BSc Chemistry", "BSc Biology", "BSc Mathematics",
    "── General ──",
    "BA/BSc General", "BBA / MBA", "BS English", "Other Program"
]

YEARS = [
    "1st Year / Semester 1", "1st Year / Semester 2",
    "2nd Year / Semester 3", "2nd Year / Semester 4",
    "3rd Year / Semester 5", "3rd Year / Semester 6",
    "4th Year / Semester 7", "4th Year / Semester 8",
    "Not Applicable"
]

# MCQ count options
REGULAR_MCQ_OPTIONS = [5, 10, 15, 20, 25, 30, 50]
ENTRY_TEST_MCQ_OPTIONS = [
    5, 10, 15, 20, 25, 30, 40, 50,
    75, 100, 150, 200
]

# ============================================
# SESSION STATE INIT
# ============================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "current_mcqs" not in st.session_state:
    st.session_state.current_mcqs = None
if "current_meta" not in st.session_state:
    st.session_state.current_meta = None
if "parsed_mcqs" not in st.session_state:
    st.session_state.parsed_mcqs = []
if "daily_tip" not in st.session_state:
    st.session_state.daily_tip = random.choice(STUDY_TIPS)


# ============================================
# SIDEBAR
# ============================================

def show_sidebar():
    with st.sidebar:

        # ── Branding ──
        st.markdown("""
        <div style='text-align:center; padding:10px 0'>
            <h2>📚 StudyMate AI</h2>
            <p style='color:gray; font-size:13px'>
                Smart Study Companion<br>for Pakistani Students
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        # ── App Stats ──
        # stats = get_app_stats()
        # st.markdown("### 📊 App Stats")
        # col1, col2 = st.columns(2)
        # with col1:
            # st.metric("👥 Students", stats["total_users"])
            # st.metric("📖 Sessions", stats["total_sessions"])
        # with col2:
            # st.metric("❓ MCQs", f"{stats['total_mcqs']:,}")
            # st.metric("📝 Tests", stats["total_tests"])

        # st.divider()

                # ── Daily Tip ──
        st.markdown("### 💡 Study Tip of the Day")
        st.markdown(f"""
        <div class="tip-box">{st.session_state.daily_tip}</div>
        """, unsafe_allow_html=True)
        if st.button("🔄 New Tip", use_container_width=True):
            st.session_state.daily_tip = random.choice(STUDY_TIPS)
            st.rerun()

        st.divider()

        
        # ── Suggestion Box ──
        st.markdown("### 💬 Suggestion Box")
        st.markdown(
            "<small>Help us improve StudyMate AI!</small>",
            unsafe_allow_html=True
        )
        suggestion_category = st.selectbox(
            "Category",
            [
                "New Feature Request", "Bug Report",
                "Content Suggestion", "University/Board to Add",
                "Program to Add", "General Feedback"
            ],
            key="suggestion_cat"
        )
        suggestion_text = st.text_area(
            "Your Suggestion",
            placeholder="Share your idea or feedback...",
            key="suggestion_text", height=80
        )
        if st.button("📨 Send Suggestion", use_container_width=True):
            if suggestion_text.strip():
                user_name = (
                    st.session_state.user["full_name"]
                    if st.session_state.logged_in else "Anonymous"
                )
                if save_suggestion(user_name, suggestion_category, suggestion_text):
                    st.success("✅ Thank you! Received.")
                else:
                    st.error("❌ Could not save.")
            else:
                st.warning("⚠️ Please write something.")

        st.divider()

        # ── Useful Links ──
        st.markdown("### 🔗 Useful Links")
        for category, links in USEFUL_LINKS.items():
            with st.expander(category):
                for name, url in links:
                    st.markdown(f"[{name}]({url})")

        st.divider()

        # ── Settings ──
        if st.session_state.logged_in:
            st.divider()
            with st.expander("⚙️ Account Settings"):
                show_change_password(
                    st.session_state.user["id"]
                )

        # ── Admin Access ──
        st.write("")
        with st.expander("🔐 Admin Access"):
            if st.button(
                "🛡️ Open Admin Panel",
                use_container_width=True
            ):
                st.session_state.show_admin = True
                st.rerun()
        
        st.divider()

        # ── Developer Credit ──
        st.markdown("""
        <div style='text-align:center; font-size:11px;
        color:gray; line-height:1.8; padding:5px 0'>
            📚 <b>StudyMate AI v8.0</b><br>
            Developed by <b>Aftab Ahmed</b> 🇵🇰<br>
            Built with ❤️ for Pakistani Students<br>
            © 2025 All Rights Reserved
        </div>
        """, unsafe_allow_html=True)

# ============================================
# MCQ PARSER & RENDERER
# ============================================

def parse_mcqs(raw_text):
    questions = re.split(r'\n(?=Q\d+[\.\)])', raw_text.strip())
    parsed = []
    for q_block in questions:
        if not q_block.strip() or not re.match(r'Q\d+', q_block.strip()):
            continue
        lines = q_block.strip().split('\n')
        mcq = {
            "question": "", "options": [], "correct": "",
            "explanation": "", "keynote": "", "examtip": ""
        }
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if re.match(r'Q\d+[\.\)]', line):
                mcq["question"] = re.sub(r'^Q\d+[\.\)]\s*', '', line)
            elif re.match(r'^[A-D][\.\)]\s', line):
                mcq["options"].append(line)
            elif '✅' in line or line.lower().startswith('correct answer'):
                mcq["correct"] = re.sub(
                    r'(✅\s*Correct Answer\s*:|Correct Answer\s*:)',
                    '', line, flags=re.IGNORECASE).strip()
            elif '📝' in line or line.lower().startswith('explanation'):
                mcq["explanation"] = re.sub(
                    r'(📝\s*Explanation\s*:|Explanation\s*:)',
                    '', line, flags=re.IGNORECASE).strip()
            elif '🔑' in line or line.lower().startswith('key note'):
                mcq["keynote"] = re.sub(
                    r'(🔑\s*Key Note\s*:|Key Note\s*:)',
                    '', line, flags=re.IGNORECASE).strip()
            elif '⚡' in line or line.lower().startswith('exam tip'):
                mcq["examtip"] = re.sub(
                    r'(⚡\s*Exam Tip\s*:|Exam Tip\s*:)',
                    '', line, flags=re.IGNORECASE).strip()
        if mcq["question"] and mcq["options"]:
            parsed.append(mcq)
    return parsed


def render_mcq_card(mcq, index, show_answer=True, border_color="#4CAF50"):
    options_html = "".join(
        [f'<div class="option">{opt}</div>' for opt in mcq["options"]]
    )
    correct_html = (
        f'<div class="correct-answer">✅ Correct: {mcq["correct"]}</div>'
        if show_answer and mcq["correct"] else ""
    )
    explanation_html = (
        f'<div class="explanation">📝 <b>Explanation:</b> {mcq["explanation"]}</div>'
        if show_answer and mcq["explanation"] else ""
    )
    keynote_html = (
        f'<div class="keynote">🔑 <b>Key Note:</b> {mcq["keynote"]}</div>'
        if show_answer and mcq["keynote"] else ""
    )
    examtip_html = (
        f'<div class="examtip">⚡ <b>Exam Tip:</b> {mcq["examtip"]}</div>'
        if show_answer and mcq["examtip"] else ""
    )
    st.markdown(f"""
    <div class="mcq-card" style="border-left-color:{border_color}">
        <div class="question-text">Q{index}. {mcq["question"]}</div>
        {options_html}
        {correct_html}
        {explanation_html}
        {keynote_html}
        {examtip_html}
    </div>
    """, unsafe_allow_html=True)


# ============================================
# GENERATE MCQs
# ============================================

def generate_mcqs(exam_mode, program, year, institution,
                  subject, topic, num_questions, difficulty):
    from ai_backend import chat

    if num_questions > 10:
        return generate_mcqs_in_batches(
            exam_mode, program, year, institution,
            subject, topic, num_questions, difficulty
        )

    if exam_mode == "Entry Test Preparation":
        prompt = f"""Generate exactly {num_questions} MCQs for {institution} entry test.
Subject: {subject} | Topic: {topic} | Difficulty: {difficulty}

Format each MCQ exactly as:
Q1. [Question]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Correct Answer: [Letter]) [Answer]
Explanation: [three sentence]
Key Note: [One point]
Exam Tip: [One tip]
---"""

    else:
        prompt = f"""Generate exactly {num_questions} MCQs for {program} students.
Subject: {subject} | Topic: {topic} | Difficulty: {difficulty}
Institution: {institution} | Year: {year}

Format each MCQ exactly as:
Q1. [Question]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Correct Answer: [Letter]) [Answer]
Explanation: [three sentence]
Key Note: [One point]
---"""

    try:
        result = chat(prompt)
        if not result or "Error" in result[:20]:
            return None
        return result
    except Exception as e:
        print(f"MCQ Error: {e}")
        return None


def generate_mcqs_in_batches(exam_mode, program, year, institution,
                              subject, topic, num_questions, difficulty):
    from ai_backend import chat
    import time

    BATCH_SIZE    = 10
    all_content   = []
    q_counter     = 1
    total_batches = (num_questions + BATCH_SIZE - 1) // BATCH_SIZE

    progress = st.progress(0, text="Starting...")

    for batch_num in range(total_batches):
        remaining     = num_questions - (batch_num * BATCH_SIZE)
        current_batch = min(BATCH_SIZE, remaining)

        progress.progress(
            batch_num / total_batches,
            text=f"⏳ Batch {batch_num+1}/{total_batches} — generating {current_batch} MCQs..."
        )

        if exam_mode == "Entry Test Preparation":
            prompt = f"""Generate exactly {current_batch} MCQs for {institution} entry test.
Subject: {subject} | Topic: {topic} | Difficulty: {difficulty}
Start from Q{q_counter}. Do not repeat previous topics.

Format each MCQ exactly as:
Q{q_counter}. [Question]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Correct Answer: [Letter]) [Answer]
Explanation: [three sentence]
Key Note: [One point]
Exam Tip: [One tip]
---"""
        else:
            prompt = f"""Generate exactly {current_batch} MCQs for {program} students.
Subject: {subject} | Topic: {topic} | Difficulty: {difficulty}
Start from Q{q_counter}. Do not repeat previous topics.

Format each MCQ exactly as:
Q{q_counter}. [Question]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Correct Answer: [Letter]) [Answer]
Explanation: [three sentence]
Key Note: [One point]
---"""

        try:
            result = chat(prompt)
            if result:
                if result.startswith("Groq Error"):
                    st.error(f"❌ Batch {batch_num+1}: {result}")
                    print(f"\n===BATCH RESULT ERROR===\n{result}\n")
                else:
                    all_content.append(result.strip())
                st.write(f"✅ Batch {batch_num+1} OK — got {len(result)} chars")
            else:
                st.error(f"❌ Batch {batch_num+1}: result was None/empty")
        except Exception as e:
            st.error(f"❌ Batch {batch_num+1} FULL ERROR: {str(e)}")
            print(f"\n===BATCH ERROR===\n{str(e)}\n=================\n")

        q_counter += current_batch

        # ── Rate limit buffer ──
        if batch_num < total_batches - 1:
            time.sleep(2)

    progress.progress(1.0, text="✅ Done!")

    if not all_content:
        return None

    return "\n\n".join(all_content)


# ============================================
# PAGES
# ============================================

def show_dashboard():
    user = st.session_state.user
    stats = get_user_stats(user["id"])

    st.markdown(f"### 👋 Welcome back, {user['full_name']}!")
    st.markdown(
        f"<small style='color:gray'>📅 {datetime.now().strftime('%A, %d %B %Y')}</small>",
        unsafe_allow_html=True
    )
    st.divider()

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color:#1976d2">{stats['total_sessions']}</h2>
            <p>Study Sessions</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color:#388e3c">{stats['total_mcqs']:,}</h2>
            <p>MCQs Generated</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color:#7b1fa2">{stats['total_assessments']}</h2>
            <p>Tests Taken</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h2 style="color:#e65100">{stats['avg_score']}%</h2>
            <p>Average Score</p>
        </div>""", unsafe_allow_html=True)

    st.write("")

    # Motivational message based on score
    avg = stats["avg_score"]
    if avg == 0:
        msg = "🚀 Ready to start? Generate your first MCQs!"
        color = "#1976d2"
    elif avg >= 80:
        msg = "🌟 Excellent performance! Keep it up!"
        color = "#2e7d32"
    elif avg >= 60:
        msg = "👍 Good progress! A little more effort and you'll ace it!"
        color = "#f57c00"
    else:
        msg = "💪 Keep practicing — consistency is the key to success!"
        color = "#c62828"

    st.markdown(f"""
    <div style="background:white; border-radius:10px; padding:15px 20px;
    border-left:4px solid {color}; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
        <b style="color:{color}">{msg}</b>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col_left, col_right = st.columns(2)

    # Recent sessions
    with col_left:
        st.markdown("#### 📖 Recent Study Sessions")
        history = get_user_history(user["id"], limit=5)
        if not history:
            st.info("No sessions yet. Start generating MCQs!")
        else:
            for h in history:
                st.markdown(f"""
                <div class="history-card">
                    <b>📖 {h['subject']} — {h['topic']}</b><br>
                    <small style='color:gray'>
                        {h['program']} | {h['num_questions']} MCQs |
                        {h['difficulty']} | {h['created_at'][:16]}
                    </small>
                </div>
                """, unsafe_allow_html=True)

    # Recent assessments
    with col_right:
        st.markdown("#### 📊 Recent Assessment Results")
        assessments = get_user_assessments(user["id"], limit=5)
        if not assessments:
            st.info("No assessments yet. Take a test after generating MCQs!")
        else:
            for a in assessments:
                color = (
                    "#2e7d32" if a["score_pct"] >= 70
                    else "#e65100" if a["score_pct"] >= 40
                    else "#c62828"
                )
                st.markdown(f"""
                <div class="history-card">
                    <b>📊 {a['subject']} — {a['topic']}</b><br>
                    <span style="color:{color}; font-weight:600;">
                        {a['correct']}/{a['total_qs']} ({a['score_pct']}%)
                    </span>
                    <small style='color:gray'>
                        | {a['difficulty']} | {a['created_at'][:16]}
                    </small>
                </div>
                """, unsafe_allow_html=True)


def show_generate_page():
    st.markdown("### 🎯 What are you preparing for?")
    exam_mode = st.radio(
        "Select Mode",
        ["Regular Exam Preparation", "Entry Test Preparation"],
        horizontal=True
    )

    # Warning for large MCQ sets
    if exam_mode == "Entry Test Preparation":
        st.markdown("""
        <div class="warning-box">
            ⚠️ <b>Note:</b> Generating 100–200 MCQs will take
            several minutes as it runs in batches.
            Please be patient and don't close the browser.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    if exam_mode == "Entry Test Preparation":
        st.markdown("### 📝 Entry Test Details")
        col1, col2 = st.columns(2)
        with col1:
            et_select = st.selectbox("🏆 Entry Test", ENTRY_TESTS)
            if et_select == "Other Entry Test":
                entry_test = st.text_input(
                    "Enter Entry Test Name",
                    placeholder="e.g. Bahria University Entry Test"
                )
            else:
                entry_test = et_select
        with col2:
            subject = st.text_input(
                "📖 Subject",
                placeholder="e.g. Biology, Physics, Chemistry"
            )

        topic = st.text_input(
            "🔍 Topic",
            placeholder="e.g. Cell Division, Newton's Laws"
        )

        col3, col4, col5 = st.columns(3)
        with col3:
            num_questions = st.selectbox(
                "❓ Number of Questions",
                ENTRY_TEST_MCQ_OPTIONS,
                index=3  # Default: 20
            )
        with col4:
            difficulty = st.selectbox(
                "⚡ Difficulty", ["Easy", "Medium", "Hard", "Advanced"]
            )
        with col5:
            estimated = max(1, num_questions // 30)
            st.markdown(f"""
            <div style="padding-top:30px; font-size:13px; color:gray;">
                ⏱️ Est. time: ~{estimated} min
            </div>
            """, unsafe_allow_html=True)

        institution = entry_test
        program = "Entry Test"
        year = "Not Applicable"

    else:
        st.markdown("### 🎓 Student Details")
        col1, col2 = st.columns(2)
        with col1:
            prog_select = st.selectbox("🎓 Program", PROGRAMS)
            if prog_select == "Other Program":
                program = st.text_input(
                    "Enter Program",
                    placeholder="e.g. BS Islamic Studies"
                )
            else:
                program = prog_select
        with col2:
            year = st.selectbox("📅 Year / Semester", YEARS)

        col3, col4 = st.columns(2)
        with col3:
            inst_type = st.radio(
                "Institution Type",
                ["Board", "University"],
                horizontal=True
            )
        with col4:
            if inst_type == "Board":
                b_select = st.selectbox("🏫 Board", BOARDS)
                institution = (
                    st.text_input(
                        "Enter Board Name",
                        placeholder="e.g. BISE Kohat"
                    )
                    if b_select == "Other Board" else b_select
                )
            else:
                u_select = st.selectbox("🏛️ University", UNIVERSITIES)
                institution = (
                    st.text_input(
                        "Enter University Name",
                        placeholder="e.g. University of Swat"
                    )
                    if u_select == "Other University" else u_select
                )

        col5, col6 = st.columns(2)
        with col5:
            subject = st.text_input(
                "📖 Subject",
                placeholder="e.g. Anatomy, Physics"
            )
        with col6:
            topic = st.text_input(
                "🔍 Topic",
                placeholder="e.g. Nervous System"
            )

        col7, col8 = st.columns(2)
        with col7:
            num_questions = st.selectbox(
                "❓ Number of Questions", REGULAR_MCQ_OPTIONS
            )
        with col8:
            difficulty = st.selectbox(
                "⚡ Difficulty", ["Easy", "Medium", "Hard"]
            )

    st.divider()

    if st.button("🚀 Generate MCQs", use_container_width=True):
        errors = []
        if not subject.strip():
            errors.append("Subject")
        if not topic.strip():
            errors.append("Topic")
        if errors:
            for e in errors:
                st.error(f"❌ Please enter: {e}")
        else:
            with st.spinner(
            f"⏳ Generating {num_questions} MCQs... Please wait..."
        ):
                    result = generate_mcqs(
                exam_mode, program, year, institution,
                subject, topic, num_questions, difficulty
            )

        # ── Handle result ──
        if not result:
            st.error(
                "❌ Generation failed. Please try again or "
                "reduce the number of MCQs."
            )
            st.stop()

        parsed = parse_mcqs(result)

        if not parsed:
            st.error(
                "❌ MCQs generated but could not be read. "
                "Please try again."
            )
            st.stop()

        save_mcq_history(
            st.session_state.user["id"],
            exam_mode, program, year, institution,
            subject, topic, difficulty,
            len(parsed), result
        )

        st.session_state.current_mcqs  = result
        st.session_state.parsed_mcqs   = parsed
        st.session_state.current_meta  = {
            "exam_mode":     exam_mode,
            "program":       program,
            "year":          year,
            "institution":   institution,
            "subject":       subject,
            "topic":         topic,
            "difficulty":    difficulty,
            "num_questions": num_questions
        }
        st.session_state.answers   = {}
        st.session_state.submitted = False

        st.success(f"✅ {len(parsed)} MCQs Generated & Saved!")
        st.rerun()

            # Subtle support prompt
        st.markdown("""
            <div style='background:#E8F4FD; border-radius:8px;
            padding:10px 15px; font-size:12px; color:#1565C0;
            border-left:3px solid #1565C0; margin-top:5px'>
                💙 <b>Enjoying StudyMate AI?</b>
                Consider supporting us via the
                <b>"Support Us"</b> tab above.
                Every contribution keeps this tool free! 🇵🇰
            </div>
            """, unsafe_allow_html=True)
    

    # Display generated MCQs
    if st.session_state.current_mcqs:
        meta = st.session_state.current_meta
        st.divider()
        st.markdown(f"""
        <div class="info-box">
        🎓 <b>{meta['program']}</b> | 📅 {meta['year']}<br>
        🏫 <b>{meta['institution']}</b><br>
        📖 <b>{meta['subject']}</b> | 🔍 {meta['topic']}<br>
        ⚡ {meta['difficulty']} |
        ❓ {len(st.session_state.parsed_mcqs)} Questions Generated
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        parsed = st.session_state.parsed_mcqs
        for i, mcq in enumerate(parsed, 1):
            render_mcq_card(mcq, i)

        st.divider()
        if st.button("📝 Take Assessment Test", use_container_width=True):
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.rerun()


def show_history_page():
    st.markdown("### 📖 Your Learning History")
    history = get_user_history(st.session_state.user["id"], limit=100)

    if not history:
        st.info("No history yet. Start generating MCQs!")
        return

    # Search filter
    search = st.text_input(
        "🔍 Search by subject or topic",
        placeholder="e.g. Anatomy, Cell Biology..."
    )

    filtered = history
    if search.strip():
        filtered = [
            h for h in history
            if search.lower() in h["subject"].lower()
            or search.lower() in h["topic"].lower()
        ]

    st.markdown(f"Showing **{len(filtered)}** sessions")
    st.divider()

    for h in filtered:
        with st.expander(
            f"📖 {h['subject']} — {h['topic']} | "
            f"{h['num_questions']} MCQs | {h['created_at'][:16]}"
        ):
            st.markdown(f"""
            **Program:** {h['program']} | **{h['year']}**
            **Institution:** {h['institution']}
            **Mode:** {h['exam_mode']} | **Difficulty:** {h['difficulty']}
            """)
            st.divider()
            parsed = parse_mcqs(h['mcq_content'])
            for i, mcq in enumerate(parsed, 1):
                render_mcq_card(mcq, i)


def show_assessment_page():
    st.markdown("### 📝 Assessment Mode")

    if not st.session_state.parsed_mcqs:
        st.info(
            "No MCQs loaded. Go to **Generate MCQs** tab first, "
            "generate questions, then come back here."
        )
        return

    meta = st.session_state.current_meta
    parsed = st.session_state.parsed_mcqs

    st.markdown(f"""
    <div class="info-box">
    📖 <b>{meta['subject']}</b> — {meta['topic']} |
    ⚡ {meta['difficulty']} | ❓ {len(parsed)} Questions
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if not st.session_state.submitted:
        for i, mcq in enumerate(parsed):
            st.markdown(f"""
            <div class="mcq-card">
                <div class="question-text">Q{i+1}. {mcq['question']}</div>
            </div>
            """, unsafe_allow_html=True)
            if mcq["options"]:
                choice = st.radio(
                    f"Q{i+1}",
                    mcq["options"],
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
                st.session_state.answers[i] = choice
            st.write("")

        st.divider()
        if st.button("✅ Submit Assessment", use_container_width=True):
            st.session_state.submitted = True
            st.rerun()

    else:
        correct_count = 0
        for i, mcq in enumerate(parsed):
            user_answer = st.session_state.answers.get(i, "")
            correct_letter = mcq["correct"][:1] if mcq["correct"] else ""
            user_letter = user_answer[:1] if user_answer else ""
            is_correct = user_letter == correct_letter
            if is_correct:
                correct_count += 1

            border_color = "#4CAF50" if is_correct else "#f44336"
            result_icon = "✅" if is_correct else "❌"

            options_html = "".join([
                f'<div class="option" style="background:'
                f'{"#e8f5e9" if opt[:1]==correct_letter else "#ffebee" if opt[:1]==user_letter else "#f1f3f4"}'
                f'">{opt}</div>'
                for opt in mcq["options"]
            ])

            st.markdown(f"""
            <div class="mcq-card" style="border-left-color:{border_color}">
                <div class="question-text">
                    {result_icon} Q{i+1}. {mcq['question']}
                </div>
                {options_html}
                <div class="correct-answer">
                    ✅ Correct: {mcq['correct']}
                </div>
                <div style="font-size:13px;padding:4px 0;color:#555">
                    Your Answer: {user_answer}
                </div>
                {'<div class="explanation">📝 <b>Explanation:</b> ' + mcq["explanation"] + '</div>' if mcq["explanation"] else ""}
                {'<div class="keynote">🔑 <b>Key Note:</b> ' + mcq["keynote"] + '</div>' if mcq["keynote"] else ""}
            </div>
            """, unsafe_allow_html=True)

        save_assessment(
            st.session_state.user["id"],
            meta["subject"], meta["topic"],
            len(parsed), correct_count, meta["difficulty"]
        )

        score_pct = round((correct_count / len(parsed)) * 100, 1)
        color = (
            "#2e7d32" if score_pct >= 70
            else "#e65100" if score_pct >= 40
            else "#c62828"
        )
        grade = (
            "Excellent! 🎉" if score_pct >= 80
            else "Good Job! 👍" if score_pct >= 60
            else "Keep Practicing 📚" if score_pct >= 40
            else "Needs More Study 💪"
        )

        st.divider()
        st.markdown(f"""
        <div style="text-align:center; padding:25px; background:white;
        border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
            <h2 style="color:{color}">
                {correct_count}/{len(parsed)} — {score_pct}%
            </h2>
            <h3>{grade}</h3>
            <p style="color:gray; font-size:13px">
                Result saved to your dashboard
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.submitted = False
            st.session_state.answers = {}
            st.rerun()

def show_notes_page():
    """Smart Notes & Question Solver page"""

    st.markdown("### 📝 What do you need?")
    mode = st.radio(
        "Select Mode",
        ["📖 Generate Study Notes", "✏️ Solve a Question"],
        horizontal=True
    )
    st.divider()

    # ── Shared Fields ──
    st.markdown("### 🎓 Student Details")
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input(
            "👤 Your Name",
            placeholder="e.g. Ahmed Khan",
            key="notes_student_name"
        )
    with col2:
        prog_select = st.selectbox(
            "🎓 Program", PROGRAMS, key="notes_program"
        )
        if prog_select == "Other Program":
            program = st.text_input(
                "Enter Program", key="notes_prog_other",
                placeholder="e.g. BS Islamic Studies"
            )
        else:
            program = prog_select

    col3, col4 = st.columns(2)
    with col3:
        year = st.selectbox("📅 Year / Semester", YEARS, key="notes_year")
    with col4:
        inst_type = st.radio(
            "Institution Type",
            ["Board", "University"],
            horizontal=True, key="notes_inst_type"
        )

    if inst_type == "Board":
        b_sel = st.selectbox("🏫 Board", BOARDS, key="notes_board")
        institution = (
            st.text_input("Enter Board Name", key="notes_board_other")
            if b_sel == "Other Board" else b_sel
        )
    else:
        u_sel = st.selectbox("🏛️ University", UNIVERSITIES, key="notes_uni")
        institution = (
            st.text_input("Enter University Name", key="notes_uni_other")
            if u_sel == "Other University" else u_sel
        )

    col5, col6 = st.columns(2)
    with col5:
        subject = st.text_input(
            "📖 Subject",
            placeholder="e.g. Anatomy, Physics",
            key="notes_subject"
        )
    with col6:
        topic = st.text_input(
            "🔍 Topic",
            placeholder="e.g. Nervous System",
            key="notes_topic"
        )

    st.divider()

    # ── Mode-specific fields ──
    if "📖 Generate Study Notes" in mode:
        difficulty = st.selectbox(
            "⚡ Detail Level",
            ["Basic", "Intermediate", "Advanced"],
            key="notes_difficulty"
        )
        question_text = None
        marks = None
        btn_label = "📝 Generate Notes"
        doc_type = "notes"

    else:
        st.markdown("### ✏️ Question Details")
        question_text = st.text_area(
            "📋 Paste Your Question Here",
            placeholder=(
                "e.g. Describe the structure and function "
                "of the heart. (10 marks)"
            ),
            height=120,
            key="notes_question"
        )

        col7, col8 = st.columns([1, 3])
        with col7:
            marks = st.number_input(
                "📊 Marks",
                min_value=1, max_value=100,
                value=10, step=1,
                key="notes_marks"
            )
        with col8:
            mark_guide = (
                "Very brief — 2-3 lines" if marks <= 2
                else "Short — definition + key points" if marks <= 5
                else "Medium — structured paragraphs" if marks <= 10
                else "Detailed — full essay with all sections"
            )
            st.markdown(f"""
            <div style='padding-top:28px; font-size:13px;
            color:#1565C0'>
                📏 Expected: <b>{mark_guide}</b>
            </div>
            """, unsafe_allow_html=True)

        difficulty = "Exam Level"
        btn_label = f"✏️ Solve Question ({marks} Marks)"
        doc_type = "solution"

    st.divider()

    if st.button(btn_label, use_container_width=True, key="notes_generate"):
        # Validate
        errors = []
        if not student_name.strip():
            errors.append("Your Name")
        if not subject.strip():
            errors.append("Subject")
        if not topic.strip():
            errors.append("Topic")
        if doc_type == "solution" and not question_text.strip():
            errors.append("Question")

        if errors:
            for e in errors:
                st.error(f"❌ Please enter: {e}")
        else:
            with st.spinner("⏳ Generating... Please wait 1-2 minutes..."):
                if doc_type == "notes":
                    content = generate_notes(
                        program, year, institution,
                        subject, topic, difficulty
                    )
                else:
                    content = solve_question(
                        program, year, institution,
                        subject, topic, question_text, marks
                    )

            st.success("✅ Generated Successfully!")
            st.session_state.notes_content = content
            st.session_state.notes_meta = {
                "student_name": student_name,
                "program": program, "year": year,
                "institution": institution,
                "subject": subject, "topic": topic,
                "doc_type": doc_type,
                "question_text": question_text,
                "marks": marks, "difficulty": difficulty
            }
            st.rerun()

    # ── Display & Download ──
    if "notes_content" in st.session_state and st.session_state.notes_content:
        meta = st.session_state.notes_meta
        content = st.session_state.notes_content

        st.divider()
        st.markdown(f"""
        <div class="info-box">
        👤 <b>{meta['student_name']}</b> |
        🎓 {meta['program']} | 📅 {meta['year']}<br>
        🏫 {meta['institution']}<br>
        📖 <b>{meta['subject']}</b> — {meta['topic']}
        </div>
        """, unsafe_allow_html=True)

        # Preview
        with st.expander("👁️ Preview Content", expanded=True):
            st.markdown(content)

        st.divider()

        # Generate PDF
        st.markdown("### 📥 Download as PDF")
        col1, col2 = st.columns([3, 1])

        with col1:
            filename = st.text_input(
                "📄 File Name",
                value=f"{meta['student_name'].replace(' ', '_')}_"
                      f"{meta['subject'].replace(' ', '_')}_"
                      f"{meta['topic'].replace(' ', '_')}",
                key="notes_filename"
            )

        with col2:
            st.write("")
            st.write("")
            if st.button("⚙️ Generate PDF", use_container_width=True):
                with st.spinner("📄 Creating PDF..."):
                    pdf_bytes = generate_pdf(
                        content=content,
                        student_name=meta["student_name"],
                        subject=meta["subject"],
                        topic=meta["topic"],
                        program=meta["program"],
                        year=meta["year"],
                        institution=meta["institution"],
                        doc_type=meta["doc_type"],
                        question_text=meta.get("question_text"),
                        marks=meta.get("marks")
                    )
                st.session_state.pdf_bytes = pdf_bytes
                st.session_state.pdf_filename = f"{filename}.pdf"
                st.rerun()

        if "pdf_bytes" in st.session_state and st.session_state.pdf_bytes:
            st.download_button(
                label="📥 Download PDF Now",
                data=st.session_state.pdf_bytes,
                file_name=st.session_state.pdf_filename,
                mime="application/pdf",
                use_container_width=True
            )
            st.success(
                f"✅ PDF ready: **{st.session_state.pdf_filename}**"
            )
            st.markdown("""
            <div class="warning-box">
                💡 <b>Tip:</b> Clear notes content before
                generating new notes using the button below.
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Clear & Start New", use_container_width=True):
            st.session_state.notes_content = None
            st.session_state.notes_meta = None
            if "pdf_bytes" in st.session_state:
                del st.session_state["pdf_bytes"]
            st.rerun()

def show_share_bar(app_url):
    """Social media sharing bar"""

    # Encode URL for sharing
    import urllib.parse
    encoded_url = urllib.parse.quote(app_url)
    share_text = urllib.parse.quote(
        "🚀 StudyMate AI — Free AI-powered study tool for Pakistani students! "
        "Generate MCQs, Smart Notes, Practice Tests & more. "
        "Completely FREE! 📚"
    )

    whatsapp_url = (
        f"https://wa.me/?text={share_text}%20{encoded_url}"
    )
    facebook_url = (
        f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
    )
    twitter_url = (
        f"https://twitter.com/intent/tweet?text={share_text}"
        f"&url={encoded_url}"
    )
    linkedin_url = (
        f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}"
    )

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#1565C0,#42A5F5);
    border-radius:12px; padding:14px 20px; margin:10px 0;
    text-align:center'>
        <p style='color:white; font-size:13px; margin:0 0 10px 0'>
        📢 <b>Share StudyMate AI with your friends & classmates!</b><br>
        <small style='opacity:0.85'>
        Help fellow Pakistani students study smarter — it's completely FREE
        </small>
        </p>
        <div style='display:flex; gap:8px; justify-content:center;
        flex-wrap:wrap'>
            <a href='{whatsapp_url}' target='_blank'
            style='background:#25D366; color:white; padding:8px 16px;
            border-radius:8px; text-decoration:none; font-size:13px;
            font-weight:bold'>
                📱 WhatsApp
            </a>
            <a href='{facebook_url}' target='_blank'
            style='background:#1877F2; color:white; padding:8px 16px;
            border-radius:8px; text-decoration:none; font-size:13px;
            font-weight:bold'>
                📘 Facebook
            </a>
            <a href='{twitter_url}' target='_blank'
            style='background:#000000; color:white; padding:8px 16px;
            border-radius:8px; text-decoration:none; font-size:13px;
            font-weight:bold'>
                𝕏 Twitter/X
            </a>
            <a href='{linkedin_url}' target='_blank'
            style='background:#0A66C2; color:white; padding:8px 16px;
            border-radius:8px; text-decoration:none; font-size:13px;
            font-weight:bold'>
                💼 LinkedIn
            </a>
        </div>
        <p style='color:white; font-size:11px;
        margin:10px 0 0 0; opacity:0.85'>
            🔗 App Link: <b>{app_url}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# MAIN APP FLOW
# ============================================

# Always show sidebar
def get_app_stats():
    return {
        "total_users": 0,
        "total_sessions": 0,
        "total_mcqs": 0,
        "total_tests": 0
    }
# Always show sidebar
show_sidebar()

# ── Admin Panel Check ──
if st.session_state.get("show_admin"):
    show_admin_page()
    if st.button("← Back to App", key="back_from_admin"):
        st.session_state.show_admin = False
        st.rerun()
    st.stop()

if not st.session_state.logged_in:
    show_auth_page()
else:
    user = st.session_state.user

    col1, col2 = st.columns([5, 1])
    with col1:
        st.title("📚 StudyMate AI")
    with col2:
        st.write("")
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # ── Share Bar ── (correctly outside logout block)
    APP_URL = os.getenv("APP_URL", "http://localhost:8501")
    show_share_bar(APP_URL)
    st.write("")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "🏠 Dashboard",
        "🚀 Generate MCQs",
        "📝 Smart Notes",
        "✅ Assessment",
        "📊 My Progress",
        "⏳ Exam Countdown",
        "📚 Notes Library",
        "📄 Past Papers",
        "👥 Community",
        "📖 History",
    ])

    with tab1:
        show_dashboard()
    with tab2:
        show_generate_page()
    with tab3:
        show_notes_page()
    with tab4:
        show_assessment_page()
    with tab5:
        show_progress_charts(user["id"])
    with tab6:
        show_exam_countdown(user["id"])
    with tab7:
        show_admin_notes_student()
    with tab8:
        show_past_papers_student()
    with tab9:
        show_community_page(user)
    with tab10:
        show_history_page()

# ── Footer ──
st.divider()
st.markdown("""
<div style='text-align:center; color:gray; font-size:12px; padding:10px 0'>
    📚 <b>StudyMate AI v6.0</b> | Built with ❤️ for Pakistani Students |
    Developer: <b>Aftab Ahmed</b> |
    © 2025 All Rights Reserved
</div>
""", unsafe_allow_html=True)