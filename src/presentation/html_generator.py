"""
HTMLレポート生成器
"""
from typing import List
from pathlib import Path
import os

from ..data.html_models import HtmlReportData


class HtmlGenerator:
    """HTMLレポート生成器"""
    
    def generate_html_report(self, report_data: HtmlReportData, output_path: str) -> str:
        """
        HTMLレポートを生成
        
        Args:
            report_data: HTMLレポートデータ
            output_path: 出力ファイルパス
            
        Returns:
            生成されたHTMLファイルのパス
        """
        # 出力ディレクトリを作成
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # HTMLコンテンツを生成
        html_content = self._generate_html_content(report_data)
        
        # ファイルに書き込み
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _generate_html_content(self, report_data: HtmlReportData) -> str:
        """HTMLコンテンツを生成"""
        return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>配列差分比較レポート</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>配列差分比較レポート</h1>
            <div class="file-info">
                <p><strong>変更前ファイル:</strong> {report_data.before_file_name}</p>
                <p><strong>変更後ファイル:</strong> {report_data.after_file_name}</p>
                <p><strong>生成日時:</strong> {report_data.summary.generated_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </header>

        <main>
            {self._generate_summary_section(report_data.summary)}
            {self._generate_record_summary_section(report_data.record_summaries)}
            {self._generate_mismatch_detail_section(report_data.mismatch_details)}
        </main>
    </div>
</body>
</html>"""
    
    def _get_css_styles(self) -> str:
        """CSSスタイルを取得"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .file-info {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 8px;
        }
        
        .file-info p {
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .summary-section, .record-summary-section, .mismatch-detail-section {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .section-title {
            font-size: 1.8em;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .summary-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #3498db;
        }
        
        .summary-card h3 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        .summary-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #e74c3c;
        }
        
        .field-mismatches {
            background: #fff3cd;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
        }
        
        .field-mismatches h4 {
            color: #856404;
            margin-bottom: 15px;
        }
        
        .field-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }
        
        .field-item {
            background: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            border: 1px solid #ffc107;
        }
        
        .field-item .field-name {
            font-weight: bold;
            color: #856404;
        }
        
        .field-item .field-count {
            font-size: 1.2em;
            color: #e74c3c;
            margin-top: 5px;
        }
        
        .record-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .record-table th,
        .record-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        .record-table th {
            background-color: #f8f9fa;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .record-table tr:hover {
            background-color: #f5f5f5;
        }
        
        .mismatch-count {
            font-weight: bold;
            color: #e74c3c;
        }
        
        .mismatch-rate {
            color: #e74c3c;
            font-weight: bold;
        }
        
        .mismatch-detail-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .mismatch-detail-table th,
        .mismatch-detail-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
            font-size: 0.9em;
        }
        
        .mismatch-detail-table th {
            background-color: #f8f9fa;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .mismatch-detail-table tr:hover {
            background-color: #f5f5f5;
        }
        
        .before-value {
            color: #e74c3c;
            font-weight: bold;
        }
        
        .after-value {
            color: #27ae60;
            font-weight: bold;
        }
        
        .no-data {
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
            padding: 40px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            header h1 {
                font-size: 2em;
            }
            
            .summary-grid {
                grid-template-columns: 1fr;
            }
            
            .field-list {
                grid-template-columns: 1fr;
            }
            
            .record-table,
            .mismatch-detail-table {
                font-size: 0.8em;
            }
        }
        """
    
    def _generate_summary_section(self, summary) -> str:
        """サマリーセクションを生成"""
        return f"""
        <section class="summary-section">
            <h2 class="section-title">比較結果サマリー</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>総レコード数</h3>
                    <div class="value">{summary.total_records:,}</div>
                </div>
                <div class="summary-card">
                    <h3>総項目数</h3>
                    <div class="value">{summary.total_items:,}</div>
                </div>
                <div class="summary-card">
                    <h3>総不一致数</h3>
                    <div class="value">{summary.total_mismatches:,}</div>
                </div>
                <div class="summary-card">
                    <h3>不一致率</h3>
                    <div class="value">{summary.mismatch_rate:.2f}%</div>
                </div>
            </div>
            
            <div class="field-mismatches">
                <h4>フィールド別不一致数</h4>
                <div class="field-list">
                    {self._generate_field_mismatch_items(summary.field_mismatches)}
                </div>
            </div>
        </section>
        """
    
    def _generate_field_mismatch_items(self, field_mismatches) -> str:
        """フィールド不一致アイテムを生成"""
        items = []
        for field, count in field_mismatches.items():
            items.append(f"""
                <div class="field-item">
                    <div class="field-name">{field}</div>
                    <div class="field-count">{count:,}</div>
                </div>
            """)
        return ''.join(items)
    
    def _generate_record_summary_section(self, record_summaries) -> str:
        """レコードサマリーセクションを生成"""
        if not record_summaries:
            return """
            <section class="record-summary-section">
                <h2 class="section-title">個別レコードサマリー</h2>
                <div class="no-data">不一致があるレコードはありません。</div>
            </section>
            """
        
        return f"""
        <section class="record-summary-section">
            <h2 class="section-title">個別レコードサマリー（不一致があるレコードのみ）</h2>
            <p>不一致があるレコード数: <strong>{len(record_summaries)}</strong></p>
            <table class="record-table">
                <thead>
                    <tr>
                        <th>レコードID</th>
                        <th>社員ID</th>
                        <th>社員名</th>
                        <th>項目数</th>
                        <th>不一致数</th>
                        <th>不一致率</th>
                        <th>フィールド別不一致数</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_record_summary_rows(record_summaries)}
                </tbody>
            </table>
        </section>
        """
    
    def _generate_record_summary_rows(self, record_summaries) -> str:
        """レコードサマリー行を生成"""
        rows = []
        for record in record_summaries:
            field_mismatch_text = ', '.join([f"{field}: {count}" for field, count in record.field_mismatches.items() if count > 0])
            rows.append(f"""
                <tr>
                    <td>{record.record_id}</td>
                    <td>{record.shain_id}</td>
                    <td>{record.shain_name}</td>
                    <td>{record.total_items:,}</td>
                    <td class="mismatch-count">{record.total_mismatches:,}</td>
                    <td class="mismatch-rate">{record.mismatch_rate:.2f}%</td>
                    <td>{field_mismatch_text}</td>
                </tr>
            """)
        return ''.join(rows)
    
    def _generate_mismatch_detail_section(self, mismatch_details) -> str:
        """不一致詳細セクションを生成"""
        if not mismatch_details:
            return """
            <section class="mismatch-detail-section">
                <h2 class="section-title">不一致詳細</h2>
                <div class="no-data">不一致はありません。</div>
            </section>
            """
        
        return f"""
        <section class="mismatch-detail-section">
            <h2 class="section-title">不一致詳細</h2>
            <p>総不一致数: <strong>{len(mismatch_details)}</strong></p>
            <table class="mismatch-detail-table">
                <thead>
                    <tr>
                        <th>レコードID</th>
                        <th>社員ID</th>
                        <th>社員名</th>
                        <th>給与項目コード</th>
                        <th>給与項目名</th>
                        <th>フィールド名</th>
                        <th>変更前値</th>
                        <th>変更後値</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_mismatch_detail_rows(mismatch_details)}
                </tbody>
            </table>
        </section>
        """
    
    def _generate_mismatch_detail_rows(self, mismatch_details) -> str:
        """不一致詳細行を生成"""
        rows = []
        for detail in mismatch_details:
            rows.append(f"""
                <tr>
                    <td>{detail.record_id}</td>
                    <td>{detail.shain_id}</td>
                    <td>{detail.shain_name}</td>
                    <td>{detail.kyuyo_komoku_code}</td>
                    <td>{detail.kyuyo_komoku_name}</td>
                    <td>{detail.field_name}</td>
                    <td class="before-value">{detail.before_value}</td>
                    <td class="after-value">{detail.after_value}</td>
                </tr>
            """)
        return ''.join(rows)
