# offering_finder プロジェクト概要

## プロジェクトの目的
AWS Reserved Instance (RI) および Savings Plans の Offering ID を検索し、購入コマンドを生成するCLIツール

## 対応サービス
- Amazon RDS
- Amazon ElastiCache
- AWS Savings Plans
- Amazon OpenSearch

## 技術スタック
- **言語**: Python 3.13+
- **パッケージマネージャ**: uv
- **主要ライブラリ**:
  - boto3 (AWS SDK)
  - click (CLI フレームワーク)
  - pydantic (データバリデーション)
  - pytest (テストフレームワーク)

## プロジェクト構造

```
offering_finder/
├── cli.py                  # エントリーポイント（CLIグループの定義）
├── mycli/                  # CLIサブコマンド実装
│   ├── rds.py             # RDS コマンド
│   ├── elasticache.py     # ElastiCache コマンド
│   ├── savingsplans.py    # Savings Plans コマンド
│   └── opensearch.py      # OpenSearch コマンド
├── src/offering_finder/    # コアロジック
│   ├── clients/           # AWS クライアントラッパー
│   │   └── AWSClient.py   # 統一された AWS API クライアント
│   ├── managers/          # ビジネスロジック層
│   │   ├── rds_manager.py
│   │   ├── elasticache_manager.py
│   │   ├── savingsplans_manager.py
│   │   └── opensearch_manager.py
│   └── models/            # Pydantic データモデル
│       ├── rds_params.py
│       ├── elasticache_params.py
│       ├── savingsplans_params.py
│       └── opensearch_params.py
└── tests/                 # テストコード
    └── test_elasticache_manager.py
```

## アーキテクチャパターン

### レイヤー構造
1. **CLI層** (`mycli/`): ユーザーインターフェース、引数パース
2. **Manager層** (`managers/`): ビジネスロジック、データ加工
3. **Client層** (`clients/`): AWS API呼び出しのラッパー
4. **Model層** (`models/`): データバリデーションとスキーマ定義

### データフロー
```
CLI (click) → Manager → AWSClient → boto3 → AWS API
                ↓
            Pydantic Model (バリデーション)
```

## 主要機能

### 1. Offering検索
- AWS各サービスのReserved Instanceオファリングを検索
- フィルタリング条件:
  - リージョン
  - インスタンスタイプ/クラス
  - 期間（1年/3年）
  - 支払いオプション（All Upfront/Partial Upfront/No Upfront）
  - 数量

### 2. 購入コマンド生成
- 検索結果から自動的にAWS CLI購入コマンドを生成
- プロファイル指定に対応
- 見積金額の自動計算

### 3. 出力形式
- JSON形式での結果出力
- タイムスタンプ付き
- 注文数量と見積金額を含む

## 使用例

### RDS Reserved Instance検索
```bash
uv run cli.py rds \
  --region_name 'ap-northeast-1' \
  --product_description 'MySQL' \
  --db_instance_class 'db.m5.large' \
  --duration 31536000 \
  --quantity 2 \
  --offering_type 'All Upfront'
```

### 出力例（RDS）
```json
[
  {
    "ReservedDBInstancesOfferingId": "xxx-xxx-xxx",
    "DBInstanceClass": "db.m5.large",
    "Duration": 31536000,
    "FixedPrice": 1234.56,
    "OrderQuantity": 2,
    "OrderEstimatedAmount": 2469.12,
    "Timestamp": "2025-01-17T12:34:56.789Z",
    "PurchaseCommand": "aws rds purchase-reserved-db-instances-offering ..."
  }
]
```

## コード設計の特徴

### 1. 統一されたクライアント設計
`AWSClient`クラスが複数のAWSサービスAPIを統一的に扱う：
- `describe_offerings()` メソッドで各サービスに応じたAPI呼び出しを自動切り替え
- サービス判定は `client.meta.service_model.service_name` を使用

### 2. Pydanticによるバリデーション
- 各サービスのパラメータを型安全に管理
- `model_dump(exclude_none=True)` でNoneを除外してAPI呼び出し
- API仕様とのマッピングを明確化

