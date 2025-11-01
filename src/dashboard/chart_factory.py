"""
Chart Factory
Plotly chart creation templates
Extracted from sc_dashboard_new.py
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
sys.path.append('../..')
from config import COLORS

class ChartFactory:
    """Create standardized Plotly charts"""
    
    def __init__(self):
        self.colors = COLORS
    
    def create_plot(self, data: pd.DataFrame, plot_type: str, **kwargs):
        """
        Create standardized plots
        Extracted from sc_dashboard_new.py create_plot
        """
        plots = {
            'scatter': px.scatter,
            'bar': px.bar,
            'pie': px.pie,
            'line': px.line
        }
        return plots[plot_type](data, **kwargs)
    
    def create_correlation_heatmap(self, correlation_df: pd.DataFrame, title: str = "Correlation Matrix"):
        """Create correlation heatmap using Plotly"""
        fig = go.Figure(data=go.Heatmap(
            z=correlation_df.values,
            x=correlation_df.columns,
            y=correlation_df.index,
            colorscale='RdBu_r',
            zmid=0,
            text=correlation_df.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Sector",
            yaxis_title="Sector",
            height=500,
            width=700
        )
        
        return fig
    
    def create_time_series_chart(self, ts_df: pd.DataFrame, group_col: str = 'Sector'):
        """Create time series recovery pattern chart"""
        fig = px.line(
            ts_df,
            x='Date',
            y='Normalized_Price',
            color=group_col,
            title="Stock Price Recovery Patterns (Normalized to Base 100)",
            labels={'Normalized_Price': 'Price Index (Base 100)', 'Date': 'Date'},
            line_shape='spline',
            hover_data=['Ticker'] if 'Ticker' in ts_df.columns else None
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price Index (Base 100)",
            hovermode='x unified',
            height=500
        )
        
        return fig