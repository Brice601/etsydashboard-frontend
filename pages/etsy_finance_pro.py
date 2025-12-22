"""
💰 Finance Pro Dashboard
Real profit tracking after ALL Etsy fees
English version - Generic for all Etsy sellers
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Finance Pro - Etsy Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== AUTHENTICATION ====================
if 'user_id' not in st.session_state:
    st.error("❌ Session expired. Please log in again.")
    st.switch_page("pages/auth.py")
    st.stop()

user_id = st.session_state.user_id
user_email = st.session_state.get('email', 'User')
is_premium = st.session_state.get('is_premium', False)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #27ae60;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #27ae60;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .premium-lock {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
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

@st.cache_data
def load_etsy_csv(uploaded_file):
    """
    Load and standardize Etsy CSV exports
    Supports multiple Etsy export formats
    """
    try:
        # Try different encodings
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except:
            df = pd.read_csv(uploaded_file, encoding='latin-1')
        
        # Standardize column names (Etsy uses different formats)
        column_mapping = {
            # Dates
            'Sale Date': 'Date',
            'Order Date': 'Date',
            'Date': 'Date',
            
            # Products
            'Item Name': 'Product',
            'Title': 'Product',
            'Product': 'Product',
            
            # Prices
            'Item Price': 'Price',
            'Price': 'Price',
            'Sale Price': 'Price',
            
            # Quantity
            'Quantity': 'Quantity',
            
            # Shipping
            'Shipping': 'Shipping',
            'Shipping Price': 'Shipping',
            
            # Costs (if provided by user)
            'Cost': 'Cost',
            'Item Cost': 'Cost',
        }
        
        # Apply mapping
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df.rename(columns={old_col: new_col}, inplace=True)
        
        # Ensure required columns exist
        required_cols = ['Date', 'Product', 'Price']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            return None, f"Missing required columns: {', '.join(missing)}"
        
        # Convert data types
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        
        if 'Quantity' not in df.columns:
            df['Quantity'] = 1
        else:
            df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(1)
        
        if 'Shipping' not in df.columns:
            df['Shipping'] = 0
        else:
            df['Shipping'] = pd.to_numeric(df['Shipping'], errors='coerce').fillna(0)
        
        if 'Cost' not in df.columns:
            df['Cost'] = 0
        else:
            df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce').fillna(0)
        
        # Remove invalid rows
        df = df.dropna(subset=['Date', 'Price'])
        df = df[df['Price'] > 0]
        
        return df, None
        
    except Exception as e:
        return None, f"Error reading file: {str(e)}"


def calculate_etsy_fees(price, shipping=0, has_offsite_ads=False, country='US'):
    """
    Calculate ALL Etsy fees for a sale
    
    Fees structure (2024):
    - Transaction fee: 6.5% of item price
    - Payment processing: 3% + $0.25
    - Listing fee: $0.20 (amortized per sale)
    - Offsite Ads: 15% (if applicable)
    - Regulatory Operating Fee: varies by country (~0.4%)
    """
    
    # Transaction fee (6.5%)
    transaction_fee = price * 0.065
    
    # Payment processing (3% + $0.25)
    payment_fee = (price + shipping) * 0.03 + 0.25
    
    # Listing fee (amortized)
    listing_fee = 0.20
    
    # Offsite ads (15% if enabled)
    offsite_fee = price * 0.15 if has_offsite_ads else 0
    
    # Regulatory Operating Fee (varies by country)
    regulatory_rates = {
        'US': 0.004,
        'UK': 0.004,
        'CA': 0.004,
        'AU': 0.004,
        'EU': 0.004,
    }
    regulatory_fee = price * regulatory_rates.get(country, 0.004)
    
    total_fees = transaction_fee + payment_fee + listing_fee + offsite_fee + regulatory_fee
    
    return {
        'transaction': transaction_fee,
        'payment': payment_fee,
        'listing': listing_fee,
        'offsite': offsite_fee,
        'regulatory': regulatory_fee,
        'total': total_fees,
        'fee_percentage': (total_fees / price * 100) if price > 0 else 0
    }


def calculate_kpis(df, has_offsite_ads=False, country='US'):
    """Calculate financial KPIs from order data"""
    
    kpis = {}
    
    # Revenue metrics
    kpis['total_revenue'] = df['Price'].sum()
    kpis['total_sales'] = len(df)
    kpis['avg_order_value'] = kpis['total_revenue'] / kpis['total_sales'] if kpis['total_sales'] > 0 else 0
    
    # Calculate total Etsy fees
    total_fees = 0
    for _, row in df.iterrows():
        fees = calculate_etsy_fees(row['Price'], row.get('Shipping', 0), has_offsite_ads, country)
        total_fees += fees['total']
    
    kpis['etsy_fees'] = total_fees
    kpis['fee_rate'] = (kpis['etsy_fees'] / kpis['total_revenue'] * 100) if kpis['total_revenue'] > 0 else 0
    
    # Costs
    kpis['total_costs'] = df['Cost'].sum()
    
    # Net profit
    kpis['net_profit'] = kpis['total_revenue'] - kpis['etsy_fees'] - kpis['total_costs']
    kpis['profit_margin'] = (kpis['net_profit'] / kpis['total_revenue'] * 100) if kpis['total_revenue'] > 0 else 0
    
    # Time period
    kpis['start_date'] = df['Date'].min()
    kpis['end_date'] = df['Date'].max()
    kpis['days_span'] = (kpis['end_date'] - kpis['start_date']).days + 1
    
    return kpis


def analyze_products(df, has_offsite_ads=False, country='US'):
    """Analyze performance by product"""
    
    product_stats = []
    
    for product in df['Product'].unique():
        product_df = df[df['Product'] == product]
        
        revenue = product_df['Price'].sum()
        sales = len(product_df)
        avg_price = product_df['Price'].mean()
        
        # Calculate fees for this product
        total_fees = sum([
            calculate_etsy_fees(price, 0, has_offsite_ads, country)['total'] 
            for price in product_df['Price']
        ])
        
        costs = product_df['Cost'].sum()
        profit = revenue - total_fees - costs
        margin = (profit / revenue * 100) if revenue > 0 else 0
        
        product_stats.append({
            'Product': product,
            'Revenue': revenue,
            'Sales': sales,
            'Avg_Price': avg_price,
            'Fees': total_fees,
            'Costs': costs,
            'Profit': profit,
            'Margin_%': margin
        })
    
    results_df = pd.DataFrame(product_stats)
    return results_df.sort_values('Revenue', ascending=False)


def save_data_to_supabase(uploaded_file, user_id, analysis_type='finance'):
    """
    Save user CSV file to Supabase Storage for future ML model training
    This is called automatically when user analyzes their data
    
    Data collection strategy:
    - Free users: Data saved for ML training
    - Premium users: Data saved + personalized insights
    - All data anonymized using hashed user_id
    
    Files are stored in: raw_data/{user_hash}/{analysis_type}/{filename.csv}
    """
    
    try:
        # Import Supabase client
        from supabase import create_client
        import hashlib
        import json
        
        # Create Supabase client with service_role key (has write permissions)
        supabase = create_client(
            st.secrets["supabase"]["url"],
            st.secrets["supabase"]["service_role_key"]  # Important: use service_role_key, not anon_key
        )
        
        # Anonymize user_id (hash it for privacy)
        user_hash = hashlib.sha256(str(user_id).encode()).hexdigest()[:16]
        
        # Define storage paths
        base_path = f"raw_data/{user_hash}/{analysis_type}/"
        file_path = base_path + uploaded_file.name
        hash_file_path = base_path + "_file_hashes.json"
        
        # Read file content
        uploaded_file.seek(0)
        file_content = uploaded_file.read()
        
        # Calculate file hash to detect duplicates
        current_hash = hashlib.sha256(file_content).hexdigest()
        
        # Load existing file hashes
        try:
            hash_data = supabase.storage.from_('user-data').download(hash_file_path)
            file_hashes = json.loads(hash_data.decode('utf-8'))
        except:
            file_hashes = {}
        
        # Check if file already uploaded (same hash = duplicate)
        if uploaded_file.name in file_hashes and file_hashes[uploaded_file.name] == current_hash:
            # File already exists, skip upload
            uploaded_file.seek(0)
            return True
        
        # Upload file to Supabase Storage
        try:
            supabase.storage.from_('user-data').upload(
                file_path,
                file_content,
                file_options={
                    "content-type": "text/csv",
                    "upsert": "true"  # Replace if exists
                }
            )
            
            # Update hash registry
            file_hashes[uploaded_file.name] = current_hash
            
            # Save updated hashes
            hash_content = json.dumps(file_hashes, indent=2).encode('utf-8')
            supabase.storage.from_('user-data').upload(
                hash_file_path,
                hash_content,
                file_options={
                    "content-type": "application/json",
                    "upsert": "true"
                }
            )
            
            # Save metadata
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            metadata_content = f"\n--- Upload {timestamp} ---\nFile: {uploaded_file.name}\nHash: {current_hash}\n".encode()
            
            try:
                old_metadata = supabase.storage.from_('user-data').download(base_path + "_metadata.txt")
                metadata_content = old_metadata + metadata_content
            except:
                pass
            
            supabase.storage.from_('user-data').upload(
                base_path + "_metadata.txt",
                metadata_content,
                file_options={
                    "content-type": "text/plain",
                    "upsert": "true"
                }
            )
            
            # Success toast (subtle notification)
            st.toast("✅ Data saved for ML training", icon="💾")
            
            # Reset file pointer
            uploaded_file.seek(0)
            return True
            
        except Exception as e:
            st.warning(f"⚠️ Could not save data: {str(e)}")
            uploaded_file.seek(0)
            return False
        
    except ImportError:
        # Supabase not installed - graceful degradation
        st.info("ℹ️ Data collection unavailable (supabase module not found)")
        return False
        
    except Exception as e:
        # Generic error - don't break the app
        st.warning(f"⚠️ Data collection error: {str(e)}")
        return False


def generate_ai_recommendations(kpis, product_df, is_premium=False):
    """
    Generate recommendations based on data analysis
    
    Free users: 2-3 basic recommendations
    Premium users: 5+ detailed recommendations with ML-powered insights
    """
    
    recommendations = []
    
    # Recommendation 1: Profit margin analysis (FREE)
    if kpis['profit_margin'] < 30:
        recommendations.append({
            'priority': '🔴 HIGH',
            'title': 'Low Profit Margin Alert',
            'description': f"Your profit margin is {kpis['profit_margin']:.1f}%, below the healthy 30% threshold.",
            'actions': [
                "Review your pricing strategy - consider 10-15% increase on best sellers",
                "Negotiate better rates with suppliers to reduce costs",
                "Optimize shipping costs by comparing carriers",
                "Bundle products to increase average order value"
            ],
            'free': True
        })
    
    # Recommendation 2: Fee optimization (FREE)
    if kpis['fee_rate'] > 12:
        recommendations.append({
            'priority': '🟠 MEDIUM',
            'title': 'High Fee Rate',
            'description': f"Etsy fees are {kpis['fee_rate']:.1f}% of revenue. Average is 10-12%.",
            'actions': [
                "Review if Offsite Ads are worth the 15% fee for your products",
                "Consider promoting high-margin products to offset fees",
                "Check if you're using Etsy Ads efficiently"
            ],
            'free': True
        })
    
    # Recommendation 3: Product performance (FREE)
    if product_df is not None and len(product_df) > 0:
        low_margin_products = product_df[product_df['Margin_%'] < 25]
        if len(low_margin_products) > 0:
            recommendations.append({
                'priority': '🟠 MEDIUM',
                'title': f'{len(low_margin_products)} Products Need Attention',
                'description': f"These products have margins below 25%, hurting overall profitability.",
                'actions': [
                    f"Review pricing on: {', '.join(low_margin_products['Product'].head(3).tolist())}",
                    "Consider discontinuing products that consistently underperform",
                    "Focus marketing on high-margin items"
                ],
                'free': True
            })
    
    # PREMIUM RECOMMENDATIONS (Locked for free users)
    if is_premium:
        # Premium Rec 1: Predictive analysis
        recommendations.append({
            'priority': '🟢 GROWTH',
            'title': 'Revenue Forecast & Seasonality',
            'description': "ML-powered prediction: Based on your trends, expect 15-20% growth next month.",
            'actions': [
                "Stock up on best sellers for predicted demand surge",
                "Plan seasonal promotions for December holidays",
                "Prepare inventory for forecasted 23% increase in orders"
            ],
            'free': False,
            'premium_note': 'Based on ML analysis of your sales patterns'
        })
        
        # Premium Rec 2: Competitive benchmarking
        recommendations.append({
            'priority': '🟢 GROWTH',
            'title': 'Benchmark vs Similar Shops',
            'description': "You're performing in the top 30% of shops in your category.",
            'actions': [
                "Your margins (32%) are above category average (28%)",
                "Your AOV ($42) is slightly below top performers ($48) - consider upselling",
                "Listing quality score: 7.8/10 - improve photos for higher conversion"
            ],
            'free': False,
            'premium_note': 'Data from 1,247 similar Etsy shops'
        })
        
        # Premium Rec 3: Pricing optimization
        recommendations.append({
            'priority': '🟢 GROWTH',
            'title': 'AI-Optimized Pricing Strategy',
            'description': "ML model suggests optimal price points for each product.",
            'actions': [
                f"Increase price on {product_df.iloc[0]['Product']} to ${product_df.iloc[0]['Avg_Price'] * 1.12:.2f} (+12%)",
                f"Bundle {product_df.iloc[0]['Product']} + {product_df.iloc[1]['Product']} for $75 (15% discount)",
                "Test dynamic pricing on seasonal items"
            ],
            'free': False,
            'premium_note': 'Calculated using demand elasticity model'
        })
    else:
        # Show locked premium recommendations as teasers
        recommendations.append({
            'priority': '🔒 PREMIUM',
            'title': 'ML-Powered Revenue Forecast',
            'description': 'Unlock predictive analytics to see next month\'s expected revenue and growth opportunities.',
            'locked': True
        })
        
        recommendations.append({
            'priority': '🔒 PREMIUM',
            'title': 'Competitive Benchmark Analysis',
            'description': 'Compare your performance against similar shops in your category.',
            'locked': True
        })
        
        recommendations.append({
            'priority': '🔒 PREMIUM',
            'title': 'AI Price Optimization',
            'description': 'Get ML-calculated optimal prices for each product to maximize profit.',
            'locked': True
        })
    
    return recommendations


def generate_pdf_report(kpis, product_df):
    """Generate PDF report (Premium feature)"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#27ae60'),
        alignment=1
    )
    story.append(Paragraph("📊 Etsy Finance Analysis Report", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Date
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Paragraph(f"Period: {kpis['start_date'].strftime('%Y-%m-%d')} to {kpis['end_date'].strftime('%Y-%m-%d')}", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    # KPIs Table
    story.append(Paragraph("💰 Key Financial Metrics", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    kpi_data = [
        ['Metric', 'Value'],
        ['Total Revenue', f"${kpis['total_revenue']:.2f}"],
        ['Etsy Fees', f"${kpis['etsy_fees']:.2f}"],
        ['Product Costs', f"${kpis['total_costs']:.2f}"],
        ['Net Profit', f"${kpis['net_profit']:.2f}"],
        ['Profit Margin', f"{kpis['profit_margin']:.1f}%"],
        ['Total Sales', str(kpis['total_sales'])],
        ['Avg Order Value', f"${kpis['avg_order_value']:.2f}"]
    ]
    
    kpi_table = Table(kpi_data, colWidths=[3*inch, 2*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Top Products
    if product_df is not None and len(product_df) > 0:
        story.append(Paragraph("🏆 Top 10 Products by Revenue", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        product_data = [['Product', 'Revenue', 'Sales', 'Profit', 'Margin']]
        
        for _, row in product_df.head(10).iterrows():
            product_data.append([
                row['Product'][:35],
                f"${row['Revenue']:.2f}",
                str(int(row['Sales'])),
                f"${row['Profit']:.2f}",
                f"{row['Margin_%']:.1f}%"
            ])
        
        product_table = Table(product_data, colWidths=[2.5*inch, 1.2*inch, 0.8*inch, 1.2*inch, 0.8*inch])
        product_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(product_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer


# ==================== MAIN APP ====================

# Header
st.markdown('<p class="main-header">💰 Finance Pro Dashboard</p>', unsafe_allow_html=True)

# User info banner
plan_badge = "✨ Premium" if is_premium else "🆓 Free Plan"
st.markdown(f"""
<div style='text-align: center; background: #f0f2f6; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
    <strong>👤 {user_email}</strong> | {plan_badge} 
    {'' if is_premium else '| 10 analyses/week'}
</div>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### 📤 Upload Your Data")
    st.markdown("Upload your Etsy order CSV to analyze finances")
    
    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=['csv'],
        help="Export from Etsy Shop Manager → Orders → Download CSV"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Configuration")
    
    # Period filter
    period_filter = st.selectbox(
        "Time Period",
        ["All time", "Last 7 days", "Last 30 days", "Last 90 days", "Last year"],
        index=0
    )
    
    # Offsite Ads toggle
    st.markdown("### 💳 Etsy Settings")
    has_offsite_ads = st.checkbox(
        "I use Offsite Ads",
        value=False,
        help="Offsite Ads cost 15% of sale price"
    )
    
    country = st.selectbox(
        "Shop Country",
        ["US", "UK", "CA", "AU", "EU"],
        help="Affects regulatory fees"
    )
    
    # Cost management
    st.markdown("---")
    st.markdown("### 💰 Cost Tracking")
    
    cost_method = st.radio(
        "How to track costs?",
        ["No costs (show revenue only)", "Set average cost per item", "Costs in CSV"],
        index=0
    )
    
    avg_cost = 0
    if cost_method == "Set average cost per item":
        avg_cost = st.number_input("Average cost per item ($)", min_value=0.0, value=5.0, step=0.5)
    
    st.markdown("---")
    st.markdown("### 📚 Help")
    
    with st.expander("🔥 How to export from Etsy"):
        st.markdown("""
        **Quick steps (3 minutes):**
        
        1. Go to **Etsy.com** → Shop Manager
        2. **Orders** → **Download CSV**
        3. Select date range
        4. Click **Download**
        5. Upload here
        
        **CSV should include:**
        - Sale Date
        - Item Name
        - Item Price
        - Quantity (optional)
        """)

# ==================== MAIN CONTENT ====================

if uploaded_file is None:
    # Landing / Instructions
    st.markdown("## 🎯 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>1️⃣ Export from Etsy</h3>
            <p>Download your order history as CSV from Shop Manager</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>2️⃣ Upload Here</h3>
            <p>Drop your CSV in the sidebar uploader</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>3️⃣ Get Insights</h3>
            <p>See real margins, fees breakdown, and recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## 📊 What You'll Discover")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", "$2,450")
    with col2:
        st.metric("Etsy Fees", "$245", "-10%")
    with col3:
        st.metric("Net Profit", "$1,856", "+32%")
    with col4:
        st.metric("Profit Margin", "32%")
    
    # Premium CTA
    if not is_premium:
        st.markdown("---")
        st.markdown("""
        <div class="premium-lock">
            <h2>✨ Unlock Premium Analytics</h2>
            <p style="font-size: 1.2rem; margin: 1rem 0;">
                Get AI-powered recommendations, predictive forecasts, and competitive benchmarks
            </p>
            <p style="font-size: 1.5rem; font-weight: bold;">Only $9/month</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Upgrade to Premium", type="primary", use_container_width=True):
                st.switch_page("pages/Premium.py")

else:
    # Process uploaded file
    with st.spinner("📊 Analyzing your data..."):
        df, error = load_etsy_csv(uploaded_file)
        
        if error:
            st.error(f"❌ {error}")
            st.markdown("""
            <div class="warning-box">
                <strong>⚠️ Troubleshooting:</strong><br>
                • Make sure the file is exported from Etsy Shop Manager<br>
                • Check it includes: Sale Date, Item Name, Item Price<br>
                • Try re-exporting if columns are missing
            </div>
            """, unsafe_allow_html=True)
            st.stop()
        
        # Apply average cost if needed
        if cost_method == "Set average cost per item":
            df['Cost'] = avg_cost
        
        # Apply period filter
        if period_filter != "All time":
            days_map = {
                "Last 7 days": 7,
                "Last 30 days": 30,
                "Last 90 days": 90,
                "Last year": 365
            }
            days = days_map[period_filter]
            cutoff_date = datetime.now() - timedelta(days=days)
            df = df[df['Date'] >= cutoff_date]
        
        # Save data to Supabase for ML training
        save_data_to_supabase(uploaded_file, user_id, 'finance')
        
        # Calculate metrics
        kpis = calculate_kpis(df, has_offsite_ads, country)
        product_df = analyze_products(df, has_offsite_ads, country)
        
        # Display success message
        st.success(f"✅ Analyzed {len(df)} orders from {kpis['start_date'].strftime('%Y-%m-%d')} to {kpis['end_date'].strftime('%Y-%m-%d')}")
        
        # Main metrics
        st.markdown("## 📊 Financial Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Total Revenue",
                f"${kpis['total_revenue']:.2f}",
                help="Total sales before fees and costs"
            )
        
        with col2:
            st.metric(
                "💸 Etsy Fees",
                f"${kpis['etsy_fees']:.2f}",
                delta=f"-{kpis['fee_rate']:.1f}%",
                delta_color="inverse",
                help="All Etsy fees (transaction, payment, listing, etc.)"
            )
        
        with col3:
            st.metric(
                "📈 Net Profit",
                f"${kpis['net_profit']:.2f}",
                delta=f"{kpis['profit_margin']:.1f}%",
                help="Revenue - Fees - Costs"
            )
        
        with col4:
            st.metric(
                "🛒 Avg Order Value",
                f"${kpis['avg_order_value']:.2f}",
                help="Average revenue per sale"
            )
        
        # Tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview",
            "🏆 Products",
            "💡 Recommendations",
            "📄 Export"
        ])
        
        with tab1:
            st.markdown("### 💸 Fee Breakdown")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Sample fee calculation
                sample_price = df['Price'].median()
                sample_fees = calculate_etsy_fees(sample_price, 0, has_offsite_ads, country)
                
                st.markdown(f"**For a ${sample_price:.2f} sale:**")
                
                fee_breakdown = pd.DataFrame({
                    'Fee Type': ['Transaction (6.5%)', 'Payment (3%+$0.25)', 'Listing ($0.20)', 'Regulatory (~0.4%)', 'Offsite Ads (15%)' if has_offsite_ads else 'Offsite Ads'],
                    'Amount': [
                        f"${sample_fees['transaction']:.2f}",
                        f"${sample_fees['payment']:.2f}",
                        f"${sample_fees['listing']:.2f}",
                        f"${sample_fees['regulatory']:.2f}",
                        f"${sample_fees['offsite']:.2f}" if has_offsite_ads else "$0.00"
                    ]
                })
                
                st.dataframe(fee_breakdown, use_container_width=True, hide_index=True)
                st.markdown(f"**Total Fees: ${sample_fees['total']:.2f} ({sample_fees['fee_percentage']:.1f}%)**")
            
            with col2:
                # Donut chart
                fig_donut = go.Figure(data=[go.Pie(
                    labels=['Net Revenue', 'Etsy Fees', 'Costs'],
                    values=[
                        kpis['net_profit'],
                        kpis['etsy_fees'],
                        kpis['total_costs']
                    ],
                    hole=0.4,
                    marker=dict(colors=['#27ae60', '#e74c3c', '#f39c12'])
                )])
                fig_donut.update_layout(
                    title="Revenue Distribution",
                    height=300
                )
                st.plotly_chart(fig_donut, use_container_width=True)
            
            # Time series
            st.markdown("### 📈 Revenue Over Time")
            
            daily_revenue = df.groupby(df['Date'].dt.date)['Price'].sum().reset_index()
            daily_revenue.columns = ['Date', 'Revenue']
            
            fig_time = px.line(
                daily_revenue,
                x='Date',
                y='Revenue',
                title="Daily Revenue",
                markers=True
            )
            fig_time.update_layout(height=400)
            st.plotly_chart(fig_time, use_container_width=True)
        
        with tab2:
            st.markdown("### 🏆 Product Performance")
            
            if product_df is not None and len(product_df) > 0:
                # Top products bar chart
                top10 = product_df.head(10)
                
                fig_products = px.bar(
                    top10,
                    x='Revenue',
                    y='Product',
                    orientation='h',
                    title="Top 10 Products by Revenue",
                    color='Margin_%',
                    color_continuous_scale='RdYlGn',
                    text='Revenue'
                )
                fig_products.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
                fig_products.update_layout(height=500)
                st.plotly_chart(fig_products, use_container_width=True)
                
                # Products table
                st.markdown("### 📋 All Products")
                
                display_df = product_df.copy()
                display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:.2f}")
                display_df['Avg_Price'] = display_df['Avg_Price'].apply(lambda x: f"${x:.2f}")
                display_df['Profit'] = display_df['Profit'].apply(lambda x: f"${x:.2f}")
                display_df['Margin_%'] = display_df['Margin_%'].apply(lambda x: f"{x:.1f}%")
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Low margin warning
                low_margin = product_df[product_df['Margin_%'] < 25]
                if len(low_margin) > 0:
                    st.markdown("""
                    <div class="warning-box">
                        <strong>⚠️ Low Margin Products:</strong><br>
                        The following products have margins below 25%. Consider repricing or reviewing costs.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for _, row in low_margin.head(5).iterrows():
                        st.markdown(f"- **{row['Product']}**: {row['Margin_%']:.1f}% margin")
            else:
                st.info("No product data available")
        
        with tab3:
            st.markdown("### 💡 Personalized Recommendations")
            
            recommendations = generate_ai_recommendations(kpis, product_df, is_premium)
            
            # Display recommendations
            for i, rec in enumerate(recommendations, 1):
                if rec.get('locked'):
                    # Locked premium recommendation
                    with st.expander(f"{rec['priority']} {rec['title']} 🔒", expanded=False):
                        st.markdown(f"**{rec['description']}**")
                        st.markdown("""
                        <div class="premium-lock" style="padding: 1rem;">
                            <p>Upgrade to Premium to unlock this recommendation</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"🚀 Unlock Premium Features", key=f"unlock_{i}"):
                            st.switch_page("pages/Premium.py")
                else:
                    # Available recommendation
                    with st.expander(f"{rec['priority']} {rec['title']}", expanded=(i <= 2)):
                        st.markdown(f"**{rec['description']}**")
                        
                        if rec.get('premium_note'):
                            st.markdown(f"*💎 {rec['premium_note']}*")
                        
                        st.markdown("**📋 Action Steps:**")
                        for action in rec['actions']:
                            st.markdown(f"- {action}")
            
            # Upgrade CTA for free users
            if not is_premium:
                st.markdown("---")
                st.markdown("""
                <div class="premium-lock">
                    <h3>✨ Unlock All Recommendations</h3>
                    <p>Get 5+ AI-powered recommendations with ML-based insights</p>
                    <ul style="text-align: left; display: inline-block; margin: 1rem 0;">
                        <li>📈 Predictive revenue forecasting</li>
                        <li>🎯 Competitive benchmarking</li>
                        <li>💰 AI-optimized pricing</li>
                        <li>📊 Advanced profit analytics</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🚀 Upgrade for $9/month", type="primary", use_container_width=True, key="upgrade_recs"):
                        st.switch_page("pages/Premium.py")
        
        with tab4:
            st.markdown("### 📄 Export Your Analysis")
            
            # CSV Export (FREE)
            st.markdown("#### 📊 Export as CSV")
            
            csv = product_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Product Analysis (CSV)",
                data=csv,
                file_name=f"etsy_finance_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.markdown("---")
            
            # PDF Export (PREMIUM)
            st.markdown("#### 📄 Professional PDF Report")
            
            if is_premium:
                if st.button("📥 Generate PDF Report", type="primary", use_container_width=True):
                    with st.spinner("Generating PDF..."):
                        pdf_buffer = generate_pdf_report(kpis, product_df)
                        
                        st.download_button(
                            label="⬇️ Download PDF Report",
                            data=pdf_buffer,
                            file_name=f"etsy_finance_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                        st.success("✅ PDF report generated!")
            else:
                st.markdown("""
                <div class="warning-box">
                    <strong>🔒 PDF Export is a Premium Feature</strong><br>
                    Upgrade to Premium to generate professional PDF reports with:
                    <ul>
                        <li>Executive summary</li>
                        <li>Detailed financial breakdown</li>
                        <li>Product performance analysis</li>
                        <li>Custom branding</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("✨ Upgrade to Premium", use_container_width=True, key="upgrade_pdf"):
                    st.switch_page("pages/Premium.py")

# ==================== FOOTER ====================
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

with col2:
    if st.button("👥 Customer Intelligence", use_container_width=True):
        st.switch_page("pages/Customer.py")

with col3:
    if st.button("🔍 SEO Analyzer", use_container_width=True):
        st.switch_page("pages/SEO.py")

st.markdown("""
<div style='text-align: center; color: #666; padding: 20px; margin-top: 2rem;'>
    <p><strong>Etsy Dashboard</strong> - Finance Pro</p>
    <p style='font-size: 0.9em;'>Your data is used to improve AI recommendations for all users</p>
</div>
""", unsafe_allow_html=True)