### 3. ページネーション対応
RDSManagerの例：
```python
while True:
    response = self.client.describe_offerings(rds_params)
    offerings = response.get("ReservedDBInstancesOfferings", [])
    result.extend(offerings)
    if "Marker" in response:
        rds_params["Marker"] = response["Marker"]
    else:
        break
```

## 開発状態

### 実装済み
- ✅ RDS Offering検索・購入コマンド生成
- ✅ ElastiCache Offering検索・購入コマンド生成
- ✅ Savings Plans Offering検索
- ✅ OpenSearch Offering検索・購入コマンド生成
- ✅ CLI インターフェース
- ✅ Pydantic モデル定義
- ✅ AWSClient 統一ラッパー

### テスト状況
- ✅ RDS Manager のテストコードあり (`test_rds_manager.py`)
- ✅ ElastiCache Manager のテストコードあり (`test_elasticache_manager.py`)
- ✅ Savings Plans Manager のテストコードあり (`test_savingsplans_manager.py`)
- ✅ OpenSearch Manager のテストコードあり (`test_opensearch_manager.py`)
- ✅ AWSClient のテストコードあり (`test_awsclient.py`)
- ✅ 全31テストがパス

### 既知の問題・改善点

#### 1. ~~RDSManager のバグ~~ ✅ 解決済み
~~ループ内でreturnしているため、最初の1件しか処理されない問題~~

**解決**: PR #4 ([0756509](https://github.com/0xmks/offering_finder/commit/0756509)) で修正済み

#### 2. ~~テストカバレッジ不足~~ ✅ 解決済み
~~RDS Manager、Savings Plans Manager、OpenSearch Manager、AWSClientのテストが未実装~~

**解決**: PR #5 ([976ac07](https://github.com/0xmks/offering_finder/commit/976ac07)) で全Managerのユニットテストを追加
- 全31テストがパス
- AWS公式ドキュメントに基づくテストデータを使用
- モックを使用してAWS APIに依存しないテスト

#### 3. エラーハンドリング
- 現状はログ出力のみ
- ユーザーへのエラーメッセージが不明瞭
- CLI層でのエラーハンドリングが未実装

#### 4. ~~型ヒントの不整合~~ ✅ 解決済み
~~全Managerのadd_keys_to_offeringsメソッドで引数・戻り値の型が`Dict[str, Any]`となっているが、実際は`List[Dict[str, Any]]`~~

**解決**: PR #8で修正済み - 正しい型ヒント`List[Dict[str, Any]]`に変更

## 改善提案

### 優先度: 高
1. ~~**RDSManager.add_keys_to_offerings のバグ修正**~~ ✅ 解決済み
2. ~~**全Managerのユニットテスト実装**~~ ✅ 解決済み
3. **統合テストの追加**（モック使用）

### 優先度: 中
4. ~~**型ヒントの不整合修正**~~ ✅ 解決済み
5. **エラーハンドリングの改善**
   - CLIでの適切なエラーメッセージ表示
   - ユーザーフレンドリーなエラー説明
6. **ログ設定の統一**
   - logging設定を外部化
   - ログレベルのCLIオプション化
7. **型ヒントのさらなる厳密化**
   - `Dict[str, Any]` をTypedDictに変更
   - Optional型の適切な使用

### 優先度: 低
8. **ドキュメント充実**
   - docstringの追加
   - 使用例の拡充
9. **CI/CD パイプライン構築**
   - GitHub Actions設定
   - 自動テスト実行
10. **パッケージング**
   - PyPI公開の準備

## 依存関係

### boto3 APIマッピング
| サービス | boto3 メソッド |
|---------|---------------|
| RDS | `describe_reserved_db_instances_offerings` |
| ElastiCache | `describe_reserved_cache_nodes_offerings` |
| Savings Plans | `describe_savings_plans_offerings` |
| OpenSearch | `describe_reserved_instance_offerings` |

### AWS CLIマッピング（購入コマンド）
| サービス | AWS CLI コマンド |
|---------|-----------------|
| RDS | `aws rds purchase-reserved-db-instances-offering` |
| ElastiCache | `aws elasticache purchase-reserved-cache-nodes-offering` |
| Savings Plans | `aws savingsplans create-savings-plan` |
| OpenSearch | `aws opensearch purchase-reserved-instance-offering` |

## ライセンス
Unlicense - パブリックドメイン

## 最終更新
2025-01-30
