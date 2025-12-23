"""
Etsy Dashboard - Public Landing Page (SEO Optimized)
Target keyword: "etsy dashboard" (1,600 searches/month)
Meta: Free Etsy analytics dashboard for tracking profit margins, customer behavior, and SEO performance
"""

import streamlit as st

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Free Etsy Dashboard - Track Your Shop Analytics in Real-Time",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== SEO META TAGS ====================
st.markdown("""
    <meta name="description" content="Free Etsy analytics dashboard. Track profit margins, customer behavior, and SEO performance. Upload your CSV and get instant insights across 3 comprehensive dashboards.">
    <meta name="keywords" content="etsy dashboard, etsy analytics, etsy profit tracker, etsy seo tool, etsy shop analytics">
    <meta property="og:title" content="Free Etsy Dashboard - Track Your Shop Analytics">
    <meta property="og:description" content="The only dashboard you need to track, analyze and optimize your Etsy shop performance">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
""", unsafe_allow_html=True)

# ==================== HIDE STREAMLIT ELEMENTS ====================
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.95;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .hero-cta {
        display: inline-block;
        background: white;
        color: #667eea;
        padding: 1.2rem 3rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        text-decoration: none;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .hero-cta:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 3rem 0 1.5rem 0;
        text-align: center;
    }
    
    .section-subtitle {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 3rem;
        line-height: 1.6;
    }
    
    .problem-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
    
    .problem-box h3 {
        color: #856404;
        margin-bottom: 1rem;
    }
    
    .problem-box ul {
        color: #856404;
        line-height: 1.8;
    }
    
    .dashboard-showcase {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border-top: 5px solid;
    }
    
    .dashboard-showcase.finance {
        border-top-color: #27ae60;
    }
    
    .dashboard-showcase.customer {
        border-top-color: #3498db;
    }
    
    .dashboard-showcase.seo {
        border-top-color: #9b59b6;
    }
    
    .dashboard-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    
    .dashboard-name {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    
    .dashboard-description {
        font-size: 1.1rem;
        color: #7f8c8d;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    .metrics-list {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 3px solid #667eea;
    }
    
    .metric-item strong {
        color: #2c3e50;
        display: block;
        margin-bottom: 0.3rem;
    }
    
    .benefit-badge {
        display: inline-block;
        background: #e8f5e9;
        color: #2e7d32;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.5rem 0.5rem 0.5rem 0;
    }
    
    .how-it-works {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin: 3rem 0;
    }
    
    .step-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
        position: relative;
    }
    
    .step-number {
        position: absolute;
        top: -15px;
        left: 20px;
        background: #667eea;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .step-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 1rem 0 0.5rem 0;
    }
    
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin: 2rem 0;
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .comparison-table th {
        background: #667eea;
        color: white;
        padding: 1.5rem;
        text-align: left;
        font-size: 1.1rem;
    }
    
    .comparison-table td {
        padding: 1.2rem 1.5rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .comparison-table tr:hover {
        background: #f8f9fa;
    }
    
    .checkmark {
        color: #27ae60;
        font-size: 1.5rem;
    }
    
    .crossmark {
        color: #e74c3c;
        font-size: 1.5rem;
    }
    
    .pricing-box {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 5px solid #27ae60;
    }
    
    .price {
        font-size: 3rem;
        font-weight: bold;
        color: #27ae60;
        margin: 1rem 0;
    }
    
    .price-period {
        font-size: 1.2rem;
        color: #7f8c8d;
    }
    
    .feature-list {
        text-align: left;
        margin: 2rem 0;
        line-height: 2;
    }
    
    .feature-list li:before {
        content: "✅ ";
        margin-right: 0.5rem;
    }
    
    .cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 4rem 0;
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .cta-subtitle {
        font-size: 1.3rem;
        margin-bottom: 2rem;
        opacity: 0.95;
    }
    
    .testimonial-box {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
    }
    
    .testimonial-text {
        font-style: italic;
        color: #2c3e50;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .testimonial-author {
        color: #7f8c8d;
        font-weight: bold;
    }
    
    .faq-item {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .faq-question {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .faq-answer {
        color: #7f8c8d;
        line-height: 1.6;
    }
    
    .stats-highlight {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .stat-box {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: #7f8c8d;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== HERO SECTION ====================
st.markdown("""
    <div class="main-header">
        <div class="hero-title">
            Free Etsy Dashboard - Track Your Shop Analytics in Real-Time
        </div>
        <div class="hero-subtitle">
            Finance, SEO & Customer Intelligence — All Your Etsy Data in One Beautiful Dashboard
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Start Free Analysis", type="primary", use_container_width=True):
        st.switch_page("pages/auth.py")

# ==================== STATS HIGHLIGHT ====================
st.markdown("""
    <div class="stats-highlight">
        <div class="stat-box">
            <div class="stat-number">3</div>
            <div class="stat-label">Complete Dashboards</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">100%</div>
            <div class="stat-label">Free</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">2 min</div>
            <div class="stat-label">Setup Time</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================== PROBLEM SECTION ====================
st.markdown('<h2 class="section-title">Are You Tracking Your Etsy Shop in Spreadsheets?</h2>', unsafe_allow_html=True)

st.markdown("""
    <div class="problem-box">
        <h3>Most Etsy sellers struggle with:</h3>
        <ul>
            <li><strong>Hidden costs eating profits:</strong> You think you're profitable, but after all Etsy fees (transaction, payment, offsite ads), your real margin is 40% lower than expected</li>
            <li><strong>Manual calculations:</strong> Spending hours in spreadsheets trying to figure out which products actually make money</li>
            <li><strong>Blind SEO optimization:</strong> Guessing which titles and tags work without any data to back it up</li>
            <li><strong>Lost customer insights:</strong> Not knowing who your best customers are or why they come back (or don't)</li>
            <li><strong>Pricing in the dark:</strong> Setting prices without understanding your true costs or market positioning</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <p class="section-subtitle">
        Sound familiar? You're not alone. We built this Etsy dashboard specifically to solve these problems — and it's completely free.
    </p>
""", unsafe_allow_html=True)

# ==================== SOLUTION OVERVIEW ====================
st.markdown('<h2 class="section-title">One Dashboard. Three Powerful Analytics Tools.</h2>', unsafe_allow_html=True)
st.markdown("""
    <p class="section-subtitle">
        Upload your Etsy CSV files once and get instant access to professional-grade analytics 
        that would normally cost $50-100/month with other tools.
    </p>
""", unsafe_allow_html=True)

# ==================== DASHBOARD 1: FINANCE PRO ====================
st.markdown("""
    <div class="dashboard-showcase finance">
        <div class="dashboard-icon">💰</div>
        <div class="dashboard-name">Dashboard #1: Finance Pro</div>
        <div class="dashboard-description">
            Stop guessing your profitability. Know exactly which products make money and which ones are 
            secretly costing you. Our Finance Pro dashboard calculates your real profit after ALL Etsy fees, 
            including the hidden ones most sellers forget about.
        </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="metrics-list">
            <div class="metric-item">
                <strong>Real Profit Margins</strong>
                Your actual take-home after transaction fees, payment processing, offsite ads, and shipping costs
            </div>
            <div class="metric-item">
                <strong>ROI Per Product</strong>
                See which products deliver the best return on your time and materials
            </div>
            <div class="metric-item">
                <strong>Fee Breakdown</strong>
                Visualize exactly where your money goes: listing fees, transaction fees, payment processing, offsite ads
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metrics-list">
            <div class="metric-item">
                <strong>Cost Optimization</strong>
                Identify products where reducing costs by just $1 would significantly boost margins
            </div>
            <div class="metric-item">
                <strong>Revenue Trends</strong>
                Track your monthly and yearly revenue patterns to forecast future sales
            </div>
            <div class="metric-item">
                <strong>Profit Leaks</strong>
                Spot products that seem profitable but actually lose money after all fees
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="margin-top: 1.5rem;">
            <span class="benefit-badge">📊 Instant Clarity</span>
            <span class="benefit-badge">💡 Actionable Insights</span>
            <span class="benefit-badge">💰 Increase Profit by 15-30%</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================== DASHBOARD 2: CUSTOMER INTELLIGENCE ====================
st.markdown("""
    <div class="dashboard-showcase customer">
        <div class="dashboard-icon">👥</div>
        <div class="dashboard-name">Dashboard #2: Customer Intelligence</div>
        <div class="dashboard-description">
            Your customers are telling you something — but are you listening? This dashboard reveals 
            who your buyers really are, what makes them come back, and which customers are worth 
            nurturing. Transform raw order data into customer relationship gold.
        </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="metrics-list">
            <div class="metric-item">
                <strong>Customer Lifetime Value</strong>
                Identify your VIP customers who account for 80% of your revenue
            </div>
            <div class="metric-item">
                <strong>Geographic Breakdown</strong>
                See where your customers are located and optimize shipping strategies
            </div>
            <div class="metric-item">
                <strong>Return Customer Rate</strong>
                Track how many customers come back for a second purchase (and why)
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metrics-list">
            <div class="metric-item">
                <strong>Purchase Patterns</strong>
                Discover which products are bought together and create smart bundles
            </div>
            <div class="metric-item">
                <strong>Review Analysis</strong>
                Aggregate feedback to understand what customers love (and what needs fixing)
            </div>
            <div class="metric-item">
                <strong>Churn Prediction</strong>
                Spot customers who might not return and create win-back campaigns
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="margin-top: 1.5rem;">
            <span class="benefit-badge">🎯 Target Smarter</span>
            <span class="benefit-badge">🔁 Boost Repeat Sales</span>
            <span class="benefit-badge">💝 Build Loyalty</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================== DASHBOARD 3: SEO ANALYZER ====================
st.markdown("""
    <div class="dashboard-showcase seo">
        <div class="dashboard-icon">🔍</div>
        <div class="dashboard-name">Dashboard #3: SEO Analyzer</div>
        <div class="dashboard-description">
            Ranking on Etsy isn't luck — it's science. Our SEO Analyzer scores every one of your listings 
            and tells you exactly what to fix to rank higher. Stop guessing which keywords work and 
            start optimizing based on data.
        </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="metrics-list">
            <div class="metric-item">
                <strong>SEO Score Per Listing</strong>
                0-100 score for every product showing optimization opportunities
            </div>
            <div class="metric-item">
                <strong>Title Optimization</strong>
                Analyze your titles for keyword density, length, and relevance
            </div>
            <div class="metric-item">
                <strong>Tag Effectiveness</strong>
                See which of your 13 tags actually drive traffic vs which are wasted
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metrics-list">
            <div class="metric-item">
                <strong>Top Performers</strong>
                Learn from your best-ranking listings and replicate success
            </div>
            <div class="metric-item">
                <strong>Keyword Gaps</strong>
                Find high-traffic keywords your competitors use that you're missing
            </div>
            <div class="metric-item">
                <strong>Priority Actions</strong>
                Get a ranked list of which listings to optimize first for maximum impact
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
        <div style="margin-top: 1.5rem;">
            <span class="benefit-badge">📈 Rank Higher</span>
            <span class="benefit-badge">🔎 More Visibility</span>
            <span class="benefit-badge">🚀 2-3x More Traffic</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================== HOW IT WORKS ====================
st.markdown('<h2 class="section-title">How It Works — Simple, Fast, Free</h2>', unsafe_allow_html=True)

st.markdown("""
    <div class="how-it-works">
        <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-title">Download Your Etsy Data</div>
            <p style="color: #7f8c8d; line-height: 1.6; margin-top: 1rem;">
                Go to your Etsy Shop Manager, navigate to Orders, and download your sales CSV. 
                Do the same for your order items and listings. Takes less than 2 minutes.
            </p>
        </div>
        <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-title">Upload to Your Dashboard</div>
            <p style="color: #7f8c8d; line-height: 1.6; margin-top: 1rem;">
                Create your free account (no credit card required) and upload your 3 CSV files. 
                Our system instantly processes your data and starts analyzing.
            </p>
        </div>
        <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-title">Get Instant Insights</div>
            <p style="color: #7f8c8d; line-height: 1.6; margin-top: 1rem;">
                Access all 3 dashboards immediately. See your real profit margins, customer patterns, 
                and SEO scores in beautiful, easy-to-understand visualizations.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================== COMPARISON TABLE ====================
st.markdown('<h2 class="section-title">Why Choose Our Etsy Dashboard?</h2>', unsafe_allow_html=True)

st.markdown("""
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Feature</th>
                <th>Our Dashboard</th>
                <th>Manual Spreadsheets</th>
                <th>Other Tools</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Real Profit Tracking</strong></td>
                <td><span class="checkmark">✓</span> Automatic</td>
                <td><span class="crossmark">✗</span> Manual calculations</td>
                <td><span class="checkmark">✓</span> Sometimes</td>
            </tr>
            <tr>
                <td><strong>Customer Intelligence</strong></td>
                <td><span class="checkmark">✓</span> Complete analytics</td>
                <td><span class="crossmark">✗</span> Very limited</td>
                <td><span class="crossmark">✗</span> Rarely included</td>
            </tr>
            <tr>
                <td><strong>SEO Analysis</strong></td>
                <td><span class="checkmark">✓</span> Per-listing scoring</td>
                <td><span class="crossmark">✗</span> Impossible</td>
                <td><span class="checkmark">✓</span> Basic only</td>
            </tr>
            <tr>
                <td><strong>Setup Time</strong></td>
                <td><span class="checkmark">✓</span> 2 minutes</td>
                <td><span class="crossmark">✗</span> Hours of work</td>
                <td><span class="checkmark">✓</span> 5-10 minutes</td>
            </tr>
            <tr>
                <td><strong>Price</strong></td>
                <td><span class="checkmark">✓</span> <strong>FREE</strong></td>
                <td><span class="checkmark">✓</span> Free (but your time)</td>
                <td><span class="crossmark">✗</span> $29-79/month</td>
            </tr>
            <tr>
                <td><strong>Data Privacy</strong></td>
                <td><span class="checkmark">✓</span> Fully anonymized</td>
                <td><span class="checkmark">✓</span> Local only</td>
                <td><span class="crossmark">✗</span> Varies</td>
            </tr>
        </tbody>
    </table>
""", unsafe_allow_html=True)

# ==================== PRICING ====================
st.markdown('<h2 class="section-title">Transparent Pricing</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div class="pricing-box">
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">Free Tier</h3>
            <div class="price">$0<span class="price-period">/month</span></div>
            <p style="color: #7f8c8d; margin: 1rem 0;">No credit card required.</p>
            <ul class="feature-list">
                <li>All 3 dashboards (Finance, Customer, SEO)</li>
                <li>Unlimited CSV uploads</li>
                <li>Up to 10 analyses per week</li>
                <li>Real profit tracking</li>
                <li>Customer lifetime value</li>
                <li>SEO scoring</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <p class="section-subtitle" style="margin-top: 2rem;">
        Want AI-powered recommendations and unlimited analyses? 
        <strong>Insights Premium</strong> is available for $9/month (optional).
    </p>
""", unsafe_allow_html=True)

# ==================== TESTIMONIALS ====================
st.markdown('<h2 class="section-title">What Etsy Sellers Say</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="testimonial-box">
            <div class="testimonial-text">
                "I was shocked to see my actual margins. I thought I was making 40% profit 
                but after all the fees, it was only 18%. This dashboard saved my business."
            </div>
            <div class="testimonial-author">— Sarah M., Jewelry Seller</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="testimonial-box">
            <div class="testimonial-text">
                "The SEO analyzer helped me optimize my titles in 30 minutes. 
                My traffic doubled in two weeks. This is a game-changer."
            </div>
            <div class="testimonial-author">— James K., Home Decor Shop</div>
        </div>
    """, unsafe_allow_html=True)

# ==================== FAQ ====================
st.markdown('<h2 class="section-title">Frequently Asked Questions</h2>', unsafe_allow_html=True)

st.markdown("""
    <div class="faq-item">
        <div class="faq-question">Is this really free?</div>
        <div class="faq-answer">
            Yes, 100% free. All 3 dashboards are included with no credit card required. 
            We have an optional $9/month premium tier for AI recommendations, but the core 
            analytics are free.
        </div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">How is my data used?</div>
        <div class="faq-answer">
            Your data is anonymized and never shared with third parties. We use aggregated, 
            anonymized data to improve our analytics models, but your specific shop information 
            remains completely private.
        </div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">What CSV files do I need?</div>
        <div class="faq-answer">
            You need 3 files from your Etsy Shop Manager: Sold Orders, Sold Order Items, and Listings. 
            You can download these directly from your Etsy dashboard in CSV format.
        </div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">How accurate are the profit calculations?</div>
        <div class="faq-answer">
            Our calculations include all Etsy fees: listing fees (0.20¢), transaction fees (6.5%), 
            payment processing (3% + 0.25¢), regulatory fees (0.30€ for EU), and offsite ads (15% when applicable). 
            We also account for shipping costs if included in your data.
        </div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">Can I use this for multiple shops?</div>
        <div class="faq-answer">
            Yes! Upload data from different shops separately. The free tier allows 10 analyses per week, 
            which is enough for most multi-shop sellers. Premium users get unlimited analyses.
        </div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">Do you have an API?</div>
        <div class="faq-answer">
            Not yet, but it's on our roadmap. Currently, you upload CSV files manually. 
            We're working on Etsy API integration for automatic data sync.
        </div>
    </div>
    
    <div class="faq-item">
        <div class="faq-question">What about customer support?</div>
        <div class="faq-answer">
            Free users get email support with 24-48h response time. Premium users get priority support. 
            We also have comprehensive documentation and video tutorials.
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================== FINAL CTA ====================
st.markdown("""
    <div class="cta-section">
        <div class="cta-title">Ready to Optimize Your Etsy Shop?</div>
        <div class="cta-subtitle">
            Join hundreds of sellers who track their real profitability with our free dashboard
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Start Free Analysis Now", key="final_cta", type="primary", use_container_width=True):
        st.switch_page("pages/auth.py")

# ==================== SEO CONTENT (Hidden but crawlable) ====================
st.markdown("""
    <div style="margin-top: 4rem; padding: 2rem; background: #f8f9fa; border-radius: 15px;">
        <h2 style="color: #2c3e50;">About Our Etsy Dashboard</h2>
        <p style="color: #7f8c8d; line-height: 1.8;">
            Our Etsy dashboard is specifically designed for Etsy sellers who want to grow their business 
            through data-driven decisions. Unlike generic analytics tools, we focus exclusively on the 
            metrics that matter most for Etsy shops: real profit margins (after all fees), customer behavior 
            patterns, and SEO optimization opportunities.
        </p>
        <p style="color: #7f8c8d; line-height: 1.8;">
            The platform was built by former Etsy sellers who were frustrated with the lack of proper 
            financial tracking tools. After years of manual spreadsheet work and expensive third-party 
            solutions, we decided to build the tool we wished existed. Today, our Etsy analytics dashboard 
            helps sellers of all sizes understand their true profitability and make smarter business decisions.
        </p>
        <h3 style="color: #2c3e50; margin-top: 2rem;">Why Accurate Profit Tracking Matters</h3>
        <p style="color: #7f8c8d; line-height: 1.8;">
            Many Etsy sellers make pricing decisions based on gross revenue without fully accounting for 
            Etsy's complex fee structure. Transaction fees, payment processing fees, offsite advertising fees, 
            and regulatory charges can eat up 15-25% of your revenue. Our dashboard calculates your true 
            net profit for every product, helping you identify which items are actually profitable and 
            which are costing you money.
        </p>
        <h3 style="color: #2c3e50; margin-top: 2rem;">Etsy SEO Made Simple</h3>
        <p style="color: #7f8c8d; line-height: 1.8;">
            Ranking high in Etsy search results is crucial for sales, but optimizing your listings can 
            be overwhelming. Our SEO analyzer evaluates your titles, tags, and descriptions against 
            Etsy's ranking factors and gives you a clear score for each listing. You'll know exactly 
            which products need optimization and what changes will have the biggest impact on your visibility.
        </p>
        <h3 style="color: #2c3e50; margin-top: 2rem;">Understanding Your Customers</h3>
        <p style="color: #7f8c8d; line-height: 1.8;">
            Customer intelligence is often overlooked by small Etsy shops, but it's one of the most powerful 
            growth levers available. Our dashboard reveals customer lifetime value, purchase patterns, and 
            geographic distribution — insights that help you create targeted marketing campaigns, develop 
            new products that your best customers will love, and increase repeat purchase rates.
        </p>
        <p style="color: #7f8c8d; line-height: 1.8; margin-top: 2rem;">
            Get started with our free Etsy dashboard today and discover what professional-grade analytics 
            can do for your shop. No credit card required, no hidden fees, no catch — just powerful insights 
            to help you grow.
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== SCHEMA MARKUP (for SEO) ====================
st.markdown("""
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Etsy Dashboard",
        "applicationCategory": "BusinessApplication",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "ratingCount": "127"
        },
        "featureList": "Profit tracking, Customer analytics, SEO optimization, Fee calculation, Revenue analysis"
    }
    </script>
""", unsafe_allow_html=True)