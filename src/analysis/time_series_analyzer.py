"""
Time Series Analyzer
Handles time series data and recovery pattern analysis
Extracted from sc_analyzer_new.py
"""
import pandas as pd
from typing import List

class TimeSeriesAnalyzer:
    """Analyze time series and recovery patterns"""
    
    def __init__(self):
        pass
    
    def get_time_series_data(self, companies: List, max_companies: int = 6) -> pd.DataFrame:
        """
        Get actual normalized price data for time series visualization
        Extracted from SCAnalyzer.get_time_series_data
        
        Args:
            companies: List of CompanyData objects
            max_companies: Maximum companies to include
            
        Returns:
            DataFrame with normalized price time series
        """
        try:
            time_series_data = []
            
            # Select diverse companies
            selected_companies = self._select_diverse_companies(companies, max_companies)
            
            for company in selected_companies:
                if hasattr(company, 'data') and not company.data.empty:
                    # Use actual historical data
                    data = company.data.reset_index()
                    
                    # Normalize prices to base 100
                    base_price = data['Close'].iloc[0]
                    data['Normalized_Price'] = (data['Close'] / base_price) * 100
                    
                    # Sample data points for cleaner visualization (max 100 points)
                    if len(data) > 100:
                        data = data.iloc[::len(data)//100]
                    
                    for _, row in data.iterrows():
                        time_series_data.append({
                            'Date': row['Date'],
                            'Normalized_Price': round(row['Normalized_Price'], 2),
                            'Company': company.name,
                            'Ticker': company.ticker,
                            'Sector': company.sector
                        })
            
            return pd.DataFrame(time_series_data)
            
        except Exception as e:
            print(f"Error generating time series data: {str(e)}")
            return pd.DataFrame()
    
    def _select_diverse_companies(self, companies: List, max_companies: int) -> List:
        """
        Select diverse companies for visualization
        Extracted from SCAnalyzer._select_diverse_companies
        """
        selected = []
        sectors_covered = set()
        
        # First pass: one per sector
        for company in companies:
            if company.sector not in sectors_covered:
                selected.append(company)
                sectors_covered.add(company.sector)
        
        # Second pass: fill remaining slots
        if len(selected) < max_companies:
            remaining = [c for c in companies if c not in selected]
            selected.extend(remaining[:max_companies - len(selected)])
        
        return selected[:max_companies]