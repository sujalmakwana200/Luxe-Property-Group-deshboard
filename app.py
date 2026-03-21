import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts, JsCode
import pydeck as pdk
import gc

st.set_page_config(page_title="Luxe Property | Sales Analytics", layout="wide")

hide_streamlit_style = """
            <style>
            [data-testid="stAppViewContainer"] { background-color: #000000; }
            [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            div[data-testid="metric-container"] {
                background-color: #0A0A0A;
                border-radius: 8px;
                padding: 15px;
                border-left: 2px solid #B8860B;
                border-top: 1px solid #222222;
                border-bottom: 1px solid #222222;
                border-right: 1px solid #222222;
                box-shadow: 0 4px 6px rgba(0,0,0,0.5);
            }
            p, h1, h2, h3, h4, h5, h6, label { color: #FFFFFF !important; }
            .stSlider [role="slider"] {
                background-color: #B8860B !important; 
                border: 2px solid #E5C158 !important; 
                box-shadow: 0 0 10px rgba(184, 134, 11, 0.4) !important;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

@st.cache_data
def load_data():
    np.random.seed(42)
    data = {
        'Property_ID': range(1001, 1601),
        'Property Type': np.random.choice(["Villa", "Penthouse", "Apartment", "Townhouse"], 600),
        'Price': np.random.randint(500000, 25000000, 600),
        'Days on Market': np.random.randint(5, 120, 600),
        'Latitude': np.random.uniform(40.70, 40.80, 600),
        'Longitude': np.random.uniform(-74.02, -73.94, 600)
    }
    return pd.DataFrame(data)

st.title("LUXE PROPERTY GROUP")
st.markdown("Global Asset Portfolio & Transaction Intelligence Suite.")

uploaded_file = st.file_uploader("Upload Real Estate Data (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data()

with st.form("portfolio_form"):
    ctrl1, ctrl2 = st.columns(2)
    with ctrl1:
        price_range = st.slider("Select Price Range ($)", min_value=0, max_value=25000000, value=(500000, 25000000))
    with ctrl2:
        property_type = st.multiselect("Property Type", ["Villa", "Penthouse", "Apartment", "Townhouse"], default=["Villa", "Penthouse", "Apartment", "Townhouse"])
    
    submit_sync = st.form_submit_button("Initiate Portfolio Sync")

st.divider()

if submit_sync:
    st.session_state['sync_active'] = True
    st.session_state['price_range'] = price_range
    st.session_state['property_type'] = property_type
    gc.collect()

if st.session_state.get('sync_active', False):
    try:
        filtered_df = df[
            (df['Price'] >= st.session_state['price_range'][0]) &
            (df['Price'] <= st.session_state['price_range'][1]) &
            (df['Property Type'].isin(st.session_state['property_type']))
        ].copy()
        
        col1, col2, col3, col4 = st.columns(4)

        total_volume = filtered_df['Price'].sum()
        avg_price = filtered_df['Price'].mean() if not filtered_df.empty else 0
        total_assets = len(filtered_df)
        avg_days = filtered_df['Days on Market'].mean() if not filtered_df.empty else 0

        with col1:
            st.metric(label="Total Portfolio Volume", value=f"${total_volume/1_000_000_000:,.2f}B" if total_volume >= 1e9 else f"${total_volume/1_000_000:,.1f}M")
        with col2:
            st.metric(label="Average Asset Price", value=f"${avg_price/1_000_000:,.1f}M")
        with col3:
            st.metric(label="Assets in View", value=total_assets)
        with col4:
            st.metric(label="Avg Days on Market", value=f"{avg_days:.0f} Days")
            
        st.divider()

        map_col, chart_col = st.columns([2, 1])

        with map_col:
            st.subheader("Geographic Asset Distribution")
            if not filtered_df.empty:
                color_map = {"Penthouse": [212, 175, 55, 140], "Villa": [192, 192, 192, 140], "Townhouse": [139, 115, 85, 140], "Apartment": [184, 134, 11, 140]}
                filtered_df['color'] = filtered_df['Property Type'].apply(lambda x: color_map.get(x, [100, 100, 100, 140]))
                filtered_df['radius'] = (filtered_df['Price'] / filtered_df['Price'].max()) * 60 + 20

                layer = pdk.Layer("ScatterplotLayer", filtered_df, get_position="[Longitude, Latitude]", get_fill_color="color", get_line_color="[255, 255, 255, 180]", get_radius="radius", stroked=True, line_width_min_pixels=1.2, pickable=True, auto_highlight=True)
                view_state = pdk.ViewState(latitude=filtered_df["Latitude"].mean(), longitude=filtered_df["Longitude"].mean(), zoom=11.5, pitch=45, bearing=15)
                r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="dark", tooltip={"html": "<b>{Property Type}</b>: ${Price}"})
                st.pydeck_chart(r, use_container_width=True)

        with chart_col:
            st.subheader("Capital Allocation by Class")
            if not filtered_df.empty:
                type_vol = filtered_df.groupby('Property Type')['Price'].sum().reset_index().sort_values('Price', ascending=False)
                bar_data = [{"value": int(row['Price']), "itemStyle": {"color": "#B8860B"}} for index, row in type_vol.iterrows()]
                
                formatter_js = JsCode("""
                function(params) {
                    var val = params.value;
                    if (val >= 1000000000) return '$' + (val / 1000000000).toFixed(1) + 'B';
                    if (val >= 1000000) return '$' + (val / 1000000).toFixed(1) + 'M';
                    return '$' + val.toLocaleString();
                }
                """)

                bar_options = {
                    "grid": {"left": "15%", "right": "5%", "bottom": "15%"},
                    "xAxis": {"type": "category", "data": type_vol['Property Type'].tolist(), "axisLabel": {"color": "#FFFFFF"}},
                    "yAxis": {"type": "value", "axisLabel": {"color": "#888"}, "splitLine": {"lineStyle": {"color": "#222222"}}},
                    "series": [{
                        "data": bar_data, "type": "bar", "barWidth": "35%",
                        "label": {"show": True, "position": "top", "color": "#D4AF37", "fontWeight": "bold", "formatter": formatter_js}
                    }]
                }
                # FIXED: Removed allow_js_hash
                st_echarts(options=bar_options, height="450px")

        st.divider()
        
        st.subheader("Market Velocity: Time-to-Sale Metrics")
        if not filtered_df.empty:
            bins = [0, 30, 60, 90, 120, 500]
            labels = ['0-30 Days', '31-60 Days', '61-90 Days', '91-120 Days', '120+ Days']
            filtered_df['Time Category'] = pd.cut(filtered_df['Days on Market'], bins=bins, labels=labels)
            velocity_data = filtered_df.groupby('Time Category', observed=True)['Price'].sum().reset_index()
            v_bar_data = [{"value": int(row['Price']), "itemStyle": {"color": "#B8860B"}} for index, row in velocity_data.iterrows()]
            
            velocity_options = {
                "grid": {"left": "10%", "right": "5%", "bottom": "15%"},
                "xAxis": {"type": "category", "data": velocity_data['Time Category'].tolist(), "axisLabel": {"color": "#FFFFFF"}},
                "yAxis": {"type": "value", "axisLabel": {"color": "#888"}, "splitLine": {"lineStyle": {"color": "#222222"}}},
                "series": [{
                    "data": v_bar_data, "type": "bar", "barWidth": "40%",
                    "label": {"show": True, "position": "top", "color": "#D4AF37", "fontWeight": "bold", "formatter": formatter_js}
                }]
            }
            # FIXED: Removed allow_js_hash
            st_echarts(options=velocity_options, height="400px")
                
    except KeyError as e:
        st.error(f"System Error: Missing column {e}.")
else:
    st.info("System Ready. Upload dataset or configure filters to initiate sync.")
