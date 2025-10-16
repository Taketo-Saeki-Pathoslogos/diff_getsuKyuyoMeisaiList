"""
HTML出力用のデータモデル
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class HtmlSummaryData:
    """HTMLサマリーデータ"""
    total_records: int
    total_items: int
    total_mismatches: int
    mismatch_rate: float
    field_mismatches: Dict[str, int]
    generated_at: datetime


@dataclass
class HtmlRecordSummaryData:
    """HTMLレコードサマリーデータ"""
    record_id: str
    shain_id: str
    shain_name: str
    total_items: int
    total_mismatches: int
    mismatch_rate: float
    field_mismatches: Dict[str, int]


@dataclass
class HtmlMismatchDetailData:
    """HTML不一致詳細データ"""
    record_id: str
    shain_id: str
    shain_name: str
    kyuyo_komoku_code: str
    kyuyo_komoku_name: str
    field_name: str
    before_value: Any
    after_value: Any
    is_match: bool


@dataclass
class HtmlReportData:
    """HTMLレポート全体データ"""
    summary: HtmlSummaryData
    record_summaries: List[HtmlRecordSummaryData]
    mismatch_details: List[HtmlMismatchDetailData]
    before_file_name: str
    after_file_name: str
