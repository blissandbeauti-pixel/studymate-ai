# ============================================
# StudyMate AI - Authentication v2.0
# Student/Teacher signup, Terms, Password Reset
# ============================================

import streamlit as st
from database import (
    create_user, login_user,
    change_user_password,
    save_terms_acceptance,
    create_password_reset_token,
    reset_password_with_token,
    save_teacher_profile
)
from terms import show_terms_page, show_terms_checkbox

SUBJECTS = [
    "Mathematics", "Physics", "Chemistry", "Biology",
    "English", "Urdu", "Islamiat", "Pakistan Studies",
    "Computer Science", "Statistics", "Economics",
    "Anatomy", "Physiology", "Pharmacology",
    "Civil Engineering", "Electrical Engineering",
    "Mechanical Engineering", "Other"
]

CITIES = [
    "Lahore", "Karachi", "Islamabad", "Rawalpindi",
    "Faisalabad", "Multan", "Peshawar", "Quetta",
    "Sialkot", "Gujranwala", "Hyderabad", "Abbottabad",
    "Muzaffarabad", "Mirpur", "Other"
]


def show_auth_page():
    """Main authentication page"""

    # Check for password reset mode
    if st.session_state.get("reset_mode"):
        show_reset_password()
        return

    # Check for forgot password mode
    if st.session_state.get("forgot_mode"):
        show_forgot_password()
        return

    st.title("📚 StudyMate AI")
    st.subheader("Smart Study Companion for Pakistani Students")
    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "🔑 Login",
        "📝 Sign Up",
        "📋 Terms & Conditions"
    ])

    # ── LOGIN ──
    with tab1:
        show_login()

    # ── SIGNUP ──
    with tab2:
        show_signup()

    # ── TERMS ──
    with tab3:
        show_terms_page(standalone=False)


