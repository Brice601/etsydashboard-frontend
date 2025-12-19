"""
Calculate Etsy Fees Landing Page
Free calculator with instant results + CTA to full dashboard
Target keywords: "calculate etsy fees", "etsy calculator"
"""

import streamlit as st
from components.seo_meta import render_calculate_fees_seo, hide_streamlit_elements, render_schema_faq

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Free Etsy Fee Calculator - Calculate Your Real Profit After All Fees",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit elements
hide_streamlit_elements()

# Render SEO (meta tags + schema)
render_calculate_fees_seo()

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
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
    
    /* Calculator Card */
    .calculator-card {
        background: white;
        border-radius: 15px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .result-box {
        background: #e8f5e9;
        border-left: 5px solid #27ae60;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
    }
    
    .result-box.warning {
        background: #fff3e0;
        border-left-color: #F56400;
    }
    
    .result-box.danger {
        background: #ffebee;
        border-left-color: #e74c3c;
    }
    
    .big-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #27ae60;
        margin: 0.5rem 0;
    }
    
    .big-number.negative {
        color: #e74c3c;
    }
    
    .fees-breakdown {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
    }
    
    .fee-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #dee2e6;
    }
    
    .fee-item:last-child {
        border-bottom: none;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .cta-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
    
    .cta-button {
        display: inline-block;
        background: #F56400;
        color: white !important;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        text-decoration: none;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .cta-button:hover {
        background: #ff7a1a;
        transform: scale(1.05);
    }
    
    /* Insight boxes */
    .insight-box {
        background: #e3f2fd;
        border-left: 5px solid #2196F3;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
    }
    
    .insight-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1976D2;
        margin-bottom: 0.5rem;
    }
    
    /* Tips section */
    .tips-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .tip-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .tip-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .tip-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== HERO SECTION ====================
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Free Etsy Fee Calculator</h1>
        <p class="hero-subtitle">Calculate your real profit after ALL Etsy fees in seconds</p>
        <p style="font-size: 1rem; opacity: 0.9;">
            ✅ Transaction Fees • Payment Processing • Offsite Ads • Shipping
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== CALCULATOR ====================
st.markdown('<div class="calculator-card">', unsafe_allow_html=True)

st.markdown("### 💰 Calculate Your Etsy Profit")

col1, col2 = st.columns(2)

with col1:
    sale_price = st.number_input(
        "Sale Price ($)",
        min_value=0.0,
        value=29.99,
        step=0.01,
        help="The price your customer pays"
    )
    
    production_cost = st.number_input(
        "Production Cost ($)",
        min_value=0.0,
        value=12.0,
        step=0.01,
        help="Materials, labor, packaging"
    )
    
    shipping_cost = st.number_input(
        "Shipping Cost ($)",
        min_value=0.0,
        value=4.0,
        step=0.01,
        help="What you pay for shipping"
    )

with col2:
    offsite_ads = st.checkbox(
        "Offsite Ads Enabled",
        value=False,
        help="15% fee when sales come from Etsy ads"
    )
    
    etsy_plus = st.checkbox(
        "Etsy Plus Subscriber ($10/month)",
        value=False
    )
    
    monthly_sales = st.number_input(
        "Expected Monthly Sales",
        min_value=1,
        value=15,
        step=1,
        help="For profit projections"
    )

# Calculate fees
transaction_fee = sale_price * 0.065  # 6.5%
listing_fee = 0.20
payment_processing = (sale_price * 0.03) + 0.25
offsite_ads_fee = sale_price * 0.15 if offsite_ads else 0.0

total_fees = transaction_fee + listing_fee + payment_processing + offsite_ads_fee
net_revenue = sale_price - total_fees
profit = net_revenue - production_cost - shipping_cost

profit_margin = (profit / sale_price * 100) if sale_price > 0 else 0
monthly_profit = profit * monthly_sales

# ==================== RESULTS ====================
st.markdown("### 📊 Your Results")

# Main result box
result_class = "result-box"
if profit < 0:
    result_class += " danger"
elif profit_margin < 20:
    result_class += " warning"

st.markdown(f"""
    <div class="{result_class}">
        <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">Net Profit Per Sale</div>
        <div class="big-number {'negative' if profit < 0 else ''}">${profit:.2f}</div>
        <div style="font-size: 1rem; opacity: 0.8;">
            {profit_margin:.1f}% profit margin
        </div>
    </div>
""", unsafe_allow_html=True)

# Fees breakdown
st.markdown(f"""
    <div class="fees-breakdown">
        <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 1rem;">Fee Breakdown</div>
        <div class="fee-item">
            <span>Sale Price</span>
            <span>${sale_price:.2f}</span>
        </div>
        <div class="fee-item">
            <span>Transaction Fee (6.5%)</span>
            <span>-${transaction_fee:.2f}</span>
        </div>
        <div class="fee-item">
            <span>Listing Fee</span>
            <span>-${listing_fee:.2f}</span>
        </div>
        <div class="fee-item">
            <span>Payment Processing (3% + $0.25)</span>
            <span>-${payment_processing:.2f}</span>
        </div>
        {'<div class="fee-item"><span>Offsite Ads (15%)</span><span>-$' + f'{offsite_ads_fee:.2f}' + '</span></div>' if offsite_ads else ''}
        <div class="fee-item">
            <span>Production Cost</span>
            <span>-${production_cost:.2f}</span>
        </div>
        <div class="fee-item">
            <span>Shipping Cost</span>
            <span>-${shipping_cost:.2f}</span>
        </div>
        <div class="fee-item">
            <span>NET PROFIT</span>
            <span style="color: {'#e74c3c' if profit < 0 else '#27ae60'};">${profit:.2f}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Monthly projection
st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">📈 Monthly Projection</div>
        <p style="font-size: 1.1rem; margin: 0.5rem 0;">
            At {monthly_sales} sales/month, you'll make: <strong>${monthly_profit:.2f}/month</strong>
        </p>
        <p style="font-size: 0.9rem; opacity: 0.8; margin: 0;">
            Annual projection: ${monthly_profit * 12:.2f}/year
        </p>
    </div>
""", unsafe_allow_html=True)

# Insights and recommendations
if profit < 0:
    st.markdown(f"""
        <div class="result-box danger">
            <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">⚠️ You're Losing Money!</div>
            <p>You're losing ${abs(profit):.2f} per sale. Consider:</p>
            <ul>
                <li>Increasing your price to at least ${sale_price + abs(profit) + 2:.2f}</li>
                <li>Reducing production costs</li>
                <li>Disabling offsite ads ({offsite_ads_fee:.2f} saved per sale)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
elif profit_margin < 20:
    st.markdown(f"""
        <div class="result-box warning">
            <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">⚡ Low Profit Margin</div>
            <p>Your {profit_margin:.1f}% margin is below the healthy 20-30% range for Etsy.</p>
            <p>To reach 25% margin, you should price at: <strong>${(production_cost + shipping_cost + total_fees) / 0.75:.2f}</strong></p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class="result-box">
            <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">✅ Healthy Profit Margin!</div>
            <p>Your {profit_margin:.1f}% margin is in the healthy range. Keep optimizing to maintain profitability.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==================== CTA TO FULL DASHBOARD ====================
st.markdown("""
    <div class="cta-box">
        <h2 style="margin-bottom: 1rem;">Want to Analyze ALL Your Products?</h2>
        <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
            You just calculated 1 product manually. Our dashboard analyzes your entire shop automatically.
        </p>
        <p style="font-size: 1rem; opacity: 0.9; margin-bottom: 1.5rem;">
            ✅ Upload your CSV • Track ALL products • Find hidden losses • Get AI recommendations
        </p>
        <a href="/auth" class="cta-button">Start Free Analysis →</a>
        <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.8;">
            100% Free • No Credit Card Required
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== TIPS & INSIGHTS ====================
st.markdown("---")
st.markdown("## 💡 Tips to Maximize Your Etsy Profit")

st.markdown('<div class="tips-grid">', unsafe_allow_html=True)

st.markdown("""
    <div class="tip-card">
        <div class="tip-icon">🎯</div>
        <div class="tip-title">Optimize Pricing</div>
        <p>Aim for 25-30% profit margin. Price too low and you lose money, too high and sales drop.</p>
    </div>
    
    <div class="tip-card">
        <div class="tip-icon">📊</div>
        <div class="tip-title">Track All Costs</div>
        <p>Don't forget packaging, labels, tape, and your time. These "small" costs add up quickly.</p>
    </div>
    
    <div class="tip-card">
        <div class="tip-icon">🚫</div>
        <div class="tip-title">Review Offsite Ads</div>
        <p>Offsite ads cost 15% per sale. Disable them if your margin is already tight.</p>
    </div>
    
    <div class="tip-card">
        <div class="tip-icon">📦</div>
        <div class="tip-title">Bundle Products</div>
        <p>Increase average order value by bundling. You pay Etsy fees once but sell more.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==================== SEO CONTENT ====================
st.markdown("---")
st.markdown("## Understanding Etsy Fees")

st.markdown("""
Etsy charges several types of fees that impact your profitability:

### Transaction Fee (6.5%)
Etsy charges 6.5% of your item's sale price (including shipping). This is their main revenue source and applies to every sale.

### Listing Fee ($0.20)
Each listing costs $0.20 and lasts for 4 months or until sold. If you auto-renew, that's another $0.20.

### Payment Processing (3% + $0.25)
Etsy Payments charges 3% + $0.25 per transaction to process credit cards and handle the money transfer.

### Offsite Ads (12-15%)
If Etsy advertises your product on Google, Facebook, or other platforms and makes a sale, they charge 12% (for sellers over $10k/year) or 15% (under $10k/year). You can opt out if under $10k.

### Hidden Costs
Don't forget:
- Shipping materials and postage
- Production time and labor
- Packaging and labels
- Etsy Plus subscription ($10/month)
- Etsy Ads budget (if using)

**The average Etsy seller pays 12-15% in total fees**, but with offsite ads enabled, this can jump to 25-30%.
""")

st.markdown("### How to Reduce Etsy Fees")

st.markdown("""
1. **Disable Offsite Ads** (if under $10k/year revenue) - saves 15% per offsite sale
2. **Use Free Shipping** strategically - build shipping into your price
3. **Bundle products** - pay fees once but sell more
4. **Optimize listings** - better SEO means less need for paid ads
5. **Track everything** - know your real profit margins

Want to track all this automatically? **[Try our free Etsy Dashboard](/auth)** - upload your CSV and see profitability across all products instantly.
""")

# ==================== FAQ SCHEMA ====================
faqs = [
    {
        "question": "How much does Etsy take per sale?",
        "answer": "Etsy charges 6.5% transaction fee + $0.20 listing fee + 3% + $0.25 payment processing fee. In total, expect 10-12% in base fees, plus potentially 12-15% for offsite ads if enabled."
    },
    {
        "question": "Are Etsy fees tax deductible?",
        "answer": "Yes, all Etsy fees (transaction, listing, payment processing, ads) are business expenses and tax deductible. Keep your monthly statements for tax filing."
    },
    {
        "question": "What is the Etsy payment processing fee?",
        "answer": "Etsy Payments charges 3% + $0.25 per transaction to process credit card payments. This applies to every sale and is separate from the 6.5% transaction fee."
    },
    {
        "question": "Should I turn off Etsy offsite ads?",
        "answer": "If you're under $10,000/year in sales, you can opt out of offsite ads. If your profit margin is already thin (under 20%), consider disabling them to save the 15% fee. If over $10k/year, offsite ads are mandatory."
    }
]

render_schema_faq(faqs)

# ==================== FINAL CTA ====================
st.markdown("""
    <div style="background: #f8f9fa; padding: 3rem 2rem; text-align: center; border-radius: 15px; margin: 3rem 0;">
        <h2 style="color: #2c3e50; margin-bottom: 1rem;">Ready to Analyze Your Entire Shop?</h2>
        <p style="font-size: 1.1rem; color: #7f8c8d; margin-bottom: 2rem;">
            Stop calculating one product at a time. Upload your Etsy data and get instant insights across your entire catalog.
        </p>
        <a href="/auth" style="display: inline-block; background: #667eea; color: white; padding: 1rem 2.5rem; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 1.1rem;">
            Get Started Free →
        </a>
    </div>
""", unsafe_allow_html=True)