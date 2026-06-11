import os
import smtplib

from pathlib import Path
from dotenv import load_dotenv

from email.message import EmailMessage

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_FILE = BASE_DIR / "reports" / "workforce_report.pdf"


def send_report():

    msg = EmailMessage()

    msg["Subject"] = "Workforce Intelligence Report"

    msg["From"] = os.getenv("EMAIL_USER")

    msg["To"] = os.getenv("EMAIL_TO")

    msg.set_content(
        "Please find attached the latest Workforce Intelligence Report."
    )

    with open(PDF_FILE, "rb") as f:

        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="workforce_report.pdf"
        )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            os.getenv("EMAIL_USER"),
            os.getenv("EMAIL_PASSWORD")
        )

        smtp.send_message(msg)

    print("Email Sent Successfully")