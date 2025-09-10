# XAU_XAG_sessions.py
import streamlit as st
import pandas as pd
from datetime import datetime, time
from zoneinfo import ZoneInfo

# ---------- Helpers ----------
TZ_ABBR_TO_IANA = {
    # AU / NZ
    "AEST": "Australia/Sydney", "AEDT": "Australia/Sydney",
    "ACST": "Australia/Adelaide", "ACDT": "Australia/Adelaide",
    "AWST": "Australia/Perth",
    "NZST": "Pacific/Auckland", "NZDT": "Pacific/Auckland",
    # US
    "EST": "America/New_York", "EDT": "America/New_York",
    "CST": "America/Chicago", "CDT": "America/Chicago",
    "MST": "America/Denver",  "MDT": "America/Denver",
    "PST": "America/Los_Angeles", "PDT": "America/Los_Angeles",
    # EU / UK
    "GMT": "UTC", "BST": "Europe/London",
    "CET": "Europe/Berlin", "CEST": "Europe/Berlin",
    "EET": "Europe/Athens", "EEST": "Europe/Athens",
    # Asia
    "HKT": "Asia/Hong_Kong", "SGT": "Asia/Singapore",
    "JST": "Asia/Tokyo", "KST": "Asia/Seoul",
    "IST": "Asia/Kolkata",  # 这里把 IST 映射到印度时区（而不是爱尔兰夏令时）
}

def _resolve_tz(name: str) -> ZoneInfo:
    """Accept IANA name or abbreviation; return ZoneInfo."""
    if name in TZ_ABBR_TO_IANA:
        name = TZ_ABBR_TO_IANA[name]
    # special case
    if name.upper() == "UTC":
        name = "UTC"
    return ZoneInfo(name)

def _fmt_range_no_date(start_dt, end_dt, show_tz=True):
    tzname = start_dt.tzname()
    same_day = start_dt.date() == end_dt.date()
    span = f"{start_dt:%H:%M} - {end_dt:%H:%M}"
    if not same_day:
        span += " +1d"
    if show_tz and tzname:
        span += f" {tzname}"
    return span

def _today_in_tz(tzname: str):
    tz = _resolve_tz(tzname)
    return datetime.now(tz).date(), tz

def _to_utc_range(tzname, open_t, close_t):
    d, tz = _today_in_tz(tzname)
    return (
        datetime.combine(d, open_t, tzinfo=tz).astimezone(ZoneInfo("UTC")),
        datetime.combine(d, close_t, tzinfo=tz).astimezone(ZoneInfo("UTC")),
    )

