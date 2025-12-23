"""
🔍 SEO Analyzer Dashboard v2.0 - ENRICHED VERSION
Optimize your Etsy listings to rank higher in search

Features:
✅ SEO score per listing (0-100) with detailed breakdown
✅ Title optimization analysis with keyword frequency
✅ Tags performance tracking with sales correlation
✅ Image analysis and correlation with sales
✅ Variation performance analysis
✅ SEO opportunities identification
✅ Correlation SEO score vs sales (Premium)
✅ Best-sellers vs non-sellers comparison (Premium)
✅ AI-powered recommendations (Premium)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from collections import Counter
import re

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="SEO Analyzer - Etsy Dashboard",
    page_icon="🔍",
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
    .main-header {font-size: 3rem; font-weight: bold; color: #9b59b6; text-align: center; margin-bottom: 2rem;}
    .metric-card {background-color: #f0f2f6; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #9b59b6; margin: 0.5rem 0;}
    .seo-score-high {background-color: #d4edda; padding: 1rem; border-radius: 8px; border-left: 5px solid #28a745; margin: 1rem 0;}
    .seo-score-medium {background-color: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 5px solid #ffc107; margin: 1rem 0;}
    .seo-score-low {background-color: #f8d7da; padding: 1rem; border-radius: 8px; border-left: 5px solid #dc3545; margin: 1rem 0;}
    .warning-box {background-color: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; margin: 1rem 0;}
    .success-box {background-color: #d4edda; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745; margin: 1rem 0;}
    .info-box {background: #e3f2fd; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196F3; margin: 1rem 0;}
    .premium-lock {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;}
    </style>
""", unsafe_allow_html=True)

# ==================== DATA LOADING ====================

def check_data_availability():
    """Check if required data is available"""
    if 'listings_df' not in st.session_state or st.session_state['listings_df'] is None:
        st.warning("⚠️ No listings data loaded. Please upload your files first.")
        st.info("👉 Go to **Upload Data** page to upload **Listings CSV**")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📤 Go to Upload Data", type="primary", use_container_width=True):
                st.switch_page("pages/Upload_Data.py")
        st.stop()
        return False
    return True


@st.cache_data
def load_and_prepare_listings(listings_df):
    """Prepare listings data with enhanced mapping"""
    df = listings_df.copy()
    
    # Column mapping (supports both EN and FR)
    column_mapping = {
        'Title': 'Title', 'Titre': 'Title', 'TITRE': 'Title',
        'Price': 'Price', 'Prix': 'Price', 'PRIX': 'Price',
        'Quantity': 'Quantity', 'Stock': 'Quantity', 'QUANTITÉ': 'Quantity', 'Quantité': 'Quantity',
        'Tags': 'Tags', 'Étiquettes': 'Tags', 'TAGS': 'Tags',
        'Description': 'Description', 'DESCRIPTION': 'Description',
        'Images': 'Images', 'Photos': 'Images',
        'SKU': 'SKU', 'RÉFÉRENCE': 'SKU', 'Référence': 'SKU', 'Reference': 'SKU'
    }
    
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)
    
    # Clean price
    if 'Price' in df.columns:
        if not pd.api.types.is_numeric_dtype(df['Price']):
            df['Price'] = (df['Price'].fillna('0').astype(str)
                          .str.replace('€|$|USD|EUR|GBP| |,', '', regex=True)
                          .str.strip())
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
    
    # Count images from IMAGE columns
    image_cols = [f'IMAGE {i}' for i in range(1, 11)]
    available_image_cols = [col for col in image_cols if col in df.columns]
    
    if available_image_cols:
        df['Num_Images'] = df[available_image_cols].notna().sum(axis=1)
    elif 'Images' in df.columns:
        df['Num_Images'] = df['Images'].apply(lambda x: 
            len(str(x).split(',')) if pd.notna(x) and str(x) else 0
        )
    else:
        df['Num_Images'] = 0
    
    # Remove invalid rows
    df = df.dropna(subset=['Title'])
    
    return df


# ==================== ENHANCED SEO ANALYSIS FUNCTIONS ====================

