# World Insight Morning Editorial Pipeline v0.1

World Insightの日次運用を、既存の編集文書とBuilderへ接続する作業手順である。これは記事本文を自動生成したり、公開を自動承認したりする仕組みではない。

## 標準フロー

1. **World Brief確認** — 最新号の存在と日付だけを確認する。World Briefは候補ニュースの入力源であり、別プロジェクト・別サイトである。
2. **Candidate Topics** — `DAILY_EDITORIAL_YYYY-MM-DD.md`に3〜5候補を記録する。
3. **Scorecard** — `SCORECARD.md`で判断密度、利害関係者、Reflection、構造、自分事化を補助評価する。
4. **Source Verification** — 一次資料を確認し、A/B/Cを人間が判定する。Cなら候補を保留・変更する。
5. **Topic Decision** — 採用テーマとToday's Questionを人間が決める。
6. **Article Draft** — `INSIGHT_ARTICLE_TEMPLATE.md`に沿ってMarkdownを編集する。Markdownが正本である。
7. **Editorial Review** — `EDITOR_CHECKLIST.md`で事実、公平性、読者体験を確認する。
8. **Insight Shift Gate** — A/B/Cを編集レビューで記録する。Cなら記事化しない。Bは要確認、Aは次へ進める。
9. **Take One Thing Gate** — 他分野へ持ち運べるか、一文で言えるか、要約になっていないかを確認する。FAILなら公開しない。
10. **Build** — `source .venv/bin/activate && python3 scripts/build.py`で静的HTMLを再生成する。
11. **Preview** — `python3 -m http.server 8000`を使い、Safari / Chromeでlocalhost確認する。
12. **Manual Publish** — `git diff`と公開承認を人間が確認してから、必要に応じてGit操作を行う。

## Publish Gate v0.1

Build後の確認は、別システムではなくこのMorning Pipelineの公開直前Gateとして扱う。`docs/PUBLISH_YYYY-MM-DD.md`を記事ごとの人間編集用記録として使える。記録がない項目は自動的に完了扱いにしない。

### 対応付けと品質Gate

- Source Verificationは、検証文書内に`Article: articles/<対象>.md`のような明示的な対応がある場合だけ、そのA/B/Cを採用する。同じ日付やファイル名だけでは推測しない。対応がなければ`Source Verification Link: UNRESOLVED`とする。
- Editorial Reviewは、対象記事を明記した独立レビュー記録の`Editorial Review: COMPLETE/PENDING/UNRESOLVED`だけで判定する。記事本文の「最終自己評価」は独立レビューと混同しない。
- Insight Shiftは既存仕様どおりA/B/Cを人間が記録する。Aは通過、BはEditorial Reviewで要確認、CはBLOCKEDである。
- Take One Thingは人間が`PASS/NEEDS_WORK/FAIL`を記録する。FAILは公開しない。

### 手動確認項目

`PUBLISH_YYYY-MM-DD.md`には、少なくとも次を対象記事とともに記録する。

- `Local Preview`: `NOT_CHECKED / COMPLETE / FAILED`
- `Safari`、`Chrome`: `NOT_CHECKED / PASS / FAIL`
- `Git Diff Review`: `NOT_CHECKED / COMPLETE / ISSUE_FOUND`
- `Final Approval`: `PENDING / APPROVED / REJECTED`

Previewではindex、archive、当日記事、CSS、内部リンク、横スクロール、Insight Shiftの識別性を確認する。Git Diff Reviewでは意図しない変更、`sample/`や`.DS_Store`、生成HTML、記事Markdown、Source Verification記録を確認する。

### Publish Readiness

Pipelineは次の状態を表示する。`READY_TO_PUBLISH`でも自動pushは行わない。

1. `BLOCKED` — Source Verificationの対応未解決/C、Insight Shift C、Take One Thing FAILなど。
2. `NEEDS_REVIEW` — 独立Editorial Review未完了、Insight Shift B、Take One Thing NEEDS_WORKなど。
3. `NEEDS_PREVIEW` — BuildまたはSafari / ChromeのLocal Preview未完了。
4. `NEEDS_GIT_REVIEW` — Git Diff Review未完了。
5. `WAITING_FOR_APPROVAL` — それ以外のGateを通過し、Final ApprovalだけがPENDING。
6. `READY_TO_PUBLISH` — Final Approvalが人間によってAPPROVED。

日刊であることは公開理由にならない。Gateを通らない日は保留することが正しい判断である。

## Gateの原則

- Source Verificationは記事ドラフト前の必須Gateである。
- Insight Shiftは最重要品質Gateである。内容の自動採点はしない。
- Take One Thingは、ニュースを離れても使えるかを必ず確認する。
- `editorial_pipeline.py`はファイルの存在と明示的な編集記録を確認するだけで、テーマ、A/B/C、品質を自動決定しない。
- 日刊だから公開するのではない。品質Gateを通らなければ、その日は公開しないことも正しい判断である。

## 実行

```bash
cd ~/Workspace/world-insight
source .venv/bin/activate
python3 scripts/editorial_pipeline.py
```

必要なら対象日を指定できる。

```bash
python3 scripts/editorial_pipeline.py --date 2026-08-09
```

不足しているDaily Editorialは、`DAILY_EDITORIAL.md`を空の作業テンプレートとして複製する。候補本文や記事本文は捏造しない。

## 公開前の人間承認

以下は自動化しない。

- 最終テーマ採用
- Source Verification A/B/C
- Insight Shift Quality
- Take One Thing評価
- Editorial Review
- Git commit / push
- GitHub Pages公開承認

## Pilot #2の確認例

2026-08-09のPilot #2では、World Brief、Daily Editorial、記事Markdown、Builder成果物、`PILOT_002B_SOURCE_VERIFICATION.md`のA判定候補を確認できる。しかし、検証文書に対象記事への明示的リンクがないためSource Verification Linkは`UNRESOLVED`であり、独立Editorial Review、Local Preview、Git Diff Review、Final Approvalの記録も存在しない。したがってPublish Readinessは証拠に基づき`BLOCKED`となる。記事本文の自己評価はInsight Shift / Take One Thingの参考信号に留める。
