import streamlit as st
import pandas as pd

def ea_page():
    translations = {
        "en": {
            "title": "🤖 What is an EA (Expert Advisor)?",
            "intro": (
                "An EA is a rule-based trading robot that can analyze markets and place/close orders "
                "automatically in MT4/MT5 or other platforms. Below are common EA families, when they work, "
                "and what to watch out for."
            ),
            "compare_title": "🆚 Common EA Families – Quick Comparison",
            "col_strategy": "EA Type / Logic",
            "col_regime": "Best Market Regime",
            "col_freq": "Trading Frequency",
            "col_risk": "Risk Profile",
            "col_edge": "Strengths",
            "col_pitfall": "Pitfalls",
            "rows": [
                ["MA Crossover / Trend-Following","Trending (clear momentum)","Low–Medium","Medium","Simple, robust; rides large trends","Whipsaws in choppy ranges; needs filters"],
                ["Breakout (Range → Expansion)","Low volatility squeeze → expansion","Medium","Medium","Captures big moves after consolidation","False breakouts; needs volatility/time filters"],
                ["Mean Reversion (RSI/BB)","Range-bound, mean-reverting","Medium–High","Medium–High","Many small wins in ranges","Trend days can cause large losses"],
                ["Grid / Martingale","Sideways or gently trending","High","High","High win-rate illusion without forecasting","Tail risk; equity cliffs during trends"],
                ["News / Event EA","High-impact news windows","Low (but bursty)","High","Targets volatility bursts","Slippage, spreads widen; broker rules"],
                ["ATR Trailing Stop Trend","Sustained trends with pullbacks","Low–Medium","Medium","Let profits run, cuts losses","Gives back profit in reversals; late entries"],
            ],
            "picker_title": "🔍 Explore EA Types",
            "picker_label": "Choose an EA family to learn more",
            "details": {
                "MA":  {"name":"MA Crossover / Trend-Following","how":"Enter when fast MA crosses slow MA; exit on opposite cross or ATR stop.","use":"Liquid FX pairs, indices, gold during directional trends.","risk":"Use fixed fractional risk, ATR-based stop, avoid ranging hours.","metrics":"Low win-rate with higher payoff. Watch MAR, max drawdown, profit factor."},
                "BRK": {"name":"Breakout EA","how":"Detect range (Donchian/NR7). Buy/sell on break with volatility filter.","use":"Session opens, post-news expansions.","risk":"Initial stop behind range. Reduce size when spreads widen.","metrics":"Expectancy concentrated on expansion days. Track slippage."},
                "MR":  {"name":"Mean Reversion EA","how":"Fade RSI/BB extremes toward mean. Scale out near mid-band.","use":"Ranging hours and symbols.","risk":"Hard stop beyond band expansion. Avoid strong-trend days.","metrics":"High hit-rate with tail losses. Watch skew/kurtosis and MAE."},
                "GRID":{"name":"Grid / Martingale EA","how":"Layer orders every X pips, often increasing size after losses.","use":"Long ranges without one-way trends.","risk":"Extreme tail risk. Need equity cap, circuit breaker, news pause.","metrics":"Do not trust win-rate alone. Stress test with trend walk-forward."},
                "NEWS":{"name":"News / Event EA","how":"Time-based triggers around events. Straddle or momentum continuation.","use":"CPI, NFP, rate decisions.","risk":"Slippage and widened spreads. Verify broker rules and execution.","metrics":"Execution quality dominates. Track realized versus expected slippage."},
                "ATR": {"name":"ATR Trailing Stop Trend EA","how":"Trend filter (MA slope or ADX). Trail stop by k×ATR.","use":"Persistent trends with pullbacks.","risk":"ATR multiple too tight → stop-outs. Too loose → giveback.","metrics":"Average win much larger than average loss. Focus on long-run CAGR and DD."},
            },
            "checklist_title": "✅ Backtest & Risk Checklist",
            "checklist": [
                "Data quality: tick vs 1m, realistic spreads, commissions and swaps.",
                "Walk-forward and out-of-sample validation across symbols and sessions.",
                "Slippage model for news and volatility. Test widened spreads.",
                "Position sizing: fixed-fractional or volatility-scaling. Daily loss limit.",
                "Circuit breakers: news pause, max drawdown stop, max open orders.",
                "Broker constraints: hedging, FIFO, min distance, execution type."
            ],
            "btn_show_table": "Show / Hide Comparison Table",

            # New: Seen-in-the-wild EA list
            "wild_title": "🗂️ EAs we have seen in the wild",
            "wild_intro": "These are example identifiers we have encountered in order comments or EA signatures. They are labels or device-model strings, not strategy names.",
            "wild_cols": ["Identifier", "Vendor/Model", "Notes"],
            "wild_rows": [
                ["I40O", "Internal code", "Generic ID seen in flow. Strategy varies by build."],
                ["I50O", "Internal code", "Another internal series. Classification needs case-by-case review."],
                ["I60O", "Internal code", "Often appears with short holding patterns in some accounts."],
                ["I61O", "Internal code", "Variant with ATR-like trailing behavior observed in logs."],
                ["HUAWEI/ANA-AN00_AO", "HUAWEI", "Device string found in comments. Not a strategy by itself."],
                ["HONOR/ALI-AN00_AO", "HONOR", "Device model tag observed in order notes."],
                ["Redmi/23013RK75C_AO", "Redmi", "Android model tag carried through to EA signature."],
                ["OPPO/PEQM00_AO", "OPPO", "Vendor-model label. Treat as source identifier."],
                ["vivo/V2425A_AO", "vivo", "Model string from environment or EA build."],
                ["OnePlus/PHK110_AO", "OnePlus", "Seen as part of user agent style comment."]
            ],

            # New: Toxic EA
            "toxic_title": "☣️ What is a Toxic EA?",
            "toxic_def": (
                "A toxic EA is one whose order flow systematically exploits execution asymmetries or stale prices, "
                "creating abnormal adverse selection and broker-side losses that are not explained by ordinary trading risk."
            ),
            "toxic_signals_title": "Early warning signals",
            "toxic_signals": [
                "Very short holding time with unusually positive slippage profile around news or session opens.",
                "PnL clustered in narrow time windows (macro events) while outside windows shows little activity.",
                "Win-rate very high with tiny average win but rare large losses avoided due to fast exits or cancels.",
                "Latency arbitrage patterns: entries at top-of-burst ticks, price advantage vs VWAP within seconds.",
                "Order storms: many micro-orders or cancels within milliseconds across multiple symbols.",
                "Copy-trade from a known toxic source; identical timestamps across accounts."
            ],
            "toxic_mitigations_title": "Mitigations",
            "toxic_mitigations": [
                "News protections and dynamic spread controls around high-impact events.",
                "Minimum holding time or last-look style checks per venue rules.",
                "Throttle order rate and cap concurrent positions; enforce daily loss limits.",
                "Virtual SL/TP with server-side hard stops; reject orders breaching min distance.",
                "Continuous slippage monitoring and toxic-source lists for routing decisions."
            ],
        },

        "zh": {
            "title": "🤖 什么是 EA（自动交易程序）？",
            "intro": "EA 是基于规则的交易机器人，可在 MT4/MT5 等平台自动分析并下单或平仓。下面列出常见家族、适用场景与风险要点。",
            "compare_title": "🆚 常见 EA 家族对比",
            "col_strategy": "策略类型/逻辑",
            "col_regime": "最适市场状态",
            "col_freq": "交易频率",
            "col_risk": "风险画像",
            "col_edge": "优势",
            "col_pitfall": "常见问题",
            "rows": [
                ["均线金叉/趋势跟随","单边趋势明显","低-中","中","结构简单、可吃到大趋势","震荡时易被反复打止损，需要过滤"],
                ["突破（盘整→扩张）","低波动收敛后将扩张","中","中","抓住盘整后的大波动","假突破多，需要波动/时间过滤"],
                ["均值回归（RSI/布林）","区间震荡、均值回归","中-高","中-高","区间内小胜多","趋势日可能出现大亏"],
                ["网格/马丁","宽幅震荡或缓慢单边","高","高","胜率高的表象","尾部风险极大，趋势中易爆仓"],
                ["新闻/事件 EA","高影响力新闻窗口","低（但爆发）","高","捕捉事件波动","滑点与点差放大，需要合规检查"],
                ["ATR 趋势拖尾","有回撤的持续趋势","低-中","中","让利润奔跑，止损明确","反转时回吐较多，进场偏慢"],
            ],
            "picker_title": "🔍 展开查看 EA 细节",
            "picker_label": "选择一个 EA 家族",
            "details": {
                "MA":  {"name":"均线金叉 / 趋势跟随","how":"快均线越过慢均线进场，反向或 ATR 止损离场。","use":"外汇主流、指数、黄金的趋势阶段。","risk":"用 ATR 止损与固定比例控仓，避开震荡时段。","metrics":"胜率偏低但盈亏比高，关注 MAR、最大回撤、收益因子。"},
                "BRK": {"name":"突破 EA","how":"识别盘整区间（Donchian/NR7），突破配合波动过滤进场。","use":"开盘时段与新闻后扩张。","risk":"初始止损放在区间外，点差异常时减仓。","metrics":"期望值集中在扩张日，重点跟踪滑点。"},
                "MR":  {"name":"均值回归 EA","how":"在 RSI/布林带极值反转，靠近中轨分批止盈。","use":"震荡市与安静时段。","risk":"极端扩张设置硬止损，趋势日尽量规避。","metrics":"命中率高但尾部损失大，关注偏度/峰度与最大不利波动。"},
                "GRID":{"name":"网格 / 马丁","how":"按固定间距分层挂单，亏损后可能加倍补仓。","use":"长时间宽幅震荡。","risk":"尾部风险很大，需要权益上限、熔断、新闻暂停。","metrics":"不要被高胜率迷惑，要做趋势压力回放。"},
                "NEWS":{"name":"新闻 / 事件 EA","how":"在事件时间点触发进场，对敲或顺势延续。","use":"CPI、非农、利率决议等。","risk":"滑点与点差大，需核对经纪商规则与执行。","metrics":"执行质量决定结果，跟踪实际与预期滑点。"},
                "ATR": {"name":"ATR 拖尾止损 EA","how":"趋势过滤（均线斜率或 ADX），止损跟随 k×ATR。","use":"持续趋势且回撤有序。","risk":"ATR 倍数过紧易被扫，过松回吐多。","metrics":"平均盈利明显大于平均亏损，关注长期 CAGR 与回撤。"},
            },
            "checklist_title": "✅ 回测与风控清单",
            "checklist": [
                "数据质量：tick 与 1m、真实点差、佣金与隔夜利息是否计入",
                "走步验证与样本外测试，覆盖多个品种与时段",
                "为新闻和高波动建模滑点，并测试点差放大情景",
                "仓位：固定比例或波动缩放，设置日亏限",
                "熔断：新闻暂停、最大回撤停机、最大持仓与订单数限制",
                "经纪商限制：是否允许对冲/FIFO、最小止损距离、执行类型"
            ],
            "btn_show_table": "显示/隐藏 对比表",

            # 新增：我们见过的 EA/设备标识
            "wild_title": "🗂️ 我们见过的 EA / 设备标识",
            "wild_intro": "以下是在订单注释或 EA 签名里出现过的标识。它们是标签或设备型号，并非策略名称。",
            "wild_cols": ["标识", "厂商/型号", "备注"],
            "wild_rows": [
                ["I40O", "内部编号", "在多账户出现过，具体策略需按构建版本判定"],
                ["I50O", "内部编号", "同系列编号，需结合日志分类"],
                ["I60O", "内部编号", "部分账户出现短持仓特征"],
                ["I61O", "内部编号", "日志里呈现类似 ATR 拖尾的出场方式"],
                ["HUAWEI/ANA-AN00_AO", "华为", "注释里的设备字符串，本身不是策略"],
                ["HONOR/ALI-AN00_AO", "荣耀", "订单备注中的机型标签"],
                ["Redmi/23013RK75C_AO", "红米", "来自系统或 EA 构建环境的型号"],
                ["OPPO/PEQM00_AO", "OPPO", "厂商型号标签，可作来源识别"],
                ["vivo/V2425A_AO", "vivo", "类似 UA 的型号字符串"],
                ["OnePlus/PHK110_AO", "一加", "在部分订单注释中出现过"]
            ],

            # 新增：Toxic EA
            "toxic_title": "☣️ 什么是 Toxic EA？",
            "toxic_def": "Toxic EA 指利用执行不对称或陈旧报价等结构性漏洞获取超额优势，从而给经纪商侧带来异常不利选择和损失的策略流。",
            "toxic_signals_title": "识别信号",
            "toxic_signals": [
                "持仓极短但在新闻或开盘时段获得异常正向滑点",
                "盈利高度集中在少数时间窗口，其他时间几乎不交易",
                "胜率很高且单笔很小，但通过极快退出规避大亏",
                "延迟套利特征：进场价格显著优于同期 VWAP，常在波峰波谷成交",
                "短时大量微订单与撤单，多品种同时发生",
                "复制自已知的“毒性源”，多个账户时间戳高度一致"
            ],
            "toxic_mitigations_title": "缓解措施",
            "toxic_mitigations": [
                "新闻保护与动态点差，在高影响事件前后加强风控",
                "最小持仓时长或 last-look 类检查（遵守场所规则）",
                "限流：限制下单速率与并发持仓，设置日亏限",
                "虚拟止损/止盈配合服务器硬止损，拒绝不满足最小距离的订单",
                "持续监控滑点画像，维护毒性来源名单并调整路由"
            ],
        }
    }

    lang = st.session_state.get("language", "en")
    t = translations[lang]

    st.markdown("""
        <style>
        .block-container {max-width: 900px; padding-top:2rem;}
        .pros-card {background:#ebfaf4;border-radius:1.1em;padding:1em 1.2em;}
        .cons-card {background:#fff6f0;border-radius:1.1em;padding:1em 1.2em;}
        </style>
    """, unsafe_allow_html=True)

    st.title(t["title"])
    st.write(t["intro"])

    # 对比表
    with st.expander(t["btn_show_table"], expanded=True):
        df = pd.DataFrame(t["rows"], columns=[t["col_strategy"], t["col_regime"], t["col_freq"], t["col_risk"], t["col_edge"], t["col_pitfall"]])
        st.subheader(t["compare_title"])
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.divider()

    # 选择器
    st.subheader(t["picker_title"])
    options = {
        "MA": t["details"]["MA"]["name"],
        "BRK": t["details"]["BRK"]["name"],
        "MR": t["details"]["MR"]["name"],
        "GRID": t["details"]["GRID"]["name"],
        "NEWS": t["details"]["NEWS"]["name"],
        "ATR": t["details"]["ATR"]["name"],
    }
    key = st.selectbox(t["picker_label"], options=list(options.keys()), format_func=lambda k: options[k])

    d = t["details"][key]
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"### {d['name']}")
        st.markdown(f"**How it works ：** {d['how']}")
        st.markdown(f"**Best use ：** {d['use']}")
    with c2:
        st.markdown(f"**Risk：** {d['risk']}")
        st.markdown(f"**Key metrics：** {d['metrics']}")

    st.divider()

    # 我们见过的 EA/设备标识
    st.subheader(t["wild_title"])
    st.write(t["wild_intro"])
    wild_df = pd.DataFrame(t["wild_rows"], columns=t["wild_cols"])
    st.dataframe(wild_df, hide_index=True, use_container_width=True)

    st.divider()

    # Toxic EA
    st.subheader(t["toxic_title"])
    st.write(t["toxic_def"])
    st.markdown("**" + t["toxic_signals_title"] + "**")
    for s in t["toxic_signals"]:
        st.markdown(f"- {s}")
    st.markdown("**" + t["toxic_mitigations_title"] + "**")
    for s in t["toxic_mitigations"]:
        st.markdown(f"- {s}")

    st.divider()
    st.subheader(t["checklist_title"])
    st.markdown("<div class='pros-card'>" + "<br>".join([f"- {item}" for item in t["checklist"]]) + "</div>", unsafe_allow_html=True)
