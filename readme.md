# Workforce Intelligence Platform

Automated Workforce Intelligence Reporting System built for Wohlig Transformations.

The platform processes workforce allocation data, generates professional HTML/PDF reports, and emails stakeholders automatically.

---

## Features

### Workforce Analytics

* Active Employees
* Project Employees
* Retainer Employees
* Internal Employees
* Multi-Allocated Employees
* Unallocated Employees (Bench)

### Project Allocation Summary

* Project-wise employee allocation
* Employee count per project
* Allocation visibility across teams

### Bench Monitoring

* Unallocated employee list
* Current role
* Reporting manager

### Report Generation

* Professional HTML report
* A4-ready PDF report
* Corporate branding support

### Email Automation

* SMTP-based email delivery
* PDF report attachment
* Environment variable configuration

---

## Project Structure

```text
managin_app/

├── data/
│   ├── Wohlig Active Employee Data.xlsx
│   ├── all_files_extracted_data.json
│   └── processed_workforce_data.json
│
├── img/
│   └── wohlig_logo.webp
│
├── templates/
│   └── workforce_report_template.html
│
├── reports/
│   ├── workforce_report.html
│   └── workforce_report.pdf
│
├── services/
│   ├── report_service.py
│   ├── pdf_service.py
│   └── email_service.py
│
├── Notebooks/
│   ├── 01_extraction.ipynb
│   └── 02_insights.ipynb
│
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## Installation

Clone repository:

```bash
git clone https://github.com/aryangupta-alt/workforce.git

cd workforce
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

Mac/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browser:

```bash
playwright install chromium
```

---

## Environment Variables

Create `.env`

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_TO=recipient@gmail.com
```

---

## Running The Pipeline

```bash
python main.py
```

Pipeline:

```text
Excel Data
      ↓
JSON Processing
      ↓
HTML Report
      ↓
PDF Report
      ↓
Email Delivery
```

---

## Output

Generated Reports:

```text
reports/workforce_report.html
reports/workforce_report.pdf
```

---

## Current Workflow

```text
Workforce Excel
      ↓
Extraction Notebook
      ↓
Processed Workforce JSON
      ↓
HTML Report
      ↓
PDF Report
      ↓
Email Delivery
```

---

## Future Enhancements

* FastAPI Backend
* Next.js Dashboard
* Scheduled Reports
* AI Executive Insights (LLM)
* Google Drive Integration
* Multi-user Reporting
* Report History Tracking

---

## Author

Aryan Gupta

Workforce Intelligence Platform
Wohlig Transformations
