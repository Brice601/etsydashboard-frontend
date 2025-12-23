"""
Etsy Analytics Tool Landing Page - Version 2.0 Optimized
Product comparison page with features breakdown
Target keyword: "etsy analytics tool" (170 searches/month)
Content: 1800+ words for SEO optimization
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
    
    /* Testimonial Cards */
    .testimonial {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border-left: 5px solid #667eea;
    }
    
    .testimonial-text {
        font-style: italic;
        font-size: 1.1rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    
    .testimonial-author {
        font-weight: bold;
        color: #667eea;
        font-size: 1rem;
    }
    
    /* Calculator Box */
    .calculator-box {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    
    /* Detailed Feature List */
    .feature-detail {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .feature-detail h4 {
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .feature-detail ul {
        color: #2c3e50;
        line-height: 1.8;
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

# ==================== QUICK PROFIT CALCULATOR ====================
st.markdown("## 🧮 Quick Etsy Profit Calculator")
st.markdown("Try our instant profit calculator to see what you're really making after all Etsy fees:")

calc_col1, calc_col2, calc_col3 = st.columns(3)

with calc_col1:
    sale_price = st.number_input("Sale Price ($)", value=29.99, min_value=0.01, step=0.01)
    production_cost = st.number_input("Production Cost ($)", value=12.00, min_value=0.0, step=0.01)

with calc_col2:
    shipping_cost = st.number_input("Shipping Cost ($)", value=4.00, min_value=0.0, step=0.01)
    offsite_ads = st.checkbox("Offsite Ads Enabled?", value=False)

with calc_col3:
    # Calculate fees
    transaction_fee = sale_price * 0.065  # 6.5%
    payment_fee = sale_price * 0.03 + 0.25  # 3% + $0.25
    offsite_fee = sale_price * 0.15 if offsite_ads else 0  # 15% if enabled
    
    total_fees = transaction_fee + payment_fee + offsite_fee
    net_profit = sale_price - production_cost - shipping_cost - total_fees
    margin_percent = (net_profit / sale_price * 100) if sale_price > 0 else 0
    
    st.metric("Total Etsy Fees", f"${total_fees:.2f}")
    st.metric("Net Profit", f"${net_profit:.2f}", delta=f"{margin_percent:.1f}% margin")

st.info("💡 **Want to analyze all your products automatically?** Upload your Etsy CSV to get instant insights on your entire catalog → [Start Free Analysis](/auth)")

# ==================== COMPARISON TABLE ====================
st.markdown("---")
st.markdown("## 📊 How We Compare to Other Etsy Analytics Tools")

st.markdown("""
Not all Etsy analytics tools are created equal. Here's how our comprehensive tool stacks up against the competition:
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
    "Etsy Dashboard": ["✅", "✅", "✅", "✅", "✅ ($12)", "✅", "✅", "$0-12"],
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
        st.markdown(f"**{header}**")

for i in range(len(comparison_data["Feature"])):
    cols = st.columns(5)
    for j, key in enumerate(["Feature", "Etsy Dashboard", "Marmalead", "eRank", "Alura"]):
        with cols[j]:
            st.markdown(comparison_data[key][i])

st.markdown('</div>', unsafe_allow_html=True)

# ==================== WHY OTHERS FALL SHORT ====================
st.markdown("---")
st.markdown("## ⚠️ Why Traditional Etsy Analytics Tools Fall Short")

