from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent

HTML_FILE = BASE_DIR / "reports" / "workforce_report.html"
PDF_FILE = BASE_DIR / "reports" / "workforce_report.pdf"


def generate_pdf():

    if not HTML_FILE.exists():
        raise FileNotFoundError(
            f"HTML report not found: {HTML_FILE}"
        )

    with sync_playwright() as p:

        browser = p.chromium.launch()

        page = browser.new_page()

        page.goto(
            f"file://{HTML_FILE.resolve()}",
            wait_until="networkidle"
        )

        page.pdf(
            path=str(PDF_FILE),
            format="A4",
            print_background=True,
            margin={
                "top": "10mm",
                "bottom": "10mm",
                "left": "10mm",
                "right": "10mm",
            }
        )

        browser.close()

    print(f"PDF generated: {PDF_FILE}")

if __name__ == "__main__":
    generate_pdf()