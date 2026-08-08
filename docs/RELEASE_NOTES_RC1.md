# World Insight Release Candidate 1

## 概要

World Insight RC1は、Design Freeze v0.2で確定した理念、判断モデル、編集運用、Pilot #1、静的サイト生成を、初回コミットとGitHub Pages公開の候補として整理したリリース候補です。

RC1の目的は、新しい思想や機能を追加することではありません。Markdownを正本として記事を編集し、ローカルで静的HTMLを生成し、将来リポジトリルートをGitHub Pagesで配信できる状態を確認することです。

## 完成したもの

### Foundation

- Mission、Vision、North Star
- World Insightの理念とマニフェスト
- 編集原則、問いのフレームワーク、Insight Pyramid
- Layer 3「利害関係者」を中心とするHuman Context設計
- Thinking Trap、Insight Shift、Take One Thing、Reflection
- Editor's Pledge

### Architecture and editorial system

- `ARCHITECTURE.md`によるThree-Layer Architecture
- Thinking Journeyの7フェーズ
- Priority-Based OptionsによるQuick Choices / Virtual Cabinet
- Behind the Choiceによる優先順位・責任・リスクの明示
- Three Tests：Is it true? / Is it fair? / Is it useful?
- Source Policy、Editorial Workflow、Editor Checklist

### Pilot #1

- ホルムズ海峡をめぐる交渉を題材にしたMarkdown記事
- Question First
- Quick Choices
- Decision Materials、Human Context、Decision Space
- Virtual CabinetとA/B/Cの優先順位比較
- Challenge、Insight Shift、Thinking Trap
- Take One Thing、Final Question、Reflection
- 公式資料と報道情報を分けたSources

### Builder and static site

- `scripts/build.py`
- `templates/insight.html`
- `templates/index.html`
- `templates/archive.html`
- 生成物としての`index.html`
- 生成物としての`archive.html`
- 生成物としての`archive/2026-08-08.html`
- GitHub Pagesを想定した相対パスのCSS参照
- `.gitignore`による`.DS_Store`、仮想環境、Pythonキャッシュの除外

## まだ未実装

- GitHubリポジトリ作成
- Git remote設定
- GitHub Pages設定と公開
- 日次のニュース収集
- 複数記事の本格的な自動処理
- JSON入力との接続
- Markdownからの高度なセクション別レンダリング
- Reflection Engine
- launchd等による日次自動化
- RSS、sitemap

RC1では、生成HTMLを直接編集しません。編集対象は`articles/*.md`であり、HTMLはBuilderで再生成します。

## 次フェーズ

1. RC1の初回コミット
2. GitHubリポジトリ作成
3. GitHub Pagesの最小公開
4. Safari / Chromeでの公開URL確認
5. Pilot #1の読者レビュー
6. 10〜20本の記事運用によるDesign Freeze検証

## Builder Roadmap

### Phase 1：完了候補

- 1本の記事を入力にした静的HTML生成
- トップページと日付別アーカイブ
- GitHub Pages向け相対パス
- 再ビルド時の不要差分がないことの確認

### Phase 2：検証

- 複数Markdown記事の一覧化
- 記事メタデータの明示的な管理
- Safari / Chromeでの表示差確認
- 公開後のリンクとアーカイブ確認

### Phase 3：将来検討

- JSON入力との接続
- 日次生成の半自動化
- Reflectionデータの保存と参照

## Design Freeze宣言

RC1では、Design Freeze v0.2を維持します。

- 新しい概念を思いつきだけで追加しない。
- 10〜20本の記事運用で既存設計を検証する。
- 設計変更はPilot、読者レビュー、Reflectionなどの実証に基づく。
- 新機能は、読者の判断力を高めるかで評価する。

RC1は完成宣言ではありません。公開可能な最小構成を検証し、次の実証へ進むための候補版です。
