"""
Configuration Center for Supply Chain Analysis
Extracted from working sc_analyzer_new.py and sc_dashboard_new.py
"""
from datetime import datetime

# ============================================================================
# VISUALIZATION COLORS (from sc_dashboard_new.py)
# ============================================================================

COLORS = {
    'Critical': '#dc2626',
    'Severe': '#ea580c',
    'Moderate': '#d97706',
    'Low': '#65a30d',
    'High': '#ef4444'
}

# ============================================================================
# DEFAULT ANALYSIS PARAMETERS (from sc_dashboard_new.py)
# ============================================================================

DEFAULT_TICKERS = "TSM, NVDA, INTC, AMD, QCOM, AVGO, F, GM, TSLA, AAPL, HPQ, DELL, CSCO, TATAMOTORS.NS, MARUTI.NS"

DATE_RANGE = {
    'start': datetime(2019, 1, 1),
    'end': datetime(2023, 12, 31)
}

# ============================================================================
# SECTOR CLASSIFICATIONS (from sc_analyzer_new.py __init__)
# ============================================================================

SECTOR_MAP = {
    'Semiconductors': ['TSM', 'NVDA', 'INTC', 'AMD', 'AVGO', 'ASML', 'QCOM'],
    'Automotive': ['TSLA', 'F', 'GM', 'TM', 'TATAMOTORS.NS', 'MARUTI.NS'],
    'Consumer Electronics': ['AAPL', 'SONY', 'HPQ', 'DELL', 'MSFT'],
    'Telecom_Industrial': ['CSCO', 'ERIC', 'NOK', 'ABB']
}

# ============================================================================
# IMPACT THRESHOLDS (from sc_analyzer_new.py __init__)
# ============================================================================

IMPACT_THRESHOLDS = {
    'Critical': 60,
    'Severe': 40,
    'Moderate': 20,
    'Low': 0
}

# ============================================================================
# DEPENDENCY LEVELS (from sc_analyzer_new.py _get_dependency)
# ============================================================================

SEMICONDUCTOR_DEPENDENCY = {
    'Semiconductors': 'Supplier',
    'Automotive': 'Critical (50-150 chips/vehicle)',
    'Consumer Electronics': 'High (Core component)',
    'Telecom_Industrial': 'Medium (Infrastructure)',
    'Other': 'Low'
}

# ============================================================================
# STRATEGIC RECOMMENDATIONS (from sc_analyzer_new.py _get_recommendation)
# ============================================================================

STRATEGIC_RECOMMENDATIONS = {
    'Automotive': {
        'high': 'Immediate supplier diversification and inventory buildup',
        'medium': 'Diversify suppliers and increase safety stock',
        'low': 'Strengthen existing supplier relationships'
    },
    'Consumer Electronics': {
        'high': 'Increase inventory buffers and dual-source components',
        'medium': 'Optimize component sourcing and increase flexibility',
        'low': 'Maintain current sourcing strategy with monitoring'
    },
    'Semiconductors': {
        'high': 'Expand production capacity and geographic diversification',
        'low': 'Invest in R&D and process optimization'
    },
    'default': {
        'high': 'Review and diversify supply chain dependencies',
        'low': 'Monitor supply chain risks regularly'
    }
}

# ============================================================================
# RISK LEVEL THRESHOLDS (from sc_analyzer_new.py _get_risk_level)
# ============================================================================

RISK_LEVEL_THRESHOLDS = {
    'Extreme': 40,
    'High': 25,
    'Medium': 15,
    'Low': 0
}

# ============================================================================
# RECOVERY TIME ESTIMATES (from sc_analyzer_new.py _estimate_recovery)
# ============================================================================

RECOVERY_TIME_RULES = [
    (50, '3-6 months'),
    (20, '6-12 months'),
    (0, '12-18 months'),
    (float('-inf'), '18+ months')
]