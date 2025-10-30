# セキュリティガイドライン

## 機密情報の取り扱い

このプロジェクトでは機密情報の混入を防ぐために、以下の対策を実施しています。

### 1. .gitignoreによる予防

以下のファイルはGit管理から除外されています：

- **認証情報**: `*.pem`, `*.key`, `credentials.json`, `secrets.json`
- **AWS関連**: `.aws/`, `*credentials.csv`
- **環境変数**: `.env`, `.env.*`（`.env.example`などのテンプレートは除く）
- **データベース**: `*.db`, `*.sqlite`
- **バックアップファイル**: `*.bak`, `*.backup`

### 2. 推奨ツール

#### git-secrets（推奨）

コミット前に機密情報を自動検出します。

**インストール方法（macOS）:**
```bash
brew install git-secrets
```

**セットアップ:**
```bash
# リポジトリ内で実行
git secrets --install
git secrets --register-aws

# カスタムパターンを追加（オプション）
cat .gitsecrets-patterns.txt | while read pattern; do
  [[ -n "$pattern" ]] && [[ ! "$pattern" =~ ^# ]] && git secrets --add "$pattern"
done
```

#### pre-commit（代替案）

より包括的なチェックを行う場合：

```bash
# インストール
pip install pre-commit

# .pre-commit-config.yaml を作成後
pre-commit install
```

### 3. AWS認証情報の管理

このツールはAWS CLIの認証情報を使用します。以下の方法で安全に管理してください：

**推奨方法:**
- `~/.aws/credentials` でプロファイルを管理
- AWS IAM Identity Center（旧SSO）を使用
- 一時的な認証情報を使用

**避けるべき方法:**
- ❌ プロジェクトディレクトリ内に認証情報ファイルを配置
- ❌ 環境変数に直接ハードコード
- ❌ コード内に認証情報を埋め込み

### 4. 環境変数の使用方法

環境変数が必要な場合：

1. `.env.example` にサンプルを作成（値は含めない）
2. `.env` に実際の値を設定（このファイルはgitignore済み）
3. README.mdで設定方法を説明

**例（.env.example）:**
```
AWS_PROFILE=your-profile-name
AWS_REGION=ap-northeast-1
```

### 5. 緊急時の対応

もし機密情報をコミットしてしまった場合：

1. **即座にローカルで修正**
   ```bash
   git reset --soft HEAD~1  # コミットを取り消し
   ```

2. **すでにプッシュしてしまった場合**
   - 該当する認証情報を直ちに無効化・再発行
   - `git-filter-repo` または `BFG Repo-Cleaner` で履歴から削除
   - チームメンバーに通知

3. **AWS認証情報の場合**
   - AWS IAMコンソールでアクセスキーを無効化
   - 新しいアクセスキーを発行
   - CloudTrailで不正使用がないか確認

### 6. チェックリスト

コミット前に確認：

- [ ] `.env` ファイルが含まれていないか
- [ ] 認証情報ファイル（`credentials.json`など）が含まれていないか
- [ ] AWSアクセスキー/シークレットキーが含まれていないか
- [ ] データベースファイルが含まれていないか
- [ ] `git diff --cached` で変更内容を確認したか

### 7. 参考リンク

- [git-secrets](https://github.com/awslabs/git-secrets)
- [pre-commit](https://pre-commit.com/)
- [AWS認証情報のベストプラクティス](https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/best-practices.html)
