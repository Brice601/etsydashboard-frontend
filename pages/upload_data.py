"""
📤 Upload Your Etsy Data - Centralized Upload Page
Upload once, analyze everywhere (Finance, Customer, SEO)
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Upload Data - Etsy Dashboard",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== AUTHENTICATION ====================
if 'user_id' not in st.session_state:
    st.error("❌ Session expired. Please log in again.")
    st.switch_page("pages/auth.py")
    st.stop()

user_email = st.session_state.get('email', 'User')

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .upload-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .file-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================

def load_csv_file(uploaded_file, file_type):
    """Load and validate CSV file"""
    try:
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except:
            try:
                df = pd.read_csv(uploaded_file, encoding='latin-1')
            except:
                df = pd.read_csv(uploaded_file, encoding='cp1252')
        
        st.success(f"✅ {file_type}: {len(df)} rows loaded")
        return df, None
    except Exception as e:
        st.error(f"❌ Error loading {file_type}: {str(e)}")
        return None, str(e)


def load_json_file(uploaded_file, file_type):
    """Load and validate JSON file"""
    try:
        data = json.load(uploaded_file)
        st.success(f"✅ {file_type}: {len(data)} reviews loaded")
        return data, None
    except Exception as e:
        st.error(f"❌ Error loading {file_type}: {str(e)}")
        return None, str(e)


def check_data_status():
    """Check which data files are already uploaded"""
    status = {
        'sold_items_df': '❌ Not uploaded',
        'payments_df': '❌ Not uploaded',
        'sold_orders_df': '❌ Not uploaded',
        'reviews_data': '❌ Not uploaded',
        'listings_df': '❌ Not uploaded'
    }
    
    for key in status.keys():
        if key in st.session_state and st.session_state[key] is not None:
            if isinstance(st.session_state[key], pd.DataFrame):
                status[key] = f"✅ Uploaded ({len(st.session_state[key])} rows)"
            elif isinstance(st.session_state[key], list):
                status[key] = f"✅ Uploaded ({len(st.session_state[key])} items)"
            else:
                status[key] = "✅ Uploaded"
    
    return status


# ==================== MAIN UI ====================

st.markdown("# 📤 Upload Your Etsy Data")

st.markdown("""
<div class="info-box">
<strong>ℹ️ How it works:</strong>
<ul>
<li>Upload your Etsy CSV files <strong>once</strong></li>
<li>Navigate to any dashboard (Finance, Customer, SEO)</li>
<li>Your data will be automatically available everywhere</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ==================== DATA STATUS ====================
st.markdown("---")
st.markdown("## 📊 Current Data Status")

data_status = check_data_status()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💰 Finance Pro")
    st.markdown(f"**Sold Order Items:** {data_status['sold_items_df']}")
    st.markdown(f"**Payments:** {data_status['payments_df']}")

with col2:
    st.markdown("### 👥 Customer Intelligence")
    st.markdown(f"**Sold Orders:** {data_status['sold_orders_df']}")
    st.markdown(f"**Reviews:** {data_status['reviews_data']}")

with col3:
    st.markdown("### 🔍 SEO Analyzer")
    st.markdown(f"**Listings:** {data_status['listings_df']}")

# ==================== UPLOAD SECTION ====================
st.markdown("---")
st.markdown("## 📤 Upload Files")

st.markdown("""
<div class="info-box">
<strong>💡 Where to download these files from Etsy:</strong>
<ol>
<li>Go to <strong>Shop Manager</strong> → <strong>Settings</strong> → <strong>Options</strong></li>
<li>Click <strong>"Download Data"</strong></li>
<li>Select <strong>2024</strong> (or your desired year)</li>
<li>Download: <strong>Sold Order Items</strong>, <strong>Sold Orders</strong>, <strong>Direct Checkout Payments</strong>, <strong>Listings</strong></li>
<li>For reviews: Go to <strong>Reviews</strong> → <strong>Export</strong></li>
</ol>
</div>
""", unsafe_allow_html=True)

