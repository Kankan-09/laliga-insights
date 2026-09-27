import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from data import (
    RUNNING_DATA, CORNER_ATTACK, CORNER_DEFENSE,
    SHOOTING_DATA, TEAM_COLORS, SOURCES
)

st.set_page_config(
    page_title="La Liga 2025/26 — Insights",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-title {
        font-size: 2.6rem; font-weight: 800;
        background: linear-gradient(90deg, #A50044, #FEBE10);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-title { color: #888; font-size: 1rem; margin-top: 0; margin-bottom: 2rem; }
    .insight-box {
        background: #1a1a2e; border-left: 4px solid #A50044;
        padding: 1rem 1.2rem; border-radius: 6px;
        margin-bottom: 1rem; color: #e0e0e0;
    }
    .insight-box strong { color: #FEBE10; }
    .metric-card {
        background: #16162a; border: 1px solid #2a2a4a;
        border-radius: 10px; padding: 1rem; text-align: center;
    }
    .metric-card h3 { color: #FEBE10; margin: 0; font-size: 1.8rem; }
    .metric-card p { color: #aaa; margin: 0; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)


def build_running_df():
    return pd.DataFrame(RUNNING_DATA, columns=[
        "Team", "Position", "Points", "TotalDistance_km",
        "HighIntensity_m", "HighIntensityActions", "Sprints"
    ])

def build_corner_attack_df():
    return pd.DataFrame(CORNER_ATTACK, columns=[
        "Team", "CornersTaken", "GoalsFromCorners", "Conversion_pct"
    ]).sort_values("Conversion_pct", ascending=False)

def build_corner_defense_df():
    return pd.DataFrame(CORNER_DEFENSE, columns=[
        "Team", "CornersFaced", "GoalsConceded", "ConcededRate_pct"
    ]).sort_values("ConcededRate_pct", ascending=True)

def build_shooting_df():
    return pd.DataFrame(SHOOTING_DATA, columns=[
        "Team", "Shots", "Goals", "Conversion_pct"
    ])


st.markdown('<p class="main-title">La Liga 2025/26 — Insights</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Three data stories that explain the season beyond the table.</p>',
    unsafe_allow_html=True
)

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose an insight",
    [
        "🏃 The Running Paradox",
        "🎯 Corner Efficiency Gap",
        "⚽ Shooting Efficiency",
        "📊 Full Data Table",
        "📚 Sources & Notes",
    ]
)

# ==================================================================
if page == "🏃 The Running Paradox":
    st.header("The Running Paradox")
    st.markdown("**Total distance covered is a vanity metric. Sprint intensity wins La Liga.**")

    df = build_running_df()
    barca = df[df["Team"] == "Barcelona"].iloc[0]
    madrid = df[df["Team"] == "Real Madrid"].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card"><h3>#1</h3>
        <p>Barcelona — Sprint count<br>({barca['Sprints']} per match)</p></div>""",
        unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card"><h3>20th</h3>
        <p>Real Madrid — Total distance<br>({madrid['TotalDistance_km']} km)</p></div>""",
        unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card"><h3>16th</h3>
        <p>Barcelona — Total distance<br>({barca['TotalDistance_km']} km)</p></div>""",
        unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="metric-card"><h3>+883m</h3>
        <p>Barca vs Madrid<br>high-intensity gap per match</p></div>""",
        unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Total Distance vs. League Points")
    st.caption("If running volume won titles, the top-right would be crowded. It isn't.")

    fig1 = px.scatter(
        df, x="TotalDistance_km", y="Points", size="Sprints",
        color="Points", text="Team", color_continuous_scale="Turbo",
        labels={"TotalDistance_km": "Avg Total Distance (km/match)",
                "Points": "League Points", "Sprints": "Sprints per match"},
        height=550,
    )
    fig1.update_traces(textposition="top center", textfont_size=10)
    fig1.update_layout(template="plotly_dark", plot_bgcolor="#0e0e1a", paper_bgcolor="#0e0e1a")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""<div class="insight-box">
    <strong>Reading it:</strong> Barcelona (1st, 88 pts) ran the 16th-most total distance.
    Real Madrid (2nd, 84 pts) ran the <em>least</em> of any team. Relegated Real Oviedo
    ran the most. Volume ≠ success.
    </div>""", unsafe_allow_html=True)

    st.subheader("Sprint Count per Match — Full Ranking")
    fig2 = px.bar(
        df.sort_values("Sprints"), x="Sprints", y="Team", orientation="h",
        color="Sprints", color_continuous_scale="Plasma",
        labels={"Sprints": "Sprints per match", "Team": ""}, height=650,
    )
    fig2.update_layout(template="plotly_dark", plot_bgcolor="#0e0e1a",
                       paper_bgcolor="#0e0e1a", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ==================================================================
elif page == "🎯 Corner Efficiency Gap":
    st.header("The Corner Efficiency Gap")
    st.markdown("**The most efficient corner-attacking team was relegated. "
                "The best corner defense in Europe won nothing.**")

    atk = build_corner_attack_df()
    dfd = build_corner_defense_df()

    tab1, tab2 = st.tabs(["⚔️ Attacking Corners", "🛡️ Defending Corners"])

    with tab1:
        st.subheader("Corner Conversion Rate — Attacking")
        fig = px.bar(atk, x="Conversion_pct", y="Team", orientation="h",
                     color="Conversion_pct", color_continuous_scale="Viridis",
                     text="Conversion_pct",
                     labels={"Conversion_pct": "Conversion rate (%)", "Team": ""},
                     height=650)
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig.update_layout(template="plotly_dark", plot_bgcolor="#0e0e1a",
                          paper_bgcolor="#0e0e1a", showlegend=False, xaxis_range=[0, 8])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""<div class="insight-box">
        <strong>Headline:</strong> Real Oviedo (relegated) converted <strong>6.67%</strong>
        of corners — best in La Liga, 11th in Europe's Big Five. Levante (relegated) 2nd
        at 6.17%. Barcelona 3rd at 5.30%.
        </div>""", unsafe_allow_html=True)

    with tab2:
        st.subheader("Corner Conversion Rate — Defending")
        st.caption("Lower is better.")
        fig = px.bar(dfd, x="ConcededRate_pct", y="Team", orientation="h",
                     color="ConcededRate_pct", color_continuous_scale="Reds_r",
                     text="ConcededRate_pct",
                     labels={"ConcededRate_pct": "Conceded rate (%)", "Team": ""},
                     height=650)
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig.update_layout(template="plotly_dark", plot_bgcolor="#0e0e1a",
                          paper_bgcolor="#0e0e1a", showlegend=False, xaxis_range=[0, 10])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""<div class="insight-box">
        <strong>Headline:</strong> Real Madrid conceded just <strong>2 goals from 138
        corners (1.45%)</strong> — best in Europe's Big Five. Alavés (1.41%) and
        Elche (1.48%) also top-5 in Europe.
        </div>""", unsafe_allow_html=True)

# ==================================================================
elif page == "⚽ Shooting Efficiency":
    st.header("Shooting Efficiency — Volume vs. Precision")
    st.markdown("**Barcelona took the most shots and scored the most. "
                "They weren't the most efficient.**")

    sdf = build_shooting_df()
    st.subheader("Shots vs. Goals")

    z = np.polyfit(sdf["Shots"], sdf["Goals"], 1)
    xline = np.linspace(sdf["Shots"].min(), sdf["Shots"].max(), 100)
    yline = np.polyval(z, xline)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xline, y=yline, mode="lines",
                             name="Expected (linear fit)",
                             line=dict(color="#555", dash="dash")))
    for _, row in sdf.iterrows():
        color = TEAM_COLORS.get(row["Team"], "#8888cc")
        fig.add_trace(go.Scatter(
            x=[row["Shots"]], y=[row["Goals"]], mode="markers+text",
            marker=dict(size=14, color=color, line=dict(width=1, color="#fff")),
            text=[row["Team"]], textposition="top center",
            textfont=dict(size=9, color="#ccc"), showlegend=False,
            hovertemplate=(f"<b>{row['Team']}</b><br>Shots: {row['Shots']}<br>"
                           f"Goals: {row['Goals']}<br>"
                           f"Conversion: {row['Conversion_pct']}%<extra></extra>"),
        ))
    fig.update_layout(template="plotly_dark", plot_bgcolor="#0e0e1a",
                      paper_bgcolor="#0e0e1a", xaxis_title="Total Shots",
                      yaxis_title="Goals Scored", height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""<div class="insight-box">
    <strong>Above the line = clinical. Below = wasteful.</strong>
    Villarreal (11.4%) and Celta Vigo (10.2%) sit above trend.
    Rayo Vallecano (5.5%) and Real Oviedo (4.8%) are the biggest underperformers.
    </div>""", unsafe_allow_html=True)

    st.subheader("Conversion Rate — Full Ranking")
    fig2 = px.bar(sdf.sort_values("Conversion_pct"), x="Conversion_pct", y="Team",
                  orientation="h", color="Conversion_pct", color_continuous_scale="Turbo",
                  text="Conversion_pct",
                  labels={"Conversion_pct": "Goals per shot (%)", "Team": ""}, height=650)
    fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig2.update_layout(template="plotly_dark", plot_bgcolor="#0e0e1a",
                       paper_bgcolor="#0e0e1a", showlegend=False, xaxis_range=[0, 13])
    st.plotly_chart(fig2, use_container_width=True)

# ==================================================================
elif page == "📊 Full Data Table":
    st.header("Full Data Tables")
    st.caption("Download-ready. Every number used in this dashboard.")

    st.subheader("Running Intensity")
    st.dataframe(build_running_df(), use_container_width=True, hide_index=True)
    st.subheader("Corner Attack")
    st.dataframe(build_corner_attack_df(), use_container_width=True, hide_index=True)
    st.subheader("Corner Defense")
    st.dataframe(build_corner_defense_df(), use_container_width=True, hide_index=True)
    st.subheader("Shooting")
    st.dataframe(build_shooting_df(), use_container_width=True, hide_index=True)

    combined = build_running_df().merge(build_shooting_df(), on="Team", how="outer")
    csv = combined.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download combined CSV", data=csv,
                       file_name="laliga_2025_26_insights.csv", mime="text/csv")

# ==================================================================
elif page == "📚 Sources & Notes":
    st.header("Sources & Methodology Notes")
    st.markdown("### Data Sources")
    for k, v in SOURCES.items():
        st.markdown(f"- **{k.title()}**: {v}")
    st.markdown("### Transparency Notes")
    st.markdown("""
    - **Running data** comes from Driblab tracking (via Marca) — third-party, not official.
    - **Corner and shooting data** compiled from FBref, Transfermarkt, Sportradar.
    - Figures in this demo are illustrative. Swap `data.py` with a live scraper before
      publishing as factual.
    """)
    st.markdown("### Portfolio Framing")
    st.markdown("""> **La Liga 2025/26: What the Numbers Actually Say About Winning**
    >
    > Three data stories — running intensity, corner efficiency, shooting precision —
    > reveal tactical specialization, not raw effort, drives outcomes.""")

st.markdown("---")
st.caption("Built with Streamlit · Plotly · Pandas · "
           "Data: FBref / Transfermarkt / Sportradar / Driblab via Marca")