from pathlib import Path
import sys

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Services
from services.report_service import generate_report


def run_pipeline():

    print("\n" + "=" * 60)
    print("WORKFORCE INTELLIGENCE PLATFORM")
    print("=" * 60)

    try:

        print("\n[1/1] Generating Workforce Report...")
        generate_report()

        print("\n✅ Pipeline Completed Successfully")

    except Exception as e:

        print("\n❌ Pipeline Failed")
        print(e)


if __name__ == "__main__":
    run_pipeline()