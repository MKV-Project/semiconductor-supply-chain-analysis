"""
Dashboard Components
Reusable Streamlit UI components
Extracted from sc_dashboard_new.py
"""
import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict
from .chart_factory import ChartFactory
import sys
sys.path.append('../..')
from config import COLORS

class DashboardComponents:
    """Reusable dashboard UI components"""
    
    def __init__(self):
        self.chart_factory = ChartFactory()
        self.colors = COLORS
    
    def display_executive_summary(self, results: Dict):
        """
        Display executive summary section
        Extracted from sc_dashboard_new.py display_executive_summary
        """
        col1, col2, col3, col4 = st.columns(4)
        
        sc_data = results.get('supply_chain_impact', [])
        if sc_data:
            df = pd.DataFrame(sc_data)
            
            period = results.get('metadata', {}).get('period', 'N/A')
            formatted_period = "N/A"
            duration = "N/A"
            
            if ' to ' in period:
                start_part, end_part = period.split(' to ')
                try:
                    start_year = int(start_part.strip().split('-')[0])
                    end_year = int(end_part.strip().split('-')[0])
                    formatted_period = f"{start_year} to {end_year}"
                    duration = f"{end_year - start_year + 1} Years"
                except:
                    formatted_period = period
                    duration = "Multi-Year"
            
            with col1:
                st.metric("Analysis Period", formatted_period, delta=duration, delta_color="off")
            
            with col2:
                critical_count = len(df[df['Impact_Severity'] == 'Critical'])
                total_count = len(df)
                st.metric(
                    "Critical Impact", 
                    critical_count, 
                    delta=f"{critical_count/total_count*100:.0f}%" if total_count > 0 else "N/A", 
                    delta_color="inverse"
                )
                
            with col3:
                if not df['Estimated_Recovery_Months'].empty:
                    recovery_modes = df['Estimated_Recovery_Months'].mode()
                    avg_recovery = recovery_modes.iloc[0] if not recovery_modes.empty else "N/A"
                    st.metric("Avg Recovery", avg_recovery)
                else:
                    st.metric("Avg Recovery", "N/A")
                
            with col4:
                high_resilience = len(df[df['Supply_Chain_Resilience'] > 70])
                st.metric(
                    "Resilient Companies", 
                    high_resilience,
                    delta=f"{high_resilience/len(df)*100:.0f}%" if len(df) > 0 else "N/A"
                )
        
        st.subheader("Executive Summary")
        self._display_metrics(results)
        
        if sc_data:
            severity_counts = df['Impact_Severity'].value_counts().reset_index()
            severity_counts.columns = ['Severity', 'Count']
            
            if not severity_counts.empty:
                fig = self.chart_factory.create_plot(
                    data=severity_counts,
                    plot_type='pie',
                    values='Count',
                    names='Severity',
                    title="Distribution of Supply Chain Impact Severity",
                    color='Severity',
                    color_discrete_map=self.colors
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _display_metrics(self, results: Dict):
        """Display key performance metrics"""
        sc_data = pd.DataFrame(results.get('supply_chain_impact', []))
        if sc_data.empty:
            st.warning("No supply chain data available for summary")
            return

        cols = st.columns(4)
        
        cols[0].metric("Companies Analyzed", len(sc_data))
        cols[1].metric("Critical Impact", len(sc_data[sc_data['Impact_Severity'] == 'Critical']))
        cols[2].metric("Avg Resilience", f"{sc_data['Supply_Chain_Resilience'].mean():.1f}")
        
        sector_impacts = sc_data.groupby('Sector')['Financial_Impact_pct'].mean()
        if not sector_impacts.empty:
            highest_impact_sector = sector_impacts.idxmax()
            highest_impact_value = sector_impacts.max()
            cols[3].metric(f"{highest_impact_sector} Impact", f"{highest_impact_value:.1f}%")
        else:
            cols[3].metric("Sector Impact", "N/A")
    
    def display_performance_analysis(self, results: Dict):
        """Display performance analysis section"""
        st.subheader("Performance Analysis")
        
        if not (perf_data := results.get('performance')):
            st.warning("No performance data available")
            return
        
        df = pd.DataFrame([
            {
                'Company': data['name'],
                'Ticker': ticker,
                'Sector': data['sector'],
                'Return (%)': data['return'],
                'Volatility (%)': data['volatility'],
                'Drawdown (%)': data['drawdown'],
                'Abs_Drawdown': abs(data['drawdown'])
            }
            for ticker, data in perf_data.items()
        ])
        
        # Performance charts
        fig1 = self.chart_factory.create_plot(
            df,
            plot_type='bar',
            x='Company',
            y='Return (%)',
            color='Sector',
            title="Total Returns by Company",
            hover_data=['Ticker', 'Drawdown (%)']
        )
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = self.chart_factory.create_plot(
            df,
            plot_type='scatter',
            x='Volatility (%)',
            y='Return (%)',
            color='Sector',
            size='Abs_Drawdown',
            hover_data=['Company', 'Ticker'],
            title="Risk-Return Profile: Volatility vs Return",
            size_max=30
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        display_df = df.drop('Abs_Drawdown', axis=1).copy()
        display_df.index = range(1, len(display_df) + 1)
        st.dataframe(display_df, use_container_width=True)
    
    def display_risk_analysis(self, results: Dict):
        """Display risk analysis section"""
        st.subheader("Risk Assessment")
        
        if not (risk_data := results.get('risk')) or not (perf_data := results.get('performance')):
            st.warning("No risk assessment data available")
            return
        
        df = pd.DataFrame([
            {
                'Company': perf['name'],
                'Ticker': ticker,
                'Sector': perf['sector'],
                'Return (%)': perf['return'],
                'Volatility (%)': perf['volatility'],
                'Drawdown (%)': perf['drawdown'],
                'Risk_Score': risk_data.get(ticker, {}).get('score', 'Unknown')
            }
            for ticker, perf in perf_data.items()
        ])
        
        fig = self.chart_factory.create_plot(
            df,
            plot_type='scatter',
            x='Volatility (%)',
            y='Drawdown (%)',
            color='Risk_Score',
            size='Volatility (%)',
            hover_data=['Company', 'Sector', 'Return (%)'],
            title="Risk Analysis: Volatility vs Drawdown",
            color_discrete_map={'High': self.colors['High'], 'Low': self.colors['Low']}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        risk_counts = df['Risk_Score'].value_counts().reset_index()
        risk_counts.columns = ['Risk_Score', 'Count']
        fig = self.chart_factory.create_plot(
            risk_counts,
            plot_type='pie',
            values='Count',
            names='Risk_Score',
            title="Risk Score Distribution",
            color='Risk_Score',
            color_discrete_map={'High': self.colors['High'], 'Low': self.colors['Low']}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Sector Correlation Analysis")
        correlation_data = self._create_dynamic_correlation_matrix(results)
        
        if not correlation_data.empty:
            fig = self.chart_factory.create_correlation_heatmap(
                correlation_data,
                "Sector Performance Correlation Matrix"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("""
            **Interpretation:**
            - Values close to +1 (red): Strong positive correlation
            - Values close to -1 (blue): Strong negative correlation
            - Values close to 0 (white): No correlation
            """)
        
        display_df = df.copy()
        display_df.index = range(1, len(display_df) + 1)
        st.dataframe(display_df, use_container_width=True)
    
    def _create_dynamic_correlation_matrix(self, results: Dict) -> pd.DataFrame:
        """Create correlation matrix based on actual returns data"""
        try:
            perf_data = results.get('performance', {})
            if not perf_data:
                return pd.DataFrame()
            
            sector_returns = {}
            for ticker, data in perf_data.items():
                sector = data['sector']
                if sector not in sector_returns:
                    sector_returns[sector] = []
                sector_returns[sector].append(data['return'])
            
            sectors = list(sector_returns.keys())
            n_sectors = len(sectors)
            
            if n_sectors < 2:
                return pd.DataFrame()
            
            correlation_matrix = np.zeros((n_sectors, n_sectors))
            
            for i in range(n_sectors):
                for j in range(n_sectors):
                    if i == j:
                        correlation_matrix[i, j] = 1.0
                    else:
                        returns_i = np.array(sector_returns[sectors[i]])
                        returns_j = np.array(sector_returns[sectors[j]])
                        
                        min_len = min(len(returns_i), len(returns_j))
                        if min_len > 1:
                            corr = np.corrcoef(returns_i[:min_len], returns_j[:min_len])[0, 1]
                            correlation_matrix[i, j] = corr if not np.isnan(corr) else 0.0
                        else:
                            correlation_matrix[i, j] = 0.0
            
            return pd.DataFrame(correlation_matrix, index=sectors, columns=sectors)
            
        except Exception as e:
            st.warning(f"Could not generate correlation matrix: {str(e)}")
            return pd.DataFrame()
    
    def display_supply_chain_analysis(self, results: Dict):
        """Display supply chain impact analysis"""
        st.subheader("Supply Chain Impact Analysis")
        
        if not (sc_data := results.get('supply_chain_impact')):
            st.warning("No supply chain impact data available")
            return
        
        df = pd.DataFrame(sc_data)
        severity_counts = df['Impact_Severity'].value_counts()
        
        col1, col2 = st.columns(2)
        
        severity_df = severity_counts.reset_index()
        severity_df.columns = ['Severity', 'Count']
        
        with col1:
            if not severity_counts.empty:
                fig = self.chart_factory.create_plot(
                    severity_df,
                    plot_type='pie',
                    values='Count',
                    names='Severity',
                    title="Supply Chain Impact Severity",
                    color='Severity',
                    color_discrete_map=self.colors
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if not severity_counts.empty:
                fig = self.chart_factory.create_plot(
                    severity_df,
                    plot_type='bar',
                    x='Severity',
                    y='Count',
                    title="Impact Severity Count",
                    color='Severity',
                    color_discrete_map=self.colors
                )
                st.plotly_chart(fig, use_container_width=True)
        
        sectors = df['Sector'].unique()
        if len(sectors) > 0:
            sector_impact = df.groupby('Sector').agg({
                'Financial_Impact_pct': 'mean',
                'Supply_Chain_Resilience': 'mean',
                'Company': 'count'
            }).round(1)
            
            sector_impact_df = sector_impact.reset_index()
            if not sector_impact_df.empty:
                fig = self.chart_factory.create_plot(
                    sector_impact_df,
                    plot_type='bar',
                    x='Sector',
                    y='Financial_Impact_pct',
                    title="Average Financial Impact by Sector (%)",
                    color='Financial_Impact_pct',
                    color_continuous_scale='reds',
                    hover_data=['Supply_Chain_Resilience']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Recovery Trajectory Comparison")
        
        time_series_data = results.get('time_series_data')
        
        if time_series_data is not None:
            if isinstance(time_series_data, list):
                ts_df = pd.DataFrame(time_series_data)
            elif isinstance(time_series_data, pd.DataFrame):
                ts_df = time_series_data
            else:
                ts_df = pd.DataFrame()
            
            if not ts_df.empty and 'Date' in ts_df.columns:
                ts_df['Date'] = pd.to_datetime(ts_df['Date'])
                
                group_col = 'Sector' if 'Sector' in ts_df.columns else 'Company'
                
                fig = self.chart_factory.create_time_series_chart(ts_df, group_col)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Time series data unavailable or incomplete.")
        else:
            st.warning("No time series data available.")
        
        display_df = df[[
            'Company', 'Ticker', 'Sector', 'Semiconductor_Dependency',
            'Financial_Impact_pct', 'Impact_Severity', 'Estimated_Recovery_Months',
            'Supply_Chain_Resilience', 'Strategic_Recommendation'
        ]]
        
        display_df.index = range(1, len(display_df) + 1)
        st.dataframe(
            display_df.style.applymap(
                lambda x: f"background-color: {self.colors.get(x, '#65a30d')}; color: white" 
                if x in self.colors else '',
                subset=['Impact_Severity']
            ),
            use_container_width=True,
            height=400
        )
    
    def display_strategic_recommendations(self, results: Dict):
        """Display strategic recommendations"""
        st.subheader("Strategic Recommendations")
        
        if not (sc_data := results.get('supply_chain_impact')):
            st.warning("No data available for recommendations")
            return
        
        df = pd.DataFrame(sc_data)
        
        for sector in sorted(df['Sector'].unique()):
            sector_companies = df[df['Sector'] == sector]
            critical_companies = sector_companies[
                sector_companies['Impact_Severity'].isin(['Critical', 'Severe'])
            ]
            
            if critical_companies.empty:
                st.success(f"**{sector} Sector - Stable**")
                st.write(f"• {len(sector_companies)} companies analyzed")
                if not sector_companies.empty:
                    st.write(f"• Recommended action: {sector_companies['Strategic_Recommendation'].iloc[0]}")
            else:
                st.error(f"**{sector} Sector - Immediate Attention Required**")
                st.write(f"• {len(critical_companies)} companies with critical/severe impact")
                st.write(f"• Primary recommendation: {critical_companies['Strategic_Recommendation'].iloc[0]}")
            st.markdown("---")