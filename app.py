"""
Content Calendar Planner — Light Version
Built for external testing via Streamlit Community Cloud.
Covers: Calendar View, Performance Tracker, AI Recommendations, Learnings Report.
"""

import streamlit as st
import pandas as pd
import json
from datetime import date, datetime, timedelta
import calendar as cal_lib
import plotly.express as px
import plotly.graph_objects as go
from data.config import CONFIGS, SAMPLE_POSTS, PLATFORMS, FORMATS, STATUSES, OUTCOMES, STATUS_COLORS, OUTCOME_COLORS
from data.holidays import get_holidays_for_month, get_holidays_for_date, HOLIDAY_TYPE_CONFIG

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Content Calendar Planner",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Nunito Sans', sans-serif; }

.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    color: white;
}
.main-header h1 { margin: 0; font-size: 1.8rem; font-weight: 700; }
.main-header p  { margin: 0.25rem 0 0; opacity: 0.75; font-size: 0.9rem; }

.metric-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.metric-card .value { font-size: 1.8rem; font-weight: 700; margin: 0; }
.metric-card .label { font-size: 0.75rem; color: #6b7280; margin: 0; }

.post-card {
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.6rem;
    background: white;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.holiday-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 2px 2px;
}
.pillar-bar {
    height: 4px;
    border-radius: 2px;
    margin-bottom: 0.5rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #f3f4f6;
}
.tip-box {
    background: #f0fdf4;
    border-left: 3px solid #22c55e;
    padding: 0.6rem 0.8rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.82rem;
    margin: 0.4rem 0;
}
.warning-box {
    background: #fefce8;
    border-left: 3px solid #eab308;
    padding: 0.6rem 0.8rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.82rem;
    margin: 0.4rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "business_type" not in st.session_state:
    st.session_state.business_type = "retail"
if "posts" not in st.session_state:
    st.session_state.posts = {
        "retail": list(SAMPLE_POSTS["retail"]),
        "airbnb": list(SAMPLE_POSTS["airbnb"]),
    }
if "current_year"  not in st.session_state: st.session_state.current_year  = 2026
if "current_month" not in st.session_state: st.session_state.current_month = 5
if "active_tab"    not in st.session_state: st.session_state.active_tab    = "📅 Calendar"
if "ai_preset_theme"   not in st.session_state: st.session_state.ai_preset_theme   = None
if "ai_preset_context" not in st.session_state: st.session_state.ai_preset_context = ""
# Editable holidays — seeded from static data, user can add/edit/delete at runtime
if "holidays" not in st.session_state:
    from data.holidays import HOLIDAYS_2026
    st.session_state.holidays = [dict(h) for h in HOLIDAYS_2026]

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_config():
    return CONFIGS[st.session_state.business_type]

def get_posts():
    return st.session_state.posts[st.session_state.business_type]

def get_pillar_map():
    return {p["id"]: p for p in get_config()["pillars"]}

def get_holidays_for_month_live(year: int, month: int) -> list:
    prefix = f"{year}-{str(month).zfill(2)}"
    return [h for h in st.session_state.holidays if h["date"].startswith(prefix)]

def get_holidays_for_date_live(date_str: str) -> list:
    return [h for h in st.session_state.holidays if h["date"] == date_str]

MONTHS = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📅 Content Calendar")
    st.markdown("*Built on best practices · Co-built with Manus*")
    st.divider()

    # Business type switcher
    biz = st.radio(
        "Business Type",
        options=["retail", "airbnb"],
        format_func=lambda x: "🏪 Retail / C-Store" if x == "retail" else "🏠 Short-Term Rental",
        key="business_type",
        horizontal=False,
    )
    config = get_config()
    st.caption(config["tagline"])
    st.divider()

    # Month navigation
    st.markdown("**Navigate Month**")
    col_prev, col_mid, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.button("◀", use_container_width=True):
            m = st.session_state.current_month - 1
            y = st.session_state.current_year
            if m < 1: m = 12; y -= 1
            st.session_state.current_month = m
            st.session_state.current_year  = y
            st.rerun()
    with col_mid:
        # Read state after any button press so label is always in sync
        st.markdown(
            f"<div style='text-align:center;font-weight:700;padding-top:0.4rem'>"
            f"{MONTHS[st.session_state.current_month-1][:3]} {st.session_state.current_year}</div>",
            unsafe_allow_html=True,
        )
    with col_next:
        if st.button("▶", use_container_width=True):
            m = st.session_state.current_month + 1
            y = st.session_state.current_year
            if m > 12: m = 1; y += 1
            st.session_state.current_month = m
            st.session_state.current_year  = y
            st.rerun()
    st.divider()

    # Strategy pillars
    st.markdown("**Content Pillars**")
    posts = get_posts()
    actual_posts = [p for p in posts if p.get("entryType") != "recommendation"]
    total_actual = len(actual_posts) or 1
    for pillar in config["pillars"]:
        count = sum(1 for p in actual_posts if p["pillar"] == pillar["id"])
        pct   = round(count / total_actual * 100)
        target = pillar["target_pct"]
        color  = "normal" if abs(pct - target) <= 5 else ("inverse" if pct > target else "off")
        st.markdown(f"<div style='display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:2px'><span>● {pillar['name']}</span><span><b>{pct}%</b> / {target}%</span></div>", unsafe_allow_html=True)
        bar_color = pillar["color"]
        st.markdown(f"<div style='background:#f3f4f6;border-radius:4px;height:6px;margin-bottom:8px'><div style='background:{bar_color};width:{min(pct,100)}%;height:6px;border-radius:4px'></div></div>", unsafe_allow_html=True)
    st.divider()

    # Posting cadence
    st.markdown("**Posting Cadence**")
    for c in config["cadence"]:
        priority_color = "#22c55e" if c["priority"] == "Primary" else ("#f59e0b" if c["priority"] == "Secondary" else "#9ca3af")
        st.markdown(f"<div style='font-size:0.78rem;margin-bottom:4px'><span style='color:{priority_color}'>●</span> <b>{c['platform']}</b>: {c['frequency']}</div>", unsafe_allow_html=True)

# ── Main header ───────────────────────────────────────────────────────────────
# Re-read state here so header always reflects the current month after rerun
accent = config["accent"]
_month_label = MONTHS[st.session_state.current_month - 1]
_year_label  = st.session_state.current_year
st.markdown(f"""
<div class="main-header">
  <h1>📅 Content Calendar Planner</h1>
  <p>{config['label']} · {_month_label} {_year_label} · Cebu City, Philippines</p>
</div>
""", unsafe_allow_html=True)

# ── Tab navigation ────────────────────────────────────────────────────────────
tabs = st.tabs(["📅 Calendar", "📊 Performance Tracker", "✨ AI Ideas", "📋 Learnings Report", "🗓️ Holiday Manager"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CALENDAR
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    year  = st.session_state.current_year
    month = st.session_state.current_month
    posts = get_posts()
    config = get_config()
    pillar_map = get_pillar_map()

    month_holidays = get_holidays_for_month_live(year, month)
    holiday_dates  = {h["date"] for h in month_holidays}

    # Month heading — always matches sidebar navigation
    st.markdown(
        f"<h2 style='margin:0 0 0.75rem;font-size:1.4rem;font-weight:700;color:#111827'>"
        f"📅 {MONTHS[month-1]} {year}</h2>",
        unsafe_allow_html=True,
    )

    # Month summary bar
    month_posts = [p for p in posts if p["date"].startswith(f"{year}-{str(month).zfill(2)}")]
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Posts This Month", len(month_posts))
    with c2: st.metric("Holidays", len(month_holidays))
    with c3: st.metric("Published", sum(1 for p in month_posts if p["status"] == "Published"))
    with c4: st.metric("Scheduled", sum(1 for p in month_posts if p["status"] == "Scheduled"))
    with c5: st.metric("Ideas/Draft", sum(1 for p in month_posts if p["status"] in ("Idea","Draft")))

    # Holiday legend
    if month_holidays:
        st.markdown("**Holidays this month:**")
        hol_html = ""
        for h in month_holidays:
            tc = HOLIDAY_TYPE_CONFIG[h["type"]]
            hol_html += f'<span class="holiday-badge" style="background:{tc["color"]};color:{tc["text"]};border:1px solid {tc["border"]}">{tc["icon"]} {h["name"]} ({h["date"][8:10]})</span> '
        st.markdown(hol_html, unsafe_allow_html=True)
        st.markdown("")

    # Calendar grid
    first_weekday, days_in_month = cal_lib.monthrange(year, month)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols_header = st.columns(7)
    for i, d in enumerate(day_names):
        cols_header[i].markdown(f"<div style='text-align:center;font-weight:700;font-size:0.8rem;color:#6b7280;padding:4px 0'>{d}</div>", unsafe_allow_html=True)

    # Build week rows
    day_num = 1
    week_days = []
    # pad start
    for _ in range(first_weekday):
        week_days.append(None)
    for d in range(1, days_in_month + 1):
        week_days.append(d)
    # pad end
    while len(week_days) % 7 != 0:
        week_days.append(None)

    for week_start in range(0, len(week_days), 7):
        week = week_days[week_start:week_start+7]
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day is None:
                    st.markdown("<div style='min-height:80px'></div>", unsafe_allow_html=True)
                    continue
                date_str = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
                day_posts    = [p for p in posts if p["date"] == date_str]
                day_holidays = get_holidays_for_date(date_str)
                is_today     = date_str == str(date.today())

                # Day cell
                border = f"2px solid {accent}" if is_today else "1px solid #e5e7eb"
                bg     = config["accent_light"] if is_today else "white"
                cell_html = f"<div style='border:{border};border-radius:8px;padding:6px;min-height:80px;background:{bg}'>"
                cell_html += f"<div style='font-weight:700;font-size:0.85rem;margin-bottom:4px'>{day}</div>"

                # Holiday badges
                for h in day_holidays:
                    tc = HOLIDAY_TYPE_CONFIG[h["type"]]
                    cell_html += f'<div style="font-size:0.65rem;background:{tc["color"]};color:{tc["text"]};border-radius:4px;padding:1px 4px;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{tc["icon"]} {h["name"]}</div>'

                # Post dots
                for p in day_posts[:3]:
                    pillar = pillar_map.get(p["pillar"], {})
                    pcolor = pillar.get("color", "#9ca3af")
                    cell_html += f'<div style="font-size:0.65rem;background:{pcolor}22;color:{pcolor};border-radius:4px;padding:1px 4px;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">● {p["title"][:20]}</div>'
                if len(day_posts) > 3:
                    cell_html += f'<div style="font-size:0.6rem;color:#9ca3af">+{len(day_posts)-3} more</div>'

                cell_html += "</div>"
                st.markdown(cell_html, unsafe_allow_html=True)

    st.divider()

    # Day detail + post management
    st.markdown("### 📋 Manage Posts")
    col_date, col_add = st.columns([3, 1])
    with col_date:
        selected_date = st.date_input(
            "Select date",
            value=date(year, month, 1),
            min_value=date(year, month, 1),
            max_value=date(year, month, days_in_month),
        )
    with col_add:
        st.markdown("<div style='padding-top:1.6rem'>", unsafe_allow_html=True)
        add_post = st.button("➕ Add Post", use_container_width=True, type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    selected_str  = selected_date.strftime("%Y-%m-%d")
    selected_posts = [p for p in posts if p["date"] == selected_str]
    sel_holidays   = get_holidays_for_date_live(selected_str)

    if sel_holidays:
        for h in sel_holidays:
            tc = HOLIDAY_TYPE_CONFIG[h["type"]]
            scope_note = f" · {h['note']}" if h.get("note") else ""
            st.markdown(f'<div style="background:{tc["color"]};border:1px solid {tc["border"]};border-radius:8px;padding:0.5rem 0.75rem;margin-bottom:0.5rem;font-size:0.82rem"><b>{tc["icon"]} {h["name"]}</b> · {tc["label"]}{scope_note}</div>', unsafe_allow_html=True)
            if st.button(f"✨ Get AI ideas for {h['name']}", key=f"hol_ai_{h['date']}_{h['name'][:10]}"):
                st.session_state.ai_preset_theme   = "holiday"
                st.session_state.ai_preset_context = f"Upcoming holiday: {h['name']} on {h['date']}. Create content ideas tied to this occasion."
                st.success(f"Switched to AI Ideas tab with '{h['name']}' pre-filled. Click the ✨ AI Ideas tab above.")

    # Add post form
    if add_post:
        st.session_state["show_add_form"] = True

    if st.session_state.get("show_add_form"):
        with st.expander("➕ New Post", expanded=True):
            with st.form("add_post_form"):
                title    = st.text_input("Post Title *")
                caption  = st.text_area("Caption", height=80)
                cta      = st.text_input("Call to Action")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    platform = st.selectbox("Platform", PLATFORMS)
                with col_b:
                    fmt      = st.selectbox("Format", FORMATS)
                with col_c:
                    pillar_opts = {p["name"]: p["id"] for p in config["pillars"]}
                    pillar_name = st.selectbox("Pillar", list(pillar_opts.keys()))
                status = st.selectbox("Status", STATUSES)
                notes  = st.text_input("Notes (optional)")
                submitted = st.form_submit_button("Add to Calendar", type="primary")
                if submitted and title:
                    import uuid
                    new_post = {
                        "id": str(uuid.uuid4())[:8],
                        "date": selected_str,
                        "title": title,
                        "platform": platform,
                        "format": fmt,
                        "pillar": pillar_opts[pillar_name],
                        "caption": caption,
                        "cta": cta,
                        "status": status,
                        "outcome": None,
                        "reach": None,
                        "engagement": None,
                        "clicks": None,
                        "notes": notes or None,
                        "entryType": "post",
                        "aiGenerated": False,
                    }
                    st.session_state.posts[st.session_state.business_type].append(new_post)
                    st.session_state["show_add_form"] = False
                    st.success(f"✅ Post '{title}' added to {selected_str}")
                    st.rerun()

    # Display selected day posts
    if selected_posts:
        st.markdown(f"**{len(selected_posts)} post(s) on {selected_date.strftime('%B %d, %Y')}**")
        for p in selected_posts:
            pillar = pillar_map.get(p["pillar"], {})
            pcolor = pillar.get("color", "#9ca3af")
            outcome_str = p.get("outcome") or "Not evaluated"
            oc = OUTCOME_COLORS.get(outcome_str, {"bg": "#f3f4f6", "text": "#374151", "icon": "—"})
            with st.container():
                st.markdown(f'<div style="height:3px;background:{pcolor};border-radius:2px;margin-bottom:4px"></div>', unsafe_allow_html=True)
                col_info, col_actions = st.columns([4, 1])
                with col_info:
                    badges = f'<span style="background:{STATUS_COLORS.get(p["status"],"#f3f4f6")};padding:2px 8px;border-radius:12px;font-size:0.72rem;font-weight:600">{p["status"]}</span>'
                    if p.get("aiGenerated"):
                        badges += ' <span style="background:#dbeafe;color:#1d4ed8;padding:2px 8px;border-radius:12px;font-size:0.72rem;font-weight:600">✨ AI</span>'
                    if p.get("entryType") == "recommendation":
                        badges += ' <span style="background:#f3e8ff;color:#7c3aed;padding:2px 8px;border-radius:12px;font-size:0.72rem;font-weight:600">💡 Rec</span>'
                    st.markdown(f"**{p['title']}** {badges}", unsafe_allow_html=True)
                    st.caption(f"{p['platform']} · {p['format']} · {pillar.get('name','')}")
                    if p.get("caption"):
                        st.caption(p["caption"][:120] + ("…" if len(p.get("caption","")) > 120 else ""))
                with col_actions:
                    if p.get("outcome") == "Worked ✅":
                        if st.button("📋 Dup", key=f"dup_{p['id']}", help="Duplicate to next month"):
                            import uuid
                            next_m = month + 1
                            next_y = year
                            if next_m > 12: next_m = 1; next_y += 1
                            new_date = f"{next_y}-{str(next_m).zfill(2)}-{p['date'][8:]}"
                            dup = dict(p)
                            dup["id"] = str(uuid.uuid4())[:8]
                            dup["date"] = new_date
                            dup["status"] = "Idea"
                            dup["outcome"] = None
                            dup["reach"] = dup["engagement"] = dup["clicks"] = None
                            st.session_state.posts[st.session_state.business_type].append(dup)
                            st.success(f"Duplicated to {new_date}")
                            st.rerun()
                    if st.button("✏️ Edit", key=f"edit_btn_{p['id']}", help="Edit this post"):
                        st.session_state[f"editing_{p['id']}"] = True
                    if st.button("🗑️ Del", key=f"del_{p['id']}", help="Delete this post"):
                        st.session_state.posts[st.session_state.business_type] = [
                            x for x in st.session_state.posts[st.session_state.business_type] if x["id"] != p["id"]
                        ]
                        st.rerun()

            # Inline edit form — shown below the post card when Edit is clicked
            if st.session_state.get(f"editing_{p['id']}"):
                with st.expander(f"✏️ Editing: {p['title']}", expanded=True):
                    with st.form(f"edit_form_{p['id']}"):
                        e_title   = st.text_input("Post Title *", value=p.get("title", ""))
                        e_caption = st.text_area("Caption", value=p.get("caption", "") or "", height=80)
                        e_cta     = st.text_input("Call to Action", value=p.get("cta", "") or "")
                        e_date    = st.date_input(
                            "Date",
                            value=datetime.strptime(p["date"], "%Y-%m-%d").date(),
                        )
                        ec1, ec2, ec3 = st.columns(3)
                        with ec1:
                            e_platform = st.selectbox("Platform", PLATFORMS, index=PLATFORMS.index(p["platform"]) if p["platform"] in PLATFORMS else 0)
                        with ec2:
                            e_fmt = st.selectbox("Format", FORMATS, index=FORMATS.index(p["format"]) if p["format"] in FORMATS else 0)
                        with ec3:
                            pillar_opts  = {pl["name"]: pl["id"] for pl in config["pillars"]}
                            pillar_names = list(pillar_opts.keys())
                            cur_pillar_name = next((pl["name"] for pl in config["pillars"] if pl["id"] == p["pillar"]), pillar_names[0])
                            e_pillar_name = st.selectbox("Pillar", pillar_names, index=pillar_names.index(cur_pillar_name) if cur_pillar_name in pillar_names else 0)
                        e_status = st.selectbox("Status", STATUSES, index=STATUSES.index(p["status"]) if p["status"] in STATUSES else 0)
                        e_notes  = st.text_input("Notes (optional)", value=p.get("notes", "") or "")
                        save_col, cancel_col = st.columns(2)
                        with save_col:
                            save_edit = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                        with cancel_col:
                            cancel_edit = st.form_submit_button("✕ Cancel", use_container_width=True)

                        if save_edit and e_title:
                            for i, x in enumerate(st.session_state.posts[st.session_state.business_type]):
                                if x["id"] == p["id"]:
                                    st.session_state.posts[st.session_state.business_type][i].update({
                                        "title":    e_title,
                                        "caption":  e_caption or None,
                                        "cta":      e_cta or None,
                                        "date":     e_date.strftime("%Y-%m-%d"),
                                        "platform": e_platform,
                                        "format":   e_fmt,
                                        "pillar":   pillar_opts[e_pillar_name],
                                        "status":   e_status,
                                        "notes":    e_notes or None,
                                    })
                                    break
                            st.session_state.pop(f"editing_{p['id']}", None)
                            st.success(f"✅ '{e_title}' updated")
                            st.rerun()
                        if cancel_edit:
                            st.session_state.pop(f"editing_{p['id']}", None)
                            st.rerun()
            st.divider()
    else:
        st.info("No posts on this date. Click '➕ Add Post' to create one.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PERFORMANCE TRACKER
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    posts      = get_posts()
    config     = get_config()
    pillar_map = get_pillar_map()

    published   = [p for p in posts if p["status"] == "Published"]
    evaluated   = [p for p in published if p.get("outcome")]
    worked      = [p for p in evaluated if p["outcome"] == "Worked ✅"]
    didnt_work  = [p for p in evaluated if p["outcome"] == "Didn't Work ❌"]
    mixed       = [p for p in evaluated if p["outcome"] == "Mixed 🔶"]
    total_reach = sum(p.get("reach") or 0 for p in posts)
    win_rate    = round(len(worked) / len(evaluated) * 100) if evaluated else 0

    st.markdown("### 📊 Performance Summary")
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Total Posts",    len(posts))
    m2.metric("Published",      len(published))
    m3.metric("Evaluated",      len(evaluated))
    m4.metric("✅ Worked",      len(worked))
    m5.metric("❌ Didn't Work", len(didnt_work))
    m6.metric("Win Rate",       f"{win_rate}%")

    if evaluated:
        # Breakdown charts
        st.markdown("### 📈 Breakdown Analysis")
        col_chart1, col_chart2, col_chart3 = st.columns(3)

        # By pillar
        with col_chart1:
            pillar_data = {}
            for p in evaluated:
                pname = pillar_map.get(p["pillar"], {}).get("name", p["pillar"])
                if pname not in pillar_data:
                    pillar_data[pname] = {"Worked ✅": 0, "Mixed 🔶": 0, "Didn't Work ❌": 0}
                pillar_data[pname][p["outcome"]] = pillar_data[pname].get(p["outcome"], 0) + 1
            df_pillar = pd.DataFrame(pillar_data).T.reset_index().rename(columns={"index": "Pillar"})
            fig = px.bar(df_pillar, x="Pillar", y=["Worked ✅", "Mixed 🔶", "Didn't Work ❌"],
                         title="By Pillar", color_discrete_map={"Worked ✅": "#22c55e", "Mixed 🔶": "#f59e0b", "Didn't Work ❌": "#ef4444"},
                         height=280)
            fig.update_layout(margin=dict(t=40, b=20, l=10, r=10), legend=dict(orientation="h", y=-0.3))
            st.plotly_chart(fig, use_container_width=True)

        # By platform
        with col_chart2:
            plat_data = {}
            for p in evaluated:
                plat = p["platform"]
                if plat not in plat_data:
                    plat_data[plat] = {"Worked ✅": 0, "Mixed 🔶": 0, "Didn't Work ❌": 0}
                plat_data[plat][p["outcome"]] = plat_data[plat].get(p["outcome"], 0) + 1
            df_plat = pd.DataFrame(plat_data).T.reset_index().rename(columns={"index": "Platform"})
            fig2 = px.bar(df_plat, x="Platform", y=["Worked ✅", "Mixed 🔶", "Didn't Work ❌"],
                          title="By Platform", color_discrete_map={"Worked ✅": "#22c55e", "Mixed 🔶": "#f59e0b", "Didn't Work ❌": "#ef4444"},
                          height=280)
            fig2.update_layout(margin=dict(t=40, b=20, l=10, r=10), legend=dict(orientation="h", y=-0.3))
            st.plotly_chart(fig2, use_container_width=True)

        # By format
        with col_chart3:
            fmt_data = {}
            for p in evaluated:
                f = p["format"]
                if f not in fmt_data:
                    fmt_data[f] = {"Worked ✅": 0, "Mixed 🔶": 0, "Didn't Work ❌": 0}
                fmt_data[f][p["outcome"]] = fmt_data[f].get(p["outcome"], 0) + 1
            df_fmt = pd.DataFrame(fmt_data).T.reset_index().rename(columns={"index": "Format"})
            fig3 = px.bar(df_fmt, x="Format", y=["Worked ✅", "Mixed 🔶", "Didn't Work ❌"],
                          title="By Format", color_discrete_map={"Worked ✅": "#22c55e", "Mixed 🔶": "#f59e0b", "Didn't Work ❌": "#ef4444"},
                          height=280)
            fig3.update_layout(margin=dict(t=40, b=20, l=10, r=10), legend=dict(orientation="h", y=-0.3))
            st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    st.markdown("### 📝 Log & Review Posts")

    filter_tab = st.radio("Filter", ["All", "Published", "✅ Worked", "❌ Didn't Work", "🔶 Mixed", "Not Evaluated"],
                          horizontal=True)

    def filter_posts(posts, f):
        if f == "Published":    return [p for p in posts if p["status"] == "Published"]
        if f == "✅ Worked":    return [p for p in posts if p.get("outcome") == "Worked ✅"]
        if f == "❌ Didn't Work": return [p for p in posts if p.get("outcome") == "Didn't Work ❌"]
        if f == "🔶 Mixed":     return [p for p in posts if p.get("outcome") == "Mixed 🔶"]
        if f == "Not Evaluated": return [p for p in posts if p["status"] == "Published" and not p.get("outcome")]
        return posts

    filtered = sorted(filter_posts(posts, filter_tab), key=lambda p: p["date"], reverse=True)

    for p in filtered:
        pillar = pillar_map.get(p["pillar"], {})
        pcolor = pillar.get("color", "#9ca3af")
        outcome_str = p.get("outcome") or "Not evaluated"
        oc = OUTCOME_COLORS.get(outcome_str, {"bg": "#f3f4f6", "text": "#374151", "icon": "—"})

        with st.expander(f"{oc['icon']} {p['title']} · {p['date']} · {p['platform']}"):
            col_l, col_r = st.columns([3, 2])
            with col_l:
                st.markdown(f"**Pillar:** {pillar.get('name','—')}  |  **Format:** {p['format']}  |  **Status:** {p['status']}")
                if p.get("caption"):
                    st.caption(p["caption"])
                if p.get("performanceNotes"):
                    st.markdown(f'<div class="tip-box">📝 {p["performanceNotes"]}</div>', unsafe_allow_html=True)
            with col_r:
                if p.get("reach") or p.get("engagement") or p.get("clicks"):
                    r, e, cl = p.get("reach") or 0, p.get("engagement") or 0, p.get("clicks") or 0
                    eng_rate = round(e / r * 100, 1) if r else 0
                    st.metric("Reach",       f"{r:,}")
                    st.metric("Engagement",  f"{e:,}")
                    st.metric("Eng. Rate",   f"{eng_rate}%")

            # Log performance form
            with st.form(f"outcome_form_{p['id']}"):
                st.markdown("**Log Performance**")
                new_outcome = st.selectbox("Outcome", ["— Not set —"] + OUTCOMES, key=f"oc_{p['id']}",
                                           index=0 if not p.get("outcome") else (OUTCOMES.index(p["outcome"]) + 1))
                c1, c2, c3 = st.columns(3)
                with c1: new_reach = st.number_input("Reach", value=p.get("reach") or 0, min_value=0, key=f"r_{p['id']}")
                with c2: new_eng   = st.number_input("Engagement", value=p.get("engagement") or 0, min_value=0, key=f"e_{p['id']}")
                with c3: new_clicks= st.number_input("Clicks", value=p.get("clicks") or 0, min_value=0, key=f"cl_{p['id']}")
                new_notes = st.text_area("What worked / didn't work?", value=p.get("performanceNotes") or "", height=60, key=f"n_{p['id']}")
                save_btn = st.form_submit_button("💾 Save Performance", type="primary")
                if save_btn:
                    for post in st.session_state.posts[st.session_state.business_type]:
                        if post["id"] == p["id"]:
                            if new_outcome != "— Not set —":
                                post["outcome"] = new_outcome
                            post["reach"]            = new_reach or None
                            post["engagement"]       = new_eng or None
                            post["clicks"]           = new_clicks or None
                            post["performanceNotes"] = new_notes or None
                            break
                    st.success("Performance saved!")
                    st.rerun()

            # Duplicate button for worked posts
            if p.get("outcome") == "Worked ✅":
                if st.button(f"📋 Duplicate to next month", key=f"dup_tracker_{p['id']}"):
                    import uuid
                    post_month = int(p["date"][5:7])
                    post_year  = int(p["date"][:4])
                    next_m = post_month + 1
                    next_y = post_year
                    if next_m > 12: next_m = 1; next_y += 1
                    new_date = f"{next_y}-{str(next_m).zfill(2)}-{p['date'][8:]}"
                    dup = dict(p)
                    dup["id"]     = str(uuid.uuid4())[:8]
                    dup["date"]   = new_date
                    dup["status"] = "Idea"
                    dup["outcome"] = dup["reach"] = dup["engagement"] = dup["clicks"] = None
                    dup["performanceNotes"] = None
                    st.session_state.posts[st.session_state.business_type].append(dup)
                    st.success(f"✅ Duplicated to {new_date}")
                    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — AI IDEAS
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    config = get_config()
    year   = st.session_state.current_year
    month  = st.session_state.current_month

    st.markdown("### ✨ AI Content Ideas")
    st.caption("Generate theme-based content ideas powered by Claude AI. Ideas can be added directly to your calendar.")

    THEMES = [
        {"id": "promotion",   "label": "Promotions & Deals",       "icon": "🏷️"},
        {"id": "holiday",     "label": "Holiday & Occasions",       "icon": "🎉"},
        {"id": "lifestyle",   "label": "Lifestyle & Relatable",     "icon": "☕"},
        {"id": "product",     "label": "Product / Property Spotlight","icon": "✨"},
        {"id": "community",   "label": "Community & UGC",           "icon": "👥"},
        {"id": "educational", "label": "Educational & Tips",        "icon": "💡"},
        {"id": "ugc",         "label": "UGC & Social Proof",        "icon": "⭐"},
        {"id": "seasonal",    "label": "Seasonal Moments",          "icon": "🌿"},
    ]

    # Consume preset from holiday shortcut
    preset_theme   = st.session_state.get("ai_preset_theme")
    preset_context = st.session_state.get("ai_preset_context", "")

    theme_labels = [f"{t['icon']} {t['label']}" for t in THEMES]
    theme_ids    = [t["id"] for t in THEMES]
    default_idx  = theme_ids.index(preset_theme) if preset_theme and preset_theme in theme_ids else 0

    selected_theme_label = st.radio("Select Theme", theme_labels, index=default_idx, horizontal=True)
    selected_theme_id    = theme_ids[theme_labels.index(selected_theme_label)]

    # Clear preset after consumption
    if preset_theme:
        st.session_state.ai_preset_theme   = None

    # Holiday context notice
    month_holidays = get_holidays_for_month_live(year, month)
    if month_holidays and selected_theme_id == "holiday":
        hol_names = ", ".join(h["name"] for h in month_holidays)
        st.markdown(f'<div class="warning-box">🗓️ <b>Holidays in {MONTHS[month-1]}:</b> {hol_names}</div>', unsafe_allow_html=True)

    custom_context = st.text_area(
        "Additional context (optional)",
        value=preset_context,
        placeholder="e.g. Launching new iced coffee line, targeting Gen Z, budget promo week...",
        height=70,
    )
    if preset_context:
        st.session_state.ai_preset_context = ""

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Get a free key at console.anthropic.com. Your key is never stored.",
    )

    generate_btn = st.button("✨ Generate Ideas", type="primary", use_container_width=True)

    if generate_btn:
        if not api_key:
            st.warning("Please enter your Anthropic API key to generate ideas.")
        else:
            business_desc = (
                "a convenience store / C-store (similar to 7-Eleven) in Cebu City, Philippines"
                if config["type"] == "retail"
                else "a short-term rental / Airbnb property in Cebu City, Philippines"
            )
            pillars_desc = "\n".join(f"- {p['name']} (id: {p['id']}): {p['description']}" for p in config["pillars"])
            holiday_ctx  = (
                f"Upcoming holidays in {MONTHS[month-1]}: {', '.join(h['name'] + ' (' + h['date'] + ')' for h in month_holidays)}."
                if month_holidays else f"No major holidays in {MONTHS[month-1]}."
            )
            theme_meta   = next(t for t in THEMES if t["id"] == selected_theme_id)
            extra_ctx    = f"\nAdditional context: {custom_context}" if custom_context else ""
            pillar_ids   = [p["id"] for p in config["pillars"]]

            prompt = f"""You are a social media content strategist for {business_desc}.

Business type: {config['type']}
Month: {MONTHS[month-1]} {year}
{holiday_ctx}

Content pillars available:
{pillars_desc}

Generate 4 social media post ideas for the theme: {theme_meta['label']} — {theme_meta['icon']}
{extra_ctx}

Return ONLY a valid JSON array with exactly 4 objects. Each object must have:
- "title": short post title (max 8 words)
- "caption": full post caption with emojis (100-150 words)
- "cta": call to action (max 10 words)
- "platform": one of {PLATFORMS}
- "format": one of {FORMATS}
- "pillarId": one of {pillar_ids}
- "rationale": why this post works (1-2 sentences)

Return ONLY the JSON array, no other text."""

            with st.spinner("Generating ideas with Claude AI..."):
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=api_key)
                    message = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=2000,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    raw = message.content[0].text.strip()
                    # Strip markdown code fences if present
                    if raw.startswith("```"):
                        raw = raw.split("```")[1]
                        if raw.startswith("json"):
                            raw = raw[4:]
                    ideas = json.loads(raw.strip())
                    st.session_state["ai_ideas"] = ideas
                    st.session_state["ai_ideas_theme"] = selected_theme_id
                except Exception as e:
                    st.error(f"Error generating ideas: {e}")

    # Display ideas
    if st.session_state.get("ai_ideas"):
        st.divider()
        st.markdown(f"### 💡 Generated Ideas — {next((t['icon']+' '+t['label']) for t in THEMES if t['id'] == st.session_state.get('ai_ideas_theme','promotion'))}")
        for i, idea in enumerate(st.session_state["ai_ideas"]):
            with st.expander(f"**{idea.get('title','Idea')}** · {idea.get('platform','')} · {idea.get('format','')}"):
                st.markdown(f"**Caption:**\n{idea.get('caption','')}")
                st.markdown(f"**CTA:** {idea.get('cta','')}")
                st.markdown(f"**Pillar:** {pillar_map.get(idea.get('pillarId',''), {}).get('name', idea.get('pillarId',''))}")
                st.markdown(f'<div class="tip-box">💡 <b>Why this works:</b> {idea.get("rationale","")}</div>', unsafe_allow_html=True)

                add_date = st.date_input(f"Add to calendar on", value=date(year, month, 1), key=f"idea_date_{i}")
                if st.button(f"➕ Add to Calendar", key=f"add_idea_{i}", type="primary"):
                    import uuid
                    new_post = {
                        "id":         str(uuid.uuid4())[:8],
                        "date":       add_date.strftime("%Y-%m-%d"),
                        "title":      idea.get("title","AI Post"),
                        "platform":   idea.get("platform", PLATFORMS[0]),
                        "format":     idea.get("format", FORMATS[0]),
                        "pillar":     idea.get("pillarId", config["pillars"][0]["id"]),
                        "caption":    idea.get("caption",""),
                        "cta":        idea.get("cta",""),
                        "status":     "Idea",
                        "outcome":    None,
                        "reach":      None,
                        "engagement": None,
                        "clicks":     None,
                        "notes":      f"AI rationale: {idea.get('rationale','')}",
                        "entryType":  "recommendation",
                        "aiGenerated": True,
                    }
                    st.session_state.posts[st.session_state.business_type].append(new_post)
                    st.success(f"✅ Added '{idea.get('title')}' to {add_date.strftime('%B %d, %Y')}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — LEARNINGS REPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    posts      = get_posts()
    config     = get_config()
    pillar_map = get_pillar_map()

    evaluated = [p for p in posts if p.get("outcome")]

    st.markdown("### 📋 Learnings Report")
    st.caption("Compiled from all posts with a logged outcome. Export to CSV for sharing.")

    if not evaluated:
        st.info("No evaluated posts yet. Go to the Performance Tracker tab to log outcomes for published posts.")
    else:
        worked_list    = [p for p in evaluated if p["outcome"] == "Worked ✅"]
        mixed_list     = [p for p in evaluated if p["outcome"] == "Mixed 🔶"]
        didnt_list     = [p for p in evaluated if p["outcome"] == "Didn't Work ❌"]
        total_reach    = sum(p.get("reach") or 0 for p in evaluated)
        total_eng      = sum(p.get("engagement") or 0 for p in evaluated)
        win_rate       = round(len(worked_list) / len(evaluated) * 100)

        # TLDR
        st.markdown("#### TLDR")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Evaluated Posts", len(evaluated))
        c2.metric("✅ Worked",       len(worked_list))
        c3.metric("🔶 Mixed",        len(mixed_list))
        c4.metric("❌ Didn't Work",  len(didnt_list))
        c5.metric("Win Rate",        f"{win_rate}%")

        st.divider()

        # Breakdown tables
        def build_breakdown(key_fn, label):
            data = {}
            for p in evaluated:
                k = key_fn(p)
                if k not in data:
                    data[k] = {"Total": 0, "Worked": 0, "Mixed": 0, "Didn't Work": 0, "Reach": 0}
                data[k]["Total"] += 1
                if p["outcome"] == "Worked ✅":    data[k]["Worked"]      += 1
                elif p["outcome"] == "Mixed 🔶":   data[k]["Mixed"]       += 1
                elif p["outcome"] == "Didn't Work ❌": data[k]["Didn't Work"] += 1
                data[k]["Reach"] += p.get("reach") or 0
            rows = [{"Name": k, **v, "Win Rate": f"{round(v['Worked']/v['Total']*100)}%" if v["Total"] else "—"} for k, v in data.items()]
            return pd.DataFrame(rows).sort_values("Worked", ascending=False)

        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            st.markdown("**By Pillar**")
            df_p = build_breakdown(lambda p: pillar_map.get(p["pillar"], {}).get("name", p["pillar"]), "Pillar")
            st.dataframe(df_p, use_container_width=True, hide_index=True)
        with col_b2:
            st.markdown("**By Platform**")
            df_pl = build_breakdown(lambda p: p["platform"], "Platform")
            st.dataframe(df_pl, use_container_width=True, hide_index=True)
        with col_b3:
            st.markdown("**By Format**")
            df_f = build_breakdown(lambda p: p["format"], "Format")
            st.dataframe(df_f, use_container_width=True, hide_index=True)

        st.divider()

        # What worked / didn't work
        col_w, col_d = st.columns(2)
        with col_w:
            st.markdown("#### ✅ What Worked")
            for p in worked_list:
                st.markdown(f"**{p['title']}** · {p['platform']} · {p['format']}")
                if p.get("performanceNotes"):
                    st.markdown(f'<div class="tip-box">{p["performanceNotes"]}</div>', unsafe_allow_html=True)
                st.caption(f"Reach: {(p.get('reach') or 0):,} · Eng: {(p.get('engagement') or 0):,}")
        with col_d:
            st.markdown("#### ❌ What Didn't Work")
            for p in didnt_list:
                st.markdown(f"**{p['title']}** · {p['platform']} · {p['format']}")
                if p.get("performanceNotes"):
                    st.markdown(f'<div class="warning-box">{p["performanceNotes"]}</div>', unsafe_allow_html=True)
                st.caption(f"Reach: {(p.get('reach') or 0):,} · Eng: {(p.get('engagement') or 0):,}")

        st.divider()

        # CSV Export
        st.markdown("#### 📥 Export")
        export_rows = []
        for p in evaluated:
            pillar = pillar_map.get(p["pillar"], {})
            r = p.get("reach") or 0
            e = p.get("engagement") or 0
            export_rows.append({
                "Date":             p["date"],
                "Title":            p["title"],
                "Pillar":           pillar.get("name", p["pillar"]),
                "Platform":         p["platform"],
                "Format":           p["format"],
                "Status":           p["status"],
                "Outcome":          p.get("outcome") or "",
                "Reach":            r,
                "Engagement":       e,
                "Clicks":           p.get("clicks") or 0,
                "Eng Rate %":       round(e / r * 100, 1) if r else 0,
                "Performance Notes": p.get("performanceNotes") or "",
            })
        df_export = pd.DataFrame(export_rows)
        csv = df_export.to_csv(index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"learnings_report_{config['type']}_{year}_{str(month).zfill(2)}.csv",
            mime="text/csv",
            type="primary",
        )
        st.dataframe(df_export, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — HOLIDAY MANAGER
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    from data.holidays import HOLIDAY_TYPE_CONFIG

    st.markdown("### 🗃️ Holiday Manager")
    st.caption("Add, edit, or remove holidays. Changes reflect immediately on the calendar. Reloading the page resets to the default 2026 Cebu City list.")

    HOLIDAY_TYPES = list(HOLIDAY_TYPE_CONFIG.keys())
    HOLIDAY_SCOPES = ["national", "cebu-city", "cebu-province", "other"]

    # ── Add new holiday form
    with st.expander("➕ Add New Holiday", expanded=False):
        with st.form("add_holiday_form"):
            h_name  = st.text_input("Holiday Name *", placeholder="e.g. Fiesta Señor")
            h_date  = st.date_input("Date *", value=date(st.session_state.current_year, st.session_state.current_month, 1))
            hc1, hc2 = st.columns(2)
            with hc1:
                h_type  = st.selectbox("Type", HOLIDAY_TYPES,
                    format_func=lambda x: HOLIDAY_TYPE_CONFIG[x]["label"])
            with hc2:
                h_scope = st.selectbox("Scope", HOLIDAY_SCOPES)
            h_note  = st.text_input("Note (optional)", placeholder="e.g. City ordinance No. 123")
            add_hol = st.form_submit_button("➕ Add Holiday", type="primary", use_container_width=True)
            if add_hol and h_name:
                st.session_state.holidays.append({
                    "date":  h_date.strftime("%Y-%m-%d"),
                    "name":  h_name,
                    "type":  h_type,
                    "scope": h_scope,
                    "note":  h_note or None,
                })
                st.success(f"✅ '{h_name}' added on {h_date.strftime('%B %d, %Y')}")
                st.rerun()

    st.divider()

    # ── Filter by month
    st.markdown("**Filter by month**")
    fc1, fc2 = st.columns([2, 1])
    with fc1:
        filter_month = st.selectbox("Month", ["All months"] + MONTHS, index=st.session_state.current_month)
    with fc2:
        filter_type  = st.selectbox("Type", ["All types"] + HOLIDAY_TYPES,
            format_func=lambda x: x if x == "All types" else HOLIDAY_TYPE_CONFIG[x]["label"])

    # Build filtered list
    filtered_holidays = sorted(st.session_state.holidays, key=lambda h: h["date"])
    if filter_month != "All months":
        m_idx = str(MONTHS.index(filter_month) + 1).zfill(2)
        filtered_holidays = [h for h in filtered_holidays if h["date"][5:7] == m_idx]
    if filter_type != "All types":
        filtered_holidays = [h for h in filtered_holidays if h["type"] == filter_type]

    st.markdown(f"**{len(filtered_holidays)} holiday(s) shown**")

    if not filtered_holidays:
        st.info("No holidays match the current filter.")
    else:
        for idx, h in enumerate(filtered_holidays):
            tc = HOLIDAY_TYPE_CONFIG.get(h["type"], HOLIDAY_TYPE_CONFIG["special-non-working"])
            # Find the real index in session state for editing/deleting
            real_idx = next((i for i, x in enumerate(st.session_state.holidays)
                             if x["date"] == h["date"] and x["name"] == h["name"]), None)
            uid = f"{h['date']}_{h['name'][:8]}_{idx}"

            col_info, col_edit, col_del = st.columns([6, 1, 1])
            with col_info:
                st.markdown(
                    f'<div style="background:{tc["color"]};border:1px solid {tc["border"]};border-radius:8px;'
                    f'padding:0.5rem 0.75rem;font-size:0.85rem">'
                    f'<b>{tc["icon"]} {h["name"]}</b> &nbsp;·&nbsp; {h["date"]} &nbsp;·&nbsp; '
                    f'<span style="color:{tc["text"]}">{tc["label"]}</span>'
                    f'{(" &nbsp;·&nbsp; " + h["note"]) if h.get("note") else ""}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with col_edit:
                if st.button("✏️", key=f"hedit_{uid}", help="Edit this holiday"):
                    st.session_state[f"h_editing_{uid}"] = True
            with col_del:
                if st.button("🗑️", key=f"hdel_{uid}", help="Delete this holiday"):
                    if real_idx is not None:
                        st.session_state.holidays.pop(real_idx)
                    st.rerun()

            # Inline edit form
            if st.session_state.get(f"h_editing_{uid}") and real_idx is not None:
                with st.expander(f"✏️ Editing: {h['name']}", expanded=True):
                    with st.form(f"hedit_form_{uid}"):
                        eh_name  = st.text_input("Holiday Name *", value=h["name"])
                        eh_date  = st.date_input("Date *", value=datetime.strptime(h["date"], "%Y-%m-%d").date())
                        ehc1, ehc2 = st.columns(2)
                        with ehc1:
                            eh_type  = st.selectbox("Type", HOLIDAY_TYPES,
                                index=HOLIDAY_TYPES.index(h["type"]) if h["type"] in HOLIDAY_TYPES else 0,
                                format_func=lambda x: HOLIDAY_TYPE_CONFIG[x]["label"])
                        with ehc2:
                            eh_scope = st.selectbox("Scope", HOLIDAY_SCOPES,
                                index=HOLIDAY_SCOPES.index(h["scope"]) if h["scope"] in HOLIDAY_SCOPES else 0)
                        eh_note  = st.text_input("Note (optional)", value=h.get("note") or "")
                        es1, es2 = st.columns(2)
                        with es1:
                            save_h = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
                        with es2:
                            cancel_h = st.form_submit_button("✕ Cancel", use_container_width=True)
                        if save_h and eh_name:
                            st.session_state.holidays[real_idx] = {
                                "date":  eh_date.strftime("%Y-%m-%d"),
                                "name":  eh_name,
                                "type":  eh_type,
                                "scope": eh_scope,
                                "note":  eh_note or None,
                            }
                            st.session_state.pop(f"h_editing_{uid}", None)
                            st.success(f"✅ '{eh_name}' updated")
                            st.rerun()
                        if cancel_h:
                            st.session_state.pop(f"h_editing_{uid}", None)
                            st.rerun()

    st.divider()
    # Reset to defaults
    if st.button("🔄 Reset to Default 2026 Cebu City Holidays", use_container_width=True):
        from data.holidays import HOLIDAYS_2026
        st.session_state.holidays = [dict(h) for h in HOLIDAYS_2026]
        st.success("✅ Holidays reset to default 2026 Cebu City list")
        st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center;font-size:0.75rem;color:#9ca3af'>Content Calendar Planner · Built on best practices · Co-built with Manus · Cebu City 2026 holidays included</div>",
    unsafe_allow_html=True,
)
