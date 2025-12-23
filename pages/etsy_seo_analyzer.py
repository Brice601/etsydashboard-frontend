"""
🔍 SEO Analyzer Dashboard v1.0
Optimize your Etsy listings to rank higher in search

Features:
✅ SEO score per listing (0-100)
✅ Title optimization analysis
✅ Tags performance tracking
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
    """Prepare listings data"""
    df = listings_df.copy()
    
    # Column mapping
    column_mapping = {
        'Title': 'Title', 'Titre': 'Title',
        'Price': 'Price', 'Prix': 'Price',
        'Quantity': 'Quantity', 'Stock': 'Quantity',
        'Tags': 'Tags', 'Étiquettes': 'Tags',
        'Description': 'Description',
        'Images': 'Images', 'Photos': 'Images',
        'SKU': 'SKU'
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
    
    # Count images (simplified - assume column contains count or comma-separated URLs)
    if 'Images' in df.columns:
        df['Num_Images'] = df['Images'].apply(lambda x: 
            len(str(x).split(',')) if pd.notna(x) and str(x) else 0
        )
    else:
        df['Num_Images'] = 0
    
    # Remove invalid rows
    df = df.dropna(subset=['Title'])
    
    return df


# ==================== SEO ANALYSIS FUNCTIONS ====================

def calculate_title_seo_score(title):
    """Calculate SEO score for a title (0-100)"""
    score = 0
    issues = []
    recommendations = []
    
    if pd.isna(title):
        return 0, ["❌ Missing title"], ["Add a descriptive title"]
    
    title_str = str(title)
    title_len = len(title_str)
    
    # Optimal length (Etsy allows 140 chars)
    if 100 <= title_len <= 140:
        score += 30
    elif 80 <= title_len < 100:
        score += 20
        recommendations.append("📏 Increase title length (optimal: 100-140 characters)")
    elif title_len < 80:
        score += 10
        issues.append("❌ Title too short")
        recommendations.append("📏 Extend title to 100-140 characters")
    else:
        score += 15
        issues.append("⚠️ Title too long")
        recommendations.append("✂️ Reduce to max 140 characters")
    
    # Number of keywords (separated by commas)
    keywords = [k.strip() for k in title_str.split(',') if k.strip()]
    num_keywords = len(keywords)
    
    if num_keywords >= 3:
        score += 25
    elif num_keywords >= 2:
        score += 15
        recommendations.append("📝 Add more keywords separated by commas")
    else:
        score += 5
        issues.append("❌ Not enough keywords")
        recommendations.append("📝 Use commas to separate keywords")
    
    # Presence of important keywords (generic)
    important_keywords = ['handmade', 'gift', 'vintage', 'custom', 'personalized',
                         'unique', 'jewelry', 'art', 'home', 'decor', 'wedding']
    
    title_lower = title_str.lower()
    keywords_found = sum(1 for kw in important_keywords if kw in title_lower)
    
    if keywords_found >= 2:
        score += 25
    elif keywords_found >= 1:
        score += 15
        recommendations.append("🎯 Add more relevant keywords")
    else:
        score += 5
        issues.append("❌ Missing relevant keywords")
        recommendations.append("🎯 Include keywords like 'handmade', 'gift', 'unique', etc.")
    
    # Special characters (emojis can help)
    if any(char in title_str for char in ['✨', '💎', '🎁', '❤️', '⭐']):
        score += 10
    
    # First letter capitalized
    if title_str[0].isupper():
        score += 10
    else:
        recommendations.append("🔤 Capitalize first letter")
    
    return min(score, 100), issues, recommendations


def analyze_tags(tags_str):
    """Analyze tags from a listing"""
    if pd.isna(tags_str):
        return []
    
    # Split by comma or semicolon
    tags = re.split(r'[,;]', str(tags_str))
    tags = [tag.strip().lower() for tag in tags if tag.strip()]
    
    return tags


def get_seo_category(score):
    """Return SEO category based on score"""
    if score >= 80:
        return "🟢 Excellent", "seo-score-high"
    elif score >= 60:
        return "🟡 Good", "seo-score-medium"
    elif score >= 40:
        return "🟠 Average", "seo-score-medium"
    else:
        return "🔴 Low", "seo-score-low"


def analyze_listing_performance(listings_df, sales_df):
    """Cross listings with sales to identify performance"""
    if sales_df is None:
        return None
    
    # Map column names
    product_col = 'Item Name' if 'Item Name' in sales_df.columns else 'Product'
    
    if product_col not in sales_df.columns:
        return None
    
    # Count sales per product
    sales_count = sales_df.groupby(product_col).agg({
        'Quantity': 'sum' if 'Quantity' in sales_df.columns else 'count',
        'Price': 'sum' if 'Price' in sales_df.columns else 'count'
    }).reset_index()
    
    sales_count.columns = ['Title', 'Sales_Count', 'Revenue']
    
    # Merge with listings
    performance = listings_df.merge(sales_count, on='Title', how='left')
    performance['Sales_Count'] = performance['Sales_Count'].fillna(0)
    performance['Revenue'] = performance['Revenue'].fillna(0)
    
    return performance


def extract_keywords_from_titles(titles):
    """Extract most frequent keywords from titles"""
    all_words = []
    
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
                  'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was'}
    
    for title in titles:
        if pd.notna(title):
            # Split by comma and space
            words = re.split(r'[,\s]+', str(title).lower())
            # Filter short words and stop words
            words = [w.strip() for w in words if len(w) > 3 and w not in stop_words]
            all_words.extend(words)
    
    return Counter(all_words)


# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ SEO Analysis Settings")
    
    min_score_filter = st.slider(
        "Min SEO Score",
        0, 100, 0,
        help="Filter listings by minimum SEO score"
    )
    
    show_sales = st.checkbox(
        "Show Sales Data",
        value=True,
        help="Cross-reference with sales data if available",
        disabled='sold_items_df' not in st.session_state
    )

# ==================== MAIN APP ====================

st.markdown('<h1 class="main-header">🔍 SEO Analyzer Dashboard</h1>', unsafe_allow_html=True)

# Check data availability
check_data_availability()

# Load data
listings_df = load_and_prepare_listings(st.session_state['listings_df'])

# Optional: Sales data
sales_df = None
if show_sales and 'sold_items_df' in st.session_state and st.session_state['sold_items_df'] is not None:
    sales_df = st.session_state['sold_items_df']

# Calculate SEO scores for all listings
st.info("🔍 Analyzing SEO for all listings...")

seo_results = []
for idx, row in listings_df.iterrows():
    score, issues, recs = calculate_title_seo_score(row['Title'])
    
    seo_results.append({
        'Title': row['Title'],
        'SEO_Score': score,
        'Price': row.get('Price', 0),
        'Num_Images': row.get('Num_Images', 0),
        'Tags': row.get('Tags', ''),
        'Issues': issues,
        'Recommendations': recs
    })

seo_analysis = pd.DataFrame(seo_results)

# Cross with sales if available
if sales_df is not None:
    performance_df = analyze_listing_performance(listings_df, sales_df)
    if performance_df is not None:
        seo_analysis = seo_analysis.merge(
            performance_df[['Title', 'Sales_Count', 'Revenue']], 
            on='Title', 
            how='left'
        )
        seo_analysis['Sales_Count'] = seo_analysis['Sales_Count'].fillna(0)
        seo_analysis['Revenue'] = seo_analysis['Revenue'].fillna(0)

# Apply filter
filtered_seo = seo_analysis[seo_analysis['SEO_Score'] >= min_score_filter]

st.success(f"✅ Analyzed {len(seo_analysis)} listings!")

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 SEO Overview",
    "🔍 Title Analysis",
    "🏷️ Tags Performance",
    "📈 Advanced Analytics",
    "🤖 AI Recommendations"
])

with tab1:
    st.markdown("## 📊 SEO Overview")
    
    # KPIs
    avg_score = seo_analysis['SEO_Score'].mean()
    excellent_count = len(seo_analysis[seo_analysis['SEO_Score'] >= 80])
    to_optimize_count = len(seo_analysis[seo_analysis['SEO_Score'] < 60])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average SEO Score", f"{avg_score:.1f}/100")
    
    with col2:
        excellent_pct = (excellent_count / len(seo_analysis) * 100) if len(seo_analysis) > 0 else 0
        st.metric("Excellent Listings", f"{excellent_count}", delta=f"{excellent_pct:.0f}%")
    
    with col3:
        to_optimize_pct = (to_optimize_count / len(seo_analysis) * 100) if len(seo_analysis) > 0 else 0
        st.metric("Need Optimization", f"{to_optimize_count}", 
                 delta=f"-{to_optimize_pct:.0f}%", delta_color="inverse")
    
    with col4:
        avg_images = seo_analysis['Num_Images'].mean()
        st.metric("Avg Photos", f"{avg_images:.1f}")
    
    st.markdown("---")
    
    # Score distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 SEO Score Distribution")
        
        fig = px.histogram(
            seo_analysis,
            x='SEO_Score',
            nbins=20,
            title="SEO Score Distribution",
            color_discrete_sequence=['#9b59b6']
        )
        fig.update_layout(
            xaxis_title="SEO Score",
            yaxis_title="Number of Listings",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 SEO Categories")
        
        categories = pd.cut(seo_analysis['SEO_Score'], 
                           bins=[0, 40, 60, 80, 100],
                           labels=['🔴 Low', '🟠 Average', '🟡 Good', '🟢 Excellent'])
        
        cat_counts = categories.value_counts()
        
        fig = px.pie(
            values=cat_counts.values,
            names=cat_counts.index,
            title="SEO Categories",
            color_discrete_sequence=['#dc3545', '#ffc107', '#28a745', '#9b59b6']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # All listings table
    st.markdown("### 📋 All Listings with SEO Score")
    
    display_df = filtered_seo[['Title', 'SEO_Score', 'Price', 'Num_Images']].copy()
    display_df['SEO_Score'] = display_df['SEO_Score'].apply(lambda x: f"{x:.0f}/100")
    display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.2f}")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("## 🔍 Detailed Title Analysis")
    
    # Title statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_title_len = listings_df['Title'].str.len().mean()
        st.metric("Average Length", f"{avg_title_len:.0f} chars")
    
    with col2:
        optimal_titles = len(listings_df[listings_df['Title'].str.len().between(100, 140)])
        st.metric("Optimal Length (100-140)", optimal_titles)
    
    with col3:
        short_titles = len(listings_df[listings_df['Title'].str.len() < 80])
        st.metric("Too Short (<80)", short_titles)
    
    st.markdown("---")
    
    # Title length distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📏 Title Length Distribution")
        
        fig = px.histogram(
            listings_df,
            x=listings_df['Title'].str.len(),
            nbins=20,
            title="Title Length (characters)",
            color_discrete_sequence=['#3498db']
        )
        fig.add_vline(x=100, line_dash="dash", line_color="green", 
                     annotation_text="Min optimal (100)")
        fig.add_vline(x=140, line_dash="dash", line_color="red",
                     annotation_text="Max Etsy (140)")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Length vs SEO Score")
        
        fig = px.scatter(
            seo_analysis,
            x=listings_df['Title'].str.len(),
            y='SEO_Score',
            title="Title Length Impact on SEO Score",
            color='SEO_Score',
            color_continuous_scale='RdYlGn',
            labels={'x': 'Title Length (chars)', 'y': 'SEO Score'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed listing analysis
    st.markdown("### 📝 Detailed Analysis by Listing")
    
    for idx, row in filtered_seo.head(20).iterrows():  # Limit to 20 for performance
        category, css_class = get_seo_category(row['SEO_Score'])
        
        title_preview = row['Title'][:60] + "..." if len(row['Title']) > 60 else row['Title']
        
        with st.expander(f"{category} - {title_preview} (Score: {row['SEO_Score']:.0f}/100)"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Full Title:** {row['Title']}")
                st.markdown(f"**Length:** {len(row['Title'])} characters")
                st.markdown(f"**Price:** ${row['Price']:.2f}")
                st.markdown(f"**Photos:** {row['Num_Images']}")
                
                if row['Issues']:
                    st.markdown("**⚠️ Issues:**")
                    for issue in row['Issues']:
                        st.markdown(f"- {issue}")
            
            with col2:
                st.markdown("**💡 Recommendations:**")
                if row['Recommendations']:
                    for rec in row['Recommendations']:
                        st.markdown(f"- {rec}")
                else:
                    st.success("✅ Title is well optimized!")

with tab3:
    st.markdown("## 🏷️ Tags Analysis")
    
    # Extract all tags
    all_tags = []
    for idx, row in listings_df.iterrows():
        if 'Tags' in row and pd.notna(row['Tags']):
            tags = analyze_tags(row['Tags'])
            all_tags.extend(tags)
    
    if all_tags:
        tag_counter = Counter(all_tags)
        most_common_tags = tag_counter.most_common(20)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏆 Top 20 Most Used Tags")
            
            tags_df = pd.DataFrame(most_common_tags, columns=['Tag', 'Count'])
            
            fig = px.bar(
                tags_df,
                x='Count',
                y='Tag',
                orientation='h',
                title="Most Frequent Tags",
                color='Count',
                color_continuous_scale='Purples'
            )
            fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Tag Statistics")
            
            st.metric("Unique Tags", len(tag_counter))
            st.metric("Total Tags", len(all_tags))
            st.metric("Avg per Listing", f"{len(all_tags)/len(listings_df):.1f}")
            
            st.markdown("---")
            
            st.markdown("### 🎯 Recommended Tags")
            
            recommended_tags = [
                'handmade', 'gift', 'vintage', 'custom', 'personalized',
                'unique', 'birthday', 'wedding', 'home', 'decor',
                'jewelry', 'art', 'minimalist', 'boho', 'modern'
            ]
            
            tags_present = [tag for tag in recommended_tags if tag in all_tags]
            tags_missing = [tag for tag in recommended_tags if tag not in all_tags]
            
            st.markdown("**✅ Present Tags:**")
            st.write(", ".join(tags_present) if tags_present else "None")
            
            st.markdown("**❌ Missing Tags (Opportunities):**")
            st.write(", ".join(tags_missing) if tags_missing else "All present!")
        
        # Tags by listing
        st.markdown("---")
        st.markdown("### 📋 Tags per Listing")
        
        tags_by_listing = []
        for idx, row in listings_df.iterrows():
            tags = analyze_tags(row.get('Tags', ''))
            tags_by_listing.append({
                'Title': row['Title'][:50] + "...",
                'Num_Tags': len(tags),
                'Tags': ', '.join(tags[:5]) + ('...' if len(tags) > 5 else '')
            })
        
        st.dataframe(pd.DataFrame(tags_by_listing), use_container_width=True, hide_index=True)
    
    else:
        st.warning("⚠️ No tags found in your listings. Add tags to improve SEO!")

with tab4:
    st.markdown("## 📈 Advanced Analytics")
    
    if is_premium:
        st.success("💎 **Premium Features Unlocked**")
        
        if sales_df is not None and 'Sales_Count' in seo_analysis.columns:
            # SEO Score vs Sales correlation
            st.markdown("### 🎯 SEO Score Impact on Sales")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.scatter(
                    seo_analysis,
                    x='SEO_Score',
                    y='Sales_Count',
                    size='Revenue',
                    color='SEO_Score',
                    hover_data=['Title'],
                    title="SEO Score vs Sales Count",
                    color_continuous_scale='RdYlGn',
                    labels={'Sales_Count': 'Number of Sales', 'SEO_Score': 'SEO Score'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Best-sellers vs non-sellers
                best_sellers = seo_analysis[seo_analysis['Sales_Count'] > 0]
                non_sellers = seo_analysis[seo_analysis['Sales_Count'] == 0]
                
                comparison = pd.DataFrame({
                    'Category': ['Products Sold', 'Products Not Sold'],
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
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Photos impact
            st.markdown("### 📸 Photos Impact on Sales")
            
            photo_analysis = seo_analysis.groupby('Num_Images').agg({
                'Sales_Count': 'sum',
                'Revenue': 'sum',
                'Title': 'count'
            }).reset_index()
            photo_analysis.columns = ['Photos', 'Sales', 'Revenue', 'Listings']
            
            fig = px.bar(
                photo_analysis,
                x='Photos',
                y='Sales',
                title='Sales by Number of Photos',
                color='Sales',
                color_continuous_scale='Blues',
                text='Sales'
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
            # Zero-sales alert
            zero_sales = seo_analysis[seo_analysis['Sales_Count'] == 0]
            
            if len(zero_sales) > 0:
                st.markdown("---")
                st.markdown("### ⚠️ Listings with Zero Sales")
                
                st.markdown(f"""
                <div class="warning-box">
                <strong>Action Needed:</strong> {len(zero_sales)} listings have <strong>0 sales</strong>.<br>
                Average SEO Score: {zero_sales['SEO_Score'].mean():.1f}/100<br>
                <strong>Recommendation:</strong> Optimize titles, add more photos, review pricing.
                </div>
                """, unsafe_allow_html=True)
                
                display_zero = zero_sales.nsmallest(10, 'SEO_Score')[['Title', 'SEO_Score', 'Price', 'Num_Images']]
                display_zero['SEO_Score'] = display_zero['SEO_Score'].apply(lambda x: f"{x:.0f}/100")
                display_zero['Price'] = display_zero['Price'].apply(lambda x: f"${x:.2f}")
                
                st.dataframe(display_zero, use_container_width=True, hide_index=True)
        
        else:
            st.warning("📊 Upload Sold Items CSV to unlock sales correlation analysis")
    
    else:
        # Premium CTA
        st.markdown("""
        <div class="info-box">
        💎 <strong>Premium Features Available with Insights ($9/month):</strong>
        <ul>
        <li>🎯 SEO Score vs Sales correlation</li>
        <li>📊 Best-sellers vs Non-sellers comparison</li>
        <li>📸 Photos impact on performance</li>
        <li>⚠️ Zero-sales listings identification</li>
        <li>💡 SEO optimization ROI tracking</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if sales_df is not None:
            st.markdown("### 🎯 SEO vs Sales (preview)")
            st.markdown("""
            <div style='filter: blur(8px); pointer-events: none; user-select: none;'>
                <img src='https://via.placeholder.com/800x400/f0f2f6/666?text=SEO+Score+vs+Sales+Chart' style='width: 100%; border-radius: 10px;'>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div class="premium-lock">
            <h3 style="margin-bottom: 1rem;">💎 Unlock Advanced Analytics</h3>
            <p style="font-size: 1.1rem; margin-bottom: 2rem;">
                Only $9/month
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚀 Upgrade to Premium", type="primary", use_container_width=True):
                st.switch_page("pages/Premium.py")

with tab5:
    st.markdown("## 🤖 AI-Powered Recommendations")
    
    if is_premium:
        st.success("💎 **Premium Recommendations**")
        
        # Top opportunities
        worst_performers = seo_analysis.nsmallest(5, 'SEO_Score')
        
        st.markdown("### 🎯 Top 5 Listings to Optimize")
        
        for idx, row in worst_performers.iterrows():
            st.markdown(f"""
            <div class="warning-box">
            <strong>📝 {row['Title'][:60]}...</strong><br>
            SEO Score: <strong>{row['SEO_Score']:.0f}/100</strong> | Price: ${row['Price']:.2f} | Photos: {row['Num_Images']}<br>
            <strong>Priority Actions:</strong>
            <ul>
            {''.join(['<li>' + rec + '</li>' for rec in row['Recommendations'][:3]])}
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # General recommendations
        st.markdown("---")
        st.markdown("### 💡 General SEO Improvements")
        
        if avg_score < 70:
            st.markdown("""
            <div class="warning-box">
            ⚠️ <strong>Your average SEO score is low ({:.1f}/100)</strong><br>
            <strong>Priority:</strong> Focus on improving title quality across all listings.
            </div>
            """.format(avg_score), unsafe_allow_html=True)
        
        if seo_analysis['Num_Images'].mean() < 5:
            st.markdown("""
            <div class="info-box">
            📸 <strong>Add more photos!</strong><br>
            Listings with 5+ photos typically perform better. Average: {:.1f} photos per listing.
            </div>
            """.format(seo_analysis['Num_Images'].mean()), unsafe_allow_html=True)
        
        if len(all_tags) < len(listings_df) * 10:
            st.markdown("""
            <div class="info-box">
            🏷️ <strong>Use all 13 tag slots</strong><br>
            You're averaging {:.1f} tags per listing. Etsy allows 13 tags - use them all!
            </div>
            """.format(len(all_tags) / len(listings_df)), unsafe_allow_html=True)
    
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
    <p><strong>Etsy Dashboard</strong> - SEO Analyzer v1.0</p>
    <p style='font-size: 0.9em;'>Optimize your listings to rank higher in Etsy search</p>
</div>
""", unsafe_allow_html=True)