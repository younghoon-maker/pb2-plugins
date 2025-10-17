"""
@CODE:SHEETS-001 | SPEC: SPEC-SHEETS-001.md | TEST: tests/test_loader.py

Google Sheets 데이터 로더
"""

from pathlib import Path
from typing import List, Optional, Any
import re
import tempfile

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


class SheetsLoader:
    """Google Sheets API를 사용한 데이터 로더"""

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
    TAB_NAME = "new_raw"

    def __init__(self, service_account_file: Path) -> None:
        """
        초기화

        Args:
            service_account_file: Service Account JSON 파일 경로

        Raises:
            FileNotFoundError: 파일이 존재하지 않을 경우
        """
        if not service_account_file.exists():
            raise FileNotFoundError(
                f"Service Account 파일을 찾을 수 없습니다: {service_account_file}"
            )

        credentials = service_account.Credentials.from_service_account_file(
            str(service_account_file), scopes=self.SCOPES
        )
        self.service = build("sheets", "v4", credentials=credentials)
        self.drive_service = build("drive", "v3", credentials=credentials)

    def load_row(self, sheet_id: str, row_number: int) -> List[str]:
        """
        단일 행 로드

        Args:
            sheet_id: Google Sheets ID
            row_number: 행 번호 (1-based)

        Returns:
            셀 값 리스트

        Raises:
            HttpError: API 오류 발생 시
        """
        range_name = f"{self.TAB_NAME}!A{row_number}:KN{row_number}"
        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])
        return values[0] if values else []

    def load_rows(
        self, sheet_id: str, start_row: int, end_row: int
    ) -> List[List[str]]:
        """
        여러 행 일괄 로드

        Args:
            sheet_id: Google Sheets ID
            start_row: 시작 행 번호 (1-based, inclusive)
            end_row: 끝 행 번호 (1-based, inclusive)

        Returns:
            행별 셀 값 리스트

        Raises:
            HttpError: API 오류 발생 시
        """
        range_name = f"{self.TAB_NAME}!A{start_row}:KN{end_row}"
        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )
        return result.get("values", [])

    def get_all_product_codes(self, sheet_id: str) -> List[str]:
        """
        시트 A열에서 모든 제품 코드 추출 (헤더 제외)

        Args:
            sheet_id: Google Sheets ID

        Returns:
            제품 코드 리스트 (빈 셀 제외)

        Raises:
            HttpError: API 오류 발생 시
        """
        range_name = f"{self.TAB_NAME}!A2:A1000"  # A2부터 시작 (헤더 제외)
        result = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )

        values = result.get("values", [])
        # 빈 셀 제외, 제품 코드만 반환
        codes = [row[0].strip() for row in values if row and row[0].strip()]
        return codes

    def extract_hyperlinks(
        self, sheet_id: str, row_number: int
    ) -> List[Optional[str]]:
        """
        셀 하이퍼링크 추출

        Args:
            sheet_id: Google Sheets ID
            row_number: 행 번호 (1-based)

        Returns:
            셀별 하이퍼링크 리스트 (없으면 None)

        Raises:
            HttpError: API 오류 발생 시
        """
        # includeGridData=True로 셀 메타데이터 포함
        range_name = f"{self.TAB_NAME}!A{row_number}:KN{row_number}"
        result = (
            self.service.spreadsheets()
            .get(
                spreadsheetId=sheet_id,
                ranges=[range_name],
                includeGridData=True,
            )
            .execute()
        )

        # 첫 번째 시트의 첫 번째 데이터 행 추출
        sheets = result.get("sheets", [])
        if not sheets:
            return []

        row_data = sheets[0].get("data", [{}])[0].get("rowData", [])
        if not row_data:
            return []

        # 각 셀의 hyperlink 추출
        cells = row_data[0].get("values", [])
        return [cell.get("hyperlink") for cell in cells]

    def _extract_drive_file_id(self, drive_url: str) -> Optional[str]:
        """
        Google Drive URL에서 파일 ID 추출

        Args:
            drive_url: Google Drive URL

        Returns:
            파일 ID 또는 None
        """
        patterns = [
            r"drive\.google\.com/file/d/([a-zA-Z0-9_-]+)",
            r"drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)",
            r"id=([a-zA-Z0-9_-]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, drive_url)
            if match:
                return match.group(1)

        return None

    def download_image(
        self, drive_url: str, output_path: Path
    ) -> bool:
        """
        Google Drive에서 이미지 다운로드 (인증된 API 사용)

        Args:
            drive_url: Google Drive URL
            output_path: 저장할 파일 경로

        Returns:
            성공 여부

        Raises:
            Exception: 다운로드 실패 시
        """
        file_id = self._extract_drive_file_id(drive_url)
        if not file_id:
            raise ValueError(f"유효하지 않은 Drive URL: {drive_url}")

        try:
            # Drive API로 파일 다운로드
            request = self.drive_service.files().get_media(fileId=file_id)

            with open(output_path, "wb") as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()

            return True

        except Exception as e:
            raise Exception(f"이미지 다운로드 실패 ({drive_url}): {e}")

    def extract_text_formatting(
        self, sheet_id: str, row_number: int
    ) -> List[Optional[List[dict]]]:
        """
        셀 텍스트 서식 추출 (볼드, 이탤릭 등)

        Args:
            sheet_id: Google Sheets ID
            row_number: 행 번호 (1-based)

        Returns:
            셀별 textFormatRuns 리스트 (없으면 None)
            각 textFormatRun은 {'startIndex': int, 'format': {'bold': bool, 'italic': bool, ...}}

        Raises:
            HttpError: API 오류 발생 시
        """
        # includeGridData=True로 셀 메타데이터 포함
        range_name = f"{self.TAB_NAME}!A{row_number}:KN{row_number}"
        result = (
            self.service.spreadsheets()
            .get(
                spreadsheetId=sheet_id,
                ranges=[range_name],
                includeGridData=True,
            )
            .execute()
        )

        # 첫 번째 시트의 첫 번째 데이터 행 추출
        sheets = result.get("sheets", [])
        if not sheets:
            return []

        row_data = sheets[0].get("data", [{}])[0].get("rowData", [])
        if not row_data:
            return []

        # 각 셀의 textFormatRuns 추출
        cells = row_data[0].get("values", [])
        format_runs = []
        for cell in cells:
            # effectiveValue에서 stringValue 확인 (텍스트 셀만)
            effective_value = cell.get("effectiveValue", {})
            if "stringValue" not in effective_value:
                format_runs.append(None)
                continue

            # textFormatRuns 추출 (없으면 None)
            runs = cell.get("textFormatRuns")
            format_runs.append(runs)

        return format_runs
