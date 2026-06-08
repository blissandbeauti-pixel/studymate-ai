# ============================================
# StudyMate AI - Study Streak Tracker
# Daily goals, streaks, badges, calendar
# ============================================

import streamlit as st
from datetime import date, timedelta
from database import (
    get_streak, get_activity_calendar,
    get_user_stats, get_user_preferences,
    save_user_preferences, update_streak
)


# ============================================
# BADGE SYSTEM
# ============================================

def get_badges(streak_data, total_mcqs):
    """Calculate earned badges based on activity"""
    badges = []
    current = streak_data.get("current_streak", 0)
    longest = streak_data.get("longest_streak", 0)
    total   = streak_data.get("total_days", 0)

    if current >= 1:
        badges.append(("🌱", "First Step",      "Studied for 1 day"))
    if current >= 3:
        badges.append(("🔥", "On Fire",         "3-day streak!"))
    if current >= 7:
        badges.append(("⚡", "One Week",        "7-day streak!"))
    if current >= 14:
        badges.append(("🌟", "Two Weeks",       "14-day streak!"))
    if current >= 30:
        badges.append(("👑", "Champion",        "30-day streak!"))
    if longest >= 50:
        badges.append(("🏆", "Legend",          "50-day streak achieved!"))

    if total_mcqs >= 50:
        badges.append(("📝", "Quiz Starter",    "50 MCQs completed"))
    if total_mcqs >= 200:
        badges.append(("📚", "Quiz Master",     "200 MCQs completed"))
    if total_mcqs >= 500:
        badges.append(("🎓", "Scholar",         "500 MCQs completed"))
    if total_mcqs >= 1000:
        badges.append(("💎", "Diamond Scholar", "1000 MCQs completed"))

    if total >= 10:
        badges.append(("📅", "Consistent",      "10 days studied"))
    if total >= 30:
        badges.append(("🗓️", "Dedicated",       "30 days studied"))

    return badges


# ============================================
# MAIN STREAK PAGE
# ============================================

