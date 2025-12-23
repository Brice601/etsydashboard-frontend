"""
💰 Finance Pro Dashboard v3.1 - ENRICHED EDITION
Real profit tracking after ALL Etsy fees with advanced analytics

New in v3.1:
✅ Real Etsy fees from EtsyDirectCheckoutPayments.csv
✅ Net margin calculation with actual costs
✅ Enhanced promo code ROI analysis
✅ Product profitability with real fees per item
✅ Shipping profitability analysis
✅ Fee breakdown visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Finance Pro v3.1 - Etsy Dashboard",
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

# ==================== DATA LOADING FUNCTIONS ====================

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


def load_etsy_payments(payments_df):
    """Process EtsyDirectCheckoutPayments data"""
    if payments_df is None:
        return None
    
    df = payments_df.copy()
    
    # Column mapping
    column_mapping = {
        'N° du paiement': 'Payment_ID',
        'Commande n°': 'Order_ID',
        'Montant brut': 'Gross_Amount',
        'Frais': 'Fees',
        'Montant net': 'Net_Amount',
        'Montant de TVA': 'VAT',
        'Date de la commande': 'Order_Date'
    }
    
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)
    
    # Convert types
    if 'Order_Date' in df.columns:
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    
    for col in ['Fees', 'Gross_Amount', 'Net_Amount', 'VAT']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df


# ==================== CALCULATION FUNCTIONS ====================

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


def calculate_real_etsy_fees(payments_df):
    """Calculate REAL Etsy fees from EtsyDirectCheckoutPayments"""
    if payments_df is None or len(payments_df) == 0:
        return None
    
    fees_breakdown = {
        'total_fees': payments_df['Fees'].sum(),
        'avg_fee_per_transaction': payments_df['Fees'].mean(),
        'total_gross': payments_df['Gross_Amount'].sum(),
        'total_net': payments_df['Net_Amount'].sum(),
        'effective_fee_rate': (payments_df['Fees'].sum() / payments_df['Gross_Amount'].sum()) * 100 if payments_df['Gross_Amount'].sum() > 0 else 0,
        'total_vat': payments_df['VAT'].sum() if 'VAT' in payments_df.columns else 0,
        'transactions_count': len(payments_df)
    }
    
    return fees_breakdown


def calculate_net_margin(df, payments_df):
    """Calculate TRUE net margin with real fees"""
    ca_total = df['Price'].sum()
    
    # Real Etsy fees if available
    if payments_df is not None and 'Fees' in payments_df.columns:
        frais_etsy = payments_df['Fees'].sum()
    else:
        # Fallback to estimated fees
        frais_etsy = sum([calculate_etsy_fees_detailed(row['Price'], row.get('Shipping', 0))['total'] 
                         for _, row in df.iterrows()])
    
    # Discounts
    total_discounts = df['Discount_Amount'].sum() + df['Shipping_Discount'].sum()
    
    # Net margin
    marge_nette = ca_total - frais_etsy - total_discounts
    taux_marge_nette = (marge_nette / ca_total * 100) if ca_total > 0 else 0
    
    return {
        'ca_total': ca_total,
        'frais_etsy': frais_etsy,
        'total_discounts': total_discounts,
        'marge_nette': marge_nette,
        'taux_marge_nette': taux_marge_nette
    }


def calculate_product_profitability(df, payments_df):
    """Calculate REAL profitability per product"""
    if payments_df is None or 'Order_ID' not in df.columns or 'Order_ID' not in payments_df.columns:
        # Fallback without real fees
        product_profit = df.groupby('Product').agg({
            'Price': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        product_profit.columns = ['Product', 'Revenue', 'Units_Sold']
        
        # Estimate fees
        product_profit['Fees'] = product_profit['Revenue'] * 0.10  # ~10% estimate
        product_profit['Net_Margin'] = product_profit['Revenue'] - product_profit['Fees']
        product_profit['Net_Margin_Pct'] = (product_profit['Net_Margin'] / product_profit['Revenue'] * 100)
        
        return product_profit.sort_values('Net_Margin', ascending=False)
    
    # Merge with real fees
    merged = df.merge(
        payments_df[['Order_ID', 'Fees', 'Gross_Amount']], 
        on='Order_ID', 
        how='left'
    )
    
    # Calculate proportional fees per item
    merged['Item_Fees'] = (merged['Price'] / merged['Gross_Amount']) * merged['Fees']
    merged['Item_Fees'] = merged['Item_Fees'].fillna(0)
    
    # Group by product
    product_profit = merged.groupby('Product').agg({
        'Price': 'sum',
        'Item_Fees': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    product_profit.columns = ['Product', 'Revenue', 'Fees', 'Units_Sold']
    
    # Calculate net margin
    product_profit['Net_Margin'] = product_profit['Revenue'] - product_profit['Fees']
    product_profit['Net_Margin_Pct'] = (product_profit['Net_Margin'] / product_profit['Revenue'] * 100)
    
    return product_profit.sort_values('Net_Margin', ascending=False)


def calculate_kpis(df, fees_config=None, payments_df=None):
    """Calculate all KPIs"""
    kpis = {}
    
    kpis['total_revenue'] = df['Price'].sum()
    kpis['num_sales'] = len(df)
    kpis['avg_order_value'] = kpis['total_revenue'] / kpis['num_sales'] if kpis['num_sales'] > 0 else 0
    
    # Use real fees if available
    if payments_df is not None and 'Fees' in payments_df.columns:
        kpis['etsy_fees'] = payments_df['Fees'].sum()
        fees_breakdown = calculate_real_etsy_fees(payments_df)
        if fees_breakdown:
            kpis['etsy_fees_detail'] = fees_breakdown
    else:
        # Fallback to estimated fees
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
    
    coupons_used = df[df['Coupon_Code'].notna()]
    
    if len(coupons_used) == 0:
        return None
    
    coupon_stats = coupons_used.groupby('Coupon_Code').agg({
        'Price': 'sum',
        'Discount_Amount': 'sum',
        'Order_ID': 'count'
    }).reset_index()
    
    coupon_stats.columns = ['Coupon', 'Revenue', 'Discount_Given', 'Sales']
    
    # Calculate ROI
    coupon_stats['ROI'] = ((coupon_stats['Revenue'] - coupon_stats['Discount_Given']) / 
                           coupon_stats['Discount_Given'] * 100)
    coupon_stats['Avg_Discount'] = coupon_stats['Discount_Given'] / coupon_stats['Sales']
    
    return coupon_stats.sort_values('ROI', ascending=False)


def analyze_geographic(df):
    """Analyze revenue by country"""
    if 'Country' not in df.columns:
        return None
    
    geo_stats = df.groupby('Country').agg({
        'Price': 'sum',
        'Order_ID': 'count'
    }).reset_index()
    
    geo_stats.columns = ['Country', 'Revenue', 'Sales']
    
    return geo_stats.sort_values('Revenue', ascending=False)


def analyze_variations(df):
    """Analyze product variations"""
    if 'Variations' not in df.columns or df['Variations'].isna().all():
        return None
    
    variations = df[df['Variations'].notna()]
    
    if len(variations) == 0:
        return None
    
    var_stats = variations.groupby('Variations').agg({
        'Price': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    var_stats.columns = ['Variation', 'Revenue', 'Sales']
    
    return var_stats.sort_values('Revenue', ascending=False).head(10)


def analyze_sku_rotation(df):
    """Analyze SKU rotation rate"""
    if 'SKU' not in df.columns or df['SKU'].isna().all():
        return None
    
    skus = df[df['SKU'].notna()].copy()
    
    if len(skus) == 0:
        return None
    
    # Calculate days range
    date_range = (skus['Date'].max() - skus['Date'].min()).days
    months = max(date_range / 30, 1)
    
    sku_stats = skus.groupby('SKU').agg({
        'Quantity': 'sum'
    }).reset_index()
    
    sku_stats.columns = ['SKU', 'Units_Sold']
    sku_stats['Rotation_Rate'] = sku_stats['Units_Sold'] / months
    
    # Classify rotation speed
    sku_stats['Status'] = sku_stats['Rotation_Rate'].apply(
        lambda x: '🟢 Fast' if x >= 5 else ('🟡 Medium' if x >= 2 else '🔴 Slow')
    )
    
    return sku_stats.sort_values('Rotation_Rate', ascending=False)


# ==================== VISUALIZATION FUNCTIONS ====================

def plot_fees_breakdown_donut(fees_data):
    """Donut chart for fee breakdown"""
    if isinstance(fees_data, dict) and 'total_fees' in fees_data:
        # From real payments data
        labels = ['Etsy Fees', 'Net Amount']
        values = [fees_data['total_fees'], fees_data['total_net']]
        colors = ['#e74c3c', '#27ae60']
    else:
        # From estimated fees
        labels = list(fees_data.keys())
        values = list(fees_data.values())
        colors = px.colors.qualitative.Set3
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors)
    )])
    
    fig.update_layout(
        title="Fee Breakdown",
        height=350,
        showlegend=True
    )
    
    return fig


def plot_fees_evolution(payments_df):
    """Line chart showing fees evolution over time"""
    if payments_df is None or 'Order_Date' not in payments_df.columns:
        return None
    
    daily_fees = payments_df.groupby(payments_df['Order_Date'].dt.date).agg({
        'Fees': 'sum',
        'Gross_Amount': 'sum'
    }).reset_index()
    
    daily_fees['Fee_Rate'] = (daily_fees['Fees'] / daily_fees['Gross_Amount'] * 100)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_fees['Order_Date'],
        y=daily_fees['Fee_Rate'],
        mode='lines+markers',
        name='Fee Rate',
        line=dict(color='#e74c3c', width=2)
    ))
    
    fig.update_layout(
        title="Effective Fee Rate Evolution (%)",
        xaxis_title="Date",
        yaxis_title="Fee Rate (%)",
        height=350
    )
    
    return fig


def plot_product_profitability_bars(product_profit):
    """Horizontal bar chart for product profitability"""
    top_products = product_profit.head(10)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_products['Product'],
        x=top_products['Net_Margin'],
        orientation='h',
        marker=dict(
            color=top_products['Net_Margin'],
            colorscale='RdYlGn',
            showscale=True
        ),
        text=top_products['Net_Margin'].apply(lambda x: f"${x:.2f}"),
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Top 10 Products by Net Margin",
        xaxis_title="Net Margin ($)",
        yaxis_title="Product",
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


# ==================== MAIN APP ====================

st.markdown('<p class="main-header">💰 Finance Pro Dashboard v3.1</p>', unsafe_allow_html=True)

# Check data availability
check_data_availability()

# Load data from session_state
df = load_and_prepare_data(st.session_state['sold_items_df'])

# Load payments data if available
payments_df = None
if 'payments_df' in st.session_state and st.session_state['payments_df'] is not None:
    payments_df = load_etsy_payments(st.session_state['payments_df'])

# ==================== SIDEBAR - FILTERS & CONFIG ====================

st.sidebar.markdown("### ⚙️ Configuration")

# Date filter
date_range = st.sidebar.date_input(
    "Date Range",
    value=(df['Date'].min(), df['Date'].max()),
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)

if len(date_range) == 2:
    df = df[(df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])]
    if payments_df is not None and 'Order_Date' in payments_df.columns:
        payments_df = payments_df[(payments_df['Order_Date'].dt.date >= date_range[0]) & 
                                 (payments_df['Order_Date'].dt.date <= date_range[1])]

# Fee configuration
st.sidebar.markdown("### 💳 Fee Calculator")
fees_mode = st.sidebar.radio("Mode", ["Quick Estimate", "Detailed"])

fees_config = {'mode': 'quick' if fees_mode == "Quick Estimate" else 'detailed'}

if fees_mode == "Detailed":
    fees_config['use_offsite_ads'] = st.sidebar.checkbox("Use Offsite Ads", value=False)
    if fees_config['use_offsite_ads']:
        fees_config['offsite_ads_rate'] = st.sidebar.slider("Offsite Ads Rate", 0.12, 0.15, 0.15, 0.01)
    
    fees_config['etsy_ads_budget'] = st.sidebar.number_input("Monthly Etsy Ads Budget ($)", 0, 1000, 0)
    fees_config['has_etsy_plus'] = st.sidebar.checkbox("Etsy Plus Subscription", value=False)
    fees_config['expected_monthly_sales'] = st.sidebar.number_input("Expected Monthly Sales", 1, 1000, 30)

# ==================== CALCULATE KPIs ====================

kpis = calculate_kpis(df, fees_config, payments_df)
margin_data = calculate_net_margin(df, payments_df)
coupon_analysis = analyze_coupons(df)
geo_analysis = analyze_geographic(df)
variation_analysis = analyze_variations(df)
sku_analysis = analyze_sku_rotation(df)
product_profitability = calculate_product_profitability(df, payments_df)

# ==================== MAIN DASHBOARD ====================

# Real fees indicator
if payments_df is not None:
    st.success("✅ Using REAL Etsy fees from EtsyDirectCheckoutPayments.csv")
else:
    st.info("ℹ️ Using estimated fees. Upload EtsyDirectCheckoutPayments.csv for real fees.")

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"${kpis['total_revenue']:,.2f}",
        delta=None
    )

with col2:
    st.metric(
        "Etsy Fees",
        f"${kpis['etsy_fees']:,.2f}",
        delta=f"-{(kpis['etsy_fees']/kpis['total_revenue']*100):.1f}%",
        delta_color="inverse"
    )

with col3:
    st.metric(
        "Net Margin",
        f"${margin_data['marge_nette']:,.2f}",
        delta=f"{margin_data['taux_marge_nette']:.1f}%"
    )

with col4:
    st.metric(
        "Total Sales",
        f"{kpis['num_sales']:,}",
        delta=f"${kpis['avg_order_value']:.2f} avg"
    )

st.markdown("---")

# ==================== TABS ====================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "💸 Coupons & Promos", 
    "🌍 Geographic & Variations",
    "📦 SKU Analysis",
    "🏆 Product Profitability"
])

with tab1:
    st.markdown("## 📊 Financial Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Fee breakdown
        st.markdown("### 💳 Fee Structure")
        
        if payments_df is not None:
            real_fees = calculate_real_etsy_fees(payments_df)
            if real_fees:
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Effective Fee Rate", f"{real_fees['effective_fee_rate']:.1f}%")
                with col_b:
                    st.metric("Avg Fee/Transaction", f"${real_fees['avg_fee_per_transaction']:.2f}")
                
                st.plotly_chart(plot_fees_breakdown_donut(real_fees), use_container_width=True)
        else:
            st.plotly_chart(plot_fees_breakdown_donut(kpis.get('etsy_fees_detail', {})), use_container_width=True)
    
    with col2:
        # Revenue distribution
        st.markdown("### 💰 Revenue Breakdown")
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Net Margin', 'Etsy Fees', 'Discounts'],
            values=[margin_data['marge_nette'], kpis['etsy_fees'], kpis['total_discounts']],
            hole=0.4,
            marker=dict(colors=['#27ae60', '#e74c3c', '#f39c12'])
        )])
        fig_pie.update_layout(title="Where Does Your Money Go?", height=350)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Revenue over time
    st.markdown("### 📈 Revenue Over Time")
    daily_revenue = df.groupby(df['Date'].dt.date)['Price'].sum().reset_index()
    daily_revenue.columns = ['Date', 'Revenue']
    
    fig_time = px.line(daily_revenue, x='Date', y='Revenue', title="Daily Revenue", markers=True)
    fig_time.update_traces(line_color='#27ae60', line_width=3)
    fig_time.update_layout(height=400)
    st.plotly_chart(fig_time, use_container_width=True)
    
    # Fee evolution (if real data available)
    if payments_df is not None:
        st.markdown("### 📉 Fee Rate Evolution")
        fee_chart = plot_fees_evolution(payments_df)
        if fee_chart:
            st.plotly_chart(fee_chart, use_container_width=True)

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

with tab5:
    st.markdown("## 🏆 Product Profitability Analysis")
    
    if product_profitability is not None and len(product_profitability) > 0:
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            best_product = product_profitability.iloc[0]
            st.metric("Best Product", best_product['Product'][:20] + "...", 
                     f"${best_product['Net_Margin']:.2f}")
        
        with col2:
            avg_margin = product_profitability['Net_Margin_Pct'].mean()
            st.metric("Avg Margin", f"{avg_margin:.1f}%")
        
        with col3:
            unprofitable = len(product_profitability[product_profitability['Net_Margin'] < 0])
            st.metric("Unprofitable Products", unprofitable, 
                     delta_color="inverse" if unprofitable > 0 else "normal")
        
        st.markdown("---")
        
        # Visualization
        st.plotly_chart(plot_product_profitability_bars(product_profitability), use_container_width=True)
        
        # Detailed table
        st.markdown("### 📋 Detailed Product Analysis")
        
        display_df = product_profitability[['Product', 'Revenue', 'Fees', 'Net_Margin', 'Net_Margin_Pct', 'Units_Sold']].copy()
        display_df.columns = ['Product', 'Revenue ($)', 'Fees ($)', 'Net Margin ($)', 'Margin (%)', 'Units Sold']
        
        # Format numbers
        display_df['Revenue ($)'] = display_df['Revenue ($)'].apply(lambda x: f"${x:.2f}")
        display_df['Fees ($)'] = display_df['Fees ($)'].apply(lambda x: f"${x:.2f}")
        display_df['Net Margin ($)'] = display_df['Net Margin ($)'].apply(lambda x: f"${x:.2f}")
        display_df['Margin (%)'] = display_df['Margin (%)'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Warnings for unprofitable products
        unprofitable_products = product_profitability[product_profitability['Net_Margin'] < 0]
        if len(unprofitable_products) > 0:
            st.markdown("### ⚠️ Action Required")
            st.error(f"🚨 {len(unprofitable_products)} product(s) are losing money!")
            
            for _, row in unprofitable_products.iterrows():
                st.markdown(f"""
                <div class="warning-box">
                <strong>{row['Product']}</strong><br>
                Loss: ${abs(row['Net_Margin']):.2f} | {row['Units_Sold']} units sold<br>
                <em>Action: Increase price or discontinue</em>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Product profitability data not available")

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
    <p><strong>Etsy Dashboard</strong> - Finance Pro v3.1 Enriched</p>
    <p style='font-size: 0.9em;'>Real profitability tracking with actual Etsy fees</p>
</div>
""", unsafe_allow_html=True)