#!/usr/bin/env python3
"""
配列差分比較ツール - メインスクリプト

使用方法:
    python main.py <before_file> <after_file> [output_dir]

例:
    python main.py source/before_getsuKyuyoMeisai-1760089647.csv source/after_getsuKyuyoMeisai-1760089701.csv
"""
import sys
import argparse
from pathlib import Path

from src.presentation.array_diff_controller import ArrayDiffController


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description='配列差分比較ツール - getsuKyuyoResultMeisaiListの配列を比較して差分を検出します'
    )
    parser.add_argument(
        'before_file', 
        help='変更前のCSVファイルパス'
    )
    parser.add_argument(
        'after_file', 
        help='変更後のCSVファイルパス'
    )
    parser.add_argument(
        'output_dir', 
        nargs='?', 
        default='DIFF_KYUYOKOMOKU',
        help='出力ディレクトリ（デフォルト: DIFF_KYUYOKOMOKU）'
    )
    parser.add_argument(
        '--summary', 
        action='store_true',
        help='比較結果のサマリーを表示'
    )
    parser.add_argument(
        '--html', 
        action='store_true',
        help='HTMLレポートを生成'
    )
    parser.add_argument(
        '--html-output', 
        type=str,
        help='HTML出力ファイルパス（--htmlオプションと併用）'
    )

    args = parser.parse_args()

    try:
        # コントローラーを初期化
        controller = ArrayDiffController()
        
        # 配列差分比較を実行
        output_files = controller.process_comparison(
            args.before_file, 
            args.after_file, 
            args.output_dir
        )
        
        print(f"\n出力ファイル数: {len(output_files)}")
        print("出力ファイル一覧:")
        for i, file_path in enumerate(output_files[:10]):  # 最初の10個のみ表示
            print(f"  {i+1}. {file_path}")
        if len(output_files) > 10:
            print(f"  ... 他 {len(output_files) - 10} ファイル")
        
        # サマリーを表示
        if args.summary:
            print("\n=== 比較結果サマリー ===")
            summary = controller.get_comparison_summary(output_files)
            if summary:
                print(f"総レコード数: {summary['total_records']}")
                print(f"総項目数: {summary['total_items']}")
                print(f"総不一致数: {summary['total_mismatches']}")
                print(f"不一致率: {summary['mismatch_rate']:.2f}%")
                print("\nフィールド別不一致数:")
                for field, count in summary['field_mismatches'].items():
                    print(f"  {field}: {count}")
            
            # 個別レコードのサマリーを表示（不一致があるレコードのみ）
            print("\n=== 個別レコードサマリー（不一致があるレコードのみ） ===")
            mismatch_records = []
            for output_file in output_files:
                record_summary = controller.get_record_comparison_summary(output_file)
                if record_summary and record_summary['total_mismatches'] > 0:
                    mismatch_records.append(record_summary)
            
            if mismatch_records:
                print(f"不一致があるレコード数: {len(mismatch_records)}")
                for i, record in enumerate(mismatch_records[:10]):  # 最初の10個のみ表示
                    print(f"\n{i+1}. レコードID: {record['record_id']}")
                    print(f"   社員ID: {record['shain_id']}")
                    print(f"   社員名: {record['shain_name']}")
                    print(f"   項目数: {record['total_items']}")
                    print(f"   不一致数: {record['total_mismatches']}")
                    print(f"   不一致率: {record['mismatch_rate']:.2f}%")
                    print("   フィールド別不一致数:")
                    for field, count in record['field_mismatches'].items():
                        if count > 0:
                            print(f"     {field}: {count}")
                
                if len(mismatch_records) > 10:
                    print(f"\n... 他 {len(mismatch_records) - 10} レコード")
            else:
                print("不一致があるレコードはありません。")
        
        # HTMLレポートを生成
        if args.html:
            print("\n=== HTMLレポート生成 ===")
            html_file_path = controller.generate_html_report(
                output_files, 
                args.before_file, 
                args.after_file, 
                args.html_output
            )
            print(f"HTMLレポート: {html_file_path}")
        
        print("\n処理が完了しました。")
        
    except FileNotFoundError as e:
        print(f"エラー: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
