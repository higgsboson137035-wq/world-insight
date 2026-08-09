# World Insight Publish Gate Record

このファイルは、記事ごとの公開直前確認を人間が記録するためのテンプレートです。機械的な存在確認だけで `COMPLETE` や `APPROVED` に変更しません。

```text
Date: YYYY-MM-DD
Article: articles/pilot_002.md

Source Verification Link: VERIFIED
Editorial Review: COMPLETE
Insight Shift: A
Take One Thing: PASS
Build: READY

Local Preview: COMPLETE
index.html: PASS
archive.html: PASS
Article HTML: PASS
Safari: PASS
Chrome: PASS
CSS: PASS
Horizontal Scroll: PASS
Internal Links: PASS
Insight Shift Visibility: PASS

Git Diff Review: COMPLETE
Final Approval: PENDING
```

## 記録ルール

- `Article:` は対象Markdownを明記する。日付やファイル名の類似だけでは対応付けない。
- `Local Preview`、Safari / Chrome、`Git Diff Review` は実際に確認した人が記録する。
- `Final Approval` は `PENDING` から始め、最終承認者が判断する。Pipelineは `APPROVED` に変更しない。
- Source VerificationとEditorial Reviewは、それぞれ記事への明示的リンクを持つ記録が必要である。記事本文内の自己評価は独立Editorial Reviewの代わりにならない。

