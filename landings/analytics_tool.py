"""
Etsy Analytics Tool Landing Page
Product comparison page with features breakdown
Target keyword: "etsy analytics tool" (170 searches/month)
"""

import streamlit as st
from components.seo_meta import render_analytics_tool_seo, hide_streamlit_elements, render_schema_faq

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Etsy Analytics Tool - Track Profit, Customers & SEO | Free Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit elements
hide_streamlit_elements()

# Render SEO
render_analytics_tool_seo()

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        text-align: center;
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        margin-bottom: 1.5rem;
    }
    
    /* Comparison Table */
    .comparison-table {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .comparison-table table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .comparison-table th {
        background: #f8f9fa;
        padding: 1rem;
        text-align: left;
        font-weight: bold;
        border-bottom: 2px solid #dee2e6;
    }
    
    .comparison-table td {
        padding: 1rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .comparison-table tr:hover {
        background: #f8f9fa;
    }
    
    .feature-highlight {
        background: #667eea;
        color: white;
        font-weight: bold;
    }
    
    .check-mark {
        color: #27ae60;
        font-size: 1.3rem;
    }
    
    .cross-mark {
        color: #e74c3c;
        font-size: 1.3rem;
    }
    
    /* Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: #7f8c8d;
        line-height: 1.6;
    }
    
    /* CTA Box */
    .cta-box {
        background: linear-gradient(135deg, #F56400 0%, #ff7a1a 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 3rem 0;
    }
    
    .cta-button {
        display: inline-block;
        background: white;
        color: #F56400 !important;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        text-decoration: none;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .cta-button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    
    /* Use Case Cards */
    .usecase-card {
        background: #f8f9fa;
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .usecase-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== HERO SECTION ====================
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Complete Etsy Analytics Tool</h1>
        <p class="hero-subtitle">Finance, SEO & Customer Intelligence - All in One Dashboard</p>
        <p style="font-size: 1rem; opacity: 0.9;">
            The only tool you need to track, analyze, and optimize your Etsy shop performance
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== COMPARISON TABLE ====================
st.markdown("## 📊 How We Compare")

st.markdown("""
Not all Etsy analytics tools are created equal. Here's how our tool stacks up against the competition:
""")

comparison_data = {
    "Feature": [
        "Real Profit Tracking",
        "Customer Intelligence",
        "SEO Analysis",
        "Financial Insights",
        "AI Recommendations",
        "CSV Upload",
        "Free Tier",
        "Monthly Price"
    ],
    "Etsy Dashboard": ["✅", "✅", "✅", "✅", "✅ ($9)", "✅", "✅", "$0-9"],
    "Marmalead": ["❌", "❌", "✅", "❌", "❌", "❌", "❌", "$19"],
    "eRank": ["❌", "Limited", "✅", "❌", "❌", "Limited", "Limited", "$5.99"],
    "Alura": ["❌", "❌", "✅", "❌", "Limited", "❌", "❌", "$19.99"]
}

# Create comparison table
st.markdown('<div class="comparison-table">', unsafe_allow_html=True)

cols = st.columns(5)
headers = ["Feature", "Etsy Dashboard", "Marmalead", "eRank", "Alura"]

for i, header in enumerate(headers):
    with cols[i]:
        if i == 1:
            st.markdown(f"**{header}** 👑")
        else:
            st.markdown(f"**{header}**")

for row_idx in range(len(comparison_data["Feature"])):
    cols = st.columns(5)
    for col_idx, key in enumerate(["Feature", "Etsy Dashboard", "Marmalead", "eRank", "Alura"]):
        with cols[col_idx]:
            value = comparison_data[key][row_idx]
            if col_idx == 1:  # Our column
                st.markdown(f"**{value}**")
            else:
                st.markdown(value)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background: #e8f5e9; padding: 1rem; border-radius: 10px; border-left: 5px solid #27ae60; margin: 2rem 0;">
    <strong>✅ Why We're Different:</strong> Most Etsy tools focus only on SEO. We provide comprehensive analytics 
    across finance, customers, and SEO - all in one dashboard. Plus, we calculate your <strong>real profit margins</strong> 
    after ALL fees, not just revenue.
</div>
""", unsafe_allow_html=True)

# ==================== FEATURES BREAKDOWN ====================
st.markdown("---")
st.markdown("## 🎯 Complete Feature Breakdown")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💰</div>
            <div class="feature-title">Finance Pro</div>
            <div class="feature-description">
                <ul style="text-align: left; padding-left: 1.5rem;">
                    <li>Real profit after ALL Etsy fees</li>
                    <li>Transaction, payment, offsite ads</li>
                    <li>ROI per product tracking</li>
                    <li>Cost breakdown analysis</li>
                    <li>Margin optimization tips</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👥</div>
            <div class="feature-title">Customer Intelligence</div>
            <div class="feature-description">
                <ul style="text-align: left; padding-left: 1.5rem;">
                    <li>Customer lifetime value</li>
                    <li>Geographic breakdown</li>
                    <li>Return customer tracking</li>
                    <li>Review sentiment analysis</li>
                    <li>Buyer behavior patterns</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">SEO Analyzer</div>
            <div class="feature-description">
                <ul style="text-align: left; padding-left: 1.5rem;">
                    <li>SEO score per listing</li>
                    <li>Title optimization tips</li>
                    <li>Tag effectiveness analysis</li>
                    <li>Keyword ranking insights</li>
                    <li>Competitor benchmarking</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==================== USE CASES ====================
st.markdown("---")
st.markdown("## 💡 Perfect For Etsy Sellers Who Want To...")

st.markdown("""
    <div class="usecase-card">
        <div class="usecase-title">📈 Understand Real Profitability</div>
        <p>Stop guessing which products make money. See exact profit margins after ALL fees (transaction, payment, offsite ads, shipping). 
        Identify your most profitable products and double down on what works.</p>
    </div>
    
    <div class="usecase-card">
        <div class="usecase-title">👥 Track Customer Behavior</div>
        <p>Know who's buying, where they're from, and whether they come back. Calculate customer lifetime value and 
        identify your best customer segments. Build loyalty strategies based on data, not guesses.</p>
    </div>
    
    <div class="usecase-card">
        <div class="usecase-title">🔍 Optimize SEO Strategy</div>
        <p>Get SEO scores for every listing with actionable tips to improve. See which titles and tags drive the most traffic. 
        Rank higher in Etsy search and get discovered by more buyers.</p>
    </div>
    
    <div class="usecase-card">
        <div class="usecase-title">⚡ Make Data-Driven Decisions</div>
        <p>Stop flying blind. Upload your Etsy data once and get instant insights across finance, customers, and SEO. 
        Make confident decisions backed by real numbers, not gut feelings.</p>
    </div>
""", unsafe_allow_html=True)

# ==================== PRICING ====================
st.markdown("---")
st.markdown("## 💸 Simple, Transparent Pricing")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="background: white; border-radius: 15px; padding: 2rem; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center;">
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">Free Forever</h3>
            <div style="font-size: 3rem; font-weight: bold; color: #27ae60; margin: 1rem 0;">
                $0
            </div>
            <p style="color: #7f8c8d; margin-bottom: 2rem;">No credit card required</p>
            <ul style="text-align: left; line-height: 2; margin-bottom: 2rem;">
                <li>✅ All 3 dashboards</li>
                <li>✅ Finance Pro analytics</li>
                <li>✅ Customer Intelligence</li>
                <li>✅ SEO Analyzer</li>
                <li>✅ 10 analyses/week</li>
                <li>✅ CSV uploads</li>
            </ul>
            <a href="/auth" style="display: block; background: #667eea; color: white; 
                                   padding: 1rem; border-radius: 50px; text-decoration: none; 
                                   font-weight: bold;">
                Start Free
            </a>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background: white; border-radius: 15px; padding: 2rem; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center;
                    border: 3px solid #F56400;">
            <span style="background: #F56400; color: white; padding: 0.3rem 1rem; 
                         border-radius: 20px; font-size: 0.9rem; font-weight: bold;">
                Most Popular
            </span>
            <h3 style="color: #2c3e50; margin: 1rem 0;">Insights Premium</h3>
            <div style="font-size: 3rem; font-weight: bold; color: #667eea; margin: 1rem 0;">
                $9
            </div>
            <p style="color: #7f8c8d; margin-bottom: 2rem;">per month</p>
            <ul style="text-align: left; line-height: 2; margin-bottom: 2rem;">
                <li>✅ Everything in Free</li>
                <li>✨ Unlimited analyses</li>
                <li>✨ AI-powered recommendations</li>
                <li>✨ Priority optimization lists</li>
                <li>✨ Advanced profitability insights</li>
                <li>✨ Customer re-engagement strategies</li>
            </ul>
            <a href="/auth" style="display: block; background: #F56400; color: white; 
                                   padding: 1rem; border-radius: 50px; text-decoration: none; 
                                   font-weight: bold;">
                Upgrade to Premium
            </a>
        </div>
    """, unsafe_allow_html=True)

# ==================== CTA ====================
st.markdown("""
    <div class="cta-box">
        <h2 style="margin-bottom: 1rem; font-size: 2.5rem;">Ready to Transform Your Etsy Shop?</h2>
        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">
            Join hundreds of Etsy sellers using data to grow their business
        </p>
        <p style="font-size: 1rem; opacity: 0.9; margin-bottom: 2rem;">
            ✅ 100% Free to Start • No Credit Card • 3 Complete Dashboards
        </p>
        <a href="/auth" class="cta-button">Get Started Free →</a>
    </div>
""", unsafe_allow_html=True)

# ==================== SEO CONTENT ====================
st.markdown("---")
st.markdown("## What is an Etsy Analytics Tool?")

st.markdown("""
An **Etsy analytics tool** helps sellers track and analyze their shop performance beyond what Etsy's native Stats dashboard provides. 
While Etsy gives you basic metrics like views and favorites, a comprehensive analytics tool provides deeper insights into:

### Financial Performance
- Real profit margins after ALL fees (transaction, payment, offsite ads)
- Cost breakdowns by product
- ROI tracking
- Revenue trends and projections

### Customer Insights
- Customer lifetime value
- Repeat purchase rates
- Geographic distribution
- Buying patterns and preferences

### SEO Optimization
- Listing-level SEO scores
- Keyword effectiveness
- Title and tag optimization
- Competitor benchmarking

### Why You Need One
Etsy's built-in Stats are limited. They show you surface-level metrics but don't help you answer critical questions like:
- Which products are actually profitable after all costs?
- Where should I focus my marketing efforts?
- How can I improve my search rankings?
- What pricing strategy maximizes profit?

A dedicated analytics tool fills these gaps with actionable insights.
""")

st.markdown("### Best Etsy Analytics Tools in 2025")

st.markdown("""
The Etsy analytics landscape has several players, each with different strengths:

**Finance-Focused Tools (like ours)**
- Best for: Sellers who want to understand real profitability
- Strengths: Accurate fee calculations, margin tracking, ROI analysis
- Ideal user: Serious sellers focused on sustainable growth

**SEO-Focused Tools (Marmalead, eRank)**
- Best for: Sellers primarily focused on search optimization
- Strengths: Keyword research, tag analysis, competitor tracking
- Limitation: Limited financial insights

**All-in-One Tools (rare)**
- Best for: Sellers who want comprehensive analytics without multiple subscriptions
- Strengths: Finance + SEO + Customer insights in one place
- Example: Our Etsy Dashboard

Most sellers benefit most from an all-in-one solution that covers finance, customers, and SEO rather than juggling multiple specialized tools.
""")

# ==================== FAQ ====================
st.markdown("---")
st.markdown("## ❓ Frequently Asked Questions")

faqs = [
    {
        "question": "What makes this different from other Etsy analytics tools?",
        "answer": "Most Etsy tools focus only on SEO. We provide comprehensive analytics across finance, customers, and SEO in one dashboard. Plus, we calculate your real profit margins after ALL fees (transaction, payment, offsite ads), not just revenue. This gives you a complete picture of your shop's health."
    },
    {
        "question": "Do I need technical skills to use this tool?",
        "answer": "No! Simply download your CSV files from Etsy Shop Manager and upload them to our dashboard. The tool automatically analyzes your data and presents insights in easy-to-understand visualizations. No coding or technical knowledge required."
    },
    {
        "question": "How is the free tier different from premium?",
        "answer": "The free tier includes all 3 dashboards (Finance, Customer, SEO) with up to 10 analyses per week. Premium ($9/month) adds unlimited analyses, AI-powered recommendations, priority optimization lists, and advanced profitability insights. Start free and upgrade only if you need the premium features."
    },
    {
        "question": "Is my data secure?",
        "answer": "Yes. We use bank-level encryption to protect your data. Your CSV files are processed securely and never shared with third parties. You can delete your data at any time from your account settings."
    },
    {
        "question": "Can I cancel anytime?",
        "answer": "Yes. If you upgrade to Premium, you can cancel anytime with no penalties or fees. Your subscription will remain active until the end of your billing period, then automatically revert to the free tier."
    }
]

for faq in faqs:
    with st.expander(f"**{faq['question']}**"):
        st.write(faq['answer'])

# Render FAQ schema
render_schema_faq(faqs)

# ==================== FINAL CTA ====================
st.markdown("""
    <div style="background: #f8f9fa; padding: 3rem 2rem; text-align: center; 
                border-radius: 15px; margin: 3rem 0;">
        <h2 style="color: #2c3e50; margin-bottom: 1rem;">
            Stop Guessing. Start Growing.
        </h2>
        <p style="font-size: 1.1rem; color: #7f8c8d; margin-bottom: 2rem;">
            Upload your Etsy data and get instant insights across finance, customers, and SEO
        </p>
        <a href="/auth" style="display: inline-block; background: #667eea; color: white; 
                               padding: 1rem 2.5rem; border-radius: 50px; text-decoration: none; 
                               font-weight: bold; font-size: 1.1rem;">
            Analyze Your Shop Free →
        </a>
    </div>
""", unsafe_allow_html=True)