"""
Chart Components
Reusable Plotly and Altair visualizations for dashboards
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
from typing import List, Optional, Dict, Any


def create_margin_chart(
    df: pd.DataFrame,
    product_col: str = "Product",
    margin_col: str = "Margin",
    title: str = "Profit Margin by Product"
) -> go.Figure:
    """
    Create horizontal bar chart for profit margins
    
    Args:
        df: DataFrame with product and margin data
        product_col: Column name for products
        margin_col: Column name for margins
        title: Chart title
        
    Returns:
        Plotly figure
    """
    # Sort by margin
    df = df.sort_values(by=margin_col)
    
    # Color based on margin value
    colors = ['#e74c3c' if m < 0 else '#f39c12' if m < 20 else '#27ae60' 
              for m in df[margin_col]]
    
    fig = go.Figure(data=[
        go.Bar(
            y=df[product_col],
            x=df[margin_col],
            orientation='h',
            marker=dict(color=colors),
            text=df[margin_col].round(1).astype(str) + '%',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Profit Margin (%)",
        yaxis_title="",
        height=max(400, len(df) * 30),
        showlegend=False,
        template="plotly_white"
    )
    
    return fig


def create_revenue_chart(
    df: pd.DataFrame,
    date_col: str = "Date",
    revenue_col: str = "Revenue",
    title: str = "Revenue Over Time"
) -> go.Figure:
    """
    Create line chart for revenue over time
    
    Args:
        df: DataFrame with date and revenue data
        date_col: Column name for dates
        revenue_col: Column name for revenue
        title: Chart title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[date_col],
        y=df[revenue_col],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        height=400,
        template="plotly_white",
        hovermode='x unified'
    )
    
    return fig


def create_profit_chart(
    df: pd.DataFrame,
    date_col: str = "Date",
    revenue_col: str = "Revenue",
    cost_col: str = "Cost",
    title: str = "Revenue vs Costs"
) -> go.Figure:
    """
    Create dual-axis chart comparing revenue and costs
    
    Args:
        df: DataFrame with date, revenue, and cost data
        date_col: Column name for dates
        revenue_col: Column name for revenue
        cost_col: Column name for costs
        title: Chart title
        
    Returns:
        Plotly figure
    """
    df['Profit'] = df[revenue_col] - df[cost_col]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df[date_col],
        y=df[revenue_col],
        name='Revenue',
        marker_color='#27ae60'
    ))
    
    fig.add_trace(go.Bar(
        x=df[date_col],
        y=df[cost_col],
        name='Costs',
        marker_color='#e74c3c'
    ))
    
    fig.add_trace(go.Scatter(
        x=df[date_col],
        y=df['Profit'],
        name='Profit',
        line=dict(color='#667eea', width=3),
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        height=400,
        template="plotly_white",
        barmode='group',
        hovermode='x unified'
    )
    
    return fig


def create_pie_chart(
    labels: List[str],
    values: List[float],
    title: str = "Distribution",
    colors: Optional[List[str]] = None
) -> go.Figure:
    """
    Create pie chart
    
    Args:
        labels: Category labels
        values: Category values
        title: Chart title
        colors: Custom colors (optional)
        
    Returns:
        Plotly figure
    """
    if colors is None:
        colors = px.colors.qualitative.Set3
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hole=0.3,
        textinfo='label+percent',
        textposition='outside'
    )])
    
    fig.update_layout(
        title=title,
        height=400,
        showlegend=True,
        template="plotly_white"
    )
    
    return fig


