"""
配列差分比較コントローラー
"""
from typing import List, Dict, Any
from pathlib import Path
import os
import time
from datetime import datetime

from ..data.csv_reader import CsvReader
from ..data.csv_writer import CsvWriter
from ..data.models import KyuyoRecord
from ..business.comparison_service import ComparisonService
from ..business.html_report_service import HtmlReportService
from .html_generator import HtmlGenerator


class ArrayDiffController:
    """配列差分比較コントローラー"""

    def __init__(self):
        self.csv_reader = CsvReader()
        self.csv_writer = CsvWriter()
        self.comparison_service = ComparisonService()
        self.html_report_service = HtmlReportService()
        self.html_generator = HtmlGenerator()

    def process_comparison(
        self, 
        before_file_path: str, 
        after_file_path: str, 
        output_dir: str = "DIFF_KYUYOKOMOKU"
    ) -> List[str]:
        """
        配列差分比較を実行する
        
        Args:
            before_file_path: 変更前のCSVファイルパス
            after_file_path: 変更後のCSVファイルパス
            output_dir: 出力ディレクトリ
            
        Returns:
            出力ファイルのパスのリスト
        """
        try:
            # ファイルの存在確認
            self._validate_input_files(before_file_path, after_file_path)
            
            # CSVファイルを読み込み
            print("CSVファイルを読み込み中...")
            before_records = self.csv_reader.read_csv(before_file_path)
            after_records = self.csv_reader.read_csv(after_file_path)
            
            print(f"変更前レコード数: {len(before_records)}")
            print(f"変更後レコード数: {len(after_records)}")
            
            # 比較処理を実行
            print("配列差分比較を実行中...")
            comparison_results = self.comparison_service.compare_records(
                before_records, after_records
            )
            
            print(f"比較結果数: {len(comparison_results)}")
            
            # レコードごとにCSVファイルを出力
            output_files = []
            total_results = len(comparison_results)
            start_time = time.time()
            
            for i, result in enumerate(comparison_results):
                # CSV出力用データを生成
                csv_data = self.comparison_service.generate_comparison_csv_data([result])
                
                # 出力ファイルパスを生成
                output_file_path = self._generate_output_file_path_for_record(
                    output_dir, result.record_id
                )
                
                # CSVファイルに出力
                self.csv_writer.write_comparison_results(csv_data, output_file_path)
                output_files.append(output_file_path)
                
                # 進捗表示
                current_time = time.time()
                elapsed_time = current_time - start_time
                progress_percentage = ((i + 1) / total_results) * 100
                
                print(f"出力進捗: {i + 1}/{total_results} ({progress_percentage:.1f}%) - 経過時間: {elapsed_time:.1f}秒")
            
            print("配列差分比較が完了しました。")
            return output_files
            
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            raise

    def _validate_input_files(self, before_file_path: str, after_file_path: str) -> None:
        """
        入力ファイルの存在確認
        
        Args:
            before_file_path: 変更前のファイルパス
            after_file_path: 変更後のファイルパス
        """
        if not os.path.exists(before_file_path):
            raise FileNotFoundError(f"変更前ファイルが見つかりません: {before_file_path}")
        
        if not os.path.exists(after_file_path):
            raise FileNotFoundError(f"変更後ファイルが見つかりません: {after_file_path}")

    def _generate_output_file_path_for_record(
        self, 
        output_dir: str, 
        record_id: str
    ) -> str:
        """
        レコード用の出力ファイルパスを生成
        
        Args:
            output_dir: 出力ディレクトリ
            record_id: レコードID
            
        Returns:
            出力ファイルパス
        """
        # 出力ディレクトリを作成
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # ファイル名を生成（record_idを使用）
        filename = f"{record_id}.csv"
        
        return os.path.join(output_dir, filename)

    def get_record_comparison_summary(self, output_file_path: str) -> Dict[str, Any]:
        """
        個別レコードの比較結果サマリーを取得
        
        Args:
            output_file_path: 出力ファイルパス
            
        Returns:
            レコード別サマリー情報
        """
        try:
            csv_data = self.csv_reader.read_csv_as_dict(output_file_path)
            
            if not csv_data:
                return {}
            
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
            
            return {
                'record_id': record_id,
                'shain_id': shain_id,
                'shain_name': shain_name,
                'total_items': total_items,
                'total_mismatches': total_mismatches,
                'field_mismatches': field_mismatches,
                'mismatch_rate': total_mismatches / total_items * 100 if total_items > 0 else 0
            }
            
        except Exception as e:
            print(f"レコードサマリー取得中にエラーが発生しました: {e}")
            return {}

    def get_comparison_summary(self, output_files: List[str]) -> Dict[str, Any]:
        """
        比較結果のサマリーを取得
        
        Args:
            output_files: 出力ファイルパスのリスト
            
        Returns:
            サマリー情報
        """
        try:
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
            
            return {
                'total_records': total_records,
                'total_items': total_items,
                'total_mismatches': total_mismatches,
                'field_mismatches': field_mismatches,
                'mismatch_rate': total_mismatches / total_items * 100 if total_items > 0 else 0
            }
            
        except Exception as e:
            print(f"サマリー取得中にエラーが発生しました: {e}")
            return {}

    def generate_html_report(
        self, 
        output_files: List[str], 
        before_file_path: str, 
        after_file_path: str, 
        html_output_path: str = None
    ) -> str:
        """
        HTMLレポートを生成
        
        Args:
            output_files: 出力ファイルパスのリスト
            before_file_path: 変更前ファイルパス
            after_file_path: 変更後ファイルパス
            html_output_path: HTML出力ファイルパス（指定しない場合は自動生成）
            
        Returns:
            生成されたHTMLファイルのパス
        """
        try:
            # ファイル名を取得
            before_file_name = os.path.basename(before_file_path)
            after_file_name = os.path.basename(after_file_path)
            
            # HTML出力パスを生成（指定されていない場合）
            if html_output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                html_output_path = f"DIFF_KYUYOKOMOKU/comparison_report_{timestamp}.html"
            
            print("HTMLレポートを生成中...")
            
            # HTMLレポートデータを生成
            report_data = self.html_report_service.generate_html_report_data(
                output_files, before_file_name, after_file_name
            )
            
            # HTMLファイルを生成
            html_file_path = self.html_generator.generate_html_report(
                report_data, html_output_path
            )
            
            print(f"HTMLレポートを生成しました: {html_file_path}")
            return html_file_path
            
        except Exception as e:
            print(f"HTMLレポート生成中にエラーが発生しました: {e}")
            raise
