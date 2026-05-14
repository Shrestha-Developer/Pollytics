import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Poll Results Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
df = pd.read_csv("data/cleaned_poll_data.csv")

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0B1120;
    color: white;
}

header[data-testid="stHeader"] {
    background: transparent;
    height: 0rem;
}

div[data-testid="stToolbar"] {
    right: 1rem;
}

section.main > div {
    padding-top: 0rem !important;
}

.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem;
    max-width: 95%;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #0F172A 100%);
    border-right: 1px solid #1F2937;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #1F2937 !important;
    color: white !important;
    border: 1px solid #374151 !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: #60A5FA;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    color: #9CA3AF;
    font-size: 15px;
    margin-bottom: 30px;
}

/* KPI Cards */
.metric-card {
    background: #111827;
    border: 1px solid #1E3A5F;
    border-radius: 18px;
    padding: 22px 10px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(0,0,0,0.35);
    margin-bottom: 18px;
}

.metric-title {
    color: #D1D5DB;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 12px;
}

.metric-blue {
    color: #60A5FA;
    font-size: 42px;
    font-weight: bold;
}

.metric-green {
    color: #86EFAC;
    font-size: 42px;
    font-weight: bold;
}

.metric-yellow {
    color: #FCD34D;
    font-size: 42px;
    font-weight: bold;
}

/* Chart Cards */
.chart-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 18px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.35);
}

.chart-title {
    text-align: center;
    color: #E5E7EB;
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.markdown("## 🔎 Filters")

region_options = ["All"] + sorted(df["Region"].unique().tolist())

selected_region = st.sidebar.selectbox(
    "Select Region",
    region_options
)

# ---------------------------------------------------------
# FILTER DATA
# ---------------------------------------------------------
if selected_region != "All":
    filtered_df = df[df["Region"] == selected_region]
else:
    filtered_df = df.copy()

# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------
total_responses = len(filtered_df)
most_preferred = filtered_df["Selected_Option"].mode()[0]
avg_satisfaction = round(filtered_df["Satisfaction"].mean(), 1)

vote_summary = filtered_df["Selected_Option"].value_counts()
satisfaction_summary = filtered_df["Satisfaction"].value_counts().sort_index()
region_summary = filtered_df["Region"].value_counts()

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.markdown(
    """
    <div class="main-title">📊 POLLYTICS</div>

    <div style="
        font-size: 32px;
        font-weight: 700;
        margin-top: 10px;
        color: white;
    ">
        AI-Powered Poll Analytics Dashboard
    </div>

    <div class="subtitle" style="
        font-size: 18px;
        margin-top: 8px;
        color: #cfcfcf;
    ">
        Interactive dashboard for survey responses, product preferences and satisfaction trends
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Responses</div>
        <div class="metric-blue">{total_responses}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Most Preferred Product</div>
        <div class="metric-green">{most_preferred}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Satisfaction</div>
        <div class="metric-yellow">{avg_satisfaction} / 5</div>
    </div>
    """, unsafe_allow_html=True)

# Replace your entire CHART ROW 1 and CHART ROW 2 section with this

# ---------------------------------------------------------
# CHART ROW 1
# ---------------------------------------------------------
col1, col2 = st.columns(2)

colors = ['#60A5FA', '#86EFAC', '#F97316']

with col1:
    st.markdown("### Vote Count by Product")

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    fig1.patch.set_facecolor('#111827')
    ax1.set_facecolor('#111827')

    ax1.bar(
        vote_summary.index,
        vote_summary.values,
        color=colors[:len(vote_summary)],
        edgecolor='white',
        linewidth=1.2
    )

    ax1.set_ylabel("Votes", color='white')
    ax1.tick_params(colors='white')
    ax1.spines['bottom'].set_color('white')
    ax1.spines['left'].set_color('white')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    st.pyplot(fig1, use_container_width=True)

with col2:
    st.markdown("### Vote Share")

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    fig2.patch.set_facecolor('#111827')
    ax2.set_facecolor('#111827')

    ax2.pie(
        vote_summary.values,
        labels=vote_summary.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors[:len(vote_summary)],
        wedgeprops=dict(edgecolor='white', linewidth=1.5),
        textprops=dict(color='white', fontsize=12)
    )

    ax2.axis('equal')

    st.pyplot(fig2, use_container_width=True)

# ---------------------------------------------------------
# CHART ROW 2
# ---------------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    st.markdown("### Satisfaction Distribution")

    fig3, ax3 = plt.subplots(figsize=(6, 4))
    fig3.patch.set_facecolor('#111827')
    ax3.set_facecolor('#111827')

    ax3.bar(
        satisfaction_summary.index.astype(str),
        satisfaction_summary.values,
        color='#FCD34D',
        edgecolor='white',
        linewidth=1.2
    )

    ax3.set_xlabel("Rating", color='white')
    ax3.set_ylabel("Responses", color='white')
    ax3.tick_params(colors='white')
    ax3.spines['bottom'].set_color('white')
    ax3.spines['left'].set_color('white')
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)

    st.pyplot(fig3, use_container_width=True)

with col4:
    st.markdown("### Region-wise Responses")

    fig4, ax4 = plt.subplots(figsize=(6, 4))
    fig4.patch.set_facecolor('#111827')
    ax4.set_facecolor('#111827')

    ax4.bar(
        region_summary.index,
        region_summary.values,
        color='#A78BFA',
        edgecolor='white',
        linewidth=1.2
    )

    ax4.set_xlabel("Region", color='white')
    ax4.set_ylabel("Responses", color='white')
    ax4.tick_params(colors='white')
    ax4.spines['bottom'].set_color('white')
    ax4.spines['left'].set_color('white')
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)

    st.pyplot(fig4, use_container_width=True)