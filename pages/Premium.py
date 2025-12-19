"""
Premium Upgrade Page
Subscription management and upgrade to Insights Premium
"""

import streamlit as st
from components.seo_meta import hide_streamlit_elements
from utils.helpers import format_currency

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Upgrade to Premium - Etsy Dashboard",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit elements
hide_streamlit_elements()

# ==================== AUTHENTICATION CHECK ====================
if 'user_id' not in st.session_state or not st.session_state.user_id:
    st.warning("🔒 Please log in to upgrade")
    st.markdown("""
        <meta http-equiv="refresh" content="2;url=/auth">
    """, unsafe_allow_html=True)
    st.info("🔄 Redirecting to login...")
    st.stop()

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .premium-hero {
        background: linear-gradient(135deg, #F56400 0%, #ff7a1a 100%);
        padding: 4rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .premium-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .premium-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        margin-bottom: 2rem;
    }
    
    .comparison-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .plan-card {
        background: white;
        border-radius: 15px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        position: relative;
    }
    
    .plan-card.featured {
        border: 3px solid #F56400;
        transform: scale(1.05);
    }
    
    .plan-badge {
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
    
    .plan-name {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .plan-price {
        font-size: 3rem;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .plan-period {
        color: #7f8c8d;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .plan-features {
        list-style: none;
        padding: 0;
        margin: 2rem 0;
        text-align: left;
    }
    
    .plan-features li {
        padding: 0.75rem 0;
        color: #2c3e50;
        line-height: 1.5;
    }
    
    .plan-features li:before {
        content: "✅ ";
        margin-right: 0.5rem;
    }
    
    .plan-features li.premium-only {
        font-weight: bold;
        color: #F56400;
    }
    
    .plan-features li.premium-only:before {
        content: "✨ ";
    }
    
    .upgrade-button {
        display: block;
        background: #F56400;
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        text-align: center;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        font-size: 1.1rem;
    }
    
    .upgrade-button:hover {
        background: #ff7a1a;
        transform: scale(1.05);
    }
    
    .upgrade-button.secondary {
        background: #95a5a6;
    }
    
    .upgrade-button.secondary:hover {
        background: #7f8c8d;
    }
    
    .feature-comparison {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 3rem 0;
    }
    
    .testimonial {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #F56400;
        margin: 1rem 0;
    }
    
    .testimonial-text {
        font-style: italic;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .testimonial-author {
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    
    .faq-item {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    
    .faq-question {
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .faq-answer {
        color: #7f8c8d;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
is_premium = st.session_state.get('is_premium', False)

# ==================== HERO SECTION ====================
st.markdown("""
    <div class="premium-hero">
        <div class="premium-title">✨ Upgrade to Insights Premium</div>
        <div class="premium-subtitle">
            Unlock AI-powered recommendations and unlimited analyses
        </div>
        <p style="font-size: 1rem; opacity: 0.9;">
            Transform your Etsy shop with advanced insights • Cancel anytime
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== PRICING COMPARISON ====================
st.markdown("## 💎 Choose Your Plan")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="plan-card">
            <div class="plan-name">Free Forever</div>
            <div class="plan-price">$0</div>
            <div class="plan-period">Always free</div>
            
            <ul class="plan-features">
                <li>Finance Pro Dashboard</li>
                <li>Customer Intelligence Dashboard</li>
                <li>SEO Analyzer Dashboard</li>
                <li>10 analyses per week</li>
                <li>CSV uploads</li>
                <li>All core metrics</li>
                <li>Email support</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if is_premium:
        st.info("✅ You currently have the Free plan as a fallback")
    else:
        st.info("✅ You're currently on the Free plan")

with col2:
    st.markdown("""
        <div class="plan-card featured">
            <span class="plan-badge">Most Popular</span>
            <div class="plan-name">Insights Premium</div>
            <div class="plan-price">$9</div>
            <div class="plan-period">per month</div>
            
            <ul class="plan-features">
                <li>Everything in Free</li>
                <li class="premium-only">Unlimited analyses</li>
                <li class="premium-only">AI-powered recommendations</li>
                <li class="premium-only">Priority optimization lists</li>
                <li class="premium-only">Advanced profitability insights</li>
                <li class="premium-only">Customer re-engagement strategies</li>
                <li class="premium-only">Priority support</li>
                <li class="premium-only">Early access to new features</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if is_premium:
        st.success("✅ You're currently on Premium!")
        if st.button("Manage Subscription", use_container_width=True):
            st.info("💡 Subscription management coming soon")
    else:
        if st.button("🚀 Upgrade to Premium", type="primary", use_container_width=True):
            st.session_state.show_checkout = True
            st.rerun()

# ==================== CHECKOUT MODAL ====================
if st.session_state.get('show_checkout', False):
    st.markdown("---")
    st.markdown("### 💳 Complete Your Upgrade")
    
    with st.form("checkout_form"):
        st.markdown("""
            <div style="background: #e8f5e9; padding: 1rem; border-radius: 10px; 
                        border-left: 5px solid #27ae60; margin-bottom: 2rem;">
                <strong>✅ You're upgrading to Insights Premium</strong><br>
                $9/month • Unlimited analyses • AI recommendations • Cancel anytime
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
            card_name = st.text_input("Cardholder Name", placeholder="John Doe")
        
        with col2:
            card_expiry = st.text_input("Expiry Date", placeholder="MM/YY")
            card_cvc = st.text_input("CVC", placeholder="123", type="password")
        
        st.markdown("""
            <div style="font-size: 0.9rem; color: #7f8c8d; margin: 1rem 0;">
                🔒 Secure payment processed by Stripe. Your information is encrypted and safe.
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submitted = st.form_submit_button("💳 Complete Upgrade ($9/mo)", 
                                             type="primary", 
                                             use_container_width=True)
        
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.show_checkout = False
                st.rerun()
        
        if submitted:
            with st.spinner("Processing payment..."):
                import time
                time.sleep(2)
                st.session_state.is_premium = True
                st.session_state.show_checkout = False
                st.success("✅ Welcome to Premium! Your upgrade is complete.")
                st.balloons()
                time.sleep(2)
                st.rerun()

# ==================== FEATURE COMPARISON TABLE ====================
st.markdown("---")
st.markdown("## 📊 Detailed Feature Comparison")

comparison_data = {
    "Feature": [
        "Finance Pro Dashboard",
        "Customer Intelligence",
        "SEO Analyzer",
        "Weekly Analyses",
        "CSV Uploads",
        "Core Metrics",
        "AI Recommendations",
        "Priority Optimization Lists",
        "Advanced Profitability Insights",
        "Re-engagement Strategies",
        "Support"
    ],
    "Free": ["✅", "✅", "✅", "10/week", "✅", "✅", "❌", "❌", "❌", "❌", "Email"],
    "Premium": ["✅", "✅", "✅", "Unlimited", "✅", "✅", "✅", "✅", "✅", "✅", "Priority"]
}

cols = st.columns([3, 1, 1])

with cols[0]:
    st.markdown("**Feature**")
with cols[1]:
    st.markdown("**Free**")
with cols[2]:
    st.markdown("**Premium**")

for i in range(len(comparison_data["Feature"])):
    cols = st.columns([3, 1, 1])
    with cols[0]:
        st.markdown(comparison_data["Feature"][i])
    with cols[1]:
        st.markdown(comparison_data["Free"][i])
    with cols[2]:
        if comparison_data["Premium"][i] not in ["✅", "❌"]:
            st.markdown(f"**{comparison_data['Premium'][i]}**")
        else:
            st.markdown(comparison_data["Premium"][i])

# ==================== TESTIMONIALS ====================
st.markdown("---")
st.markdown("## 💬 What Premium Users Say")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="testimonial">
            <div class="testimonial-text">
                "The AI recommendations helped me identify my most profitable products. 
                I increased my profit margin by 15% in the first month!"
            </div>
            <div class="testimonial-author">
                - Sarah M., Premium User
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="testimonial">
            <div class="testimonial-text">
                "Unlimited analyses mean I can test different pricing strategies without worrying. 
                Best $9/month I spend on my Etsy business."
            </div>
            <div class="testimonial-author">
                - James T., Premium User
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==================== FAQ ====================
st.markdown("---")
st.markdown("## ❓ Frequently Asked Questions")

faqs = [
    {
        "question": "Can I cancel anytime?",
        "answer": "Yes! You can cancel your Premium subscription at any time. Your account will remain Premium until the end of your billing period, then automatically revert to the free tier."
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept all major credit cards (Visa, Mastercard, American Express) through our secure payment processor, Stripe."
    },
    {
        "question": "Will I lose my data if I downgrade?",
        "answer": "No. All your historical data and analyses remain accessible. You'll just be limited to 10 analyses per week instead of unlimited."
    },
    {
        "question": "What are AI recommendations?",
        "answer": "Our AI analyzes your shop data and provides personalized recommendations for pricing, product focus, customer targeting, and SEO optimization to maximize your profitability."
    },
    {
        "question": "Is there a free trial for Premium?",
        "answer": "We don't offer a separate trial since our Free tier is already feature-rich. You can always upgrade for a month to test Premium features and cancel if it's not right for you."
    }
]

for faq in faqs:
    with st.expander(f"**{faq['question']}**"):
        st.write(faq['answer'])

# ==================== MONEY-BACK GUARANTEE ====================
st.markdown("---")
st.markdown("""
    <div style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%); 
                color: white; padding: 3rem 2rem; border-radius: 15px; text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">💯</div>
        <h2 style="margin-bottom: 1rem;">30-Day Money-Back Guarantee</h2>
        <p style="font-size: 1.1rem; opacity: 0.95;">
            Not satisfied with Premium? Get a full refund within 30 days, no questions asked.
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== FINAL CTA ====================
if not is_premium:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Your Premium Upgrade", type="primary", use_container_width=True):
            st.session_state.show_checkout = True
            st.rerun()