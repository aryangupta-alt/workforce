from pathlib import Path
import sys

# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# ============================================================
# SERVICES
# ============================================================

from services.report_service import generate_report
from services.pdf_service import generate_pdf
from services.email_service import send_report

# ============================================================
# PIPELINE
# ============================================================

def run_pipeline():

    print("\n" + "=" * 60)
    print("WORKFORCE INTELLIGENCE PLATFORM")
    print("=" * 60)

    try:

        # ----------------------------------------------------
        # STEP 1: Generate HTML Report
        # ----------------------------------------------------
        print("\n[1/3] Generating HTML Report...")
        generate_report()

        # ----------------------------------------------------
        # STEP 2: Generate PDF
        # ----------------------------------------------------
        print("\n[2/3] Generating PDF Report...")
        generate_pdf()

        # ----------------------------------------------------
        # STEP 3: Send Email
        # ----------------------------------------------------
        print("\n[3/3] Sending Email...")
        send_report()

        print("\n✅ Pipeline Completed Successfully")

    except Exception as e:

        print("\n❌ Pipeline Failed")
        print(f"Error: {e}")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_pipeline()