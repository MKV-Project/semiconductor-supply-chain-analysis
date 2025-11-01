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
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    print("=" * 60)
    print("🔗 Supply Chain Resilience Analysis Dashboard")
    print("=" * 60)
    print(f"\nLaunching dashboard from: {src_path}")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        from dashboard.app import main
        main()
    except ImportError:
        from src.dashboard.app import main
        main()

# if __name__ == "__main__":
#     main()
