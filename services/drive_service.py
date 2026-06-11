from pathlib import Path
import io

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload


BASE_DIR = Path(__file__).resolve().parent.parent

SERVICE_ACCOUNT_FILE = (
    BASE_DIR /"config" / "google_service_account.json"
)

DOWNLOAD_FOLDER = BASE_DIR / "data"

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]

FILE_ID = "1EAGD1LreF9KF3kSyqsOTSinmo9iSEDWn"


def authenticate_drive():

    creds = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_FILE),
        scopes=SCOPES
    )

    return build(
        "drive",
        "v3",
        credentials=creds
    )


def download_file_from_drive(
    service,
    file_id,
    output_path
):

    request = service.files().get_media(
        fileId=file_id
    )

    fh = io.FileIO(
        output_path,
        "wb"
    )

    downloader = MediaIoBaseDownload(
        fh,
        request
    )

    done = False

    while not done:

        status, done = downloader.next_chunk()

        print(
            f"Download {int(status.progress() * 100)}%"
        )

    return output_path


def fetch_latest_workbook():

    DOWNLOAD_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    drive_service = authenticate_drive()

    local_file_path = (
        DOWNLOAD_FOLDER
        / "Wohlig Active Employee Data.xlsx"
    )

    download_file_from_drive(
        drive_service,
        FILE_ID,
        local_file_path
    )

    print(
        f"Workbook downloaded: {local_file_path}"
    )

    return local_file_path


if __name__ == "__main__":

    fetch_latest_workbook()