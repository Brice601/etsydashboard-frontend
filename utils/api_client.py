"""
API Client for Backend Communication
Handles all requests to the private backend API
"""

import requests
import streamlit as st
from typing import Dict, Any, Optional, List
import json


class APIClient:
    """Client for communicating with backend API"""
    
    def __init__(self):
        """Initialize API client with credentials from secrets"""
        try:
            self.base_url = st.secrets["api"]["backend_url"]
            self.api_key = st.secrets["api"]["api_key"]
        except KeyError:
            # Fallback for development
            self.base_url = "http://localhost:8000"
            self.api_key = "dev-key"
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/calculate-fees")
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data as dict
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return {"error": str(e)}
    
    # ==================== FEE CALCULATIONS ====================
    
    def calculate_fees(
        self,
        sale_price: float,
        production_cost: float = 0.0,
        shipping_cost: float = 0.0,
        offsite_ads: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate Etsy fees for a product
        
        Args:
            sale_price: Product sale price
            production_cost: Cost to produce
            shipping_cost: Shipping cost
            offsite_ads: Whether offsite ads are enabled
            
        Returns:
            Fee breakdown and profit calculation
        """
        data = {
            "sale_price": sale_price,
            "production_cost": production_cost,
            "shipping_cost": shipping_cost,
            "offsite_ads": offsite_ads
        }
        
        return self._make_request("POST", "/api/calculate-fees", data=data)
    
    # ==================== USER MANAGEMENT ====================
    
    def register_user(self, email: str, password: str, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Register new user
        
        Args:
            email: User email
            password: User password
            name: User name (optional)
            
        Returns:
            User data with access token
        """
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        
        return self._make_request("POST", "/api/auth/register", data=data)
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login user
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User data with access token
        """
        data = {
            "email": email,
            "password": password
        }
        
        return self._make_request("POST", "/api/auth/login", data=data)
    
    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """
        Get user information
        
        Args:
            user_id: User ID
            
        Returns:
            User data
        """
        return self._make_request("GET", f"/api/users/{user_id}")
    
    # ==================== DATA ANALYSIS ====================
    
    def analyze_sales_data(self, csv_data: str, analysis_type: str = "finance") -> Dict[str, Any]:
        """
        Analyze uploaded sales CSV data
        
        Args:
            csv_data: CSV data as string
            analysis_type: Type of analysis (finance, customer, seo)
            
        Returns:
            Analysis results
        """
        data = {
            "csv_data": csv_data,
            "analysis_type": analysis_type
        }
        
        return self._make_request("POST", "/api/analyze/sales", data=data)
    
    def get_product_insights(self, product_id: str) -> Dict[str, Any]:
        """
        Get AI insights for a specific product
        
        Args:
            product_id: Product ID
            
        Returns:
            Product insights and recommendations
        """
        return self._make_request("GET", f"/api/insights/product/{product_id}")
    
    # ==================== DASHBOARD DATA ====================
    
    def get_dashboard_data(self, user_id: str, dashboard_type: str) -> Dict[str, Any]:
        """
        Get dashboard data for user
        
        Args:
            user_id: User ID
            dashboard_type: Dashboard type (finance, customer, seo)
            
        Returns:
            Dashboard data
        """
        params = {"dashboard_type": dashboard_type}
        return self._make_request("GET", f"/api/dashboard/{user_id}", params=params)
    
    # ==================== PREMIUM FEATURES ====================
    
    def get_ai_recommendations(self, user_id: str) -> Dict[str, Any]:
        """
        Get AI-powered recommendations (Premium feature)
        
        Args:
            user_id: User ID
            
        Returns:
            AI recommendations
        """
        return self._make_request("GET", f"/api/premium/recommendations/{user_id}")
    
    def upgrade_to_premium(self, user_id: str, payment_method_id: str) -> Dict[str, Any]:
        """
        Upgrade user to premium
        
        Args:
            user_id: User ID
            payment_method_id: Stripe payment method ID
            
        Returns:
            Subscription data
        """
        data = {
            "user_id": user_id,
            "payment_method_id": payment_method_id
        }
        
        return self._make_request("POST", "/api/subscription/upgrade", data=data)
    
    # ==================== BENCHMARKS ====================
    
    def get_category_benchmarks(self, category: str) -> Dict[str, Any]:
        """
        Get benchmark data for a category
        
        Args:
            category: Product category
            
        Returns:
            Benchmark data (median price, sales volume, etc.)
        """
        params = {"category": category}
        return self._make_request("GET", "/api/benchmarks/category", params=params)
    
    def get_pricing_elasticity(self, category: str) -> Dict[str, Any]:
        """
        Get price elasticity model for category
        
        Args:
            category: Product category
            
        Returns:
            Elasticity model data
        """
        params = {"category": category}
        return self._make_request("GET", "/api/benchmarks/elasticity", params=params)


# ==================== CONVENIENCE FUNCTIONS ====================

@st.cache_resource
def get_api_client() -> APIClient:
    """Get cached API client instance"""
    return APIClient()


def handle_api_error(response: Dict[str, Any]) -> bool:
    """
    Check if API response contains error and display it
    
    Args:
        response: API response dict
        
    Returns:
        True if error, False if success
    """
    if "error" in response:
        st.error(f"Error: {response['error']}")
        return True
    return False