def create_geographic_map(
    df: pd.DataFrame,
    country_col: str = "Country",
    value_col: str = "Sales",
    title: str = "Sales by Country"
) -> go.Figure:
    """
    Create choropleth map for geographic data
    
    Args:
        df: DataFrame with country and value data
        country_col: Column name for countries
        value_col: Column name for values
        title: Chart title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(data=go.Choropleth(
        locations=df[country_col],
        z=df[value_col],
        locationmode='country names',
        colorscale='Blues',
        marker_line_color='white',
        marker_line_width=0.5,
        colorbar_title=value_col
    ))
    
    fig.update_layout(
        title=title,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        height=500,
        template="plotly_white"
    )
    
    return fig


def create_funnel_chart(
    stages: List[str],
    values: List[float],
    title: str = "Sales Funnel"
) -> go.Figure:
    """
    Create funnel chart
    
    Args:
        stages: Funnel stage names
        values: Values for each stage
        title: Chart title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent initial",
        marker=dict(
            color=['#667eea', '#764ba2', '#F56400', '#e74c3c']
        )
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        template="plotly_white"
    )
    
    return fig


def create_comparison_bar_chart(
    categories: List[str],
    series1: List[float],
    series2: List[float],
    series1_name: str = "Current",
    series2_name: str = "Previous",
    title: str = "Comparison"
) -> go.Figure:
    """
    Create grouped bar chart for comparisons
    
    Args:
        categories: Category labels
        series1: First data series
        series2: Second data series
        series1_name: Name for first series
        series2_name: Name for second series
        title: Chart title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=series1,
        name=series1_name,
        marker_color='#667eea'
    ))
    
    fig.add_trace(go.Bar(
        x=categories,
        y=series2,
        name=series2_name,
        marker_color='#95a5a6'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="",
        yaxis_title="Value",
        height=400,
        barmode='group',
        template="plotly_white",
        hovermode='x unified'
    )
    
    return fig


def create_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    size_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: str = "Scatter Plot"
) -> go.Figure:
    """
    Create scatter plot
    
    Args:
        df: DataFrame
        x_col: X-axis column
        y_col: Y-axis column
        size_col: Column for bubble size (optional)
        color_col: Column for color (optional)
        title: Chart title
        
    Returns:
        Plotly figure
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        size=size_col,
        color=color_col,
        title=title,
        height=400,
        template="plotly_white"
    )
    
    return fig


def create_gauge_chart(
    value: float,
    max_value: float = 100,
    title: str = "Performance",
    threshold_low: float = 33,
    threshold_high: float = 66
) -> go.Figure:
    """
    Create gauge chart (KPI indicator)
    
    Args:
        value: Current value
        max_value: Maximum value
        title: Chart title
        threshold_low: Low threshold (red to yellow)
        threshold_high: High threshold (yellow to green)
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, threshold_low], 'color': "#ffebee"},
                {'range': [threshold_low, threshold_high], 'color': "#fff3e0"},
                {'range': [threshold_high, max_value], 'color': "#e8f5e9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold_high
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        template="plotly_white"
    )
    
    return fig


def create_heatmap(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    value_col: str,
    title: str = "Heatmap"
) -> go.Figure:
    """
    Create heatmap
    
    Args:
        df: DataFrame
        x_col: X-axis column
        y_col: Y-axis column
        value_col: Value column for colors
        title: Chart title
        
    Returns:
        Plotly figure
    """
    pivot_table = df.pivot(index=y_col, columns=x_col, values=value_col)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='Blues',
        text=pivot_table.values,
        texttemplate='%{text:.1f}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title=title,
        height=400,
        template="plotly_white"
    )
    
    return fig


def display_chart(fig: go.Figure, use_container_width: bool = True):
    """
    Display Plotly chart in Streamlit
    
    Args:
        fig: Plotly figure
        use_container_width: Use full container width
    """
    st.plotly_chart(fig, use_container_width=use_container_width)


def create_metric_cards(metrics: List[Dict[str, Any]]):
    """
    Create metric cards layout
    
    Args:
        metrics: List of dicts with 'label', 'value', 'delta' keys
    """
    cols = st.columns(len(metrics))
    
    for i, metric in enumerate(metrics):
        with cols[i]:
            st.metric(
                label=metric['label'],
                value=metric['value'],
                delta=metric.get('delta'),
                delta_color=metric.get('delta_color', 'normal')
            )