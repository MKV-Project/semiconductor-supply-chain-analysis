# 🔗 Semiconductor Supply Chain Resilience Analysis

**MBA Data Science & Analytics Project**  
*Analysis of 2020-2021 semiconductor shortage impact on industry stock performance*

---

## 📋 Project Overview

This project analyzes how the 2020-2021 semiconductor supply shortage affected stock market performance across semiconductor-dependent industries and characterizes recovery patterns.

### Key Features
- ✅ Real-time stock data fetching via Yahoo Finance API
- ✅ Machine learning risk detection using Isolation Forest
- ✅ Interactive Streamlit dashboard with Plotly visualizations
- ✅ Multi-sector correlation analysis
- ✅ Supply chain resilience scoring
- ✅ Excel/CSV export capabilities

---

## 📁 Project Structure

```
semiconductor-supply-chain-analysis/
│
├── config.py                          # Configuration & constants
├── requirements.txt                   # Python dependencies
├── run_analysis.py                    # CLI entry point
├── README.md                          # This file
│
├── src/
│   ├── analysis/                      # Analysis modules
│   │   ├── __init__.py
│   │   ├── performance_analyzer.py    # Stock data & metrics
│   │   ├── risk_analyzer.py           # Risk assessment
│   │   ├── supply_chain_analyzer.py   # Impact analysis
│   │   ├── sector_analyzer.py         # Sector metrics
│   │   └── time_series_analyzer.py    # Recovery patterns
│   │
│   └── dashboard/                     # Visualization modules
│       ├── __init__.py
│       ├── app.py                     # Main Streamlit app
│       ├── chart_factory.py           # Plotly templates
│       ├── dashboard_components.py    # UI components
│       └── export_utils.py            # Export functionality
│
└── outputs/                           # Generated reports
    ├── reports/
    └── screenshots/
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone <repository-url>
cd semiconductor-supply-chain-analysis

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Dashboard

**Option A: Using run script**
```bash
python run_analysis.py
```

**Option B: Direct Streamlit**
```bash
streamlit run src/dashboard/app.py
```

### 3. Access Dashboard
Open browser to: `http://localhost:8501`

---

## 📊 Usage Guide

### Default Analysis
1. Launch dashboard
2. Default tickers and date range pre-loaded
3. Click **"Run Analysis"**
4. View results in tabs:
   - **Summary**: Key metrics & trends
   - **Performance**: Returns & volatility
   - **Risk**: Correlation analysis
   - **Supply Chain**: Impact assessment
   - **Recommendations**: Strategic actions

### Custom Analysis
1. Modify ticker list in sidebar
2. Adjust date range (2019-2024 recommended)
3. Set risk sensitivity (0.1-0.5)
4. Run analysis

### Export Results
- **Excel**: All sheets consolidated
- **CSV**: Individual datasets
- Download from sidebar after analysis

---

## 🔬 Methodology

### Data Sources
- **Stock Data**: Yahoo Finance API
- **Period**: January 2019 - December 2024
- **Companies**: 50+ across 5 sectors

### Analysis Techniques
1. **Time-Series Analysis**: Price trends, volatility patterns
2. **Correlation Analysis**: Sector relationships (Pearson coefficient)
3. **Risk Detection**: Isolation Forest (anomaly detection)
4. **Recovery Metrics**: Time-to-recovery, resilience scoring

### Sectors Analyzed
- Semiconductors (suppliers)
- Automotive (high dependency)
- Consumer Electronics (moderate dependency)
- Telecom/Industrial (low dependency)
- Other

---

## 📈 Key Findings

### Impact Severity (2020-2021)
- **Automotive**: 82% avg drawdown, 14-15 month recovery
- **Consumer Electronics**: 79% avg drawdown, 8-10 month recovery
- **Semiconductors**: 84% avg drawdown, 5-6 month recovery

### Risk Factors
- Just-in-time inventory vulnerability
- Supplier concentration risk
- Geographic dependency (Taiwan)

### Resilience Drivers
- Supplier diversification
- Safety stock levels
- Design flexibility
- Production redundancy

---

## 🛠️ Technical Details

### Architecture
- **Modular Design**: Separate analysis & visualization layers
- **Caching**: LRU cache for API calls
- **Error Handling**: Robust exception management
- **Data Validation**: Missing data & outlier detection

### Key Technologies
- **Python 3.8+**
- **Streamlit**: Interactive dashboards
- **Plotly**: Visualizations
- **yfinance**: Stock data
- **scikit-learn**: ML models
- **pandas/numpy**: Data processing

---

## ⚠️ Limitations

- Stock prices reflect multiple factors (not just semiconductors)
- Large-cap companies only (data availability)
- Historical event specificity (2020-2021)
- Time-series correlation ≠ causation


## 🙏 Acknowledgments

- Yahoo Finance for data access
- Streamlit/Plotly for visualization frameworks
- HITS Faculty for guidance
- Open-source community

---

## 📞 Support

For technical issues:
1. Check `requirements.txt` versions
2. Verify Yahoo Finance API access
3. Ensure Python 3.8+ installed
4. Review error logs in terminal

---

**Last Updated**: November 2025  
**Version**: 1.0.0