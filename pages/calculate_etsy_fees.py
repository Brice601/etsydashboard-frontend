"""
Calculate Etsy Fees Landing Page - ENHANCED VERSION
Free calculator with instant results + pricing scenarios + opportunities detection
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
    
    /* NEW: Opportunity alert box */
    .opportunity-box {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .opportunity-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .opportunity-item {
        background: rgba(255,255,255,0.2);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* NEW: Scenario comparison */
    .scenario-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    .scenario-card.best {
        border: 3px solid #27ae60;
        box-shadow: 0 4px 20px rgba(39, 174, 96, 0.3);
    }
    
    .scenario-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin-bottom: 0.5rem;
    }
    
    .scenario-price {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 0.5rem 0;
    }
    
    .scenario-profit {
        font-size: 1.5rem;
        color: #27ae60;
        font-weight: bold;
    }
    
    .scenario-details {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin-top: 0.5rem;
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
    
    /* NEW: Category examples table */
    .category-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.5rem 0;
    }
    
    .category-table th {
        background: #667eea;
        color: white;
        padding: 1rem;
        text-align: left;
        font-weight: bold;
    }
    
    .category-table td {
        padding: 0.8rem 1rem;
        border-bottom: 1px solid #dee2e6;
    }
    
    .category-table tr:hover {
        background: #f8f9fa;
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

# Calculate fees for current price
def calculate_profit(price, prod_cost, ship_cost, offsite_enabled):
    transaction_fee = price * 0.065
    listing_fee = 0.20
    payment_processing = (price * 0.03) + 0.25
    offsite_fee = price * 0.15 if offsite_enabled else 0.0
    
    total_fees = transaction_fee + listing_fee + payment_processing + offsite_fee
    net_revenue = price - total_fees
    profit = net_revenue - prod_cost - ship_cost
    margin = (profit / price * 100) if price > 0 else 0
    
    return {
        'transaction_fee': transaction_fee,
        'listing_fee': listing_fee,
        'payment_processing': payment_processing,
        'offsite_fee': offsite_fee,
        'total_fees': total_fees,
        'profit': profit,
        'margin': margin
    }

current = calculate_profit(sale_price, production_cost, shipping_cost, offsite_ads)

# ==================== MAIN RESULTS ====================
st.markdown("### 📊 Your Results")

# Main result box
result_class = "result-box"
if current['profit'] < 0:
    result_class += " danger"
elif current['margin'] < 20:
    result_class += " warning"

st.markdown(f"""
    <div class="{result_class}">
        <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">Net Profit Per Sale</div>
        <div class="big-number {'negative' if current['profit'] < 0 else ''}">${current['profit']:.2f}</div>
        <div style="font-size: 1rem; opacity: 0.8;">
            {current['margin']:.1f}% profit margin
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
            <span>-${current['transaction_fee']:.2f}</span>
        </div>
        <div class="fee-item">
            <span>Listing Fee</span>
            <span>-${current['listing_fee']:.2f}</span>
        </div>
        <div class="fee-item">
            <span>Payment Processing (3% + $0.25)</span>
            <span>-${current['payment_processing']:.2f}</span>
        </div>
        <div class="fee-item">
            <span>Offsite Ads (15%)</span>
            <span>-${current['offsite_fee']:.2f}</span>
        </div>
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
            <span style="color: {'#e74c3c' if current['profit'] < 0 else '#27ae60'};">${current['profit']:.2f}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Monthly projection
monthly_profit_current = current['profit'] * monthly_sales

st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">📈 Monthly Projection</div>
        <p style="font-size: 1.1rem; margin: 0.5rem 0;">
            At {monthly_sales} sales/month, you'll make: <strong>${monthly_profit_current:.2f}/month</strong>
        </p>
        <p style="font-size: 0.9rem; opacity: 0.8; margin: 0;">
            Annual projection: ${monthly_profit_current * 12:.2f}/year
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== NEW: PRICING SCENARIOS ====================
st.markdown("---")
st.markdown("### 🎯 Pricing Strategy Simulator")
st.markdown("**See how different prices impact your monthly profit:**")

