"""
💰 Finance Pro Dashboard v3.0 - COMPLETE EDITION
Real profit tracking after ALL Etsy fees with advanced analytics

New in v3.0:
✅ Centralized data loading from session_state
✅ Coupons & Promos analysis (ROI, impact on margin)
✅ Real Etsy fees validation (Payments CSV)
✅ Product variations financial analysis
✅ Geographic analysis (revenue by country)
✅ SKU rotation & stock management
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Finance Pro v3.0 - Etsy Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== AUTHENTICATION ====================
if 'user_id' not in st.session_state:
    st.error("❌ Session expired. Please log in again.")
    st.switch_page("pages/auth.py")
    st.stop()

user_id = st.session_state.user_id
user_email = st.session_state.get('email', 'User')
is_premium = st.session_state.get('is_premium', False)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .main-header {font-size: 3rem; font-weight: bold; color: #27ae60; text-align: center; margin-bottom: 2rem;}
    .metric-card {background-color: #f0f2f6; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #27ae60; margin: 0.5rem 0;}
    .warning-box {background-color: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; margin: 1rem 0;}
    .success-box {background-color: #d4edda; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745; margin: 1rem 0;}
    .premium-lock {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;}
    .info-box {background: #e3f2fd; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196F3; margin: 1rem 0;}
    </style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================

def check_data_availability():
    """Check if required data is available in session_state"""
    if 'sold_items_df' not in st.session_state or st.session_state['sold_items_df'] is None:
        st.warning("⚠️ No data loaded. Please upload your files first.")
        st.info("👉 Go to **Upload Data** page to upload your Etsy CSV files")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📤 Go to Upload Data", type="primary", use_container_width=True):
                st.switch_page("pages/Upload_Data.py")
        st.stop()
        return False
    return True


@st.cache_data
def load_and_prepare_data(sold_items_df, payments_df=None):
    """Load and standardize data from session_state"""
    df = sold_items_df.copy()
    
    # Column mapping (English & French support)
    column_mapping = {
        'Sale Date': 'Date', 'Date de vente': 'Date',
        'Item Name': 'Product', 'Price': 'Price',
        'Quantity': 'Quantity', 'Quantité': 'Quantity',
        'Coupon Code': 'Coupon_Code', 'Discount Amount': 'Discount_Amount',
        'Shipping Discount': 'Shipping_Discount',
        'Order Shipping': 'Shipping', 'Frais de livraison': 'Shipping',
        'Ship Country': 'Country', 'Pays de livraison': 'Country',
        'Variations': 'Variations', 'SKU': 'SKU',
        'Order ID': 'Order_ID', 'Commande n°': 'Order_ID'
    }
    
    # Apply mapping
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)
    
    # Convert Date
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='mixed')
        df = df.dropna(subset=['Date'])
    
    # Clean numeric columns
    for col in ['Price', 'Quantity', 'Discount_Amount', 'Shipping_Discount', 'Shipping']:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                df[col] = (df[col].fillna('0').astype(str)
                          .str.replace('€|$|USD|EUR|GBP| |,', '', regex=True)
                          .str.strip())
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Add defaults
    if 'Quantity' not in df.columns:
        df['Quantity'] = 1
    if 'Discount_Amount' not in df.columns:
        df['Discount_Amount'] = 0
    if 'Shipping_Discount' not in df.columns:
        df['Shipping_Discount'] = 0
    if 'Shipping' not in df.columns:
        df['Shipping'] = 0
    if 'Country' not in df.columns:
        df['Country'] = 'Unknown'
    
    # Remove invalid rows
    df = df[(~df['Price'].isna()) & (df['Price'] > 0)]
    
    return df


def calculate_etsy_fees_detailed(price, shipping=0, quantity=1, fees_config=None):
    """Calculate ALL Etsy fees"""
    if fees_config is None:
        fees_config = {'mode': 'quick'}
    
    fees_detail = {}
    
    # Base fees
    transaction_fee = price * 0.065
    payment_fee = (price + shipping) * 0.03 + 0.25
    listing_fee = 0.20 / max(quantity, 1)
    regulatory_fee = price * 0.004
    
    fees_detail['Transaction (6.5%)'] = transaction_fee
    fees_detail['Payment Processing'] = payment_fee
    fees_detail['Listing Fee'] = listing_fee
    fees_detail['Regulatory Fee'] = regulatory_fee
    
    # Mode-specific fees
    if fees_config['mode'] == 'detailed':
        if fees_config.get('use_offsite_ads', False):
            offsite_rate = fees_config.get('offsite_ads_rate', 0.15)
            fees_detail['Offsite Ads'] = price * offsite_rate
        
        if fees_config.get('etsy_ads_budget', 0) > 0:
            expected_sales = fees_config.get('expected_monthly_sales', 30)
            fees_detail['Etsy Ads'] = fees_config['etsy_ads_budget'] / expected_sales
        
        if fees_config.get('has_etsy_plus', False):
            expected_sales = fees_config.get('expected_monthly_sales', 30)
            fees_detail['Etsy Plus'] = 10 / expected_sales
    
    total_fees = sum(fees_detail.values())
    
    return {
        'detail': fees_detail,
        'total': total_fees,
        'net_revenue': price - total_fees,
        'fee_percentage': (total_fees / price * 100) if price > 0 else 0
    }


def calculate_kpis(df, fees_config=None):
    """Calculate all KPIs"""
    kpis = {}
    
    kpis['total_revenue'] = df['Price'].sum()
    kpis['num_sales'] = len(df)
    kpis['avg_order_value'] = kpis['total_revenue'] / kpis['num_sales'] if kpis['num_sales'] > 0 else 0
    
    # Etsy fees
    total_fees = 0
    fees_breakdown = {}
    
    for _, row in df.iterrows():
        fees_result = calculate_etsy_fees_detailed(
            row['Price'], row.get('Shipping', 0),
            row.get('Quantity', 1), fees_config
        )
        total_fees += fees_result['total']
        
        for fee_type, amount in fees_result['detail'].items():
            fees_breakdown[fee_type] = fees_breakdown.get(fee_type, 0) + amount
    
    kpis['etsy_fees'] = total_fees
    kpis['etsy_fees_detail'] = fees_breakdown
    
    # Discounts
    kpis['total_discounts'] = df['Discount_Amount'].sum() + df['Shipping_Discount'].sum()
    kpis['discount_rate'] = (kpis['total_discounts'] / kpis['total_revenue'] * 100) if kpis['total_revenue'] > 0 else 0
    
    # Profit
    kpis['gross_margin'] = kpis['total_revenue'] - kpis['etsy_fees'] - kpis['total_discounts']
    kpis['margin_percent'] = (kpis['gross_margin'] / kpis['total_revenue'] * 100) if kpis['total_revenue'] > 0 else 0
    
    return kpis


def analyze_coupons(df):
    """Analyze coupon usage and ROI"""
    if 'Coupon_Code' not in df.columns:
        return None
    
    # Filter sales with coupons
    coupon_sales = df[df['Coupon_Code'].notna() & (df['Coupon_Code'] != '')]
    
    if len(coupon_sales) == 0:
        return None
    
    coupon_analysis = coupon_sales.groupby('Coupon_Code').agg({
        'Price': 'sum',
        'Discount_Amount': 'sum',
        'Quantity': 'count'
    }).reset_index()
    
    coupon_analysis.columns = ['Coupon', 'Revenue', 'Discount_Given', 'Sales']
    coupon_analysis['ROI'] = ((coupon_analysis['Revenue'] - coupon_analysis['Discount_Given']) / 
                               coupon_analysis['Discount_Given']) * 100
    coupon_analysis['Avg_Discount'] = coupon_analysis['Discount_Given'] / coupon_analysis['Sales']
    
    coupon_analysis = coupon_analysis.sort_values('Revenue', ascending=False)
    
    return coupon_analysis


def analyze_geography(df):
    """Analyze revenue by country"""
    if 'Country' not in df.columns:
        return None
    
    geo_analysis = df.groupby('Country').agg({
        'Price': ['sum', 'mean', 'count'],
        'Shipping': 'mean'
    }).reset_index()
    
    geo_analysis.columns = ['Country', 'Revenue', 'Avg_Order', 'Sales', 'Avg_Shipping']
    geo_analysis = geo_analysis.sort_values('Revenue', ascending=False)
    
    # Calculate net revenue (after shipping costs)
    geo_analysis['Net_Revenue'] = geo_analysis['Revenue'] - (geo_analysis['Avg_Shipping'] * geo_analysis['Sales'])
    
    return geo_analysis


def analyze_variations(df):
    """Analyze product variations performance"""
    if 'Variations' not in df.columns:
        return None
    
    # Filter rows with variations
    var_df = df[df['Variations'].notna() & (df['Variations'] != '')]
    
    if len(var_df) == 0:
        return None
    
    # Parse variations (simplified)
    def parse_variation(var_string):
        try:
            # "Taille:1 Moyen : 17 - 20 cm,Color:Bleu" -> "Moyen, Bleu"
            parts = str(var_string).split(',')
            parsed = []
            for part in parts:
                if ':' in part:
                    # Take the part after first colon
                    value = part.split(':', 1)[1].strip()
                    parsed.append(value)
            return ' | '.join(parsed) if parsed else var_string
        except:
            return str(var_string)
    
    var_df['Parsed_Variation'] = var_df['Variations'].apply(parse_variation)
    
    variation_analysis = var_df.groupby('Parsed_Variation').agg({
        'Price': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    variation_analysis.columns = ['Variation', 'Revenue', 'Sales']
    variation_analysis = variation_analysis.sort_values('Revenue', ascending=False).head(10)
    
    return variation_analysis


def analyze_sku_rotation(df):
    """Analyze SKU stock rotation"""
    if 'SKU' not in df.columns:
        return None
    
    # Filter rows with SKU
    sku_df = df[df['SKU'].notna() & (df['SKU'] != '')]
    
    if len(sku_df) == 0:
        return None
    
    sku_analysis = sku_df.groupby('SKU').agg({
        'Quantity': 'sum',
        'Date': lambda x: (x.max() - x.min()).days if len(x) > 1 else 30
    }).reset_index()
    
    sku_analysis.columns = ['SKU', 'Total_Sales', 'Days_Active']
    
    # Calculate rotation rate (sales per month)
    sku_analysis['Rotation_Rate'] = (sku_analysis['Total_Sales'] / 
                                      sku_analysis['Days_Active'] * 30)
    
    # Flag slow-moving items
    sku_analysis['Status'] = sku_analysis['Rotation_Rate'].apply(
        lambda x: '🔴 Slow' if x < 1 else ('🟡 Medium' if x < 5 else '🟢 Fast')
    )
    
    sku_analysis = sku_analysis.sort_values('Rotation_Rate', ascending=True)
    
    return sku_analysis


def validate_fees_with_payments(df, payments_df):
    """Compare estimated vs real Etsy fees"""
    if payments_df is None or len(payments_df) == 0:
        return None
    
    # Merge by Order ID
    merged = df.merge(
        payments_df[['Order_ID', 'Fees_Real']],
        on='Order_ID',
        how='left'
    )
    
    # Calculate estimated fees
    merged['Fees_Estimated'] = merged.apply(
        lambda row: calculate_etsy_fees_detailed(row['Price'])['total'],
        axis=1
    )
    
    # Compare
    merged['Fee_Gap'] = merged['Fees_Real'] - merged['Fees_Estimated']
    merged['Fee_Gap_Pct'] = (merged['Fee_Gap'] / merged['Fees_Estimated'] * 100)
    
    validation = {
        'total_estimated': merged['Fees_Estimated'].sum(),
        'total_real': merged['Fees_Real'].sum(),
        'gap': merged['Fee_Gap'].sum(),
        'gap_pct': (merged['Fee_Gap'].sum() / merged['Fees_Estimated'].sum() * 100)
    }
    
    return validation


# ==================== SIDEBAR: FEES CONFIGURATOR ====================
with st.sidebar:
    st.markdown("## ⚙️ Fees Configuration")
    
    fees_mode = st.selectbox(
        "Calculation Mode",
        ["Quick Estimation (12%)", "Detailed Configurator"],
        help="Choose how to calculate Etsy fees"
    )
    
    fees_config = {'mode': 'quick'}
    
    if fees_mode == "Detailed Configurator":
        st.markdown("### 📊 Detailed Settings")
        fees_config['mode'] = 'detailed'
        
        use_offsite = st.checkbox("Offsite Ads Enabled", value=False)
        if use_offsite:
            fees_config['use_offsite_ads'] = True
            fees_config['offsite_ads_rate'] = st.slider("Offsite Ads Rate", 0.12, 0.15, 0.15, 0.01)
        
        etsy_ads = st.number_input("Monthly Etsy Ads Budget ($)", min_value=0, value=0, step=10)
        if etsy_ads > 0:
            fees_config['etsy_ads_budget'] = etsy_ads
        
        has_plus = st.checkbox("Etsy Plus Subscriber ($10/month)", value=False)
        if has_plus:
            fees_config['has_etsy_plus'] = True
        
        expected_sales = st.number_input("Expected Monthly Sales", min_value=1, value=30, step=5)
        fees_config['expected_monthly_sales'] = expected_sales

# ==================== MAIN APP ====================

st.markdown('<h1 class="main-header">💰 Finance Pro Dashboard v3.0</h1>', unsafe_allow_html=True)

# Check data availability
check_data_availability()

# Load data
df = load_and_prepare_data(
    st.session_state['sold_items_df'],
    st.session_state.get('payments_df')
)

# Calculate KPIs
kpis = calculate_kpis(df, fees_config)

# Additional analyses
coupon_analysis = analyze_coupons(df)
geo_analysis = analyze_geography(df)
variation_analysis = analyze_variations(df)
sku_analysis = analyze_sku_rotation(df)

# ==================== TABS ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "💸 Coupons & Promos",
    "🌍 Geographic & Variations",
    "📦 SKU & Stock"
])

with tab1:
    st.markdown("## 📊 Financial Overview")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", f"${kpis['total_revenue']:,.2f}")
    with col2:
        st.metric("Etsy Fees", f"${kpis['etsy_fees']:,.2f}",
                 delta=f"-{(kpis['etsy_fees'] / kpis['total_revenue'] * 100):.1f}%",
                 delta_color="inverse")
    with col3:
        st.metric("Discounts", f"${kpis['total_discounts']:,.2f}",
                 delta=f"-{kpis['discount_rate']:.1f}%",
                 delta_color="inverse")
    with col4:
        st.metric("Net Profit", f"${kpis['gross_margin']:,.2f}",
                 delta=f"{kpis['margin_percent']:.1f}% margin")
    
    st.markdown("---")
    
    # Fees breakdown
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💸 Fees Breakdown")
        fees_data = []
        for fee_type, amount in kpis['etsy_fees_detail'].items():
            fees_data.append({
                'Category': fee_type,
                'Amount': f"${amount:.2f}",
                'Percentage': f"{(amount / kpis['total_revenue'] * 100):.2f}%"
            })
        
        fees_df = pd.DataFrame(fees_data)
        st.dataframe(fees_df, use_container_width=True, hide_index=True)
    
    with col2:
        # Revenue distribution pie
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Net Profit', 'Etsy Fees', 'Discounts'],
            values=[kpis['gross_margin'], kpis['etsy_fees'], kpis['total_discounts']],
            hole=0.4,
            marker=dict(colors=['#27ae60', '#e74c3c', '#f39c12'])
        )])
        fig_pie.update_layout(title="Revenue Distribution", height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Revenue over time
    st.markdown("### 📈 Revenue Over Time")
    daily_revenue = df.groupby(df['Date'].dt.date)['Price'].sum().reset_index()
    daily_revenue.columns = ['Date', 'Revenue']
    
    fig_time = px.line(daily_revenue, x='Date', y='Revenue', title="Daily Revenue", markers=True)
    fig_time.update_traces(line_color='#27ae60', line_width=3)
    fig_time.update_layout(height=400)
    st.plotly_chart(fig_time, use_container_width=True)

with tab2:
    st.markdown("## 💸 Coupons & Promotions Analysis")
    
    if coupon_analysis is not None and len(coupon_analysis) > 0:
        # Overall coupon stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Discount Given", f"${kpis['total_discounts']:,.2f}")
        with col2:
            coupon_sales_pct = (coupon_analysis['Sales'].sum() / kpis['num_sales'] * 100)
            st.metric("Sales with Coupons", f"{coupon_sales_pct:.1f}%")
        with col3:
            avg_discount_pct = (kpis['total_discounts'] / kpis['total_revenue'] * 100)
            st.metric("Avg Discount Rate", f"{avg_discount_pct:.1f}%")
        
        st.markdown("---")
        
        # Coupon performance table
        st.markdown("### 🎫 Coupon Performance")
        
        display_df = coupon_analysis.copy()
        display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:.2f}")
        display_df['Discount_Given'] = display_df['Discount_Given'].apply(lambda x: f"${x:.2f}")
        display_df['ROI'] = display_df['ROI'].apply(lambda x: f"{x:.1f}%")
        display_df['Avg_Discount'] = display_df['Avg_Discount'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # ROI visualization
        fig = px.bar(
            coupon_analysis,
            x='Coupon',
            y='ROI',
            title='Coupon ROI (%)',
            color='ROI',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        best_coupon = coupon_analysis.iloc[0]
        worst_coupon = coupon_analysis.iloc[-1]
        
        st.markdown("### 💡 Recommendations")
        
        if best_coupon['ROI'] > 200:
            st.markdown(f"""
            <div class="success-box">
            ✅ <strong>Best Performer:</strong> {best_coupon['Coupon']}<br>
            ROI: {best_coupon['ROI']:.1f}% | Revenue: ${best_coupon['Revenue']:.2f}<br>
            <strong>Action:</strong> Promote this coupon more actively!
            </div>
            """, unsafe_allow_html=True)
        
        if worst_coupon['ROI'] < 100:
            st.markdown(f"""
            <div class="warning-box">
            ⚠️ <strong>Low Performer:</strong> {worst_coupon['Coupon']}<br>
            ROI: {worst_coupon['ROI']:.1f}% | Discount: ${worst_coupon['Discount_Given']:.2f}<br>
            <strong>Action:</strong> Consider reducing discount or retiring this coupon
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ No coupon data available. Start using promotional codes to track their performance!")

