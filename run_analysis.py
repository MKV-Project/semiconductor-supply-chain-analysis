"""
CLI Entry Point for Supply Chain Analysis
Run this file to launch the Streamlit dashboard
"""
import subprocess
import sys
from pathlib import Path

def main():
    # """Launch Streamlit dashboard"""
    # dashboard_path = Path(__file__).parent / "src" / "dashboard" / "app.py"
    
    # print("=" * 60)
    # print("🔗 Supply Chain Resilience Analysis Dashboard")
    # print("=" * 60)
    # print(f"\nLaunching dashboard from: {dashboard_path}")
    # print("\nPress Ctrl+C to stop the server\n")
    
    # try:
    #     subprocess.run([
    #         sys.executable,
    #         "-m",
    #         "streamlit",
    #         "run",
    #         str(dashboard_path),
    #         "--server.port=8501",
    #         "--server.headless=true"
    #     ])
    # except KeyboardInterrupt:
    #     print("\n\n✅ Dashboard stopped")
    # except Exception as e:
    #     print(f"\n❌ Error launching dashboard: {e}")
    #     print("\nTry running directly:")
    #     print(f"  streamlit run {dashboard_path}")

    dashboard_path = Path(__file__).parent / "src" / "dashboard" / "app.py"
    sys.argv = ["streamlit", "run", str(dashboard_path)]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