# Calculate 3 scenarios
price_low = sale_price * 0.90  # -10%
price_high = sale_price * 1.10  # +10%

# Volume estimates (simple elasticity model)
volume_low = int(monthly_sales * 1.20)  # -10% price = +20% volume (elastic)
volume_current = monthly_sales
volume_high = int(monthly_sales * 0.85)  # +10% price = -15% volume

scenario_low = calculate_profit(price_low, production_cost, shipping_cost, offsite_ads)
scenario_high = calculate_profit(price_high, production_cost, shipping_cost, offsite_ads)

monthly_low = scenario_low['profit'] * volume_low
monthly_high = scenario_high['profit'] * volume_high

# Find best scenario
scenarios = [
    {'name': 'Lower Price (-10%)', 'price': price_low, 'volume': volume_low, 'profit': scenario_low['profit'], 'monthly': monthly_low, 'margin': scenario_low['margin']},
    {'name': 'Current Price', 'price': sale_price, 'volume': volume_current, 'profit': current['profit'], 'monthly': monthly_profit_current, 'margin': current['margin']},
    {'name': 'Higher Price (+10%)', 'price': price_high, 'volume': volume_high, 'profit': scenario_high['profit'], 'monthly': monthly_high, 'margin': scenario_high['margin']}
]

best_scenario = max(scenarios, key=lambda x: x['monthly'])

col1, col2, col3 = st.columns(3)

for idx, (col, scenario) in enumerate(zip([col1, col2, col3], scenarios)):
    with col:
        is_best = scenario == best_scenario
        card_class = "scenario-card best" if is_best else "scenario-card"
        
        st.markdown(f"""
            <div class="{card_class}">
                <div class="scenario-label">{scenario['name']}</div>
                <div class="scenario-price">${scenario['price']:.2f}</div>
                <div class="scenario-profit">${scenario['monthly']:.2f}/mo</div>
                <div class="scenario-details">
                    {scenario['volume']} sales/mo<br>
                    ${scenario['profit']:.2f}/sale ({scenario['margin']:.1f}%)
                </div>
                {'<div style="color: #27ae60; font-weight: bold; margin-top: 0.5rem;">✅ BEST OPTION</div>' if is_best else ''}
            </div>
        """, unsafe_allow_html=True)

st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">💡 Pricing Recommendation</div>
        <p>Based on your inputs, <strong>{best_scenario['name'].lower()}</strong> maximizes monthly profit at <strong>${best_scenario['monthly']:.2f}/month</strong>.</p>
        <p style="font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;">
            Note: Volume estimates assume moderate price elasticity. Test different prices to find your sweet spot!
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== NEW: OPPORTUNITY ALERTS ====================
st.markdown("---")

opportunities = []
potential_savings = 0

# Detect opportunities
if offsite_ads and current['margin'] < 25:
    savings = current['offsite_fee'] * monthly_sales
    opportunities.append({
        'title': 'Disable Offsite Ads',
        'savings': savings,
        'description': f"You're paying ${current['offsite_fee']:.2f}/sale for offsite ads with only {current['margin']:.1f}% margin. That's ${savings:.2f}/month you could save."
    })
    potential_savings += savings

if current['margin'] < 20:
    target_price = (production_cost + shipping_cost + current['total_fees']) / 0.75
    price_increase = target_price - sale_price
    additional_profit = (price_increase * 0.75) * monthly_sales  # 75% goes to profit after fees
    opportunities.append({
        'title': 'Optimize Your Pricing',
        'savings': additional_profit,
        'description': f"Increasing price to ${target_price:.2f} (25% margin) would add ${additional_profit:.2f}/month profit."
    })
    potential_savings += additional_profit

