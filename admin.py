# ============================================
# StudyMate AI - Admin Panel
# ============================================

import streamlit as st
import io
import csv
from datetime import datetime, date
from database import (
    get_all_users, get_all_suggestions,
    get_full_stats, delete_user,
    get_past_papers, save_past_paper
)
from database import (
    get_all_users, get_all_suggestions,
    get_full_stats, delete_user,
    get_past_papers, save_past_paper,
    save_admin_note, get_admin_notes,
    delete_admin_note
)


# ============================================
# ADMIN STYLES
# ============================================

ADMIN_STYLE = """
<style>
    .admin-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 5px solid #1565C0;
    }
    .admin-stat {
        background: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .user-row {
        background: white;
        border-radius: 8px;
        padding: 12px 15px;
        margin: 5px 0;
        border-left: 3px solid #42A5F5;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        font-size: 13px;
    }
    .suggestion-card {
        background: white;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 8px 0;
        border-left: 4px solid #7B1FA2;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .admin-header {
        background: linear-gradient(135deg, #1565C0, #42A5F5);
        color: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .danger-zone {
        background: #FFF3F3;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #FFCDD2;
        margin-top: 10px;
    }
</style>
"""


# ============================================
# CSV EXPORT HELPERS
# ============================================

def export_users_csv(users):
    """Export users to CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Full Name", "Email", "Program",
        "Institution", "Sessions", "Tests",
        "Avg Score", "Joined"
    ])
    for u in users:
        writer.writerow([
            u["id"], u["full_name"], u["email"],
            u.get("program", ""), u.get("institution", ""),
            u.get("total_sessions", 0), u.get("total_tests", 0),
            round(u.get("avg_score", 0), 1),
            u["created_at"][:10]
        ])
    return output.getvalue().encode("utf-8")


def export_suggestions_csv(suggestions):
    """Export suggestions to CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "User", "Category", "Message", "Date"
    ])
    for s in suggestions:
        writer.writerow([
            s["id"], s["user_name"], s["category"],
            s["message"], s["created_at"][:16]
        ])
    return output.getvalue().encode("utf-8")


# ============================================
# 1. ADMIN DASHBOARD
# ============================================

