import os
import json
import re
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "all_files_extracted_data.json"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "workforce_analysis_output.json"
)

MODEL_NAME = "gemma4:31b-cloud"


_api_key = os.environ.get('OLLAMA_API_KEY') or ""
if not _api_key:
    print("[WARNING] OLLAMA_API_KEY is not set. Requests will likely fail with 401.")

client = Client(
    host="https://ollama.com",
    headers={'Authorization': f'Bearer {_api_key}'}
)
# ==========================================


def load_input_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}. Please ensure the file exists.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: {filepath} is not valid JSON.")
        exit(1)


# def build_prompt(json_data):
#     data_string = json.dumps(json_data, indent=2)

#     prompt = f"""
# You are an Expert HR & Project Allocation Auditor. I am providing you with the complete extracted JSON data from a Workforce system.

# Your objective is to reconcile this data by applying a strict, step-by-step logical thinking process. You MUST build the lists first, apply role filters, resolve typos and ghost employees, filter inactive projects, check for multi-allocations, and then calculate accurate final totals.

# ### ROBUST LOGICAL THINKING FRAMEWORK:
# You MUST follow this exact sequence in your `step_by_step_reasoning` section:

# * **Step 1: Master Employee Extraction & Role Filtering:**
#   Scan the Active, Retainer, and Internal sheets. Extract all employee names.
#   CRITICAL RULE: You MUST include employees whose role contains "Intern".
#   You MUST EXCLUDE any employee whose role contains "Tech Lead".
#   Deduplicate this master list so no name appears more than once.
#   Log every exclusion in `audit_logs`.

# * **Step 2: Ghost & Typo Resolution:**
#   Map all names from project sheets back against the Step 1 filtered master list.
#   Resolve typos (e.g., "Apollo Hispital" -> "Apollo Hospital").
#   Identify ghost employees (appear in project sheets but not in the master list) and discard them.
#   Resolve empty rows in the Active sheet by assigning the project data to the last named employee above them.

# * **Step 3: Status Filtering:**
#   Check the "Status" column for ALL Projects, Retainers, and Internal tasks.
#   If the Status is "Done", "Closed", or "Finished", completely EXCLUDE that entry from active arrays.
#   Track excluded entries in `workforce_overview.completed_project_names` and `closed_project_names`.

# * **Step 4: Build Active Allocation Lists:**
#   Construct final arrays for active `projects`, `retainers`, and `internal` tasks — containing only entries with active statuses and valid (non-Tech-Lead, non-ghost) employees.
#   Additionally, compile a unified `active_projects_table` that consolidates all three types into a single flat list with a `project_type` field for each entry.

# * **Step 5: Build Unallocated List:**
#   Build the complete list of `unallocated_employees` — those in the Active sheet with an empty project, "No Task", or "Bench".
#   Apply the Tech Lead exclusion rule here as well.

# * **Step 6: Multi-Allocation Cross-Check (CRITICAL):**
#   Scan every employee name inside your finalized active `projects`, `retainers`, and `internal` lists.
#   If an employee appears MORE THAN ONCE across these lists combined (e.g., in a Retainer AND an Internal task), they are multi-allocated.
#   List their names and all the projects they appear in. State the exact total count.

# * **Step 7: Calculate Final Totals:**
#   Sum all counts strictly from the arrays generated above.
#   `total_multi_allocated_employees` MUST equal the count from Step 6.
#   `total_filtered_employees` MUST equal the count from the deduplicated Step 1 master list.

# ### CORE AUDIT RULES:
# - The "Active Employee" data is the absolute source of truth.
# - Tech Leads MUST be excluded from ALL final employee counts, project assignments, and unallocated lists.
# - Interns are explicitly treated as active employees and must be included.
# - Projects with "Done" or "Closed" Status must ONLY appear in completed/closed counters — NOT in any active allocation array.

# ### REQUIRED JSON OUTPUT SCHEMA:
# Return ONLY a valid JSON object matching the exact structure below. No markdown, no extra text.

