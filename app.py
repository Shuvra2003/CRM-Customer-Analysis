import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Custom Dashboard Styling

st.markdown("""
<style>

    /* Main dashboard background */
    .stApp {
    background: #10141b;
    color: #f5f7fa;
    }

    /* Main content area */
    .main {
        background: #10141b;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #151a22;
        border-right: 1px solid #252c38;
    }

    /* KPI metric cards */
    div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #1a202b,
        #121720
    );

    border: 1px solid #2b3442;

    border-radius: 18px;

    padding: 18px;

    box-shadow:
        0 8px 20px rgba(0, 0, 0, 0.55),
        inset 0 1px 0 rgba(255, 255, 255, 0.04),
        0 0 18px rgba(80, 140, 255, 0.10);
    }

    /* KPI labels */
    div[data-testid="stMetricLabel"] {
        color: #b8c0cc;
    }

    /* KPI values */
    div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-weight: 700;
    }

    /* Chart cards */

    div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        145deg,
        #1a202b,
        #121720
    );

    border: 1px solid #2b3442;
    border-radius: 18px;

    box-shadow:
        0 10px 25px rgba(0, 0, 0, 0.55),
        inset 0 1px 0 rgba(255, 255, 255, 0.04),
        0 0 20px rgba(80, 140, 255, 0.07);
    }

    /* Streamlit headings */
    h1, h2, h3 {
        color: #f5f7fa;
    }

</style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="CRM Customer Analytics",
    page_icon="📊",
    layout="wide"
)

# Load cleaned dataset
df = pd.read_csv("output/cleaned_crm_data.csv")
df_original = df.copy()

# Sidebar Filters

st.sidebar.header("🔎 Filters")

segment_filter = st.sidebar.multiselect(
    "Customer Segment",
    options=df_original["Customer_Segment"].unique(),
    default=df_original["Customer_Segment"].unique(),
    key="segment_filter"
)

category_filter = st.sidebar.multiselect(
    "Product Category",
    options=df_original["Product_Category"].unique(),
    default=df_original["Product_Category"].unique(),
    key="category_filter"
)

channel_filter = st.sidebar.multiselect(
    "Acquisition Channel",
    options=df_original["Acquisition_Channel"].unique(),
    default=df_original["Acquisition_Channel"].unique(),
    key="channel_filter"
)

if st.sidebar.button("🔄 Reset Filters"):
    st.session_state["segment_filter"] = df_original["Customer_Segment"].unique().tolist()
    st.session_state["category_filter"] = df_original["Product_Category"].unique().tolist()
    st.session_state["channel_filter"] = df_original["Acquisition_Channel"].unique().tolist()
    st.rerun()

# Apply Filters

df = df[
    (df["Customer_Segment"].isin(segment_filter)) &
    (df["Product_Category"].isin(category_filter)) &
    (df["Acquisition_Channel"].isin(channel_filter))
]

# Dashboard Title

st.title("📊 CRM Customer Analytics Dashboard")

st.write(
    "Interactive analysis of customer behavior, "
    "spending patterns and customer segments."
)

# Calculate KPIs

total_customers = df["Customer_ID"].nunique()
total_revenue = df["Total_Spending"].sum()
total_purchases = df["Total_Purchases"].sum()
average_spending = df["Total_Spending"].mean()

high_value_customers = (
    df["Customer_Segment"] == "High Value"
).sum()

at_risk_customers = (
    df["Customer_Segment"] == "At Risk"
).sum()

# KPI Cards

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "💰 Total Revenue",
        f"Rs. {total_revenue / 1_000_000:,.0f}M"
    )

with col3:
    st.metric(
        "🛒 Total Purchases",
        f"{total_purchases:,}"
    )

with col4:
    st.metric(
        "💎 High Value Customers",
        f"{high_value_customers:,}"
    )

with col5:
    st.metric(
        "⚠️ At Risk Customers",
        f"{at_risk_customers:,}"
    )

# Dashboard Charts

col1, col2 = st.columns(2)

# Customer Segment Distribution
with col1:
    with st.container(border=True):

        st.subheader("👥 Customer Segment Distribution")

        segment_counts = df["Customer_Segment"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 5))

        fig.patch.set_facecolor("#151a22")
        ax.set_facecolor("#151a22")

        bar_colors = [
            "#ff5c5c",   # At Risk
            "#4da6ff",   # High Value
            "#a66cff",   # Potential Loyalists
            "#39d98a",   # Loyal Customers
            "#ffb84d"    # Low Value
        ]

        ax.bar(
            segment_counts.index,
            segment_counts.values,
            color=bar_colors,
            edgecolor="none"
        )
        for bar in ax.patches:
            bar.set_alpha(0.9)

        ax.set_xlabel("Customer Segment")
        ax.set_ylabel("Customers")

        ax.title.set_color("#f5f7fa")
        ax.xaxis.label.set_color("#b8c0cc")
        ax.yaxis.label.set_color("#b8c0cc")

        ax.tick_params(axis="x", colors="#b8c0cc")
        ax.tick_params(axis="y", colors="#b8c0cc")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#303846")
        ax.spines["bottom"].set_color("#303846")

        ax.grid(
            axis="y",
            color="#303846",
            linestyle="--",
            alpha=0.45
        )

        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()

        st.pyplot(fig)


# Revenue by Customer Segment
with col2:
    with st.container(border=True):

        st.subheader("💰 Revenue by Customer Segment")

        segment_revenue = (
            df.groupby("Customer_Segment")["Total_Spending"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        fig.patch.set_facecolor("#151a22")
        ax.set_facecolor("#151a22")

        bar_colors = [
            "#4da6ff",
            "#ff5c5c",
            "#39d98a",
            "#a66cff",
            "#ffb84d"
        ]

        ax.bar(
            segment_revenue.index,
            segment_revenue.values,
            color=bar_colors,
            edgecolor="none"
        )

        ax.set_xlabel("Customer Segment")
        ax.set_ylabel("Revenue")

        ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"₹{x / 1_000_000:.0f}M")
        )

        ax.xaxis.label.set_color("#b8c0cc")
        ax.yaxis.label.set_color("#b8c0cc")

        ax.tick_params(axis="x", colors="#b8c0cc")
        ax.tick_params(axis="y", colors="#b8c0cc")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#303846")
        ax.spines["bottom"].set_color("#303846")

        ax.grid(
            axis="y",
            color="#303846",
            linestyle="--",
            alpha=0.45
        )

        plt.xticks(rotation=25, ha="right")

        plt.tight_layout()

        st.pyplot(fig)


# Revenue by Product Category
with col1:
    with st.container(border=True):

        st.subheader("📦 Revenue by Product Category")

        category_revenue = (
            df.groupby("Product_Category")["Total_Spending"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        fig.patch.set_facecolor("#151a22")
        ax.set_facecolor("#151a22")

        category_colors = [
            "#4da6ff",
            "#39d98a",
            "#ffb84d",
            "#a66cff",
            "#ff5c5c",
            "#22d3ee"
        ]

        ax.bar(
            category_revenue.index,
            category_revenue.values,
            color=category_colors[:len(category_revenue)],
            edgecolor="none"
        )

        ax.set_xlabel("Product Category")
        ax.set_ylabel("Revenue")

        ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"₹{x / 1_000_000:.0f}M")
        )

        ax.xaxis.label.set_color("#b8c0cc")
        ax.yaxis.label.set_color("#b8c0cc")

        ax.tick_params(axis="x", colors="#b8c0cc")
        ax.tick_params(axis="y", colors="#b8c0cc")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#303846")
        ax.spines["bottom"].set_color("#303846")

        ax.grid(
            axis="y",
            color="#303846",
            linestyle="--",
            alpha=0.45
        )

        plt.xticks(rotation=25, ha="right")

        plt.tight_layout()

        st.pyplot(fig)


# Revenue by Acquisition Channel
with col2:
    with st.container(border=True):

        st.subheader("📣 Revenue by Acquisition Channel")

        channel_revenue = (
            df.groupby("Acquisition_Channel")["Total_Spending"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        fig.patch.set_facecolor("#151a22")
        ax.set_facecolor("#151a22")

        channel_colors = [
            "#a66cff",
            "#4da6ff",
            "#39d98a",
            "#ffb84d",
            "#ff5c5c",
            "#22d3ee"
        ]

        ax.bar(
            channel_revenue.index,
            channel_revenue.values,
            color=channel_colors[:len(channel_revenue)],
            edgecolor="none"
        )

        ax.set_xlabel("Acquisition Channel")
        ax.set_ylabel("Revenue")

        ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"₹{x / 1_000_000:.0f}M")
        )

        ax.xaxis.label.set_color("#b8c0cc")
        ax.yaxis.label.set_color("#b8c0cc")

        ax.tick_params(axis="x", colors="#b8c0cc")
        ax.tick_params(axis="y", colors="#b8c0cc")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#303846")
        ax.spines["bottom"].set_color("#303846")

        ax.grid(
            axis="y",
            color="#303846",
            linestyle="--",
            alpha=0.45
        )

        plt.xticks(rotation=25, ha="right")

        plt.tight_layout()

        st.pyplot(fig)


# Customer Status Distribution
with col1:
    with st.container(border=True):

        st.subheader("📊 Customer Status Distribution")

        status_counts = df["Customer_Status"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 5))

        fig.patch.set_facecolor("#151a22")
        ax.set_facecolor("#151a22")

        status_colors = [
            "#39d98a",
            "#ff5c5c",
            "#4da6ff",
            "#ffb84d",
            "#a66cff"
        ]

        ax.bar(
            status_counts.index,
            status_counts.values,
            color=status_colors[:len(status_counts)],
            edgecolor="none"
        )

        ax.set_xlabel("Customer Status")
        ax.set_ylabel("Customers")

        ax.xaxis.label.set_color("#b8c0cc")
        ax.yaxis.label.set_color("#b8c0cc")

        ax.tick_params(axis="x", colors="#b8c0cc")
        ax.tick_params(axis="y", colors="#b8c0cc")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#303846")
        ax.spines["bottom"].set_color("#303846")

        ax.grid(
            axis="y",
            color="#303846",
            linestyle="--",
            alpha=0.45
        )

        plt.xticks(rotation=25, ha="right")

        plt.tight_layout()

        st.pyplot(fig)


# Top 10 Customers
with col2:
    with st.container(border=True):

        st.subheader("🏆 Top 10 Customers by Spending")

        top_customers = (
            df.groupby("Customer_ID")["Total_Spending"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        fig.patch.set_facecolor("#151a22")
        ax.set_facecolor("#151a22")

        ax.barh(
            top_customers.index[::-1],
            top_customers.values[::-1],
            color="#a66cff",
            edgecolor="none"
        )

        ax.set_xlabel("Total Spending")
        ax.set_ylabel("Customer ID")

        ax.xaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"₹{x / 1_000:.0f}K")
        )

        ax.xaxis.label.set_color("#b8c0cc")
        ax.yaxis.label.set_color("#b8c0cc")

        ax.tick_params(axis="x", colors="#b8c0cc")
        ax.tick_params(axis="y", colors="#b8c0cc")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#303846")
        ax.spines["bottom"].set_color("#303846")

        ax.grid(
            axis="x",
            color="#303846",
            linestyle="--",
            alpha=0.45
        )

        plt.tight_layout()

        st.pyplot(fig)

# Customer Details

st.subheader("👤 Customer Details")

display_columns = [
    "Customer_ID",
    "Age",
    "Gender",
    "Location",
    "Total_Purchases",
    "Total_Spending",
    "Recency_Days",
    "Customer_Segment",
    "Customer_Status"
]

st.dataframe(
    df[display_columns].sort_values(
        "Total_Spending",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)

# Download Filtered Data

csv_data = df[display_columns].to_csv(index=False)

st.download_button(
    label="📥 Download Customer Data",
    data=csv_data,
    file_name="filtered_crm_customer_data.csv",
    mime="text/csv"
)

# Key Insights

st.subheader("💡 Key Insights")

top_segment = df["Customer_Segment"].value_counts().idxmax()

top_category = (
    df.groupby("Product_Category")["Total_Spending"]
    .sum()
    .idxmax()
)

top_channel = (
    df.groupby("Acquisition_Channel")["Total_Spending"]
    .sum()
    .idxmax()
)

highest_revenue_segment = (
    df.groupby("Customer_Segment")["Total_Spending"]
    .sum()
    .idxmax()
)

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"👥 **Largest Customer Segment:** {top_segment}"
    )

    st.info(
        f"📦 **Top Revenue Product Category:** {top_category}"
    )

with col2:
    st.info(
        f"📣 **Top Revenue Acquisition Channel:** {top_channel}"
    )

    st.info(
        f"💰 **Highest Revenue Customer Segment:** "
        f"{highest_revenue_segment}"
    )

st.markdown("---")

st.caption(
    "CRM Customer Analytics | Built with Python, Pandas, NumPy, Matplotlib, "
    "Seaborn & Streamlit | Built by [*Shuvradipta Mukhopadhyay*] | © 2026"
)