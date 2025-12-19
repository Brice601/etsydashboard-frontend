"""
Helper functions for Etsy Dashboard
Generic utilities for formatting, validation, calculations
"""

import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Union, List, Dict, Any
import re


# ==================== FORMATTING FUNCTIONS ====================

def format_currency(amount: float, currency: str = "USD", show_symbol: bool = True) -> str:
    """
    Format a number as currency
    
    Args:
        amount: The amount to format
        currency: Currency code (USD, EUR, GBP)
        show_symbol: Whether to show currency symbol
        
    Returns:
        Formatted string (e.g., "$1,234.56" or "1,234.56")
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "CAD": "CA$",
        "AUD": "A$"
    }
    
    symbol = symbols.get(currency, "$") if show_symbol else ""
    
    # Handle negative numbers
    if amount < 0:
        return f"-{symbol}{abs(amount):,.2f}"
    
    return f"{symbol}{amount:,.2f}"


def format_percentage(value: float, decimals: int = 1, show_sign: bool = False) -> str:
    """
    Format a number as percentage
    
    Args:
        value: The value to format (0.25 = 25%)
        decimals: Number of decimal places
        show_sign: Whether to show + for positive values
        
    Returns:
        Formatted string (e.g., "25.0%" or "+25.0%")
    """
    formatted = f"{value * 100:.{decimals}f}%"
    
    if show_sign and value > 0:
        formatted = "+" + formatted
    
    return formatted


def format_number(value: float, decimals: int = 0) -> str:
    """
    Format a number with thousands separator
    
    Args:
        value: The value to format
        decimals: Number of decimal places
        
    Returns:
        Formatted string (e.g., "1,234" or "1,234.56")
    """
    if decimals == 0:
        return f"{int(value):,}"
    return f"{value:,.{decimals}f}"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


# ==================== CALCULATION FUNCTIONS ====================

def calculate_percentage(part: float, total: float) -> float:
    """
    Calculate percentage safely (handles division by zero)
    
    Args:
        part: The part value
        total: The total value
        
    Returns:
        Percentage as decimal (0.25 = 25%)
    """
    if total == 0:
        return 0.0
    return part / total


def calculate_margin(revenue: float, cost: float) -> float:
    """
    Calculate profit margin
    
    Args:
        revenue: Total revenue
        cost: Total cost
        
    Returns:
        Margin percentage as decimal
    """
    if revenue == 0:
        return 0.0
    profit = revenue - cost
    return profit / revenue


def calculate_roi(profit: float, investment: float) -> float:
    """
    Calculate ROI (Return on Investment)
    
    Args:
        profit: Net profit
        investment: Initial investment
        
    Returns:
        ROI as decimal (1.5 = 150% ROI)
    """
    if investment == 0:
        return 0.0
    return profit / investment


def calculate_etsy_fees(
    sale_price: float,
    include_offsite_ads: bool = False,
    offsite_ads_rate: float = 0.15
) -> Dict[str, float]:
    """
    Calculate all Etsy fees for a sale
    
    Args:
        sale_price: The sale price
        include_offsite_ads: Whether offsite ads are enabled
        offsite_ads_rate: Offsite ads rate (0.15 = 15%)
        
    Returns:
        Dict with breakdown of all fees
    """
    transaction_fee = sale_price * 0.065  # 6.5%
    listing_fee = 0.20
    payment_processing = (sale_price * 0.03) + 0.25  # 3% + $0.25
    offsite_ads_fee = sale_price * offsite_ads_rate if include_offsite_ads else 0.0
    
    total_fees = transaction_fee + listing_fee + payment_processing + offsite_ads_fee
    
    return {
        "transaction_fee": transaction_fee,
        "listing_fee": listing_fee,
        "payment_processing": payment_processing,
        "offsite_ads": offsite_ads_fee,
        "total_fees": total_fees,
        "net_revenue": sale_price - total_fees
    }


# ==================== VALIDATION FUNCTIONS ====================

def validate_csv(df: pd.DataFrame, required_columns: List[str]) -> tuple:
    """
    Validate that a DataFrame has required columns
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if df is None or df.empty:
        return False, "File is empty"
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    return True, None


def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing dangerous characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path separators and dangerous characters
    filename = re.sub(r'[/\\:*?"<>|]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename


# ==================== CONSTANTS ====================

ETSY_FEE_RATES = {
    "transaction_fee": 0.065,
    "payment_processing_percent": 0.03,
    "payment_processing_fixed": 0.25,
    "listing_fee": 0.20,
    "offsite_ads_standard": 0.15,
    "offsite_ads_premium": 0.12
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "CAD": "CA$",
    "AUD": "A$"
}