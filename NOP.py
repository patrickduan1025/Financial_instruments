import streamlit as st
import pandas as pd

def nop_page():
    translations = {
        "en": {
            "title": "📈 Net Open Position (NOP) Dashboard",
            "concept": "Concept",
            "concept_text": (
                "Net Open Position (NOP) = Total Longs - Total Shorts, for each product. "
                "Reflects your true net risk exposure per asset, crucial for risk management, compliance and reporting."
            ),
            "formula": "NOP = Σ(Long Positions) - Σ(Short Positions)",
            "result": "Net Position (NOP)",
            "nop_table": "Net Open Position Overview",
            "product": "Instrument",
            "add_order": "Add Position",
            "import_csv": "Import Orders (CSV)",
            "export_csv": "Export Orders (CSV)",
            "longs": "Long Size",
            "shorts": "Short Size",
            "direction": "Direction",
            "size": "Position Size",
            "summary": "Summary & Warnings",
            "risk_note": "If NOP < 0: Net short. If NOP > 0: Net long. NOP = 0: Fully hedged.",
            "compliance_tip": "NOP is a regulatory metric for broker/prop desk risk. Always track NOP by product and total portfolio.",
            "reset": "Clear All Orders",
            "examples": "Examples",
            "ex1": "EUR/USD: Long 200,000, Short 150,000 → NOP = +50,000 (Net Long)",
            "ex2": "BTC/USD: Long 1, Short 1.5 → NOP = -0.5 (Net Short)",
            "warning_high_nop": "⚠️ NOP exceeds 1,000,000 units for this product! Consider reducing net risk.",
            "fully_hedged": "🟢 Fully Hedged",
            "net_long": "🔵 Net Long",
            "net_short": "🔴 Net Short"
        },
        "zh": {
            "title": "📈 净持仓（NOP）终端",
            "concept": "概念",
            "concept_text": (
                "净持仓（NOP）= 多头总量 − 空头总量（按品种统计）。"
                "真实反映每个品种的风险暴露，是风控与监管合规的核心指标。"
            ),
            "formula": "净持仓 = 多头持仓总和 − 空头持仓总和",
            "result": "净持仓 (NOP)", # <--- ADD THIS
            "nop_table": "各品种净持仓总览",
            "product": "品种",
            "add_order": "添加持仓",
            "import_csv": "导入订单（CSV）",
            "export_csv": "导出订单（CSV）",
            "longs": "多头",
            "shorts": "空头",
            "direction": "方向",
            "size": "持仓量",
            "summary": "汇总与预警",
            "risk_note": "NOP<0：净空头；NOP>0：净多头；NOP=0：完全对冲。",
            "compliance_tip": "NOP是机构监管风险核心指标，请分别统计每个品种和总账面NOP。",
            "reset": "清空全部持仓",
            "examples": "示例",
            "ex1": "EUR/USD：多头20万，空头15万 → NOP=+5万（净多头）",
            "ex2": "BTC/USD：多头1，空头1.5 → NOP=-0.5（净空头）",
            "warning_high_nop": "⚠️ 该品种净持仓已超百万单位！请注意风险暴露。",
            "fully_hedged": "🟢 完全对冲",
            "net_long": "🔵 净多头",
            "net_short": "🔴 净空头"
        }
    }

    lang = st.session_state.get("language", "en")
    t = translations[lang]
    st.markdown("""
        <style>
        .block-container {max-width: 950px; padding-top: 2rem;}
        .stDataFrame thead tr th {background: #f6f8fa !important;}
        .risk-box {background:#f7f7e7;border-radius:0.7em;padding:1em 1.5em;}
        .warning {color:#d54f0e;font-weight:bold;}
        .success {color:#107313;font-weight:bold;}
        </style>
    """, unsafe_allow_html=True)

    st.title(t["title"])

    with st.expander("💡 " + t["concept"], expanded=False):
        st.markdown(f"{t['concept_text']}")
        st.code(t["formula"])
        st.caption(t["risk_note"])

    st.divider()

    # 支持多产品批量订单录入
    default_products = ["EUR/USD", "USD/JPY", "XAUUSD", "BTC/USD", "ETH/USD"]
    if "nop_orders" not in st.session_state:
        st.session_state["nop_orders"] = []

    # 新订单录入
    with st.form("add_nop_order_form"):
        c1, c2, c3 = st.columns([3,2,2])
        with c1:
            product = st.selectbox(t["product"], default_products, key="nop_product")
        with c2:
            direction = st.selectbox(t["direction"], [t["longs"], t["shorts"]], key="nop_dir")
        with c3:
            size = st.number_input(t["size"], min_value=0.0, value=100000.0)
        add_btn = st.form_submit_button(t["add_order"])
        if add_btn:
            st.session_state["nop_orders"].append({
                "Product": product,
                "Direction": direction,
                "Size": size
            })
            st.success("✅ Added.")

    # 导入导出CSV
    csv_cols = ["Product", "Direction", "Size"]
    csv_buffer = None
    c0, c1, c2 = st.columns([2,2,2])
    with c0:
        uploaded = st.file_uploader(t["import_csv"], type=["csv"])
        if uploaded is not None:
            df = pd.read_csv(uploaded)
            if set(csv_cols).issubset(df.columns):
                st.session_state["nop_orders"] = df[csv_cols].to_dict("records")
                st.success("Imported!")
            else:
                st.error("Invalid CSV columns.")
    with c1:
        if st.session_state["nop_orders"]:
            df_exp = pd.DataFrame(st.session_state["nop_orders"])
            st.download_button(t["export_csv"], df_exp.to_csv(index=False).encode(), "nop_orders.csv")

    with c2:
        if st.button(t["reset"]):
            st.session_state["nop_orders"] = []

    st.divider()

    # 汇总各产品NOP
    if st.session_state["nop_orders"]:
        df = pd.DataFrame(st.session_state["nop_orders"])
        nop_summaries = []
        for product in df["Product"].unique():
            prod_orders = df[df["Product"] == product]
            long_sum = prod_orders[prod_orders["Direction"] == t["longs"]]["Size"].sum()
            short_sum = prod_orders[prod_orders["Direction"] == t["shorts"]]["Size"].sum()
            nop = long_sum - short_sum
            # 状态判定
            if nop == 0:
                status = t["fully_hedged"]
                color = "🟢"
            elif nop > 0:
                status = t["net_long"]
                color = "🔵"
            else:
                status = t["net_short"]
                color = "🔴"
            warning = t["warning_high_nop"] if abs(nop) >= 1_000_000 else ""
            nop_summaries.append({
                t["product"]: product,
                t["longs"]: long_sum,
                t["shorts"]: short_sum,
                t["result"]: nop,
                "Status": status,
                "Warning": warning
            })
        # 展示 DataFrame
        sum_df = pd.DataFrame(nop_summaries)
        st.dataframe(sum_df, use_container_width=True, hide_index=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # 汇总净持仓（全品种合计）
        net_nop_total = sum_df[t["result"]].sum()
        st.markdown(f"""
        <div class="risk-box">
            <b>Portfolio Net NOP：</b> <span class="{'success' if net_nop_total==0 else ('warning' if abs(net_nop_total)>1_000_000 else '')}">{net_nop_total:,.2f}</span>
            <br>{t['risk_note']}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("📄 " + t["nop_table"] + ": " + t["no_orders"] if "no_orders" in t else "No open positions yet. Please add orders above.")

    st.divider()
    # 示例区
    with st.expander("📖 " + t["examples"], expanded=False):
        st.markdown(f"- {t['ex1']}")
        st.markdown(f"- {t['ex2']}")
        st.caption("💡 " + t["compliance_tip"])

# 直接用 nop_page()
