# ============================================
# StudyMate AI - Authentication UI
# Login & Signup Forms
# ============================================

import streamlit as st
from database import create_user, login_user


def show_auth_page():
    """Show login/signup page"""

    st.title("📚 StudyMate AI")
    st.subheader("Smart Study Companion for Pakistani Students")
    st.divider()

    # Tab selection
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    # ─────────────────────────────
    # LOGIN TAB
    # ─────────────────────────────
    with tab1:
        st.markdown("### Welcome Back!")
        st.markdown("Login to continue your learning journey.")
        st.write("")

        email = st.text_input(
            "📧 Email Address",
            key="login_email",
            placeholder="your@email.com"
        )
        password = st.text_input(
            "🔒 Password",
            type="password",
            key="login_password",
            placeholder="Enter your password"
        )

        st.write("")

        if st.button("🔑 Login", use_container_width=True, key="login_btn"):
            if not email.strip() or not password.strip():
                st.error("❌ Please fill in all fields.")
            else:
                success, user, message = login_user(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success(f"✅ Welcome back, {user['full_name']}!")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

    # ─────────────────────────────
    # SIGNUP TAB
    # ─────────────────────────────
    with tab2:
        st.markdown("### Create Your Account")
        st.markdown("Join thousands of Pakistani students studying smarter.")
        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input(
                "👤 Full Name",
                key="signup_name",
                placeholder="Ahmed Khan"
            )
        with col2:
            signup_email = st.text_input(
                "📧 Email Address",
                key="signup_email",
                placeholder="your@email.com"
            )

        col3, col4 = st.columns(2)

        with col3:
            signup_password = st.text_input(
                "🔒 Password",
                type="password",
                key="signup_password",
                placeholder="Min 6 characters"
            )
        with col4:
            confirm_password = st.text_input(
                "🔒 Confirm Password",
                type="password",
                key="confirm_password",
                placeholder="Repeat password"
            )

        st.write("")

        if st.button("📝 Create Account", use_container_width=True, key="signup_btn"):
            # Validate
            errors = []
            if not full_name.strip():
                errors.append("Full name is required")
            if not signup_email.strip():
                errors.append("Email is required")
            if len(signup_password) < 6:
                errors.append("Password must be at least 6 characters")
            if signup_password != confirm_password:
                errors.append("Passwords do not match")

            if errors:
                for e in errors:
                    st.error(f"❌ {e}")
            else:
                success, user_id, message = create_user(
                    full_name, signup_email, signup_password
                )
                if success:
                    st.success("✅ Account created! Please login.")
                else:
                    st.error(f"❌ {message}")