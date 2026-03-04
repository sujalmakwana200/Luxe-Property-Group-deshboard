import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. Page Configuration
st.set_page_config(
    page_title="Luxe Property Group | Sales Analytics",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Mock Data Generator (Runs if no file is uploaded)
@st.cache_data
def load_data():
    np.random.seed(42)
    data = {
        'Property_ID': range(1001, 1201),
        'Property Type': np.random.choice(["Villa", "Penthouse", "Apartment", "Townhouse"], 200),
        'Price': np.random.randint(500000, 5000000, 200),
        'Days on Market': np.random.randint(5, 90, 200),
        'Latitude': np.random.uniform(47.5, 47.7, 200),
        'Longitude': np.random.uniform(-122.4, -122.2, 200)
    }
    return pd.DataFrame(data)

# 3. Main Title and Description
st.title("🏘️ Luxe Property Group: Sales Dashboard")
st.markdown("Interactive analysis of premium property sales, market trends, and geographic pricing for business stakeholders.")
st.divider()

# 4. Sidebar Setup & File Uploader
st.sidebar.header("Executive Filters")
st.sidebar.markdown("Use these filters to drill down into specific market segments.")

# This is the new file uploader logic
uploaded_file = st.sidebar.file_uploader("Upload Real Estate Data (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File uploaded successfully!")
else:
    df = load_data()
    st.sidebar.info("Using mock data. Upload a CSV to see your own data.")

# 5. Dynamic Filters
price_range = st.sidebar.slider("Select Price Range ($)", min_value=0, max_value=5000000, value=(500000, 2000000))
property_type = st.sidebar.multiselect("Property Type", ["Villa", "Penthouse", "Apartment", "Townhouse"], default=["Villa", "Penthouse"])

# 6. Apply Filters & Render Visuals (Wrapped in a try/except to prevent crashes on bad CSVs)
try:
    filtered_df = df[
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1]) &
        (df['Property Type'].isin(property_type))
    ]
    
    # KPI Metrics
    st.subheader("Market Snapshot")
    col1, col2, col3, col4 = st.columns(4)

    total_volume = filtered_df['Price'].sum()
    avg_price = filtered_df['Price'].mean() if not filtered_df.empty else 0
    total_sold = len(filtered_df)
    avg_days = filtered_df['Days on Market'].mean() if not filtered_df.empty else 0

    with col1:
        st.metric(label="Total Sales Volume", value=f"${total_volume:,.0f}")
    with col2:
        st.metric(label="Average Sale Price", value=f"${avg_price:,.0f}")
    with col3:
        st.metric(label="Properties Sold", value=total_sold)
    with col4:
        st.metric(label="Avg Days on Market", value=f"{avg_days:.0f} Days")
        
    st.divider()

    # Data Visualizations
    col_map, col_chart = st.columns([2, 1])

    with col_map:
        st.subheader("Geographic Price Distribution")
        if not filtered_df.empty:
            fig_map = px.scatter_mapbox(
                filtered_df, lat="Latitude", lon="Longitude", color="Price", size="Price",
                color_continuous_scale=px.colors.sequential.Viridis, size_max=15, zoom=10,
                mapbox_style="carto-positron", hover_name="Property Type"
            )
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("No properties match the selected filters.")
                
    with col_chart:
        st.subheader("Sales by Property Type")
        if not filtered_df.empty:
            fig_bar = px.bar(
                filtered_df.groupby('Property Type')['Price'].sum().reset_index(),
                x='Property Type', y='Price', color='Property Type'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("No data to display.")

except KeyError:
    # This catches the error if an uploaded CSV doesn't have the exact column names we expect
    st.error("⚠️ The uploaded CSV must contain exactly these columns: 'Price', 'Property Type', 'Days on Market', 'Latitude', 'Longitude'. Please clear the file to return to mock data.")
