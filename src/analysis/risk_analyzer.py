"""
Risk Analyzer
Handles risk assessment using Isolation Forest
Extracted from sc_analyzer_new.py
"""
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Dict

class RiskAnalyzer:
    """Analyze company risks using machine learning"""
    
    def __init__(self):
        pass
    
    def analyze_risk(self, companies: List, threshold: float = 0.3) -> Dict[str, Dict]:
        """
        Analyze company risks using Isolation Forest
        Extracted from SCAnalyzer._analyze_risk
        
        Args:
            companies: List of CompanyData objects
            threshold: Risk detection sensitivity (0.1-0.5)
            
        Returns:
            Dictionary of risk assessments by ticker
        """
        if len(companies) < 3:
            return {}
        
        # Prepare feature matrix
        features = []
        valid_companies = []
        
        for company in companies:
            vol = company.metrics['volatility']
            dd = abs(company.metrics['drawdown'])
            
            if not np.isnan([vol, dd]).any():
                features.append([vol, dd])
                valid_companies.append(company)
        
        if len(features) < 3:
            return {}
        
        # Run isolation forest
        detector = IsolationForest(
            contamination=min(threshold, 0.5),
            random_state=42
        )
        scores = detector.fit_predict(np.array(features))
        
        return {
            company.ticker: {
                'name': company.name,
                'sector': company.sector,
                'score': 'High' if score == -1 else 'Low'
            }
            for company, score in zip(valid_companies, scores)
        }