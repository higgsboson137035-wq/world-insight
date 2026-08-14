# World Insight Daily Publish Record v1

通常日のHuman Read、Technical Validation、Final Approvalを一つにまとめる短い記録。機械的な存在確認だけでPASSやAPPROVEDへ変更しない。

```text
Date: YYYY-MM-DD
Article: articles/YYYY-MM-DD-slug.md
Daily Result: IN_PROGRESS

Insight Shift Review: PENDING
Human Read: PENDING
Human Read Note:
Local Preview: NOT_CHECKED
Safari: NOT_CHECKED
Chrome: NOT_CHECKED

Technical Validation: NOT_STARTED
Build: NEEDED
Internal Links: NOT_CHECKED
HTTP 200: NOT_CHECKED
Git Diff Review: NOT_CHECKED
Builder Idempotency: OPTIONAL

Final Approval: PENDING
```

## 記録ルール

- Insight Shift Reviewは`PENDING / APPROVED`。Insight Shift Bだけが明示的な`APPROVED`を必要とし、Aは未承認でも通過、Cは承認値にかかわらず通過しない。不正値は安全側で停止する。
- Human ReadではInsightの価値、再検討が起きるか、A/B/C、公平性、Thinking Trap、読み味を確認する。
- Safari / Chromeは人間が実際に確認する。
- Technical ValidationにはBuild、生成物、内部リンク、記事順、不確実性表示、不要URL、`git diff --check`を含める。
- Git Diff Reviewは公開対象と意図しないファイル混入を確認する。
- Builder/template/生成ロジックを変更していない通常日は二重BuildとSHA比較をOPTIONALとする。変更日は実施する。
- Final Approvalは人間だけが`APPROVED`へ変更する。
- NO_PUBLISH日はこのPublish記録を作らず、Daily Editorialの`NO_PUBLISH Confirmation: CONFIRMED`で正常終了する。
