# ============================================
# StudyMate AI - AI Chat Tutor
# Supports English and Urdu
# ============================================

import streamlit as st
from ai_backend import chat
from database import (
    save_chat_message, get_chat_history,
    clear_chat_history, update_streak
)

SUBJECTS = [
    "General (Any Topic)",
    "Biology", "Chemistry", "Physics", "Mathematics",
    "English", "Urdu", "Islamiat", "Pakistan Studies",
    "Computer Science", "Statistics", "Economics",
    "Anatomy", "Physiology", "Pharmacology",
    "Civil Engineering", "Electrical Engineering",
    "Mechanical Engineering", "Other"
]


def build_system_prompt(subject, program, language):
    """Build AI tutor system prompt"""
    lang_instruction = (
        "Always respond in Urdu language. "
        "Use simple, clear Urdu that students can understand easily."
        if language == "urdu"
        else
        "Always respond in English."
    )

    return f"""You are an expert AI tutor for Pakistani students.

Student Program : {program}
Subject Focus   : {subject}
Language        : {language.title()}

Your role:
- Explain concepts clearly and simply
- Use examples relevant to Pakistani students
- Follow HEC Pakistan curriculum standards
- For medical topics: use clinical examples
- For engineering: use practical examples
- Break down complex topics step by step
- Encourage the student warmly

{lang_instruction}

Keep responses focused, clear and educational.
Never give harmful or inappropriate content.
"""


def show_chat_tutor(user):
    """Main AI Chat Tutor page"""

    # ── Update streak on visit ──
    update_streak(user["id"])

    # ── Get language preference ──
    language = st.session_state.get("language", "english")

    # ── Page Title ──
    title = (
        "🤖 اے آئی ٹیوٹر" if language == "urdu"
        else "🤖 AI Chat Tutor"
    )
    subtitle = (
        "اپنا سوال پوچھیں — آپ کا ذاتی AI استاد"
        if language == "urdu"
        else "Ask anything — your personal AI teacher, available 24/7"
    )

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#1B2A4A,#2E4A7A);
    border-radius:14px; padding:22px; color:white;
    text-align:center; margin-bottom:20px'>
        <h2 style='margin:0; font-size:24px'>{title}</h2>
        <p style='margin:8px 0 0; opacity:0.9; font-size:13px'>
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Controls Row ──
    col1, col2, col3 = st.columns([3, 2, 1])

    with col1:
        subject = st.selectbox(
            "📖 Subject Focus",
            SUBJECTS,
            key="chat_subject"
        )

    with col2:
        lang_options = ["English", "اردو (Urdu)"]
        lang_choice  = st.selectbox(
            "🌐 Language",
            lang_options,
            index=0 if language == "english" else 1,
            key="chat_language_select"
        )
        # Update language in session
        new_lang = (
            "urdu" if "Urdu" in lang_choice else "english"
        )
        if new_lang != language:
            st.session_state.language = new_lang
            st.rerun()

    with col3:
        st.write("")
        st.write("")
        if st.button(
            "🗑️ Clear",
            use_container_width=True,
            key="clear_chat_btn"
        ):
            clear_chat_history(user["id"])
            if "chat_messages" in st.session_state:
                st.session_state.chat_messages = []
            st.rerun()

    st.divider()

    # ── Initialize chat messages in session ──
    if "chat_messages" not in st.session_state:
        # Load from database
        history = get_chat_history(user["id"], limit=30)
        st.session_state.chat_messages = [
            {"role": h["role"], "content": h["message"]}
            for h in history
        ]

    # ── Welcome message if no history ──
    if not st.session_state.chat_messages:
        if language == "urdu":
            welcome = (
                f"السلام علیکم {user['full_name']}! 👋\n\n"
                f"میں آپ کا AI ٹیوٹر ہوں۔ "
                f"آپ مجھ سے کوئی بھی سوال پوچھ سکتے ہیں۔ "
                f"میں آپ کی مدد کرنے کے لیے حاضر ہوں! 📚"
            )
        else:
            welcome = (
                f"Welcome {user['full_name']}! 👋\n\n"
                f"I'm your personal AI Tutor. Ask me anything "
                f"about **{subject}** or any other subject. "
                f"I'm here to help you learn and succeed! 📚"
            )
        st.session_state.chat_messages.append({
            "role":    "assistant",
            "content": welcome
        })

    # ── Display Chat Messages ──
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # ── Suggested Questions ──
    if len(st.session_state.chat_messages) <= 1:
        st.markdown("**💡 Try asking:**")

        if language == "urdu":
            suggestions = [
                "مائٹوسس کو آسان الفاظ میں سمجھائیں",
                "نیوٹن کے قوانین کیا ہیں؟",
                "دل کی ساخت بیان کریں",
                "MDCAT کی تیاری کیسے کریں؟",
            ]
        else:
            suggestions = [
                "Explain mitosis in simple words",
                "What are Newton's laws of motion?",
                "Describe the structure of the heart",
                "How to prepare for MDCAT effectively?",
            ]

        cols = st.columns(2)
        for idx, suggestion in enumerate(suggestions):
            with cols[idx % 2]:
                if st.button(
                    suggestion,
                    key=f"suggest_{idx}",
                    use_container_width=True
                ):
                    st.session_state.pending_message = suggestion
                    st.rerun()

    # ── Process Pending Message (from suggestion buttons) ──
    if "pending_message" in st.session_state:
        pending = st.session_state.pop("pending_message")
        st.session_state.chat_messages.append({
            "role": "user", "content": pending
        })
        save_chat_message(
            user["id"], "user", pending,
            subject, language
        )

        with st.spinner(
            "🤔 سوچ رہا ہوں..." if language == "urdu"
            else "🤔 Thinking..."
        ):
            system = build_system_prompt(
                subject,
                user.get("program", "General"),
                language
            )
            response = chat(pending, system_prompt=system)

        st.session_state.chat_messages.append({
            "role": "assistant", "content": response
        })
        save_chat_message(
            user["id"], "assistant", response,
            subject, language
        )
        st.rerun()

    # ── Chat Input ──
    placeholder = (
        "اپنا سوال یہاں لکھیں..."
        if language == "urdu"
        else "Type your question here..."
    )

    if user_input := st.chat_input(placeholder):
        # Add user message
        st.session_state.chat_messages.append({
            "role": "user", "content": user_input
        })
        save_chat_message(
            user["id"], "user",
            user_input, subject, language
        )

        # Get AI response
        with st.spinner(
            "🤔 سوچ رہا ہوں..." if language == "urdu"
            else "🤔 Thinking..."
        ):
            system = build_system_prompt(
                subject,
                user.get("program", "General"),
                language
            )
            response = chat(user_input, system_prompt=system)

        # Add AI response
        st.session_state.chat_messages.append({
            "role": "assistant", "content": response
        })
        save_chat_message(
            user["id"], "assistant",
            response, subject, language
        )
        st.rerun()