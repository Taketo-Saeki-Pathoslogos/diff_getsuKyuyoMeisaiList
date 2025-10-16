"""
CSVファイル書き込み処理
"""
import csv
from typing import List, Dict, Any
from pathlib import Path


class CsvWriter:
    """CSVファイル書き込みクラス"""

    @staticmethod
    def write_comparison_results(
        results: List[Dict[str, Any]], 
        output_path: str
    ) -> None:
        """
        比較結果をCSVファイルに書き込む
        
        Args:
            results: 比較結果の辞書リスト
            output_path: 出力ファイルのパス
        """
        if not results:
            return

        # 出力ディレクトリを作成
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as file:
                # ヘッダーを取得
                fieldnames = results[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # ヘッダーを書き込み
                writer.writeheader()
                
                # データを書き込み
                for result in results:
                    writer.writerow(result)
        except Exception as e:
            raise Exception(f"CSVファイルの書き込み中にエラーが発生しました: {e}")

    @staticmethod
    def write_kyuyo_records(
        records: List[Dict[str, Any]], 
        output_path: str
    ) -> None:
        """
        給与レコードをCSVファイルに書き込む
        
        Args:
            records: 給与レコードの辞書リスト
            output_path: 出力ファイルのパス
        """
        if not records:
            return

        # 出力ディレクトリを作成
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as file:
                # ヘッダーを取得
                fieldnames = records[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # ヘッダーを書き込み
                writer.writeheader()
                
                # データを書き込み
                for record in records:
                    writer.writerow(record)
        except Exception as e:
            raise Exception(f"CSVファイルの書き込み中にエラーが発生しました: {e}")
