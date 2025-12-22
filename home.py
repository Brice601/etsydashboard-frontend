import streamlit as st

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Free Etsy Dashboard - Track Your Shop Analytics in Real-Time",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'mailto:support@etsydashboard.com',
        'About': "Free Etsy Analytics Dashboard - Track profit margins, customers & SEO"
    }
)

# ==================== HIDE STREAMLIT MENU ====================
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .main > div {padding-top: 0rem;}
    </style>
""", unsafe_allow_html=True)

# ==================== SEO META TAGS ====================
st.markdown("""
    <title>Free Etsy Dashboard - Track Your Shop Analytics in Real-Time</title>
    <meta name="description" content="Free Etsy analytics dashboard. Track profit margins, customer behavior, and SEO performance. Upload your CSV and get instant insights.">
    <meta name="keywords" content="etsy dashboard, etsy analytics, etsy profit calculator, etsy shop analytics, etsy margins, etsy seo tool">
    <meta property="og:title" content="Free Etsy Dashboard - Track Your Shop Analytics">
    <meta property="og:description" content="Finance, SEO & Customer Intelligence - All Your Etsy Data in One Beautiful Dashboard">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
""", unsafe_allow_html=True)

# ==================== SCHEMA MARKUP (Product) ====================
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
      "description": "Free Etsy analytics dashboard with Finance, Customer Intelligence, and SEO tools"
    }
    </script>
""", unsafe_allow_html=True)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 5rem 2rem;
        text-align: center;
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.2;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.95;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .hero-cta {
        display: inline-block;
        background: #F56400;
        color: white !important;
        padding: 1.2rem 3rem;
        border-radius: 50px;
        font-size: 1.3rem;
        font-weight: bold;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 0 0.5rem;
    }
    
    .hero-cta:hover {
        background: #ff7a1a;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    
    .hero-cta.secondary {
        background: transparent;
        border: 2px solid white;
    }
    
    .hero-cta.secondary:hover {
        background: rgba(255,255,255,0.1);
    }
    
    /* Problem Section */
    .problem-section {
        background: #fff3e0;
        padding: 3rem 2rem;
        margin: 3rem -1rem;
        border-left: 5px solid #F56400;
    }
    
    .problem-title {
        font-size: 2rem;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    .problem-text {
        font-size: 1.2rem;
        color: #34495e;
        line-height: 1.8;
    }
    
    /* Dashboard Cards */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .dashboard-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-top: 4px solid;
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
    
    .dashboard-card h3 {
        font-size: 1.8rem;
        margin-bottom: 1rem;
        color: #2c3e50;
    }
    
    .dashboard-card p {
        font-size: 1.1rem;
        color: #7f8c8d;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    .feature-list {
        font-size: 1rem;
        line-height: 2;
        color: #34495e;
    }
    
    .feature-list li {
        margin-bottom: 0.5rem;
    }
    
    /* How it Works */
    .how-it-works {
        background: #f8f9fa;
        padding: 3rem 2rem;
        margin: 3rem -1rem;
        border-radius: 15px;
    }
    
    .how-title {
        font-size: 2.5rem;
        text-align: center;
        color: #2c3e50;
        margin-bottom: 3rem;
        font-weight: 700;
    }
    
    .steps-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
    }
    
    .step-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .step-number {
        font-size: 3rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 1rem;
    }
    
    .step-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .step-text {
        font-size: 1rem;
        color: #7f8c8d;
        line-height: 1.6;
    }
    
    /* Pricing Section */
    .pricing-section {
        margin: 4rem 0;
    }
    
    .pricing-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .pricing-card {
        background: white;
        border-radius: 15px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
        position: relative;
    }
    
    .pricing-card.premium {
        border: 3px solid #F56400;
        transform: scale(1.05);
    }
    
    .pricing-badge {
        position: absolute;
        top: -15px;
        right: 20px;
        background: #F56400;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
    }
    
    .pricing-title {
        font-size: 1.8rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .pricing-price {
        font-size: 3rem;
        color: #667eea;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .pricing-period {
        font-size: 1rem;
        color: #7f8c8d;
        margin-bottom: 2rem;
    }
    
    .pricing-features {
        text-align: left;
        margin-bottom: 2rem;
        font-size: 1rem;
        line-height: 2;
    }
    
    .pricing-cta {
        display: block;
        background: #667eea;
        color: white !important;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .pricing-cta:hover {
        background: #5568d3;
        transform: scale(1.05);
    }
    
    .pricing-cta.premium-cta {
        background: #F56400;
    }
    
    .pricing-cta.premium-cta:hover {
        background: #ff7a1a;
    }
    
    /* Final CTA */
    .final-cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4rem 2rem;
        margin: 4rem -1rem -1rem -1rem;
        text-align: center;
        border-radius: 20px 20px 0 0;
    }
    
    .final-cta-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    .final-cta-text {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.95;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {font-size: 2.5rem;}
        .hero-subtitle {font-size: 1.2rem;}
        .dashboard-grid, .pricing-grid {grid-template-columns: 1fr;}
        .pricing-card.premium {transform: scale(1);}
    }
    </style>
""", unsafe_allow_html=True)

# ==================== HERO SECTION ====================
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Free Etsy Dashboard - Track Your Shop Analytics in Real-Time</h1>
        <p class="hero-subtitle">Finance, SEO & Customer Intelligence - All Your Etsy Data in One Beautiful Dashboard</p>
        <div>
            <a href="/auth" class="hero-cta">Start Free Analysis</a>
            <a href="/calculate-etsy-fees" class="hero-cta secondary">Try Fee Calculator</a>
        </div>
        <p style='margin-top: 2rem; font-size: 1rem; opacity: 0.9;'>
            ✅ 100% Free • No Credit Card Required • 3 Complete Dashboards
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== PROBLEM SECTION ====================
st.markdown("""
    <div class="problem-section">
        <h2 class="problem-title">Are you tracking your Etsy shop performance in spreadsheets? 📊</h2>
        <p class="problem-text">
            Most Etsy sellers <strong>lose money without knowing it</strong>. They track sales but ignore hidden costs, 
            don't analyze customer behavior, and guess which listings perform best. 
            <br><br>
            <strong>Stop flying blind.</strong> Get instant insights into what's working (and what's costing you money).
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== SECTION: 3 DASHBOARDS ====================
st.markdown('<h2 class="how-title">3 Free Dashboards to Transform Your Shop</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="dashboard-card finance">
            <h3>💰 Finance Pro</h3>
            <p>Know exactly which products make money</p>
            <ul class="feature-list">
                <li>✅ Real profit margins after ALL fees</li>
                <li>✅ Hidden cost breakdown</li>
                <li>✅ ROI per product</li>
                <li>✅ Revenue trends over time</li>
                <li>🔒 AI profitability recommendations (Premium)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="dashboard-card customer">
            <h3>👥 Customer Intelligence</h3>
            <p>Understand who buys and why they come back</p>
            <ul class="feature-list">
                <li>✅ Customer lifetime value</li>
                <li>✅ Geographic breakdown</li>
                <li>✅ Return customer rate</li>
                <li>✅ Review analysis</li>
                <li>🔒 Re-engagement strategies (Premium)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="dashboard-card seo">
            <h3>🔍 SEO Analyzer</h3>
            <p>Optimize your listings to rank higher</p>
            <ul class="feature-list">
                <li>✅ SEO score per listing</li>
                <li>✅ Title optimization tips</li>
                <li>✅ Tag effectiveness analysis</li>
                <li>✅ Top performing listings</li>
                <li>🔒 Priority optimization list (Premium)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# ==================== HOW IT WORKS ====================
st.markdown("""
    <div class="how-it-works">
        <h2 class="how-title">How It Works (In 3 Simple Steps)</h2>
        <div class="steps-grid">
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-title">Upload Your CSV Files</div>
                <p class="step-text">Download your sales, orders, and listings data from Etsy. Upload them securely to our dashboard.</p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-title">Get Instant Analysis</div>
                <p class="step-text">Our tool automatically calculates margins, analyzes customers, and scores your SEO across all 3 dashboards.</p>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-title">Make Data-Driven Decisions</div>
                <p class="step-text">See exactly what's profitable, who's buying, and how to optimize. Grow your shop with confidence.</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==================== PRICING SECTION ====================
st.markdown('<h2 class="how-title" style="margin-top: 4rem;">Transparent Pricing</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="pricing-card">
            <div class="pricing-title">Free</div>
            <div class="pricing-price">$0</div>
            # <div class="pricing-period">now free</div>
            <ul class="pricing-features">
                <li>✅ Finance Pro Dashboard</li>
                <li>✅ Customer Intelligence Dashboard</li>
                <li>✅ SEO Analyzer Dashboard</li>
                <li>✅ 10 analyses per week</li>
                <li>✅ CSV uploads</li>
                <li>✅ All core metrics</li>
            </ul>
            <a href="/auth" class="pricing-cta">Start Free</a>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="pricing-card premium">
            <span class="pricing-badge">Most Popular</span>
            <div class="pricing-title">Insights Premium</div>
            <div class="pricing-price">$12</div>
            <div class="pricing-period">per month</div>
            <ul class="pricing-features">
                <li>✅ Everything in Free</li>
                <li>✨ Unlimited analyses</li>
                <li>✨ AI-powered recommendations</li>
                <li>✨ Priority optimization lists</li>
                <li>✨ Advanced profitability insights</li>
                <li>✨ Customer re-engagement strategies</li>
            </ul>
            <a href="/auth" class="pricing-cta premium-cta">Upgrade to Premium</a>
        </div>
    """, unsafe_allow_html=True)

# ==================== FINAL CTA ====================
st.markdown("""
    <div class="final-cta-section">
        <h2 class="final-cta-title">Start Analyzing Your Etsy Data for Free</h2>
        <p class="final-cta-text">
            Join hundreds of Etsy sellers who've transformed their shops with data-driven insights.
            <br>No credit card required. No setup fees. Start in 30 seconds.
        </p>
        <a href="/auth" class="hero-cta">Get Started Free →</a>
    </div>
""", unsafe_allow_html=True)

# ==================== LONG-FORM SEO CONTENT ====================
st.markdown("---")
st.markdown("## Why You Need an Etsy Dashboard")

st.markdown("""
Running a successful Etsy shop requires more than just great products. You need to **track your real profitability**, 
understand your customers, and optimize your listings for search. That's where a comprehensive Etsy dashboard becomes essential.

### Track Real Profit Margins

Many Etsy sellers focus on revenue but forget to account for all costs. Our **Finance Pro Dashboard** calculates your true profit 
after deducting:
- Etsy transaction fees (6.5%)
- Payment processing fees (3% + $0.25)
- Offsite ads fees (12-15% when applicable)
- Shipping costs
- Production costs
- Hidden fees most sellers miss

### Understand Customer Behavior

The **Customer Intelligence Dashboard** reveals who's buying from your shop, where they're located, and whether they come back. 
Track customer lifetime value, analyze reviews, and identify your most valuable customer segments.

### Optimize for Etsy Search

SEO is critical for Etsy success. Our **SEO Analyzer Dashboard** scores each listing and provides actionable tips to improve 
your titles, tags, and descriptions. See which listings rank best and replicate that success across your shop.

### Make Data-Driven Decisions

Stop guessing. Our Etsy analytics dashboard gives you the insights you need to:
- Price products profitably
- Focus on high-margin items
- Improve customer retention
- Rank higher in Etsy search
- Scale your shop sustainably

**Ready to transform your Etsy shop?** Start your free analysis today.
""")

# ==================== FAQ SCHEMA (for SEO) ====================
st.markdown("""
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Is the Etsy dashboard really free?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes! Our core Etsy dashboard with all 3 analytics tools (Finance Pro, Customer Intelligence, SEO Analyzer) is 100% free forever. You get 10 analyses per week at no cost. Premium features with AI recommendations are available for $9/month."
          }
        },
        {
          "@type": "Question",
          "name": "How do I upload my Etsy data?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Simply download your CSV files from your Etsy Shop Manager (Sales, Orders, and Listings), then upload them to our dashboard. The process takes less than 2 minutes."
          }
        },
        {
          "@type": "Question",
          "name": "What makes this different from other Etsy tools?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Most Etsy tools focus only on SEO. We provide comprehensive analytics across finance, customers, and SEO - all in one dashboard. Plus, we calculate your real profit margins after ALL fees, not just revenue."
          }
        }
      ]
    }
    </script>
""", unsafe_allow_html=True)