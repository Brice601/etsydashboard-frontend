"""
Main Dashboard Page
Hub for accessing Finance, Customer, and SEO dashboards
"""

import streamlit as st
from components.ui_elements import render_header, render_feature_card, render_cta, render_badge
from components.seo_meta import hide_streamlit_elements
from utils.api_client import get_api_client

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Dashboard - Etsy Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit elements
hide_streamlit_elements()

# ==================== AUTHENTICATION CHECK ====================
if 'user_id' not in st.session_state or not st.session_state.user_id:
    st.warning("🔒 Please log in to access your dashboard")
    st.markdown("""
        <meta http-equiv="refresh" content="2;url=/auth">
    """, unsafe_allow_html=True)
    st.info("🔄 Redirecting to login...")
    st.stop()

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .dashboard-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .dashboard-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-top: 4px solid;
        position: relative;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    .dashboard-card.finance {
        border-top-color: #27ae60;
    }
    
    .dashboard-card.customer {
        border-top-color: #3498db;
    }
    
    .dashboard-card.seo {
        border-top-color: #9b59b6;
    }
    
    .dashboard-card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .dashboard-card-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-card-description {
        color: #7f8c8d;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    .dashboard-card-features {
        list-style: none;
        padding: 0;
        margin: 1.5rem 0;
    }
    
    .dashboard-card-features li {
        padding: 0.5rem 0;
        color: #2c3e50;
    }
    
    .dashboard-card-features li:before {
        content: "✅ ";
        margin-right: 0.5rem;
    }
    
    .dashboard-card-features li.premium:before {
        content: "🔒 ";
    }
    
    .access-button {
        display: block;
        background: #667eea;
        color: white;
        padding: 1rem;
        border-radius: 50px;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .access-button:hover {
        background: #5568d3;
        transform: scale(1.02);
    }
    
    .access-button.finance {
        background: #27ae60;
    }
    
    .access-button.finance:hover {
        background: #229954;
    }
    
    .access-button.customer {
        background: #3498db;
    }
    
    .access-button.customer:hover {
        background: #2980b9;
    }
    
    .access-button.seo {
        background: #9b59b6;
    }
    
    .access-button.seo:hover {
        background: #8e44ad;
    }
    
    .premium-banner {
        background: linear-gradient(135deg, #F56400 0%, #ff7a1a 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 3rem 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== USER INFO ====================
user_email = st.session_state.get('email', 'User')
is_premium = st.session_state.get('is_premium', False)

# ==================== HEADER ====================
st.markdown(f"""
    <div class="dashboard-hero">
        <div class="dashboard-title">Welcome back, {user_email.split('@')[0].capitalize()}! 👋</div>
        <div class="dashboard-subtitle">
            Access your Etsy analytics dashboards
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================== QUICK STATS ====================
st.markdown("### 📊 Your Quick Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Analyses This Week</div>
            <div class="stat-value">7</div>
            <div class="stat-label" style="font-size: 0.8rem; margin-top: 0.5rem;">
                3 remaining
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Account Type</div>
            <div class="stat-value" style="font-size: 1.5rem;">
                """ + ("Premium" if is_premium else "Free") + """
            </div>
            <div class="stat-label" style="font-size: 0.8rem; margin-top: 0.5rem;">
                """ + ("✨ All features" if is_premium else "10/week limit") + """
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Products Analyzed</div>
            <div class="stat-value">23</div>
            <div class="stat-label" style="font-size: 0.8rem; margin-top: 0.5rem;">
                Across all uploads
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Member Since</div>
            <div class="stat-value" style="font-size: 1.5rem;">Dec 2024</div>
            <div class="stat-label" style="font-size: 0.8rem; margin-top: 0.5rem;">
                3 days ago
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==================== DASHBOARD CARDS ====================
st.markdown("---")
st.markdown("## 🎯 Your Dashboards")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="dashboard-card finance">
            <div class="dashboard-card-icon">💰</div>
            <div class="dashboard-card-title">Finance Pro</div>
            <div class="dashboard-card-description">
                Discover your real profit margins after ALL Etsy fees
            </div>
            <ul class="dashboard-card-features">
                <li>Real profit tracking</li>
                <li>Fee breakdown analysis</li>
                <li>ROI per product</li>
                <li>Cost optimization tips</li>
                <li class="premium">AI profitability insights</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Button to Finance dashboard (would link to actual dashboard page)
    if st.button("🚀 Open Finance Pro", key="finance_btn", use_container_width=True):
        st.switch_page("pages/etsy_finance_pro.py")

with col2:
    st.markdown("""
        <div class="dashboard-card customer">
            <div class="dashboard-card-icon">👥</div>
            <div class="dashboard-card-title">Customer Intelligence</div>
            <div class="dashboard-card-description">
                Understand who buys and why they come back
            </div>
            <ul class="dashboard-card-features">
                <li>Customer lifetime value</li>
                <li>Geographic breakdown</li>
                <li>Return customer rate</li>
                <li>Review analysis</li>
                <li class="premium">Re-engagement strategies</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Open Customer Intelligence", key="customer_btn", use_container_width=True):
        st.switch_page("pages/etsy_customer_intelligence.py")

with col3:
    st.markdown("""
        <div class="dashboard-card seo">
            <div class="dashboard-card-icon">🔍</div>
            <div class="dashboard-card-title">SEO Analyzer</div>
            <div class="dashboard-card-description">
                Optimize your listings to rank higher in Etsy search
            </div>
            <ul class="dashboard-card-features">
                <li>SEO score per listing</li>
                <li>Title optimization tips</li>
                <li>Tag effectiveness</li>
                <li>Top performers</li>
                <li class="premium">Priority optimization list</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Open SEO Analyzer", key="seo_btn", use_container_width=True):
        st.switch_page("pages/etsy_seo_analyzer.py")

# # ==================== FILE UPLOAD SECTION ====================
# st.markdown("---")
# st.markdown("## 📤 Upload New Data")

# st.markdown("""
#     <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; margin: 2rem 0;">
#         <h3 style="color: #2c3e50; margin-bottom: 1rem;">Upload Your Etsy CSV Files</h3>
#         <p style="color: #7f8c8d; margin-bottom: 1.5rem;">
#             Download your sales, orders, and listings data from Etsy Shop Manager and upload here 
#             for instant analysis across all 3 dashboards.
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# col1, col2, col3 = st.columns(3)

# with col1:
#     sales_file = st.file_uploader(
#         "📊 Sales CSV",
#         type=['csv'],
#         help="Download from Shop Manager > Orders > Download CSV"
#     )

# with col2:
#     orders_file = st.file_uploader(
#         "📦 Orders CSV",
#         type=['csv'],
#         help="Download from Shop Manager > Orders"
#     )

# with col3:
#     listings_file = st.file_uploader(
#         "📝 Listings CSV",
#         type=['csv'],
#         help="Download from Shop Manager > Listings"
#     )

# if st.button("🔍 Analyze Data", type="primary", use_container_width=True):
#     if sales_file and orders_file and listings_file:
#         with st.spinner("Analyzing your data..."):
#             # Simulate analysis
#             import time
#             time.sleep(2)
#             st.success("✅ Analysis complete! Check your dashboards for insights.")
#             st.balloons()
#     else:
#         st.warning("⚠️ Please upload all 3 CSV files to proceed")

# ==================== PREMIUM UPSELL ====================
if not is_premium:
    st.markdown("---")
    st.markdown("""
        <div class="premium-banner">
            <h2 style="margin-bottom: 1rem; font-size: 2rem;">
                ✨ Upgrade to Insights Premium
            </h2>
            <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                Unlock AI-powered recommendations and unlimited analyses
            </p>
            <p style="font-size: 1rem; opacity: 0.9; margin-bottom: 2rem;">
                Only $9/month • Cancel anytime
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Upgrade to Premium", type="primary", use_container_width=True):
            st.switch_page("pages/Premium.py")

# ==================== RECENT ACTIVITY ====================
st.markdown("---")
st.markdown("### 📋 Recent Activity")

st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.08); margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 1rem 0; border-bottom: 1px solid #f0f0f0;">
            <div>
                <strong>Finance Pro Analysis</strong>
                <div style="font-size: 0.9rem; color: #7f8c8d; margin-top: 0.3rem;">
                    23 products analyzed
                </div>
            </div>
            <div style="color: #7f8c8d; font-size: 0.9rem;">
                2 hours ago
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 1rem 0; border-bottom: 1px solid #f0f0f0;">
            <div>
                <strong>Customer Intelligence</strong>
                <div style="font-size: 0.9rem; color: #7f8c8d; margin-top: 0.3rem;">
                    156 customers analyzed
                </div>
            </div>
            <div style="color: #7f8c8d; font-size: 0.9rem;">
                5 hours ago
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 1rem 0;">
            <div>
                <strong>SEO Analyzer</strong>
                <div style="font-size: 0.9rem; color: #7f8c8d; margin-top: 0.3rem;">
                    23 listings scored
                </div>
            </div>
            <div style="color: #7f8c8d; font-size: 0.9rem;">
                Yesterday
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================== HELP SECTION ====================
st.markdown("---")
st.markdown("### 💡 Need Help?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 10px; 
                    border-left: 5px solid #2196F3;">
            <h4 style="color: #1976D2; margin-bottom: 0.5rem;">📚 Documentation</h4>
            <p style="color: #424242; font-size: 0.9rem;">
                Learn how to get the most out of your dashboards
            </p>
            <a href="#" style="color: #2196F3; text-decoration: none; font-weight: bold;">
                View Guides →
            </a>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 10px; 
                    border-left: 5px solid #9c27b0;">
            <h4 style="color: #7b1fa2; margin-bottom: 0.5rem;">💬 Support</h4>
            <p style="color: #424242; font-size: 0.9rem;">
                Get help from our support team
            </p>
            <a href="mailto:support@etsydashboard.com" style="color: #9c27b0; text-decoration: none; font-weight: bold;">
                Contact Us →
            </a>
        </div>
    """, unsafe_allow_html=True)