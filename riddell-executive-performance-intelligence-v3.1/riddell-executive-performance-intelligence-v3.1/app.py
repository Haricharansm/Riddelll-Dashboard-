
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
ASSET_DIR = APP_DIR / "assets"
LOGO_PATH = ASSET_DIR / "riddell-logo.png"
LOGO_IMAGE = Image.open(LOGO_PATH)

st.set_page_config(
    page_title="Riddell Executive Performance Intelligence",
    page_icon=LOGO_IMAGE,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# Riddell visual system
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
        :root {
            --riddell-red: #C8102E;
            --riddell-red-soft: #FFF3F4;
            --ink: #20232B;
            --muted: #6B7280;
            --line: #E5E7EB;
            --surface: #FFFFFF;
            --surface-soft: #F7F8FA;
            --good: #15803D;
            --watch: #B45309;
            --critical: #B42318;
        }

        /* Keep app content below Streamlit's hosted toolbar */
        .block-container {
            padding-top: 3.3rem;
            padding-bottom: 2.2rem;
            max-width: 1460px;
        }

        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: -0.025em;
        }

        h2 { margin-top: .3rem; }
        h3 { margin-top: 1.2rem; }

        /* Main app bar */
        .appbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            padding: 0 0 .7rem 0;
        }

        .appbar-center {
            flex: 1;
            min-width: 0;
        }

        .app-title {
            color: var(--ink);
            font-size: 1.55rem;
            font-weight: 850;
            line-height: 1.1;
            letter-spacing: -0.025em;
            white-space: nowrap;
        }

        .app-subtitle {
            color: var(--muted);
            font-size: .88rem;
            margin-top: .22rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .app-meta {
            text-align: right;
            color: var(--muted);
            font-size: .79rem;
            line-height: 1.5;
            white-space: nowrap;
        }

        .brand-rule {
            height: 3px;
            background: var(--riddell-red);
            border-radius: 99px;
            margin: 0 0 1.25rem 0;
        }

        .section-kicker {
            color: var(--riddell-red);
            text-transform: uppercase;
            letter-spacing: .08em;
            font-size: .76rem;
            font-weight: 800;
            margin-bottom: .2rem;
        }

        .section-copy {
            color: var(--muted);
            font-size: .92rem;
            margin-top: -.25rem;
            margin-bottom: .8rem;
        }

        /* Pulse */
        .pulse-card {
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 14px 16px 13px 16px;
            background: var(--surface);
            min-height: 108px;
            box-shadow: 0 1px 2px rgba(0,0,0,.025);
        }

        .pulse-label {
            color: var(--muted);
            font-size: .74rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .065em;
        }

        .pulse-number {
            font-size: 2rem;
            line-height: 1;
            margin: .38rem 0 .3rem 0;
            font-weight: 850;
        }

        .pulse-desc {
            color: #4B5563;
            font-size: .82rem;
            line-height: 1.25;
        }

        .good { color: var(--good); }
        .watch { color: var(--watch); }
        .critical { color: var(--critical); }

        /* AI brief */
        .ai-brief {
            border: 1px solid #F0CED4;
            border-left: 5px solid var(--riddell-red);
            border-radius: 12px;
            background: linear-gradient(90deg, var(--riddell-red-soft) 0%, #FFFFFF 58%);
            padding: 16px 18px;
            margin: .65rem 0 1.1rem 0;
        }

        .ai-grid {
            display: grid;
            grid-template-columns: 1.65fr .85fr;
            gap: 24px;
            align-items: start;
        }

        .ai-title {
            color: var(--ink);
            font-size: 1.03rem;
            font-weight: 850;
            margin-bottom: .32rem;
        }

        .ai-copy {
            color: #424752;
            font-size: .9rem;
            line-height: 1.45;
        }

        .focus-box {
            border-left: 1px solid #EBC4CB;
            padding-left: 18px;
        }

        .focus-label {
            color: var(--riddell-red);
            font-size: .72rem;
            font-weight: 850;
            letter-spacing: .07em;
            text-transform: uppercase;
        }

        .focus-value {
            color: var(--ink);
            font-size: .95rem;
            font-weight: 800;
            margin-top: .25rem;
        }

        .focus-copy {
            color: var(--muted);
            font-size: .8rem;
            margin-top: .25rem;
            line-height: 1.35;
        }

        /* Connected process-health strip */
        .process-strip {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 8px;
            margin: .45rem 0 1.15rem 0;
        }

        .process-node {
            position: relative;
            border: 1px solid var(--line);
            border-top: 3px solid var(--riddell-red);
            border-radius: 11px;
            padding: 11px 12px;
            background: #FFFFFF;
            min-height: 132px;
            width: 100%;
            box-sizing: border-box;
        }

        .process-name {
            color: var(--muted);
            font-size: .68rem;
            font-weight: 800;
            letter-spacing: .045em;
            text-transform: uppercase;
            min-height: 34px;
            line-height: 1.25;
            overflow-wrap: anywhere;
        }

        .process-score {
            color: var(--ink);
            font-size: 1.55rem;
            font-weight: 850;
            line-height: 1;
            margin: .3rem 0 .4rem 0;
        }

        .process-status {
            font-size: .79rem;
            font-weight: 800;
        }

        .process-health {
            color: #9CA3AF;
            font-size: .71rem;
            margin-top: .35rem;
        }

        /* Exception cards */
        .exception-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            margin: .5rem 0 1rem 0;
        }

        .exception-card {
            border: 1px solid var(--line);
            border-radius: 11px;
            background: #FFFFFF;
            padding: 12px 14px;
        }

        .exception-title {
            color: var(--ink);
            font-weight: 800;
            font-size: .88rem;
            margin-bottom: .22rem;
        }

        .exception-copy {
            color: var(--muted);
            font-size: .78rem;
            line-height: 1.38;
        }

        .mini-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }

        .mini-dot.critical { background: var(--critical); }
        .mini-dot.watch { background: var(--watch); }
        .mini-dot.good { background: var(--good); }

        /* KPI story / governance */
        .story-card {
            border: 1px solid var(--line);
            border-left: 4px solid var(--riddell-red);
            border-radius: 10px;
            padding: 12px 14px;
            background: #FFFFFF;
            margin: 8px 0;
        }

        .story-kicker {
            color: var(--riddell-red);
            font-size: .7rem;
            text-transform: uppercase;
            letter-spacing: .07em;
            font-weight: 850;
        }

        .story-title {
            color: var(--ink);
            font-size: 1rem;
            font-weight: 820;
            margin: .18rem 0;
        }

        .story-copy {
            color: var(--muted);
            font-size: .82rem;
            line-height: 1.4;
        }

        .trust-card {
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 18px;
            background: #FFFFFF;
        }

        /* Streamlit primitives */
        [data-testid="stMetric"] {
            border: 1px solid var(--line);
            padding: 11px 13px;
            border-radius: 11px;
            background: #FFFFFF;
        }

        [data-testid="stSidebar"] {
            background: #FAFAFA;
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 2.3rem;
        }

        /* Make radio navigation feel like app navigation */
        [data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 3px;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label {
            border-radius: 8px;
            padding: .48rem .6rem;
            transition: all .15s ease;
            border-left: 3px solid transparent;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: #F3F4F6;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            background: var(--riddell-red-soft);
            border-left-color: var(--riddell-red);
            color: var(--riddell-red);
            font-weight: 800;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
            display: none;
        }

        [data-testid="stSidebar"] hr {
            margin: 1rem 0;
        }

        .sidebar-kicker {
            color: #9CA3AF;
            font-size: .68rem;
            font-weight: 800;
            letter-spacing: .08em;
            text-transform: uppercase;
            margin: .65rem 0 .35rem 0;
        }

        .sidebar-brand {
            color: var(--riddell-red);
            font-size: .72rem;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: .075em;
            margin-top: .2rem;
        }

        .sidebar-note {
            color: var(--muted);
            font-size: .75rem;
            line-height: 1.35;
        }

        .brand-footer {
            border-top: 1px solid var(--line);
            margin-top: 2rem;
            padding-top: .75rem;
            color: #9CA3AF;
            font-size: .73rem;
            display: flex;
            justify-content: space-between;
        }

        @media (max-width: 1100px) {
            .exception-grid { grid-template-columns: 1fr; }
            .ai-grid { grid-template-columns: 1fr; }
            .focus-box { border-left: 0; border-top: 1px solid #EBC4CB; padding-left: 0; padding-top: 10px; }
            .app-title { white-space: normal; }
            .app-subtitle { white-space: normal; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------
@st.cache_data
def load_data():
    kpis = pd.read_csv(DATA_DIR / "kpis.csv")
    trends = pd.read_csv(DATA_DIR / "kpi_trends.csv")
    drivers = pd.read_csv(DATA_DIR / "otif_drivers.csv")
    impact = pd.read_csv(DATA_DIR / "otif_impact.csv")
    flow = pd.read_csv(DATA_DIR / "cross_process_story.csv")
    return kpis, trends, drivers, impact, flow


kpis, trends, drivers, impact, flow = load_data()


def status_tone(status: str) -> str:
    return {
        "On Track": "good",
        "Watch": "watch",
        "Action Required": "critical",
    }.get(status, "")


def status_dot(status: str) -> str:
    return {
        "On Track": "🟢",
        "Watch": "🟠",
        "Action Required": "🔴",
    }.get(status, "⚪")


def fmt_value(row) -> str:
    value = row["current"]
    unit = row["unit"]
    if unit == "%":
        return f"{value:.1f}%"
    if unit == "days":
        return f"{value:.1f} days"
    if unit == "$M":
        return f"${value:.1f}M"
    return f"{value:.1f}"


def app_header(persona: str, period: str):
    left, center, right = st.columns([1.05, 4.6, 2.25], vertical_alignment="center")
    with left:
        st.image(str(LOGO_PATH), width=128)
    with center:
        st.markdown(
            """
            <div class="appbar-center">
                <div class="app-title">Executive Performance Intelligence</div>
                <div class="app-subtitle">Enterprise pulse • exceptions • drivers • connected business context</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"""
            <div class="app-meta">
                <b>{persona}</b> &nbsp;•&nbsp; {period}<br>
                Last refreshed 7:03 AM &nbsp;•&nbsp; Demo data
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('<div class="brand-rule"></div>', unsafe_allow_html=True)


def footer():
    st.markdown(
        """
        <div class="brand-footer">
            <span>Riddell Executive Performance Intelligence • Prototype</span>
            <span>Illustrative data only</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------
with st.sidebar:
    st.image(str(LOGO_PATH), width=132)
    st.markdown('<div class="sidebar-brand">Executive Performance Intelligence</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-kicker">Navigate</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigate",
        [
            "Overview",
            "KPI Stories",
            "Business Connections",
            "Ask Riddell",
            "KPI Governance",
        ],
        label_visibility="collapsed",
        key="main_nav",
    )

    st.divider()
    st.markdown('<div class="sidebar-kicker">Executive View</div>', unsafe_allow_html=True)
    persona = st.selectbox(
        "Executive View",
        ["Enterprise", "CEO", "CFO", "COO", "Supply Chain"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-kicker">Reporting Period</div>', unsafe_allow_html=True)
    period = st.selectbox(
        "Reporting Period",
        ["August 2026", "Last 30 Days", "Q3 2026", "FY 2026 YTD"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown('<div class="sidebar-kicker">Data Status</div>', unsafe_allow_html=True)
    st.markdown("🟢 **Sample data loaded**")
    st.markdown(
        '<div class="sidebar-note">Replace with the customer-approved 45 KPI definitions and source mappings for the production POC.</div>',
        unsafe_allow_html=True,
    )

app_header(persona, period)


# ---------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------
if page == "Overview":
    st.markdown('<div class="section-kicker">Enterprise Pulse</div>', unsafe_allow_html=True)
    st.subheader("What deserves leadership attention?")
    st.markdown(
        '<div class="section-copy">A concise view of performance health, emerging risk, and the connected business story behind the numbers.</div>',
        unsafe_allow_html=True,
    )

    counts = kpis["status"].value_counts()
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="pulse-card">
                <div class="pulse-label">On Track</div>
                <div class="pulse-number good">{counts.get("On Track", 0)}</div>
                <div class="pulse-desc">KPIs performing within threshold</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="pulse-card">
                <div class="pulse-label">Watch</div>
                <div class="pulse-number watch">{counts.get("Watch", 0)}</div>
                <div class="pulse-desc">KPIs showing emerging risk</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="pulse-card">
                <div class="pulse-label">Action Required</div>
                <div class="pulse-number critical">{counts.get("Action Required", 0)}</div>
                <div class="pulse-desc">KPIs outside target threshold</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="ai-brief">
            <div class="ai-grid">
                <div>
                    <div class="section-kicker">AI Executive Brief</div>
                    <div class="ai-title">Fulfillment pressure appears to be connected to upstream supply and production constraints.</div>
                    <div class="ai-copy">
                        OTIF and production schedule adherence deteriorated together. Supplier delivery performance is the strongest
                        upstream risk signal in the current view, suggesting leadership should investigate the issue as a connected
                        procurement → manufacturing → fulfillment chain rather than as an isolated logistics problem.
                    </div>
                </div>
                <div class="focus-box">
                    <div class="focus-label">Recommended Focus</div>
                    <div class="focus-value">Supplier constraints → production exceptions → customer-order exposure</div>
                    <div class="focus-copy">Validate the four suppliers contributing most to component delays and quantify the open-order impact.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-kicker">Business Process Health</div>', unsafe_allow_html=True)
    st.subheader("Where is the issue occurring?")

    process_order = [
        ("Procure to Pay", "Procure to Pay"),
        ("Plan to Produce", "Plan to Produce"),
        ("Fulfillment", "Fulfillment"),
        ("Order to Cash", "Order to Cash"),
        ("Record to Report", "Record to Report"),
        ("Hire to Retire / IT", "People / IT"),
    ]

    process_summary = (
        kpis.groupby("process")
        .agg(
            score=("process_score", "mean"),
            action=("status", lambda x: (x == "Action Required").sum()),
            watch=("status", lambda x: (x == "Watch").sum()),
        )
        .reset_index()
        .set_index("process")
    )

    # Render each process card independently inside native Streamlit columns.
    # This avoids Markdown parsing multi-line HTML as a code block on hosted Streamlit.
    process_cols = st.columns(6, gap="small")
    for idx, (source_name, display_name) in enumerate(process_order):
        row = process_summary.loc[source_name]
        status = "Action Required" if row["action"] > 0 else ("Watch" if row["watch"] > 0 else "On Track")
        tone = status_tone(status)
        label = "Action" if status == "Action Required" else status

        card_html = (
            '<div class="process-node">'
            f'<div class="process-name">{display_name}</div>'
            f'<div class="process-score">{row["score"]:.0f}%</div>'
            f'<div class="process-status {tone}">{status_dot(status)} {label}</div>'
            '<div class="process-health">Process health</div>'
            '</div>'
        )

        with process_cols[idx]:
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">Executive Attention</div>', unsafe_allow_html=True)
    st.subheader("Top exceptions to investigate")

    st.markdown(
        """
        <div class="exception-grid">
            <div class="exception-card">
                <div class="exception-title"><span class="mini-dot critical"></span>Fulfillment below target</div>
                <div class="exception-copy">OTIF is 5.9 points below target; three product groups account for most of the decline.</div>
            </div>
            <div class="exception-card">
                <div class="exception-title"><span class="mini-dot critical"></span>Production schedule risk</div>
                <div class="exception-copy">Schedule adherence is down 4.2 points and overlaps with the same impacted product groups.</div>
            </div>
            <div class="exception-card">
                <div class="exception-title"><span class="mini-dot watch"></span>Supplier performance</div>
                <div class="exception-copy">Four suppliers represent a disproportionate share of component-delay signals.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.4, 1])
    with left:
        st.markdown("### Performance Trends")
        chosen = st.multiselect(
            "KPIs",
            ["On-Time-In-Full", "Production Schedule Adherence", "Supplier OTIF", "Gross Margin"],
            default=["On-Time-In-Full", "Production Schedule Adherence", "Supplier OTIF"],
            label_visibility="collapsed",
        )
        chart_data = trends[trends["kpi"].isin(chosen)]
        fig = px.line(chart_data, x="month", y="value", color="kpi", markers=True)
        fig.update_layout(
            height=330,
            margin=dict(l=8, r=8, t=8, b=8),
            legend_title_text="",
            yaxis_title="KPI value",
            xaxis_title="",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("### KPIs Requiring Attention")
        attention = kpis[kpis["status"] != "On Track"].copy()
        attention["Current"] = attention.apply(fmt_value, axis=1)
        attention["Status"] = attention["status"].map(lambda x: f"{status_dot(x)} {x}")
        st.dataframe(
            attention[["kpi", "Current", "Status"]],
            hide_index=True,
            use_container_width=True,
            height=330,
        )


# ---------------------------------------------------------------------
# KPI Stories
# ---------------------------------------------------------------------
elif page == "KPI Stories":
    st.markdown('<div class="section-kicker">KPI Story</div>', unsafe_allow_html=True)
    st.subheader("On-Time-In-Full: from metric to business explanation")
    st.markdown(
        '<div class="section-copy">An executive should be able to move from “what changed?” to “why?” and “where should we investigate?” without interpreting a wall of charts.</div>',
        unsafe_allow_html=True,
    )

    otif = kpis[kpis["kpi"] == "On-Time-In-Full"].iloc[0]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Current", f"{otif['current']:.1f}%", f"{otif['delta']:+.1f} pts")
    m2.metric("Target", f"{otif['target']:.1f}%")
    m3.metric("Benchmark", f"{otif['benchmark']:.1f}%")
    m4.metric("Status", f"{status_dot(otif['status'])} {otif['status']}")

    left, right = st.columns([1.35, 1])
    with left:
        st.markdown("### 12-Month Performance")
        otif_trend = trends[trends["kpi"] == "On-Time-In-Full"]
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=otif_trend["month"],
                y=otif_trend["value"],
                mode="lines+markers",
                name="OTIF",
            )
        )
        fig.add_hline(y=float(otif["target"]), line_dash="dash", annotation_text="Target")
        fig.update_layout(
            height=320,
            margin=dict(l=8, r=8, t=15, b=8),
            yaxis_title="OTIF %",
            xaxis_title="",
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("### AI KPI Story")
        st.markdown(
            """
            <div class="ai-brief" style="margin-top:0;">
                <div class="ai-title">OTIF declined 3.7 points versus the prior month.</div>
                <div class="ai-copy">
                    About 63% of the decline is concentrated in three product groups. Component availability and production
                    schedule adherence are the strongest contributing signals, suggesting an upstream constraint is flowing
                    through manufacturing and into customer fulfillment.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### What is driving the change?")
    fig = px.bar(
        drivers.sort_values("impact_points"),
        x="impact_points",
        y="driver",
        orientation="h",
        text="impact_points",
    )
    fig.update_layout(
        height=280,
        margin=dict(l=8, r=8, t=8, b=8),
        xaxis_title="Estimated contribution (points)",
        yaxis_title="",
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("### Where is the impact?")
        st.dataframe(impact, hide_index=True, use_container_width=True)
    with c2:
        st.markdown("### Recommended investigation")
        st.markdown(
            """
            1. Review component shortages in the top impacted product groups.
            2. Identify production orders with schedule exceptions.
            3. Compare delayed orders against supplier delivery performance.
            4. Quantify revenue exposure for open orders currently at risk.
            """
        )

    with st.expander("View KPI definition and lineage"):
        st.markdown(
            """
            **Definition:** Percentage of customer orders delivered complete and on/before the committed date.  
            **Formula:** OTIF orders ÷ total delivered orders  
            **Primary source:** SAP ECC  
            **Supporting source:** Transportation system  
            **Refresh:** Daily  
            **Business owner:** VP Supply Chain
            """
        )
        st.code("SAP ECC + Transportation System → Enterprise Data Platform / Fabric → KPI Semantic Model → Executive Experience")


# ---------------------------------------------------------------------
# Business Connections
# ---------------------------------------------------------------------
elif page == "Business Connections":
    st.markdown('<div class="section-kicker">Connected Business Context</div>', unsafe_allow_html=True)
    st.subheader("See the chain, not six disconnected dashboards")
    st.markdown(
        '<div class="section-copy">The value of the executive experience is its ability to connect procurement, production, fulfillment, customer, and financial signals.</div>',
        unsafe_allow_html=True,
    )

    for _, row in flow.iterrows():
        st.markdown(
            f"""
            <div class="story-card">
                <div class="story-kicker">{row['process']}</div>
                <div class="story-title">{row['signal']}</div>
                <div class="story-copy">{row['story']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Executive interpretation")
    st.markdown(
        """
        <div class="ai-brief">
            <div class="ai-title">The evidence suggests a procurement → manufacturing → fulfillment chain.</div>
            <div class="ai-copy">
                Supplier delivery deterioration appears upstream of production schedule misses. Those misses are concentrated
                in the same product groups where OTIF has fallen, creating potential revenue and margin exposure.
                The fulfillment issue therefore should not be managed only as a downstream logistics problem.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### POC KPI coverage")
    poc = kpis[kpis["poc"] == "Yes"].copy()
    poc["Current"] = poc.apply(fmt_value, axis=1)
    poc["Status"] = poc["status"].map(lambda x: f"{status_dot(x)} {x}")
    st.dataframe(
        poc[["process", "kpi", "Current", "Status", "owner"]],
        hide_index=True,
        use_container_width=True,
    )


# ---------------------------------------------------------------------
# Ask Riddell
# ---------------------------------------------------------------------
elif page == "Ask Riddell":
    st.markdown('<div class="section-kicker">Conversational Investigation</div>', unsafe_allow_html=True)
    st.subheader("Ask Riddell")
    st.markdown(
        '<div class="section-copy">Natural-language investigation should sit on top of governed KPI definitions and trusted enterprise evidence—not replace them.</div>',
        unsafe_allow_html=True,
    )

    suggestions = [
        "Why did fulfillment decline this month?",
        "Which suppliers are contributing most to the problem?",
        "Which KPIs deteriorated for three consecutive months?",
        "What should leadership focus on this week?",
    ]

    b1, b2 = st.columns(2)
    for i, q in enumerate(suggestions):
        with (b1 if i % 2 == 0 else b2):
            if st.button(q, use_container_width=True, key=f"suggest_{i}"):
                st.session_state["demo_question"] = q

    question = st.chat_input("Ask a business question")
    if not question:
        question = st.session_state.pop("demo_question", None)

    if question:
        with st.chat_message("user"):
            st.write(question)

        q = question.lower()
        if "supplier" in q:
            answer = (
                "Four suppliers are driving most of the component-delay signal in the mock data. "
                "The next investigation should connect their delivery exceptions to the production orders "
                "and product groups with schedule misses."
            )
        elif "fulfillment" in q or "otif" in q:
            answer = (
                "Fulfillment weakened primarily because OTIF fell 3.7 points. About 63% of the decline is "
                "concentrated in three product groups, with component availability and production schedule "
                "adherence as the strongest contributing signals."
            )
        elif "three consecutive" in q or "deteriorated" in q:
            answer = (
                "OTIF, supplier OTIF, and production schedule adherence show the clearest sustained deterioration "
                "in the sample data. More importantly, these three measures form a connected operational story."
            )
        elif "focus" in q or "week" in q:
            answer = (
                "Leadership should focus on supplier component delays, production schedule exceptions, and the resulting "
                "customer-order exposure. The goal is to resolve the upstream driver rather than treat fulfillment as an isolated issue."
            )
        else:
            answer = (
                "This prototype uses deterministic demo responses. A production implementation can ground an approved LLM "
                "against the KPI semantic model, SAP/Fabric data, lineage, and user permissions."
            )

        with st.chat_message("assistant"):
            st.write(answer)
            st.caption("Prototype response • grounded on simulated KPI context")

    st.info(
        "Production pattern: governed KPI model + enterprise data + security context + approved LLM. "
        "The LLM explains evidence; it should not become the source of KPI truth."
    )


# ---------------------------------------------------------------------
# KPI Governance
# ---------------------------------------------------------------------
elif page == "KPI Governance":
    st.markdown('<div class="section-kicker">Trust & Governance</div>', unsafe_allow_html=True)
    st.subheader("Every KPI should be explainable and traceable")
    st.markdown(
        '<div class="section-copy">Riddell has already invested in defining formulas and sources. The executive experience should preserve that governance and make it visible on demand.</div>',
        unsafe_allow_html=True,
    )

    kpi_name = st.selectbox("Select KPI", kpis["kpi"].tolist(), index=0)
    row = kpis[kpis["kpi"] == kpi_name].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current", fmt_value(row))
    c2.metric("Target", f"{row['target']:.1f}{'%' if row['unit'] == '%' else ''}")
    c3.metric("Benchmark", f"{row['benchmark']:.1f}{'%' if row['unit'] == '%' else ''}")
    c4.metric("Data quality", f"{row['data_quality']:.1f}%")

    st.markdown(
        f"""
        <div class="trust-card">
            <div class="section-kicker">{row['process']}</div>
            <h3 style="margin:.2rem 0 .6rem 0;">{row['kpi']}</h3>
            <p style="color:#4B5563;">{row['definition']}</p>
            <hr style="border:none;border-top:1px solid #E5E7EB;margin:1rem 0;">
            <b>Business owner</b> &nbsp; {row['owner']}<br>
            <b>Formula</b> &nbsp; {row['formula']}<br>
            <b>Primary source</b> &nbsp; {row['source']}<br>
            <b>Refresh</b> &nbsp; {row['refresh']}<br>
            <b>Status</b> &nbsp; {status_dot(row['status'])} {row['status']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Example lineage")
    st.code(
        f"{row['source']} → Enterprise Data Platform / Fabric → KPI Semantic Model → Executive Experience → AI Narrative"
    )

footer()