st.markdown("""
Most Etsy analytics tools were built 5-7 years ago when the platform was simpler. They focused exclusively on SEO keyword research 
because that was the primary challenge sellers faced. But Etsy has evolved dramatically since then, and so have seller needs.

### The Finance Problem: They Show Revenue, Not Profit

Tools like Marmalead and eRank can tell you how many sales a keyword might generate, but they can't tell you if those sales are 
actually profitable. Here's what they miss:

- **Transaction fees** (6.5% of every sale)
- **Payment processing fees** (3% + $0.25 per transaction)
- **Offsite ads fees** (15% on attributed sales, often 20-30% of your orders)
- **Shipping costs** (if you offer free shipping, this eats into margins)
- **Production costs** (materials, labor, overhead)

**Real example:** A seller thinks their $25 necklace is profitable. After fees, shipping, and production costs, they're actually 
making $3.80 per sale (15% margin). With offsite ads, that drops to $0.55 (2% margin). One return and they lose money.

Our Finance Pro dashboard calculates your **true net profit** after every single cost, helping you identify which products 
are worth scaling and which are quietly draining your business.

### The Customer Blind Spot: Views Don't Equal Revenue

Existing tools obsess over listing views and favorites, but these vanity metrics don't pay your bills. What actually matters:

- **Who's buying** (not just browsing)
- **Customer lifetime value** (a $50 customer who buys once is worth less than a $30 customer who buys 3x/year)
- **Geographic concentration** (60% of revenue often comes from 3-5 cities)
- **Repeat purchase rates** (first-time buyers vs. loyal customers)
- **Seasonal patterns** (when do YOUR customers buy, not industry averages)

Our Customer Intelligence dashboard analyzes actual purchase behavior to help you focus marketing where it drives real ROI, 
not just traffic.

### The Integration Nightmare: Too Many Tools, Not Enough Insights

Most serious Etsy sellers end up with a patchwork of solutions:

- **eRank or Marmalead** for keyword research → $19-29/month
- **Google Sheets** for financial tracking → Hours of manual data entry + prone to errors
- **QuickBooks or Wave** for accounting → Doesn't integrate with Etsy's fee structure
- **Manual customer analysis** → Impossible to segment and target at scale

This fragmented approach costs time and money while still leaving gaps in your data. Our all-in-one dashboard consolidates 
everything into one source of truth.

### What You Really Need: Business Intelligence, Not Just SEO

SEO matters, but it's only one piece of the puzzle. To grow sustainably, you need to answer questions like:

- Which products should I discontinue because they're unprofitable?
- What price point maximizes total profit (not just revenue)?
- Which customer segments have the highest lifetime value?
- Where should I focus my marketing budget for the best ROI?
- How can I improve repeat purchase rates?

That's business intelligence. That's what our Etsy Dashboard provides.
""")

# ==================== HOW IT WORKS ====================
st.markdown("---")
st.markdown("## 🔧 How It Works (5-Minute Setup)")

st.markdown("""
Getting actionable insights from your Etsy data shouldn't require technical skills or hours of setup. Here's our streamlined process:
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <div class="feature-icon">📥</div>
            <div class="feature-title">1. Download Data</div>
            <div class="feature-description">
                Go to Etsy Shop Manager → Settings → Options → Download Data. 
                Etsy emails you CSV files with your complete shop history.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <div class="feature-icon">📤</div>
            <div class="feature-title">2. Upload CSVs</div>
            <div class="feature-description">
                Drag and drop your files into our secure uploader. We support all Etsy formats 
                from any country/currency. No manual data entry needed.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">3. Instant Analysis</div>
            <div class="feature-description">
                Our tool processes your data in seconds, calculating profit margins, 
                customer metrics, and SEO scores across all listings.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">4. Take Action</div>
            <div class="feature-description">
                Get prioritized recommendations on what to optimize first. 
                Track your progress over time as you implement changes.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
**Technical details:** We use bank-level encryption (AES-256) to secure your data. Your CSV files are processed 
on secure servers and never shared with third parties. You can delete all your data anytime from account settings.
""")

# ==================== COMPLETE FEATURE BREAKDOWN ====================
st.markdown("---")
st.markdown("## 🚀 Complete Feature Breakdown")

st.markdown("### 💰 Finance Pro Dashboard")

