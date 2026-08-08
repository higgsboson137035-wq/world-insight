# World Insight Project Status

以下のJSONコードブロックは Project Dashboard `schema_version=1` 用の管理情報である。進捗は v0.1 の完了を100とする概算値であり、作業内容の変化に応じて更新する。

```json
{
  "schema_version": 1,
  "project_id": "world-insight",
  "name": "World Insight",
  "status": "in_progress",
  "priority": "high",
  "current_work": "初回Gitコミットとv0.1プロトタイプの準備",
  "progress": 40,
  "remaining_tasks": [
    "v0.1: 初回Gitコミット",
    "v0.1: HTMLプロトタイプ",
    "v0.1: JSONデータ形式設計",
    "v0.1: 最新ページ",
    "v0.1: 日付別アーカイブ",
    "v0.1: Safari表示確認",
    "v0.1: 実ニュースを使った創刊号",
    "v0.1以降: GitHubリポジトリ作成",
    "v0.1以降: GitHub Pages",
    "v0.1以降: 日次生成の半自動化",
    "v0.1以降: 日次自動化"
  ],
  "risks": [
    "AIが結論を押し付ける",
    "利害関係者を自己利益だけで単純化する",
    "判断資料と意見が混在する",
    "テーマ選定がニュースの話題性だけに引っ張られる",
    "World Briefとの役割が曖昧になる"
  ],
  "estimated_sessions": 5
}
```

## 現在地

- Foundation 第1段階の理念・編集基盤7文書は作成済み。
- Foundation 第2段階のプロジェクト仕様、情報源方針、編集ワークフロー、および Foundation Review は完了済み。
- 実装、公開、日次運用は未着手。

## 進捗の考え方

`progress` は Foundation 文書、運用仕様、Foundation Review の完了を反映して40とする。今後は、v0.1 に必要な初回Gitコミット、プロトタイプ、データ形式、創刊号、表示確認の完了に応じて更新する。`estimated_sessions` は現時点から v0.1 までを対象とし、外部公開と自動化は含めない。