# {{
#   "step_by_step_reasoning": {{
#     "step_1_extraction_and_role_filtering": "Detail the extraction, inclusion of Interns, explicit exclusion of Tech Leads, and deduplication.",
#     "step_2_ghosts_and_typos": "Describe typo fixes, ghost removals, and empty row resolutions.",
#     "step_3_status_filtering": "List all projects/retainers/internal tasks marked Done or Closed that are excluded.",
#     "step_4_build_active_allocations": "Confirm the active projects, retainers, internal tasks, and the unified active_projects_table.",
#     "step_5_build_unallocated": "List all unallocated employees (after Tech Lead exclusion). State the total count.",
#     "step_6_multi_allocation_cross_check": "List every employee appearing in more than one active list, and which lists. State the exact count.",
#     "step_7_calculate_totals": "Show the arithmetic for all totals. Confirm multi-allocated and filtered totals match Steps 6 and 1."
#   }},
#   "active_employees_filtered_list": ["string"],
#   "unallocated_employees": [
#     {{
#       "name": "string",
#       "current_role": "string",
#       "reporting_to": "string"
#     }}
#   ],
#   "project_allocations": {{
#     "projects": [
#       {{ "project_name": "string", "employee_count": 0, "employees": ["string"] }}
#     ],
#     "retainers": [
#       {{ "project_name": "string", "employee_count": 0, "employees": ["string"] }}
#     ],
#     "internal": [
#       {{ "project_name": "string", "employee_count": 0, "employees": ["string"] }}
#     ]
#   }},
#   "active_projects_table": [
#     {{
#       "project_name": "string",
#       "project_type": "Project | Retainer | Internal",
#       "status": "string",
#       "employee_count": 0,
#       "employees": ["string"]
#     }}
#   ],
#   "workforce_overview": {{
#     "total_filtered_employees": 0,
#     "total_unallocated_employees": 0,
#     "total_multi_allocated_employees": 0,
#     "multi_allocated_names": ["string"],
#     "total_active_projects": 0,
#     "total_project_type_employees": 0,
#     "total_retainer_type_employees": 0,
#     "total_internal_type_employees": 0,
#     "completed_projects_count": 0,
#     "completed_project_names": ["string"],
#     "closed_projects_count": 0,
#     "closed_project_names": ["string"]
#   }},
#   "audit_logs": [
#     "string (e.g., 'ROLE FILTER: Excluded [Name] — role is Tech Lead.' or 'MULTI-ALLOCATION: [Name] found in both Retainers and Internal.')"
#   ]
# }}

# ### DATA INPUT (JSON format):
# {data_string}
# """
#     return prompt

