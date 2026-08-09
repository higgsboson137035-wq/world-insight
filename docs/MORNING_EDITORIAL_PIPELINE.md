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

2026-08-09のPilot #2では、World Brief、Daily Editorial、Source Verification A、記事Markdown、Insight Shift A相当の編集記録、Take One Thing PASS、Builder成果物を確認できる。ただし、CLIの表示がREADYでも、公開承認は必ず手動で行う。