def calculate_enhanced_seo_score(row):
    """
    Enhanced SEO score calculation (0-100) with detailed breakdown
    Combines both original and enriched scoring logic
    """
    score = 0
    issues = []
    recommendations = []
    details = {}
    
    # ========== TITLE ANALYSIS (40 points) ==========
    title = str(row.get('Title', ''))
    if pd.isna(title) or not title:
        return {
            'score': 0,
            'issues': ["❌ Missing title"],
            'recommendations': ["Add a descriptive title"],
            'details': {},
            'grade': '❌ F'
        }
    
    title_len = len(title)
    title_words = len(title.split())
    
    # Length optimization (20 points)
    if 100 <= title_len <= 140:
        score += 20
        details['title_length'] = '✅ Optimal length'
    elif 80 <= title_len < 100:
        score += 15
        recommendations.append("📏 Increase title length (optimal: 100-140 characters)")
        details['title_length'] = '⚠️ Length to optimize'
    elif title_len < 80:
        score += 10
        issues.append("❌ Title too short")
        recommendations.append("📏 Extend title to 100-140 characters")
        details['title_length'] = '❌ Too short'
    else:
        score += 15
        issues.append("⚠️ Title too long")
        recommendations.append("✂️ Reduce to max 140 characters")
        details['title_length'] = '⚠️ Too long'
    
    # Word count (20 points)
    if 10 <= title_words <= 15:
        score += 20
        details['title_words'] = '✅ Good word count'
    elif title_words >= 8:
        score += 15
        recommendations.append("📝 Aim for 10-15 words")
        details['title_words'] = '⚠️ Word count to optimize'
    else:
        score += 5
        issues.append("❌ Not enough words")
        recommendations.append("📝 Add more descriptive words (10-15 optimal)")
        details['title_words'] = '❌ Too few words'
    
    # ========== TAGS ANALYSIS (30 points) ==========
    tags = str(row.get('Tags', ''))
    tags_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else []
    num_tags = len(tags_list)
    
    # Tag count (20 points)
    if num_tags == 13:
        score += 20
        details['tags_count'] = '✅ 13 tags (maximum)'
    elif num_tags >= 10:
        score += 15
        recommendations.append("🏷️ Add more tags (13 max)")
        details['tags_count'] = '✅ 10+ tags'
    elif num_tags >= 7:
        score += 10
        issues.append("⚠️ Less than 10 tags")
        recommendations.append("🏷️ Use all 13 tag slots")
        details['tags_count'] = '⚠️ Less than 10 tags'
    else:
        score += 5
        issues.append("❌ Not enough tags")
        recommendations.append("🏷️ Add tags (13 recommended)")
        details['tags_count'] = '❌ Too few tags'
    
    # Tag quality (10 points)
    quality_tags = [t for t in tags_list if len(t) > 3]
    if len(quality_tags) == num_tags and num_tags > 0:
        score += 10
        details['tags_quality'] = '✅ All quality tags'
    elif len(quality_tags) > 0:
        score += 5
        recommendations.append("🎯 Use longer, more specific tags")
        details['tags_quality'] = '⚠️ Some short tags'
    else:
        details['tags_quality'] = '❌ Low quality tags'
    
    # ========== DESCRIPTION ANALYSIS (20 points) ==========
    description = str(row.get('Description', ''))
    desc_length = len(description)
    
    if desc_length >= 1000:
        score += 20
        details['description'] = '✅ Complete description'
    elif desc_length >= 500:
        score += 15
        recommendations.append("📄 Extend description (1000+ chars optimal)")
        details['description'] = '✅ Good description'
    elif desc_length >= 200:
        score += 10
        issues.append("⚠️ Short description")
        recommendations.append("📄 Add more detail to description")
        details['description'] = '⚠️ Short description'
    else:
        score += 5
        issues.append("❌ Very short description")
        recommendations.append("📄 Write detailed description (500+ chars)")
        details['description'] = '❌ Too short'
    
    # ========== IMAGES ANALYSIS (10 points) ==========
    num_images = int(row.get('Num_Images', 0))
    
    if num_images >= 10:
        score += 10
        details['images'] = '✅ 10 images (maximum)'
    elif num_images >= 7:
        score += 8
        recommendations.append("📸 Add more images (10 max)")
        details['images'] = '✅ 7+ images'
    elif num_images >= 5:
        score += 6
        recommendations.append("📸 Add more images (aim for 10)")
        details['images'] = '⚠️ 5-6 images'
    elif num_images >= 3:
        score += 4
        issues.append("⚠️ Only 3-4 images")
        recommendations.append("📸 Add significantly more images")
        details['images'] = '⚠️ 3-4 images'
    else:
        score += 2
        issues.append("❌ Very few images")
        recommendations.append("📸 Add at least 5 images")
        details['images'] = '❌ Too few images'
    
    # Determine grade
    if score >= 90:
        grade = '🏆 A+'
    elif score >= 80:
        grade = '🥇 A'
    elif score >= 70:
        grade = '🥈 B'
    elif score >= 60:
        grade = '🥉 C'
    elif score >= 50:
        grade = '⚠️ D'
    else:
        grade = '❌ F'
    
    return {
        'score': score,
        'issues': issues,
        'recommendations': recommendations[:5],  # Top 5 recommendations
        'details': details,
        'grade': grade
    }