def show_streak_tracker(user):
    """Main streak tracker page"""

    update_streak(user["id"])

    language = st.session_state.get("language", "english")
    is_urdu  = language == "urdu"

    # ── Page Header ──
    title    = "🔥 مطالعہ اسٹریک" if is_urdu else "🔥 Study Streak"
    subtitle = (
        "اپنی روزانہ مطالعے کی عادت کو ٹریک کریں"
        if is_urdu else
        "Track your daily study habit and stay consistent"
    )

    st.markdown(
        f"<div style='background:linear-gradient(135deg,#E65100,#FF8F00);"
        f"border-radius:14px;padding:22px;color:white;text-align:center;"
        f"margin-bottom:20px'>"
        f"<h2 style='margin:0'>{title}</h2>"
        f"<p style='margin:8px 0 0;opacity:0.9;font-size:13px'>{subtitle}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ── Get Data ──
    streak_data = get_streak(user["id"])
    stats       = get_user_stats(user["id"])
    prefs       = get_user_preferences(user["id"])
    total_mcqs  = stats.get("total_mcqs", 0)
    daily_goal  = prefs.get("daily_goal", 20)

    current = streak_data.get("current_streak", 0)
    longest = streak_data.get("longest_streak", 0)
    total   = streak_data.get("total_days", 0)
    last    = streak_data.get("last_study_date", None)

    # ── Status Message ──
    today     = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    if last == today:
        status_msg   = "✅ آج آپ نے مطالعہ کیا! جاری رکھیں!" if is_urdu else "✅ You've studied today! Keep it up!"
        status_color = "#2E7D32"
    elif last == yesterday:
        status_msg   = "⚠️ اسٹریک بچانے کے لیے آج مطالعہ کریں!" if is_urdu else "⚠️ Study today to keep your streak alive!"
        status_color = "#E65100"
    else:
        status_msg   = "❌ اسٹریک شروع کرنے کے لیے مطالعہ شروع کریں!" if is_urdu else "❌ Start studying to begin your streak!"
        status_color = "#C62828"

    st.markdown(
        f"<div style='background:{status_color}15;border-left:4px solid {status_color};"
        f"border-radius:8px;padding:12px 16px;font-size:14px;color:{status_color};"
        f"font-weight:600;margin-bottom:16px'>{status_msg}</div>",
        unsafe_allow_html=True
    )

    # ── Stats Cards ──
    c1, c2, c3, c4 = st.columns(4)
    stats_items = [
        (c1, "🔥", str(current),       "موجودہ اسٹریک"  if is_urdu else "Current Streak",  "#E65100"),
        (c2, "🏆", str(longest),       "سب سے لمبی"      if is_urdu else "Longest Streak",  "#7B1FA2"),
        (c3, "📅", str(total),         "کل دن"           if is_urdu else "Total Days",       "#1565C0"),
        (c4, "❓", f"{total_mcqs:,}",  "مکمل MCQs"       if is_urdu else "MCQs Done",        "#2E7D32"),
    ]
    for col, icon, value, label, color in stats_items:
        with col:
            st.markdown(
                f"<div style='background:white;border-radius:12px;padding:18px 12px;"
                f"text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.08);"
                f"border-top:4px solid {color}'>"
                f"<div style='font-size:28px'>{icon}</div>"
                f"<div style='font-size:26px;font-weight:800;color:{color}'>{value}</div>"
                f"<div style='font-size:11px;color:gray;margin-top:4px'>{label}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.write("")

    # ── Flame Visualization ──
    st.markdown("### 🔥 اسٹریک" if is_urdu else "### 🔥 Streak")

    flames = min(current, 30)
    if flames > 0:
        flame_html = ""
        for i in range(flames):
            size    = 16 + min(i * 0.5, 12)
            opacity = 0.4 + min(i * 0.02, 0.6)
            flame_html += f"<span style='font-size:{size}px;opacity:{opacity}'>🔥</span>"

        st.markdown(
            f"<div style='line-height:2;letter-spacing:2px'>{flame_html}</div>",
            unsafe_allow_html=True
        )
        if current > 30:
            st.caption(f"... and {current - 30} more days! 🔥")
    else:
        st.markdown(
            "<div style='font-size:40px;opacity:0.3'>🔥</div>",
            unsafe_allow_html=True
        )
        st.caption(
            "اسٹریک شروع کرنے کے لیے مطالعہ شروع کریں!" if is_urdu
            else "Start studying to light your streak flame!"
        )

    st.write("")

    # ── Activity Calendar ──
    st.markdown("### 📅 گزشتہ 30 دن کی سرگرمی" if is_urdu else "### 📅 Last 30 Days Activity")

    active_dates = get_activity_calendar(user["id"], days=30)
    today_date   = date.today()

    # Build calendar — NO indentation inside HTML strings (prevents markdown code blocks)
    cal_html = "<div style='display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px'>"

    for i in range(29, -1, -1):
        d        = today_date - timedelta(days=i)
        d_str    = str(d)
        is_today = (d == today_date)
        active   = d_str in active_dates

        if active:
            bg = "#2E7D32"; fg = "white"; border = "#2E7D32"
        elif is_today:
            bg = "#E3F2FD"; fg = "#1565C0"; border = "#1565C0"
        else:
            bg = "#F5F5F5"; fg = "#AAAAAA"; border = "#E0E0E0"

        day_str = d.strftime("%d")
        mon_str = d.strftime("%b")

        # ⚠️ Key fix: NO leading whitespace/indentation in the HTML
        cal_html += (
            f"<div style='width:38px;height:38px;background:{bg};"
            f"border:1.5px solid {border};border-radius:6px;"
            f"display:flex;flex-direction:column;"
            f"align-items:center;justify-content:center;'>"
            f"<span style='font-size:9px;color:{fg};font-weight:600'>{day_str}</span>"
            f"<span style='font-size:8px;color:{fg};opacity:0.8'>{mon_str}</span>"
            f"</div>"
        )

    cal_html += "</div>"
    cal_html += (
        "<div style='font-size:11px;color:gray;margin-top:4px'>"
        "<span style='background:#2E7D32;color:white;"
        "padding:2px 8px;border-radius:4px'>Active</span>"
        "&nbsp;&nbsp;"
        "<span style='background:#E3F2FD;color:#1565C0;"
        "padding:2px 8px;border-radius:4px;border:1px solid #1565C0'>Today</span>"
        "&nbsp;&nbsp;"
        "<span style='background:#F5F5F5;color:#AAAAAA;"
        "padding:2px 8px;border-radius:4px'>Inactive</span>"
        "</div>"
    )

    st.markdown(cal_html, unsafe_allow_html=True)
    st.write("")

    # ── Daily Goal ──
    st.divider()
    st.markdown("### 🎯 روزانہ کا ہدف" if is_urdu else "### 🎯 Daily Goal")

    col1, col2 = st.columns([3, 1])
    with col1:
        new_goal = st.slider(
            "MCQs per day target",
            min_value=5, max_value=100,
            value=daily_goal, step=5,
            key="daily_goal_slider"
        )
    with col2:
        st.write("")
        st.write("")
        st.write("")
        if st.button("💾 Save Goal", use_container_width=True, key="save_goal_btn"):
            save_user_preferences(user["id"], language=language, daily_goal=new_goal)
            st.success("✅ Goal saved!")

    # Progress bar
    pct = min(int((total_mcqs / max(new_goal, 1)) * 100), 100)
    bar_color = "#2E7D32" if pct >= 100 else "#1565C0"
    done_msg  = "🎉 Goal completed!" if pct >= 100 else ""

    st.markdown(
        f"<div style='background:white;border-radius:10px;padding:14px 18px;"
        f"margin:8px 0;box-shadow:0 2px 6px rgba(0,0,0,0.06)'>"
        f"<div style='display:flex;justify-content:space-between;margin-bottom:8px'>"
        f"<span style='font-size:13px;font-weight:600'>Daily Progress</span>"
        f"<span style='font-size:13px;color:{bar_color};font-weight:700'>{pct}%</span>"
        f"</div>"
        f"<div style='background:#F0F0F0;border-radius:10px;height:10px;overflow:hidden'>"
        f"<div style='background:{bar_color};width:{pct}%;height:100%;border-radius:10px'></div>"
        f"</div>"
        f"<div style='font-size:11px;color:gray;margin-top:6px'>"
        f"Goal: {new_goal} MCQs/day &nbsp; {done_msg}"
        f"</div></div>",
        unsafe_allow_html=True
    )

    # ── Badges ──
    st.divider()
    st.markdown("### 🏅 آپ کے بیجز" if is_urdu else "### 🏅 Your Badges")

    badges = get_badges(streak_data, total_mcqs)
    if badges:
        # Build badge HTML with no indentation
        badge_html = "<div style='display:flex;flex-wrap:wrap;gap:10px'>"
        for icon, name, desc in badges:
            badge_html += (
                f"<div style='background:white;border-radius:10px;"
                f"padding:12px 16px;text-align:center;"
                f"box-shadow:0 2px 8px rgba(0,0,0,0.08);"
                f"border-top:3px solid #FFB300;min-width:100px'>"
                f"<div style='font-size:28px'>{icon}</div>"
                f"<div style='font-weight:700;font-size:12px;"
                f"color:#1B2A4A;margin:4px 0'>{name}</div>"
                f"<div style='font-size:10px;color:gray'>{desc}</div>"
                f"</div>"
            )
        badge_html += "</div>"
        st.markdown(badge_html, unsafe_allow_html=True)
    else:
        st.info(
            "🏅 بیجز حاصل کرنے کے لیے مطالعہ شروع کریں!" if is_urdu
            else "🏅 Start studying to earn your first badge!"
        )

    # ── Motivational Tip ──
    st.write("")
    if is_urdu:
        tip = "💡 مطالعہ جاری رکھیں — مسلسل محنت کامیابی کی کلید ہے!"
    elif current == 0:
        tip = "💡 Start today! Even 10 minutes of study counts towards your streak."
    elif current < 3:
        tip = "💡 Great start! Study tomorrow to keep building your streak."
    elif current < 7:
        tip = "💡 You're building momentum! Keep going through this week."
    elif current < 14:
        tip = "💡 One week streak! You're developing a powerful study habit."
    elif current < 30:
        tip = "💡 Incredible consistency! You're in the top 10% of students."
    else:
        tip = "💡 LEGENDARY! You are an inspiration to other students! 🌟"

    st.markdown(
        f"<div style='background:#E8F4FD;border-radius:10px;"
        f"padding:12px 16px;font-size:13px;color:#1565C0;"
        f"border-left:4px solid #1565C0'>{tip}</div>",
        unsafe_allow_html=True
    )