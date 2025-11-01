"""
Main Streamlit Dashboard Application
Orchestrates all analysis and visualization components
Refactored from sc_dashboard_new.py
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config import DEFAULT_TICKERS, DATE_RANGE, COLORS
from src.analysis.performance_analyzer import PerformanceAnalyzer
from src.analysis.risk_analyzer import RiskAnalyzer
from src.analysis.supply_chain_analyzer import SupplyChainAnalyzer
from src.analysis.sector_analyzer import SectorAnalyzer
from src.analysis.time_series_analyzer import TimeSeriesAnalyzer
from src.dashboard.dashboard_components import DashboardComponents
from src.dashboard.export_utils import ExportUtils

# Page config
st.set_page_config(
    page_title="SC-ALERT: Supply Chain Resilience",
    page_icon="🔗",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #2563eb; text-align: center; margin-bottom: 1rem; }
    .impact-critical { background-color: #dc2626; color: white; padding: 0.2rem 0.5rem; border-radius: 5px; }
    .impact-severe { background-color: #ea580c; color: white; padding: 0.2rem 0.5rem; border-radius: 5px; }
    .impact-moderate { background-color: #d97706; color: white; padding: 0.2rem 0.5rem; border-radius: 5px; }
    .impact-low { background-color: #65a30d; color: white; padding: 0.2rem 0.5rem; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def run_analysis(tickers: list, start_date: datetime, end_date: datetime, 
                risk_threshold: float) -> dict:
    """Run complete analysis pipeline"""
    with st.spinner('Analyzing supply chain impacts...'):
        # Clean tickers
        tickers = [t.strip().upper() for t in tickers if t.strip()]
        
        # Initialize analyzers
        perf_analyzer = PerformanceAnalyzer()
        risk_analyzer = RiskAnalyzer()
        sc_analyzer = SupplyChainAnalyzer()
        sector_analyzer = SectorAnalyzer()
        ts_analyzer = TimeSeriesAnalyzer()
        
        # Fetch data
        companies = perf_analyzer.fetch_companies(tickers, start_date, end_date)
        
        if not companies:
            raise ValueError("No valid stock data collected")
        
        # Run analyses
        results = {
            'metadata': {
                'tickers': tickers,
                'period': f"{start_date} to {end_date}",
                'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'total_companies': len(companies)
            },
            'performance': perf_analyzer.get_performance_dict(companies),
            'risk': risk_analyzer.analyze_risk(companies, risk_threshold),
            'supply_chain_impact': sc_analyzer.analyze_supply_chain(companies),
            'sector_vulnerability': sector_analyzer.analyze_sectors(companies),
            'time_series_data': ts_analyzer.get_time_series_data(companies),
            'companies': [c.ticker for c in companies]
        }
        
        return results

def main():
    """Main application function"""
    st.markdown('<h1 class="main-header">RiskFlow</h1>', unsafe_allow_html=True)
    st.markdown("### Semiconductor Supply Chain Resilience Analysis")
    
    # Initialize dashboard components
    dashboard = DashboardComponents()
    
    # Sidebar controls
    st.sidebar.title("Analysis Controls")
    tickers = [t.strip() for t in st.sidebar.text_area(
        "Enter company tickers (comma-separated):",
        value=DEFAULT_TICKERS,
        height=100,
        help="Include companies from different sectors"
    ).split(',') if t.strip()]
    
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("Start Date", value=DATE_RANGE['start'])
    end_date = col2.date_input("End Date", value=DATE_RANGE['end'])
    
    risk_threshold = st.sidebar.slider(
        "Risk Detection Sensitivity:",
        min_value=0.1,
        max_value=0.5,
        value=0.3,
        step=0.05,
        help="Higher values detect more anomalies"
    )
    
    # Analysis controls
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Run Analysis", type="primary", use_container_width=True):
        try:
            results = run_analysis(tickers, start_date, end_date, risk_threshold)
            st.session_state.results = results
            st.success("Analysis completed successfully!")
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
    
    if col2.button("Clear Results", use_container_width=True):
        st.session_state.pop('results', None)
        st.rerun()
    
    # Display results
    if results := st.session_state.get('results'):
        # Export options
        st.sidebar.markdown("---")
        st.sidebar.subheader("Export Results")
        
        if st.sidebar.button("Export All Data to Excel", use_container_width=True):
            if excel_file := ExportUtils.create_excel_export(results):
                st.sidebar.download_button(
                    "⬇ Download Excel",
                    excel_file,
                    file_name=f"supply_chain_analysis_{datetime.now():%Y%m%d_%H%M}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        # Individual CSV exports
        for label, data_key in [
            ("Supply Chain Impact", 'supply_chain_impact'),
            ("Sector Vulnerability", 'sector_vulnerability'),
            ("Performance Data", 'performance')
        ]:
            if data := results.get(data_key):
                df = pd.DataFrame(data)
                if data_key == 'performance':
                    df = df.T
                st.sidebar.download_button(
                    f"{label}",
                    df.to_csv(index=False),
                    file_name=f"{data_key}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        # Analysis tabs
        tabs = st.tabs([
            "Summary",
            "Performance",
            "Risk",
            "Supply Chain",
            "Recommendations"
        ])
        
        with tabs[0]:
            dashboard.display_executive_summary(results)
        
        with tabs[1]:
            dashboard.display_performance_analysis(results)
        
        with tabs[2]:
            dashboard.display_risk_analysis(results)
        
        with tabs[3]:
            dashboard.display_supply_chain_analysis(results)
        
        with tabs[4]:
            dashboard.display_strategic_recommendations(results)
    
    else:
        st.info("""
        ## Supply Chain Risk Analysis Dashboard

        Analyze and monitor semiconductor supply chain risks across industries.
        
        ### Quick Start:
        1. Enter tickers in sidebar
        2. Set date range
        3. Run analysis
        4. View results in tabs

        ### Key Features:
        • Real-time stock data analysis
        • Machine learning risk detection
        • Interactive visualizations
        • Multi-sector correlation analysis
        • Excel/CSV export options
        """)

if __name__ == "__main__":
    main()