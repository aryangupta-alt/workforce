import json
from pathlib import Path
from datetime import datetime
from jinja2 import Template


# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

JSON_FILE = BASE_DIR / "data" / "workforce_analysis_output.json"
TEMPLATE_FILE = BASE_DIR / "templates" / "workforce_report_template.html"
OUTPUT_FILE = BASE_DIR / "reports" / "workforce_report.html"


# ── Report generation ──────────────────────────────────────────────────────
def generate_report() -> None:

    # 1. Load data
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Build structure expected by HTML
    overview = {

        "active_employees":
            data["workforce_overview"]["total_filtered_employees"],

        "current_projects":
            data["workforce_overview"]["total_active_projects"],

        "unallocated_employees":
            data["workforce_overview"]["total_unallocated_employees"],

        "project_distribution": {

            "client_projects": {
                "count": len(data["project_allocations"]["projects"]),
                "projects": [
                    p["project_name"]
                    for p in data["project_allocations"]["projects"]
                ]
            },

            "retainer_projects": {
                "count": len(data["project_allocations"]["retainers"]),
                "projects": [
                    p["project_name"]
                    for p in data["project_allocations"]["retainers"]
                ]
            },

            "internal_projects": {
                "count": len(data["project_allocations"]["internal"]),
                "projects": [
                    p["project_name"]
                    for p in data["project_allocations"]["internal"]
                ]
            }
        }
    }

    project_allocation_summary = data["active_projects_table"]

    unallocated_employee_list = data["unallocated_employees"]

    generated_date = datetime.now().strftime("%d %B %Y")

    # 2. Load Jinja2 template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = Template(f.read())

    # 3. Render
    html = template.render(
        workforce=overview,
        project_allocation_summary=project_allocation_summary,
        unallocated_employee_list=unallocated_employee_list,
        generated_date=generated_date,
        logo_path="../img/64e32576ae89c46bfb5ed1c3_wohlighighres.webp",
    )

    # 4. Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report generated: {OUTPUT_FILE}")


# ── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    generate_report()