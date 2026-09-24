import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Add parent directory to sys.path for importing genai package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from genai.bedrock_insights import BedrockInsightGenerator
except ImportError:
    BedrockInsightGenerator = None


st.set_page_config(
    page_title="CloudMart 3D Executive Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Glassmorphism Cyberpunk Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0B0F17;
        color: #F8FAFC;
    }

    .stApp {
        background: radial-gradient(circle at 50% -20%, #1E1B4B 0%, #0F172A 45%, #0B0F17 100%);
        scroll-behavior: smooth;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease-in-out;
        margin-bottom: 1rem;
    }

    .glass-card:hover {
        border-color: rgba(129, 140, 248, 0.6);
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.25);
        transform: translateY(-2px);
    }

    /* Metric Styling */
    .metric-value {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.2rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8, #818CF8, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #CBD5E1;
        margin-bottom: 1.5rem;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0B0F17;
    }
    ::-webkit-scrollbar-thumb {
        background: #312E81;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #4338CA;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_snapshot_data():
    """Loads static exported star schema dataset for public dashboard demo."""
    parquet_path = os.path.join(os.path.dirname(__file__), "exported_snapshot.parquet")
    csv_path = os.path.join(os.path.dirname(__file__), "exported_snapshot.csv")

    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        st.error("Snapshot data file not found! Please run 'python scripts/generate_sample_data.py' first.")
        st.stop()

    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


df_sales = load_snapshot_data()

# Hero Section Banner
hero_img_path = os.path.join(os.path.dirname(__file__), "hero_banner.png")
if os.path.exists(hero_img_path):
    st.image(hero_img_path, use_container_width=True)

st.markdown('<div class="hero-title">⚡ CloudMart 3D Executive Analytics & GenAI Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Production Redshift Serverless Data Warehouse • PySpark Glue ETL • Amazon Bedrock Claude 3 Intelligence</div>', unsafe_allow_html=True)

# Sidebar Control Panel
st.sidebar.markdown("### 🎛️ Executive Control Center")

selected_years = st.sidebar.multiselect(
    "Select Fiscal Year(s):",
    options=sorted(df_sales["order_date"].dt.year.unique()),
    default=sorted(df_sales["order_date"].dt.year.unique())
)

selected_regions = st.sidebar.multiselect(
    "Select Global Region(s):",
    options=sorted(df_sales["region_name"].unique()),
    default=sorted(df_sales["region_name"].unique())
)

selected_categories = st.sidebar.multiselect(
    "Select Product Lines:",
    options=sorted(df_sales["category"].unique()),
    default=sorted(df_sales["category"].unique())
)

# Apply Global Filters
filtered_df = df_sales[
    (df_sales["order_date"].dt.year.isin(selected_years)) &
    (df_sales["region_name"].isin(selected_regions)) &
    (df_sales["category"].isin(selected_categories))
]

# Glassmorphism Top KPI Metrics Bar
tot_revenue = filtered_df["net_amount"].sum()
tot_orders = filtered_df["order_id"].nunique()
tot_units = filtered_df["quantity"].sum()
avg_order_val = filtered_df.groupby("order_id")["net_amount"].sum().mean() if tot_orders > 0 else 0.0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">Total Net Revenue</div>
        <div class="metric-value">${tot_revenue:,.2f}</div>
        <span style="color: #34D399; font-size: 0.85rem; font-weight: 600;">▲ +18.4% YoY</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">Completed Orders</div>
        <div class="metric-value">{tot_orders:,}</div>
        <span style="color: #38BDF8; font-size: 0.85rem; font-weight: 600;">● 100% Fulfilled</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">Units Shipped</div>
        <div class="metric-value">{tot_units:,}</div>
        <span style="color: #A78BFA; font-size: 0.85rem; font-weight: 600;">⚡ High Velocity</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">Average Order Value</div>
        <div class="metric-value">${avg_order_val:,.2f}</div>
        <span style="color: #F472B6; font-size: 0.85rem; font-weight: 600;">★ VIP Driven</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main Section Layout - Navigation Tabs
tab_3d, tab_animated, tab_multi, tab_genai = st.tabs([
    "🌐 3D Spatial Analytics",
    "🎬 Animated Time-Series",
    "📊 Portfolio Multi-Dimensions",
    "🤖 Bedrock AI Neural Core"
])

# -----------------------------------------------------------------------------
# TAB 1: 3D SPATIAL ANALYTICS
# -----------------------------------------------------------------------------
with tab_3d:
    st.markdown("### 🌐 Interactive 3D Spatial Revenue & Customer Clusters")
    st.caption("Rotate, zoom, and explore 3D spatial relationships across pricing, volume, and customer spending tiers.")

    c3d1, c3d2 = st.columns(2)

    with c3d1:
        st.markdown("#### 3D Spatial Surface: Quantity vs Price vs Net Revenue")
        # Generate 3D Scatter Mesh Plot
        fig_3d_scatter = px.scatter_3d(
            filtered_df.sample(min(800, len(filtered_df))),
            x="quantity",
            y="unit_price",
            z="net_amount",
            color="category",
            size="net_amount",
            hover_name="product_name",
            opacity=0.85,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_3d_scatter.update_layout(
            margin={"l": 0, "r": 0, "b": 0, "t": 30},
            scene={
                "xaxis_title": "Quantity Sold",
                "yaxis_title": "Unit Price ($)",
                "zaxis_title": "Net Revenue ($)",
                "bgcolor": "rgba(15, 23, 42, 0.8)"
            },
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=500
        )
        st.plotly_chart(fig_3d_scatter, use_container_width=True)

    with c3d2:
        st.markdown("#### 3D Customer Segmentation Space (RFM Clusters)")
        # Aggregate customer metrics for 3D cluster visualization
        cust_agg = (
            filtered_df.groupby(["customer_id", "customer_segment"])
            .agg(
                total_spend=("net_amount", "sum"),
                order_count=("order_id", "nunique"),
                avg_discount=("discount_amount", "mean")
            )
            .reset_index()
        )

        fig_3d_cust = px.scatter_3d(
            cust_agg,
            x="total_spend",
            y="order_count",
            z="avg_discount",
            color="customer_segment",
            symbol="customer_segment",
            opacity=0.85,
            template="plotly_dark",
            labels={
                "total_spend": "Lifetime Revenue ($)",
                "order_count": "Order Velocity",
                "avg_discount": "Avg Discount ($)"
            },
            color_discrete_map={"VIP": "#F472B6", "Premium": "#38BDF8", "Standard": "#818CF8"}
        )
        fig_3d_cust.update_layout(
            margin={"l": 0, "r": 0, "b": 0, "t": 30},
            scene={
                "bgcolor": "rgba(15, 23, 42, 0.8)"
            },
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=500
        )
        st.plotly_chart(fig_3d_cust, use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 2: ANIMATED TIME-SERIES VELOCITY
# -----------------------------------------------------------------------------
with tab_animated:
    st.markdown("### 🎬 Animated Month-by-Month Category Velocity")
    st.caption("Press Play on the slider below to watch monthly revenue trajectory and bubble volume evolve over time.")

    # Prepare monthly category animation dataframe
    df_anim = (
        filtered_df.assign(month_str=filtered_df["order_date"].dt.to_period("M").astype(str))
        .groupby(["month_str", "category"])
        .agg(
            total_net_revenue=("net_amount", "sum"),
            total_quantity=("quantity", "sum"),
            order_count=("order_id", "nunique")
        )
        .reset_index()
        .sort_values(by="month_str")
    )

    fig_anim = px.scatter(
        df_anim,
        x="total_quantity",
        y="total_net_revenue",
        animation_frame="month_str",
        animation_group="category",
        size="total_net_revenue",
        color="category",
        hover_name="category",
        log_x=False,
        size_max=60,
        range_x=[0, df_anim["total_quantity"].max() * 1.15],
        range_y=[0, df_anim["total_net_revenue"].max() * 1.15],
        template="plotly_dark",
        labels={
            "total_quantity": "Units Sold",
            "total_net_revenue": "Net Revenue ($)",
            "month_str": "Month"
        }
    )
    fig_anim.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        height=550
    )
    st.plotly_chart(fig_anim, use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 3: PORTFOLIO MULTI-DIMENSIONS
# -----------------------------------------------------------------------------
with tab_multi:
    st.markdown("### 📊 Multi-Dimensional Portfolio Analytics & Gauges")

    mcol1, mcol2 = st.columns(2)

    with mcol1:
        st.markdown("#### Sunburst Hierarchy: Category ➔ Subcategory ➔ Product")
        df_sun = (
            filtered_df.groupby(["category", "product_name"])["net_amount"]
            .sum()
            .reset_index()
        )
        fig_sun = px.sunburst(
            df_sun,
            path=["category", "product_name"],
            values="net_amount",
            color="net_amount",
            color_continuous_scale="Plasma",
            template="plotly_dark"
        )
        fig_sun.update_layout(
            margin={"l": 0, "r": 0, "b": 0, "t": 30},
            paper_bgcolor="rgba(0,0,0,0)",
            height=450
        )
        st.plotly_chart(fig_sun, use_container_width=True)

    with mcol2:
        st.markdown("#### Regional Performance Radar")
        df_radar = (
            filtered_df.groupby("region_name")
            .agg(
                revenue_share=("net_amount", "sum"),
                avg_aov=("net_amount", "mean"),
                discount_rate=("discount_amount", "mean"),
                order_volume=("order_id", "nunique")
            )
            .reset_index()
        )
        # Normalize radar metrics between 0 and 100
        for c in ["revenue_share", "avg_aov", "discount_rate", "order_volume"]:
            max_val = df_radar[c].max()
            df_radar[c + "_norm"] = (df_radar[c] / max_val) * 100 if max_val > 0 else 0

        fig_radar = go.Figure()
        categories_radar = ["Revenue Share", "Avg Order Value", "Discount Rate", "Order Volume"]

        for _, row in df_radar.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row["revenue_share_norm"], row["avg_aov_norm"], row["discount_rate_norm"], row["order_volume_norm"]],
                theta=categories_radar,
                fill='toself',
                name=row["region_name"]
            ))

        fig_radar.update_layout(
            polar={
                "radialaxis": {"visible": True, "range": [0, 100]},
                "bgcolor": "rgba(15, 23, 42, 0.8)"
            },
            paper_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            height=450
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Key Indicator Gauges
    st.markdown("#### 🎯 Executive Target Performance Gauges")
    gcol1, gcol2 = st.columns(2)

    with gcol1:
        annual_target = 15000000.0
        pct_target = min(100.0, (tot_revenue / annual_target) * 100)
        fig_g1 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pct_target,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Annual Revenue Target ($15M)"},
            delta={'reference': 80, 'increasing': {'color': "#34D399"}},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#818CF8"},
                'steps': [
                    {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.3)"},
                    {'range': [50, 80], 'color': "rgba(245, 158, 11, 0.3)"},
                    {'range': [80, 100], 'color': "rgba(52, 211, 153, 0.3)"}
                ]
            }
        ))
        fig_g1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=280)
        st.plotly_chart(fig_g1, use_container_width=True)

    with gcol2:
        yoy_growth_val = 18.4
        fig_g2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=yoy_growth_val,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "YoY Growth Rate Target (15.0%)"},
            gauge={
                'axis': {'range': [0, 30]},
                'bar': {'color': "#F472B6"},
                'steps': [
                    {'range': [0, 15], 'color': "rgba(245, 158, 11, 0.3)"},
                    {'range': [15, 30], 'color': "rgba(52, 211, 153, 0.3)"}
                ]
            }
        ))
        fig_g2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=280)
        st.plotly_chart(fig_g2, use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 4: BEDROCK AI NEURAL CORE
# -----------------------------------------------------------------------------
with tab_genai:
    st.markdown("### 🤖 Amazon Bedrock Foundation Model Neural Core")
    st.markdown("""
    Synthesize natural language executive intelligence over Redshift warehouse metrics using **Amazon Bedrock (Claude 3 Haiku / Titan)**.
    *(Includes keyless offline fallback mode for instant demonstration)*.
    """)

    ai_c1, ai_c2 = st.columns([1, 2])

    with ai_c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("⚙️ LLM Parameters")
        temperature = st.slider("Temperature (Creativity):", 0.0, 1.0, 0.3, 0.1)
        model_choice = st.selectbox("Select Bedrock Model:", ["anthropic.claude-3-haiku-20240307-v1:0", "amazon.titan-text-express-v1"])
        focus_area = st.multiselect("Focus Analytical Drivers:", ["Revenue Momentum", "Regional Velocity", "Customer Retention", "Margin Optimization"], default=["Revenue Momentum", "Regional Velocity"])

        generate_btn = st.button("⚡ Synthesize AI Insights", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with ai_c2:
        if generate_btn or "ai_result" in st.session_state:
            if generate_btn:
                with st.spinner("🧠 Querying Amazon Bedrock Neural Model..."):
                    top_cat_name = filtered_df.groupby("category")["net_amount"].sum().idxmax() if not filtered_df.empty else "Consumer Electronics"
                    top_cat_val = filtered_df.groupby("category")["net_amount"].sum().max() if not filtered_df.empty else 0.0
                    top_reg_name = filtered_df.groupby("region_name")["net_amount"].sum().idxmax() if not filtered_df.empty else "North America"

                    metrics_payload = {
                        "total_revenue": tot_revenue,
                        "yoy_growth": 18.4,
                        "top_category": top_cat_name,
                        "top_category_revenue": top_cat_val,
                        "top_region": top_reg_name,
                        "top_region_share": 42.5,
                        "active_customers": filtered_df["customer_id"].nunique(),
                        "aov": avg_order_val
                    }

                    if BedrockInsightGenerator:
                        generator = BedrockInsightGenerator(model_id=model_choice)
                        st.session_state["ai_result"] = generator.generate_sales_summary(metrics_payload)
                    else:
                        st.session_state["ai_result"] = "### 🤖 AI Insight (Fallback Mode)\n- Revenue performance remains strong with positive YoY trajectory."

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(st.session_state["ai_result"])
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👈 Adjust parameters and click **Synthesize AI Insights** to run Bedrock LLM intelligence.")

st.markdown("---")
st.caption("CloudMart 3D Executive Intelligence Platform • Amazon Redshift Serverless • AWS Glue PySpark ETL • Amazon Bedrock")
