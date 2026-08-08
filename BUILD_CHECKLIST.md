# World Insight Daily Build Checklist

記事完成後から公開確認までの技術・公開運用チェック。思想と記事品質は`EDITOR_CHECKLIST.md`で確認する。

## A. Before Build

- □ `.venv`有効
- □ 記事Markdown保存済み
- □ `EDITOR_CHECKLIST.md`完了
- □ Sources確認済み
- □ `git status`確認

記事の編集対象は`articles/*.md`。HTMLは生成物であり、直接編集しない。

## B. Build

標準コマンド：

```bash
source .venv/bin/activate
python3 scripts/build.py
```

確認：

- □ build成功
- □ `index.html`更新
- □ `archive.html`更新
- □ 日付記事HTML生成
- □ エラーなし

## C. Local Preview

Browser Preview Ruleに従い、`file://`直開きは標準手順にしない。

```bash
cd ~/Workspace/world-insight
python3 -m http.server 8000
```

Safari / Chromeで確認する。

- □ トップ
- □ Archive
- □ 最新記事
- □ CSS
- □ 内部リンク
- □ 横スクロールなし
- □ Question First
- □ Quick Choices
- □ Insight Shift
- □ Final Question

終了：

```text
Control + C
```

## D. Git Review

- □ `git diff`確認
- □ 意図しないファイル変更なし
- □ `.DS_Store`なし
- □ `.venv`なし
- □ Markdownと生成HTMLの両方を確認

## E. Publish

現時点では手動運用。具体的なコミットメッセージは固定しない。

- □ `git add`
- □ `git commit`
- □ `git push`

## F. GitHub Pages

- □ GitHub push成功
- □ Pages deployment成功
- □ 公開トップ表示
- □ Archive表示
- □ 最新記事表示
- □ Safari確認
- □ 必要ならiPhone確認

## G. Completion

- □ 公開完了時刻
- □ 公開記事ID
- □ Reflection対象として記録
- □ 問題があればメモ

World BriefとWorld Insightは別プロジェクト・別サイトである。World Briefは候補ニュースの主要入力源になり得るが、World Insightの生成や公開に技術的に依存しない。World Brief本体は変更しない。

この文書はDesign Freeze v0.2後の運用テンプレートであり、新しい思想、記事Phase、品質概念、機能案を追加しない。
