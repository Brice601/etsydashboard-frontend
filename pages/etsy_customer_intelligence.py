"""
👥 Customer Intelligence Dashboard v1.0
Understand who buys and why they come back

Features:
✅ Geographic analysis (world map, top countries)
✅ Reviews sentiment analysis
✅ Purchase behavior & shipping delays
✅ Customer retention & LTV
✅ Recurring customers detection
✅ Churn risk analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import Counter
import json
import re
from typing import Dict, Tuple, Optional

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Customer Intelligence - Etsy Dashboard",
    page_icon="👥",
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
    .main-header {font-size: 3rem; font-weight: bold; color: #3498db; text-align: center; margin-bottom: 2rem;}
    .metric-card {background-color: #f0f2f6; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #3498db; margin: 0.5rem 0;}
    .warning-box {background-color: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; margin: 1rem 0;}
    .success-box {background-color: #d4edda; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745; margin: 1rem 0;}
    .info-box {background: #e3f2fd; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196F3; margin: 1rem 0;}
    .premium-lock {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;}
    </style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================

def check_data_availability():
    """Check if required data is available"""
    if 'sold_orders_df' not in st.session_state or st.session_state['sold_orders_df'] is None:
        st.warning("⚠️ No customer data loaded. Please upload your files first.")
        st.info("👉 Go to **Upload Data** page to upload **Sold Orders CSV**")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📤 Go to Upload Data", type="primary", use_container_width=True):
                st.switch_page("pages/Upload_Data.py")
        st.stop()
        return False
    return True


@st.cache_data
def load_and_prepare_orders(orders_df):
    """Prepare orders data"""
    df = orders_df.copy()
    
    # Column mapping
    column_mapping = {
        # Dates (EN + FR)
        'Sale Date': 'Date', 
        'Order Date': 'Date',
        'Date de vente': 'Date', 
        'Date de commande': 'Date',
        
        # Buyer (EN + FR)
        'Buyer': 'Buyer', 
        'Acheteur': 'Buyer',
        
        # Country (EN + FR)
        'Ship Country': 'Country', 
        'Pays de livraison': 'Country',
        'Pays': 'Country',
        
        # City (EN + FR)
        'Ship City': 'City', 
        'Ville de livraison': 'City',
        'Ville': 'City',
        
        # Total/Order Value (EN + FR)
        'Order Value': 'Total',
        'Order Total': 'Total',
        'Total de la commande': 'Total',
        'Item Total': 'Total',
        'Total': 'Total',
        
        # Order ID (EN + FR)
        'Order ID': 'Order_ID',
        'Commande n°': 'Order_ID',
        'Commande': 'Order_ID',
        
        # Date Paid (EN + FR)
        'Date Paid': 'Date_Paid',
        'Date payée': 'Date_Paid',
        
        # Date Shipped (EN + FR)
        'Date Shipped': 'Date_Shipped',
        "Date d'envoi": 'Date_Shipped',
        'Date expédiée': 'Date_Shipped'
    }
    
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)
    
    # Convert dates
    date_cols = ['Date', 'Date_Paid', 'Date_Shipped']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', format='mixed')
    
    # Clean numeric
    if 'Total' in df.columns:
        if not pd.api.types.is_numeric_dtype(df['Total']):
            df['Total'] = (df['Total'].fillna('0').astype(str)
                          .str.replace('€|$|USD|EUR|GBP| |,', '', regex=True)
                          .str.strip())
        df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0)
    
    # Remove invalid rows
    df = df.dropna(subset=['Date'])
    
    return df


@st.cache_data
def load_and_prepare_reviews(reviews_data):
    """Prepare reviews data from JSON"""
    if isinstance(reviews_data, list):
        df = pd.DataFrame(reviews_data)
    else:
        df = reviews_data.copy()
    
    # Column mapping
    column_mapping = {
        'reviewer': 'Reviewer',
        'date_reviewed': 'Date',
        'star_rating': 'Rating',
        'message': 'Review_Text',
        'order_id': 'Order_ID'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Convert date
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='mixed')
    
    # Ensure Rating is numeric
    if 'Rating' in df.columns:
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    
    # Fill empty reviews
    if 'Review_Text' in df.columns:
        df['Review_Text'] = df['Review_Text'].fillna('')
    
    df = df.dropna(subset=['Date', 'Rating'])
    
    return df


# ==================== ANALYSIS FUNCTIONS ====================

def analyze_geography(orders_df):
    """Analyze customer geography"""
    if 'Country' not in orders_df.columns:
        return None, None
    
    # By country
    country_analysis = orders_df.groupby('Country').agg({
        'Order_ID': 'count',
        'Total': 'sum'
    }).reset_index()
    country_analysis.columns = ['Country', 'Orders', 'Revenue']
    country_analysis['Avg_Basket'] = country_analysis['Revenue'] / country_analysis['Orders']
    country_analysis = country_analysis.sort_values('Revenue', ascending=False)
    
    # By city
    city_analysis = None
    if 'City' in orders_df.columns:
        city_analysis = orders_df.groupby('City').agg({
            'Order_ID': 'count',
            'Total': 'sum'
        }).reset_index()
        city_analysis.columns = ['City', 'Orders', 'Revenue']
        city_analysis = city_analysis.sort_values('Orders', ascending=False).head(10)
    
    return country_analysis, city_analysis


def analyze_customer_retention(orders_df):
    """Analyze customer retention and LTV"""
    if 'Buyer' not in orders_df.columns:
        return None
    
    customer_analysis = orders_df.groupby('Buyer').agg({
        'Order_ID': 'count',
        'Total': 'sum',
        'Date': ['min', 'max']
    }).reset_index()
    
    customer_analysis.columns = ['Buyer', 'Num_Orders', 'Total_Spent', 'First_Order', 'Last_Order']
    
    # Days between orders
    customer_analysis['Days_Between_Orders'] = (
        customer_analysis['Last_Order'] - customer_analysis['First_Order']
    ).dt.days / (customer_analysis['Num_Orders'] - 1)
    customer_analysis['Days_Between_Orders'] = customer_analysis['Days_Between_Orders'].fillna(0)
    
    # Lifetime Value
    customer_analysis['LTV'] = customer_analysis['Total_Spent']
    
    # Churn risk (no purchase in 90+ days)
    customer_analysis['Days_Since_Last'] = (datetime.now() - customer_analysis['Last_Order']).dt.days
    customer_analysis['Churn_Risk'] = customer_analysis['Days_Since_Last'] > 90
    
    # Customer segment
    def segment_customer(row):
        if row['Num_Orders'] == 1:
            return 'New'
        elif row['Num_Orders'] <= 3:
            return 'Occasional'
        else:
            return 'VIP'
    
    customer_analysis['Segment'] = customer_analysis.apply(segment_customer, axis=1)
    
    return customer_analysis


def analyze_reviews_sentiment(reviews_df):
    """Sentiment analysis on reviews"""
    if reviews_df is None or 'Review_Text' not in reviews_df.columns:
        return None, None
    
    # Positive & negative keywords (English & French)
    positive_keywords = [
        'perfect', 'great', 'excellent', 'beautiful', 'love', 'amazing', 'best',
        'fast', 'quality', 'recommend', 'gorgeous', 'stunning', 'wonderful',
        'parfait', 'super', 'magnifique', 'rapide', 'qualité', 'recommande', 'joli'
    ]
    
    negative_keywords = [
        'disappointed', 'broken', 'bad', 'poor', 'late', 'delay', 'problem',
        'small', 'not received', 'scam', 'fraud', 'terrible', 'horrible',
        'déçu', 'abîmé', 'retard', 'problème', 'mauvais', 'petit'
    ]
    
    positive_counts = Counter()
    negative_counts = Counter()
    
    for text in reviews_df['Review_Text']:
        if pd.notna(text) and text:
            text_lower = str(text).lower()
            
            for keyword in positive_keywords:
                if keyword in text_lower:
                    positive_counts[keyword] += text_lower.count(keyword)
            
            for keyword in negative_keywords:
                if keyword in text_lower:
                    negative_counts[keyword] += text_lower.count(keyword)
    
    return positive_counts, negative_counts


def extract_all_words(reviews_df):
    """Extract all significant words from reviews"""
    if reviews_df is None or 'Review_Text' not in reviews_df.columns:
        return Counter()
    
    # Stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her',
        'et', 'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'à', 'en',
        'dans', 'pour', 'par', 'sur', 'avec', 'sans', 'est', 'sont', 'ai', 'très'
    }
    
    all_words = Counter()
    
    for text in reviews_df['Review_Text']:
        if pd.notna(text) and text:
            # Clean and split
            words = re.findall(r'\b[a-zA-Zàâäéèêëïîôùûüÿæœç]+\b', str(text).lower())
            
            for word in words:
                if len(word) > 3 and word not in stop_words:
                    all_words[word] += 1
    
    return all_words


def calculate_shipping_delays(orders_df):
    """Calculate shipping delays"""
    if 'Date_Paid' not in orders_df.columns or 'Date_Shipped' not in orders_df.columns:
        return None
    
    df = orders_df.copy()
    df = df.dropna(subset=['Date_Paid', 'Date_Shipped'])
    
    df['Shipping_Delay'] = (df['Date_Shipped'] - df['Date_Paid']).dt.days
    
    # Remove negative delays (data errors)
    df = df[df['Shipping_Delay'] >= 0]
    
    return df


def detect_recurring_customers(customer_analysis):
    """Detect and analyze recurring customers"""
    if customer_analysis is None:
        return None
    
    recurring = customer_analysis[customer_analysis['Num_Orders'] > 1].copy()
    recurring = recurring.sort_values('LTV', ascending=False)
    
    return recurring


# ==================== ENRICHED ANALYSIS FUNCTIONS ====================

def calculate_rfm_analysis(orders_df) -> Optional[pd.DataFrame]:
    """
    RFM Segmentation (Recency, Frequency, Monetary)
    Segments customers based on their purchase behavior
    """
    if 'Date' not in orders_df.columns or 'Buyer' not in orders_df.columns:
        return None
    
    # Reference date (today or max date in data)
    reference_date = orders_df['Date'].max() + timedelta(days=1)
    
    # Calculate RFM
    rfm = orders_df.groupby('Buyer').agg({
        'Date': lambda x: (reference_date - x.max()).days,  # Recency
        'Order_ID': 'nunique',  # Frequency
        'Total': 'sum'  # Monetary
    }).reset_index()
    
    rfm.columns = ['Customer', 'Recency', 'Frequency', 'Monetary']
    
    # Scoring (1-4 for each dimension)
    try:
        rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1], duplicates='drop')
        rfm['F_Score'] = pd.qcut(rfm['Frequency'], 4, labels=[1,2,3,4], duplicates='drop')
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4], duplicates='drop')
    except Exception:
        # Fallback if not enough data for quartiles
        rfm['R_Score'] = pd.cut(rfm['Recency'], 4, labels=[4,3,2,1])
        rfm['F_Score'] = pd.cut(rfm['Frequency'], 4, labels=[1,2,3,4])
        rfm['M_Score'] = pd.cut(rfm['Monetary'], 4, labels=[1,2,3,4])
    
    # Combined score
    rfm['RFM_Score'] = (rfm['R_Score'].astype(str) + 
                       rfm['F_Score'].astype(str) + 
                       rfm['M_Score'].astype(str))
    
    # Customer segmentation
    def segment_customer(row):
        score = int(row['R_Score']) + int(row['F_Score']) + int(row['M_Score'])
        
        if score >= 9:
            return '🏆 Champions'
        elif score >= 7:
            return '💚 Loyal'
        elif score >= 5:
            return '🌱 Potential'
        elif score >= 3:
            return '⚠️ At Risk'
        else:
            return '💤 Dormant'
    
    rfm['Segment'] = rfm.apply(segment_customer, axis=1)
    
    return rfm


def calculate_detailed_customer_metrics(orders_df) -> Optional[pd.DataFrame]:
    """
    Calculate detailed metrics per customer
    """
    if 'Buyer' not in orders_df.columns:
        return None
    
    customer_metrics = orders_df.groupby('Buyer').agg({
        'Order_ID': 'nunique',  # Number of orders
        'Total': ['sum', 'mean'],  # LTV and avg basket
        'Date': ['min', 'max']  # First and last order
    }).reset_index()
    
    customer_metrics.columns = ['Customer', 'Num_Orders', 'LTV', 'Avg_Order', 'First_Purchase', 'Last_Purchase']
    
    # Calculate days between purchases (for repeat customers)
    customer_metrics['Days_Since_First'] = (customer_metrics['Last_Purchase'] - customer_metrics['First_Purchase']).dt.days
    customer_metrics['Avg_Days_Between_Orders'] = customer_metrics['Days_Since_First'] / (customer_metrics['Num_Orders'] - 1)
    customer_metrics['Avg_Days_Between_Orders'] = customer_metrics['Avg_Days_Between_Orders'].fillna(0)
    
    # Calculate days since last order
    reference_date = orders_df['Date'].max()
    customer_metrics['Days_Since_Last_Order'] = (reference_date - customer_metrics['Last_Purchase']).dt.days
    
    # Identify repeat customers
    customer_metrics['Is_Repeat'] = customer_metrics['Num_Orders'] > 1
    
    return customer_metrics


def identify_vip_customers(customer_metrics: pd.DataFrame, percentile: int = 90) -> Tuple[pd.DataFrame, Dict]:
    """
    Identify VIP customers (top X%)
    """
    if customer_metrics is None or len(customer_metrics) == 0:
        return None, None
    
    # Top X% threshold
    threshold = customer_metrics['LTV'].quantile(percentile / 100)
    
    vip_customers = customer_metrics[customer_metrics['LTV'] >= threshold].copy()
    vip_customers = vip_customers.sort_values('LTV', ascending=False)
    
    # Check if we have VIP customers
    if len(vip_customers) == 0:
        return None, None
    
    # VIP stats
    total_ca = customer_metrics['LTV'].sum()
    vip_ca = vip_customers['LTV'].sum()
    
    vip_stats = {
        'count': len(vip_customers),
        'total_ca': vip_ca,
        'avg_ltv': vip_customers['LTV'].mean() if len(vip_customers) > 0 else 0,
        'pct_of_total_ca': (vip_ca / total_ca * 100) if total_ca > 0 else 0
    }
    
    return vip_customers, vip_stats


def analyze_customer_retention_detailed(customer_metrics: pd.DataFrame) -> Dict:
    """
    Detailed retention analysis
    """
    total_customers = len(customer_metrics)
    repeat_customers = len(customer_metrics[customer_metrics['Is_Repeat']])
    
    repeat_rate = (repeat_customers / total_customers * 100) if total_customers > 0 else 0
    
    # Order distribution
    order_counts = customer_metrics['Num_Orders'].value_counts().sort_index()
    
    # Average days between orders (for repeat customers only)
    repeat_df = customer_metrics[customer_metrics['Is_Repeat']]
    avg_days_between = repeat_df['Avg_Days_Between_Orders'].mean() if len(repeat_df) > 0 else 0
    
    return {
        'total_customers': total_customers,
        'repeat_customers': repeat_customers,
        'repeat_rate': repeat_rate,
        'order_distribution': order_counts.to_dict(),
        'avg_days_between_orders': avg_days_between
    }


def identify_churn_risk_customers(customer_metrics: pd.DataFrame, days_threshold: int = 90) -> pd.DataFrame:
    """
    Identify customers at risk of churn
    """
    at_risk = customer_metrics[
        (customer_metrics['Days_Since_Last_Order'] > days_threshold) &
        (customer_metrics['Num_Orders'] > 1)  # Only repeat customers
    ].copy()
    
    at_risk = at_risk.sort_values('LTV', ascending=False)
    
    return at_risk


def analyze_geography_detailed(orders_df) -> Optional[Dict]:
    """
    Detailed geographic analysis by country, state, and city
    """
    if 'Country' not in orders_df.columns:
        return None
    
    geo_analysis = {
        'by_country': orders_df.groupby('Country').agg({
            'Order_ID': 'count',
            'Total': ['sum', 'mean']
        }).reset_index()
    }
    
    # Flatten columns
    geo_analysis['by_country'].columns = ['Country', 'Orders', 'Revenue', 'Avg_Basket']
    geo_analysis['by_country'] = geo_analysis['by_country'].sort_values('Revenue', ascending=False)
    
    # By city (if available)
    if 'City' in orders_df.columns:
        geo_analysis['by_city'] = orders_df.groupby(['Country', 'City']).agg({
            'Order_ID': 'count',
            'Total': 'sum'
        }).reset_index()
        geo_analysis['by_city'].columns = ['Country', 'City', 'Orders', 'Revenue']
        geo_analysis['by_city'] = geo_analysis['by_city'].nlargest(20, 'Orders')
    else:
        geo_analysis['by_city'] = None
    
    return geo_analysis


def analyze_reviews_detailed(orders_df, reviews_df) -> Optional[Dict]:
    """
    Detailed analysis of reviews impact
    """
    if reviews_df is None or len(reviews_df) == 0:
        return None
    
    # Merge orders with reviews
    merged = orders_df.merge(
        reviews_df, 
        left_on='Order_ID', 
        right_on='Order_ID', 
        how='left'
    )
    
    # Global metrics
    avg_rating = reviews_df['Rating'].mean()
    rating_distribution = reviews_df['Rating'].value_counts().sort_index()
    
    # Revenue by rating level
    revenue_by_rating = merged.groupby('Rating')['Total'].sum().sort_index()
    
    # Sentiment analysis
    sentiment_data = analyze_review_sentiment_detailed(reviews_df)
    
    return {
        'avg_rating': avg_rating,
        'rating_distribution': rating_distribution,
        'revenue_by_rating': revenue_by_rating,
        'sentiment': sentiment_data,
        'total_reviews': len(reviews_df)
    }


def analyze_review_sentiment_detailed(reviews_df) -> Dict:
    """
    Detailed sentiment analysis of review messages
    """
    # Positive/negative keywords
    positive_keywords = [
        'perfect', 'great', 'love', 'beautiful', 'excellent', 'amazing',
        'happy', 'recommend', 'fast', 'quality', 'wonderful',
        'parfait', 'super', 'ravie', 'merci', 'rapide', 'jolie', 
        'magnifique', 'excellente', 'satisfait'
    ]
    
    negative_keywords = [
        'disappointed', 'bad', 'broken', 'wrong', 'never', 'poor',
        'slow', 'terrible', 'waste', 'awful',
        'déçu', 'problème', 'lent', 'mauvais', 'cassé', 'erreur',
        'insatisfait', 'nul'
    ]
    
    def classify_sentiment(message):
        if pd.isna(message) or message == '':
            return 'neutral'
        
        message_lower = str(message).lower()
        
        positive_count = sum(1 for word in positive_keywords if word in message_lower)
        negative_count = sum(1 for word in negative_keywords if word in message_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    reviews_df['sentiment'] = reviews_df['Review_Text'].apply(classify_sentiment)
    
    sentiment_counts = reviews_df['sentiment'].value_counts()
    
    # Extract frequent keywords
    all_messages = ' '.join(reviews_df['Review_Text'].dropna().astype(str)).lower()
    keyword_freq = {}
    for word in positive_keywords + negative_keywords:
        keyword_freq[word] = all_messages.count(word)
    
    top_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    top_keywords = [kw for kw in top_keywords if kw[1] > 0]  # Filter out 0 counts
    
    return {
        'distribution': sentiment_counts,
        'top_keywords': top_keywords
    }


# ==================== VISUALIZATION FUNCTIONS ====================

def plot_rfm_segments(rfm_df: pd.DataFrame) -> go.Figure:
    """Plot RFM segmentation pie chart"""
    segment_counts = rfm_df['Segment'].value_counts()
    
    colors = {
        '🏆 Champions': '#27ae60',
        '💚 Loyal': '#3498db',
        '🌱 Potential': '#f39c12',
        '⚠️ At Risk': '#e67e22',
        '💤 Dormant': '#95a5a6'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=segment_counts.index,
        values=segment_counts.values,
        marker=dict(colors=[colors.get(seg, '#95a5a6') for seg in segment_counts.index])
    )])
    
    fig.update_layout(
        title="RFM Customer Segmentation",
        height=400
    )
    
    return fig


def plot_customer_lifetime_distribution(customer_metrics: pd.DataFrame) -> go.Figure:
    """Plot LTV distribution histogram"""
    fig = px.histogram(
        customer_metrics,
        x='LTV',
        nbins=30,
        title='Customer Lifetime Value Distribution',
        labels={'LTV': 'Lifetime Value ($)', 'count': 'Customers'},
        color_discrete_sequence=['#3498db']
    )
    fig.update_layout(height=400)
    
    return fig


def plot_repeat_customer_funnel(repeat_data: Dict) -> go.Figure:
    """Plot repeat customer funnel"""
    order_dist = repeat_data['order_distribution']
    
    # Prepare funnel data (max 5 levels)
    levels = sorted([k for k in order_dist.keys() if k <= 5])
    values = [order_dist.get(level, 0) for level in levels]
    labels = [f"{level} Order{'s' if level > 1 else ''}" for level in levels]
    
    fig = go.Figure(go.Funnel(
        y=labels,
        x=values,
        textinfo="value+percent initial",
        marker=dict(color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6'][:len(levels)])
    ))
    
    fig.update_layout(
        title="Customer Retention Funnel",
        height=400
    )
    
    return fig


def plot_geographic_heatmap(geo_data: Dict) -> go.Figure:
    """Plot geographic revenue heatmap"""
    country_df = geo_data['by_country']
    
    fig = px.choropleth(
        country_df,
        locations='Country',
        locationmode='country names',
        color='Revenue',
        hover_data=['Orders', 'Avg_Basket'],
        title='Revenue by Country',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=500)
    
    return fig


# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ Filters")
    
    period = st.selectbox(
        "Time Period",
        ["All Time", "Last 30 days", "Last 90 days", "Last 6 months", "Last Year"],
        help="Filter data by time period"
    )

# ==================== MAIN APP ====================

st.markdown('<h1 class="main-header">👥 Customer Intelligence Dashboard</h1>', unsafe_allow_html=True)

# Check data availability
check_data_availability()

# Load data
orders_df = load_and_prepare_orders(st.session_state['sold_orders_df'])

# Optional: Reviews
reviews_df = None
if 'reviews_data' in st.session_state and st.session_state['reviews_data'] is not None:
    reviews_df = load_and_prepare_reviews(st.session_state['reviews_data'])

# Optional: Items (for cross-reference)
items_df = None
if 'sold_items_df' in st.session_state and st.session_state['sold_items_df'] is not None:
    items_df = st.session_state['sold_items_df']

# Apply period filter
if period != "All Time" and 'Date' in orders_df.columns:
    days_map = {
        "Last 30 days": 30,
        "Last 90 days": 90,
        "Last 6 months": 180,
        "Last Year": 365
    }
    if period in days_map:
        cutoff_date = datetime.now() - timedelta(days=days_map[period])
        orders_df = orders_df[orders_df['Date'] >= cutoff_date]
        
        if reviews_df is not None and 'Date' in reviews_df.columns:
            reviews_df = reviews_df[reviews_df['Date'] >= cutoff_date]

# Run analyses
country_analysis, city_analysis = analyze_geography(orders_df)
customer_analysis = analyze_customer_retention(orders_df)
recurring_customers = detect_recurring_customers(customer_analysis)

positive_words, negative_words = None, None
all_words = Counter()
if reviews_df is not None:
    positive_words, negative_words = analyze_reviews_sentiment(reviews_df)
    all_words = extract_all_words(reviews_df)

orders_with_delays = calculate_shipping_delays(orders_df)

# ==================== ENRICHED ANALYSES ====================
# RFM Segmentation
rfm_analysis = calculate_rfm_analysis(orders_df)

# Detailed customer metrics
customer_metrics = calculate_detailed_customer_metrics(orders_df)

# VIP customers
vip_customers, vip_stats = None, None
if customer_metrics is not None and len(customer_metrics) > 0:
    try:
        vip_customers, vip_stats = identify_vip_customers(customer_metrics, percentile=90)
    except Exception as e:
        st.sidebar.error(f"Error identifying VIP customers: {str(e)}")
        vip_customers, vip_stats = None, None

# Retention analysis
repeat_data = None
if customer_metrics is not None:
    repeat_data = analyze_customer_retention_detailed(customer_metrics)

# Churn risk customers
at_risk = None
if customer_metrics is not None:
    at_risk = identify_churn_risk_customers(customer_metrics, days_threshold=90)

# Detailed geography
geo_data = analyze_geography_detailed(orders_df)

# Detailed reviews analysis
review_analysis = None
if reviews_df is not None:
    review_analysis = analyze_reviews_detailed(orders_df, reviews_df)

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌍 Customer Profile",
    "⭐ Reviews Analysis",
    "🛒 Purchase Behavior",
    "🔄 Retention & LTV",
    "🎯 RFM & VIP Analysis",
    "📧 Actionable Insights"
])

with tab1:
    st.markdown("## 🌍 Customer Geographic Profile")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = orders_df['Buyer'].nunique() if 'Buyer' in orders_df.columns else 0
        st.metric("Unique Customers", total_customers)
    
    with col2:
        total_countries = orders_df['Country'].nunique() if 'Country' in orders_df.columns else 0
        st.metric("Countries Covered", total_countries)
    
    with col3:
        if customer_analysis is not None:
            repeat_customers = (customer_analysis['Num_Orders'] > 1).sum()
            repeat_rate = (repeat_customers / len(customer_analysis) * 100) if len(customer_analysis) > 0 else 0
            st.metric("Repeat Customers", f"{repeat_rate:.1f}%")
    
    with col4:
        new_customers = (customer_analysis['Num_Orders'] == 1).sum() if customer_analysis is not None else 0
        st.metric("New Customers", new_customers)
    
    st.markdown("---")
    
    # Geographic visualization
    if country_analysis is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🗺️ World Revenue Map")
            
            fig = px.choropleth(
                country_analysis,
                locations='Country',
                locationmode='country names',
                color='Revenue',
                hover_name='Country',
                hover_data={'Orders': True, 'Revenue': ':.2f'},
                color_continuous_scale='Blues',
                title="Revenue by Country"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🏆 Top 10 Countries")
            
            top_10 = country_analysis.head(10)
            
            fig = px.bar(
                top_10,
                x='Revenue',
                y='Country',
                orientation='h',
                text='Revenue',
                color='Orders',
                color_continuous_scale='Oranges'
            )
            fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
            fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Top cities
        if city_analysis is not None:
            st.markdown("---")
            st.markdown("### 🏙️ Top 10 Cities")
            
            fig = px.bar(
                city_analysis,
                x='Orders',
                y='City',
                orientation='h',
                text='Orders',
                color='Revenue',
                color_continuous_scale='Greens'
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.markdown("---")
        st.markdown("### 📋 Country Details")
        
        display_df = country_analysis.copy().head(20)
        display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:.2f}")
        display_df['Avg_Basket'] = display_df['Avg_Basket'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("## ⭐ Customer Reviews Analysis")
    
    if reviews_df is not None:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_rating = reviews_df['Rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.2f}/5")
        
        with col2:
            total_reviews = len(reviews_df)
            st.metric("Total Reviews", total_reviews)
        
        with col3:
            excellent = len(reviews_df[reviews_df['Rating'] >= 4])
            excellent_pct = (excellent / total_reviews * 100) if total_reviews > 0 else 0
            st.metric("4-5★ Reviews", f"{excellent_pct:.1f}%")
        
        with col4:
            negative = len(reviews_df[reviews_df['Rating'] <= 2])
            st.metric("1-2★ Reviews", negative, delta_color="inverse")
        
        st.markdown("---")
        
        # Rating distribution & evolution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Rating Distribution")
            
            rating_dist = reviews_df['Rating'].value_counts().sort_index()
            
            fig = px.bar(
                x=rating_dist.index,
                y=rating_dist.values,
                labels={'x': 'Stars', 'y': 'Count'},
                text=rating_dist.values,
                color=rating_dist.index,
                color_continuous_scale='RdYlGn'
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Average Rating Over Time")
            
            reviews_df['Month'] = reviews_df['Date'].dt.to_period('M').astype(str)
            monthly_rating = reviews_df.groupby('Month')['Rating'].mean().reset_index()
            
            fig = px.line(
                monthly_rating,
                x='Month',
                y='Rating',
                markers=True,
                title="Monthly Average Rating"
            )
            fig.update_traces(line_color='#3498db', line_width=3)
            fig.update_layout(height=400, yaxis_range=[0, 5])
            st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment analysis
        if positive_words and negative_words:
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 😊 Positive Keywords")
                
                if positive_words:
                    top_positive = dict(positive_words.most_common(10))
                    
                    fig = px.bar(
                        x=list(top_positive.values()),
                        y=list(top_positive.keys()),
                        orientation='h',
                        text=list(top_positive.values()),
                        color=list(top_positive.values()),
                        color_continuous_scale='Greens'
                    )
                    fig.update_traces(textposition='outside')
                    fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No positive keywords detected")
            
            with col2:
                st.markdown("### 😟 Negative Keywords")
                
                if negative_words:
                    top_negative = dict(negative_words.most_common(10))
                    
                    fig = px.bar(
                        x=list(top_negative.values()),
                        y=list(top_negative.keys()),
                        orientation='h',
                        text=list(top_negative.values()),
                        color=list(top_negative.values()),
                        color_continuous_scale='Reds'
                    )
                    fig.update_traces(textposition='outside')
                    fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.success("✅ No negative keywords detected!")
        
        # Word cloud
        if all_words:
            st.markdown("---")
            st.markdown("### ☁️ Reviews Word Cloud")
            
            top_words = dict(all_words.most_common(30))
            
            words_df = pd.DataFrame({
                'word': list(top_words.keys()),
                'count': list(top_words.values())
            })
            
            fig = px.scatter(
                words_df,
                x=np.random.rand(len(words_df)),
                y=np.random.rand(len(words_df)),
                size='count',
                text='word',
                color='count',
                color_continuous_scale='Viridis',
                size_max=60
            )
            fig.update_traces(textposition='middle center')
            fig.update_layout(
                height=400,
                showlegend=False,
                xaxis={'visible': False},
                yaxis={'visible': False}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent negative reviews
        negative_reviews = reviews_df[reviews_df['Rating'] <= 2].sort_values('Date', ascending=False)
        
        if len(negative_reviews) > 0:
            st.markdown("---")
            st.markdown("### ⚠️ Recent Negative Reviews (Action Required)")
            
            for idx, row in negative_reviews.head(5).iterrows():
                with st.expander(f"⭐{int(row['Rating'])} - {row['Reviewer']} - {row['Date'].strftime('%m/%d/%Y')}"):
                    if row['Review_Text']:
                        st.markdown(f"**Comment:** {row['Review_Text']}")
                    else:
                        st.markdown("*No comment*")
                    
                    st.markdown(f"**Order ID:** {row['Order_ID']}")
    
    else:
        st.warning("⚠️ Upload reviews.json file to see reviews analysis")

with tab3:
    st.markdown("## 🛒 Purchase Behavior")
    
    # Shipping delays
    if orders_with_delays is not None and 'Shipping_Delay' in orders_with_delays.columns:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_delay = orders_with_delays['Shipping_Delay'].mean()
            st.metric("Avg Shipping Delay", f"{avg_delay:.1f} days")
        
        with col2:
            median_delay = orders_with_delays['Shipping_Delay'].median()
            st.metric("Median Delay", f"{median_delay:.0f} days")
        
        with col3:
            max_delay = orders_with_delays['Shipping_Delay'].max()
            st.metric("Max Delay", f"{max_delay:.0f} days")
        
        st.markdown("---")
        
        # Delay distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Delay Distribution")
            
            fig = px.histogram(
                orders_with_delays,
                x='Shipping_Delay',
                nbins=30,
                title="Shipping Delay Distribution (days)",
                labels={'Shipping_Delay': 'Days', 'count': 'Orders'}
            )
            fig.update_traces(marker_color='#3498db')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⏱️ Delay Performance")
            
            # Categorize delays
            def categorize_delay(days):
                if days <= 3:
                    return '🟢 Excellent (≤3 days)'
                elif days <= 7:
                    return '🟡 Good (4-7 days)'
                elif days <= 14:
                    return '🟠 Average (8-14 days)'
                else:
                    return '🔴 Slow (>14 days)'
            
            orders_with_delays['Delay_Category'] = orders_with_delays['Shipping_Delay'].apply(categorize_delay)
            
            delay_dist = orders_with_delays['Delay_Category'].value_counts()
            
            fig = px.pie(
                values=delay_dist.values,
                names=delay_dist.index,
                title='Delay Performance Categories'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Late shipments alert
        late_shipments = orders_with_delays[orders_with_delays['Shipping_Delay'] > 7]
        
        if len(late_shipments) > 0:
            pct_late = (len(late_shipments) / len(orders_with_delays) * 100)
            
            st.markdown(f"""
            <div class="warning-box">
            ⚠️ <strong>{len(late_shipments)} late shipments</strong> ({pct_late:.1f}%)<br>
            Shipped >7 days after payment. This may impact customer satisfaction and reviews.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Shipping delay data not available. Make sure Date_Paid and Date_Shipped columns are in your CSV.")
    
    # Purchase patterns
    st.markdown("---")
    st.markdown("### 📅 Purchase Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Day of week
        orders_df['Day_Of_Week'] = orders_df['Date'].dt.day_name()
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = orders_df['Day_Of_Week'].value_counts().reindex(day_order, fill_value=0)
        
        fig = px.bar(
            x=day_counts.index,
            y=day_counts.values,
            title='Orders by Day of Week',
            labels={'x': 'Day', 'y': 'Orders'},
            color=day_counts.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Month
        orders_df['Month'] = orders_df['Date'].dt.to_period('M').astype(str)
        monthly_orders = orders_df.groupby('Month')['Order_ID'].count().reset_index()
        monthly_orders.columns = ['Month', 'Orders']
        
        fig = px.line(
            monthly_orders,
            x='Month',
            y='Orders',
            title='Orders Over Time',
            markers=True
        )
        fig.update_traces(line_color='#3498db', line_width=3)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("## 🔄 Customer Retention & Lifetime Value")
    
    if customer_analysis is not None:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_ltv = customer_analysis['LTV'].mean()
            st.metric("Avg Customer LTV", f"${avg_ltv:.2f}")
        
        with col2:
            vip_customers = len(customer_analysis[customer_analysis['Segment'] == 'VIP'])
            st.metric("VIP Customers", vip_customers)
        
        with col3:
            churn_risk = customer_analysis['Churn_Risk'].sum()
            churn_pct = (churn_risk / len(customer_analysis) * 100) if len(customer_analysis) > 0 else 0
            st.metric("At Risk of Churn", f"{churn_pct:.1f}%")
        
        with col4:
            avg_days = customer_analysis['Days_Between_Orders'].replace([np.inf, -np.inf], 0).mean()
            st.metric("Avg Days Between Orders", f"{avg_days:.0f}")
        
        st.markdown("---")
        
        # Customer segmentation
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Customer Segmentation")
            
            segment_counts = customer_analysis['Segment'].value_counts()
            
            fig = px.pie(
                values=segment_counts.values,
                names=segment_counts.index,
                title='Customer Segments',
                color_discrete_sequence=['#3498db', '#95a5a6', '#f39c12']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 💰 LTV Distribution")
            
            fig = px.histogram(
                customer_analysis,
                x='LTV',
                nbins=30,
                title='Customer Lifetime Value Distribution',
                labels={'LTV': 'Lifetime Value ($)', 'count': 'Customers'},
                color_discrete_sequence=['#3498db']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Top customers
        st.markdown("---")
        st.markdown("### 🏆 Top 10 Customers by LTV")
        
        top_customers = customer_analysis.nlargest(10, 'LTV')[['Buyer', 'Num_Orders', 'LTV', 'Days_Since_Last', 'Segment']]
        
        display_df = top_customers.copy()
        display_df['LTV'] = display_df['LTV'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Churn risk customers
        churn_customers = customer_analysis[customer_analysis['Churn_Risk'] == True].sort_values('LTV', ascending=False)
        
        if len(churn_customers) > 0:
            st.markdown("---")
            st.markdown("### ⚠️ Customers at Risk of Churn")
            st.markdown("*No purchase in 90+ days*")
            
            display_churn = churn_customers.head(10)[['Buyer', 'Num_Orders', 'LTV', 'Days_Since_Last']]
            display_churn['LTV'] = display_churn['LTV'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(display_churn, use_container_width=True, hide_index=True)
            
            st.markdown("""
            <div class="warning-box">
            💡 <strong>Recommendation:</strong> Re-engage these customers with:
            <ul>
            <li>Personalized email with discount code</li>
            <li>"We miss you" campaign</li>
            <li>Showcase new products</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

with tab5:
    st.markdown("## 🎯 RFM Segmentation & VIP Analysis")
    
    if rfm_analysis is not None and customer_metrics is not None:
        # ========== SECTION 1 : MÉTRIQUES CLÉS ==========
        st.markdown("### 📊 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Customers",
                f"{len(customer_metrics)}",
                delta=None
            )
        
        with col2:
            if repeat_data is not None:
                st.metric(
                    "Repeat Rate",
                    f"{repeat_data['repeat_rate']:.1f}%",
                    delta=None
                )
        
        with col3:
            st.metric(
                "Avg Customer LTV",
                f"${customer_metrics['LTV'].mean():.2f}",
                delta=None
            )
        
        with col4:
            if repeat_data is not None:
                st.metric(
                    "Avg Days Between Orders",
                    f"{repeat_data['avg_days_between_orders']:.0f} days",
                    delta=None
                )
        
        # ========== SECTION 2 : SEGMENTATION RFM ==========
        st.markdown("---")
        st.markdown("### 🎯 RFM Segmentation")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.plotly_chart(plot_rfm_segments(rfm_analysis), use_container_width=True)
        
        with col2:
            st.markdown("**Segment Definitions:**")
            st.write("🏆 **Champions**: Best customers (buy often, recently, high value)")
            st.write("💚 **Loyal**: Regular, dependable customers")
            st.write("🌱 **Potential**: Promising customers to develop")
            st.write("⚠️ **At Risk**: Previously good customers, now inactive")
            st.write("💤 **Dormant**: Inactive customers with low engagement")
        
        # Segment details
        with st.expander("📋 Details by Segment"):
            segment_summary = rfm_analysis.groupby('Segment').agg({
                'Customer': 'count',
                'Monetary': ['sum', 'mean'],
                'Frequency': 'mean',
                'Recency': 'mean'
            }).reset_index()
            
            segment_summary.columns = ['Segment', 'Count', 'Total Revenue', 'Avg LTV', 'Avg Frequency', 'Avg Recency (days)']
            st.dataframe(segment_summary, use_container_width=True, hide_index=True)
        
        # ========== SECTION 3 : CLIENTS VIP ==========
        if vip_customers is not None and vip_stats is not None and isinstance(vip_customers, pd.DataFrame) and len(vip_customers) > 0:
            st.markdown("---")
            st.markdown("### 👑 VIP Customers (Top 10%)")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Number of VIPs",
                    f"{vip_stats['count']}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Total VIP Revenue",
                    f"${vip_stats['total_ca']:.2f}",
                    delta=None
                )
            
            with col3:
                st.metric(
                    "% of Total Revenue",
                    f"{vip_stats['pct_of_total_ca']:.1f}%",
                    delta=None
                )
            
            with col4:
                st.metric(
                    "Avg VIP LTV",
                    f"${vip_stats['avg_ltv']:.2f}",
                    delta=None
                )
            
            # VIP list
            with st.expander("📋 VIP Customer List"):
                try:
                    vip_display = vip_customers[['Customer', 'LTV', 'Num_Orders', 'Avg_Order']].head(20)
                    vip_display.columns = ['Customer', 'LTV ($)', 'Orders', 'Avg Basket ($)']
                    vip_display['LTV ($)'] = vip_display['LTV ($)'].round(2)
                    vip_display['Avg Basket ($)'] = vip_display['Avg Basket ($)'].round(2)
                    st.dataframe(vip_display, use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"Error displaying VIP customers: {str(e)}")
                    st.write(f"Type of vip_customers: {type(vip_customers)}")
                    st.write(f"Length: {len(vip_customers) if hasattr(vip_customers, '__len__') else 'N/A'}")
                    if isinstance(vip_customers, pd.DataFrame):
                        st.write(f"Columns: {vip_customers.columns.tolist()}")
        
        # ========== SECTION 4 : FIDÉLISATION ==========
        if repeat_data is not None:
            st.markdown("---")
            st.markdown("### 💚 Retention Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(plot_repeat_customer_funnel(repeat_data), use_container_width=True)
            
            with col2:
                st.plotly_chart(plot_customer_lifetime_distribution(customer_metrics), use_container_width=True)
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                first_time = repeat_data['order_distribution'].get(1, 0)
                st.metric(
                    "First-Time Customers",
                    f"{first_time}",
                    delta=f"{(1 - repeat_data['repeat_rate']/100)*100:.0f}% of customers"
                )
            
            with col2:
                st.metric(
                    "Repeat Customers",
                    f"{repeat_data['repeat_customers']}",
                    delta=f"{repeat_data['repeat_rate']:.1f}% of customers"
                )
            
            with col3:
                best_customer = customer_metrics.nlargest(1, 'Num_Orders').iloc[0]
                st.metric(
                    "Most Orders (Record)",
                    f"{int(best_customer['Num_Orders'])} orders",
                    delta=f"LTV: ${best_customer['LTV']:.2f}"
                )
        
        # ========== SECTION 5 : RISQUE CHURN ==========
        if at_risk is not None and isinstance(at_risk, pd.DataFrame):
            st.markdown("---")
            st.markdown("### ⚠️ Customers at Risk of Churn")
            
            if len(at_risk) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "Customers at Risk",
                        f"{len(at_risk)}",
                        delta=f"{len(at_risk)/len(customer_metrics)*100:.1f}% of customers",
                        delta_color="inverse"
                    )
                
                with col2:
                    st.metric(
                        "Potential Lost Revenue",
                        f"${at_risk['LTV'].sum():.2f}",
                        delta="Need to reactivate!",
                        delta_color="inverse"
                    )
                
                # At-risk customer list
                st.markdown("**Top 10 At-Risk Customers (by LTV):**")
                at_risk_display = at_risk[['Customer', 'LTV', 'Num_Orders', 'Days_Since_Last_Order']].head(10)
                at_risk_display.columns = ['Customer', 'LTV ($)', 'Orders', 'Days Inactive']
                at_risk_display['LTV ($)'] = at_risk_display['LTV ($)'].round(2)
                st.dataframe(at_risk_display, use_container_width=True, hide_index=True)
                
                # Recommendations
                with st.expander("💡 Reactivation Recommendations"):
                    st.write("**Suggested Actions:**")
                    st.write("1. 📧 Re-engagement email with 10-15% coupon code")
                    st.write("2. 🎁 Exclusive 'We miss you' offer")
                    st.write("3. 📱 Personalized message reminding them of their last purchase")
                    st.write("4. ⭐ Request a review if they haven't left one (engagement)")
            else:
                st.success("✅ No customers at risk of churn detected!")
        
        # ========== SECTION 6 : GÉOGRAPHIE DÉTAILLÉE ==========
        if geo_data is not None:
            st.markdown("---")
            st.markdown("### 🌍 Geographic Analysis")
            
            st.plotly_chart(plot_geographic_heatmap(geo_data), use_container_width=True)
            
            # Details by country
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Top 10 Countries by Revenue:**")
                top_countries = geo_data['by_country'].nlargest(10, 'Revenue')
                top_countries_display = top_countries.copy()
                top_countries_display['Revenue'] = top_countries_display['Revenue'].round(2)
                top_countries_display['Avg_Basket'] = top_countries_display['Avg_Basket'].round(2)
                st.dataframe(top_countries_display, use_container_width=True, hide_index=True)
            
            with col2:
                if geo_data['by_city'] is not None:
                    st.markdown("**Top 10 Cities:**")
                    city_display = geo_data['by_city'].head(10).copy()
                    city_display['Revenue'] = city_display['Revenue'].round(2)
                    st.dataframe(city_display, use_container_width=True, hide_index=True)
        
        # ========== SECTION 7 : AVIS CLIENTS DÉTAILLÉS ==========
        if review_analysis is not None:
            st.markdown("---")
            st.markdown("### ⭐ Detailed Reviews Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Average Rating",
                    f"{review_analysis['avg_rating']:.2f}/5",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Total Reviews",
                    f"{review_analysis['total_reviews']}",
                    delta=None
                )
            
            with col3:
                sentiment_dist = review_analysis['sentiment']['distribution']
                total_reviews = review_analysis['total_reviews']
                sentiment_pct = sentiment_dist.get('positive', 0) / total_reviews * 100 if total_reviews > 0 else 0
                st.metric(
                    "% Positive Reviews",
                    f"{sentiment_pct:.1f}%",
                    delta=None
                )
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Rating distribution
                rating_dist = review_analysis['rating_distribution']
                fig_rating = go.Figure(data=[go.Bar(
                    x=rating_dist.index,
                    y=rating_dist.values,
                    marker_color='#3498db'
                )])
                fig_rating.update_layout(
                    title="Rating Distribution",
                    xaxis_title="Stars",
                    yaxis_title="Count",
                    height=400
                )
                st.plotly_chart(fig_rating, use_container_width=True)
            
            with col2:
                # Sentiment distribution
                sentiment_dist = review_analysis['sentiment']['distribution']
                fig_sentiment = go.Figure(data=[go.Pie(
                    labels=sentiment_dist.index,
                    values=sentiment_dist.values,
                    marker=dict(colors=['#27ae60', '#95a5a6', '#e74c3c'])
                )])
                fig_sentiment.update_layout(title="Review Sentiment", height=400)
                st.plotly_chart(fig_sentiment, use_container_width=True)
            
            # Frequent keywords
            top_keywords = review_analysis['sentiment']['top_keywords']
            if top_keywords:
                with st.expander("🔑 Frequent Keywords in Reviews"):
                    st.write("**Top 10 keywords:**")
                    for word, count in top_keywords:
                        st.write(f"- **{word}** : {count} occurrences")
    
    else:
        st.info("⚠️ Not enough data for RFM analysis. Upload more orders to see detailed segmentation.")

with tab6:
    st.markdown("## 📧 Actionable Insights & Recommendations")
    
    if is_premium:
        st.markdown("### 🤖 AI-Powered Recommendations")
        
        # Insight 1: Geographic expansion
        if country_analysis is not None:
            top_country = country_analysis.iloc[0]
            
            st.markdown(f"""
            <div class="success-box">
            <strong>🌍 Geographic Opportunity</strong><br>
            Your top market is <strong>{top_country['Country']}</strong> with ${top_country['Revenue']:.2f} in revenue.<br>
            <strong>Action:</strong> Focus marketing efforts on this region and explore similar markets.
            </div>
            """, unsafe_allow_html=True)
        
        # Insight 2: Customer retention
        if customer_analysis is not None:
            vip_count = len(customer_analysis[customer_analysis['Segment'] == 'VIP'])
            vip_revenue = customer_analysis[customer_analysis['Segment'] == 'VIP']['LTV'].sum()
            
            st.markdown(f"""
            <div class="success-box">
            <strong>👑 VIP Customer Value</strong><br>
            Your {vip_count} VIP customers generated <strong>${vip_revenue:.2f}</strong> in total revenue.<br>
            <strong>Action:</strong> Create VIP loyalty program with exclusive perks and early access to new products.
            </div>
            """, unsafe_allow_html=True)
        
        # Insight 3: Review management
        if reviews_df is not None:
            negative_count = len(reviews_df[reviews_df['Rating'] <= 2])
            
            if negative_count > 0:
                st.markdown(f"""
                <div class="warning-box">
                <strong>⚠️ Review Management Alert</strong><br>
                You have <strong>{negative_count}</strong> negative reviews (1-2 stars).<br>
                <strong>Action:</strong> Reach out to these customers personally, offer solutions, and request review updates.
                </div>
                """, unsafe_allow_html=True)
        
        # Insight 4: Shipping performance
        if orders_with_delays is not None:
            late_pct = (len(orders_with_delays[orders_with_delays['Shipping_Delay'] > 7]) / len(orders_with_delays) * 100)
            
            if late_pct > 20:
                st.markdown(f"""
                <div class="warning-box">
                <strong>📦 Shipping Improvement Needed</strong><br>
                {late_pct:.1f}% of your orders ship late (>7 days).<br>
                <strong>Action:</strong> Streamline your fulfillment process, consider prep days, or update processing times on listings.
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Premium CTA
        st.markdown("""
        <div class="premium-lock">
            <h3 style="margin-bottom: 1rem;">💎 Unlock AI-Powered Insights</h3>
            <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
                Get personalized recommendations to:
            </p>
            <ul style="text-align: left; max-width: 600px; margin: 20px auto; font-size: 1rem;">
                <li>✅ Expand to high-potential markets</li>
                <li>✅ Retain VIP customers with targeted campaigns</li>
                <li>✅ Improve shipping performance</li>
                <li>✅ Respond to negative reviews effectively</li>
                <li>✅ Re-engage customers at risk of churn</li>
            </ul>
            <p style="font-size: 1.2rem; font-weight: bold; margin-top: 2rem;">
                Only $9/month
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Upgrade to Premium", type="primary", use_container_width=True):
                st.switch_page("pages/Premium.py")

# ==================== FOOTER ====================
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📤 Upload Data", use_container_width=True):
        st.switch_page("pages/Upload_Data.py")
with col2:
    if st.button("💰 Finance Pro", use_container_width=True):
        st.switch_page("pages/etsy_finance_pro.py")
with col3:
    if st.button("🔍 SEO Analyzer", use_container_width=True):
        st.switch_page("pages/etsy_seo_analyzer.py")

st.markdown("""
<div style='text-align: center; color: #666; padding: 20px; margin-top: 2rem;'>
    <p><strong>Etsy Dashboard</strong> - Customer Intelligence v1.0</p>
    <p style='font-size: 0.9em;'>Understand your customers and grow your business</p>
</div>
""", unsafe_allow_html=True)