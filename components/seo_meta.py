"""
SEO Meta Tags and Schema Markup Components
Reusable functions for SEO optimization across all landing pages
"""

import streamlit as st
from typing import Dict, List, Optional
import json


def render_seo_meta(
    title: str,
    description: str,
    keywords: str,
    og_title: Optional[str] = None,
    og_description: Optional[str] = None,
    og_image: Optional[str] = None,
    canonical_url: Optional[str] = None
):
    """
    Render SEO meta tags for a page
    
    Args:
        title: Page title (50-60 chars optimal)
        description: Meta description (150-160 chars optimal)
        keywords: Comma-separated keywords
        og_title: OpenGraph title (defaults to title)
        og_description: OpenGraph description (defaults to description)
        og_image: URL to OG image
        canonical_url: Canonical URL for the page
    """
    
    og_title = og_title or title
    og_description = og_description or description
    
    meta_html = f"""
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    
    <!-- OpenGraph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_description}">
    """
    
    if og_image:
        meta_html += f'<meta property="og:image" content="{og_image}">\n'
    
    if canonical_url:
        meta_html += f'<link rel="canonical" href="{canonical_url}">\n'
    
    meta_html += """
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{og_title}">
    <meta name="twitter:description" content="{og_description}">
    """
    
    if og_image:
        meta_html += f'<meta name="twitter:image" content="{og_image}">\n'
    
    st.markdown(meta_html, unsafe_allow_html=True)


def render_schema_product(
    name: str,
    description: str,
    price: str = "0",
    currency: str = "USD",
    rating_value: Optional[float] = None,
    rating_count: Optional[int] = None,
    offers_url: Optional[str] = None
):
    """
    Render Product schema markup (schema.org)
    
    Args:
        name: Product name
        description: Product description
        price: Price (use "0" for free products)
        currency: Currency code (USD, EUR, etc.)
        rating_value: Average rating (1-5)
        rating_count: Number of ratings
        offers_url: URL where product can be purchased
    """
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "description": description,
        "offers": {
            "@type": "Offer",
            "price": price,
            "priceCurrency": currency
        }
    }
    
    if offers_url:
        schema["offers"]["url"] = offers_url
    
    if rating_value and rating_count:
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(rating_value),
            "ratingCount": str(rating_count)
        }
    
    st.markdown(
        f'<script type="application/ld+json">{json.dumps(schema)}</script>',
        unsafe_allow_html=True
    )


def render_schema_software(
    name: str,
    description: str,
    application_category: str = "BusinessApplication",
    operating_system: str = "Web Browser",
    price: str = "0",
    currency: str = "USD",
    rating_value: Optional[float] = None,
    rating_count: Optional[int] = None
):
    """
    Render SoftwareApplication schema markup
    
    Args:
        name: Software name
        description: Software description
        application_category: Category (e.g., "BusinessApplication", "FinanceApplication")
        operating_system: OS requirements
        price: Price
        currency: Currency code
        rating_value: Average rating
        rating_count: Number of ratings
    """
    
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "applicationCategory": application_category,
        "operatingSystem": operating_system,
        "description": description,
        "offers": {
            "@type": "Offer",
            "price": price,
            "priceCurrency": currency
        }
    }
    
    if rating_value and rating_count:
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(rating_value),
            "ratingCount": str(rating_count)
        }
    
    st.markdown(
        f'<script type="application/ld+json">{json.dumps(schema)}</script>',
        unsafe_allow_html=True
    )


def render_schema_faq(faqs: List[Dict[str, str]]):
    """
    Render FAQ schema markup
    
    Args:
        faqs: List of dicts with 'question' and 'answer' keys
        
    Example:
        faqs = [
            {
                "question": "Is it free?",
                "answer": "Yes, completely free with no credit card required."
            },
            {
                "question": "How do I start?",
                "answer": "Simply upload your CSV files and click analyze."
            }
        ]
    """
    
    main_entity = []
    for faq in faqs:
        main_entity.append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity
    }
    
    st.markdown(
        f'<script type="application/ld+json">{json.dumps(schema)}</script>',
        unsafe_allow_html=True
    )


