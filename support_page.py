# ============================================
# StudyMate AI - Support & Contribution Page
# ============================================

import streamlit as st


def show_support_page():
    """Professional support/donation page"""

    # ── Hero Section ──
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1565C0,#1976D2,#42A5F5);
    border-radius:16px; padding:40px 30px; text-align:center;
    margin-bottom:25px; color:white'>
        <div style='font-size:48px; margin-bottom:10px'>🎓</div>
        <h1 style='margin:0; font-size:28px; font-weight:700'>
            Support StudyMate AI
        </h1>
        <p style='margin:12px 0 0 0; font-size:15px;
        opacity:0.9; max-width:500px; margin:10px auto 0'>
            Help keep this free educational tool alive and growing
            for students across Pakistan
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Mission Statement ──
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""
        <div style='background:white; border-radius:14px;
        padding:28px 32px; box-shadow:0 4px 16px rgba(0,0,0,0.08);
        margin-bottom:20px; line-height:1.9; font-size:14px;
        color:#333; text-align:center'>

        <p style='font-size:18px; color:#1565C0; font-weight:600;
        margin-bottom:16px'>
            بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ
        </p>

        <p>
        Assalam-o-Alaikum,
        </p>

        <p>
        <b>StudyMate AI</b> was created with one sincere purpose —
        to give every Pakistani student access to a smart,
        personalized study tool, completely <b>free of charge</b>,
        regardless of their background or financial situation.
        </p>

        <p>
        From students preparing for <b>MDCAT and ECAT</b> in remote
        areas, to BSN and DAE students in small cities — this tool
        was built for all of them.
        </p>

        <p>
        This platform is built, maintained and improved
        <b>entirely by one person</b>, using personal time
        and personal resources — with no institutional
        funding or commercial backing.
        </p>

        <p>
        Every feature you use — MCQ generation, smart notes,
        PDF export, assessment tracking, exam countdown —
        represents hours of dedicated work and real costs
        in server and AI infrastructure.
        </p>

        <p style='color:#1565C0; font-weight:600'>
        If StudyMate AI has helped you — even once —
        I humbly invite you to be a part of this mission.
        </p>

        <p>
        Your contribution, however small, directly enables:
        </p>

        </div>
        """, unsafe_allow_html=True)

    # ── Impact Cards ──
    c1, c2, c3, c4 = st.columns(4)
    impacts = [
        ("🆓", "Keep It Free", "For every student, forever"),
        ("⚡", "Better AI", "Faster, smarter responses"),
        ("📚", "More Content", "New subjects & programs"),
        ("🇵🇰", "More Tools", "New free apps for Pakistan"),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], impacts):
        with col:
            st.markdown(f"""
            <div style='background:white; border-radius:12px;
            padding:18px 12px; text-align:center;
            box-shadow:0 2px 10px rgba(0,0,0,0.07);
            border-top:3px solid #1565C0'>
                <div style='font-size:28px'>{icon}</div>
                <div style='font-weight:700; color:#1565C0;
                font-size:13px; margin:6px 0'>{title}</div>
                <div style='font-size:11px; color:gray'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # ── How to Contribute ──
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center; margin:10px 0 20px'>
            <h3 style='color:#1565C0'>
                💳 Ways to Support
            </h3>
            <p style='color:gray; font-size:13px'>
                Choose any method that's convenient for you.
                Every contribution — big or small — is deeply appreciated.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Payment Methods ──
    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("""
        <div style='background:white; border-radius:14px;
        overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.1);
        margin:5px'>
            <div style='background:linear-gradient(135deg,#00a651,#007a3d);
            padding:20px; text-align:center'>
                <div style='font-size:36px'>📱</div>
                <div style='color:white; font-size:18px;
                font-weight:700; margin-top:6px'>EasyPaisa</div>
                <div style='color:rgba(255,255,255,0.8);
                font-size:12px'>Mobile Wallet</div>
            </div>
            <div style='padding:20px; text-align:center'>
                <div style='font-size:22px; font-weight:800;
                color:#00a651; letter-spacing:2px;
                font-family:monospace'>
                    0345-6774790
                </div>
                <div style='color:gray; font-size:13px;
                margin-top:8px'>Account Name</div>
                <div style='font-weight:700; font-size:15px;
                color:#333'>Aftab Ahmed</div>
                <div style='margin-top:12px; padding:10px;
                background:#f0fdf4; border-radius:8px;
                font-size:12px; color:#2E7D32'>
                    ✅ Instant transfer<br>
                    ✅ No charges<br>
                    ✅ Available 24/7
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div style='background:white; border-radius:14px;
        overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.1);
        margin:5px'>
            <div style='background:linear-gradient(135deg,#6C2DC7,#4a1a8c);
            padding:20px; text-align:center'>
                <div style='font-size:36px'>💜</div>
                <div style='color:white; font-size:18px;
                font-weight:700; margin-top:6px'>SadaPay</div>
                <div style='color:rgba(255,255,255,0.8);
                font-size:12px'>Digital Bank</div>
            </div>
            <div style='padding:20px; text-align:center'>
                <div style='font-size:22px; font-weight:800;
                color:#6C2DC7; letter-spacing:2px;
                font-family:monospace'>
                    0308-1816669
                </div>
                <div style='color:gray; font-size:13px;
                margin-top:8px'>Account Name</div>
                <div style='font-weight:700; font-size:15px;
                color:#333'>Aftab Ahmed</div>
                <div style='margin-top:12px; padding:10px;
                background:#f5f0ff; border-radius:8px;
                font-size:12px; color:#6C2DC7'>
                    ✅ Free transfers<br>
                    ✅ Secure & fast<br>
                    ✅ Available 24/7
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div style='background:white; border-radius:14px;
        overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.1);
        margin:5px'>
            <div style='background:linear-gradient(135deg,#FF6B35,#cc4400);
            padding:20px; text-align:center'>
                <div style='font-size:36px'>🟠</div>
                <div style='color:white; font-size:18px;
                font-weight:700; margin-top:6px'>NayaPay</div>
                <div style='color:rgba(255,255,255,0.8);
                font-size:12px'>Digital Wallet</div>
            </div>
            <div style='padding:20px; text-align:center'>
                <div style='font-size:22px; font-weight:800;
                color:#FF6B35; letter-spacing:2px;
                font-family:monospace'>
                    0308-1816669
                </div>
                <div style='color:gray; font-size:13px;
                margin-top:8px'>Account Name</div>
                <div style='font-weight:700; font-size:15px;
                color:#333'>Aftab Ahmed</div>
                <div style='margin-top:12px; padding:10px;
                background:#fff5f0; border-radius:8px;
                font-size:12px; color:#FF6B35'>
                    ✅ Quick transfer<br>
                    ✅ Reliable service<br>
                    ✅ Available 24/7
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ── Suggested Amounts ──
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""
        <div style='background:white; border-radius:14px;
        padding:24px; box-shadow:0 2px 10px rgba(0,0,0,0.07);
        text-align:center; margin:10px 0'>
            <h4 style='color:#1565C0; margin-bottom:16px'>
                💡 Suggested Contribution Amounts
            </h4>
        </div>
        """, unsafe_allow_html=True)

        a1, a2, a3, a4 = st.columns(4)
        amounts = [
            ("Rs. 50", "☕", "A cup of chai", "#4CAF50"),
            ("Rs. 100", "📖", "One textbook chapter", "#1565C0"),
            ("Rs. 500", "🌟", "Monthly support", "#7B1FA2"),
            ("Any Amount", "❤️", "Every rupee helps", "#E65100"),
        ]
        for col, (amount, icon, desc, color) in zip(
            [a1, a2, a3, a4], amounts
        ):
            with col:
                st.markdown(f"""
                <div style='background:{color}15;
                border:2px solid {color}40;
                border-radius:10px; padding:14px 8px;
                text-align:center'>
                    <div style='font-size:24px'>{icon}</div>
                    <div style='font-weight:800; color:{color};
                    font-size:16px; margin:4px 0'>{amount}</div>
                    <div style='font-size:10px;
                    color:gray'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

    st.write("")

    # ── Closing Message ──
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#E3F2FD,#F3E5F5);
        border-radius:14px; padding:24px 28px; text-align:center;
        border:1px solid #BBDEFB; margin-top:10px'>
            <p style='font-size:15px; color:#333;
            line-height:1.8; margin:0'>
                Whether you contribute <b>Rs. 50 or Rs. 5,000</b>,
                your support sends a message that
                <b>education matters</b> and that
                Pakistani students deserve better tools.<br><br>
                <i style='color:#1565C0'>
                "The best charity is that given in Ramadan."
                — Prophet Muhammad ﷺ
                </i><br><br>
                May Allah reward you abundantly. 🤲<br>
                <b>JazakAllah Khair — Aftab Ahmed</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ── After-contribution message ──
    st.markdown("""
    <div style='text-align:center; color:gray;
    font-size:12px; padding:10px 0'>
        📧 After contributing, feel free to reach out:<br>
        <b>Contact via Suggestion Box in the sidebar</b><br>
        Your name will be added to our supporters list
        with your permission. 🌟
    </div>
    """, unsafe_allow_html=True)