def show_login():
    """Login form"""
    st.markdown("### Welcome Back! 👋")
    st.write("")

    email = st.text_input(
        "📧 Email",
        key="login_email",
        placeholder="your@email.com"
    )
    password = st.text_input(
        "🔒 Password",
        type="password",
        key="login_password",
        placeholder="Enter password"
    )
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "🔑 Login",
            use_container_width=True,
            key="login_btn"
        ):
            if not email.strip() or not password.strip():
                st.error("❌ Please fill all fields.")
            else:
                success, user, message = login_user(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

    with col2:
        if st.button(
            "🔐 Forgot Password?",
            use_container_width=True,
            key="forgot_btn"
        ):
            st.session_state.forgot_mode = True
            st.rerun()


def show_signup():
    """Signup form with student/teacher selection"""
    st.markdown("### Create Your Account 🎓")
    st.write("")

    # Account type selection
    account_type = st.radio(
        "I am a:",
        ["👨‍🎓 Student", "👨‍🏫 Teacher / Tutor"],
        horizontal=True,
        key="signup_account_type"
    )
    is_teacher = "Teacher" in account_type

    st.divider()

    # Basic info
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input(
            "👤 Full Name",
            key="signup_name",
            placeholder="Muhammad Ahmed"
        )
    with col2:
        signup_email = st.text_input(
            "📧 Email",
            key="signup_email",
            placeholder="your@email.com"
        )

    col3, col4 = st.columns(2)
    with col3:
        signup_pwd = st.text_input(
            "🔒 Password",
            type="password",
            key="signup_pwd",
            placeholder="Min 8 characters"
        )
    with col4:
        confirm_pwd = st.text_input(
            "🔒 Confirm Password",
            type="password",
            key="confirm_pwd",
            placeholder="Repeat password"
        )

    # Teacher extra fields
    teacher_data = {}
    if is_teacher:
        st.divider()
        st.markdown("### 👨‍🏫 Teacher Profile Details")
        st.markdown("""
        <div style='background:#E3F2FD; border-radius:8px;
        padding:10px 15px; font-size:12px; color:#1565C0;
        margin-bottom:10px'>
            ℹ️ This information will be visible to students
            looking for tutors. Please provide accurate details.
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            teacher_data["qualification"] = st.text_input(
                "🎓 Highest Qualification",
                placeholder="e.g. MBBS, BSc Engineering, MSc Physics",
                key="t_qual"
            )
            teacher_data["city"] = st.selectbox(
                "📍 City", CITIES, key="t_city"
            )
            teacher_data["experience_yrs"] = st.number_input(
                "📅 Years of Experience",
                min_value=0, max_value=50, value=1,
                key="t_exp"
            )

        with col2:
            teacher_data["hourly_rate"] = st.text_input(
                "💰 Fee per Hour (PKR)",
                placeholder="e.g. 500-1000 or Negotiable",
                key="t_rate"
            )
            teacher_data["availability"] = st.selectbox(
                "⏰ Availability",
                [
                    "Weekdays only", "Weekends only",
                    "Both weekdays & weekends",
                    "Evenings only", "Flexible"
                ],
                key="t_avail"
            )
            teacher_data["contact_info"] = st.text_input(
                "📱 Contact (WhatsApp preferred)",
                placeholder="03XX-XXXXXXX",
                key="t_contact"
            )

        teacher_data["master_subjects"] = st.multiselect(
            "📚 Subjects You Teach",
            SUBJECTS,
            key="t_subjects"
        )

        teacher_data["services"] = st.multiselect(
            "🛠️ Services Offered",
            [
                "One-on-one tutoring",
                "Group classes",
                "Online sessions",
                "Home tuition",
                "Exam preparation",
                "Assignment help",
                "Test preparation (MDCAT/ECAT)",
                "University admission guidance"
            ],
            key="t_services"
        )

        teacher_data["bio"] = st.text_area(
            "📝 About Yourself",
            placeholder=(
                "Briefly describe your teaching experience, "
                "methodology, and why students should choose you..."
            ),
            height=100,
            key="t_bio"
        )

    # Terms agreement
    st.divider()
    st.markdown("#### 📋 Terms & Conditions")
    with st.expander("Read Terms & Conditions"):
        show_terms_page(standalone=False)

    agreed = show_terms_checkbox()

    st.write("")

    if st.button(
        "📝 Create Account",
        use_container_width=True,
        key="signup_btn"
    ):
        errors = []

        # Validate basic fields
        if not full_name.strip():
            errors.append("Full name required")
        if not signup_email.strip():
            errors.append("Email required")
        if len(signup_pwd) < 8:
            errors.append("Password must be at least 8 characters")
        if signup_pwd != confirm_pwd:
            errors.append("Passwords do not match")
        if not agreed:
            errors.append("You must agree to Terms & Conditions")

        # Validate teacher fields
        if is_teacher:
            if not teacher_data.get("qualification", "").strip():
                errors.append("Qualification required for teacher account")
            if not teacher_data.get("master_subjects"):
                errors.append("Select at least one subject you teach")
            if not teacher_data.get("contact_info", "").strip():
                errors.append("Contact information required")
            if not teacher_data.get("bio", "").strip():
                errors.append("About yourself is required")

        if errors:
            for e in errors:
                st.error(f"❌ {e}")
        else:
            acc_type = "teacher" if is_teacher else "student"
            success, user_id, message = create_user(
                full_name, signup_email, signup_pwd,
                program="", institution=""
            )

            if success:
                # Save terms acceptance
                save_terms_acceptance(user_id)

                # Save teacher profile
                if is_teacher and user_id:
                    teacher_data["full_name"] = full_name
                    teacher_data["master_subjects"] = ", ".join(
                        teacher_data.get("master_subjects", [])
                    )
                    teacher_data["services"] = ", ".join(
                        teacher_data.get("services", [])
                    )
                    save_teacher_profile(user_id, teacher_data)

                st.success(
                    "✅ Account created successfully! "
                    "Please login."
                )
                if is_teacher:
                    st.info(
                        "👨‍🏫 Your teacher profile has been submitted "
                        "and will be visible in the Community section."
                    )
            else:
                st.error(f"❌ {message}")


def show_forgot_password():
    """Forgot password flow"""
    st.title("🔐 Forgot Password")
    st.divider()

    st.markdown("""
    <div style='background:#E3F2FD; border-radius:10px;
    padding:15px 20px; font-size:13px; color:#1565C0;
    margin-bottom:15px'>
        Enter your registered email address. You will receive
        a password reset code to enter below.
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "📧 Registered Email",
        placeholder="your@email.com",
        key="forgot_email"
    )

    if st.button("📨 Get Reset Code", use_container_width=True):
        if not email.strip():
            st.error("❌ Please enter your email.")
        else:
            success, token, message = create_password_reset_token(email)
            if success:
                # Store token in session
                st.session_state.reset_token = token
                st.session_state.forgot_mode = False
                st.session_state.reset_mode = True
                st.success(
                    "✅ Reset code generated! "
                    "In a real deployment this would be emailed. "
                    "For now, use the code below to reset."
                )
                st.code(token, language=None)
                st.info(
                    "📋 Copy this code and click Continue to reset password."
                )
                if st.button("Continue to Reset →"):
                    st.rerun()
            else:
                st.error(f"❌ {message}")

    st.write("")
    if st.button("← Back to Login"):
        st.session_state.forgot_mode = False
        st.rerun()


def show_reset_password():
    """Reset password with token"""
    st.title("🔐 Reset Password")
    st.divider()

    token = st.text_input(
        "🔑 Reset Code",
        placeholder="Paste your reset code here",
        key="reset_token_input"
    )
    new_pwd = st.text_input(
        "🔒 New Password",
        type="password",
        key="reset_new_pwd",
        placeholder="Min 8 characters"
    )
    confirm_new_pwd = st.text_input(
        "🔒 Confirm New Password",
        type="password",
        key="reset_confirm_pwd",
        placeholder="Repeat new password"
    )

    st.write("")
    if st.button("✅ Reset Password", use_container_width=True):
        errors = []
        if not token.strip():
            errors.append("Reset code required")
        if len(new_pwd) < 8:
            errors.append("Password must be at least 8 characters")
        if new_pwd != confirm_new_pwd:
            errors.append("Passwords do not match")

        if errors:
            for e in errors:
                st.error(f"❌ {e}")
        else:
            success, message = reset_password_with_token(
                token, new_pwd
            )
            if success:
                st.success(
                    "✅ Password reset successfully! "
                    "Please login with your new password."
                )
                st.session_state.reset_mode = False
                st.rerun()
            else:
                st.error(f"❌ {message}")

    if st.button("← Back to Login"):
        st.session_state.reset_mode = False
        st.rerun()


def show_change_password(user_id):
    """Change password form for logged-in users"""
    st.markdown("### 🔒 Change Password")

    old_pwd = st.text_input(
        "Current Password",
        type="password",
        key="change_old_pwd"
    )
    new_pwd = st.text_input(
        "New Password",
        type="password",
        key="change_new_pwd",
        placeholder="Min 8 characters"
    )
    confirm_new = st.text_input(
        "Confirm New Password",
        type="password",
        key="change_confirm_pwd"
    )

    if st.button("✅ Update Password", use_container_width=True):
        errors = []
        if not old_pwd:
            errors.append("Current password required")
        if len(new_pwd) < 8:
            errors.append("New password must be at least 8 characters")
        if new_pwd != confirm_new:
            errors.append("Passwords do not match")

        if errors:
            for e in errors:
                st.error(f"❌ {e}")
        else:
            success, message = change_user_password(
                user_id, old_pwd, new_pwd
            )
            if success:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")