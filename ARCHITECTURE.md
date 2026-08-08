# World Insight Architecture

## Design Freeze v0.2

World Insightは、「読者に何を考えるべきかを教えるメディア」ではなく、「判断がどのように組み立てられ、試され、更新されるかを理解するためのシステム」である。

Design Freeze v0.2では、新しい思想を追加せず、既存設計を実装・運用で検証する。

## Three-Layer Architecture

### Layer A — Editorial Philosophy

なぜWorld Insightが存在するのか、編集者は何を約束するのかを定める層である。

含む文書：

- `VISION.md`
- `MANIFESTO.md`
- `FOUNDING_CHARTER.md`
- `EDITOR'S_PLEDGE.md`
- `EDITORIAL_CHARTER.md`

### Layer B — Judgment Framework

人が判断を組み立てる過程をモデル化する層である。

含む要素：

- Insight Pyramid / Insight Model
- Human Context
- Decision Space
- Priority-Based Options
- Thinking Journey
- Thinking Traps
- Insight Shift
- Take One Thing
- Reflection

関連文書：

- `THINKING_FRAMEWORK.md`
- `QUESTION_FRAMEWORK.md`
- `THINKING_TRAPS.md`
- `EDITOR_WORKSPACE.md`
- `INSIGHT_ARTICLE_TEMPLATE.md`
- `EDITOR_CHECKLIST.md`
- `docs/INSIGHT_SCHEMA_DESIGN.md`

### Layer C — Publishing System

毎日の編集と公開を再現可能にする層である。

現時点の構成：

- Markdown記事
- Insight JSON
- HTMLテンプレート
- CSS
- localhost経由のブラウザ確認

将来の構成：

- Pythonによる生成
- GitHub Pages
- Reflection Engine

World BriefとWorld Insightは別サイト・別プロジェクトである。World Briefは入力候補の一つに過ぎず、World Insightの思想、編集、公開物には依存しない。

## End-to-End Flow

```text
World Brief
    ↓
Candidate News
    ↓
Morning Editorial Meeting
    ↓
EDITOR_WORKSPACE
    ↓
Insight / Judgment Model
    ↓
INSIGHT_ARTICLE_TEMPLATE
    ↓
Markdown Article
    ↓
EDITOR_CHECKLIST
    ↓
HTML
    ↓
Safari / Chrome Preview
    ↓
Publish
    ↓
Reflection
    ↓
Learning
    ↓
Future Judgment
```

候補ニュースの入口と、Insightとしての選定・分析・編集・公開は分離する。World Briefの変更はWorld Insightの運用条件ではない。

## Judgment Model

```text
Fact
  ↓
Decision Materials
  ↓
Human Context
  ↓
Decision Space
  ↓
Priority-Based Options
  ↓
Trade-offs
  ↓
Challenge
  ↓
Insight Shift
  ↓
Transfer
  ↓
Reflection
```

`Human Context`は、その主体が何を守り、どのような背景・価値・責任を持つかを整理する。`Decision Space`は、その主体が現実に何を選べ、何を選べず、何に制約されるかを整理する。前者は理解の層、後者は実行可能性と責任の層である。

## Thinking Journey

1. **Question**：Today's QuestionとQuick Choicesで、読者が最初の仮の判断を持つ。
2. **Materials**：Decision Materials、Human Context、Decision Spaceで判断材料を集める。まだ結論は出さない。
3. **Decision**：Virtual Cabinetで、Quick Choicesの判断を利益、コスト、責任、リスクから再検討する。
4. **Challenge**：What If?、Paradox、Shared Assumptions、Structural Questionで一度の判断を揺さぶる。
5. **Insight Shift**：前提、限界、新しい見方、問いの変化を通じて世界の見方を一つ増やす。
6. **Transfer**：Thinking Trap、Take One Thing、Final Questionで別の問題へ持ち運べる思考に変換する。
7. **Reflection**：結果を採点せず、当時の情報、制約、判断空間を未来から検証する。

## Priority-Based Options

Virtual Cabinetの選択肢は、思想ラベルや「賛成／反対」ではなく、何を優先するかの違いとして設計する。

- **A：即時安定** — 人命、安全通航、市場安定などを先に確保する。
- **B：抑止・圧力と限定協力の両立** — 圧力や抑止を維持しながら、限定分野で協力する。
- **C：長期的・包括的条件** — 核、制裁、地域安全保障などを含む包括条件を優先する。

Bのような中間案は意図的に検討するが、正解や推奨とは扱わない。すべての案に、コスト、責任の衝突、短期的効果、長期的効果、失敗リスクを持たせる。

## Three Tests

公開品質を、次の三つの問いで最上位から確認する。これは`EDITOR_CHECKLIST.md`を置き換えるものではなく、同チェックリストを要約する品質ゲートである。

### Is it true?

事実、出典、不確実性が確認できるか。事実と解釈、仮説、予測を混同していないか。

### Is it fair?

Human Context、Decision Space、複数の合理的立場、公平性が十分に扱われているか。機械的な両論併記になっていないか。

### Is it useful?

Insight Shift、Take One Thing、Reflectionによって、読者が別の問題にも使える判断力を残せるか。

## Success Metric

> World Insightは、読者が私たちに賛成したかではなく、記事を読む前よりも良い判断ができるようになったかで成功を測る。

PVや滞在時間は補助指標であり、目的ではない。

## Reflection Loop

Reflectionは答え合わせではない。将来、次の要素を比較する。

- 当時利用可能だった情報
- 当時のDecision Space
- 当時の前提
- 見落とし
- 実際の結果

結果から過去の判断を単純に評価するOutcome Biasを避け、当時の条件の中で判断がどのように組み立てられたかを学習可能にする。

## Engineering Principles

- HTMLを手編集し続けず、将来はMarkdown / JSONから自動生成する。
- ブラウザ確認はlocalhost経由で行う。
- SafariとChromeの両方で確認する。
- `file://`直開きは標準確認手順にしない。
- World Briefを変更しない。
- 思想、判断モデル、実装を分離する。

## Design Freeze Rule

v0.2では、次を原則とする。

- 思いつきだけで新しい概念を追加しない。
- 10〜20本の記事運用で設計を検証する。
- 設計変更はPilot、読者レビュー、Reflectionなどの実証に基づく。
- 新機能は「判断力を高めるか」で評価する。

## Current Status

- Foundation completed
- Design Freeze v0.2
- Pilot #1 in progress
- Static HTML prototype available
- Markdown→HTML automation not yet implemented
- Reflection Engine not yet implemented
