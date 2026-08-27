# World Insight Project Status

以下のJSONコードブロックは Project Dashboard `schema_version=1` 用の管理情報である。進捗は v0.1 の完了を100とする。

```json project-dashboard-v1
{
  "schema_version": 1,
  "project_id": "world-insight",
  "name": "World Insight",
  "status": "日次編集運用中",
  "progress_percent": 100,
  "priority": "高",
  "current_work": "Morning Editorial Pipelineによる日次評価と公開判断",
  "remaining_tasks": [
    "次回World Brief後のMorning Editorial Meeting",
    "品質Gateを通過した候補だけSource Verification以降へ進める",
    "公開候補発生時のHuman Reviewと手動公開"
  ],
  "risks": [
    "AIが結論を押し付ける",
    "利害関係者を自己利益だけで単純化する",
    "判断資料と意見が混在する",
    "テーマ選定がニュースの話題性だけに引っ張られる",
    "World Briefとの役割が曖昧になる"
  ],
  "estimated_sessions": null,
  "estimate_confidence": "未評価",
  "updated_at": "2026-08-27T23:37:22+09:00",
  "data_note": "進捗率はPROJECT_STATUS.md既存定義のv0.1完了を100とする基準です。初回Gitコミット、Builder、公開用HTML、日付別アーカイブ、実ニュース記事、日次Morning Editorial運用が実装済みです。2026-08-27は候補重複を理由にNO_PUBLISHで正常終了しました。必要セッション数は未評価です。",
  "repository": {
    "git_enabled": true,
    "github_enabled": true,
    "github_visibility": null,
    "default_branch": "main"
  }
}
```

## 現在地

- Foundation文書、Builder、公開用HTML、日付別アーカイブを実装済み。
- 実ニュースを使った記事と公開記録を作成済み。
- Morning Editorial Pipelineで日次に候補を評価し、品質Gateを満たさない日はNO_PUBLISHとして正常終了する運用中。
- 2026年8月27日は候補のReader Transformationが既存記事と重複したためNO_PUBLISH。

## 進捗の考え方

`progress_percent` は既存定義どおりv0.1完了を100とし、現在は100とする。次回以降の作業量は日次候補とHuman Review結果で変わるため、`estimated_sessions` は未評価とする。
