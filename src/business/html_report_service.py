"""
HTMLレポート生成サービス
"""
from typing import List, Dict, Any
from datetime import datetime
import os

from ..data.html_models import (
    HtmlSummaryData, 
    HtmlRecordSummaryData, 
    HtmlMismatchDetailData, 
    HtmlReportData
)
from ..data.csv_reader import CsvReader


class HtmlReportService:
    """HTMLレポート生成サービス"""
    
    def __init__(self):
        self.csv_reader = CsvReader()
    
    def generate_html_report_data(
        self, 
        output_files: List[str], 
        before_file_name: str, 
        after_file_name: str
    ) -> HtmlReportData:
        """
        HTMLレポート用のデータを生成
        
        Args:
            output_files: 出力ファイルパスのリスト
            before_file_name: 変更前ファイル名
            after_file_name: 変更後ファイル名
            
        Returns:
            HTMLレポートデータ
        """
        # サマリーデータを生成
        summary = self._generate_summary_data(output_files)
        
        # レコードサマリーデータを生成
        record_summaries = self._generate_record_summary_data(output_files)
        
        # 不一致詳細データを生成
        mismatch_details = self._generate_mismatch_detail_data(output_files)
        
        return HtmlReportData(
            summary=summary,
            record_summaries=record_summaries,
            mismatch_details=mismatch_details,
            before_file_name=before_file_name,
            after_file_name=after_file_name
        )
    
    def _generate_summary_data(self, output_files: List[str]) -> HtmlSummaryData:
        """サマリーデータを生成"""
        total_records = len(output_files)
        total_items = 0
        total_mismatches = 0
        
        # 各フィールドの不一致数をカウント
        field_mismatches = {}
        comparison_fields = [
            'finalValue', 'kyuyoKomokuCode', 'kyuyoKomokuKubun',
            'kyuyoKomokuName', 'order', 'processValue'
        ]
        
        for field in comparison_fields:
            field_mismatches[field] = 0
        
        # 各レコードファイルを処理
        for output_file in output_files:
            try:
                csv_data = self.csv_reader.read_csv_as_dict(output_file)
                total_items += len(csv_data)
                
                for record in csv_data:
                    for field in comparison_fields:
                        is_match_key = f"{field}_is_match"
                        if is_match_key in record:
                            # CSVから読み込まれた値は文字列なので、適切に変換
                            is_match_value = record[is_match_key]
                            if isinstance(is_match_value, str):
                                is_match = is_match_value.lower() == 'true'
                            else:
                                is_match = bool(is_match_value)
                            
                            if not is_match:
                                field_mismatches[field] += 1
                                total_mismatches += 1
            except Exception as e:
                print(f"ファイル {output_file} の処理中にエラー: {e}")
                continue
        
        return HtmlSummaryData(
            total_records=total_records,
            total_items=total_items,
            total_mismatches=total_mismatches,
            mismatch_rate=total_mismatches / total_items * 100 if total_items > 0 else 0,
            field_mismatches=field_mismatches,
            generated_at=datetime.now()
        )
    
    def _generate_record_summary_data(self, output_files: List[str]) -> List[HtmlRecordSummaryData]:
        """レコードサマリーデータを生成"""
        record_summaries = []
        
        for output_file in output_files:
            try:
                csv_data = self.csv_reader.read_csv_as_dict(output_file)
                
                if not csv_data:
                    continue
                
                record_id = csv_data[0]['record_id']
                shain_id = csv_data[0]['shainId']
                shain_name = csv_data[0]['shainName']
                
                total_items = len(csv_data)
                total_mismatches = 0
                
                # 各フィールドの不一致数をカウント
                field_mismatches = {}
                comparison_fields = [
                    'finalValue', 'kyuyoKomokuCode', 'kyuyoKomokuKubun',
                    'kyuyoKomokuName', 'order', 'processValue'
                ]
                
                for field in comparison_fields:
                    field_mismatches[field] = 0
                
                for record in csv_data:
                    for field in comparison_fields:
                        is_match_key = f"{field}_is_match"
                        if is_match_key in record:
                            # CSVから読み込まれた値は文字列なので、適切に変換
                            is_match_value = record[is_match_key]
                            if isinstance(is_match_value, str):
                                is_match = is_match_value.lower() == 'true'
                            else:
                                is_match = bool(is_match_value)
                            
                            if not is_match:
                                field_mismatches[field] += 1
                                total_mismatches += 1
                
                # 不一致があるレコードのみ追加
                if total_mismatches > 0:
                    record_summaries.append(HtmlRecordSummaryData(
                        record_id=record_id,
                        shain_id=shain_id,
                        shain_name=shain_name,
                        total_items=total_items,
                        total_mismatches=total_mismatches,
                        mismatch_rate=total_mismatches / total_items * 100 if total_items > 0 else 0,
                        field_mismatches=field_mismatches
                    ))
            except Exception as e:
                print(f"ファイル {output_file} の処理中にエラー: {e}")
                continue
        
        return record_summaries
    
    def _generate_mismatch_detail_data(self, output_files: List[str]) -> List[HtmlMismatchDetailData]:
        """不一致詳細データを生成"""
        mismatch_details = []
        
        for output_file in output_files:
            try:
                csv_data = self.csv_reader.read_csv_as_dict(output_file)
                
                if not csv_data:
                    continue
                
                record_id = csv_data[0]['record_id']
                shain_id = csv_data[0]['shainId']
                shain_name = csv_data[0]['shainName']
                
                comparison_fields = [
                    'finalValue', 'kyuyoKomokuCode', 'kyuyoKomokuKubun',
                    'kyuyoKomokuName', 'order', 'processValue'
                ]
                
                for record in csv_data:
                    kyuyo_komoku_code = record.get('kyuyoKomokuCode', '')
                    kyuyo_komoku_name = record.get('kyuyoKomokuName', '')
                    
                    for field in comparison_fields:
                        is_match_key = f"{field}_is_match"
                        before_key = f"before_{field}"
                        after_key = f"after_{field}"
                        
                        if is_match_key in record and before_key in record and after_key in record:
                            # CSVから読み込まれた値は文字列なので、適切に変換
                            is_match_value = record[is_match_key]
                            if isinstance(is_match_value, str):
                                is_match = is_match_value.lower() == 'true'
                            else:
                                is_match = bool(is_match_value)
                            
                            if not is_match:
                                mismatch_details.append(HtmlMismatchDetailData(
                                    record_id=record_id,
                                    shain_id=shain_id,
                                    shain_name=shain_name,
                                    kyuyo_komoku_code=kyuyo_komoku_code,
                                    kyuyo_komoku_name=kyuyo_komoku_name,
                                    field_name=field,
                                    before_value=record[before_key],
                                    after_value=record[after_key],
                                    is_match=is_match
                                ))
            except Exception as e:
                print(f"ファイル {output_file} の処理中にエラー: {e}")
                continue
        
        return mismatch_details