# Upload widgets
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 💰 Finance Pro Data")
    
    sold_items_file = st.file_uploader(
        "📊 Sold Order Items (2024)",
        type=['csv'],
        key='sold_items_upload',
        help="EtsySoldOrderItems2024.csv - Contains individual item sales"
    )
    
    payments_file = st.file_uploader(
        "💳 Direct Checkout Payments",
        type=['csv'],
        key='payments_upload',
        help="EtsyDirectCheckoutPayments2024.csv - Contains actual Etsy fees charged"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 🔍 SEO Analyzer Data")
    
    listings_file = st.file_uploader(
        "📋 Listings Download",
        type=['csv'],
        key='listings_upload',
        help="EtsyListingsDownload.csv - Contains your active listings with titles, tags, descriptions"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 👥 Customer Intelligence Data")
    
    sold_orders_file = st.file_uploader(
        "📦 Sold Orders (2024)",
        type=['csv'],
        key='sold_orders_upload',
        help="EtsySoldOrders2024.csv - Contains order-level information with buyer details"
    )
    
    reviews_file = st.file_uploader(
        "⭐ Reviews (JSON)",
        type=['json'],
        key='reviews_upload',
        help="reviews.json - Contains customer reviews and ratings"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PROCESS BUTTON ====================
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("✅ Upload & Process All Files", type="primary", use_container_width=True):
        with st.spinner("Processing files..."):
            any_uploaded = False
            
            # Process Sold Items
            if sold_items_file:
                df, error = load_csv_file(sold_items_file, "Sold Order Items")
                if df is not None:
                    st.session_state['sold_items_df'] = df
                    st.session_state['sold_items_upload_date'] = datetime.now()
                    any_uploaded = True
            
            # Process Payments
            if payments_file:
                df, error = load_csv_file(payments_file, "Direct Checkout Payments")
                if df is not None:
                    st.session_state['payments_df'] = df
                    st.session_state['payments_upload_date'] = datetime.now()
                    any_uploaded = True
            
            # Process Sold Orders
            if sold_orders_file:
                df, error = load_csv_file(sold_orders_file, "Sold Orders")
                if df is not None:
                    st.session_state['sold_orders_df'] = df
                    st.session_state['sold_orders_upload_date'] = datetime.now()
                    any_uploaded = True
            
            # Process Reviews
            if reviews_file:
                data, error = load_json_file(reviews_file, "Reviews")
                if data is not None:
                    st.session_state['reviews_data'] = data
                    st.session_state['reviews_upload_date'] = datetime.now()
                    any_uploaded = True
            
            # Process Listings
            if listings_file:
                df, error = load_csv_file(listings_file, "Listings")
                if df is not None:
                    st.session_state['listings_df'] = df
                    st.session_state['listings_upload_date'] = datetime.now()
                    any_uploaded = True
            
            if any_uploaded:
                st.success("✅ Files uploaded successfully!")
                st.balloons()
                
                st.markdown("""
                <div class="success-box">
                <strong>🎉 Ready to analyze!</strong><br>
                Navigate to your desired dashboard:
                <ul>
                <li><strong>💰 Finance Pro</strong> - Profit margins, fees analysis, product performance</li>
                <li><strong>👥 Customer Intelligence</strong> - Customer behavior, reviews, geographic analysis</li>
                <li><strong>🔍 SEO Analyzer</strong> - Listing optimization, tags performance</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ No files selected. Please upload at least one file.")

# ==================== CLEAR DATA OPTION ====================
if any(key in st.session_state for key in ['sold_items_df', 'payments_df', 'sold_orders_df', 'reviews_data', 'listings_df']):
    st.markdown("---")
    st.markdown("### 🗑️ Clear Uploaded Data")
    
    if st.button("🗑️ Clear All Data", help="Remove all uploaded files from memory"):
        keys_to_clear = ['sold_items_df', 'payments_df', 'sold_orders_df', 
                         'reviews_data', 'listings_df',
                         'sold_items_upload_date', 'payments_upload_date',
                         'sold_orders_upload_date', 'reviews_upload_date', 
                         'listings_upload_date']
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        st.success("✅ All data cleared!")
        st.rerun()

# ==================== NAVIGATION ====================
st.markdown("---")
st.markdown("## 🚀 Navigate to Dashboards")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💰 Finance Pro", use_container_width=True):
        st.switch_page("pages/etsy_finance_pro.py")

with col2:
    if st.button("👥 Customer Intelligence", use_container_width=True):
        st.switch_page("pages/etsy_customer_intelligence.py")

with col3:
    if st.button("🔍 SEO Analyzer", use_container_width=True):
        st.switch_page("pages/etsy_seo_analyzer.py")
        
# ==================== HELP SECTION ====================
st.markdown("---")
st.markdown("## ❓ Need Help?")

with st.expander("🔍 How to download Etsy data files"):
    st.markdown("""
    ### Step-by-step guide:
    
    **1. Go to Etsy Shop Manager**
    - Log into your Etsy account
    - Click on "Shop Manager"
    
    **2. Access Download Data**
    - Go to "Settings" → "Options"
    - Click "Download Data"
    
    **3. Select Year & Files**
    - Select year: 2024 (or your desired period)
    - Check the following files:
      - ✅ Sold Order Items
      - ✅ Sold Orders
      - ✅ Direct Checkout Payments
      - ✅ Listings
    
    **4. Download Reviews**
    - Go to "Marketing" → "Reviews"
    - Click "Export" to download reviews.json
    
    **5. Upload Here**
    - Return to this page
    - Upload all downloaded files
    - Click "Upload & Process All Files"
    """)

with st.expander("🔒 Is my data secure?"):
    st.markdown("""
    ### Data Security & Privacy
    
    ✅ **Your data never leaves your browser**
    - Files are processed locally in your session
    - No data is sent to external servers
    - Files are stored temporarily in memory
    
    ✅ **Session-based storage**
    - Data exists only during your session
    - Automatically cleared when you log out
    - You can manually clear data anytime
    
    ✅ **Privacy-first approach**
    - We don't see or store your raw data
    - Only aggregated analytics are used to improve the tool
    - Your customer information remains private
    """)

with st.expander("💡 What if I'm missing a file?"):
    st.markdown("""
    ### Don't worry!
    
    **Each dashboard works independently:**
    
    - **Finance Pro** works with:
      - Sold Order Items (required)
      - Payments (optional, for fee validation)
    
    - **Customer Intelligence** works with:
      - Sold Orders (required)
      - Reviews (optional, for sentiment analysis)
    
    - **SEO Analyzer** works with:
      - Listings (required)
      - Sold Order Items (optional, for performance data)
    
    **You can upload files progressively as you get them!**
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Etsy Dashboard</strong> - Upload Data</p>
    <p style='font-size: 0.9em;'>Upload once, analyze everywhere</p>
</div>
""", unsafe_allow_html=True)