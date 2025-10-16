"""
データモデル定義
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import json


@dataclass
class KyuyoMeisaiItem:
    """給与明細項目"""
    final_value: Any
    kyuyo_komoku_code: str
    kyuyo_komoku_kubun: str
    kyuyo_komoku_name: str
    order: int
    process_value: Any

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KyuyoMeisaiItem':
        """辞書からインスタンスを作成"""
        return cls(
            final_value=data.get('finalValue'),
            kyuyo_komoku_code=data.get('kyuyoKomokuCode', ''),
            kyuyo_komoku_kubun=data.get('kyuyoKomokuKubun', ''),
            kyuyo_komoku_name=data.get('kyuyoKomokuName', ''),
            order=data.get('order', 0),
            process_value=data.get('processValue')
        )

    def to_dict(self) -> Dict[str, Any]:
        """辞書に変換"""
        return {
            'finalValue': self.final_value,
            'kyuyoKomokuCode': self.kyuyo_komoku_code,
            'kyuyoKomokuKubun': self.kyuyo_komoku_kubun,
            'kyuyoKomokuName': self.kyuyo_komoku_name,
            'order': self.order,
            'processValue': self.process_value
        }


@dataclass
class KyuyoRecord:
    """給与レコード"""
    record_id: str
    shain_id: str
    shain_name: str
    keisan_nengetsu: str
    shori_nengetsu: str
    getsu_kyuyo_result_meisai_list: List[KyuyoMeisaiItem]

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> 'KyuyoRecord':
        """CSV行からインスタンスを作成"""
        # getsuKyuyoResultMeisaiListをJSONとしてパース
        meisai_list_json = row.get('getsuKyuyoResultMeisaiList', '[]')
        try:
            meisai_list_data = json.loads(meisai_list_json)
            meisai_list = [KyuyoMeisaiItem.from_dict(item) for item in meisai_list_data]
        except (json.JSONDecodeError, TypeError):
            meisai_list = []

        return cls(
            record_id=row.get('__id__', ''),
            shain_id=row.get('shainId', ''),
            shain_name=row.get('shainName', ''),
            keisan_nengetsu=row.get('keisanNengetsu', ''),
            shori_nengetsu=row.get('shoriNengetsu', ''),
            getsu_kyuyo_result_meisai_list=meisai_list
        )


@dataclass
class ComparisonResult:
    """比較結果"""
    record_id: str
    shain_id: str
    shain_name: str
    keisan_nengetsu: str
    shori_nengetsu: str
    before_items: List[KyuyoMeisaiItem]
    after_items: List[KyuyoMeisaiItem]
    comparison_details: List[Dict[str, Any]]

    def to_csv_row(self) -> Dict[str, Any]:
        """CSV行に変換"""
        row = {
            'record_id': self.record_id,
            'shainId': self.shain_id,
            'shainName': self.shain_name,
            'keisanNengetsu': self.keisan_nengetsu,
            'shoriNengetsu': self.shori_nengetsu,
            'kyuyoKomokuCode': '',
            'kyuyoKomokuName': '',
        }

        # 各項目の比較結果を追加
        for detail in self.comparison_details:
            for key, value in detail.items():
                row[key] = value

        return row
