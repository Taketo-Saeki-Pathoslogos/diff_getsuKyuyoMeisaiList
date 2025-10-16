# 配列差分比較ツール

`getsuKyuyoResultMeisaiList`の配列を比較して差分を検出し、CSVファイルとHTMLレポートに出力するツールです。

## 概要

beforeとafterにはどちらも、`getsuKyuyoResultMeisaiList`という列が存在します。
`docId`をキーとして行ごとにすり合わせ、配列が一致しているのか、差分としてなっているのかをみてCSVとHTMLに出力します。

## アーキテクチャ

保守性を高くするため、レイヤードアーキテクチャを採用しています。

### ディレクトリ構造
```
src/
├── __init__.py
├── data/                    # データアクセス層
│   ├── __init__.py
│   ├── models.py           # データモデル定義
│   ├── html_models.py      # HTML出力用データモデル
│   ├── csv_reader.py       # CSV読み込み処理
│   └── csv_writer.py       # CSV書き込み処理
├── business/               # ビジネスロジック層
│   ├── __init__.py
│   ├── comparison_service.py  # 比較処理ロジック
│   └── html_report_service.py # HTMLレポート生成サービス
└── presentation/           # プレゼンテーション層
    ├── __init__.py
    ├── array_diff_controller.py  # コントローラー
    └── html_generator.py   # HTML生成器
```

## 使用方法

### 基本的な使用方法
```bash
python main.py source/before_file.csv source/after_file.csv
```

### 出力ディレクトリを指定
```bash
python main.py source/before_file.csv source/after_file.csv custom_output_dir
```

### サマリー表示付き
```bash
python main.py source/before_file.csv source/after_file.csv --summary
```

### HTMLレポート生成
```bash
python main.py source/before_file.csv source/after_file.csv --html --summary
```

### カスタムHTML出力パス指定
```bash
python main.py source/before_file.csv source/after_file.csv --html --html-output custom_report.html
```

## 出力形式

### CSV出力の列構成
- `record_id`: レコードID
- `shainId`: 社員ID
- `shainName`: 社員名
- `keisanNengetsu`: 計算年月
- `shoriNengetsu`: 処理年月
- `kyuyoKomokuCode`: 給与項目コード
- `kyuyoKomokuName`: 給与項目名
- `before_finalValue`, `after_finalValue`, `finalValue_is_match`: finalValueの比較
- `before_kyuyoKomokuCode`, `after_kyuyoKomokuCode`, `kyuyoKomokuCode_is_match`: kyuyoKomokuCodeの比較
- `before_kyuyoKomokuKubun`, `after_kyuyoKomokuKubun`, `kyuyoKomokuKubun_is_match`: kyuyoKomokuKubunの比較
- `before_kyuyoKomokuName`, `after_kyuyoKomokuName`, `kyuyoKomokuName_is_match`: kyuyoKomokuNameの比較
- `before_order`, `after_order`, `order_is_match`: orderの比較
- `before_processValue`, `after_processValue`, `processValue_is_match`: processValueの比較

### HTMLレポートの特徴
- **美しいデザイン**: モダンなCSSデザインで見やすいレポート
- **詳細な情報表示**: 
  - 全体サマリー（総レコード数、総項目数、総不一致数、不一致率）
  - フィールド別不一致数
  - 個別レコードサマリー（不一致があるレコードのみ）
  - 不一致詳細（変更前値・変更後値の比較）
- **レスポンシブデザイン**: モバイルデバイスでも見やすい
- **進捗表示**: 処理の進捗をパーセンテージと経過時間で表示

## 実装の特徴

### 1. レイヤードアーキテクチャ
- **データアクセス層**: CSVファイルの読み書き処理、HTMLデータモデル
- **ビジネスロジック層**: 配列比較のロジック、HTMLレポート生成サービス
- **プレゼンテーション層**: ユーザーインターフェース、HTML生成器

### 2. 型安全性
- `dataclass`を使用したデータモデル定義
- 型ヒントによる型安全性の確保

### 3. エラーハンドリング
- ファイル存在確認
- 適切な例外処理
- ユーザーフレンドリーなエラーメッセージ

### 4. 拡張性
- 新しい比較フィールドの追加が容易
- 異なるデータ形式への対応が可能
- HTMLテンプレートのカスタマイズが可能

## 比較ロジック

### 1. レコードマッチング
- `docId`（record_id）をキーとしてレコードをマッチング

### 2. 項目マッチング
- `kyuyoKomokuCode`をキーとして給与明細項目をマッチング

### 3. 値の比較
- 型を考慮した値の比較（数値、文字列、None）
- 各フィールドの一致/不一致を判定

## コマンドラインオプション

| オプション | 説明 |
|-----------|------|
| `--summary` | 比較結果のサマリーを表示 |
| `--html` | HTMLレポートを生成 |
| `--html-output <path>` | HTML出力ファイルパスを指定（--htmlオプションと併用） |

## テスト

### 手動テスト
```bash
# 既存のファイルでテスト
python main.py source/before_getsuKyuyoMeisai-1760089647.csv source/after_getsuKyuyoMeisai-1760089701.csv --summary --html
```

## 依存関係
- Python 3.7以上
- 標準ライブラリのみ使用（外部依存なし）

## 注意事項
- 入力ファイルはUTF-8エンコーディングである必要があります
- `getsuKyuyoResultMeisaiList`は有効なJSON配列である必要があります
- 大量のデータを処理する場合は、メモリ使用量に注意してください
- HTMLレポートは大量の不一致がある場合、ファイルサイズが大きくなる可能性があります

## 出力例

### コンソール出力例
```
CSVファイルを読み込み中...
変更前レコード数: 581
変更後レコード数: 581
配列差分比較を実行中...
比較結果数: 581
出力進捗: 1/581 (0.2%) - 経過時間: 0.0秒
...
出力進捗: 581/581 (100.0%) - 経過時間: 3.0秒
配列差分比較が完了しました。

=== 比較結果サマリー ===
総レコード数: 581
総項目数: 107,749
総不一致数: 33,694
不一致率: 31.27%

フィールド別不一致数:
  finalValue: 0
  kyuyoKomokuCode: 0
  kyuyoKomokuKubun: 0
  kyuyoKomokuName: 0
  order: 33,694
  processValue: 0

=== HTMLレポート生成 ===
HTMLレポートを生成中...
HTMLレポートを生成しました: DIFF_KYUYOKOMOKU/comparison_report_20251016_122846.html
```

### HTMLレポートの内容
- ヘッダー: ファイル情報と生成日時
- サマリーセクション: 統計情報とフィールド別不一致数
- レコードサマリーセクション: 不一致があるレコードの一覧
- 不一致詳細セクション: 具体的な変更内容の詳細