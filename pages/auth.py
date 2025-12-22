"""
Authentication Page
Signup and Login for Etsy Dashboard
"""

import streamlit as st
from utils.api_client import get_api_client, handle_api_error
from utils.helpers import validate_email
from components.seo_meta import hide_streamlit_elements

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Sign Up - Etsy Dashboard",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit elements
hide_streamlit_elements()

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .auth-container {
        max-width: 500px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-title {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .auth-subtitle {
        color: #7f8c8d;
        font-size: 1rem;
    }
    
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 2rem 0;
    }
    
    .divider::before,
    .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #dee2e6;
    }
    
    .divider span {
        padding: 0 1rem;
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    
    .benefits-list {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
    
    .benefits-list ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .benefits-list li {
        padding: 0.5rem 0;
        color: #2c3e50;
    }
    
    .benefits-list li:before {
        content: "✅ ";
        margin-right: 0.5rem;
    }
    
    .switch-mode {
        text-align: center;
        margin-top: 2rem;
        padding-top: 2rem;
        border-top: 1px solid #dee2e6;
    }
    
    .switch-mode a {
        color: #667eea;
        text-decoration: none;
        font-weight: bold;
    }
    
    .switch-mode a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'signup'  # 'signup' or 'login'

if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if 'access_token' not in st.session_state:
    st.session_state.access_token = None

# ==================== HELPER FUNCTIONS ====================

def switch_mode():
    """Toggle between signup and login"""
    if st.session_state.auth_mode == 'signup':
        st.session_state.auth_mode = 'login'
    else:
        st.session_state.auth_mode = 'signup'
    st.rerun()

def handle_signup(email: str, password: str, name: str):
    """Handle user signup"""
    # Validation
    if not email or not password:
        st.error("❌ Please fill in all required fields")
        return
    
    if not validate_email(email):
        st.error("❌ Please enter a valid email address")
        return
    
    if len(password) < 6:
        st.error("❌ Password must be at least 6 characters")
        return
    
    # Call API
    api_client = get_api_client()
    response = api_client.register_user(email, password, name)
    
    if handle_api_error(response):
        return
    
    # Success
    st.session_state.user_id = response.get('user_id')
    st.session_state.access_token = response.get('access_token')
    st.session_state.email = email
    
    st.success("✅ Account created successfully!")
    st.balloons()
    
    # Redirect to dashboard
    st.switch_page("pages/Dashboard.py")

def handle_login(email: str, password: str):
    """Handle user login"""
    # Validation
    if not email or not password:
        st.error("❌ Please fill in all fields")
        return
    
    if not validate_email(email):
        st.error("❌ Please enter a valid email address")
        return
    
    # Call API
    api_client = get_api_client()
    response = api_client.login_user(email, password)
    
    if handle_api_error(response):
        return
    
    # Success
    st.session_state.user_id = response.get('user_id')
    st.session_state.access_token = response.get('access_token')
    st.session_state.email = email
    
    st.success("✅ Logged in successfully!")
    
    # Redirect to dashboard
    st.switch_page("pages/Dashboard.py")

# ==================== MAIN AUTH UI ====================

st.markdown('<div class="auth-container">', unsafe_allow_html=True)

# Header
if st.session_state.auth_mode == 'signup':
    st.markdown("""
        <div class="auth-header">
            <div class="auth-title">Create Your Free Account</div>
            <div class="auth-subtitle">Start analyzing your Etsy shop in 30 seconds</div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="auth-header">
            <div class="auth-title">Welcome Back</div>
            <div class="auth-subtitle">Log in to access your dashboard</div>
        </div>
    """, unsafe_allow_html=True)

# ==================== SIGNUP FORM ====================
if st.session_state.auth_mode == 'signup':
    
    with st.form("signup_form"):
        name = st.text_input(
            "Full Name (optional)",
            placeholder="John Doe",
            help="We'll use this to personalize your experience"
        )
        
        email = st.text_input(
            "Email Address *",
            placeholder="you@example.com",
            help="We'll never share your email"
        )
        
        password = st.text_input(
            "Password *",
            type="password",
            placeholder="At least 6 characters",
            help="Choose a strong password"
        )
        
        # Terms acceptance
        terms_accepted = st.checkbox(
            "I agree to the Terms of Service and Privacy Policy",
            value=False
        )
        
        submitted = st.form_submit_button(
            "Create Free Account",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if not terms_accepted:
                st.error("❌ Please accept the Terms of Service to continue")
            else:
                handle_signup(email, password, name)
    
    # Benefits
    st.markdown("""
        <div class="benefits-list">
            <strong style="display: block; margin-bottom: 1rem; font-size: 1.1rem;">
                What you get for free:
            </strong>
            <ul>
                <li>Finance Pro Dashboard</li>
                <li>Customer Intelligence Dashboard</li>
                <li>SEO Analyzer Dashboard</li>
                <li>10 analyses per week</li>
                <li>CSV upload & automatic analysis</li>
                <li>No credit card required</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# ==================== LOGIN FORM ====================
else:
    
    with st.form("login_form"):
        email = st.text_input(
            "Email Address",
            placeholder="you@example.com"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            remember_me = st.checkbox("Remember me")
        
        with col2:
            st.markdown(
                '<div style="text-align: right;"><a href="#" style="color: #667eea; text-decoration: none; font-size: 0.9rem;">Forgot password?</a></div>',
                unsafe_allow_html=True
            )
        
        submitted = st.form_submit_button(
            "Log In",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            handle_login(email, password)

# ==================== SWITCH MODE ====================
st.markdown('<div class="switch-mode">', unsafe_allow_html=True)

if st.session_state.auth_mode == 'signup':
    st.markdown("""
        Already have an account? 
        <a href="#" onclick="return false;">Log in</a>
    """, unsafe_allow_html=True)
    
    if st.button("Switch to Login", use_container_width=True):
        switch_mode()
else:
    st.markdown("""
        Don't have an account? 
        <a href="#" onclick="return false;">Sign up for free</a>
    """, unsafe_allow_html=True)
    
    if st.button("Switch to Sign Up", use_container_width=True):
        switch_mode()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==================== SOCIAL PROOF ====================
st.markdown("""
    <div style="text-align: center; margin: 3rem 0; color: #7f8c8d;">
        <p style="font-size: 0.9rem; margin-bottom: 1rem;">
            Trusted by hundreds of Etsy sellers worldwide
        </p>
        <div style="font-size: 2rem;">
            ⭐⭐⭐⭐⭐
        </div>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">
            4.8/5 from 127 reviews
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== SECURITY NOTE ====================
st.markdown("""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; 
                text-align: center; margin: 2rem 0;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔒</div>
        <p style="font-size: 0.9rem; color: #7f8c8d; margin: 0;">
            Your data is encrypted and secure. We use bank-level security 
            to protect your information.
        </p>
    </div>
""", unsafe_allow_html=True)