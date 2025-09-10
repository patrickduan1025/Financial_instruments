# routing_books.py
import streamlit as st

def routing_books_page():
    lang = st.session_state.get("language", "zh")

    T = {
        "en": {
            "title": "📚 Routing Console",
            "subtitle": "A-Book / B-Book / MM-Stream + Monitor (overlay)",
            "legend": "A-Book = external LP; B-Book = internal; MM-Stream = internal market-making; Monitor = overlay",
            # Formal hero (fixed policy + second-gate rule)
            "hero_abook": "Default (fixed): route to A-Book only when the computed **risk rating > 3 AND Biggest Profit > Biggest Loss**. Ratings 1–2 remain in B-Book.",
            "hero_note": (
                "Monitor is not a separate stream but an overlay tag, typically applied for onboarding, compliance, or risk-control scenarios (e.g., new account, delayed activation, AML or abnormal funding cases, or when flagged by senior management/CEO). "
                "MM-Stream is a special lane used primarily to handle heavy trade and persistent bursts with throttling/hedging."
            ),
            # Concepts
            "concepts": "Concepts (formal definitions & operational intent)",
            "concepts_md": (
                "### A-Book\n"
                "- **Objective**: Externalize risk to LP/market to protect internal book.\n"
                "- **When to Use**: Clients with stable profile and **rating > 3** **and** Biggest Profit > Biggest Loss.\n"
                "- **Key Risks**: LP depth/availability, slippage under bursts, credit lines, rejection ratios.\n"
                "- **Controls**: LP fan-out, throttles, max order rate, per-symbol caps, liquidity tiers.\n"
                "- **Examples**: Experienced hedgers; profit pattern not one-sided; moderate-to-large sizes with low manipulation signals.\n\n"
                "### B-Book\n"
                "- **Objective**: Internalize typical retail risk where edge is limited or negative; capture spread/behavioral PnL.\n"
                "- **When to Use**: **Default** for ratings **1–2**; also ratings 4–5 **if** Biggest Profit ≤ Biggest Loss (second-gate not passed).\n"
                "- **Key Risks**: Skilled clients, copy clusters, latency exploitation, martingale/stacking blow-ups.\n"
                "- **Controls**: Per-account exposure caps, circuit breakers, session kill-switch, behavior monitoring.\n"
                "- **Examples**: New/unproven accounts; profit asymmetry not established; or compliance-monitoring phase.\n\n"
                "### MM-Stream\n"
                "- **Objective**: An internal market-making environment to absorb **heavy/complex flows**, with the ability to throttle and hedge partially.\n"
                "- **When to Use**: Heavy trader with large typical size or ongoing bursts, even if rating alone would suggest A/B.\n"
                "- **Key Risks**: Inventory swings, adverse selection when hedging too late.\n"
                "- **Controls**: Inventory bands, dynamic spreads, partial hedge-on-fill, real-time kill logic.\n"
                "- **Examples**: High-frequency scalpers in peak hours; clustered bursts; symbol-specific stress.\n\n"
                "### Monitor (Overlay)\n"
                "- **Objective**: Add an operational **overlay** to any base route for enhanced supervision.\n"
                "- **When to Use**: Onboarding (new/delayed activation) or **compliance** signals (AML, abnormal funding, CEO flagged).\n"
                "- **Key Risks**: Rapid behavior change, KYC/AML findings, copy-leakage from risky sources.\n"
                "- **Controls**: Tighter caps, manual review for funding/withdrawal, increased sampling of orders/logs.\n"
                "- **Examples**: A-Book with Monitor for a seasoned but newly linked account; B-Book with Monitor during account warming."
            ),
            # Inputs
            "inputs": "Inputs",
            "recent_weight": "Recency weight (0.3–0.9)",
            "maxp": "Biggest Profit (abs $/pips)",
            "maxl": "Biggest Loss (abs $/pips)",
            "avg_size": "Typical position size (lots)",
            "burst": "Open-orders burst risk now?",
            "heavy": "Heavy trader?",
            "labels_title": "Select labels",
            "chips_quick": "Quick sets",
            "calc": "Compute suggestion",
            # Output
            "rating": "Computed risk rating (1–5)",
            "route": "Suggested routing",
            "reasons": "Attribution (why this rating)",
            "op": "Operational notes",
            "monitor_yes": "Add Monitor",
            "monitor_no": "No Monitor",
            "mm_tip": "Prefer MM-Stream under heavy with large sizes or ongoing bursts; throttle/hedge as configured.",
        },
        "zh": {
            "title": "📚 路由控制台",
            "subtitle": "A-Book / B-Book / MM-Stream + Monitor（覆盖层）",
            "legend": "A-Book=外部LP；B-Book=内部；MM-Stream=内部做市；Monitor=覆盖层",
            # 严谨 Hero（固定策略 + 二次门槛）
            "hero_abook": "固定策略：只有当**风险评级 > 3 且 Biggest Profit > Biggest Loss**时，才真正进入 A-Book；评级 1–2 默认留在 B-Book。",
            "hero_note": (
                "Monitor 在新户/合规等场景叠加（如新开/延迟激活、AML/异常资金、CEO 标记）；"
                "MM-Stream 属于特殊通道，主要用于处理 heavy trade 与持续爆单，可限流/分层对冲。"
            ),
            # 概念
            "concepts": "概念（定义与操作目标）",
            "concepts_md": (
                "### A-Book\n"
                "- **目标**：将风险对冲至外部 LP/市场，保护内部账簿。\n"
                "- **适用条件**：客户画像稳定，且**评级 > 3** **并且** Biggest Profit > Biggest Loss（通过二次门槛）。\n"
                "- **典型风险**：LP 深度/可得性、爆单下滑点、授信额度、拒单率。\n"
                "- **控制手段**：LP 扇出、下单限流、单/时段订单上限、分层流动性。\n"
                "- **使用样例**：成熟对冲型；利润不呈单边；中大仓位但操纵信号低。\n\n"
                "### B-Book\n"
                "- **目标**：内部化典型零售风险，获取点差/行为 PnL。\n"
                "- **适用条件**：**默认**用于**评级 1–2**；若评级 4–5 但 **Biggest Profit ≤ Biggest Loss**（未通过二次门槛），仍留在 B-Book。\n"
                "- **典型风险**：高水平客户、复制簇、时延套利、马丁/叠加爆仓。\n"
                "- **控制手段**：账户敞口上限、熔断、会话级 Kill-Switch、行为监控。\n"
                "- **使用样例**：新户/未验证画像；利润不具备单边优势；或处于合规观察期。\n\n"
                "### MM-Stream\n"
                "- **目标**：作为内部做市池承接**重/复杂**流，支持限流与部分对冲。\n"
                "- **适用条件**：heavy + 大典型手数，或存在持续爆单，即便仅从评级看可能走 A/B。\n"
                "- **典型风险**：库存波动、迟对冲导致不利选择。\n"
                "- **控制手段**：库存带、动态点差、部分对冲（成交即对冲）、实时 Kill 逻辑。\n"
                "- **使用样例**：高频剥头皮的峰值时段；簇状爆单；品种突发应激。\n\n"
                "### Monitor（覆盖层）\n"
                "- **目标**：在任一路由上叠加操作监督层。\n"
                "- **适用条件**：新户/延迟激活，或**合规**信号（AML、异常资金、CEO 标记）。\n"
                "- **典型风险**：行为快速变化、KYC/AML 发现、来自高风险来源的复制外溢。\n"
                "- **控制手段**：更严格的限额、资金流人工复核、订单/日志抽样频率提升。\n"
                "- **使用样例**：A-Book with Monitor；B-Book with Monitor。"
            ),
            # 输入
            "inputs": "输入项",
            "recent_weight": "最近行为权重（0.3–0.9）",
            "maxp": "Biggest Profit（绝对值 $/点）",
            "maxl": "Biggest Loss（绝对值 $/点）",
            "avg_size": "典型持仓规模（手）",
            "burst": "当前是否存在爆单/开单骤增？",
            "heavy": "是否 Heavy Trader？",
            "labels_title": "选择标签",
            "chips_quick": "快捷组合",
            "calc": "计算建议",
            # 输出
            "rating": "风险评级（1–5）",
            "route": "路由建议",
            "reasons": "评级归因（为何得到该分）",
            "op": "操作提示",
            "monitor_yes": "建议加 Monitor",
            "monitor_no": "无需 Monitor",
            "mm_tip": "Heavy 且大手数或持续爆单时优先考虑 MM-Stream，并配置限流/分层对冲。",
        }
    }[lang]

    LABELS_ALL = [
        "scalper","ultra short trader","hedger","martingale","arbitrage","stacking","fast TP",
        "Day trade","system spam orders","first two abnormal","changing trading behaviour",
        "swing trader","experience trader","no trade","inactive now","new account",
        "delay trade activation","changing EA","profiting","holds profit/loss","withdraw profit",
        "increasing trading size","low frequency trading","pending order","AML","abnormal funding",
        "large order","medium order","trade 1-3 lots per position","trade 3-6 lots per position",
        "trade 6+ lots per position","CEO flagged","copy trade"
    ]

    # ------- Styles -------
    st.markdown("""
        <style>
        .block-container {max-width: 1040px; padding-top: 0.5rem;}
        .hero {background: linear-gradient(135deg,#f8fafc,#eef2ff);
               border:1px solid #e2e8f0;border-radius:14px;padding:16px 18px;margin:.5rem 0;}
        .subtle {color:#64748b;font-size:.92rem}
        .card {background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;padding:14px;margin:.35rem 0;}
        .warn {background:#fff7ed;border-left:4px solid #f59e0b;padding:.6rem .9rem;border-radius:10px;}
        .route-badge {display:inline-block;padding:.25rem .65rem;border-radius:10px;
                      font-weight:600;border:1px solid #e5e7eb;margin-right:.35rem}
        .route-ab {background:#eefdfb;}
        .route-bb {background:#f8fafc;}
        .route-mm {background:#f0f9ff;}
        .monitor {background:#f5f3ff;}
        .h3tight {margin:8px 0 2px 0;}
        .chip {display:inline-block;padding:.12rem .6rem;border-radius:999px;border:1px solid #e5e7eb;
               margin:.2rem .35rem .2rem 0;background:#fff;font-size:.85rem}
        </style>
    """, unsafe_allow_html=True)

    # ------- Header -------
    st.title(T["title"])
    st.markdown(f"<div class='subtle'>{T['subtitle']}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='hero'><div style='font-size:1rem;margin-bottom:.3rem'>{T['hero_abook']}</div>"
        f"<div class='subtle'>{T['hero_note']}</div></div>", unsafe_allow_html=True
    )
    st.caption(T["legend"])

    # ------- Concepts -------
    with st.expander("🧭 " + T["concepts"], expanded=True):
        st.markdown(T["concepts_md"])

    # ------- Inputs -------
    st.markdown("### 🧩 " + T["inputs"])
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        recent_weight = st.slider(T["recent_weight"], 0.3, 0.9, 0.7, 0.05)
    with c2:
        heavy = st.checkbox(T["heavy"], value=False)
    with c3:
        burst = st.checkbox(T["burst"], value=False)
    with c4:
        avg_size = st.number_input(T["avg_size"], value=1.5, step=0.5, min_value=0.0)

    c5, c6 = st.columns(2)
    with c5:
        max_profit = st.number_input(T["maxp"], value=1000.0, step=100.0, min_value=0.0)
    with c6:
        max_loss = st.number_input(T["maxl"], value=800.0, step=100.0, min_value=0.0)

    # 快捷组合
    st.markdown("<div class='subtle' style='margin-top:.25rem'>" + T["chips_quick"] + "：</div>", unsafe_allow_html=True)
    quick_sets = {
        "Scalper": ["scalper","fast TP","Day trade"],
        "Martingale": ["martingale","stacking"],
        "Compliance": ["AML","abnormal funding","CEO flagged"],
        "New/Inactive": ["new account","delay trade activation","inactive now"],
        "Large size": ["large order","trade 6+ lots per position"],
        "Experienced": ["experience trader","hedger"]
    }
    chips = []
    cols = st.columns(6)
    for i, (name, vals) in enumerate(quick_sets.items()):
        with cols[i % 6]:
            if st.button(name):
                chips.extend(vals)
    chosen_labels = st.multiselect(T["labels_title"], LABELS_ALL, default=list(dict.fromkeys(chips)))

    # ------- Compute -------
    st.divider()
    if st.button("✅ " + T["calc"]):
        score = 0.0
        reasons = []

        # Profit/Loss shape
        if max_profit > 0 or max_loss > 0:
            ratio = (max_profit + 1e-9) / (max_loss + 1e-9)
            prof_signal = 2.0 * (ratio - 1.0) / (abs(ratio) + 1.0)  # bounded symmetric transform
            score += prof_signal
            reasons.append(f"P/L shape ratio≈{ratio:.2f} → {prof_signal:+.2f}")

        # Size buckets
        if "trade 6+ lots per position" in chosen_labels or avg_size >= 6:
            score += 1.2; reasons.append("Size ≥6 lots → +1.2")
        elif "trade 3-6 lots per position" in chosen_labels or avg_size >= 3:
            score += 0.7; reasons.append("Size 3–6 lots → +0.7")
        elif "trade 1-3 lots per position" in chosen_labels or avg_size >= 1:
            score += 0.3; reasons.append("Size 1–3 lots → +0.3")

        # Risk-up
        risk_up = {
            "scalper": 0.6, "ultra short trader": 0.7, "martingale": 1.3, "arbitrage": 1.0,
            "stacking": 0.7, "fast TP": 0.5, "system spam orders": 0.9, "first two abnormal": 0.5,
            "changing trading behaviour": 0.4, "changing EA": 0.4, "increasing trading size": 0.6,
            "AML": 1.6, "abnormal funding": 1.1, "large order": 0.8, "medium order": 0.4,
            "pending order": 0.2, "Day trade": 0.3, "copy trade": 0.6
        }
        for lb, w in risk_up.items():
            if lb in chosen_labels:
                score += w; reasons.append(f"Label '{lb}' → +{w}")

        # Risk-down
        risk_down = {
            "hedger": -0.7, "experience trader": -0.4, "low frequency trading": -0.25,
            "swing trader": -0.15, "holds profit/loss": -0.15, "withdraw profit": -0.15,
            "no trade": -0.25, "inactive now": -0.35, "profiting": -0.15,
        }
        for lb, w in risk_down.items():
            if lb in chosen_labels:
                score += w; reasons.append(f"Label '{lb}' → {w}")

        # Heavy affects rating only
        if heavy:
            score += 0.6; reasons.append("Heavy trader → +0.6 (rating influence only)")

        # Recency weighting
        score *= (0.5 + recent_weight/2)
        reasons.append(f"Recency weighting {recent_weight:.2f} applied")

        # Map to rating 1–5
        rating_raw = 3 + 2 * (score / 3.0)
        rating = int(min(5, max(1, round(rating_raw))))

        # ----- Routing (fixed) with second-gate -----
        abook_gate = (rating > 3) and (max_profit > max_loss)

        if abook_gate:
            base_route = "A-Book"
            route_badge = "<span class='route-badge route-ab'>A-Book</span>"
            base_note = "Rating > 3 and Biggest Profit > Biggest Loss → route to A-Book."
        else:
            base_route = "B-Book"
            route_badge = "<span class='route-badge route-bb'>B-Book</span>"
            if rating > 3 and not (max_profit > max_loss):
                base_note = "Rating > 3 but Biggest Profit ≤ Biggest Loss → stay in B-Book."
            else:
                base_note = "Rating ≤ 3 → stay in B-Book."

        # MM heuristic (non-forcing)
        prefer_mm = False
        if heavy and (avg_size >= 3 or "trade 3-6 lots per position" in chosen_labels or "trade 6+ lots per position" in chosen_labels):
            prefer_mm = True
        if burst and (heavy or avg_size >= 3):
            prefer_mm = True

        # Monitor overlay (no correlation input)
        need_monitor = False
        op_notes = [base_note]

        if "new account" in chosen_labels or "delay trade activation" in chosen_labels:
            need_monitor = True
            op_notes.append("Onboarding: add Monitor.")
        if "AML" in chosen_labels or "abnormal funding" in chosen_labels or "CEO flagged" in chosen_labels:
            need_monitor = True
            op_notes.append("Compliance flags: add Monitor.")

        # Burst notes
        if burst and base_route == "A-Book":
            op_notes.append("Burst on A-Book: verify LP depth, throttles, credit lines.")
        elif burst:
            op_notes.append("Burst internalized: enforce throttles/position caps/circuit breakers.")

        if prefer_mm:
            op_notes.append(T["mm_tip"])

        # ------- Output -------
        st.markdown("### ⭐ " + T["rating"])
        st.progress(rating / 5.0)
        st.caption(f"{rating} / 5")

        st.markdown("### 🧭 " + T["route"])
        monitor_badge = "<span class='route-badge monitor'>Monitor</span>" if need_monitor else ""
        mm_badge = "<span class='route-badge route-mm'>MM-Stream</span>" if prefer_mm else ""
        extra_monitor = " + Monitor" if need_monitor else ""
        extra_mm = " + MM-Stream (preferred)" if prefer_mm else ""

        route_html = (
            "<div class='card'>"
            "<h3 class='h3tight'>"
            f"{route_badge} {monitor_badge} {mm_badge}"
            "</h3>"
            f"<div class='subtle' style='margin-top:.25rem'>{base_route}{extra_monitor}{extra_mm}</div>"
            "</div>"
        )
        st.markdown(route_html, unsafe_allow_html=True)

        st.markdown("### 🔎 " + T["reasons"])
        st.markdown(
            "<div class='card'><ul>" + "".join([f"<li>{r}</li>" for r in reasons]) + "</ul></div>",
            unsafe_allow_html=True
        )

        if op_notes:
            st.markdown("### ⚙️ " + T["op"])
            st.markdown(
                "<div class='warn'><ul>" + "".join([f"<li>{n}</li>" for n in op_notes]) + "</ul></div>",
                unsafe_allow_html=True
            )
