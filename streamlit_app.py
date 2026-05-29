"""
Delivery Performance, Delay Risk & Logistics Efficiency Analysis
APL Logistics (KWE Group) — Streamlit Dashboard
Unified Mentor Internship Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="APL Logistics Analytics",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# THEME & CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
.stApp { background-color: #080c14; }
.block-container { padding: 1.5rem 2rem; max-width: 100%; }

section[data-testid="stSidebar"] {
    background: #0c1220;
    border-right: 1px solid #162035;
}

.hero {
    background: linear-gradient(135deg, #0c1a2e 0%, #0f2347 40%, #091a35 100%);
    border: 1px solid #1a3050;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(249,115,22,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    color: #f97316;
    background: rgba(249,115,22,0.1);
    border: 1px solid rgba(249,115,22,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    display: inline-block;
    margin-bottom: 0.8rem;
}
.hero-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #475569;
    margin: 0;
}

/* KPI cards */
.kpi-wrap {
    background: linear-gradient(145deg, #0f1a2e, #132240);
    border: 1px solid #1a3050;
    border-radius: 14px;
    padding: 1.2rem 1.3rem;
    position: relative;
    overflow: hidden;
}
.kpi-wrap.danger::before { background: linear-gradient(#ef4444, #dc2626); }
.kpi-wrap.warn::before { background: linear-gradient(#f97316, #ea580c); }
.kpi-wrap.good::before { background: linear-gradient(#22c55e, #16a34a); }
.kpi-wrap.info::before { background: linear-gradient(#3b82f6, #2563eb); }
.kpi-wrap::before {
    content: ''; position: absolute;
    top: 0; left: 0; width: 4px; height: 100%;
    background: linear-gradient(#3b82f6, #2563eb);
    border-radius: 14px 0 0 14px;
}
.kpi-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #475569;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.kpi-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.9rem;
    font-weight: 600;
    color: #f1f5f9;
    line-height: 1;
}
.kpi-note { font-size: 0.74rem; color: #64748b; margin-top: 0.3rem; }
.kpi-badge-red { color: #f87171; }
.kpi-badge-green { color: #4ade80; }
.kpi-badge-amber { color: #fbbf24; }

.section-hdr {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #475569;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-bottom: 1px solid #162035;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

.alert-critical {
    background: #1a0808;
    border-left: 4px solid #ef4444;
    border: 1px solid #7f1d1d;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: #fca5a5;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    margin: 0.3rem 0;
}
.alert-warn {
    background: #1a1000;
    border: 1px solid #78350f;
    border-left: 4px solid #f97316;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: #fdba74;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    margin: 0.3rem 0;
}
.alert-ok {
    background: #081a10;
    border: 1px solid #14532d;
    border-left: 4px solid #22c55e;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: #86efac;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    margin: 0.3rem 0;
}

.stTabs [data-baseweb="tab-list"] {
    background: #0c1220;
    border-radius: 10px;
    padding: 4px;
    gap: 3px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #475569;
    letter-spacing: 0.04em;
}
.stTabs [aria-selected="true"] {
    background: #1a3050 !important;
    color: #fb923c !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# COLORS & CHART THEME
# ─────────────────────────────────────────
C = {
    "orange": "#f97316", "blue": "#3b82f6", "green": "#22c55e",
    "red": "#ef4444", "amber": "#f59e0b", "purple": "#a855f7",
    "cyan": "#06b6d4", "slate": "#475569", "teal": "#14b8a6"
}
THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono", color="#64748b", size=11),
    xaxis=dict(gridcolor="#162035", linecolor="#162035", tickfont=dict(size=10)),
    yaxis=dict(gridcolor="#162035", linecolor="#162035", tickfont=dict(size=10)),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    margin=dict(t=35, b=40, l=5, r=10),
)

# ─────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("compressed_data.csv.gz",compression="gzip", encoding="latin1")
    df["Delay_Gap"] = df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]
    df["Delivery_Class"] = df["Delay_Gap"].apply(
        lambda x: "Early" if x < 0 else ("On-Time" if x == 0 else "Delayed")
    )
    df["On_Time_Flag"] = (df["Late_delivery_risk"] == 0).astype(int)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Place `compressed_data.csv.gz` in the same folder as this script.")
    st.stop()

# ─────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:JetBrains Mono;font-size:0.7rem;color:#f97316;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:1rem;">FILTERS</div>', unsafe_allow_html=True)

    all_modes = sorted(df["Shipping Mode"].unique())
    sel_modes = st.multiselect("Shipping Mode", all_modes, default=all_modes)

    all_markets = sorted(df["Market"].unique())
    sel_markets = st.multiselect("Market", all_markets, default=all_markets)

    all_regions = sorted(df["Order Region"].unique())
    sel_regions = st.multiselect("Order Region", all_regions, default=all_regions)

    all_segs = sorted(df["Customer Segment"].unique())
    sel_segs = st.multiselect("Customer Segment", all_segs, default=all_segs)

    st.markdown("---")
    st.markdown("### Alert Thresholds")
    late_risk_threshold = st.slider("Late Risk Alert (%)", 0, 100, 55, 1)
    delay_gap_threshold = st.slider("Avg Delay Alert (days)", 0.0, 4.0, 1.0, 0.1)

    st.markdown("---")
    st.caption("📦 APL Logistics Dataset\n180,519 orders · 40 fields")

# Apply filters
mask = (
    df["Shipping Mode"].isin(sel_modes) &
    df["Market"].isin(sel_markets) &
    df["Order Region"].isin(sel_regions) &
    df["Customer Segment"].isin(sel_segs)
)
dff = df[mask].copy()
total = len(dff)

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">APL LOGISTICS (KWE GROUP) —</div>
    <h1 class="hero-title">Delivery Performance & Delay Risk Analytics</h1>
    <p class="hero-sub">Global Supply Chain Operations · Shipping Mode Efficiency · Regional Delay Diagnostics</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# ALERT PANEL
# ─────────────────────────────────────────
late_pct = dff["Late_delivery_risk"].mean() * 100
avg_delay = dff["Delay_Gap"].mean()
first_class_late = dff[dff["Shipping Mode"] == "First Class"]["Late_delivery_risk"].mean() * 100 if "First Class" in sel_modes else 0

col_al1, col_al2, col_al3 = st.columns(3)
with col_al1:
    cls = "alert-critical" if late_pct >= late_risk_threshold else "alert-ok"
    icon = "🔴" if late_pct >= late_risk_threshold else "✅"
    st.markdown(f'<div class="{cls}">{icon} Late Delivery Risk: <b>{late_pct:.1f}%</b> — Threshold: {late_risk_threshold}%</div>', unsafe_allow_html=True)
with col_al2:
    cls2 = "alert-warn" if avg_delay >= delay_gap_threshold else "alert-ok"
    icon2 = "⚠️" if avg_delay >= delay_gap_threshold else "✅"
    st.markdown(f'<div class="{cls2}">{icon2} Avg Delay Gap: <b>{avg_delay:+.2f} days</b> — Threshold: {delay_gap_threshold:.1f}d</div>', unsafe_allow_html=True)
with col_al3:
    cls3 = "alert-critical" if first_class_late > 90 else "alert-warn"
    st.markdown(f'<div class="{cls3}">⚡ First Class Late Risk: <b>{first_class_late:.1f}%</b> — Schedule accuracy critical</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────
st.markdown('<div class="section-hdr">Key Performance Indicators</div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""<div class="kpi-wrap danger">
        <div class="kpi-label">Total Orders</div>
        <div class="kpi-val">{total:,}</div>
        <div class="kpi-note">Filtered selection</div>
    </div>""", unsafe_allow_html=True)
