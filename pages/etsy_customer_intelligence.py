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

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌍 Customer Profile",
    "⭐ Reviews Analysis",
    "🛒 Purchase Behavior",
    "🔄 Retention & LTV",
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