# ==================== TITLE ANALYSIS ====================

def analyze_titles(listings_df):
    """Enhanced title analysis with keyword extraction"""
    listings_df['title_length'] = listings_df['Title'].astype(str).str.len()
    listings_df['title_words'] = listings_df['Title'].astype(str).str.split().str.len()
    
    analysis = {
        'avg_length': listings_df['title_length'].mean(),
        'avg_words': listings_df['title_words'].mean(),
        'optimal_length': ((listings_df['title_length'] >= 100) & (listings_df['title_length'] <= 140)).sum(),
        'optimal_words': ((listings_df['title_words'] >= 10) & (listings_df['title_words'] <= 15)).sum(),
        'too_short': (listings_df['title_length'] < 80).sum(),
        'too_long': (listings_df['title_length'] > 140).sum()
    }
    
    # Extract frequent keywords
    all_titles = ' '.join(listings_df['Title'].astype(str).str.lower()).split()
    stopwords = ['de', 'le', 'la', 'les', 'un', 'une', 'et', 'pour', 'avec', 'en', 'du', 'des', 
                 'the', 'a', 'an', 'and', 'for', 'with', 'in', 'of']
    keywords = [word for word in all_titles if len(word) > 3 and word not in stopwords]
    
    keyword_freq = Counter(keywords).most_common(20)
    analysis['top_keywords'] = keyword_freq
    
    return analysis


def plot_title_length_analysis(title_analysis):
    """Visualize title length distribution"""
    categories = ['Too Short', 'Optimal', 'Too Long']
    values = [
        title_analysis['too_short'],
        title_analysis['optimal_length'],
        title_analysis['too_long']
    ]
    colors = ['#dc3545', '#28a745', '#ffc107']
    
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=values,
        textposition='outside'
    )])
    
    fig.update_layout(
        title='Title Length Distribution',
        xaxis_title='Category',
        yaxis_title='Number of Listings',
        height=400
    )
    
    return fig


# ==================== TAG ANALYSIS ====================

def analyze_tags(listings_df):
    """Comprehensive tag analysis"""
    # Extract all tags
    all_tags = []
    for tags_str in listings_df['Tags']:
        if pd.notna(tags_str):
            tags = [t.strip() for t in str(tags_str).split(',')]
            all_tags.extend([t for t in tags if t])
    
    # Tag frequency
    tag_freq = Counter(all_tags).most_common(30)
    
    # Stats per listing
    listings_df['nb_tags'] = listings_df['Tags'].apply(
        lambda x: len([t for t in str(x).split(',') if t.strip()]) if pd.notna(x) else 0
    )
    
    analysis = {
        'avg_tags_per_listing': listings_df['nb_tags'].mean(),
        'max_tags_listings': (listings_df['nb_tags'] == 13).sum(),
        'under_10_tags': (listings_df['nb_tags'] < 10).sum(),
        'top_tags': tag_freq,
        'total_unique_tags': len(set(all_tags))
    }
    
    return analysis


def analyze_tag_performance(listings_df, sales_df):
    """Correlate tags with sales performance"""
    if sales_df is None or len(sales_df) == 0:
        return None
    
    # Match column names
    item_name_col = 'Item Name' if 'Item Name' in sales_df.columns else 'TITRE'
    
    # Merge listings with sales
    merged = listings_df.merge(
        sales_df.groupby(item_name_col)['Quantity'].sum(),
        left_on='Title',
        right_index=True,
        how='left'
    )
    
    merged['Quantity'] = merged['Quantity'].fillna(0)
    
    # Calculate average sales per tag
    tag_sales = {}
    for _, row in merged.iterrows():
        if pd.notna(row['Tags']):
            tags = [t.strip() for t in str(row['Tags']).split(',')]
            for tag in tags:
                if tag:
                    if tag not in tag_sales:
                        tag_sales[tag] = []
                    tag_sales[tag].append(row['Quantity'])
    
    # Average sales per tag
    tag_performance = {
        tag: np.mean(sales) 
        for tag, sales in tag_sales.items() 
        if len(sales) >= 2  # At least 2 occurrences
    }
    
    # Top performing tags
    top_performing_tags = sorted(tag_performance.items(), key=lambda x: x[1], reverse=True)[:15]
    
    return top_performing_tags