def show_admin_dashboard():
    """Main admin statistics"""
    stats = get_full_stats()

    st.markdown(f"""
    <div class="admin-header">
        <h2>📊 StudyMate AI — Admin Dashboard</h2>
        <p style='margin:0; opacity:0.9'>
            {datetime.now().strftime('%A, %d %B %Y — %I:%M %p')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Main stats
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    metrics = [
        (c1, "👥 Users",       stats["total_users"],              "#1565C0"),
        (c2, "📖 Sessions",    stats["total_sessions"],           "#2E7D32"),
        (c3, "❓ MCQs",        f"{stats['total_mcqs']:,}",        "#7B1FA2"),
        (c4, "📝 Tests",       stats["total_tests"],              "#E65100"),
        (c5, "💬 Suggestions", stats["total_suggestions"],        "#00838F"),
        (c6, "⭐ Avg Score",   f"{stats['overall_avg']}%",        "#C62828"),
    ]
    for col, label, value, color in metrics:
        with col:
            st.markdown(f"""
            <div class="admin-stat">
                <div style='font-size:11px; color:gray'>{label}</div>
                <div style='font-size:22px; font-weight:bold;
                color:{color}'>{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 📈 Daily Sessions (Last 7 Days)")
        if stats["daily_sessions"]:
            import pandas as pd
            df = pd.DataFrame(stats["daily_sessions"])
            df.columns = ["Date", "Sessions", "MCQs"]
            st.bar_chart(df.set_index("Date")["Sessions"])
        else:
            st.info("No session data yet.")

    with col_right:
        st.markdown("#### 🎓 Top Programs")
        if stats["top_programs"]:
            import pandas as pd
            df = pd.DataFrame(stats["top_programs"])
            df.columns = ["Program", "Count"]
            df["Program"] = df["Program"].str[:20]
            st.bar_chart(df.set_index("Program"))
        else:
            st.info("No program data yet.")

    st.write("")
    st.markdown(f"""
    <div class="admin-card">
        🏆 <b>Most Popular Subject:</b>
        <span style='color:#1565C0; font-size:16px'>
            &nbsp;{stats['top_subject']}
        </span>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# 2. USER MANAGEMENT
# ============================================

def show_user_management():
    """View and manage all users"""
    st.markdown("### 👥 User Management")

    users = get_all_users(limit=200)

    search = st.text_input(
        "🔍 Search by name or email",
        placeholder="Type to search..."
    )
    if search.strip():
        users = [
            u for u in users
            if search.lower() in u["full_name"].lower()
            or search.lower() in u["email"].lower()
        ]

    st.markdown(f"**Total: {len(users)} students**")

    if users:
        csv_data = export_users_csv(users)
        st.download_button(
            "📥 Export Users CSV",
            data=csv_data,
            file_name=f"studymate_users_{date.today()}.csv",
            mime="text/csv"
        )

    st.divider()

    for u in users:
        with st.expander(
            f"👤 {u['full_name']} | {u['email']} | "
            f"Joined: {u['created_at'][:10]}"
        ):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Sessions", u.get("total_sessions", 0))
            with col2:
                st.metric("Tests", u.get("total_tests", 0))
            with col3:
                st.metric(
                    "Avg Score",
                    f"{round(u.get('avg_score', 0), 1)}%"
                )
            with col4:
                st.metric("User ID", u["id"])

            st.markdown(f"""
            <div class="user-row">
                🎓 <b>Program:</b>
                {u.get('program', 'Not set')} &nbsp;|&nbsp;
                🏫 <b>Institution:</b>
                {u.get('institution', 'Not set')}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="danger-zone">
                ⚠️ <b>Danger Zone</b>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                f"🗑️ Delete User #{u['id']}",
                key=f"del_{u['id']}"
            ):
                if delete_user(u["id"]):
                    st.success("✅ User deleted.")
                    st.rerun()
                else:
                    st.error("❌ Could not delete user.")


# ============================================
# 3. SUGGESTIONS
# ============================================

def show_suggestions():
    """View all user suggestions"""
    st.markdown("### 💬 User Suggestions")

    suggestions = get_all_suggestions(limit=200)

    categories = list(set(
        s["category"] for s in suggestions
    )) if suggestions else []
    categories.insert(0, "All Categories")

    selected_cat = st.selectbox("Filter by Category", categories)
    if selected_cat != "All Categories":
        suggestions = [
            s for s in suggestions
            if s["category"] == selected_cat
        ]

    st.markdown(f"**Total: {len(suggestions)} suggestions**")

    if suggestions:
        csv_data = export_suggestions_csv(suggestions)
        st.download_button(
            "📥 Export Suggestions CSV",
            data=csv_data,
            file_name=f"studymate_suggestions_{date.today()}.csv",
            mime="text/csv"
        )

    st.divider()

    cat_colors = {
        "New Feature Request":     "#1565C0",
        "Bug Report":              "#C62828",
        "Content Suggestion":      "#2E7D32",
        "University/Board to Add": "#E65100",
        "Program to Add":          "#7B1FA2",
        "General Feedback":        "#00838F"
    }

    for s in suggestions:
        color = cat_colors.get(s["category"], "#757575")
        st.markdown(f"""
        <div class="suggestion-card"
        style="border-left-color:{color}">
            <div style='display:flex; justify-content:space-between'>
                <b style='color:{color}'>{s['category']}</b>
                <small style='color:gray'>
                    {s['created_at'][:16]}
                </small>
            </div>
            <div style='margin:6px 0; font-size:14px'>
                {s['message']}
            </div>
            <small style='color:gray'>
                👤 {s['user_name']}
            </small>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# 4. PAST PAPERS MANAGEMENT
# ============================================

def show_past_papers_admin():
    """Admin: Upload and manage past papers"""
    st.markdown("### 📄 Past Papers Management")

    with st.expander("➕ Upload New Past Paper", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            pp_title = st.text_input(
                "📋 Paper Title",
                placeholder="e.g. MDCAT Biology 2023"
            )
            pp_board = st.text_input(
                "🏫 Board/University",
                placeholder="e.g. PMC, FBISE, NUMS"
            )
            pp_program = st.text_input(
                "🎓 Program",
                placeholder="e.g. FSc Pre-Medical"
            )
        with col2:
            pp_subject = st.text_input(
                "📖 Subject",
                placeholder="e.g. Biology"
            )
            pp_year = st.text_input(
                "📅 Year",
                placeholder="e.g. 2023"
            )
            pp_type = st.selectbox(
                "📑 Paper Type",
                [
                    "Annual Exam", "Entry Test",
                    "Mid-Term", "Mock Test",
                    "Practice Paper", "Other"
                ]
            )

        uploaded_file = st.file_uploader(
            "📁 Upload PDF",
            type=["pdf"],
            key="admin_paper_upload"
        )

        if st.button("💾 Save Past Paper", use_container_width=True):
            if not pp_title.strip():
                st.error("❌ Please enter paper title.")
            elif uploaded_file is None:
                st.error("❌ Please upload a PDF file.")
            else:
                import os
                os.makedirs("past_papers", exist_ok=True)
                file_path = f"past_papers/{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                saved = save_past_paper(
                    pp_title, pp_board, pp_program,
                    pp_subject, pp_year, pp_type,
                    file_path, "Admin"
                )
                if saved:
                    st.success("✅ Past paper uploaded successfully!")
                    st.rerun()
                else:
                    st.error("❌ Could not save paper.")

    st.divider()

    papers = get_past_papers()
    st.markdown(f"**Total Papers: {len(papers)}**")

    if not papers:
        st.info("No past papers uploaded yet.")
        return

    for p in papers:
        st.markdown(f"""
        <div class="admin-card">
            <b>📄 {p['title']}</b> ({p['year']})<br>
            <small style='color:gray'>
                🏫 {p['board']} | 🎓 {p['program']} |
                📖 {p['subject']} | 📑 {p['paper_type']} |
                📅 {p['created_at'][:10]}
            </small>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# 5. SUB-ADMIN MANAGEMENT
# ← Must be defined BEFORE show_admin_page()
# ============================================

def show_sub_admin_management(current_admin):
    """Master admin manages sub-admins"""
    from database import (
        get_all_admins, get_all_roles,
        create_sub_admin, toggle_admin_status,
        master_change_admin_password,
        change_admin_password
    )

    is_master = current_admin.get("is_master", 0)
    st.markdown("### 🛡️ Admin Management")

    # ── Change own password ──
    with st.expander("🔒 Change My Password"):
        old = st.text_input(
            "Current Password",
            type="password",
            key="adm_old_pwd"
        )
        new = st.text_input(
            "New Password",
            type="password",
            key="adm_new_pwd"
        )
        confirm = st.text_input(
            "Confirm New Password",
            type="password",
            key="adm_confirm_pwd"
        )
        if st.button("✅ Update Password", key="adm_pwd_btn"):
            if new != confirm:
                st.error("❌ Passwords do not match.")
            elif len(new) < 8:
                st.error("❌ Minimum 8 characters required.")
            else:
                changed = change_admin_password(
                    current_admin["id"], old, new
                )
                if changed:
                    st.success("✅ Password changed successfully!")
                else:
                    st.error("❌ Current password is incorrect.")

    st.divider()

    # ── Sub-admin section (master only) ──
    if not is_master:
        st.info(
            "🔒 Only Master Admin can create or manage "
            "sub-admin accounts."
        )
        return

    # Create sub-admin form
    with st.expander("➕ Create New Sub-Admin"):
        roles = get_all_roles()
        if not roles:
            st.warning("No roles found in database.")
            return

        role_names = {r["role_name"]: r["id"] for r in roles}

        col1, col2 = st.columns(2)
        with col1:
            sa_username = st.text_input(
                "👤 Username", key="sa_username",
                placeholder="e.g. content_manager"
            )
            sa_name = st.text_input(
                "📛 Full Name", key="sa_name",
                placeholder="e.g. Ali Hassan"
            )
            sa_email = st.text_input(
                "📧 Email", key="sa_email",
                placeholder="sub@studymate.ai"
            )
        with col2:
            sa_pwd = st.text_input(
                "🔒 Password",
                type="password",
                key="sa_pwd",
                placeholder="Min 8 characters"
            )
            sa_role = st.selectbox(
                "🛡️ Role",
                list(role_names.keys()),
                key="sa_role"
            )

        # Show role permissions preview
        selected_role = next(
            (r for r in roles if r["role_name"] == sa_role),
            None
        )
        if selected_role:
            perms = []
            if selected_role["can_view_stats"]:
                perms.append("✅ View Stats")
            if selected_role["can_manage_users"]:
                perms.append("✅ Manage Users")
            if selected_role["can_manage_papers"]:
                perms.append("✅ Manage Past Papers")
            if selected_role["can_manage_teachers"]:
                perms.append("✅ Verify Teachers")
            if selected_role["can_manage_admins"]:
                perms.append("✅ Manage Admins")
            st.markdown(
                f"**Permissions:** {' | '.join(perms)}"
            )

        if st.button(
            "✅ Create Sub-Admin",
            use_container_width=True,
            key="create_sa_btn"
        ):
            if not sa_username or not sa_name or not sa_pwd:
                st.error("❌ Fill all required fields.")
            elif len(sa_pwd) < 8:
                st.error("❌ Password must be at least 8 characters.")
            else:
                success, msg = create_sub_admin(
                    sa_username, sa_name, sa_email,
                    sa_pwd, role_names[sa_role],
                    current_admin["id"]
                )
                if success:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    st.divider()

    # List all admins
    st.markdown("#### 📋 All Admin Accounts")
    admins = get_all_admins()

    if not admins:
        st.info("No admin accounts found.")
        return

    for a in admins:
        badge = (
            "🔴 MASTER ADMIN"
            if a["is_master"]
            else f"🔵 {a.get('role_name', 'No Role')}"
        )
        status_color = "#2E7D32" if a["is_active"] else "#757575"

        with st.expander(
            f"{badge} | {a['full_name']} (@{a['username']})"
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **Username:** {a['username']}<br>
                **Full Name:** {a['full_name']}<br>
                **Email:** {a.get('email', 'N/A')}<br>
                **Role:** {a.get('role_name', 'Master Admin')}<br>
                **Created:** {a['created_at'][:10]}
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div style='color:{status_color};
                font-weight:bold; margin-bottom:10px'>
                    Status: {"✅ Active" if a["is_active"] else "❌ Inactive"}
                </div>
                """, unsafe_allow_html=True)

                # Master admin cannot be modified
                if a["is_master"]:
                    st.info("🔒 Master Admin — cannot be modified.")
                    continue

                # Toggle active/inactive
                if st.button(
                    "🔄 Toggle Active/Inactive",
                    key=f"toggle_{a['id']}"
                ):
                    toggle_admin_status(a["id"])
                    st.rerun()

                # Reset password
                new_pwd = st.text_input(
                    "🔑 Reset Password",
                    type="password",
                    key=f"reset_pwd_{a['id']}",
                    placeholder="Enter new password"
                )
                if st.button(
                    "🔑 Reset Password",
                    key=f"reset_btn_{a['id']}"
                ):
                    if len(new_pwd) >= 8:
                        master_change_admin_password(
                            a["id"], new_pwd
                        )
                        st.success("✅ Password reset successfully!")
                    else:
                        st.error("❌ Minimum 8 characters required.")

# ============================================
# ADMIN NOTES MANAGEMENT
# ============================================

def show_notes_admin():
    """Admin: Upload and manage study notes"""
    st.markdown("### 📝 Study Notes Management")

    st.markdown("""
    <div style='background:#E3F2FD; border-radius:8px;
    padding:10px 15px; font-size:13px; color:#1565C0;
    margin-bottom:15px; border-left:4px solid #1565C0'>
        ℹ️ Upload study notes, handouts, summaries or
        any reference material for students.
        Supported: PDF, Word (.docx), Images, Text files.
    </div>
    """, unsafe_allow_html=True)

    # ── Upload Form ──
    with st.expander("➕ Upload New Notes", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            note_title = st.text_input(
                "📋 Title",
                placeholder="e.g. Cardiovascular System Notes"
            )
            note_subject = st.text_input(
                "📖 Subject",
                placeholder="e.g. Anatomy, Physics"
            )
            note_program = st.text_input(
                "🎓 Program",
                placeholder="e.g. BSN Nursing, FSc Pre-Medical"
            )
            note_board = st.text_input(
                "🏫 Board / University",
                placeholder="e.g. FBISE, KEMU, General"
            )
        with col2:
            note_year = st.selectbox(
                "📅 Year / Semester",
                [
                    "All Years",
                    "1st Year / Semester 1",
                    "1st Year / Semester 2",
                    "2nd Year / Semester 3",
                    "2nd Year / Semester 4",
                    "3rd Year / Semester 5",
                    "3rd Year / Semester 6",
                    "4th Year / Semester 7",
                    "4th Year / Semester 8",
                ]
            )
            note_topic = st.text_input(
                "🔍 Topic / Chapter",
                placeholder="e.g. Heart Structure, Thermodynamics"
            )
            note_description = st.text_area(
                "📝 Description (optional)",
                placeholder=(
                    "Brief description of what these "
                    "notes cover..."
                ),
                height=80
            )

        uploaded_note = st.file_uploader(
            "📁 Upload File",
            type=["pdf", "docx", "doc", "txt",
                  "png", "jpg", "jpeg"],
            key="admin_note_upload",
            help="Max file size: 200MB"
        )

        if uploaded_note:
            file_size = len(uploaded_note.getvalue()) / 1024
            st.caption(
                f"📎 {uploaded_note.name} "
                f"({file_size:.1f} KB) — "
                f"Type: {uploaded_note.type}"
            )

        if st.button(
            "💾 Upload Notes",
            use_container_width=True,
            key="upload_notes_btn"
        ):
            errors = []
            if not note_title.strip():
                errors.append("Title is required")
            if not note_subject.strip():
                errors.append("Subject is required")
            if uploaded_note is None:
                errors.append("Please select a file to upload")

            if errors:
                for e in errors:
                    st.error(f"❌ {e}")
            else:
                import os
                os.makedirs("admin_notes", exist_ok=True)

                # Safe filename
                safe_name = uploaded_note.name.replace(
                    " ", "_"
                )
                file_path = f"admin_notes/{safe_name}"

                with open(file_path, "wb") as f:
                    f.write(uploaded_note.getbuffer())

                # Determine file type label
                ext = uploaded_note.name.split(".")[-1].lower()
                type_labels = {
                    "pdf":  "PDF Document",
                    "docx": "Word Document",
                    "doc":  "Word Document",
                    "txt":  "Text File",
                    "png":  "Image",
                    "jpg":  "Image",
                    "jpeg": "Image",
                }
                file_type = type_labels.get(ext, "File")

                saved = save_admin_note(
                    title       = note_title.strip(),
                    subject     = note_subject.strip(),
                    program     = note_program.strip(),
                    board       = note_board.strip(),
                    year        = note_year,
                    topic       = note_topic.strip(),
                    description = note_description.strip(),
                    file_path   = file_path,
                    file_type   = file_type,
                    uploaded_by = "Admin"
                )

                if saved:
                    st.success(
                        f"✅ '{note_title}' uploaded successfully!"
                    )
                    st.rerun()
                else:
                    st.error("❌ Could not save. Please try again.")

    st.divider()

    # ── Filter & View ──
    st.markdown("#### 📚 All Uploaded Notes")

    col1, col2, col3 = st.columns(3)
    with col1:
        f_subject = st.text_input(
            "🔍 Filter by Subject",
            placeholder="e.g. Biology",
            key="filter_note_subject"
        )
    with col2:
        f_program = st.text_input(
            "🎓 Filter by Program",
            placeholder="e.g. BSN",
            key="filter_note_program"
        )
    with col3:
        f_topic = st.text_input(
            "🔍 Filter by Topic",
            placeholder="e.g. Nervous System",
            key="filter_note_topic"
        )

    notes = get_admin_notes(
        program = f_program if f_program else None,
        subject = f_subject if f_subject else None,
        topic   = f_topic   if f_topic   else None,
    )

    st.markdown(f"**Total: {len(notes)} notes uploaded**")
    st.divider()

    if not notes:
        st.info("No notes uploaded yet.")
        return

    # File type icons
    type_icons = {
        "PDF Document":  "📄",
        "Word Document": "📝",
        "Text File":     "📃",
        "Image":         "🖼️",
        "File":          "📁",
    }

    for n in notes:
        icon = type_icons.get(n.get("file_type", ""), "📁")

        with st.expander(
            f"{icon} {n['title']}  |  "
            f"{n['subject']}  |  "
            f"{n['created_at'][:10]}"
        ):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="admin-card">
                    <b>{icon} {n['title']}</b><br>
                    <small style='color:gray; line-height:2'>
                        📖 Subject: <b>{n['subject']}</b> &nbsp;|&nbsp;
                        🔍 Topic: {n.get('topic','—')}<br>
                        🎓 Program: {n.get('program','—')} &nbsp;|&nbsp;
                        🏫 Board: {n.get('board','—')}<br>
                        📅 Year: {n.get('year','—')} &nbsp;|&nbsp;
                        📁 Type: {n.get('file_type','—')} &nbsp;|&nbsp;
                        ⬇️ Downloads: {n.get('downloads',0)}<br>
                        🗓️ Uploaded: {n['created_at'][:16]}
                    </small>
                    {f"<br><small style='color:#555'>{n['description']}</small>" if n.get('description') else ""}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.write("")
                # Download button
                try:
                    with open(n["file_path"], "rb") as f:
                        file_bytes = f.read()
                    st.download_button(
                        "📥 Download",
                        data=file_bytes,
                        file_name=n["file_path"].split("/")[-1],
                        use_container_width=True,
                        key=f"dl_note_{n['id']}"
                    )
                except FileNotFoundError:
                    st.warning("File not found on disk.")

                st.write("")

                # Delete button
                if st.button(
                    "🗑️ Delete",
                    key=f"del_note_{n['id']}",
                    use_container_width=True
                ):
                    # Delete file from disk too
                    import os
                    try:
                        if os.path.exists(n["file_path"]):
                            os.remove(n["file_path"])
                    except Exception:
                        pass
                    if delete_admin_note(n["id"]):
                        st.success("✅ Deleted.")
                        st.rerun()
                    else:
                        st.error("❌ Could not delete.")
# ============================================
# 6. MAIN ADMIN PAGE ENTRY POINT
# ← Must be defined LAST
# ============================================

def show_admin_page():
    """Main admin panel entry point"""
    st.markdown(ADMIN_STYLE, unsafe_allow_html=True)

    # Initialize session state
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    # ── Login Screen ──
    if not st.session_state.admin_logged_in:
        st.markdown("""
        <div class="admin-header">
            <h2>🔐 Admin Panel</h2>
            <p style='margin:0; opacity:0.9'>
                StudyMate AI — Administration
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input(
                "👤 Admin Username",
                placeholder="Enter username",
                key="admin_login_user"
            )
            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter password",
                key="admin_login_pwd"
            )
            st.write("")

            if st.button(
                "🔐 Login as Admin",
                use_container_width=True,
                key="admin_login_btn"
            ):
                from database import login_admin_v2
                success, admin, message = login_admin_v2(
                    username, password
                )
                if success:
                    st.session_state.admin_logged_in = True
                    st.session_state.admin = admin
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

            st.markdown("""
            <div style='text-align:center; font-size:12px;
            color:gray; margin-top:10px'>
                Master Admin: admin / Wru@studymate4me<br>
                ⚠️ Please change password after first login
            </div>
            """, unsafe_allow_html=True)
        return

    # ── Admin is Logged In ──
    admin = st.session_state.admin

    col1, col2 = st.columns([4, 1])
    with col1:
        is_master = admin.get("is_master", 0)
        badge = "🔴 Master Admin" if is_master else "🔵 Sub-Admin"
        st.markdown(f"## 🛡️ Admin Panel &nbsp; `{badge}`")
    with col2:
        st.write("")
        if st.button("🚪 Logout", key="admin_logout_btn"):
            st.session_state.admin_logged_in = False
            st.session_state.admin = None
            st.rerun()

    st.divider()

    # ── Admin Tabs ──
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard",
        "👥 Users",
        "🛡️ Sub-Admins",
        "💬 Suggestions",
        "📝 Notes",
        "📄 Past Papers"
    ])

    with tab1:
        show_admin_dashboard()
    with tab2:
        show_user_management()
    with tab3:
        show_sub_admin_management(admin)
    with tab4:
        show_suggestions()
    with tab5:
        show_notes_admin()
    with tab6:
        show_past_papers_admin()