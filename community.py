# ============================================
# StudyMate AI - Community & Profiles
# Teacher/Tutor Directory
# ============================================

import streamlit as st
from database import (
    get_all_teachers, get_teacher_profile,
    save_teacher_profile, verify_teacher
)


def show_community_page(user):
    """Community page — teacher directory"""

    st.markdown("""
    <div style='background:linear-gradient(135deg,#1565C0,#42A5F5);
    border-radius:14px; padding:25px; color:white;
    text-align:center; margin-bottom:20px'>
        <h2 style='margin:0'>👥 StudyMate Community</h2>
        <p style='margin:8px 0 0; opacity:0.9'>
            Connect with qualified teachers & tutors across Pakistan
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs([
        "🔍 Find a Tutor/Teacher",
        "👨‍🏫 My Teacher Profile"
    ])

    with tab1:
        show_teacher_directory()

    with tab2:
        show_my_teacher_profile(user)


def show_teacher_directory():
    """Browse teacher profiles"""

    st.markdown("""
    <div style='background:#FFF3E0; border-radius:10px;
    padding:12px 16px; font-size:12px; color:#E65100;
    margin-bottom:15px; border-left:4px solid #FF9800'>
        ⚠️ <b>Disclaimer:</b> StudyMate AI provides this directory
        as a convenience only. Any arrangements between students
        and teachers are purely between them. StudyMate AI bears
        no responsibility for any agreements or transactions.
    </div>
    """, unsafe_allow_html=True)

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        subject_filter = st.text_input(
            "🔍 Search by Subject",
            placeholder="e.g. Physics, Biology"
        )
    with col2:
        city_filter = st.text_input(
            "📍 Filter by City",
            placeholder="e.g. Lahore, Karachi"
        )
    with col3:
        
        st.write("")
        search_btn = st.button(
        "🔍 Search", use_container_width=True,
        key="community_search_btn"
        )

    teachers = get_all_teachers(
        subject_filter if subject_filter else None,
        city_filter if city_filter else None
    )

    st.markdown(f"**{len(teachers)} teachers found**")
    st.divider()

    if not teachers:
        st.info(
            "No teachers found. "
            "Be the first to register as a teacher!"
        )
        return

    # Display teacher cards
    for t in teachers:
        verified_badge = (
            '<span style="background:#E8F5E9; color:#2E7D32; '
            'padding:2px 8px; border-radius:10px; font-size:11px; '
            'font-weight:bold">✅ Verified</span>'
            if t["is_verified"] else
            '<span style="background:#FFF3E0; color:#E65100; '
            'padding:2px 8px; border-radius:10px; font-size:11px">'
            '⏳ Pending Verification</span>'
        )

        subjects = t.get("master_subjects", "").replace(",", " •")
        services = t.get("services", "").replace(",", " •")

        st.markdown(f"""
        <div style='background:white; border-radius:14px;
        padding:20px 24px; margin:12px 0;
        box-shadow:0 3px 12px rgba(0,0,0,0.08);
        border-left:5px solid {"#2E7D32" if t["is_verified"] else "#1565C0"}'>
            <div style='display:flex;
            justify-content:space-between; align-items:flex-start'>
                <div>
                    <h3 style='margin:0; color:#1A1A2E;
                    font-size:18px'>
                        👨‍🏫 {t['full_name']}
                    </h3>
                    <div style='margin:4px 0'>
                        {verified_badge}
                    </div>
                </div>
                <div style='text-align:right'>
                    <div style='font-size:18px; font-weight:700;
                    color:#1565C0'>
                        💰 {t.get('hourly_rate', 'Negotiable')}/hr
                    </div>
                    <div style='font-size:12px; color:gray'>
                        📍 {t.get('city', 'N/A')} |
                        📅 {t.get('experience_yrs', 0)} yrs exp
                    </div>
                </div>
            </div>

            <div style='margin:10px 0; font-size:13px; color:#555'>
                🎓 <b>Qualification:</b> {t.get('qualification', 'N/A')}
            </div>

            <div style='background:#E3F2FD; border-radius:8px;
            padding:8px 12px; margin:8px 0;
            font-size:13px; color:#1565C0'>
                📚 <b>Subjects:</b> {subjects}
            </div>

            <div style='background:#F3E5F5; border-radius:8px;
            padding:8px 12px; margin:8px 0;
            font-size:13px; color:#6A1B9A'>
                🛠️ <b>Services:</b> {services}
            </div>

            <div style='font-size:13px; color:#555;
            margin:8px 0; line-height:1.6'>
                ⏰ <b>Availability:</b>
                {t.get('availability', 'N/A')}
            </div>

            <div style='font-size:13px; color:#333;
            margin:10px 0; padding:10px;
            background:#FAFAFA; border-radius:8px'>
                {t.get('bio', '')[:200]}
                {'...' if len(t.get('bio', '')) > 200 else ''}
            </div>

            <div style='background:#E8F5E9; border-radius:8px;
            padding:10px 14px; margin-top:10px;
            font-size:13px; color:#2E7D32'>
                📱 <b>Contact:</b> {t.get('contact_info', 'N/A')}
                &nbsp;|&nbsp;
                📧 {t.get('email', 'N/A')}
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_my_teacher_profile(user):
    """Teacher can view/edit own profile"""
    account_type = user.get("account_type", "student")

    if account_type != "teacher":
        st.info(
            "👨‍🏫 This section is for Teacher accounts only.\n\n"
            "If you are a teacher, please create a new account "
            "and select 'Teacher/Tutor' as your account type."
        )
        return

    existing = get_teacher_profile(user["id"])

    st.markdown("### 👨‍🏫 Your Teacher Profile")

    if existing:
        status = (
            "✅ Verified" if existing["is_verified"]
            else "⏳ Pending Admin Verification"
        )
        st.markdown(f"""
        <div style='background:#E8F5E9; border-radius:10px;
        padding:12px 16px; font-size:13px; margin-bottom:15px'>
            <b>Profile Status:</b> {status}
        </div>
        """, unsafe_allow_html=True)

    # Profile form
    with st.form("teacher_profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            qualification = st.text_input(
                "🎓 Qualification",
                value=existing.get("qualification", "") if existing else ""
            )
            city = st.text_input(
                "📍 City",
                value=existing.get("city", "") if existing else ""
            )
            experience = st.number_input(
                "📅 Years Experience",
                min_value=0, max_value=50,
                value=int(existing.get("experience_yrs", 1)) if existing else 1
            )
        with col2:
            hourly_rate = st.text_input(
                "💰 Fee/Hour (PKR)",
                value=existing.get("hourly_rate", "") if existing else ""
            )
            availability = st.selectbox(
                "⏰ Availability",
                [
                    "Weekdays only", "Weekends only",
                    "Both weekdays & weekends",
                    "Evenings only", "Flexible"
                ],
                index=0
            )
            contact = st.text_input(
                "📱 Contact (WhatsApp)",
                value=existing.get("contact_info", "") if existing else ""
            )

        master_subjects = st.text_input(
            "📚 Subjects (comma separated)",
            value=existing.get("master_subjects", "") if existing else "",
            placeholder="e.g. Physics, Mathematics, Chemistry"
        )

        services = st.text_input(
            "🛠️ Services (comma separated)",
            value=existing.get("services", "") if existing else "",
            placeholder="e.g. One-on-one tutoring, Online sessions"
        )

        bio = st.text_area(
            "📝 About Yourself",
            value=existing.get("bio", "") if existing else "",
            height=120
        )

        submitted = st.form_submit_button(
            "💾 Save Profile",
            use_container_width=True
        )

        if submitted:
            data = {
                "full_name": user["full_name"],
                "qualification": qualification,
                "experience_yrs": experience,
                "master_subjects": master_subjects,
                "city": city,
                "contact_info": contact,
                "services": services,
                "hourly_rate": hourly_rate,
                "availability": availability,
                "bio": bio
            }
            if save_teacher_profile(user["id"], data):
                st.success("✅ Profile saved successfully!")
            else:
                st.error("❌ Could not save profile.")