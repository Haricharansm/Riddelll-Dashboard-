
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
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

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
        :root {
            --riddell-red:#C8102E;
            --riddell-dark:#171717;
            --riddell-gray:#6B7280;
            --riddell-light:#F7F7F8;
            --riddell-border:#E5E7EB;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }
        h1, h2, h3 {
            letter-spacing: -0.02em;
            color: var(--riddell-dark);
        }
        .riddell-header {
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding: 0.25rem 0 0.9rem 0;
            border-bottom: 4px solid var(--riddell-red);
            margin-bottom: 1rem;
        }
        .riddell-title {
            font-size: 1.55rem;
            font-weight: 800;
            color: var(--riddell-dark);
        }
        .riddell-subtitle {
            opacity: .7;
            font-size: .93rem;
        }
        .pulse-card {
            border: 1px solid rgba(128,128,128,.18);
            border-radius: 12px;
            padding: 18px 20px;
            background: #FFFFFF;
            min-height: 132px;
        }
        .pulse-number {
            font-size: 2.15rem;
            font-weight: 800;
            line-height: 1;
            margin-bottom: .4rem;
        }
        .small-label {
            font-size: .82rem;
            opacity: .68;
            text-transform: uppercase;
            letter-spacing: .06em;
        }
        .process-card {
            border: 1px solid rgba(128,128,128,.18);
            border-radius: 12px;
            padding: 14px;
            min-height: 130px;
            background: rgba(128,128,128,.025);
        }
        .status-green { color:#16a34a; font-weight:700; }
        .status-amber { color:#d97706; font-weight:700; }
        .status-red { color:#dc2626; font-weight:700; }
        .brief-card {
            border: 1px solid rgba(128,128,128,.18);
            border-left: 5px solid var(--riddell-red);
            border-radius: 12px;
            padding: 20px;
            background: #FFFFFF;
        }
        .story-step {
            border-left: 4px solid var(--riddell-red);
            padding: 8px 12px;
            margin: 8px 0;
        }
        [data-testid="stMetric"] {
            border: 1px solid rgba(128,128,128,.18);
            padding: 12px 14px;
            border-radius: 12px;
            background: rgba(128,128,128,.025);
        }
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128,128,128,.14);
            background: #FAFAFA;
        }
        .brand-kicker {
            font-size:.78rem;
            letter-spacing:.08em;
            font-weight:800;
            color:var(--riddell-red);
            text-transform:uppercase;
        }
        .brand-footer {
            border-top:1px solid var(--riddell-border);
            margin-top:2.2rem;
            padding-top:.8rem;
            color:#9CA3AF;
            font-size:.78rem;
            display:flex;
            justify-content:space-between;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Data
# -----------------------------
@st.cache_data
def load_data():
    kpis = pd.read_csv(DATA_DIR / "kpis.csv")
    trends = pd.read_csv(DATA_DIR / "kpi_trends.csv")
    drivers = pd.read_csv(DATA_DIR / "otif_drivers.csv")
    impact = pd.read_csv(DATA_DIR / "otif_impact.csv")
    flow = pd.read_csv(DATA_DIR / "cross_process_story.csv")
    return kpis, trends, drivers, impact, flow

kpis, trends, drivers, impact, flow = load_data()

def status_class(status):
    return {
        "On Track": "status-green",
        "Watch": "status-amber",
        "Action Required": "status-red"
    }.get(status, "")

def status_dot(status):
    return {
        "On Track": "🟢",
        "Watch": "🟠",
        "Action Required": "🔴"
    }.get(status, "⚪")

def fmt_value(row):
    unit = row["unit"]
    value = row["current"]
    if unit == "%":
        return f"{value:.1f}%"
    if unit == "days":
        return f"{value:.1f} days"
    if unit == "$M":
        return f"${value:.1f}M"
    return f"{value:.1f}"

def header():
    c1, c2, c3 = st.columns([1.1, 3.8, 2.0])
    with c1:
        st.image(str(LOGO_PATH), width=175)
    with c2:
        st.markdown(
            """<div style="padding-top:.35rem;">
            <div class="riddell-title">Executive Performance Intelligence</div>
            <div class="riddell-subtitle">Enterprise performance • exceptions • drivers • business context</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """<div style="text-align:right;padding-top:.35rem;">
            <span class="brand-kicker">Executive View</span><br>
            <span class="riddell-subtitle">August 2026 • Sample Data</span>
            </div>""",
            unsafe_allow_html=True,
        )
    st.markdown('<div style="height:4px;background:#C8102E;border-radius:999px;margin:.15rem 0 1rem 0;"></div>', unsafe_allow_html=True)

# -----------------------------
# Sidebar Navigation
# -----------------------------
with st.sidebar:
    st.image(str(LOGO_PATH), use_container_width=True)
    st.markdown('<div class="brand-kicker">Executive Performance Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:2px;background:#C8102E;margin:.7rem 0 1rem 0;"></div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigate",
        [
            "1. Executive Cockpit",
            "2. KPI Story",
            "3. Cross-Process Story",
            "4. Ask Riddell",
            "5. KPI Trust Card",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("DEMO FLOW")
    st.markdown(
        """
        **Flow**
        1. See enterprise pulse  
        2. Find exceptions  
        3. Understand drivers  
        4. Connect cross-process impact  
        5. Investigate with natural language
        """
    )
    st.divider()
    st.caption("DATA STATUS")
    st.markdown("🟢 **Sample data loaded**")
    st.caption("Replace with validated Riddell KPI data before customer use.")

header()

# -----------------------------
# PAGE 1 — EXECUTIVE COCKPIT
# -----------------------------
if page == "1. Executive Cockpit":
    st.subheader("Executive Pulse")
    st.caption("A single leadership view of what is on track, what is drifting, and what needs action.")

    counts = kpis["status"].value_counts()
    c1, c2, c3, c4 = st.columns([1,1,1,1.2])
    with c1:
        st.markdown(
            f"""<div class="pulse-card">
            <div class="small-label">On track</div>
            <div class="pulse-number status-green">{counts.get('On Track',0)}</div>
            <div>KPIs performing within threshold</div>
            </div>""", unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""<div class="pulse-card">
            <div class="small-label">Watch</div>
            <div class="pulse-number status-amber">{counts.get('Watch',0)}</div>
            <div>KPIs trending toward risk</div>
            </div>""", unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""<div class="pulse-card">
            <div class="small-label">Action required</div>
            <div class="pulse-number status-red">{counts.get('Action Required',0)}</div>
            <div>KPIs outside target threshold</div>
            </div>""", unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            """<div class="pulse-card">
            <div class="small-label">Executive focus</div>
            <div style="font-size:1.15rem;font-weight:750;margin:.2rem 0 .4rem 0;">Fulfillment & Production</div>
            <div>Service performance has weakened while supplier and production constraints are increasing.</div>
            </div>""", unsafe_allow_html=True
        )

    st.markdown("### Performance by Business Process")
    process_summary = (
        kpis.groupby("process")
        .agg(score=("process_score", "mean"),
             action=("status", lambda x: (x == "Action Required").sum()),
             watch=("status", lambda x: (x == "Watch").sum()))
        .reset_index()
    )

    cols = st.columns(6)
    for i, row in process_summary.iterrows():
        status = "Action Required" if row["action"] > 0 else ("Watch" if row["watch"] > 0 else "On Track")
        with cols[i]:
            st.markdown(
                f"""<div class="process-card">
                <div class="small-label">{row['process']}</div>
                <div style="font-size:1.75rem;font-weight:800;margin:.25rem 0;">{row['score']:.0f}%</div>
                <div class="{status_class(status)}">{status_dot(status)} {status}</div>
                <div style="opacity:.65;font-size:.84rem;margin-top:.5rem;">Composite POC score</div>
                </div>""",
                unsafe_allow_html=True,
            )

    left, right = st.columns([1.35, 1])
    with left:
        st.markdown("### KPIs Requiring Attention")
        attention = kpis[kpis["status"] != "On Track"].copy()
        attention["Current"] = attention.apply(fmt_value, axis=1)
        attention["Trend"] = attention["delta"].apply(lambda x: f"{x:+.1f}")
        attention["Status"] = attention["status"].map(lambda x: f"{status_dot(x)} {x}")
        st.dataframe(
            attention[["kpi", "process", "Current", "Trend", "Status"]],
            hide_index=True,
            use_container_width=True,
            height=260,
        )

    with right:
        st.markdown("### AI Executive Brief")
        st.markdown(
            """
            <div class="brief-card">
            <b>Three issues deserve leadership attention.</b><br><br>
            Fulfillment performance has declined, led by lower OTIF. The strongest contributing signals are component availability and production schedule adherence.<br><br>
            Supplier performance is emerging as an upstream risk, with four suppliers contributing disproportionately to material delays.<br><br>
            <b>Suggested focus:</b> validate supplier constraints, review production exceptions, and assess revenue exposure from delayed orders.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### KPI Trends")
    chosen = st.multiselect(
        "Select KPIs",
        ["On-Time-In-Full", "Production Schedule Adherence", "Supplier OTIF", "Gross Margin"],
        default=["On-Time-In-Full", "Production Schedule Adherence", "Supplier OTIF"],
    )
    chart_data = trends[trends["kpi"].isin(chosen)]
    fig = px.line(chart_data, x="month", y="value", color="kpi", markers=True)
    fig.update_layout(
        height=360,
        margin=dict(l=10, r=10, t=10, b=10),
        legend_title_text="",
        yaxis_title="KPI Value",
        xaxis_title="",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Top Business Exceptions")
    exceptions = [
        ("🔴", "Fulfillment below target", "OTIF is 5.9 points below target; three product groups account for most of the decline."),
        ("🟠", "Production schedule risk", "Schedule adherence is down 4.2 points and overlaps with the same product groups."),
        ("🟠", "Supplier performance", "Four suppliers represent a disproportionate share of delayed components."),
    ]
    for icon, title, desc in exceptions:
        with st.container(border=True):
            st.markdown(f"**{icon} {title}**")
            st.caption(desc)

# -----------------------------
# PAGE 2 — KPI STORY
# -----------------------------
elif page == "2. KPI Story":
    st.subheader("KPI Story — On-Time-In-Full")
    st.caption("Turn a KPI into an executive business story: what changed, why, where, and what to investigate next.")

    otif = kpis[kpis["kpi"] == "On-Time-In-Full"].iloc[0]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Current", f"{otif['current']:.1f}%", f"{otif['delta']:+.1f} pts")
    m2.metric("Target", f"{otif['target']:.1f}%")
    m3.metric("Industry benchmark", f"{otif['benchmark']:.1f}%")
    m4.metric("Status", f"{status_dot(otif['status'])} {otif['status']}")

    left, right = st.columns([1.3, 1])
    with left:
        st.markdown("### 12-Month Performance")
        otif_trend = trends[trends["kpi"] == "On-Time-In-Full"]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=otif_trend["month"],
            y=otif_trend["value"],
            mode="lines+markers",
            name="OTIF"
        ))
        fig.add_hline(y=float(otif["target"]), line_dash="dash", annotation_text="Target")
        fig.update_layout(
            height=340,
            margin=dict(l=10, r=10, t=20, b=10),
            yaxis_title="OTIF %",
            xaxis_title="",
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("### AI KPI Story")
        st.markdown(
            """
            <div class="brief-card">
            <b>OTIF declined 3.7 points versus the prior month.</b><br><br>
            Approximately <b>63% of the decline</b> is concentrated in three product groups. The leading business signals are lower component availability and production schedule adherence.<br><br>
            The overlap suggests an upstream supply constraint is flowing through manufacturing and into customer fulfillment.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### What Is Driving the Change?")
    fig = px.bar(
        drivers.sort_values("impact_points"),
        x="impact_points",
        y="driver",
        orientation="h",
        text="impact_points",
    )
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Estimated contribution (points)",
        yaxis_title="",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Where Is the Impact?")
    st.dataframe(
        impact,
        hide_index=True,
        use_container_width=True,
    )

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("### Recommended Investigation")
        st.markdown(
            """
            1. Review component shortages for the top three impacted product categories.
            2. Identify production orders with schedule exceptions in the same period.
            3. Compare delayed orders against supplier delivery performance.
            4. Quantify revenue exposure for open orders currently at risk.
            """
        )
    with c2:
        st.markdown("### KPI Definition")
        with st.container(border=True):
            st.markdown("**On-Time-In-Full (OTIF)**")
            st.caption("Percentage of customer orders delivered complete and on/before the committed date.")
            st.markdown(
                """
                **Formula:** OTIF orders ÷ total delivered orders  
                **Primary source:** SAP ECC  
                **Supporting source:** Transportation system  
                **Refresh:** Daily  
                **Business owner:** VP Supply Chain
                """
            )

# -----------------------------
# PAGE 3 — CROSS-PROCESS STORY
# -----------------------------
elif page == "3. Cross-Process Story":
    st.subheader("Cross-Process Business Story")
    st.caption("Connect the six process areas into one executive narrative rather than six disconnected dashboards.")

    st.markdown("### How the business issue propagates")
    for _, row in flow.iterrows():
        st.markdown(
            f"""
            <div class="story-step">
                <div class="small-label">{row['process']}</div>
                <div style="font-size:1.15rem;font-weight:750;">{row['signal']}</div>
                <div style="opacity:.75;">{row['story']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Executive interpretation")
    st.markdown(
        """
        <div class="brief-card">
        Supplier delivery deterioration appears upstream of production schedule misses. Those misses are concentrated in the same product groups where OTIF has fallen, creating potential revenue and margin exposure.<br><br>
        <b>Executive implication:</b> the fulfillment issue should not be managed only as a logistics problem. The evidence suggests a connected procurement → manufacturing → fulfillment chain.
        </div>
        """,
        unsafe_allow_html=True
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

# -----------------------------
# PAGE 4 — ASK RIDDELL
# -----------------------------
elif page == "4. Ask Riddell":
    st.subheader("Ask Riddell")
    st.caption("Natural-language investigation layered on top of governed KPIs and trusted enterprise data.")

    sample_questions = [
        "Why did fulfillment decline this month?",
        "Which suppliers are contributing most to the problem?",
        "Which KPIs deteriorated for three consecutive months?",
        "What should leadership focus on this week?",
    ]

    cols = st.columns(2)
    for idx, q in enumerate(sample_questions):
        with cols[idx % 2]:
            if st.button(q, use_container_width=True):
                st.session_state["prefill_question"] = q

    default_q = st.session_state.get("prefill_question", "")
    question = st.chat_input("Ask a business question about Riddell performance")
    if not question and default_q:
        question = default_q
        st.session_state["prefill_question"] = ""

    if question:
        with st.chat_message("user"):
            st.write(question)

        q = question.lower()
        if "supplier" in q:
            answer = (
                "Four suppliers are driving most of the component-delay signal in the mock data. "
                "The recommended next step is to compare their delivery performance with the production orders "
                "and product categories showing schedule misses."
            )
        elif "fulfillment" in q or "otif" in q:
            answer = (
                "Fulfillment weakened primarily because OTIF fell 3.7 points. In this prototype, about 63% of the "
                "decline is concentrated in three product groups, with component availability and production "
                "schedule adherence as the largest contributing signals."
            )
        elif "three consecutive" in q or "deteriorated" in q:
            answer = (
                "The strongest sustained deterioration in the sample data is visible in OTIF, supplier OTIF, and "
                "production schedule adherence. These three KPIs also form a plausible connected business story."
            )
        elif "focus" in q or "week" in q:
            answer = (
                "Leadership should focus on three linked areas: supplier component delays, production schedule "
                "exceptions, and the resulting customer-order exposure. The goal is to resolve the upstream cause "
                "rather than manage fulfillment as an isolated downstream issue."
            )
        else:
            answer = (
                "This mockup uses deterministic demo responses. In production, this panel can be connected to "
                "Azure OpenAI and grounded against the KPI semantic model, SAP/Fabric data, and governed business definitions."
            )

        with st.chat_message("assistant"):
            st.write(answer)
            st.caption("Demo response generated from simulated KPI context.")

    st.info(
        "Production path: replace the deterministic response logic with an Azure OpenAI or other approved LLM call, "
        "grounded on trusted KPI definitions, data lineage, and enterprise security."
    )

# -----------------------------
# PAGE 5 — KPI TRUST CARD
# -----------------------------
elif page == "5. KPI Trust Card":
    st.subheader("KPI Trust Card")
    st.caption("Show leadership exactly what a KPI means, where it came from, and whether the data can be trusted.")

    kpi_name = st.selectbox("Select KPI", kpis["kpi"].tolist(), index=0)
    row = kpis[kpis["kpi"] == kpi_name].iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Current", fmt_value(row))
    c2.metric("Target", f"{row['target']:.1f}{row['unit'] if row['unit'] in ['%'] else ''}")
    c3.metric("Data quality", f"{row['data_quality']:.1f}%")

    with st.container(border=True):
        st.markdown(f"## {row['kpi']}")
        st.write(row["definition"])
        st.markdown(
            f"""
            **Business process:** {row['process']}  
            **Business owner:** {row['owner']}  
            **Formula:** {row['formula']}  
            **Primary source:** {row['source']}  
            **Refresh:** {row['refresh']}  
            **Industry benchmark:** {row['benchmark']:.1f}{row['unit'] if row['unit'] == '%' else ''}  
            **Status:** {status_dot(row['status'])} {row['status']}
            """
        )

    st.markdown("### Example lineage")
    st.code(f"{row['source']} → Enterprise Data Platform / Fabric → KPI Semantic Model → Executive Cockpit → AI Narrative")


# Branded footer
st.markdown(
    """<div class="brand-footer"><span>Riddell Executive Performance Intelligence • Prototype</span><span>Illustrative data only</span></div>""",
    unsafe_allow_html=True,
)
