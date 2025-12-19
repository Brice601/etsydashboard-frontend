"""
Calculator Components
Reusable calculator logic for fee calculations, pricing scenarios, etc.
"""

import streamlit as st
from typing import Dict, List, Optional, Tuple
from utils.helpers import format_currency, format_percentage, calculate_etsy_fees


class FeesCalculator:
    """Interactive Etsy fees calculator component"""
    
    @staticmethod
    def render_basic_calculator(
        default_price: float = 29.99,
        default_cost: float = 12.0,
        default_shipping: float = 4.0
    ) -> Dict[str, float]:
        """
        Render basic fees calculator
        
        Args:
            default_price: Default sale price
            default_cost: Default production cost
            default_shipping: Default shipping cost
            
        Returns:
            Dict with calculation results
        """
        col1, col2 = st.columns(2)
        
        with col1:
            sale_price = st.number_input(
                "Sale Price ($)",
                min_value=0.0,
                value=default_price,
                step=0.01,
                help="The price your customer pays"
            )
            
            production_cost = st.number_input(
                "Production Cost ($)",
                min_value=0.0,
                value=default_cost,
                step=0.01,
                help="Materials, labor, packaging"
            )
        
        with col2:
            shipping_cost = st.number_input(
                "Shipping Cost ($)",
                min_value=0.0,
                value=default_shipping,
                step=0.01,
                help="What you pay for shipping"
            )
            
            offsite_ads = st.checkbox(
                "Offsite Ads Enabled",
                value=False,
                help="15% fee when sales come from Etsy ads"
            )
        
        # Calculate fees
        fees = calculate_etsy_fees(sale_price, offsite_ads)
        profit = fees["net_revenue"] - production_cost - shipping_cost
        profit_margin = (profit / sale_price * 100) if sale_price > 0 else 0
        
        return {
            "sale_price": sale_price,
            "production_cost": production_cost,
            "shipping_cost": shipping_cost,
            "offsite_ads": offsite_ads,
            "fees": fees,
            "profit": profit,
            "profit_margin": profit_margin
        }
    
    @staticmethod
    def display_results(results: Dict[str, float]):
        """
        Display calculation results with formatting
        
        Args:
            results: Results dict from calculator
        """
        profit = results["profit"]
        margin = results["profit_margin"]
        
        # Determine result color/style
        if profit < 0:
            result_class = "danger"
            icon = "🔴"
        elif margin < 20:
            result_class = "warning"
            icon = "🟡"
        else:
            result_class = "success"
            icon = "🟢"
        
        # Display main result
        st.markdown(f"""
            <div class="result-box {result_class}">
                <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">
                    {icon} Net Profit Per Sale
                </div>
                <div class="big-number" style="color: {'#e74c3c' if profit < 0 else '#27ae60'};">
                    {format_currency(profit)}
                </div>
                <div style="font-size: 1rem; opacity: 0.8;">
                    {format_percentage(margin / 100, decimals=1)} profit margin
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_fees_breakdown(fees: Dict[str, float], production_cost: float, shipping_cost: float):
        """
        Display detailed fees breakdown
        
        Args:
            fees: Fees dict from calculate_etsy_fees
            production_cost: Production cost
            shipping_cost: Shipping cost
        """
        total_costs = fees["total_fees"] + production_cost + shipping_cost
        
        st.markdown(f"""
            <div class="fees-breakdown">
                <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 1rem;">
                    Fee Breakdown
                </div>
                <div class="fee-item">
                    <span>Transaction Fee (6.5%)</span>
                    <span>-{format_currency(fees['transaction_fee'])}</span>
                </div>
                <div class="fee-item">
                    <span>Listing Fee</span>
                    <span>-{format_currency(fees['listing_fee'])}</span>
                </div>
                <div class="fee-item">
                    <span>Payment Processing</span>
                    <span>-{format_currency(fees['payment_processing'])}</span>
                </div>
                {'<div class="fee-item"><span>Offsite Ads (15%)</span><span>-' + format_currency(fees['offsite_ads']) + '</span></div>' if fees['offsite_ads'] > 0 else ''}
                <div class="fee-item">
                    <span>Production Cost</span>
                    <span>-{format_currency(production_cost)}</span>
                </div>
                <div class="fee-item">
                    <span>Shipping Cost</span>
                    <span>-{format_currency(shipping_cost)}</span>
                </div>
                <div class="fee-item" style="border-top: 2px solid #dee2e6; margin-top: 0.5rem; padding-top: 0.5rem;">
                    <span><strong>TOTAL COSTS</strong></span>
                    <span><strong>-{format_currency(total_costs)}</strong></span>
                </div>
            </div>
        """, unsafe_allow_html=True)


class PricingSimulator:
    """Pricing scenario simulator"""
    
    @staticmethod
    def simulate_scenarios(
        current_price: float,
        production_cost: float,
        shipping_cost: float,
        current_volume: int,
        offsite_ads: bool = False
    ) -> List[Dict[str, any]]:
        """
        Simulate different pricing scenarios
        
        Args:
            current_price: Current sale price
            production_cost: Production cost
            shipping_cost: Shipping cost
            current_volume: Current monthly sales volume
            offsite_ads: Offsite ads enabled
            
        Returns:
            List of scenario dicts
        """
        scenarios = []
        
        # Price elasticity assumptions (simplified)
        # Commodity products: high elasticity (-10% price = +20% volume)
        # Artisan products: low elasticity (-10% price = +5% volume)
        elasticity = 1.5  # Medium elasticity assumption
        
        # Scenario A: Lower price
        lower_price = current_price * 0.90
        lower_volume = int(current_volume * (1 + elasticity * 0.10))
        lower_fees = calculate_etsy_fees(lower_price, offsite_ads)
        lower_profit_per_sale = lower_fees["net_revenue"] - production_cost - shipping_cost
        lower_total_profit = lower_profit_per_sale * lower_volume
        
        scenarios.append({
            "name": "Lower Price (-10%)",
            "price": lower_price,
            "volume": lower_volume,
            "profit_per_sale": lower_profit_per_sale,
            "total_profit": lower_total_profit,
            "margin": (lower_profit_per_sale / lower_price * 100) if lower_price > 0 else 0
        })
        
        # Scenario B: Current price (baseline)
        current_fees = calculate_etsy_fees(current_price, offsite_ads)
        current_profit_per_sale = current_fees["net_revenue"] - production_cost - shipping_cost
        current_total_profit = current_profit_per_sale * current_volume
        
        scenarios.append({
            "name": "Current Price",
            "price": current_price,
            "volume": current_volume,
            "profit_per_sale": current_profit_per_sale,
            "total_profit": current_total_profit,
            "margin": (current_profit_per_sale / current_price * 100) if current_price > 0 else 0
        })
        
        # Scenario C: Higher price
        higher_price = current_price * 1.10
        higher_volume = int(current_volume * (1 - elasticity * 0.10))
        higher_fees = calculate_etsy_fees(higher_price, offsite_ads)
        higher_profit_per_sale = higher_fees["net_revenue"] - production_cost - shipping_cost
        higher_total_profit = higher_profit_per_sale * higher_volume
        
        scenarios.append({
            "name": "Higher Price (+10%)",
            "price": higher_price,
            "volume": higher_volume,
            "profit_per_sale": higher_profit_per_sale,
            "total_profit": higher_total_profit,
            "margin": (higher_profit_per_sale / higher_price * 100) if higher_price > 0 else 0
        })
        
        # Scenario D: Optimal price (maximize total profit)
        optimal_price = current_price * 1.15
        optimal_volume = int(current_volume * (1 - elasticity * 0.15))
        optimal_fees = calculate_etsy_fees(optimal_price, offsite_ads)
        optimal_profit_per_sale = optimal_fees["net_revenue"] - production_cost - shipping_cost
        optimal_total_profit = optimal_profit_per_sale * optimal_volume
        
        scenarios.append({
            "name": "Optimal Price (+15%)",
            "price": optimal_price,
            "volume": optimal_volume,
            "profit_per_sale": optimal_profit_per_sale,
            "total_profit": optimal_total_profit,
            "margin": (optimal_profit_per_sale / optimal_price * 100) if optimal_price > 0 else 0
        })
        
        return scenarios
    
    @staticmethod
    def display_scenarios(scenarios: List[Dict[str, any]]):
        """
        Display pricing scenarios comparison
        
        Args:
            scenarios: List of scenario dicts
        """
        st.markdown("### 🎯 Pricing Scenarios")
        
        # Find best scenario
        best_scenario = max(scenarios, key=lambda x: x["total_profit"])
        
        cols = st.columns(len(scenarios))
        
        for i, scenario in enumerate(scenarios):
            with cols[i]:
                is_best = scenario["name"] == best_scenario["name"]
                
                card_style = "border: 3px solid #27ae60;" if is_best else ""
                
                st.markdown(f"""
                    <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                                box-shadow: 0 2px 10px rgba(0,0,0,0.1); {card_style}">
                        <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 1rem;">
                            {scenario['name']} {'✅' if is_best else ''}
                        </div>
                        <div style="margin-bottom: 0.5rem;">
                            <strong>Price:</strong> {format_currency(scenario['price'])}
                        </div>
                        <div style="margin-bottom: 0.5rem;">
                            <strong>Volume:</strong> {scenario['volume']} sales/mo
                        </div>
                        <div style="margin-bottom: 0.5rem;">
                            <strong>Profit/Sale:</strong> {format_currency(scenario['profit_per_sale'])}
                        </div>
                        <div style="margin-bottom: 0.5rem;">
                            <strong>Total/Month:</strong> {format_currency(scenario['total_profit'])}
                        </div>
                        <div style="color: #7f8c8d; font-size: 0.9rem;">
                            {format_percentage(scenario['margin'] / 100, decimals=1)} margin
                        </div>
                    </div>
                """, unsafe_allow_html=True)


class BreakevenCalculator:
    """Break-even point calculator"""
    
    @staticmethod
    def calculate_breakeven(
        fixed_costs: float,
        variable_cost_per_unit: float,
        sale_price: float,
        offsite_ads: bool = False
    ) -> Dict[str, float]:
        """
        Calculate break-even point
        
        Args:
            fixed_costs: Monthly fixed costs
            variable_cost_per_unit: Variable cost per unit
            sale_price: Sale price per unit
            offsite_ads: Offsite ads enabled
            
        Returns:
            Break-even analysis results
        """
        fees = calculate_etsy_fees(sale_price, offsite_ads)
        net_revenue_per_unit = fees["net_revenue"]
        
        contribution_margin = net_revenue_per_unit - variable_cost_per_unit
        
        if contribution_margin <= 0:
            return {
                "breakeven_units": float('inf'),
                "breakeven_revenue": float('inf'),
                "error": "Contribution margin is negative or zero"
            }
        
        breakeven_units = fixed_costs / contribution_margin
        breakeven_revenue = breakeven_units * sale_price
        
        return {
            "breakeven_units": breakeven_units,
            "breakeven_revenue": breakeven_revenue,
            "contribution_margin": contribution_margin,
            "margin_percent": (contribution_margin / sale_price * 100) if sale_price > 0 else 0
        }
    
    @staticmethod
    def display_breakeven(results: Dict[str, float]):
        """
        Display break-even results
        
        Args:
            results: Results from calculate_breakeven
        """
        if "error" in results:
            st.error(f"⚠️ {results['error']}")
            return
        
        st.markdown(f"""
            <div class="insight-box">
                <div class="insight-title">📊 Break-Even Analysis</div>
                <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                    You need to sell <strong>{int(results['breakeven_units'])} units</strong> 
                    to cover your fixed costs.
                </p>
                <p style="font-size: 1rem; opacity: 0.8; margin: 0;">
                    Break-even revenue: <strong>{format_currency(results['breakeven_revenue'])}</strong>
                </p>
                <p style="font-size: 0.9rem; opacity: 0.7; margin-top: 0.5rem;">
                    Contribution margin: {format_currency(results['contribution_margin'])} per unit 
                    ({format_percentage(results['margin_percent'] / 100, decimals=1)})
                </p>
            </div>
        """, unsafe_allow_html=True)


class OpportunityAnalyzer:
    """Analyze profit opportunities"""
    
    @staticmethod
    def analyze_opportunities(
        current_price: float,
        production_cost: float,
        shipping_cost: float,
        monthly_volume: int,
        offsite_ads: bool = False
    ) -> List[Dict[str, any]]:
        """
        Identify profit improvement opportunities
        
        Args:
            current_price: Current sale price
            production_cost: Production cost
            shipping_cost: Shipping cost
            monthly_volume: Monthly sales volume
            offsite_ads: Offsite ads enabled
            
        Returns:
            List of opportunities
        """
        opportunities = []
        
        # Current state
        current_fees = calculate_etsy_fees(current_price, offsite_ads)
        current_profit = current_fees["net_revenue"] - production_cost - shipping_cost
        current_monthly = current_profit * monthly_volume
        
        # Opportunity 1: Optimize pricing
        optimal_price = current_price * 1.15
        optimal_fees = calculate_etsy_fees(optimal_price, offsite_ads)
        optimal_profit = optimal_fees["net_revenue"] - production_cost - shipping_cost
        optimal_monthly = optimal_profit * int(monthly_volume * 0.90)  # Assume 10% volume loss
        
        if optimal_monthly > current_monthly:
            opportunities.append({
                "type": "pricing",
                "title": "Optimize Pricing",
                "description": f"Increase price to {format_currency(optimal_price)}",
                "impact": optimal_monthly - current_monthly,
                "action": "Test higher price for 2 weeks"
            })
        
        # Opportunity 2: Disable offsite ads (if enabled and margin is low)
        if offsite_ads:
            no_ads_fees = calculate_etsy_fees(current_price, False)
            no_ads_profit = no_ads_fees["net_revenue"] - production_cost - shipping_cost
            no_ads_monthly = no_ads_profit * monthly_volume
            
            if no_ads_monthly > current_monthly:
                opportunities.append({
                    "type": "offsite_ads",
                    "title": "Disable Offsite Ads",
                    "description": "Save 15% fee on each sale",
                    "impact": no_ads_monthly - current_monthly,
                    "action": "Turn off offsite ads in Etsy settings"
                })
        
        # Opportunity 3: Reduce shipping cost
        reduced_shipping = shipping_cost * 0.80
        reduced_profit = current_fees["net_revenue"] - production_cost - reduced_shipping
        reduced_monthly = reduced_profit * monthly_volume
        
        if reduced_monthly > current_monthly:
            opportunities.append({
                "type": "shipping",
                "title": "Optimize Shipping",
                "description": f"Reduce shipping cost to {format_currency(reduced_shipping)}",
                "impact": reduced_monthly - current_monthly,
                "action": "Negotiate better shipping rates or lighter packaging"
            })
        
        # Sort by impact
        opportunities.sort(key=lambda x: x["impact"], reverse=True)
        
        return opportunities
    
    @staticmethod
    def display_opportunities(opportunities: List[Dict[str, any]]):
        """
        Display profit opportunities
        
        Args:
            opportunities: List of opportunity dicts
        """
        if not opportunities:
            st.success("✅ Your pricing is already optimized!")
            return
        
        total_impact = sum(opp["impact"] for opp in opportunities)
        
        st.markdown(f"""
            <div class="result-box warning">
                <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">
                    ⚡ You could earn {format_currency(total_impact)} more per month
                </div>
                <p>Here are {len(opportunities)} opportunities to increase profit:</p>
            </div>
        """, unsafe_allow_html=True)
        
        for i, opp in enumerate(opportunities, 1):
            st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                            box-shadow: 0 2px 10px rgba(0,0,0,0.08); margin: 1rem 0;">
                    <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem;">
                        {i}. {opp['title']} - +{format_currency(opp['impact'])}/month
                    </div>
                    <p style="margin: 0.5rem 0;">{opp['description']}</p>
                    <p style="font-size: 0.9rem; color: #667eea; margin: 0;">
                        <strong>Action:</strong> {opp['action']}
                    </p>
                </div>
            """, unsafe_allow_html=True)