# ---------- Page ----------
def xau_xag_market_page():
    lang = st.session_state.get("language", "zh")

    T = {
        "en": {
            "title": "🥇 XAU / 🥈 XAG Sessions (DST aware, no calendar dates)",
            "note": ("Spot gold/silver trade OTC 24×5. We use New York / London / Tokyo / Sydney "
                     "business hours as sessions and convert them to UTC and your timezone."),
            "tbl_sessions": "🌍 Four major sessions",
            "col_market": "Market", "col_local": "Local Time", "col_utc": "UTC", "col_yours": "Your Local",
            "ny": "New York", "ld": "London", "tk": "Tokyo", "sy": "Sydney",
            "overlaps": "🔁 Typical overlaps (shown without dates)",
            "ov_ld_ny": "London ↔ New York", "ov_tk_ld": "Tokyo ↔ London", "ov_sy_tk": "Sydney ↔ Tokyo",
            "otc_title": "⏱️ Global OTC hours for XAU/XAG (typical)",
            "otc_md": (
                "- Open: around **Sun 21:00 UTC** (Sydney starts)\n"
                "- Close: around **Fri 21:00–22:00 UTC** (NY winds down)\n"
                "- Weekday maintenance (many brokers): **~21:00–22:00 UTC** Mon–Thu, 45–60m\n"
                "- Exact windows vary by broker/server timezone; check your platform."
            ),
            "warn": "Sessions are liquidity conventions, not single-exchange opens.",
            "cfg": "Settings", "ld_close": "London close",
            "tzconv": "🕒 Timezone converter", "tz_src": "Source timezone (IANA or abbrev.)",
            "tz_time": "Time (no date)", "tz_targets": "Convert to", "tz_out": "Converted times",
        },
        "zh": {
            "title": "🥇 XAU / 🥈 XAG 市场时段（含夏令时、无日期）",
            "note": ("现货金银为 OTC 24×5。这里用纽约/伦敦/东京/悉尼的工作时段作为“会话”，并换算到 UTC 与你的本地时区。"),
            "tbl_sessions": "🌍 四大时段",
            "col_market": "市场", "col_local": "当地时间", "col_utc": "UTC", "col_yours": "你的本地时间",
            "ny": "纽约", "ld": "伦敦", "tk": "东京", "sy": "悉尼",
            "overlaps": "🔁 典型重叠时段（不含日期）",
            "ov_ld_ny": "伦敦 ↔ 纽约", "ov_tk_ld": "东京 ↔ 伦敦", "ov_sy_tk": "悉尼 ↔ 东京",
            "otc_title": "⏱️ XAU/XAG 全球 OTC 交易时间（常见口径）",
            "otc_md": (
                "- 开市：周日 **21:00 UTC**（悉尼启动）\n"
                "- 收市：周五 **21:00–22:00 UTC**（纽约收尾）\n"
                "- 工作日维护：周一至周四 **约 21:00–22:00 UTC**，45–60 分钟\n"
                "- 具体时间以券商服务器与合约细则为准。"
            ),
            "warn": "本页采用行业习惯的“会话”定义，用于教学/流动性观察。",
            "cfg": "设置", "ld_close": "伦敦收市",
            "tzconv": "🕒 时区转换器", "tz_src": "源时区（IANA 或缩写）",
            "tz_time": "时间（不含日期）", "tz_targets": "转换到", "tz_out": "换算结果",
        }
    }[lang]

    st.markdown("""
        <style>
        .block-container {max-width: 900px; padding-top: 1.0rem;}
        .note {background:#f7fafc;border-left:4px solid #3182ce;padding:.7rem 1rem;border-radius:.5rem;}
        .warn {background:#fff6f0;border-left:4px solid #f59e0b;padding:.7rem 1rem;border-radius:.5rem;}
        </style>
    """, unsafe_allow_html=True)

    st.title(T["title"])
    st.markdown(f"<div class='note'>{T['note']}</div>", unsafe_allow_html=True)

    # --- Settings: choose London close 16:30 or 17:00 ---
    with st.expander(T["cfg"], expanded=False):
        ld_close_is_17 = st.radio(T["ld_close"], options=["16:30", "17:00"], index=0, horizontal=True) == "17:00"
    london_close = time(17, 0) if ld_close_is_17 else time(16, 30)

    # Session definitions (business-hour convention)
    sessions = [
        (T["ny"], "America/New_York", time(8, 0),  time(17, 0)),
        (T["ld"], "Europe/London",    time(8, 0),  london_close),
        (T["tk"], "Asia/Tokyo",       time(9, 0),  time(18, 0)),  # no DST
        (T["sy"], "Australia/Sydney", time(8, 0),  time(17, 0)),
    ]

    # Build session table (no dates)
    your_tzinfo = datetime.now().astimezone().tzinfo
    rows = []
    for center, tzname, open_t, close_t in sessions:
        d, tz = _today_in_tz(tzname)
        open_local = datetime.combine(d, open_t, tzinfo=tz)
        close_local = datetime.combine(d, close_t, tzinfo=tz)
        open_utc, close_utc = open_local.astimezone(ZoneInfo("UTC")), close_local.astimezone(ZoneInfo("UTC"))
        open_you, close_you = open_local.astimezone(your_tzinfo), close_local.astimezone(your_tzinfo)
        rows.append([center,
                     _fmt_range_no_date(open_local, close_local),
                     _fmt_range_no_date(open_utc, close_utc),
                     _fmt_range_no_date(open_you, close_you)])
    st.subheader(T["tbl_sessions"])
    st.dataframe(pd.DataFrame(rows, columns=[T["col_market"], T["col_local"], T["col_utc"], T["col_yours"]]),
                 hide_index=True, use_container_width=True)

    # Overlaps (UTC, no dates)
    st.subheader(T["overlaps"])
    def overlap(a, b):
        s, e = max(a[0], b[0]), min(a[1], b[1])
        return (s, e) if s < e else None

    ny_utc = _to_utc_range("America/New_York", time(8,0), time(17,0))
    ld_utc = _to_utc_range("Europe/London",    time(8,0), london_close)
    tk_utc = _to_utc_range("Asia/Tokyo",       time(9,0), time(18,0))
    sy_utc = _to_utc_range("Australia/Sydney", time(8,0), time(17,0))

    ov_rows = []
    for label, win in [(T["ov_ld_ny"], overlap(ld_utc, ny_utc)),
                       (T["ov_tk_ld"], overlap(tk_utc, ld_utc)),
                       (T["ov_sy_tk"], overlap(sy_utc, tk_utc))]:
        if win:
            ov_rows.append([label,
                            _fmt_range_no_date(win[0], win[1], True),
                            _fmt_range_no_date(win[0].astimezone(your_tzinfo),
                                               win[1].astimezone(your_tzinfo), True)])
        else:
            ov_rows.append([label, "—", "—"])
    st.dataframe(pd.DataFrame(ov_rows, columns=["Overlap", "UTC", T["col_yours"]]),
                 hide_index=True, use_container_width=True)

    st.divider()
    st.subheader(T["otc_title"])
    st.markdown(T["otc_md"])
    st.markdown(f"<div class='warn'>{T['warn']}</div>", unsafe_allow_html=True)

    # --------------------
    # Timezone Converter
    # --------------------
    st.divider()
    st.subheader("🕒 " + (T["tzconv"].split(" ", 1)[1] if lang=="en" else T["tzconv"].split(" ", 1)[1]))
    # Build a clean IANA-only options list (include user's canonical zone if available)
    user_key = getattr(your_tzinfo, "key", None)
    # If only abbreviation is available, map it
    if not user_key:
        abbr = datetime.now().astimezone().tzname()
        user_key = TZ_ABBR_TO_IANA.get(abbr, "UTC")

    iana_options = sorted(set([
        "UTC", user_key,
        "America/New_York", "Europe/London", "Asia/Tokyo", "Australia/Sydney",
        "Asia/Shanghai", "Asia/Hong_Kong", "Asia/Singapore", "Europe/Berlin", "Europe/Paris",
        "America/Chicago", "America/Denver", "America/Los_Angeles", "Pacific/Auckland"
    ]))

    c1, c2 = st.columns(2)
    with c1:
        src_tz_name = st.selectbox(T["tz_src"], options=iana_options,
                                   index=iana_options.index(user_key) if user_key in iana_options else 0)
    with c2:
        src_time = st.time_input(T["tz_time"], value=time(9, 0), step=300)

    # Targets to convert to
    targets = [
        ("UTC", "UTC"),
        ("Your Local" if lang=="en" else "你的本地", user_key),
        (T["ny"], "America/New_York"),
        (T["ld"], "Europe/London"),
        (T["tk"], "Asia/Tokyo"),
        (T["sy"], "Australia/Sydney"),
    ]

    # Do conversion using safe resolver (accept abbrev if user ever types it)
    d, src_tz = _today_in_tz(src_tz_name)
    src_dt = datetime.combine(d, src_time, tzinfo=src_tz)

    conv_rows = []
    for label, tzname in targets:
        tz = _resolve_tz(tzname)
        out_dt = src_dt.astimezone(tz)
        conv_rows.append([label, f"{out_dt:%H:%M} {out_dt.tzname()}"])

    st.table(pd.DataFrame(conv_rows, columns=[T["tz_targets"], T["tz_out"]]))