def build_prompt(json_data):
    data_string = json.dumps(json_data, indent=2)

    prompt = f"""
You are an Expert HR & Project Allocation Auditor. I am providing you with the complete extracted JSON data from a Workforce system.

Your objective is to reconcile this data by applying a strict, step-by-step logical thinking process. You MUST build the lists first, apply role filters, resolve typos and ghost employees, filter inactive projects, check for multi-allocations, and then calculate accurate final totals.

### ROBUST LOGICAL THINKING FRAMEWORK:
You MUST follow this exact sequence in your `step_by_step_reasoning` section:

* **Step 1: Master Employee Extraction & Role Filtering:**
  Scan the Active, Retainer, and Internal sheets. Extract all employee names.
  CRITICAL RULE: You MUST include employees whose role contains "Intern".
  You MUST include employees whose role contains "Tech Lead" in this master list.
  Deduplicate this master list so no name appears more than once.

* **Step 2: Ghost & Typo Resolution:**
  Map all names from project sheets back against the Step 1 filtered master list.
  Resolve typos (e.g., "Apollo Hispital" -> "Apollo Hospital").
  Identify ghost employees (appear in project sheets but not in the master list) and discard them.
  Resolve empty rows in the Active sheet by assigning the project data to the last named employee above them.

* **Step 3: Status Filtering:**
  Check the "Status" column for ALL Projects, Retainers, and Internal tasks.
  If the Status is "Done", "Closed", or "Finished", completely EXCLUDE that entry from active arrays.
  Track excluded entries in `workforce_overview.completed_project_names` and `closed_project_names`.

* **Step 4: Build Active Allocation Lists:**
  Construct final arrays for active `projects`, `retainers`, and `internal` tasks — containing only entries with active statuses and valid (non-ghost) employees.
  Additionally, compile a unified `active_projects_table` that consolidates all three types into a single flat list with a `project_type` field for each entry.

* **Step 5: Build Unallocated List:**
  Build the complete list of `unallocated_employees` — those in the Active sheet with an empty project, "No Task", or "Bench".
  CRITICAL RULE: You MUST EXCLUDE any employee whose role contains "Tech Lead" from this unallocated list.
  Log every such exclusion in `audit_logs`.

* **Step 6: Multi-Allocation Cross-Check (CRITICAL):**
  Scan every employee name inside your finalized active `projects`, `retainers`, and `internal` lists.
  If an employee appears MORE THAN ONCE across these lists combined (e.g., in a Retainer AND an Internal task), they are multi-allocated.
  List their names and all the projects they appear in. State the exact total count.

* **Step 7: Calculate Final Totals:**
  Sum all counts strictly from the arrays generated above.
  `total_multi_allocated_employees` MUST equal the count from Step 6.
  `total_filtered_employees` MUST equal the count from the deduplicated Step 1 master list.

### CORE AUDIT RULES:
- The "Active Employee" data is the absolute source of truth.
- Tech Leads MUST be excluded ONLY from the `unallocated_employees` list. They remain in all other counts and project assignments.
- Interns are explicitly treated as active employees and must be included.
- Projects with "Done" or "Closed" Status must ONLY appear in completed/closed counters — NOT in any active allocation array.

### REQUIRED JSON OUTPUT SCHEMA:
Return ONLY a valid JSON object matching the exact structure below. No markdown, no extra text.

{{
  "step_by_step_reasoning": {{
    "step_1_extraction_and_role_filtering": "Detail the extraction, inclusion of Interns, inclusion of Tech Leads in the master list, and deduplication.",
    "step_2_ghosts_and_typos": "Describe typo fixes, ghost removals, and empty row resolutions.",
    "step_3_status_filtering": "List all projects/retainers/internal tasks marked Done or Closed that are excluded.",
    "step_4_build_active_allocations": "Confirm the active projects, retainers, internal tasks, and the unified active_projects_table.",
    "step_5_build_unallocated": "List all unallocated employees (after Tech Lead exclusion). State the total count.",
    "step_6_multi_allocation_cross_check": "List every employee appearing in more than one active list, and which lists. State the exact count.",
    "step_7_calculate_totals": "Show the arithmetic for all totals. Confirm multi-allocated and filtered totals match Steps 6 and 1."
  }},
  "active_employees_filtered_list": ["string"],
  "unallocated_employees": [
    {{
      "name": "string",
      "current_role": "string",
      "reporting_to": "string"
    }}
  ],
  "project_allocations": {{
    "projects": [
      {{ "project_name": "string", "employee_count": 0, "employees": ["string"] }}
    ],
    "retainers": [
      {{ "project_name": "string", "employee_count": 0, "employees": ["string"] }}
    ],
    "internal": [
      {{ "project_name": "string", "employee_count": 0, "employees": ["string"] }}
    ]
  }},
  "active_projects_table": [
    {{
      "project_name": "string",
      "project_type": "Project | Retainer | Internal",
      "status": "string",
      "employee_count": 0,
      "employees": ["string"]
    }}
  ],
  "workforce_overview": {{
    "total_filtered_employees": 0,
    "total_unallocated_employees": 0,
    "total_multi_allocated_employees": 0,
    "multi_allocated_names": ["string"],
    "total_active_projects": 0,
    "total_project_type_employees": 0,
    "total_retainer_type_employees": 0,
    "total_internal_type_employees": 0,
    "completed_projects_count": 0,
    "completed_project_names": ["string"],
    "closed_projects_count": 0,
    "closed_project_names": ["string"]
  }},
  "audit_logs": [
    "string (e.g., 'ROLE FILTER: Excluded [Name] from unallocated — role is Tech Lead.' or 'MULTI-ALLOCATION: [Name] found in both Retainers and Internal.')"
  ]
}}

### DATA INPUT (JSON format):
{data_string}
"""
    return prompt


def extract_json_from_response(response_text):
    match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if match:
        return match.group(0)
    return response_text


def analyze_workforce():
    print("Loading extracted JSON data...")
    input_data = load_input_data(INPUT_FILE)

    prompt = build_prompt(input_data)

    print(f"Sending data to {MODEL_NAME} via configured Cloud Client...")
    print("Applying Role Filters (Excluding Tech Leads, Including Interns)...")
    print("Executing Deep Cross-Check for Multi-Allocated Employees...")

    try:
        response = client.generate(
            model=MODEL_NAME,
            prompt=prompt,
            format='json',
            options={
                'temperature': 0.1
            }
        )

        result_text = response.get('response', '')

        clean_json_string = extract_json_from_response(result_text)
        parsed_json = json.loads(clean_json_string)

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(parsed_json, f, indent=2)

        print(f"Success! Full audit report saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"An error occurred during API execution: {e}")
    return OUTPUT_FILE


if __name__ == "__main__":
    analyze_workforce()