if shipping_cost > 3.0 and sale_price > 25:
    shipping_savings = (shipping_cost - 2.5) * monthly_sales
    opportunities.append({
        'title': 'Negotiate Shipping Rates',
        'savings': shipping_savings,
        'description': f"Reducing shipping from ${shipping_cost:.2f} to $2.50 could save ${shipping_savings:.2f}/month."
    })
    potential_savings += shipping_savings

# Calculate breakeven point
fixed_costs = 10 if etsy_plus else 0
if fixed_costs > 0:
    breakeven_sales = fixed_costs / current['profit'] if current['profit'] > 0 else 0
    if breakeven_sales > monthly_sales:
        wasted = (breakeven_sales - monthly_sales) * current['profit']
        opportunities.append({
            'title': 'Etsy Plus Not Worth It Yet',
            'savings': 10,
            'description': f"You need {int(breakeven_sales)} sales/month to break even on Etsy Plus. Currently at {monthly_sales} sales."
        })
        potential_savings += 10

if opportunities:
    st.markdown(f"""
        <div class="opportunity-box">
            <div class="opportunity-title">⚠️ You're Potentially Losing ${potential_savings:.2f}/Month</div>
            <p style="margin-bottom: 1rem;">We've identified {len(opportunities)} optimization opportunities:</p>
    """, unsafe_allow_html=True)
    
    for opp in opportunities:
        st.markdown(f"""
            <div class="opportunity-item">
                <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.3rem;">
                    {opp['title']} → +${opp['savings']:.2f}/month
                </div>
                <div style="font-size: 0.9rem; opacity: 0.9;">
                    {opp['description']}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            <p style="margin-top: 1rem; font-size: 1rem;">
                Want detailed action plans for each opportunity? Upload your full shop data to get personalized recommendations.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Basic insights if no opportunities
if current['profit'] > 0 and current['margin'] >= 25 and not opportunities:
    st.markdown(f"""
        <div class="result-box">
            <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">✅ Your Pricing is Optimized!</div>
            <p>Your {current['margin']:.1f}% margin is healthy. Focus on increasing sales volume to grow revenue.</p>
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

# ==================== NEW: ENHANCED SEO CONTENT ====================
st.markdown("---")
st.markdown("## Complete Guide to Calculating Etsy Profit Margins (2025)")

st.markdown("""
Understanding your true Etsy profit margin is crucial for running a sustainable business. Many sellers make the mistake of only looking at sale price minus production costs, but **Etsy takes an average of 12-17% in fees** before you see any money.

### The Real Cost of Selling on Etsy

Here's what every seller needs to account for when calculating profit:

**Fixed Etsy Fees:**
- Transaction Fee: 6.5% of sale price (including shipping)
- Listing Fee: $0.20 per listing (4 months or until sold)
- Payment Processing: 3% + $0.25 per transaction
- Etsy Plus: $10/month (optional)

**Variable Fees:**
- Offsite Ads: 12-15% of sale price (mandatory if over $10k/year revenue)
- Etsy Ads: Variable budget you set
- Currency conversion: ~2.5% if selling internationally

**Hidden Costs:**
- Shipping materials (boxes, padding, labels)
- Postage and delivery
- Production time (your labor)
- Material costs
- Packaging and branding
- Photography and listing setup time

### Etsy Fee Calculator by Category

Different product categories have different typical margins. Here's what healthy profit margins look like:
""")

# Category comparison table
st.markdown("""
<table class="category-table">
    <thead>
        <tr>
            <th>Category</th>
            <th>Avg Price</th>
            <th>Typical COGS</th>
            <th>Etsy Fees</th>
            <th>Healthy Margin</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Jewelry (Handmade)</strong></td>
            <td>$35-80</td>
            <td>$10-25</td>
            <td>$4-10</td>
            <td>30-40%</td>
        </tr>
        <tr>
            <td><strong>Art Prints</strong></td>
            <td>$20-50</td>
            <td>$3-8</td>
            <td>$2-6</td>
            <td>40-50%</td>
        </tr>
        <tr>
            <td><strong>Home Decor</strong></td>
            <td>$40-100</td>
            <td>$15-40</td>
            <td>$5-12</td>
            <td>25-35%</td>
        </tr>
        <tr>
            <td><strong>Clothing</strong></td>
            <td>$30-70</td>
            <td>$12-30</td>
            <td>$3-8</td>
            <td>20-30%</td>
        </tr>
        <tr>
            <td><strong>Digital Downloads</strong></td>
            <td>$5-20</td>
            <td>$0-2</td>
            <td>$0.50-2</td>
            <td>70-90%</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

st.markdown("""
### How to Calculate Your Breakeven Point

Your breakeven point is where revenue equals all costs. Use this formula:

**Breakeven Sales = Fixed Monthly Costs ÷ Profit Per Sale**

For example:
- Fixed costs: $50/month (Etsy Plus $10 + shipping supplies $40)
- Profit per sale: $8.50
- Breakeven: $50 ÷ $8.50 = 6 sales/month needed

If you're selling fewer than your breakeven point, you're losing money overall.

### Common Etsy Pricing Mistakes

1. **Forgetting Offsite Ads:** If you're over $10k/year, Etsy automatically deducts 12% when they advertise your product externally. This can turn a 20% margin into 8% overnight.

2. **Not Factoring Labor:** Your time has value. If a product takes 2 hours to make and you want $20/hour, that's $40 in labor costs.

3. **Underestimating Shipping:** International shipping can cost $15-30 but sellers often charge $5-10, eating into profit.

4. **Ignoring Returns:** Plan for 2-5% of orders to be returned or refunded. This affects your true profit margin.

5. **Seasonal Variations:** December sales might be 3x higher than July. Calculate annual averages, not monthly peaks.

### When to Raise Your Prices

You should consider raising prices if:
- Your profit margin is below 20%
- You're selling out consistently (high demand)
- Your material costs have increased
- Competitors charge 20%+ more for similar items
- You're spending hours on customer service for low-margin items

**Pro tip:** Test price increases on new listings first before changing existing bestsellers.

### How to Reduce Etsy Fees Without Hurting Sales

1. **Optimize for Free Shipping:** Build shipping into your price and offer "free shipping" - customers prefer it and you can optimize costs.

2. **Use Digital Marketing:** Drive your own traffic to reduce reliance on Etsy's offsite ads (only works if under $10k/year).

3. **Bundle Products:** Sell sets or bundles - you pay Etsy fees once but sell 3-5 items.

4. **Improve SEO:** Better organic ranking means less need for paid Etsy Ads.

5. **Negotiate Shipping:** Once you're shipping 50+ orders/month, negotiate discounted rates with carriers.

### Calculating ROI on Etsy Ads

If you're using Etsy Ads, track this metric:

**Ad ROI = (Revenue from Ads - Ad Spend) ÷ Ad Spend × 100**

Healthy ad ROI is 300%+ (you make $3 for every $1 spent). Below 200% and you might want to pause ads and focus on organic SEO.

### Understanding the "Sweet Spot" Pricing

There's a magical price point where volume × margin = maximum profit. It's rarely the highest price you *could* charge.

Example:
- At $50: 10 sales/month × $15 profit = $150/month
- At $40: 18 sales/month × $12 profit = $216/month ← Sweet spot!
- At $30: 30 sales/month × $8 profit = $240/month

Use our calculator above to test different scenarios and find your sweet spot.
""")

st.markdown("---")
st.markdown("## Understanding Etsy Fees in Detail")

st.markdown("""
### Transaction Fee (6.5%)
Etsy charges 6.5% of your item's sale price (including shipping). This is their main revenue source and applies to every sale. **Cannot be avoided.**

### Listing Fee ($0.20)
Each listing costs $0.20 and lasts for 4 months or until sold. If you auto-renew, that's another $0.20. For shops with 100+ listings, this adds up to $20-40/month.

### Payment Processing (3% + $0.25)
Etsy Payments charges 3% + $0.25 per transaction to process credit cards and handle the money transfer. Similar to PayPal or Stripe rates.

### Offsite Ads (12-15%)
**This is the controversial one.** If Etsy advertises your product on Google, Facebook, Pinterest, or other platforms and makes a sale:
- 15% fee if you make under $10,000/year (opt-out available)
- 12% fee if you make over $10,000/year (**mandatory**, cannot opt out)

Many sellers are surprised by this fee because it only appears *after* the sale is made. If 20% of your sales come from offsite ads, that's an extra 3% fee on your entire revenue.

### Hidden Costs to Track
Don't forget:
- Shipping materials: $1-3 per order
- Postage: Variable by location
- Production time: Your hourly rate
- Packaging: Branded boxes, tissue paper, stickers
- Etsy Plus: $10/month (includes $5 ad credit + custom shop URL)
- Etsy Ads budget: If you use promoted listings
- Business licenses: $50-200/year depending on location
- Accounting software: $10-50/month

**The average Etsy seller pays 15-20% in total fees and costs**, meaning a $30 sale nets around $24-25.5 before production costs.
""")

st.markdown("### How to Reduce Etsy Fees")

st.markdown("""
1. **Disable Offsite Ads** (if under $10k/year revenue) - saves 15% per offsite sale
2. **Use Free Shipping strategically** - build shipping into your price to qualify for search boosts
3. **Bundle products** - pay fees once but sell more items per transaction
4. **Optimize listings for SEO** - better organic ranking = less need for paid ads
5. **Track everything religiously** - know your real profit margins on each product
6. **Raise prices gradually** - Test 10% increases on new listings to see impact on conversions
7. **Focus on high-margin products** - Phase out items with <20% margins
8. **Negotiate shipping rates** - Once at volume, get carrier discounts

Want to track all this automatically across your entire product catalog? **[Try our free Etsy Dashboard](/auth)** - upload your CSV and see profitability, best sellers, and optimization opportunities instantly.
""")

# ==================== FAQ SCHEMA ====================
st.markdown("---")
st.markdown("## Frequently Asked Questions")

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
    },
    {
        "question": "What's a good profit margin on Etsy?",
        "answer": "A healthy profit margin on Etsy is 25-35% after all fees and costs. Below 20% is risky, above 40% means you might be overpricing. Digital products can achieve 70-90% margins."
    },
    {
        "question": "How do I calculate my Etsy profit margin?",
        "answer": "Profit Margin = (Sale Price - All Fees - Production Costs - Shipping) ÷ Sale Price × 100. Use our free calculator above to see your exact margin in seconds."
    }
]

render_schema_faq(faqs)

# ==================== FINAL CTA ====================
st.markdown("""
    <div style="background: #f8f9fa; padding: 3rem 2rem; text-align: center; border-radius: 15px; margin: 3rem 0;">
        <h2 style="color: #2c3e50; margin-bottom: 1rem;">Ready to Optimize Your Entire Etsy Shop?</h2>
        <p style="font-size: 1.1rem; color: #7f8c8d; margin-bottom: 2rem;">
            Stop calculating one product at a time. Upload your Etsy data and get instant insights across your entire catalog - profit by product, pricing opportunities, customer behavior, and SEO optimization.
        </p>
        <a href="/auth" style="display: inline-block; background: #667eea; color: white; padding: 1rem 2.5rem; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 1.1rem;">
            Get Started Free →
        </a>
        <p style="font-size: 0.9rem; color: #95a5a6; margin-top: 1rem;">
            3 complete dashboards • No credit card • 2 minute setup
        </p>
    </div>
""", unsafe_allow_html=True)