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
- Editorial Reviewは対象記事を明記した独立記録を使う。v1では`Final Decision`と`Required Fixes Status`まで読み、A / B / Cを`PASS / NEEDS_FIX / HOLD`へ対応させる。旧記録の`COMPLETE`は読み取り互換を維持する。記事本文の自己評価は独立レビューと混同しない。
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

## Morning Pipeline v0.2

`python3 scripts/morning.py`を毎朝の単一入口とする。これは既存の`editorial_pipeline.py`の状態判定を再利用し、記事本文を生成したり、Build・ブラウザ確認・Git操作を自動実行したりしない。

- World Briefは対象日を優先し、当日号がなければ`STALE`と表示する。古い号を当日号と誤認しない。
- Daily Editorialは、通常は存在確認だけを行う。空の作業ファイルを作る場合だけ`--prepare`を使う。
- `Next Action`には、その時点で人間が最初に行うべき1つの作業を表示する。残りのGateは必要な場合だけ一覧表示する。
- Source Verification、Editorial Review、Insight Shift、Take One Thing、Build、Local Preview、Git Diff Review、Final Approvalの既存Gateは変更しない。
- `BLOCKED`、`NEEDS_REVIEW`、`NEEDS_PREVIEW`、`NEEDS_GIT_REVIEW`、`WAITING_FOR_APPROVAL`の日は、公開を保留できる。

標準のPreviewは次のとおりである。

```bash
cd ~/Workspace/world-insight
python3 -m http.server 8000
```

`morning.py`はサーバーを起動しない。最終承認後のcommit、push、GitHub Pages操作も人間が行う。

## Daily Workflow v1 — Phase 1

### 正式目標

- Quality over Frequencyを優先し、記事を公開しない`NO_PUBLISH`を正常終了として扱う。
- World Brief生成後の人間アクティブ時間8〜10分を目標とする。品質Gateは時間のために省略しない。
- 高リスク・複雑テーマでは時間より品質を優先する。

### Daily Result

`DAILY_EDITORIAL_YYYY-MM-DD.md`に次を明示する。

```text
- Daily Result: IN_PROGRESS | NO_PUBLISH | READY_TO_PUBLISH | PUBLISHED
- Fallback Attempts: 0 | 1
- NO_PUBLISH Confirmation: PENDING | CONFIRMED
```

`HOLD_C`は個別候補のSource Verification結果、`NO_PUBLISH`は当日の最終編集結果である。Initial TopicがHOLD_Cの場合、Fallbackは原則1回まで。FallbackもHOLD_Cまたは独自性不足なら第三候補へ自動移行せず、NO_PUBLISHを人間が確認する。

NO_PUBLISH確認後はArticle、Build、index/archive変更、Publish記録、Final Approvalを要求しない。

### Editorial Review状態

Review記録は記事への明示リンクに加え、次を持つ。

```text
Review Status: COMPLETE
Final Decision: A | B | C
Required Fixes Status: NONE | OPEN | RESOLVED
```

- AかつFixがOPENでない: `PASS`。Buildへ進める。
- BまたはFixがOPEN: `NEEDS_FIX`。Build前に局所修正と再Reviewを行う。
- C: `HOLD`。BuildせずNO_PUBLISH判断へ進む。
- 旧記録の`Review Status: COMPLETE`は読み取り互換を維持する。

### Build freshness

当日記事HTML、index、archiveの存在だけでREADYにしない。記事Markdown、全記事Markdown、対応template、`scripts/build.py`の`mtime_ns`を、それぞれの生成物と比較する。入力が一つでも新しければ`Build: NEEDED`とする。

mtime比較はBuilderやHTMLへ新しいメタデータを書かずに導入でき、記事だけでなくtemplate・生成ロジック変更も検出する。時計の逆行や時刻保持コピーが疑われる運用へ移る場合は、Phase 2以降で入力hash記録を検討する。

### 統合Gate

- Independent ReviewにThree Tests、A/B/C Fairness、Insight Shift、Thinking Trap、Take One Thing、Reader Transformation、Required Fixesを統合する。
- Publish記録にHuman Read、Safari、Chrome、Technical Validation、Git Diff Review、Final Approvalを統合する。
- Builder/template/生成ロジックを変更していない通常日は二重Build＋SHA比較をOPTIONALとする。変更日は実施する。
- Final ApprovalがAPPROVEDで全Gateを通過した場合、`Publish: READY`と表示する。

### Phase 1で自動化しないもの

Candidate生成、Source Verification、Draft、Review、Review B修正、Technical Validation一括実行、Git公開は自動化しない。これらはPhase 2以降の検討対象である。
