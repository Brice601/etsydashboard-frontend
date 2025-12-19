"""
UI Elements
Reusable UI components (headers, footers, CTAs, etc.)
"""

import streamlit as st
from typing import Optional


def render_header(
    title: str,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None
):
    """
    Render page header with title and subtitle
    
    Args:
        title: Main title
        subtitle: Subtitle text (optional)
        icon: Emoji icon (optional)
    """
    if icon:
        st.markdown(f"# {icon} {title}")
    else:
        st.markdown(f"# {title}")
    
    if subtitle:
        st.markdown(f"*{subtitle}*")
    
    st.markdown("---")


def render_cta(
    text: str,
    url: str,
    style: str = "primary",
    icon: str = "→"
):
    """
    Render CTA button
    
    Args:
        text: Button text
        url: Target URL
        style: Button style (primary, secondary, success)
        icon: Icon to show (optional)
    """
    colors = {
        "primary": "#667eea",
        "secondary": "#95a5a6",
        "success": "#27ae60",
        "warning": "#F56400",
        "danger": "#e74c3c"
    }
    
    bg_color = colors.get(style, colors["primary"])
    
    st.markdown(f"""
        <a href="{url}" style="
            display: inline-block;
            background: {bg_color};
            color: white;
            padding: 0.8rem 2rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.1rem;
            transition: all 0.3s ease;
        ">
            {text} {icon}
        </a>
    """, unsafe_allow_html=True)


def render_footer(
    company_name: str = "Etsy Dashboard",
    links: Optional[dict] = None
):
    """
    Render footer with links
    
    Args:
        company_name: Company name
        links: Dict of link_text: link_url
    """
    if links is None:
        links = {
            "Privacy Policy": "/privacy",
            "Terms of Service": "/terms",
            "Contact": "mailto:support@etsydashboard.com"
        }
    
    links_html = " | ".join([
        f'<a href="{url}" style="color: #F56400; text-decoration: none;">{text}</a>'
        for text, url in links.items()
    ])
    
    st.markdown(f"""
        <div style="
            background: #262730;
            color: white;
            padding: 2rem;
            margin: 3rem -1rem -1rem -1rem;
            text-align: center;
            border-radius: 20px 20px 0 0;
        ">
            <p style="margin-bottom: 1rem;">© 2024 {company_name}. All rights reserved.</p>
            <p style="font-size: 0.9rem; opacity: 0.8;">{links_html}</p>
        </div>
    """, unsafe_allow_html=True)


def render_feature_card(
    icon: str,
    title: str,
    description: str,
    cta_text: Optional[str] = None,
    cta_url: Optional[str] = None
):
    """
    Render feature card
    
    Args:
        icon: Emoji icon
        title: Card title
        description: Card description
        cta_text: CTA button text (optional)
        cta_url: CTA button URL (optional)
    """
    cta_html = ""
    if cta_text and cta_url:
        cta_html = f"""
            <a href="{cta_url}" style="
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 0.5rem 1.5rem;
                border-radius: 50px;
                text-decoration: none;
                font-weight: bold;
                margin-top: 1rem;
            ">
                {cta_text}
            </a>
        """
    
    st.markdown(f"""
        <div style="
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
            height: 100%;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">{title}</h3>
            <p style="color: #7f8c8d; line-height: 1.6;">{description}</p>
            {cta_html}
        </div>
    """, unsafe_allow_html=True)


def render_alert(
    message: str,
    alert_type: str = "info",
    dismissible: bool = False
):
    """
    Render alert box
    
    Args:
        message: Alert message
        alert_type: Type (success, info, warning, danger)
        dismissible: Whether alert can be dismissed
    """
    colors = {
        "success": {"bg": "#e8f5e9", "border": "#27ae60", "icon": "✅"},
        "info": {"bg": "#e3f2fd", "border": "#2196F3", "icon": "ℹ️"},
        "warning": {"bg": "#fff3e0", "border": "#F56400", "icon": "⚠️"},
        "danger": {"bg": "#ffebee", "border": "#e74c3c", "icon": "❌"}
    }
    
    config = colors.get(alert_type, colors["info"])
    
    st.markdown(f"""
        <div style="
            background: {config['bg']};
            border-left: 5px solid {config['border']};
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        ">
            <strong>{config['icon']} {message}</strong>
        </div>
    """, unsafe_allow_html=True)


