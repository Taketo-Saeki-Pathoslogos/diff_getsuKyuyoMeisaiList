"""
配列差分比較サービス
"""
from typing import List, Dict, Any, Tuple
from ..data.models import KyuyoRecord, KyuyoMeisaiItem, ComparisonResult


class ComparisonService:
    """配列差分比較サービス"""

    def __init__(self):
        self.comparison_fields = [
            'finalValue',
            'kyuyoKomokuCode', 
            'kyuyoKomokuKubun',
            'kyuyoKomokuName',
            'order',
            'processValue'
        ]

    def compare_records(
        self, 
        before_records: List[KyuyoRecord], 
        after_records: List[KyuyoRecord]
    ) -> List[ComparisonResult]:
        """
        レコードを比較して差分を検出する
        
        Args:
            before_records: 変更前のレコードリスト
            after_records: 変更後のレコードリスト
            
        Returns:
            比較結果のリスト
        """
        # docIdをキーとしてレコードをマッピング
        before_map = {record.record_id: record for record in before_records}
        after_map = {record.record_id: record for record in after_records}
        
        results = []
        
        # 両方のファイルに存在するレコードを比較
        common_ids = set(before_map.keys()) & set(after_map.keys())
        
        for record_id in common_ids:
            before_record = before_map[record_id]
            after_record = after_map[record_id]
            
            comparison_result = self._compare_single_record(
                before_record, after_record
            )
            results.append(comparison_result)
        
        return results

    def _compare_single_record(
        self, 
        before_record: KyuyoRecord, 
        after_record: KyuyoRecord
    ) -> ComparisonResult:
        """
        単一レコードの比較を行う
        
        Args:
            before_record: 変更前のレコード
            after_record: 変更後のレコード
            
        Returns:
            比較結果
        """
        # 給与明細項目を比較
        comparison_details = self._compare_meisai_items(
            before_record.getsu_kyuyo_result_meisai_list,
            after_record.getsu_kyuyo_result_meisai_list
        )
        
        return ComparisonResult(
            record_id=before_record.record_id,
            shain_id=before_record.shain_id,
            shain_name=before_record.shain_name,
            keisan_nengetsu=before_record.keisan_nengetsu,
            shori_nengetsu=before_record.shori_nengetsu,
            before_items=before_record.getsu_kyuyo_result_meisai_list,
            after_items=after_record.getsu_kyuyo_result_meisai_list,
            comparison_details=comparison_details
        )

    def _compare_meisai_items(
        self, 
        before_items: List[KyuyoMeisaiItem], 
        after_items: List[KyuyoMeisaiItem]
    ) -> List[Dict[str, Any]]:
        """
        給与明細項目を比較する
        
        Args:
            before_items: 変更前の項目リスト
            after_items: 変更後の項目リスト
            
        Returns:
            比較詳細のリスト
        """
        # kyuyoKomokuCodeをキーとして項目をマッピング
        before_map = {item.kyuyo_komoku_code: item for item in before_items}
        after_map = {item.kyuyo_komoku_code: item for item in after_items}
        
        comparison_details = []
        
        # 両方に存在する項目を比較
        common_codes = set(before_map.keys()) & set(after_map.keys())
        
        for code in common_codes:
            before_item = before_map[code]
            after_item = after_map[code]
            
            detail = self._create_comparison_detail(before_item, after_item)
            comparison_details.append(detail)
        
        return comparison_details

    def _create_comparison_detail(
        self, 
        before_item: KyuyoMeisaiItem, 
        after_item: KyuyoMeisaiItem
    ) -> Dict[str, Any]:
        """
        比較詳細を作成する
        
        Args:
            before_item: 変更前の項目
            after_item: 変更後の項目
            
        Returns:
            比較詳細の辞書
        """
        detail = {
            'kyuyoKomokuCode': before_item.kyuyo_komoku_code,
            'kyuyoKomokuName': before_item.kyuyo_komoku_name,
        }
        
        # 各フィールドを比較
        for field in self.comparison_fields:
            before_value = getattr(before_item, self._to_snake_case(field))
            after_value = getattr(after_item, self._to_snake_case(field))
            
            # 値を比較（型を考慮）
            is_match = self._compare_values(before_value, after_value)
            
            # 結果を辞書に追加
            detail[f'before_{field}'] = before_value
            detail[f'after_{field}'] = after_value
            detail[f'{field}_is_match'] = is_match
        
        return detail

    def _compare_values(self, value1: Any, value2: Any) -> bool:
        """
        値を比較する（型を考慮）
        
        Args:
            value1: 比較対象の値1
            value2: 比較対象の値2
            
        Returns:
            一致する場合True
        """
        # Noneの場合は両方Noneかチェック
        if value1 is None and value2 is None:
            return True
        if value1 is None or value2 is None:
            return False
        
        # 数値の場合は型を統一して比較
        if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
            return float(value1) == float(value2)
        
        # 文字列の場合は文字列として比較
        return str(value1) == str(value2)

    def _to_snake_case(self, camel_case: str) -> str:
        """
        キャメルケースをスネークケースに変換
        
        Args:
            camel_case: キャメルケースの文字列
            
        Returns:
            スネークケースの文字列
        """
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def generate_comparison_csv_data(
        self, 
        comparison_results: List[ComparisonResult]
    ) -> List[Dict[str, Any]]:
        """
        比較結果をCSV出力用のデータに変換
        
        Args:
            comparison_results: 比較結果のリスト
            
        Returns:
            CSV出力用の辞書リスト
        """
        csv_data = []
        
        for result in comparison_results:
            for detail in result.comparison_details:
                row = {
                    'record_id': result.record_id,
                    'shainId': result.shain_id,
                    'shainName': result.shain_name,
                    'keisanNengetsu': result.keisan_nengetsu,
                    'shoriNengetsu': result.shori_nengetsu,
                    'kyuyoKomokuCode': detail['kyuyoKomokuCode'],
                    'kyuyoKomokuName': detail['kyuyoKomokuName'],
                }
                
                # 各フィールドの比較結果を追加
                for field in self.comparison_fields:
                    row[f'before_{field}'] = detail.get(f'before_{field}', '')
                    row[f'after_{field}'] = detail.get(f'after_{field}', '')
                    row[f'{field}_is_match'] = detail.get(f'{field}_is_match', False)
                
                csv_data.append(row)
        
        return csv_data