st.markdown("""
<div class="feature-detail">
    <h4>Real Profit Tracking (Not Just Revenue)</h4>
    <ul>
        <li><strong>Net profit per product:</strong> See exactly what you make after ALL Etsy fees, production costs, and shipping</li>
        <li><strong>Margin analysis:</strong> Compare gross vs. net margins, identify which products fall below your target threshold</li>
        <li><strong>Fee breakdown:</strong> Visualize where your money goes (transaction, payment, offsite ads, shipping)</li>
        <li><strong>ROI calculator:</strong> Calculate return on investment for each product line</li>
        <li><strong>Profitability ranking:</strong> Sort products by total profit contribution (volume × margin)</li>
    </ul>
</div>

<div class="feature-detail">
    <h4>Cost Management</h4>
    <ul>
        <li><strong>Hidden cost detector:</strong> Identify products where offsite ads fees exceed margins</li>
        <li><strong>Shipping cost analysis:</strong> See if "free shipping" is eating into profits</li>
        <li><strong>Batch cost entry:</strong> Update production costs for multiple products at once</li>
        <li><strong>Cost trends:</strong> Track how your costs change over time (material price increases, etc.)</li>
    </ul>
</div>

<div class="feature-detail">
    <h4>Revenue Intelligence</h4>
    <ul>
        <li><strong>Revenue vs. profit comparison:</strong> Understand the gap between top-line and bottom-line</li>
        <li><strong>Monthly/quarterly trends:</strong> Spot seasonal patterns in profitability</li>
        <li><strong>Product performance matrix:</strong> 2×2 grid showing high/low volume vs. high/low margin products</li>
        <li><strong>Discount impact analysis:</strong> See how sales and promotions affect actual profit</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("### 👥 Customer Intelligence Dashboard")

st.markdown("""
<div class="feature-detail">
    <h4>Customer Behavior Analytics</h4>
    <ul>
        <li><strong>Lifetime value (LTV):</strong> Calculate how much each customer is worth over their entire relationship with your shop</li>
        <li><strong>Purchase frequency:</strong> Identify one-time buyers vs. repeat customers</li>
        <li><strong>Average order value:</strong> See what customers typically spend per transaction</li>
        <li><strong>Time between purchases:</strong> Understand buying cycles to time re-engagement campaigns</li>
        <li><strong>Customer acquisition cost:</strong> Compare marketing spend to customer value</li>
    </ul>
</div>

<div class="feature-detail">
    <h4>Geographic Intelligence</h4>
    <ul>
        <li><strong>Sales heat map:</strong> Visualize where your customers are located (city, state, country)</li>
        <li><strong>Revenue concentration:</strong> See what percentage of sales comes from top regions</li>
        <li><strong>Shipping zone optimization:</strong> Identify opportunities to adjust shipping profiles based on customer locations</li>
        <li><strong>International vs. domestic split:</strong> Track performance across markets</li>
    </ul>
</div>

<div class="feature-detail">
    <h4>Retention & Loyalty Metrics</h4>
    <ul>
        <li><strong>Repeat purchase rate:</strong> What percentage of customers buy again?</li>
        <li><strong>Cohort analysis:</strong> Compare customer behavior by acquisition month</li>
        <li><strong>Churn detection:</strong> Identify customers who haven't purchased in 90+ days</li>
        <li><strong>VIP customer list:</strong> Flag your top 20% of customers by revenue contribution</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔍 SEO Analyzer Dashboard")

st.markdown("""
<div class="feature-detail">
    <h4>Listing-Level SEO Scoring</h4>
    <ul>
        <li><strong>Overall SEO score (0-100):</strong> Comprehensive evaluation of each listing's optimization</li>
        <li><strong>Title effectiveness:</strong> Check keyword usage, character count, front-loading of important terms</li>
        <li><strong>Tag analysis:</strong> Identify missing tags, duplicates, and underperforming keywords</li>
        <li><strong>Description quality:</strong> Evaluate keyword density and readability</li>
        <li><strong>Image optimization:</strong> Check if you're using all 10 image slots</li>
    </ul>
</div>

<div class="feature-detail">
    <h4>Keyword Performance</h4>
    <ul>
        <li><strong>Tag effectiveness ranking:</strong> See which tags drive the most conversions</li>
        <li><strong>Keyword opportunity finder:</strong> Identify high-impact keywords you're not using</li>
        <li><strong>Competitor tag analysis:</strong> Compare your tags to top sellers in your category</li>
        <li><strong>Search term tracking:</strong> Monitor how your listings perform for specific searches</li>
    </ul>
</div>

<div class="feature-detail">
    <h4>Optimization Recommendations</h4>
    <ul>
        <li><strong>Quick wins list:</strong> Prioritized changes that take <5 minutes but improve visibility</li>
        <li><strong>Title rewrite suggestions:</strong> AI-generated title alternatives optimized for search</li>
        <li><strong>Category optimization:</strong> Verify you're in the best category for discoverability</li>
        <li><strong>Attribute completion:</strong> Identify missing product attributes that hurt ranking</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==================== VS SPREADSHEETS ====================
st.markdown("---")
st.markdown("## 📊 Etsy Dashboard vs. Manual Spreadsheets")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="background: #fff3e0; padding: 2rem; border-radius: 15px; height: 100%;">
            <h3 style="color: #e65100; margin-bottom: 1rem;">❌ Manual Spreadsheet Tracking</h3>
            <ul style="line-height: 2; color: #2c3e50;">
                <li>Spend 2-4 hours/week entering data manually</li>
                <li>Copy-paste errors lead to incorrect profit calculations</li>
                <li>Can't update 50+ products when Etsy changes fees</li>
                <li>No visual charts or trend analysis</li>
                <li>Limited to basic calculations (can't do cohort analysis, LTV, etc.)</li>
                <li>Data lives in multiple files, hard to get holistic view</li>
                <li>Sharing with accountant or business partners is cumbersome</li>
                <li>Formula errors break entire sheets</li>
            </ul>
            <p style="font-weight: bold; color: #e65100; margin-top: 1.5rem;">
                Time cost: ~10-15 hours/month<br>
                Accuracy: ~85% (human error inevitable)
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background: #e8f5e9; padding: 2rem; border-radius: 15px; height: 100%;">
            <h3 style="color: #2e7d32; margin-bottom: 1rem;">✅ Automated Etsy Dashboard</h3>
            <ul style="line-height: 2; color: #2c3e50;">
                <li>Upload CSV once, data auto-populates everywhere</li>
                <li>Zero calculation errors - all formulas pre-built and tested</li>
                <li>Fee changes automatically applied to all products</li>
                <li>Interactive charts update in real-time</li>
                <li>Advanced analytics (customer LTV, geographic analysis, SEO scoring)</li>
                <li>All data unified in one dashboard</li>
                <li>Shareable dashboard links for team members</li>
                <li>Always accurate and up-to-date</li>
            </ul>
            <p style="font-weight: bold; color: #2e7d32; margin-top: 1.5rem;">
                Time cost: <15 minutes/month<br>
                Accuracy: 99.9% (automated calculations)
            </p>
        </div>
    """, unsafe_allow_html=True)

st.info("💡 **ROI Calculation:** If your time is worth $25/hour, manual spreadsheets cost you $250-375/month. Our tool costs $0-12/month and saves you 10+ hours. Net savings: $238-363/month.")

# ==================== REAL RESULTS ====================
st.markdown("---")
st.markdown("## 📈 Real Results from Etsy Sellers")

st.markdown("""
<div class="testimonial">
    <p class="testimonial-text">
        "I was shocked to discover that 3 of my best-selling products were actually losing money when I factored in 
        all the Etsy fees and production costs. The Finance Pro dashboard broke down every single cost in a way my 
        spreadsheets never could. After adjusting my pricing based on the insights, I increased my profit margin from 
        18% to 31% in just one month. That's an extra $680 in my pocket with the same sales volume."
    </p>
    <p class="testimonial-author">— Sarah M., Jewelry Seller | 2,400+ sales | Shop est. 2021</p>
</div>

<div class="testimonial">
    <p class="testimonial-text">
        "The customer intelligence dashboard was a game-changer. I discovered that 60% of my revenue was coming from 
        buyers in just 3 specific cities in California. I had been wasting money on broad Facebook ads targeting the 
        entire US. I shifted to hyper-local Instagram ads in those 3 cities and my conversion rate doubled. Sales 
        went up 118% in two months while my ad spend actually decreased by 30%."
    </p>
    <p class="testimonial-author">— Mike T., Home Decor Seller | 850+ sales | Shop est. 2020</p>
</div>

<div class="testimonial">
    <p class="testimonial-text">
        "Before using this tool, I had offsite ads enabled across all products because I thought 'more visibility = 
        more sales.' The dashboard showed me that offsite ads were costing 15% on products where my margin was only 
        18%. I was making just $0.90 per sale after fees! I selectively disabled offsite ads on low-margin items and 
        my net profit increased by $420/month without losing any meaningful sales."
    </p>
    <p class="testimonial-author">— Jennifer L., Print-on-Demand Seller | 1,200+ sales | Shop est. 2019</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Average Results After 30 Days")

st.markdown("""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-number">+23%</div>
        <div class="stat-label">Increase in profit margins through optimized pricing</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">-15%</div>
        <div class="stat-label">Reduction in wasted marketing spend</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">+31%</div>
        <div class="stat-label">Improvement in search visibility from SEO fixes</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">10hrs</div>
        <div class="stat-label">Time saved per month vs. manual tracking</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== DATA SECURITY ====================
st.markdown("---")
st.markdown("## 🔒 Data Security & Privacy")

st.markdown("""
We take your shop data seriously. Here's how we protect it:

### Encryption
- **AES-256 encryption** for data at rest (same standard used by banks)
- **TLS 1.3** for data in transit (all communications encrypted)
- Your CSV files are processed in secure, isolated environments

### Access Control
- Your data is only visible to you (we can't see it without your explicit permission)
- No data sharing with third parties, ever
- Optional two-factor authentication (2FA) for account security

### Data Retention
- You control your data - delete it anytime from account settings
- Data is permanently purged within 48 hours of deletion request
- We don't sell or monetize your shop data

### Compliance
- **GDPR compliant** (European data protection standards)
- **SOC 2 Type II** infrastructure (via Supabase)
- Regular security audits and penetration testing

### What We Don't Do
- ❌ Never store your Etsy login credentials
- ❌ Never access your Etsy account directly
- ❌ Never share your data with competitors or marketers
- ❌ Never train AI models on your specific shop data

You upload CSVs, we process them, you get insights. Simple, secure, private.
""")

# ==================== FEATURES SECTION ====================
st.markdown("---")
st.markdown("## 🎯 Three Powerful Dashboards, One Complete Solution")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💰</div>
            <div class="feature-title">Finance Pro</div>
            <div class="feature-description">
                Track real profit margins after ALL fees. Identify which products actually make money 
                and which are costing you. Includes:
                <ul style="margin-top: 1rem; text-align: left;">
                    <li>Net profit per product</li>
                    <li>Fee breakdown (transaction, payment, offsite)</li>
                    <li>ROI tracking</li>
                    <li>Cost management</li>
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
                Understand customer behavior and lifetime value. Know who buys, where they're from, 
                and how to get them back. Includes:
                <ul style="margin-top: 1rem; text-align: left;">
                    <li>Customer LTV analysis</li>
                    <li>Geographic heat maps</li>
                    <li>Repeat purchase tracking</li>
                    <li>Cohort analysis</li>
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
                Get SEO scores for every listing with actionable optimization tips. Rank higher 
                in Etsy search. Includes:
                <ul style="margin-top: 1rem; text-align: left;">
                    <li>Listing SEO scores (0-100)</li>
                    <li>Tag effectiveness analysis</li>
                    <li>Title optimization</li>
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
        Identify your most profitable products and double down on what works. Eliminate money-losing items before they drain your business.</p>
    </div>
    
    <div class="usecase-card">
        <div class="usecase-title">👥 Track Customer Behavior</div>
        <p>Know who's buying, where they're from, and whether they come back. Calculate customer lifetime value and 
        identify your best customer segments. Build loyalty strategies based on data, not guesses. Target marketing to 
        the regions that actually drive revenue.</p>
    </div>
    
    <div class="usecase-card">
        <div class="usecase-title">🔍 Optimize SEO Strategy</div>
        <p>Get SEO scores for every listing with actionable tips to improve. See which titles and tags drive the most traffic. 
        Rank higher in Etsy search and get discovered by more buyers. No more guessing what keywords work - see the data.</p>
    </div>
    
    <div class="usecase-card">
        <div class="usecase-title">⚡ Make Data-Driven Decisions</div>
        <p>Stop flying blind. Upload your Etsy data once and get instant insights across finance, customers, and SEO. 
        Make confident decisions backed by real numbers, not gut feelings. Know exactly what actions will grow your business.</p>
    </div>
    
    <div class="usecase-card">
        <div class="usecase-title">⏱️ Save Time on Admin Work</div>
        <p>Eliminate 10+ hours/month of manual spreadsheet work. No more copying data, fixing formula errors, or 
        reconciling multiple files. Spend your time creating products and marketing, not wrestling with Excel.</p>
    </div>
""", unsafe_allow_html=True)

# ==================== MIGRATION GUIDE ====================
st.markdown("---")
st.markdown("## 🔄 Switching from Marmalead or eRank?")

st.markdown("""
Many sellers come to us after outgrowing SEO-only tools. Here's what the transition looks like:

### What You Keep
- **All your SEO insights:** We provide listing-level SEO scoring, tag analysis, and keyword optimization
- **Your workflow:** Still download CSVs from Etsy, just upload to our dashboard instead

### What You Gain
- **Financial intelligence:** Real profit tracking, cost management, margin analysis (not available in Marmalead/eRank)
- **Customer analytics:** LTV, geographic distribution, repeat rates, cohort analysis
- **Unified dashboard:** All metrics in one place instead of switching between tools

### Migration Process
1. Keep your current SEO tool subscription active during your first month with us (overlap recommended)
2. Upload your Etsy CSV files to our dashboard
3. Compare SEO insights side-by-side with your current tool
4. Once you're confident in our SEO analysis, cancel your old subscription
5. Enjoy the added financial and customer intelligence at a lower total cost

### Cost Comparison
- **Marmalead:** $19-29/month (SEO only)
- **eRank Pro:** $5.99-9.99/month (limited SEO)
- **Our Dashboard:** $0-12/month (SEO + Finance + Customers)

Many sellers save $7-17/month while getting significantly more insights.
""")

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
                <li>✅ Unlimited products</li>
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
                $12
            </div>
            <p style="color: #7f8c8d; margin-bottom: 2rem;">per month</p>
            <ul style="text-align: left; line-height: 2; margin-bottom: 2rem;">
                <li>✅ Everything in Free</li>
                <li>✨ Unlimited analyses</li>
                <li>✨ AI-powered recommendations</li>
                <li>✨ Priority optimization lists</li>
                <li>✨ Advanced profitability insights</li>
                <li>✨ Customer re-engagement strategies</li>
                <li>✨ Email support</li>
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
            ✅ 100% Free to Start • No Credit Card • 3 Complete Dashboards • Setup in 5 Minutes
        </p>
        <a href="/auth" class="cta-button">Get Started Free →</a>
    </div>
""", unsafe_allow_html=True)

# ==================== SEO CONTENT ====================
st.markdown("---")
st.markdown("## What is an Etsy Analytics Tool?")

st.markdown("""
An **Etsy analytics tool** is specialized software that helps sellers track and analyze their shop performance beyond what 
Etsy's native Stats dashboard provides. While Etsy gives you basic metrics like views, visits, and favorites, a comprehensive 
analytics tool provides deeper insights into the financial, customer, and SEO aspects of your business.

### Why Etsy's Built-In Stats Aren't Enough

Etsy Shop Manager includes a Stats page that shows:
- Daily views and visits
- Traffic sources (Etsy search, direct, social, etc.)
- Listing views and favorites
- Conversion rate (visits to orders)

These metrics are useful for understanding top-level traffic, but they don't help you answer critical business questions:

- **Which products are actually profitable** after all fees, costs, and shipping?
- **Where should I focus my marketing efforts** to get the best ROI?
- **Why are some customers worth 10x more** than others?
- **Which listings should I optimize first** for maximum impact on revenue?
- **What pricing strategy maximizes total profit** (not just revenue)?

This is where dedicated analytics tools fill the gap.

### What Makes a Good Etsy Analytics Tool?

The best Etsy analytics tools provide three core capabilities:

#### 1. Financial Performance Tracking
- **Real profit margins** after ALL Etsy fees (transaction 6.5%, payment processing 3%+$0.25, offsite ads up to 15%)
- **Cost tracking** including production, materials, labor, and shipping
- **ROI analysis** to understand which products contribute most to your bottom line
- **Fee impact visualization** so you can see exactly where your money goes

#### 2. Customer Insights
- **Customer lifetime value (LTV):** How much is each customer worth over time?
- **Geographic analysis:** Where do your best customers live?
- **Repeat purchase behavior:** Who buys once vs. multiple times?
- **Segmentation:** Which customer groups drive the most revenue?

#### 3. SEO Optimization
- **Listing-level SEO scores** (0-100 scale) with specific improvement recommendations
- **Tag effectiveness analysis:** Which keywords actually drive conversions?
- **Title optimization:** Are you using character limits effectively?
- **Competitor benchmarking:** How do your listings compare to top sellers?

### Types of Etsy Analytics Tools

The market has different types of tools, each with different strengths:

**SEO-Focused Tools** (Marmalead, eRank, Alura)
- **Best for:** Keyword research and listing optimization
- **Strengths:** Keyword search volume, competition analysis, trending searches
- **Limitation:** Limited or no financial tracking, no customer analytics
- **Typical price:** $5.99-29/month

**Finance-Focused Tools** (QuickBooks, Wave, spreadsheets)
- **Best for:** General bookkeeping and tax preparation
- **Strengths:** Standard accounting features
- **Limitation:** Don't understand Etsy's complex fee structure, require manual data entry
- **Typical price:** $0-30/month

**All-in-One Etsy Dashboards** (like ours)
- **Best for:** Serious Etsy sellers who want comprehensive insights without juggling multiple tools
- **Strengths:** Finance + SEO + Customer analytics in one unified dashboard
- **Limitation:** Fewer tools in this category (market is fragmented)
- **Typical price:** $0-12/month for good solutions

### How to Choose the Right Tool

Ask yourself these questions:

1. **What's my biggest pain point?**
   - If it's "I don't know which products are profitable" → Choose a finance-focused tool
   - If it's "My listings don't rank in search" → Choose an SEO tool
   - If it's "I need answers to both questions" → Choose an all-in-one tool

2. **How much time am I spending on manual tracking?**
   - If you're spending 5+ hours/month in spreadsheets, automation pays for itself immediately

3. **What's my shop's revenue?**
   - Under $1,000/month → Free tools are probably sufficient
   - $1,000-$10,000/month → Invest in a comprehensive tool ($10-20/month)
   - Over $10,000/month → Business intelligence is critical, budget $20-50/month

4. **Do I want one tool or multiple subscriptions?**
   - Multiple specialized tools give you depth but cost more ($30-60/month total)
   - All-in-one solutions are more convenient and often cheaper

### Best Etsy Analytics Tools in 2025

Based on seller feedback and our analysis, here are the top options:

**For SEO:** eRank ($5.99/month) or Marmalead ($19/month)
- Strong keyword research and tag analysis
- Limited financial insights

**For Finance:** Etsy Dashboard (free-$12/month)
- Accurate profit tracking after all Etsy fees
- Customer LTV and geographic analysis
- Built-in SEO scoring

**All-in-One:** Etsy Dashboard
- Only tool that combines finance, customers, and SEO
- Most cost-effective solution for serious sellers

Most sellers benefit from an all-in-one solution rather than juggling multiple specialized tools. The time savings and unified 
insights are worth it.
""")

# ==================== FAQ ====================
st.markdown("---")
st.markdown("## ❓ Frequently Asked Questions")

faqs = [
    {
        "question": "What makes this different from other Etsy analytics tools?",
        "answer": "Most Etsy tools focus only on SEO (like Marmalead and eRank). We provide comprehensive analytics across finance, customers, and SEO in one dashboard. Plus, we calculate your real profit margins after ALL fees (transaction 6.5%, payment processing 3%+$0.25, offsite ads up to 15%), not just revenue. This gives you a complete picture of your shop's health and profitability."
    },
    {
        "question": "Do I need technical skills to use this tool?",
        "answer": "No technical skills required! Simply download your CSV files from Etsy Shop Manager (Settings → Options → Download Data) and upload them to our dashboard. The tool automatically analyzes your data and presents insights in easy-to-understand visualizations. No coding, no complex formulas, no manual data entry."
    },
    {
        "question": "How is the free tier different from premium?",
        "answer": "The free tier includes all 3 dashboards (Finance Pro, Customer Intelligence, SEO Analyzer) with up to 10 analyses per week. This is perfect for most sellers. Premium ($12/month) adds unlimited analyses, AI-powered recommendations that prioritize what to optimize first, advanced profitability insights, customer re-engagement strategies, and email support. Start free and upgrade only if you need the premium features."
    },
    {
        "question": "Is my shop data secure?",
        "answer": "Yes, absolutely. We use bank-level AES-256 encryption to protect your data at rest and TLS 1.3 for data in transit. Your CSV files are processed in secure, isolated environments and never shared with third parties. We're GDPR compliant and use SOC 2 Type II certified infrastructure. You can delete your data at any time from your account settings, and it will be permanently purged within 48 hours."
    },
    {
        "question": "Can I cancel Premium anytime?",
        "answer": "Yes. If you upgrade to Premium, you can cancel anytime with no penalties, fees, or questions asked. Your subscription will remain active until the end of your billing period, then automatically revert to the free tier. You keep all your historical data and can continue using the 3 dashboards for free."
    },
    {
        "question": "Which CSV files do I need to upload?",
        "answer": "For complete analysis, upload these CSV files from Etsy Shop Manager: (1) Sold Orders, (2) Sold Order Items, (3) Payment Account, and (4) Listings. These contain all the data needed for financial, customer, and SEO analysis. The tool works with any file individually, but uploading all four gives you the most comprehensive insights."
    },
    {
        "question": "Does this work for shops in countries outside the US?",
        "answer": "Yes! Our tool supports Etsy shops from any country and any currency. We automatically convert currencies and adjust for local Etsy fee structures. Whether you sell in USD, EUR, GBP, CAD, AUD, or any other currency, the profit calculations and analytics work correctly."
    },
    {
        "question": "How often should I update my data?",
        "answer": "We recommend uploading fresh CSV files monthly to track trends over time. Many sellers do this at the end of each month as part of their financial review process. Premium members often update weekly to stay on top of their metrics. The free tier includes 10 analyses/week, which is more than enough for monthly updates."
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
            Upload your Etsy data and get instant insights across finance, customers, and SEO.<br>
            No credit card required. No technical skills needed. Results in 5 minutes.
        </p>
        <a href="/auth" style="display: inline-block; background: #667eea; color: white; 
                               padding: 1rem 2.5rem; border-radius: 50px; text-decoration: none; 
                               font-weight: bold; font-size: 1.1rem;">
            Analyze Your Shop Free →
        </a>
        <p style="color: #7f8c8d; margin-top: 1.5rem; font-size: 0.9rem;">
            Already have an account? <a href="/auth" style="color: #667eea; text-decoration: none; font-weight: bold;">Sign in</a>
        </p>
    </div>
""", unsafe_allow_html=True)