def render_schema_howto(
    name: str,
    description: str,
    steps: List[Dict[str, str]]
):
    """
    Render HowTo schema markup
    
    Args:
        name: Name of the tutorial/guide
        description: Description
        steps: List of dicts with 'name' and 'text' keys
        
    Example:
        steps = [
            {"name": "Upload CSV", "text": "Download your Etsy data and upload it"},
            {"name": "Analyze", "text": "Click the analyze button"},
            {"name": "Review", "text": "Review your insights"}
        ]
    """
    
    step_list = []
    for i, step in enumerate(steps, 1):
        step_list.append({
            "@type": "HowToStep",
            "position": str(i),
            "name": step["name"],
            "text": step["text"]
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": description,
        "step": step_list
    }
    
    st.markdown(
        f'<script type="application/ld+json">{json.dumps(schema)}</script>',
        unsafe_allow_html=True
    )


def render_breadcrumbs(items: List[Dict[str, str]]):
    """
    Render BreadcrumbList schema markup
    
    Args:
        items: List of dicts with 'name' and 'url' keys
        
    Example:
        items = [
            {"name": "Home", "url": "https://etsydashboard.com"},
            {"name": "Calculator", "url": "https://etsydashboard.com/calculate-fees"}
        ]
    """
    
    item_list = []
    for i, item in enumerate(items, 1):
        item_list.append({
            "@type": "ListItem",
            "position": str(i),
            "name": item["name"],
            "item": item["url"]
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": item_list
    }
    
    st.markdown(
        f'<script type="application/ld+json">{json.dumps(schema)}</script>',
        unsafe_allow_html=True
    )


def hide_streamlit_elements():
    """
    Hide Streamlit default UI elements for cleaner landing pages
    """
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


def inject_google_analytics(tracking_id: str):
    """
    Inject Google Analytics tracking code
    
    Args:
        tracking_id: Google Analytics tracking ID (e.g., "G-XXXXXXXXXX")
    """
    st.markdown(f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={tracking_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{tracking_id}');
        </script>
    """, unsafe_allow_html=True)


def inject_meta_pixel(pixel_id: str):
    """
    Inject Meta (Facebook) Pixel tracking code
    
    Args:
        pixel_id: Meta Pixel ID
    """
    st.markdown(f"""
        <script>
          !function(f,b,e,v,n,t,s)
          {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
          n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
          if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
          n.queue=[];t=b.createElement(e);t.async=!0;
          t.src=v;s=b.getElementsByTagName(e)[0];
          s.parentNode.insertBefore(t,s)}}(window, document,'script',
          'https://connect.facebook.net/en_US/fbevents.js');
          fbq('init', '{pixel_id}');
          fbq('track', 'PageView');
        </script>
        <noscript><img height="1" width="1" style="display:none"
          src="https://www.facebook.com/tr?id={pixel_id}&ev=PageView&noscript=1"
        /></noscript>
    """, unsafe_allow_html=True)


# ==================== SEO PRESETS ====================

def render_etsy_dashboard_seo():
    """Preset SEO for main Etsy Dashboard landing page"""
    render_seo_meta(
        title="Free Etsy Dashboard - Track Your Shop Analytics in Real-Time",
        description="Free Etsy analytics dashboard. Track profit margins, customer behavior, and SEO performance. Upload your CSV and get instant insights.",
        keywords="etsy dashboard, etsy analytics, etsy profit calculator, etsy shop analytics, etsy margins, etsy seo tool",
        og_title="Free Etsy Dashboard - Track Your Shop Analytics",
        og_description="Finance, SEO & Customer Intelligence - All Your Etsy Data in One Beautiful Dashboard"
    )
    
    render_schema_software(
        name="Etsy Dashboard",
        description="Free Etsy analytics dashboard with Finance, Customer Intelligence, and SEO tools",
        application_category="BusinessApplication",
        price="0",
        currency="USD",
        rating_value=4.8,
        rating_count=127
    )


def render_calculate_fees_seo():
    """Preset SEO for Calculate Etsy Fees landing page"""
    render_seo_meta(
        title="Free Etsy Fee Calculator - Calculate Your Real Profit After All Fees",
        description="Calculate your true Etsy profit after transaction fees, payment processing, offsite ads, and shipping. Free calculator with instant results.",
        keywords="calculate etsy fees, etsy calculator, etsy fee calculator, etsy profit calculator, etsy margin calculator",
        og_title="Calculate Etsy Fees - Free Tool",
        og_description="Find out your real profit after all Etsy fees"
    )
    
    render_schema_software(
        name="Etsy Fee Calculator",
        description="Free tool to calculate Etsy fees and real profit margins",
        application_category="FinanceApplication",
        price="0",
        currency="USD"
    )


def render_analytics_tool_seo():
    """Preset SEO for Etsy Analytics Tool comparison page"""
    render_seo_meta(
        title="Etsy Analytics Tool - Track Profit, Customers & SEO | Free Tool",
        description="Complete Etsy analytics tool for serious sellers. Track real margins, analyze customer behavior, optimize SEO. Free tier available.",
        keywords="etsy analytics tool, etsy analytics software, etsy shop analytics, etsy tracking tool",
        og_title="Complete Etsy Analytics Tool",
        og_description="Finance, Customer Intelligence & SEO in one dashboard"
    )
    
    render_schema_software(
        name="Etsy Analytics Tool",
        description="Complete analytics platform for Etsy sellers with finance, customer, and SEO insights",
        application_category="BusinessApplication",
        price="0",
        currency="USD",
        rating_value=4.8,
        rating_count=127
    )