def plot_tag_frequency(tag_analysis):
    """Visualize most used tags"""
    tags_df = pd.DataFrame(tag_analysis['top_tags'][:15], columns=['Tag', 'Frequency'])
    
    fig = px.bar(
        tags_df,
        x='Frequency',
        y='Tag',
        orientation='h',
        title='Top 15 Most Used Tags',
        color='Frequency',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=500, showlegend=False)
    return fig


def plot_tag_performance(tag_performance):
    """Visualize best performing tags"""
    perf_df = pd.DataFrame(tag_performance, columns=['Tag', 'Avg Sales'])
    
    fig = px.bar(
        perf_df,
        x='Avg Sales',
        y='Tag',
        orientation='h',
        title='Top 15 Best Performing Tags',
        color='Avg Sales',
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(height=500, showlegend=False)
    return fig


# ==================== IMAGE ANALYSIS ====================

def analyze_images(listings_df):
    """Analyze image usage"""
    analysis = {
        'avg_images': listings_df['Num_Images'].mean(),
        'max_images_listings': (listings_df['Num_Images'] == 10).sum(),
        'under_5_images': (listings_df['Num_Images'] < 5).sum()
    }
    
    return analysis


def correlate_images_to_sales(listings_df, sales_df):
    """Correlate number of images with sales"""
    if sales_df is None:
        return None
    
    item_name_col = 'Item Name' if 'Item Name' in sales_df.columns else 'TITRE'
    
    merged = listings_df.merge(
        sales_df.groupby(item_name_col)['Quantity'].sum(),
        left_on='Title',
        right_index=True,
        how='left'
    )
    
    merged['Quantity'] = merged['Quantity'].fillna(0)
    
    image_corr = merged.groupby('Num_Images')['Quantity'].agg(['sum', 'mean', 'count']).reset_index()
    image_corr.columns = ['Images', 'Total_Sales', 'Avg_Sales', 'Listings']
    
    return image_corr


def plot_image_correlation(image_corr):
    """Visualize image-sales correlation"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=image_corr['Images'],
        y=image_corr['Total_Sales'],
        name='Total Sales',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Scatter(
        x=image_corr['Images'],
        y=image_corr['Avg_Sales'],
        name='Avg Sales',
        yaxis='y2',
        marker_color='orange',
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title='Sales Correlation with Number of Images',
        xaxis_title='Number of Images',
        yaxis_title='Total Sales',
        yaxis2=dict(
            title='Average Sales per Listing',
            overlaying='y',
            side='right'
        ),
        height=400
    )
    
    return fig


# ==================== VARIATION ANALYSIS ====================

def analyze_variations(sales_df):
    """Analyze performance by product variations"""
    if 'Variations' not in sales_df.columns:
        return None
    
    # Parse variations
    var_sales = {}
    for _, row in sales_df.iterrows():
        if pd.notna(row['Variations']):
            # Parse format like "Color: Blue, Size: M"
            variations = str(row['Variations']).split(',')
            for var in variations:
                if ':' in var:
                    var_type, var_value = var.split(':', 1)
                    var_type = var_type.strip()
                    var_value = var_value.strip()
                    
                    if var_type not in var_sales:
                        var_sales[var_type] = {}
                    
                    if var_value not in var_sales[var_type]:
                        var_sales[var_type][var_value] = 0
                    
                    var_sales[var_type][var_value] += row.get('Quantity', 1)
    
    # Format results
    result = {}
    for var_type, values in var_sales.items():
        sorted_values = sorted(values.items(), key=lambda x: x[1], reverse=True)[:10]
        result[var_type] = sorted_values
    
    return result if result else None


# ==================== OPPORTUNITIES IDENTIFICATION ====================

def identify_seo_opportunities(listings_df, seo_scores):
    """Identify optimization opportunities"""
    listings_df['seo_score'] = seo_scores
    
    opportunities = {
        'priority_listings': listings_df[listings_df['seo_score'] < 70].sort_values('seo_score'),
        'opportunities': {
            'missing_tags': listings_df[listings_df['Tags'].isna() | (listings_df['Tags'].str.len() < 10)],
            'short_description': listings_df[listings_df['Description'].str.len() < 500],
            'few_images': listings_df[listings_df['Num_Images'] < 5],
            'short_title': listings_df[listings_df['Title'].str.len() < 80]
        }
    }
    
    return opportunities


# ==================== DISTRIBUTION PLOTS ====================

def plot_seo_score_distribution(seo_scores):
    """Visualize SEO score distribution"""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=seo_scores,
        nbinsx=20,
        marker_color='#9b59b6',
        opacity=0.75
    ))
    
    fig.add_vline(x=np.mean(seo_scores), line_dash="dash", line_color="red", 
                  annotation_text=f"Average: {np.mean(seo_scores):.1f}")
    
    fig.update_layout(
        title='SEO Score Distribution',
        xaxis_title='SEO Score',
        yaxis_title='Number of Listings',
        height=400
    )
    
    return fig


# ==================== MAIN APP ====================

# Header
st.markdown('<h1 class="main-header">🔍 SEO Analyzer</h1>', unsafe_allow_html=True)

# Check data
if not check_data_availability():
    st.stop()

# Load data
listings_df = load_and_prepare_listings(st.session_state['listings_df'])
sales_df = st.session_state.get('sales_df', None)

# Sidebar info
st.sidebar.markdown("### 👤 User Info")
st.sidebar.info(f"📧 {user_email}")
st.sidebar.success(f"💎 Status: {'Premium' if is_premium else 'Free'}")

if not is_premium:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚀 Upgrade Benefits")
    st.sidebar.markdown("""
    **Premium Features:**
    - 📊 SEO vs Sales correlation
    - 🎯 Advanced recommendations
    - 📸 Image performance analysis
    - 🏷️ Tag performance tracking
    - ⚠️ Zero-sales alerts
    """)
    if st.sidebar.button("💎 Upgrade Now", type="primary", use_container_width=True):
        st.switch_page("pages/Premium.py")

# Calculate SEO scores
st.markdown("### 🔄 Analyzing your listings...")
progress_bar = st.progress(0)

seo_results = []
for idx, row in listings_df.iterrows():
    result = calculate_enhanced_seo_score(row)
    seo_results.append(result)
    progress_bar.progress((idx + 1) / len(listings_df))

progress_bar.empty()

# Add scores to dataframe
listings_df['SEO_Score'] = [r['score'] for r in seo_results]
listings_df['SEO_Grade'] = [r['grade'] for r in seo_results]
listings_df['SEO_Issues'] = [r['issues'] for r in seo_results]
listings_df['SEO_Recommendations'] = [r['recommendations'] for r in seo_results]

seo_scores = listings_df['SEO_Score'].tolist()
avg_score = np.mean(seo_scores)

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview", 
    "📝 Titles", 
    "🏷️ Tags", 
    "📸 Images",
    "📈 Performance",
    "🤖 Recommendations"
])

# ==================== TAB 1: OVERVIEW ====================
with tab1:
    st.markdown("## 📊 SEO Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average SEO Score", f"{avg_score:.1f}/100")
    
    with col2:
        excellent = sum(1 for s in seo_scores if s >= 80)
        st.metric("Excellent Listings", excellent, delta=f"{excellent/len(seo_scores)*100:.0f}%")
    
    with col3:
        to_improve = sum(1 for s in seo_scores if s < 70)
        st.metric("Needs Improvement", to_improve, delta=f"{to_improve/len(seo_scores)*100:.0f}%", delta_color="inverse")
    
    with col4:
        st.metric("Total Listings", len(listings_df))
    
    # Score distribution
    st.plotly_chart(plot_seo_score_distribution(seo_scores), use_container_width=True)
    
    # Quick stats
    st.markdown("---")
    st.markdown("### 📋 Quick Stats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h4>🏆 Top Performer</h4>
        <p><strong>{listings_df.nlargest(1, 'SEO_Score')['Title'].values[0][:50]}...</strong></p>
        <p>Score: {listings_df['SEO_Score'].max():.0f}/100</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h4>📉 Needs Most Work</h4>
        <p><strong>{listings_df.nsmallest(1, 'SEO_Score')['Title'].values[0][:50]}...</strong></p>
        <p>Score: {listings_df['SEO_Score'].min():.0f}/100</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        improvement_potential = (100 - avg_score) * len(listings_df)
        st.markdown(f"""
        <div class="metric-card">
        <h4>💡 Improvement Potential</h4>
        <p><strong>{improvement_potential:.0f}</strong> total points</p>
        <p>Average gain: {100 - avg_score:.1f} pts/listing</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Top/Bottom listings
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top 5 Listings")
        top5 = listings_df.nlargest(5, 'SEO_Score')[['Title', 'SEO_Score', 'SEO_Grade']]
        top5['SEO_Score'] = top5['SEO_Score'].apply(lambda x: f"{x:.0f}/100")
        st.dataframe(top5, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### ⚠️ Bottom 5 Listings")
        bottom5 = listings_df.nsmallest(5, 'SEO_Score')[['Title', 'SEO_Score', 'SEO_Grade']]
        bottom5['SEO_Score'] = bottom5['SEO_Score'].apply(lambda x: f"{x:.0f}/100")
        st.dataframe(bottom5, use_container_width=True, hide_index=True)

# ==================== TAB 2: TITLES ====================
with tab2:
    st.markdown("## 📝 Title Analysis")
    
    title_analysis = analyze_titles(listings_df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_title_length_analysis(title_analysis), use_container_width=True)
    
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Avg Length", f"{title_analysis['avg_length']:.0f} chars")
            st.metric("Avg Words", f"{title_analysis['avg_words']:.1f}")
        
        with col_b:
            st.metric("Optimal Titles", f"{title_analysis['optimal_length']}")
            st.metric("Too Short", f"{title_analysis['too_short']}")
    
    # Top keywords
    st.markdown("---")
    with st.expander("🔑 Top 20 Keywords in Titles"):
        keywords_df = pd.DataFrame(title_analysis['top_keywords'], columns=['Keyword', 'Frequency'])
        st.dataframe(keywords_df, use_container_width=True, hide_index=True)

# ==================== TAB 3: TAGS ====================
with tab3:
    st.markdown("## 🏷️ Tag Analysis")
    
    tag_analysis = analyze_tags(listings_df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg Tags/Listing", f"{tag_analysis['avg_tags_per_listing']:.1f}")
    
    with col2:
        st.metric("Listings with 13 Tags", tag_analysis['max_tags_listings'],
                 delta=f"{tag_analysis['max_tags_listings']/len(listings_df)*100:.0f}%")
    
    with col3:
        st.metric("Unique Tags", tag_analysis['total_unique_tags'])
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(plot_tag_frequency(tag_analysis), use_container_width=True)
    
    with col2:
        if sales_df is not None:
            tag_perf = analyze_tag_performance(listings_df, sales_df)
            if tag_perf:
                st.plotly_chart(plot_tag_performance(tag_perf), use_container_width=True)
            else:
                st.info("💡 Not enough data to analyze tag performance")
        else:
            st.info("💡 Upload sales data to see best performing tags")

# ==================== TAB 4: IMAGES ====================
with tab4:
    st.markdown("## 📸 Image Analysis")
    
    image_analysis = analyze_images(listings_df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Avg Images/Listing", f"{image_analysis['avg_images']:.1f}")
    
    with col2:
        st.metric("Listings with 10 Images", image_analysis['max_images_listings'],
                 delta=f"{image_analysis['max_images_listings']/len(listings_df)*100:.0f}%")
    
    with col3:
        st.metric("Less than 5 Images", image_analysis['under_5_images'],
                 delta=f"{image_analysis['under_5_images']/len(listings_df)*100:.0f}%",
                 delta_color="inverse")
    
    # Image-sales correlation
    if sales_df is not None:
        st.markdown("---")
        image_corr = correlate_images_to_sales(listings_df, sales_df)
        if image_corr is not None:
            st.plotly_chart(plot_image_correlation(image_corr), use_container_width=True)
            
            st.markdown("""
            <div class="info-box">
            💡 <strong>Insight:</strong> Listings with more images typically generate more sales. 
            Aim for at least 7-10 high-quality images per listing.
            </div>
            """, unsafe_allow_html=True)

# ==================== TAB 5: PERFORMANCE ====================
with tab5:
    st.markdown("## 📈 SEO Performance Analysis")
    
    if is_premium:
        if sales_df is not None:
            st.success("💎 **Premium Analytics Unlocked**")
            
            # Merge sales data
            item_name_col = 'Item Name' if 'Item Name' in sales_df.columns else 'TITRE'
            
            sales_summary = sales_df.groupby(item_name_col).agg({
                'Quantity': 'sum',
                'Price': 'sum'
            }).reset_index()
            sales_summary.columns = ['Title', 'Sales_Count', 'Revenue']
            
            seo_analysis = listings_df.merge(sales_summary, on='Title', how='left')
            seo_analysis['Sales_Count'] = seo_analysis['Sales_Count'].fillna(0)
            seo_analysis['Revenue'] = seo_analysis['Revenue'].fillna(0)
            
            # SEO vs Sales correlation
            st.markdown("### 📊 SEO Score vs Sales Correlation")
            
            fig = px.scatter(
                seo_analysis,
                x='SEO_Score',
                y='Sales_Count',
                size='Revenue',
                hover_data=['Title'],
                title='SEO Score Impact on Sales',
                labels={'SEO_Score': 'SEO Score', 'Sales_Count': 'Number of Sales'},
                color='SEO_Score',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Best-sellers vs non-sellers
            st.markdown("---")
            st.markdown("### 🎯 Best-Sellers vs Non-Sellers")
            
            threshold = seo_analysis['Sales_Count'].quantile(0.7)
            best_sellers = seo_analysis[seo_analysis['Sales_Count'] >= threshold]
            non_sellers = seo_analysis[seo_analysis['Sales_Count'] == 0]
            
            if len(best_sellers) > 0 or len(non_sellers) > 0:
                comparison = pd.DataFrame({
                    'Category': ['Best-Sellers', 'Zero Sales'],
                    'Avg SEO Score': [
                        best_sellers['SEO_Score'].mean() if len(best_sellers) > 0 else 0,
                        non_sellers['SEO_Score'].mean() if len(non_sellers) > 0 else 0
                    ],
                    'Count': [len(best_sellers), len(non_sellers)]
                })
                
                fig = px.bar(
                    comparison,
                    x='Category',
                    y='Avg SEO Score',
                    text='Avg SEO Score',
                    title="SEO Score: Sold vs Not Sold",
                    color='Avg SEO Score',
                    color_continuous_scale='RdYlGn'
                )
                fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            # Zero-sales alert
            if len(non_sellers) > 0:
                st.markdown("---")
                st.markdown("### ⚠️ Listings with Zero Sales")
                
                st.markdown(f"""
                <div class="warning-box">
                <strong>Action Needed:</strong> {len(non_sellers)} listings have <strong>0 sales</strong>.<br>
                Average SEO Score: {non_sellers['SEO_Score'].mean():.1f}/100<br>
                <strong>Recommendation:</strong> Optimize titles, add more photos, review pricing.
                </div>
                """, unsafe_allow_html=True)
                
                display_zero = non_sellers.nsmallest(10, 'SEO_Score')[['Title', 'SEO_Score', 'Price', 'Num_Images']]
                display_zero['SEO_Score'] = display_zero['SEO_Score'].apply(lambda x: f"{x:.0f}/100")
                display_zero['Price'] = display_zero['Price'].apply(lambda x: f"${x:.2f}")
                st.dataframe(display_zero, use_container_width=True, hide_index=True)
            
            # Variations analysis
            if 'Variations' in sales_df.columns:
                st.markdown("---")
                st.markdown("### 🎨 Variation Performance")
                
                var_analysis = analyze_variations(sales_df)
                
                if var_analysis:
                    for var_type, values in var_analysis.items():
                        with st.expander(f"📊 {var_type}"):
                            var_df = pd.DataFrame(values, columns=['Value', 'Sales'])
                            
                            fig = px.bar(
                                var_df,
                                x='Value',
                                y='Sales',
                                title=f"Performance by {var_type}",
                                color='Sales',
                                color_continuous_scale='Blues'
                            )
                            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.warning("📊 Upload Sold Items CSV to unlock sales correlation analysis")
    
    else:
        # Premium CTA
        st.markdown("""
        <div class="premium-lock">
            <h3 style="margin-bottom: 1rem;">💎 Unlock Advanced Performance Analytics</h3>
            <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
                Get insights on what drives sales:
            </p>
            <ul style="text-align: left; max-width: 600px; margin: 20px auto; font-size: 1rem;">
                <li>🎯 SEO Score vs Sales correlation</li>
                <li>📊 Best-sellers vs Non-sellers comparison</li>
                <li>📸 Image impact on performance</li>
                <li>⚠️ Zero-sales listings identification</li>
                <li>🎨 Variation performance analysis</li>
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

# ==================== TAB 6: RECOMMENDATIONS ====================
with tab6:
    st.markdown("## 🤖 AI-Powered Recommendations")
    
    if is_premium:
        st.success("💎 **Premium Recommendations**")
        
        # Identify opportunities
        opportunities = identify_seo_opportunities(listings_df, seo_scores)
        
        st.markdown("### 🎯 Priority Optimization Targets")
        
        # Top 5 worst performers
        worst_performers = listings_df.nsmallest(5, 'SEO_Score')
        
        for idx, row in worst_performers.iterrows():
            st.markdown(f"""
            <div class="warning-box">
            <strong>📝 {row['Title'][:60]}...</strong><br>
            SEO Score: <strong>{row['SEO_Score']:.0f}/100</strong> | 
            Grade: {row['SEO_Grade']} | 
            Images: {row['Num_Images']}<br>
            <strong>Top Priority Actions:</strong>
            <ul>
            {''.join(['<li>' + rec + '</li>' for rec in row['SEO_Recommendations'][:3]])}
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Opportunities breakdown
        st.markdown("---")
        st.markdown("### 💡 Optimization Opportunities")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Tags to Optimize", len(opportunities['opportunities']['missing_tags']))
            st.metric("Short Descriptions", len(opportunities['opportunities']['short_description']))
        
        with col2:
            st.metric("Few Images", len(opportunities['opportunities']['few_images']))
            st.metric("Short Titles", len(opportunities['opportunities']['short_title']))
        
        # General recommendations
        st.markdown("---")
        st.markdown("### 📋 General Improvements")
        
        if avg_score < 70:
            st.markdown(f"""
            <div class="warning-box">
            ⚠️ <strong>Your average SEO score is low ({avg_score:.1f}/100)</strong><br>
            <strong>Priority:</strong> Focus on improving title quality and tag usage across all listings.
            </div>
            """, unsafe_allow_html=True)
        
        if listings_df['Num_Images'].mean() < 5:
            st.markdown(f"""
            <div class="info-box">
            📸 <strong>Add more photos!</strong><br>
            Listings with 5+ photos typically perform better. 
            Average: {listings_df['Num_Images'].mean():.1f} photos per listing.
            </div>
            """, unsafe_allow_html=True)
        
        avg_tags = listings_df['Tags'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) else 0).mean()
        if avg_tags < 10:
            st.markdown(f"""
            <div class="info-box">
            🏷️ <strong>Use all 13 tag slots</strong><br>
            You're averaging {avg_tags:.1f} tags per listing. Etsy allows 13 tags - use them all!
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Premium CTA
        st.markdown("""
        <div class="premium-lock">
            <h3 style="margin-bottom: 1rem;">💎 Unlock AI Recommendations</h3>
            <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
                Get personalized optimization strategies:
            </p>
            <ul style="text-align: left; max-width: 600px; margin: 20px auto; font-size: 1rem;">
                <li>✅ Top 5 listings needing immediate optimization</li>
                <li>✅ Priority action lists per listing</li>
                <li>✅ General SEO improvement strategies</li>
                <li>✅ Photo and tag optimization tips</li>
                <li>✅ Keyword suggestions based on your niche</li>
                <li>✅ Variation performance insights</li>
            </ul>
            <p style="font-size: 1.2rem; font-weight: bold; margin-top: 2rem;">
                Only $9/month
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Upgrade Now", type="primary", use_container_width=True):
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
    if st.button("👥 Customer Intelligence", use_container_width=True):
        st.switch_page("pages/etsy_customer_intelligence.py")

st.markdown("""
<div style='text-align: center; color: #666; padding: 20px; margin-top: 2rem;'>
    <p><strong>Etsy Dashboard</strong> - SEO Analyzer v2.0 (Enriched)</p>
    <p style='font-size: 0.9em;'>Optimize your listings to rank higher in Etsy search</p>
</div>
""", unsafe_allow_html=True)