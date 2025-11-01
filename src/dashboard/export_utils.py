"""
Export Utilities
Handles Excel and CSV export functionality
Extracted from sc_dashboard_new.py
"""
import pandas as pd
from io import BytesIO
from typing import Dict, Optional

class ExportUtils:
    """Handle data export operations"""
    
    @staticmethod
    def create_excel_export(results: Dict) -> Optional[BytesIO]:
        """
        Create consolidated Excel export
        Extracted from sc_dashboard_new.py create_excel_export
        """
        try:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                sheets = {
                    'Analysis_Metadata': lambda: pd.DataFrame([results['metadata']]),
                    'Performance_Analysis': lambda: pd.DataFrame(results['performance']).T.reset_index(),
                    'Risk_Assessment': lambda: pd.DataFrame(results['risk']).T.reset_index(),
                    'Supply_Chain_Impact': lambda: pd.DataFrame(results['supply_chain_impact']),
                    'Sector_Vulnerability': lambda: pd.DataFrame(results['sector_vulnerability']),
                    'Analysis_Summary': lambda: pd.DataFrame([ExportUtils._create_analysis_summary(results)])
                }
                
                for sheet_name, data_func in sheets.items():
                    try:
                        df = data_func()
                        if isinstance(df, pd.DataFrame) and not df.empty:
                            if 'index' in df.columns:
                                df.columns = ['Ticker' if c == 'index' else c for c in df.columns]
                            df.to_excel(writer, sheet_name=sheet_name, index=False)
                    except Exception as e:
                        print(f"Skipping {sheet_name}: {str(e)}")
            
            output.seek(0)
            return output
        except Exception as e:
            print(f"Error creating Excel file: {str(e)}")
            return None
    
    @staticmethod
    def _create_analysis_summary(results: Dict) -> Dict:
        """
        Create analysis summary
        Extracted from sc_dashboard_new.py create_analysis_summary
        """
        summary = {
            'total_companies_analyzed': len(results.get('companies', [])),
            'analysis_period': results.get('metadata', {}).get('period', 'N/A'),
            'analysis_date': results.get('metadata', {}).get('analysis_date', 'N/A')
        }
        
        if sc_data := results.get('supply_chain_impact'):
            df = pd.DataFrame(sc_data)
            summary.update({f'{k}_companies': v for k, v in df['Sector'].value_counts().items()})
            
        if risk_data := results.get('risk'):
            risk_dist = pd.DataFrame(risk_data).T['score'].value_counts()
            summary.update({f'risk_{k.lower()}': v for k, v in risk_dist.items()})
        
        return summary