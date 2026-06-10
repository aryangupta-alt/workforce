import json
from pathlib import Path
from datetime import datetime
from jinja2 import Template


# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).resolve().parent.parent

JSON_FILE     = BASE_DIR / "data"      / "processed_workforce_data.json"
TEMPLATE_FILE = BASE_DIR / "templates" / "workforce_report_template.html"
OUTPUT_FILE   = BASE_DIR / "reports"   / "workforce_report.html"


# ── Utilization calculation ─────────────────────────────────────────────────
def calculate_utilization(data: dict) -> float:
    """
    Utilization % = (active_employees - unallocated_employees)
                    / active_employees * 100
    """
    total = data["workforce_overview"]["active_employees"]
    bench = data["workforce_overview"]["unallocated_employees"]
    return round(((total - bench) / total) * 100, 1)


# ── Report generation ────────────────────────────────────────────────────────
def generate_report() -> None:

    # 1. Load data
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    overview     = data["workforce_overview"]
    utilization  = calculate_utilization(data)
    generated_date = datetime.now().strftime("%d %B %Y")

    # 2. Load Jinja2 template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = Template(f.read())

    # 3. Render
    html = template.render(
        workforce                  = overview,
        project_allocation_summary = data["project_allocation_summary"],
        unallocated_employee_list  = data["unallocated_employee_list"],
        generated_date             = generated_date,
        utilization_percentage     = utilization,
        logo_path                  = "../img/64e32576ae89c46bfb5ed1c3_wohlighighres.webp",
    )

    # 4. Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report generated: {OUTPUT_FILE}")


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    generate_report()