def render_stats_grid(stats: list):
    """
    Render grid of statistics
    
    Args:
        stats: List of dicts with 'label', 'value', 'icon' keys
    """
    cols = st.columns(len(stats))
    
    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
                <div style="
                    background: white;
                    border-radius: 10px;
                    padding: 1.5rem;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                    text-align: center;
                ">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">
                        {stat.get('icon', '📊')}
                    </div>
                    <div style="font-size: 0.9rem; color: #7f8c8d; margin-bottom: 0.5rem;">
                        {stat['label']}
                    </div>
                    <div style="font-size: 2rem; font-weight: bold; color: #2c3e50;">
                        {stat['value']}
                    </div>
                </div>
            """, unsafe_allow_html=True)


def render_progress_bar(
    current: float,
    target: float,
    label: str = "Progress",
    show_percentage: bool = True
):
    """
    Render progress bar
    
    Args:
        current: Current value
        target: Target value
        label: Label text
        show_percentage: Show percentage text
    """
    percentage = (current / target * 100) if target > 0 else 0
    percentage = min(percentage, 100)
    
    color = "#27ae60" if percentage >= 100 else "#667eea"
    
    percentage_text = f"{percentage:.0f}%" if show_percentage else ""
    
    st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: bold;">{label}</span>
                <span>{percentage_text}</span>
            </div>
            <div style="
                background: #f0f0f0;
                border-radius: 10px;
                height: 20px;
                overflow: hidden;
            ">
                <div style="
                    background: {color};
                    width: {percentage}%;
                    height: 100%;
                    border-radius: 10px;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_badge(
    text: str,
    badge_type: str = "default"
):
    """
    Render badge
    
    Args:
        text: Badge text
        badge_type: Type (default, success, warning, danger, info)
    """
    colors = {
        "default": {"bg": "#95a5a6", "color": "white"},
        "success": {"bg": "#27ae60", "color": "white"},
        "warning": {"bg": "#F56400", "color": "white"},
        "danger": {"bg": "#e74c3c", "color": "white"},
        "info": {"bg": "#667eea", "color": "white"},
        "premium": {"bg": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "color": "white"}
    }
    
    config = colors.get(badge_type, colors["default"])
    
    st.markdown(f"""
        <span style="
            display: inline-block;
            background: {config['bg']};
            color: {config['color']};
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: bold;
            margin: 0.2rem;
        ">
            {text}
        </span>
    """, unsafe_allow_html=True)


def render_divider(
    text: Optional[str] = None,
    margin: str = "2rem 0"
):
    """
    Render divider with optional text
    
    Args:
        text: Divider text (optional)
        margin: CSS margin
    """
    if text:
        st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                text-align: center;
                margin: {margin};
            ">
                <div style="flex: 1; border-bottom: 1px solid #dee2e6;"></div>
                <span style="padding: 0 1rem; color: #7f8c8d; font-weight: bold;">
                    {text}
                </span>
                <div style="flex: 1; border-bottom: 1px solid #dee2e6;"></div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="border-bottom: 1px solid #dee2e6; margin: {margin};"></div>', 
                   unsafe_allow_html=True)


def render_tooltip(
    text: str,
    tooltip: str
):
    """
    Render text with tooltip
    
    Args:
        text: Main text
        tooltip: Tooltip text
    """
    st.markdown(f"""
        <span title="{tooltip}" style="
            border-bottom: 1px dotted #667eea;
            cursor: help;
        ">
            {text}
        </span>
    """, unsafe_allow_html=True)


def render_card(
    title: str,
    content: str,
    footer: Optional[str] = None,
    card_style: str = "default"
):
    """
    Render card component
    
    Args:
        title: Card title
        content: Card content (HTML allowed)
        footer: Card footer text (optional)
        card_style: Card style (default, primary, success, warning)
    """
    border_colors = {
        "default": "transparent",
        "primary": "#667eea",
        "success": "#27ae60",
        "warning": "#F56400",
        "danger": "#e74c3c"
    }
    
    border_color = border_colors.get(card_style, border_colors["default"])
    
    footer_html = ""
    if footer:
        footer_html = f"""
            <div style="
                border-top: 1px solid #dee2e6;
                padding-top: 1rem;
                margin-top: 1rem;
                font-size: 0.9rem;
                color: #7f8c8d;
            ">
                {footer}
            </div>
        """
    
    st.markdown(f"""
        <div style="
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            border-top: 3px solid {border_color};
            margin: 1rem 0;
        ">
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">{title}</h3>
            <div>{content}</div>
            {footer_html}
        </div>
    """, unsafe_allow_html=True)