from fastapi import APIRouter

from services.drive_service import fetch_latest_workbook
from services.extraction_service import extract_workforce_data
from services.llm_analysis_service import analyze_workforce
from services.report_service import generate_report
from services.pdf_service import generate_pdf
from services.email_service import send_report

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


@router.get("/health")
def health():

    return {
        "status": "ok"
    }


@router.post("/generate")
def generate():

    fetch_latest_workbook()

    extract_workforce_data()

    analyze_workforce()

    generate_report()

    return {
        "status": "success",
        "message": "HTML report generated successfully"
    }


@router.post("/send")
def send():

    generate_pdf()

    send_report()

    return {
        "status": "success",
        "message": "Email sent successfully"
    }