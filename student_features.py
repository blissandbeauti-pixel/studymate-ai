# ============================================
# StudyMate AI - Student Extra Features
# Exam Countdown + Progress Charts + Past Papers
# ============================================

import streamlit as st
from datetime import datetime, date, timedelta
from database import (
    save_exam_countdown, get_user_countdowns,
    delete_countdown, get_subject_progress,
    get_score_trend, get_past_papers
)


# ============================================
# EXAM COUNTDOWN
# ============================================

def show_exam_countdown(user_id):
    """Exam countdown timer feature"""
    st.markdown("### ⏳ Exam Countdown")

    # Add new countdown
    with st.expander("➕ Add New Exam", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            exam_name = st.text_input(
                "📋 Exam Name",
                placeholder="e.g. MDCAT 2025, BSN Final Exam",
                key="cd_exam_name"
            )
            subject = st.text_input(
                "📖 Main Subject (optional)",
                placeholder="e.g. Biology, All Subjects",
                key="cd_subject"
            )
        with col2:
            exam_date = st.date_input(
                "📅 Exam Date",
                min_value=date.today(),
                key="cd_date"
            )

        if st.button("⏱️ Add Countdown", use_container_width=True):
            if not exam_name.strip():
                st.error("❌ Please enter exam name.")
            else:
                saved = save_exam_countdown(
                    user_id, exam_name,
                    str(exam_date), subject
                )
                if saved:
                    st.success("✅ Exam countdown added!")
                    st.rerun()

    st.divider()

    # Show countdowns
    countdowns = get_user_countdowns(user_id)

    if not countdowns:
        st.info(
            "No exams added yet. "
            "Add your upcoming exams to track countdown!"
        )
        return

    for cd in countdowns:
        exam_dt = datetime.strptime(cd["exam_date"], "%Y-%m-%d").date()
        days_left = (exam_dt - date.today()).days

        # Color based on urgency
        if days_left < 0:
            color = "#757575"
            status = "Exam Passed"
            icon = "✅"
        elif days_left == 0:
            color = "#C62828"
            status = "TODAY!"
            icon = "🔥"
        elif days_left <= 7:
            color = "#C62828"
            status = f"{days_left} days left"
            icon = "🚨"
        elif days_left <= 30:
            color = "#E65100"
            status = f"{days_left} days left"
            icon = "⚠️"
        elif days_left <= 90:
            color = "#F57C00"
            status = f"{days_left} days left"
            icon = "📅"
        else:
            color = "#2E7D32"
            status = f"{days_left} days left"
            icon = "✅"

        # Daily study target
        if days_left > 0:
            hours_per_day = max(1, min(8, 200 // max(1, days_left)))
            study_tip = f"Study ~{hours_per_day}h/day to be prepared"
        else:
            study_tip = ""

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div style='background:white; border-radius:12px;
            padding:15px 20px; margin:8px 0;
            border-left:5px solid {color};
            box-shadow:0 2px 8px rgba(0,0,0,0.08)'>
                <div style='display:flex;
                justify-content:space-between;
                align-items:center'>
                    <div>
                        <b style='font-size:16px'>
                            {icon} {cd['exam_name']}
                        </b>
                        <br>
                        <small style='color:gray'>
                            📅 {cd['exam_date']}
                            {' | 📖 ' + cd['subject']
                             if cd['subject'] else ''}
                        </small>
                    </div>
                    <div style='text-align:center'>
                        <div style='font-size:28px;
                        font-weight:bold; color:{color}'>
                            {abs(days_left) if days_left >= 0
                             else "Over"}
                        </div>
                        <div style='font-size:11px;
                        color:{color}; font-weight:bold'>
                            {status}
                        </div>
                    </div>
                </div>
                {f'<div style="font-size:12px; color:#1565C0; margin-top:6px">💡 {study_tip}</div>' if study_tip else ''}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.write("")
            st.write("")
            if st.button(
                "🗑️",
                key=f"del_cd_{cd['id']}",
                help="Delete this countdown"
            ):
                delete_countdown(cd["id"], user_id)
                st.rerun()


# ============================================
# PROGRESS CHARTS
# ============================================

def show_progress_charts(user_id):
    """Subject-wise progress analytics"""
    st.markdown("### 📊 Your Progress Analytics")

    subject_data = get_subject_progress(user_id)
    score_trend = get_score_trend(user_id, limit=15)

    if not subject_data and not score_trend:
        st.info(
            "No assessment data yet. "
            "Take some tests to see your progress!"
        )
        return

    if subject_data:
        import pandas as pd

        # Subject performance chart
        st.markdown("#### 📚 Subject-wise Performance")
        df = pd.DataFrame(subject_data)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Average Score by Subject**")
            chart_df = df[["subject", "avg_score"]].copy()
            chart_df.columns = ["Subject", "Avg Score (%)"]
            chart_df["Subject"] = chart_df["Subject"].str[:15]
            st.bar_chart(
                chart_df.set_index("Subject"),
                color="#1565C0"
            )

        with col2:
            st.markdown("**Attempts by Subject**")
            att_df = df[["subject", "attempts"]].copy()
            att_df.columns = ["Subject", "Attempts"]
            att_df["Subject"] = att_df["Subject"].str[:15]
            st.bar_chart(
                att_df.set_index("Subject"),
                color="#2E7D32"
            )

        # Detailed table
        st.markdown("#### 📋 Detailed Subject Report")
        for row in subject_data:
            score = round(row["avg_score"], 1)
            best = round(row["best_score"], 1)
            color = (
                "#2E7D32" if score >= 70
                else "#E65100" if score >= 40
                else "#C62828"
            )
            grade = (
                "Excellent 🌟" if score >= 80
                else "Good 👍" if score >= 60
                else "Average 📚" if score >= 40
                else "Needs Work 💪"
            )

            # Progress bar width
            bar_width = int(score)

            st.markdown(f"""
            <div style='background:white; border-radius:10px;
            padding:15px 20px; margin:8px 0;
            box-shadow:0 2px 6px rgba(0,0,0,0.07);
            border-left:4px solid {color}'>
                <div style='display:flex;
                justify-content:space-between;
                align-items:center; margin-bottom:8px'>
                    <b style='font-size:15px'>
                        📖 {row['subject']}
                    </b>
                    <span style='color:{color};
                    font-weight:bold; font-size:16px'>
                        {score}% — {grade}
                    </span>
                </div>
                <div style='background:#f1f3f4;
                border-radius:10px; height:8px;
                overflow:hidden; margin-bottom:8px'>
                    <div style='background:{color};
                    width:{bar_width}%; height:100%;
                    border-radius:10px'></div>
                </div>
                <small style='color:gray'>
                    📝 {row['attempts']} tests |
                    ⭐ Best: {best}% |
                    ❓ {row['total_questions']} questions |
                    ✅ {row['total_correct']} correct
                </small>
            </div>
            """, unsafe_allow_html=True)

    # Score trend
    if score_trend:
        st.markdown("#### 📈 Recent Score Trend")
        import pandas as pd
        trend_df = pd.DataFrame(score_trend)
        trend_df = trend_df[["subject", "score_pct"]].copy()
        trend_df.columns = ["Subject", "Score (%)"]
        trend_df = trend_df.iloc[::-1]  # Chronological order
        st.line_chart(trend_df.set_index("Subject"))

    # Overall summary
    if subject_data:
        total_attempts = sum(r["attempts"] for r in subject_data)
        overall_avg = round(
            sum(r["avg_score"] for r in subject_data)
            / len(subject_data), 1
        )
        best_subject = max(
            subject_data, key=lambda x: x["avg_score"]
        )
        worst_subject = min(
            subject_data, key=lambda x: x["avg_score"]
        )

        st.divider()
        st.markdown("#### 🏆 Performance Summary")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Tests", total_attempts)
        with c2:
            st.metric("Overall Average", f"{overall_avg}%")
        with c3:
            st.metric(
                "🌟 Best Subject",
                best_subject["subject"][:12]
            )
        with c4:
            st.metric(
                "📚 Needs Work",
                worst_subject["subject"][:12]
            )


# ============================================
# PAST PAPERS (STUDENT VIEW)
# ============================================

def show_past_papers_student():
    """Student view of past papers"""
    st.markdown("### 📄 Past Papers")

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_board = st.text_input(
            "🏫 Filter by Board/University",
            placeholder="e.g. FBISE, PMC"
        )
    with col2:
        filter_program = st.text_input(
            "🎓 Filter by Program",
            placeholder="e.g. FSc Pre-Medical"
        )
    with col3:
        filter_subject = st.text_input(
            "📖 Filter by Subject",
            placeholder="e.g. Biology"
        )

    papers = get_past_papers(
        board=filter_board if filter_board else None,
        program=filter_program if filter_program else None,
        subject=filter_subject if filter_subject else None
    )

    if not papers:
        st.info(
            "📭 No past papers available yet. "
            "Admin will upload papers soon. Check back later!"
        )
        return

    st.markdown(f"**{len(papers)} papers found**")
    st.divider()

    for p in papers:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div style='background:white; border-radius:10px;
            padding:14px 18px; margin:6px 0;
            border-left:4px solid #1565C0;
            box-shadow:0 1px 4px rgba(0,0,0,0.06)'>
                <b style='font-size:15px'>
                    📄 {p['title']}
                </b><br>
                <small style='color:gray'>
                    🏫 {p['board']} |
                    🎓 {p['program']} |
                    📖 {p['subject']} |
                    📅 Year: {p['year']} |
                    📑 {p['paper_type']}
                </small>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.write("")
            # Download button
            if p.get("file_path"):
                try:
                    with open(p["file_path"], "rb") as f:
                        st.download_button(
                            "📥 Download",
                            data=f.read(),
                            file_name=f"{p['title']}.pdf",
                            mime="application/pdf",
                            key=f"dl_{p['id']}"
                        )
                except FileNotFoundError:
                    st.error("File not found")