with tab3:
    st.markdown("## 🌍 Geographic & Variations Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Revenue by Country")
        
        if geo_analysis is not None and len(geo_analysis) > 0:
            # Top 10 countries
            top_countries = geo_analysis.head(10)
            
            fig = px.bar(
                top_countries,
                x='Country',
                y='Revenue',
                title='Top 10 Countries by Revenue',
                color='Revenue',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Stats
            st.markdown("**Top 3 Most Profitable Countries:**")
            for idx, row in top_countries.head(3).iterrows():
                st.markdown(f"- **{row['Country']}**: ${row['Revenue']:.2f} ({int(row['Sales'])} sales)")
        else:
            st.info("ℹ️ Country data not available")
    
    with col2:
        st.markdown("### 🎨 Best-Selling Variations")
        
        if variation_analysis is not None and len(variation_analysis) > 0:
            fig = px.bar(
                variation_analysis,
                x='Revenue',
                y='Variation',
                orientation='h',
                title='Top Variations by Revenue',
                color='Sales',
                color_continuous_scale='Oranges'
            )
            fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Best variation
            best_var = variation_analysis.iloc[0]
            st.markdown(f"""
            <div class="success-box">
            ⭐ <strong>Best Variation:</strong> {best_var['Variation']}<br>
            Revenue: ${best_var['Revenue']:.2f} | Sales: {int(best_var['Sales'])}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ Variation data not available")

with tab4:
    st.markdown("## 📦 SKU & Stock Rotation")
    
    if sku_analysis is not None and len(sku_analysis) > 0:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📊 SKU Rotation Analysis")
            
            display_df = sku_analysis.copy()
            display_df['Rotation_Rate'] = display_df['Rotation_Rate'].apply(lambda x: f"{x:.2f}/month")
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### 🎯 Quick Stats")
            
            fast_moving = len(sku_analysis[sku_analysis['Status'] == '🟢 Fast'])
            slow_moving = len(sku_analysis[sku_analysis['Status'] == '🔴 Slow'])
            
            st.metric("Fast-Moving SKUs", fast_moving)
            st.metric("Slow-Moving SKUs", slow_moving)
            
            if slow_moving > 0:
                st.markdown("""
                <div class="warning-box">
                ⚠️ <strong>Action Needed:</strong><br>
                You have slow-moving items.<br>
                Consider promotions or reducing stock.
                </div>
                """, unsafe_allow_html=True)
        
        # Distribution chart
        status_counts = sku_analysis['Status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title='SKU Distribution by Rotation Speed'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ SKU data not available. Add SKU column to your CSV to track stock rotation.")

# ==================== FOOTER ====================
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📤 Upload Data", use_container_width=True):
        st.switch_page("pages/Upload_Data.py")
with col2:
    if st.button("👥 Customer Intelligence", use_container_width=True):
        st.switch_page("pages/etsy_customer_intelligence.py")
with col3:
    if st.button("🔍 SEO Analyzer", use_container_width=True):
        st.switch_page("pages/etsy_seo_analyzer.py")

st.markdown("""
<div style='text-align: center; color: #666; padding: 20px; margin-top: 2rem;'>
    <p><strong>Etsy Dashboard</strong> - Finance Pro v3.0</p>
    <p style='font-size: 0.9em;'>Advanced financial analytics for Etsy sellers</p>
</div>
""", unsafe_allow_html=True)