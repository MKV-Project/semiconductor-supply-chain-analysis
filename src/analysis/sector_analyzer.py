"""
Sector Analyzer
Handles sector-level vulnerability analysis
Extracted from sc_analyzer_new.py
"""
import numpy as np
from typing import List, Dict
import sys
sys.path.append('..')
from config import IMPACT_THRESHOLDS, RISK_LEVEL_THRESHOLDS

class SectorAnalyzer:
    """Analyze sector vulnerabilities"""
    
    def __init__(self):
        self._impact_thresholds = IMPACT_THRESHOLDS
        self._risk_thresholds = RISK_LEVEL_THRESHOLDS
    
    def analyze_sectors(self, companies: List) -> List[Dict]:
        """
        Analyze sector vulnerabilities
        Extracted from SCAnalyzer._analyze_sectors
        
        Args:
            companies: List of CompanyData objects
            
        Returns:
            List of sector vulnerability dictionaries
        """
        sector_data = {}
        
        for company in companies:
            if company.sector not in sector_data:
                sector_data[company.sector] = {
                    'impacts': [],
                    'returns': [],
                    'companies': 0,
                    'critical': 0,
                    'severe': 0
                }
            
            data = sector_data[company.sector]
            impact = abs(company.metrics['drawdown'])
            
            data['impacts'].append(impact)
            data['returns'].append(company.metrics['return'])
            data['companies'] += 1
            
            if impact >= self._impact_thresholds['Critical']:
                data['critical'] += 1
            elif impact >= self._impact_thresholds['Severe']:
                data['severe'] += 1
        
        return [
            {
                'Sector': sector,
                'Companies_Analyzed': data['companies'],
                'Avg_Financial_Impact_pct': round(np.mean(data['impacts']), 1),
                'Avg_Return_Pct': round(np.mean(data['returns']), 1),
                'Critical_Impact_Companies': data['critical'],
                'Severe_Impact_Companies': data['severe'],
                'Supply_Chain_Risk_Level': self._get_risk_level(np.mean(data['impacts']))
            }
            for sector, data in sector_data.items()
        ]
    
    def _get_risk_level(self, impact: float) -> str:
        """
        Get sector risk level
        Extracted from SCAnalyzer._get_risk_level
        """
        for level, threshold in self._risk_thresholds.items():
            if impact >= threshold:
                return level
        return 'Low'