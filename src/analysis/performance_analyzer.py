"""
Performance Analyzer
Handles stock data fetching and performance metrics calculation
Extracted from sc_analyzer_new.py
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
from functools import lru_cache
import warnings
warnings.filterwarnings('ignore')

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
from config import SECTOR_MAP

@dataclass
class CompanyData:
    """Container for company information"""
    name: str
    sector: str
    data: pd.DataFrame
    ticker: str
    metrics: dict

class PerformanceAnalyzer:
    """Fetch stock data and calculate performance metrics"""
    
    def __init__(self):
        self._sector_map = SECTOR_MAP
    
    def fetch_companies(self, tickers: List[str], start_date: datetime, 
                       end_date: datetime) -> List[CompanyData]:
        """
        Process company data with error handling
        Extracted from SCAnalyzer._process_companies
        """
        companies = []
        
        for ticker in tickers:
            try:
                if data := self._fetch_stock_data(ticker, start_date, end_date):
                    companies.append(data)
            except Exception as e:
                warnings.warn(f"Error processing {ticker}: {str(e)}")
                continue
                
        return companies
    
    @lru_cache(maxsize=100)
    def _fetch_stock_data(self, ticker: str, start_date: datetime, 
                         end_date: datetime) -> Optional[CompanyData]:
        """
        Fetch and process stock data with caching
        Extracted from SCAnalyzer._fetch_stock_data
        """
        try:
            # Download data
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            
            if len(data) < 30:
                return None
            
            # Calculate metrics
            data['Return'] = data['Close'].pct_change()
            data['Volatility'] = data['Return'].rolling(30, min_periods=10).std() * np.sqrt(252)
            data = data.fillna(method='ffill').fillna(method='bfill')
            
            if data.isnull().any().any():
                return None
            
            # Calculate key metrics
            returns = (data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100
            volatility = float(data['Volatility'].mean() * 100)
            drawdown = ((data['Close'].min() / data['Close'].max()) - 1) * 100
            
            return CompanyData(
                name=stock.info.get('longName', ticker),
                sector=self._determine_sector(ticker, stock),
                data=data,
                ticker=ticker,
                metrics={
                    'return': round(returns, 2),
                    'volatility': round(volatility, 2),
                    'drawdown': round(drawdown, 2)
                }
            )
            
        except Exception:
            return None
    
    def _determine_sector(self, ticker: str, stock: yf.Ticker) -> str:
        """
        Determine company sector
        Extracted from SCAnalyzer._determine_sector
        """
        # Check predefined sectors
        for sector, tickers in self._sector_map.items():
            if ticker in tickers:
                return sector
        
        # Use Yahoo Finance data
        try:
            sector = stock.info.get('sector', '').lower()
            industry = stock.info.get('industry', '').lower()
            
            if any(word in sector + industry 
                   for word in ['semiconductor', 'chip']):
                return 'Semiconductors'
            elif any(word in sector + industry 
                    for word in ['auto', 'vehicle']):
                return 'Automotive'
            elif any(word in sector + industry 
                    for word in ['electronic', 'computer']):
                return 'Consumer Electronics'
            elif any(word in sector + industry 
                    for word in ['telecom', 'industrial']):
                return 'Telecom_Industrial'
        except:
            pass
        
        return 'Other'
    
    def get_performance_dict(self, companies: List[CompanyData]) -> dict:
        """
        Extract performance data as dictionary
        Extracted from SCAnalyzer._get_performance_data
        """
        return {
            company.ticker: {
                'name': company.name,
                'sector': company.sector,
                **company.metrics
            }
            for company in companies
        }