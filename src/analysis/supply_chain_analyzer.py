"""
Supply Chain Analyzer
Handles supply chain impact assessment and resilience scoring
Extracted from sc_analyzer_new.py
"""
from typing import List, Dict
import sys
sys.path.append('..')
from config import (
    SEMICONDUCTOR_DEPENDENCY,
    IMPACT_THRESHOLDS,
    STRATEGIC_RECOMMENDATIONS,
    RECOVERY_TIME_RULES
)

class SupplyChainAnalyzer:
    """Analyze supply chain impacts and resilience"""
    
    def __init__(self):
        self._dependency_map = SEMICONDUCTOR_DEPENDENCY
        self._impact_thresholds = IMPACT_THRESHOLDS
        self._recommendations = STRATEGIC_RECOMMENDATIONS
        self._recovery_rules = RECOVERY_TIME_RULES
    
    def analyze_supply_chain(self, companies: List) -> List[Dict]:
        """
        Analyze supply chain impacts
        Extracted from SCAnalyzer._analyze_supply_chain
        
        Args:
            companies: List of CompanyData objects
            
        Returns:
            List of supply chain impact dictionaries
        """
        return [
            {
                'Company': company.name,
                'Ticker': company.ticker,
                'Sector': company.sector,
                'Semiconductor_Dependency': self._get_dependency(company.sector),
                'Financial_Impact_pct': abs(company.metrics['drawdown']),
                'Impact_Severity': self._get_severity(abs(company.metrics['drawdown'])),
                'Estimated_Recovery_Months': self._estimate_recovery(
                    company.metrics['return'],
                    company.metrics['volatility']
                ),
                'Supply_Chain_Resilience': self._calculate_resilience(
                    company.metrics['return'],
                    company.metrics['drawdown']
                ),
                'Strategic_Recommendation': self._get_recommendation(
                    company.sector,
                    abs(company.metrics['drawdown'])
                )
            }
            for company in companies
        ]
    
    def _get_dependency(self, sector: str) -> str:
        """
        Get sector dependency level
        Extracted from SCAnalyzer._get_dependency
        """
        return self._dependency_map.get(sector, 'Low')
    
    def _get_severity(self, impact: float) -> str:
        """
        Get impact severity level
        Extracted from SCAnalyzer._get_severity
        """
        for severity, threshold in self._impact_thresholds.items():
            if impact >= threshold:
                return severity
        return 'Low'
    
    def _estimate_recovery(self, returns: float, volatility: float) -> str:
        """
        Estimate recovery time
        Extracted from SCAnalyzer._estimate_recovery
        """
        for threshold, recovery_time in self._recovery_rules:
            if returns > threshold:
                return recovery_time
        return '18+ months'
    
    def _calculate_resilience(self, returns: float, drawdown: float) -> float:
        """
        Calculate resilience score (0-100)
        Extracted from SCAnalyzer._calculate_resilience
        """
        base = 50
        return_boost = max(0, returns * 0.5)
        drawdown_penalty = min(40, abs(drawdown) * 0.8)
        return round(max(0, min(100, base + return_boost - drawdown_penalty)), 1)
    
    def _get_recommendation(self, sector: str, impact: float) -> str:
        """
        Get strategic recommendation
        Extracted from SCAnalyzer._get_recommendation
        """
        sector_recs = self._recommendations.get(
            sector, 
            self._recommendations['default']
        )
        
        if impact >= 45:
            return sector_recs.get('high', sector_recs.get('low', 'Monitor supply chain risks'))
        elif impact >= 25:
            return sector_recs.get('medium', sector_recs.get('low', 'Monitor supply chain risks'))
        return sector_recs.get('low', 'Monitor supply chain risks')