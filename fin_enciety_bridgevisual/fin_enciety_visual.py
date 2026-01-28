import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="ENCiETY Financial Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# LOAD DATA (CACHED)
# ===============================
@st.cache_data
def load_data():
    df = pd.read_excel(
        "C:/Users/Eren Lutfimorea/Downloads/ENCIETY_BI/fin_enciety_output/fundamental_summary.xlsx",
        engine="openpyxl"
    )

    # safety: normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df

df = load_data()

st.title("📊 ENCiETY Financial Intelligence Dashboard")
st.caption("Source: IDX Financial Statements (Processed)")

# ===============================
# SIDEBAR FILTERS
# ===============================
st.sidebar.header("🔎 Filters")

selected_emiten = st.sidebar.multiselect(
    "Emitens",
    options=sorted(df["emiten"].dropna().unique()),
    default=None
)

selected_year = st.sidebar.multiselect(
    "Years",
    options=sorted(df["year"].dropna().unique()),
    default=None
)

selected_quarter = st.sidebar.multiselect(
    "Quarter",
    options=sorted(df["quarter"].dropna().unique()),
    default=None
)

# Apply filters
if selected_emiten:
    df = df[df["emiten"].isin(selected_emiten)]

if selected_year:
    df = df[df["year"].isin(selected_year)]

if selected_quarter:
    df = df[df["quarter"].isin(selected_quarter)]

# ===============================
# KPI SECTION
# ===============================
st.subheader("📌 Key Financial Metrics")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Rata-rata Total Aset",
    f"{df['jumlah_aset'].mean():,.0f}" if "jumlah_aset" in df else "-"
)

c2.metric(
    "Rata-rata Total Liabilitas",
    f"{df['jumlah_liabilitas'].mean():,.0f}" if "jumlah_liabilitas" in df else "-"
)

c3.metric(
    "Rata-rata Total Ekuitas",
    f"{df['jumlah_ekuitas'].mean():,.0f}" if "jumlah_ekuitas" in df else "-"
)

# ===============================
# TREND CHART
# ===============================
st.subheader("📈 Financial Trend")

metric_option = st.selectbox(
    "Pilih Metric",
    options=[
        col for col in df.columns
        if col not in ["emiten", "year", "quarter", "sektor"]
    ]
)

fig_trend = px.line(
    df,
    x="year",
    y=metric_option,
    color="emiten",
    markers=True,
    title=f"Trend {metric_option.upper()}"
)

st.plotly_chart(fig_trend, use_container_width=True)

# ===============================
# COMPARISON BAR CHART
# ===============================
st.subheader("🏢 Perbandingan Emiten")

fig_bar = px.bar(
    df,
    x="emiten",
    y=metric_option,
    color="emiten",
    title=f"Perbandingan {metric_option.upper()}",
)

st.plotly_chart(fig_bar, use_container_width=True)

# ===============================
# DATA TABLE
# ===============================
st.subheader("🧾 Data Table")

with st.expander("Lihat Data Lengkap"):
    st.dataframe(df, use_container_width=True)
