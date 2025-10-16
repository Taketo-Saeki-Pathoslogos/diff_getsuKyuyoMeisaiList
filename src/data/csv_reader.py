"""
CSVファイル読み込み処理
"""
import csv
from typing import List, Dict, Any
from pathlib import Path
from .models import KyuyoRecord


class CsvReader:
    """CSVファイル読み込みクラス"""

    @staticmethod
    def read_csv(file_path: str) -> List[KyuyoRecord]:
        """
        CSVファイルを読み込んでKyuyoRecordのリストを返す
        
        Args:
            file_path: CSVファイルのパス
            
        Returns:
            KyuyoRecordのリスト
        """
        records = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    record = KyuyoRecord.from_csv_row(row)
                    records.append(record)
        except FileNotFoundError:
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        except Exception as e:
            raise Exception(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        
        return records

    @staticmethod
    def read_csv_as_dict(file_path: str) -> List[Dict[str, Any]]:
        """
        CSVファイルを辞書のリストとして読み込む
        
        Args:
            file_path: CSVファイルのパス
            
        Returns:
            辞書のリスト
        """
        records = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    records.append(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        except Exception as e:
            raise Exception(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        
        return records
