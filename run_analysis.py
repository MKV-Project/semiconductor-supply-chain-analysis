"""
CLI Entry Point for Supply Chain Analysis
Run this file to launch the Streamlit dashboard
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Launch Streamlit dashboard directly without subprocess"""
    
    # Add src to Python path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    print("=" * 60)
    print("🔗 Supply Chain Resilience Analysis Dashboard")
    print("=" * 60)
    print(f"\nLaunching dashboard from: {src_path}")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Import and run the actual Streamlit app directly
        from dashboard.app import main as dashboard_main
        
        # Set Streamlit config for cloud deployment
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
        
        # Run the actual dashboard
        dashboard_main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nTrying alternative import...")
        try:
            from src.dashboard.app import main as dashboard_main
            dashboard_main()
        except ImportError as e2:
            print(f"❌ Alternative import failed: {e2}")
            print("\nAvailable paths:")
            for path in sys.path:
                print(f"  - {path}")
                
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        print("\nTry running directly with: streamlit run src/dashboard/app.py")

if __name__ == "__main__":
    main()