with k2:
    otd = dff["On_Time_Flag"].mean() * 100
    c = "good" if otd >= 50 else "danger"
    st.markdown(f"""<div class="kpi-wrap {c}">
        <div class="kpi-label">On-Time Rate</div>
        <div class="kpi-val">{otd:.1f}%</div>
        <div class="kpi-note"><span class="{'kpi-badge-green' if otd>=50 else 'kpi-badge-red'}">{'▲ Above' if otd>=50 else '▼ Below'} 50% baseline</span></div>
    </div>""", unsafe_allow_html=True)
with k3:
    lr = late_pct
    c = "danger" if lr >= 55 else "warn"
    st.markdown(f"""<div class="kpi-wrap {c}">
        <div class="kpi-label">Late Risk Ratio</div>
        <div class="kpi-val">{lr:.1f}%</div>
        <div class="kpi-note"><span class="kpi-badge-red">{dff['Late_delivery_risk'].sum():,} at-risk orders</span></div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="kpi-wrap warn">
        <div class="kpi-label">Avg Delay Gap</div>
        <div class="kpi-val">{avg_delay:+.2f}d</div>
        <div class="kpi-note">Actual minus scheduled days</div>
    </div>""", unsafe_allow_html=True)
with k5:
    canc = len(dff[dff["Order Status"] == "CANCELED"])
    st.markdown(f"""<div class="kpi-wrap info">
        <div class="kpi-label">Cancelled Orders</div>
        <div class="kpi-val">{canc:,}</div>
        <div class="kpi-note">{canc/max(total,1)*100:.1f}% of total</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Delivery Overview",
    "⚡ Delay Risk Analysis",
    "🚚 Shipping Mode Comparison",
    "🌍 Regional & Market",
    "📋 Executive Summary"
])

# ══════════════════════════════════════════
# TAB 1 — DELIVERY OVERVIEW
# ══════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-hdr">Delivery Performance Overview</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        # Delivery status donut
        status_counts = dff["Delivery Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_ds = px.pie(
            status_counts, values="Count", names="Status",
            hole=0.55,
            color_discrete_sequence=[C["red"], C["green"], C["blue"], C["slate"]],
            title="Delivery Status Distribution"
        )
        fig_ds.update_traces(textposition="outside", textinfo="percent+label")
        fig_ds.update_layout(height=360, showlegend=False, **THEME)
        st.plotly_chart(fig_ds, use_container_width=True)

    with c2:
        # Delivery class bar
        dc = dff["Delivery_Class"].value_counts().reset_index()
        dc.columns = ["Class", "Count"]
        color_map = {"Early": C["cyan"], "On-Time": C["green"], "Delayed": C["red"]}
        fig_dc = px.bar(
            dc, x="Class", y="Count",
            color="Class", color_discrete_map=color_map,
            title="Orders by Delivery Classification (Gap-Based)"
        )
        fig_dc.update_layout(showlegend=False, height=360, **THEME)
        st.plotly_chart(fig_dc, use_container_width=True)

    # Delay gap histogram
    fig_hist = px.histogram(
        dff, x="Delay_Gap", nbins=7,
        color_discrete_sequence=[C["orange"]],
        title="Delay Gap Distribution (Days) — Actual minus Scheduled",
        labels={"Delay_Gap": "Delay Gap (Days)"}
    )
    fig_hist.update_layout(height=300, **THEME)
    fig_hist.add_vline(x=0, line_dash="dash", line_color=C["green"],
                       annotation_text="On-Time", annotation_font_color=C["green"])
    fig_hist.add_vline(x=avg_delay, line_dash="dot", line_color=C["amber"],
                       annotation_text=f"Mean {avg_delay:+.2f}d", annotation_font_color=C["amber"])
    st.plotly_chart(fig_hist, use_container_width=True)

    # Order status bar
    os_counts = dff["Order Status"].value_counts().reset_index()
    os_counts.columns = ["Status", "Count"]
    fig_os = px.bar(
        os_counts, x="Status", y="Count",
        color_discrete_sequence=[C["blue"]],
        title="Order Status Breakdown"
    )
    fig_os.update_layout(height=300, **THEME)
    st.plotly_chart(fig_os, use_container_width=True)

# ══════════════════════════════════════════
# TAB 2 — DELAY RISK ANALYSIS
# ══════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-hdr">Delay Risk Analysis Dashboard</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        # Late risk gauge-style bar
        lr_by_mode = dff.groupby("Shipping Mode").agg(
            Late_Pct=("Late_delivery_risk", lambda x: x.mean() * 100),
            Avg_Delay=("Delay_Gap", "mean"),
            Orders=("Late_delivery_risk", "count")
        ).reset_index().sort_values("Late_Pct", ascending=True)

        fig_lr = px.bar(
            lr_by_mode, y="Shipping Mode", x="Late_Pct",
            orientation="h",
            color="Late_Pct",
            color_continuous_scale=[[0, C["green"]], [0.5, C["amber"]], [1, C["red"]]],
            title="Late Delivery Risk % by Shipping Mode",
            text=lr_by_mode["Late_Pct"].apply(lambda x: f"{x:.1f}%")
        )
        fig_lr.add_vline(x=50, line_dash="dash", line_color=C["slate"],
                         annotation_text="50% threshold")
        fig_lr.update_traces(textposition="outside")
        fig_lr.update_layout(height=340, coloraxis_showscale=False, **THEME)
        st.plotly_chart(fig_lr, use_container_width=True)

    with c2:
        # Delay gap boxplot by shipping mode
        fig_box = px.box(
            dff, x="Shipping Mode", y="Delay_Gap",
            color="Shipping Mode",
            color_discrete_sequence=[C["orange"], C["blue"], C["green"], C["purple"]],
            title="Delay Gap Distribution by Shipping Mode"
        )
        fig_box.add_hline(y=0, line_dash="dash", line_color=C["slate"],
                          annotation_text="On-Time")
        fig_box.update_layout(showlegend=False, height=340, **THEME)
        st.plotly_chart(fig_box, use_container_width=True)

    # Late risk by customer segment and payment type
    c3, c4 = st.columns(2)
    with c3:
        seg_lr = dff.groupby("Customer Segment")["Late_delivery_risk"].mean().reset_index()
        seg_lr["Late_Pct"] = (seg_lr["Late_delivery_risk"] * 100).round(2)
        fig_seg = px.bar(
            seg_lr, x="Customer Segment", y="Late_Pct",
            color="Customer Segment",
            color_discrete_sequence=[C["blue"], C["orange"], C["teal"]],
            title="Late Risk % by Customer Segment",
            text=seg_lr["Late_Pct"].apply(lambda x: f"{x:.1f}%")
        )
        fig_seg.add_hline(y=50, line_dash="dot", line_color=C["red"])
        fig_seg.update_traces(textposition="outside")
        fig_seg.update_layout(showlegend=False, height=320, **THEME)
        st.plotly_chart(fig_seg, use_container_width=True)

    with c4:
        pay_lr = dff.groupby("Type")["Late_delivery_risk"].mean().reset_index()
        pay_lr["Late_Pct"] = (pay_lr["Late_delivery_risk"] * 100).round(2)
        fig_pay = px.bar(
            pay_lr, x="Type", y="Late_Pct",
            color="Type",
            color_discrete_sequence=[C["purple"], C["cyan"], C["amber"]],
            title="Late Risk % by Payment Type",
            text=pay_lr["Late_Pct"].apply(lambda x: f"{x:.1f}%")
        )
        fig_pay.update_traces(textposition="outside")
        fig_pay.update_layout(showlegend=False, height=320, **THEME)
        st.plotly_chart(fig_pay, use_container_width=True)

    # Delay gap heatmap: shipping mode x delivery class
    heatmap_data = dff.groupby(["Shipping Mode", "Delivery_Class"]).size().unstack(fill_value=0)
    fig_hm = px.imshow(
        heatmap_data,
        color_continuous_scale=[[0, "#0c1220"], [0.5, "#1a3050"], [1, "#f97316"]],
        title="Order Volume: Shipping Mode × Delivery Classification",
        text_auto=True
    )
    fig_hm.update_layout(height=300, **THEME)
    st.plotly_chart(fig_hm, use_container_width=True)

# ══════════════════════════════════════════
# TAB 3 — SHIPPING MODE COMPARISON
# ══════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-hdr">Shipping Mode Efficiency Comparison</div>', unsafe_allow_html=True)

    mode_stats = dff.groupby("Shipping Mode").agg(
        Orders=("Late_delivery_risk", "count"),
        Late_Risk=("Late_delivery_risk", "sum"),
        Late_Pct=("Late_delivery_risk", lambda x: round(x.mean() * 100, 1)),
        Avg_Delay=("Delay_Gap", "mean"),
        Avg_Real_Days=("Days for shipping (real)", "mean"),
        Avg_Sched_Days=("Days for shipment (scheduled)", "mean"),
        Avg_Profit=("Benefit per order", "mean"),
    ).reset_index().round(2)

    c1, c2 = st.columns(2)
    with c1:
        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Bar(
            x=mode_stats["Shipping Mode"], y=mode_stats["Avg_Real_Days"],
            name="Actual Days", marker_color=C["red"], opacity=0.85
        ))
        fig_cmp.add_trace(go.Bar(
            x=mode_stats["Shipping Mode"], y=mode_stats["Avg_Sched_Days"],
            name="Scheduled Days", marker_color=C["green"], opacity=0.85
        ))
        fig_cmp.update_layout(
            barmode="group",
            title="Actual vs Scheduled Shipping Days by Mode",
            height=360, **THEME
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

    with c2:
        fig_prof = px.scatter(
            mode_stats, x="Late_Pct", y="Avg_Profit",
            size="Orders", color="Shipping Mode",
            color_discrete_sequence=[C["orange"], C["blue"], C["green"], C["purple"]],
            text="Shipping Mode",
            title="Late Risk % vs Avg Profit per Order (bubble = order volume)",
        )
        fig_prof.update_traces(textposition="top center")
        fig_prof.update_layout(showlegend=False, height=360, **THEME)
        st.plotly_chart(fig_prof, use_container_width=True)

    # Summary table
    st.markdown('<div class="section-hdr">Mode Performance Summary Table</div>', unsafe_allow_html=True)
    mode_display = mode_stats[["Shipping Mode", "Orders", "Late_Risk", "Late_Pct",
                                "Avg_Delay", "Avg_Real_Days", "Avg_Sched_Days", "Avg_Profit"]].copy()
    mode_display.columns = ["Mode", "Orders", "Late Orders", "Late %",
                             "Avg Delay (d)", "Avg Real (d)", "Avg Sched (d)", "Avg Profit ($)"]
    st.dataframe(mode_display, use_container_width=True, hide_index=True)

    # SLA compliance by mode
    st.markdown('<div class="section-hdr">SLA Compliance by Mode</div>', unsafe_allow_html=True)
    fig_sla = go.Figure()
    fig_sla.add_trace(go.Bar(
        x=mode_stats["Shipping Mode"],
        y=100 - mode_stats["Late_Pct"],
        name="SLA Compliance %",
        marker_color=[C["green"] if v >= 50 else C["red"] for v in (100 - mode_stats["Late_Pct"])],
        text=(100 - mode_stats["Late_Pct"]).apply(lambda x: f"{x:.1f}%"),
        textposition="outside"
    ))
    fig_sla.add_hline(y=95, line_dash="dot", line_color=C["cyan"],
                      annotation_text="95% SLA target", annotation_font_color=C["cyan"])
    fig_sla.add_hline(y=80, line_dash="dot", line_color=C["amber"],
                      annotation_text="80% minimum", annotation_font_color=C["amber"])
    fig_sla.update_layout(title="On-Time SLA Compliance % by Shipping Mode", height=320, **THEME)
    st.plotly_chart(fig_sla, use_container_width=True)

# ══════════════════════════════════════════
# TAB 4 — REGIONAL & MARKET
# ══════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-hdr">Regional & Market Delay Diagnostics</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        mkt_stats = dff.groupby("Market").agg(
            Orders=("Late_delivery_risk", "count"),
            Late_Pct=("Late_delivery_risk", lambda x: round(x.mean() * 100, 1)),
            Avg_Delay=("Delay_Gap", "mean"),
        ).reset_index().sort_values("Late_Pct", ascending=False)
        fig_mkt = px.bar(
            mkt_stats, x="Market", y="Late_Pct",
            color="Late_Pct",
            color_continuous_scale=[[0, C["green"]], [0.5, C["amber"]], [1, C["red"]]],
            title="Late Delivery Risk % by Market",
            text=mkt_stats["Late_Pct"].apply(lambda x: f"{x:.1f}%")
        )
        fig_mkt.update_traces(textposition="outside")
        fig_mkt.add_hline(y=50, line_dash="dash", line_color=C["slate"])
        fig_mkt.update_layout(showlegend=False, coloraxis_showscale=False, height=360, **THEME)
        st.plotly_chart(fig_mkt, use_container_width=True)

    with c2:
        reg_stats = dff.groupby("Order Region").agg(
            Orders=("Late_delivery_risk", "count"),
            Late_Pct=("Late_delivery_risk", lambda x: round(x.mean() * 100, 1)),
            Avg_Delay=("Delay_Gap", "mean"),
        ).reset_index().sort_values("Late_Pct", ascending=True)
        fig_reg = px.bar(
            reg_stats, y="Order Region", x="Late_Pct",
            orientation="h",
            color="Late_Pct",
            color_continuous_scale=[[0, C["green"]], [0.5, C["amber"]], [1, C["red"]]],
            title="Late Risk % by Region",
            text=reg_stats["Late_Pct"].apply(lambda x: f"{x:.1f}%")
        )
        fig_reg.update_traces(textposition="outside")
        fig_reg.update_layout(coloraxis_showscale=False, height=560, **THEME)
        st.plotly_chart(fig_reg, use_container_width=True)

    # Geographic scatter (lat/lon)
    st.markdown('<div class="section-hdr">Geographic Delay Distribution</div>', unsafe_allow_html=True)
    geo_sample = dff.dropna(subset=["Latitude", "Longitude"]).sample(min(5000, len(dff)), random_state=42)
    fig_geo = px.scatter_geo(
        geo_sample,
        lat="Latitude", lon="Longitude",
        color="Late_delivery_risk",
        color_continuous_scale=[[0, C["green"]], [1, C["red"]]],
        opacity=0.4,
        size_max=4,
        title="Order Locations — Late Risk (Red = Late, Green = On-Time)",
        projection="natural earth"
    )
    fig_geo.update_layout(
        height=420,
        geo=dict(bgcolor="rgba(0,0,0,0)", landcolor="#162035",
                 oceancolor="#0c1220", showocean=True,
                 framecolor="#162035", showframe=True,
                 coastlinecolor="#1a3050", showcoastlines=True),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#64748b"),
        coloraxis_showscale=False,
        margin=dict(t=35, b=10, l=0, r=0)
    )
    st.plotly_chart(fig_geo, use_container_width=True)

    # Market x shipping mode heatmap
    st.markdown('<div class="section-hdr">Late Risk % — Market × Shipping Mode</div>', unsafe_allow_html=True)
    cross = dff.groupby(["Market", "Shipping Mode"])["Late_delivery_risk"].mean().reset_index()
    cross["Late_Pct"] = (cross["Late_delivery_risk"] * 100).round(1)
    pivot = cross.pivot(index="Market", columns="Shipping Mode", values="Late_Pct")
    fig_cross = px.imshow(
        pivot,
        color_continuous_scale=[[0, "#0c1220"], [0.4, "#1a3050"], [0.7, C["amber"]], [1, C["red"]]],
        title="Late Risk % Heatmap: Market × Shipping Mode",
        text_auto=".1f",
        aspect="auto"
    )
    fig_cross.update_layout(height=320, **THEME)
    st.plotly_chart(fig_cross, use_container_width=True)

# ══════════════════════════════════════════
# TAB 5 — EXECUTIVE SUMMARY
# ══════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-hdr">Executive Summary — Government & Stakeholder Report</div>', unsafe_allow_html=True)

    st.markdown(f"**Filtered dataset:** {total:,} orders across {dff['Market'].nunique()} markets and {dff['Order Region'].nunique()} regions")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**📦 Order Volume**")
        st.metric("Total Orders", f"{total:,}")
        st.metric("On-Time Orders", f"{dff['On_Time_Flag'].sum():,}")
        st.metric("Late Risk Orders", f"{dff['Late_delivery_risk'].sum():,}")
        st.metric("Cancelled Orders", f"{len(dff[dff['Order Status']=='CANCELED']):,}")

    with c2:
        st.markdown("**⏱️ Timing**")
        st.metric("Avg Real Shipping Days", f"{dff['Days for shipping (real)'].mean():.2f}")
        st.metric("Avg Scheduled Days", f"{dff['Days for shipment (scheduled)'].mean():.2f}")
        st.metric("Avg Delay Gap", f"{avg_delay:+.2f} days")
        st.metric("Max Delay Gap", f"+{dff['Delay_Gap'].max()} days")

    with c3:
        st.markdown("**💰 Financial**")
        st.metric("Avg Sales per Customer", f"${dff['Sales per customer'].mean():.2f}")
        st.metric("Avg Benefit/Order (Late)", f"${dff[dff['Late_delivery_risk']==1]['Benefit per order'].mean():.2f}")
        st.metric("Avg Benefit/Order (On-Time)", f"${dff[dff['Late_delivery_risk']==0]['Benefit per order'].mean():.2f}")
        st.metric("Avg Order Profit Ratio", f"{dff['Order Item Profit Ratio'].mean():.4f}")

    st.markdown("---")
    st.markdown("### Key Findings")

    findings = [
        ("🔴 54.8% of All Orders Carry Late Delivery Risk",
         "This is a systemic baseline, not an anomaly. The uniformity across all 5 markets (54.4%–55.2%) confirms the root cause is global scheduling policy, not regional infrastructure."),
        ("⚡ First Class Shipping Fails 95.3% of Orders",
         "Scheduled at 1 day but consistently taking 2 days, First Class is the most misleading mode. Recalibrating its promise to 2 days would eliminate this failure without any operational change."),
        ("✅ Standard Class Is the Most Reliable Mode",
         "With only 38.1% late risk, Standard Class succeeds by setting honest expectations (4-day schedule, 4-day actual). Reliability comes from schedule accuracy, not speed."),
        ("🏢 Corporate Clients Receive No SLA Advantage",
         "Corporate customers face 54.7% late risk — identical to consumers. Enterprise SLA contracts are likely being systematically breached for more than half of all corporate orders."),
        ("🌍 Regional Differences Are Small but Real",
         "Central Africa (58.0%) and South Asia (56.3%) show the highest regional delay rates, suggesting some infrastructure-related delay on top of the global scheduling baseline."),
    ]

    for title, body in findings:
        with st.expander(title):
            st.write(body)

    st.markdown("### Recommendations")
    st.markdown("""
1. **Recalibrate First Class promised delivery from 1 → 2 days** — immediate, zero-cost fix that eliminates 95% of First Class SLA failures
2. **Recalibrate Second Class from 2 → 4 days** — same principle; actual delivery is ~4 days regardless
3. **Audit corporate SLA contracts** — 54.7% late rate means systematic breach; legal and financial exposure is significant  
4. **Build predictive delay flag** using Shipping Mode + Region + Category — these three fields can predict delay with high accuracy
5. **Investigate niche category delays** — Golf Bags (68.9%), Lacrosse (60.1%), Pet Supplies (58.9%) show above-average risk
6. **Monitor cancellation correlation with delays** — 3,692 cancellations may be delay-driven churn
    """)

    st.markdown("---")
    st.caption("APL Logistics Delivery Analytics ·  180,519 orders · 40 fields")
