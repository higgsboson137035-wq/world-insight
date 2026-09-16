Prompt-Version: phase1-0.3

# World Insight Daily Run — Phase 1

## Status

このRunは次の状態にあるExperimental Prototypeです。

- EXPERIMENTAL
- NON-AUTHORITATIVE
- NOT_ADOPTED

正式Workflow、Quality Gate、Discovery route、Candidate universe、Candidate数、Overlap基準を変更してはいけません。

このPromptの目的は、Humanが毎朝貼っている反復的なDaily Run指示を安全に機械実行できるか確認することです。

## Automation Boundary

このRunで扱う範囲は、次の範囲だけです。

```text
World Brief readiness
  ↓
Candidate Discovery
  ↓
Light Evaluation
  ↓
Human Gate 1 candidate package
  ↓
STOP
```

Gate 1 packageの出力後は停止してください。

## Input Boundary

当日のWorld BriefだけをCandidate Discoveryのinputとして使用してください。

World Briefは未検証inputです。Brief本文とBrief内Sourceは、検証済みEvidenceとして扱ってはいけません。

使用するBriefは、当日のlocal dateと一致する次のファイルだけです。

```text
/Users/kazutoshiinoue/Workspace/world-brief/briefs/YYYY-MM-DD.md
```

前日または過去のBriefを代用してはいけません。Briefが当日分としてreadyでなければ、Candidate Discoveryを開始せず、次を出力して停止してください。

```text
Brief-Readiness: BRIEF_NOT_READY
```

World Brief RepositoryおよびWorld Insight Repositoryはread-onlyで扱ってください。ファイル作成、編集、削除、移動、上書きを行ってはいけません。

## Prohibited Activities

このRunでは以下を行ってはいけません。

- Web search
- External research
- Source Verification
- Firecrawl
- World Brief generation
- `generate.sh` execution
- Article generation
- Human Read
- Editorial Review
- Build
- Preview
- Git add
- Git commit
- Git push
- Publish
- Memory update
- Observation Lens
- Pilot A
- Pilot B
- Workflow change

Source Verificationは、Candidateが有望であっても開始しないでください。必要な場合は、Gate 1 packageで次を示して停止してください。

```text
Source-Verification: NOT_STARTED
Gate-1-Follow-Up: SOURCE_VERIFICATION_REQUIRED
```

## Candidate Discovery

当日のWorld Briefを全文読んでください。Today's Top 3だけでなく、Executive Summary、Why It Matters、Big Picture、各カテゴリ、日本への影響、Tomorrow's Watchlistを含むBrief全体をCandidate universeとして扱ってください。

Candidateは最大3件程度です。候補数を埋めるために追加候補を作らないでください。Fallback Candidate、第4候補、新しいDiscovery route、Candidate universeの拡大は行わないでください。

Candidate Discoveryでは、まずconsidered candidatesを検討し、Light Evaluation後にHuman Gate 1へ正式提出するCandidate（formal Candidate）だけを選別してください。considered candidateは内部の検討対象であり、formal Candidate blockではありません。Candidate-Countはformal Candidateの件数だけを数えます。HOLD、NOT SELECTED、独立性不足、Evidence feasibility不足、Reader Transformation不足など、既存の品質基準を満たさずHuman Gate 1へ渡す価値がないconsidered candidateは、formal Candidate blockへ出力せず、Candidate-Countにも含めないでください。validatorを通すためだけに弱いCandidateをformal Candidateとして推薦してはいけません。

formal Candidateとして出力してよいのは、Light Evaluation後もmeaningfulなReader Transformationがあり、既存のOverlap / IndependenceおよびEvidence feasibilityの基準を満たし、HumanがGate 1で検討する価値がある候補だけです。これは新しい品質Gateではなく、既存のWorld Insight評価基準をformal Candidateの選別へ適用するものです。considered candidatesのprivate reasoningや詳細なRejected Candidate一覧を出力してはいけません。

Reader Transformationを最重要評価としてください。

各Candidateについて、次を評価してください。

- Brief item
- Initial Question
- Reader Transformation BEFORE
- Reader Transformation AFTER
- Structural Question
- Insight Shift
- Take One Thing
- Human Context / Responsibility conflict
- Decision Space
- Evidence feasibility
- Overlap / Independence
- Provisional evaluation

「この記事を読む前と後で、読者の判断方法が一つ変わるか」を確認してください。

ニュースの新しさ、重要性、面白さだけでは独立Candidateとしないでください。

## Independence Evaluation

OverlapはTopic名の一致・不一致だけで判断しないでください。

既存のWorld Insight記事、既存のDaily Editorial records、最近のNO_PUBLISH Candidate recordsをread-onlyで確認し、次のレベルで比較してください。

- Reader Transformation
- Structural Question
- Insight Shift
- Take One Thing
- 読者に求める判断操作

参照対象は特定の日付へ固定せず、Repository内の既存recordをファイルパターン等で確認してください。特に直近のNO_PUBLISH Candidateが使った判断操作の再演に注意してください。

表面的なTopicの類似だけで自動排除しないでください。Reader Transformation、Structural Question、Insight Shift、Take One Thing、判断操作が本当に異なる場合は、独立Candidateとして評価できます。

一方、ニュースが新しくても判断操作が実質的に同じ場合は、独立Candidateとして扱わないでください。

Candidate Discoveryが既存の判断操作へ収束した場合、そのOperational observationを記録してください。ただし原因は確定しないでください。少なくとも次の可能性を未確定のまま扱ってください。

- Brief自体のニュース構成
- Candidate Discovery prompt / workflow
- Independence Gate
- 既存Insight蓄積によるOverlap増加
- Candidate universe
- その他の要因

この観測を理由に、Quality Gateを緩めたり、Candidate数を増やしたり、Discovery routeを変更したり、Pilotを開始したりしないでください。

## Evidence Boundary

事実と分析を次の分類へ分離してください。

- Confirmed
- Claims
- Analysis
- Hypothetical
- Unknown

World Briefの記述は、World Briefに記載された内容として扱ってください。独立に確認していない事実をConfirmedへ移してはいけません。

Unknownは自動失格理由ではありません。Unknownが「判断するために何を確認する必要があるか」を示す場合はEvidence Boundaryとして保持できます。

ただし、核心Factが未確認、推測だけでReader Transformationを成立させている、Evidenceなしでも問いが面白いだけ、という場合はArticle pathを提案してはいけません。

Phase 1ではSource Verificationを実施しないため、次を固定してください。

```text
Source-Verification: NOT_STARTED
```

## Gate 1 Outcome

formal Candidateがない、または独立したReader Transformationと十分なEvidence feasibilityを同時に確認できるformal Candidateがない場合は、次を使用してください。

```text
Daily-Candidate-Outcome: NO_PUBLISH_CANDIDATE
Recommended-Candidate: NONE
Human-Decision: PENDING
Source-Verification: NOT_STARTED
Gate-1-Follow-Up: NONE
```

これはHuman承認済みの正式Daily decisionではありません。

有望Candidateがある場合は、次を使用してください。

```text
Daily-Candidate-Outcome: CANDIDATES_FOR_HUMAN_REVIEW
Human-Decision: PENDING
Source-Verification: NOT_STARTED
Gate-1-Follow-Up: SOURCE_VERIFICATION_REQUIRED
```

次の表記を使用してはいけません。

```text
NO_PUBLISH / HUMAN APPROVED
```

Human Decisionは常に`PENDING`です。Humanの承認なしに正式Daily decisionを確定してはいけません。

## Gate 1 Package Contract

出力はHuman Review用のGate 1 packageだけにしてください。前置きの進捗説明、実行宣言、記事本文、Source Verification結果を出力しないでください。

### Required Metadata

次のmetadataを必ず含めてください。

```text
Run-Date: YYYY-MM-DD
Run-Start: ISO-8601 local timestamp
Brief-Readiness: READY | BRIEF_NOT_READY
Candidate-Count: 0..3
Daily-Candidate-Outcome: NO_PUBLISH_CANDIDATE | CANDIDATES_FOR_HUMAN_REVIEW
Source-Verification: NOT_STARTED
Gate-1-Follow-Up: NONE | SOURCE_VERIFICATION_REQUIRED
Human-Decision: PENDING
Prompt-Version: phase1-0.3
Prompt-SHA256: INJECTED_BY_ORCHESTRATOR
```

`Prompt-SHA256`はこのPrompt自身で計算しないでください。将来のorchestratorが実行時に計算・注入・検証する値です。

### Required Sections

次のsectionを必ず含めてください。

```text
## World Brief Confirmation
## Candidate List
## Candidate Comparison
## Recommended Candidate
## Candidate Light Evaluations
## Confirmed
## Claims
## Analysis
## Hypothetical
## Unknown
## Evidence Boundary
## Candidate Discovery Convergence Observation
## Measurement
```

### Required Candidate Content

各CandidateのLight Evaluationには次を含めてください。

Candidate List内の各Candidate blockは、次のheadingで固定してください。

```text
### Candidate 1
### Candidate 2
### Candidate 3
```

Candidate-Countに応じて必要なformal Candidate blockだけを出力してください。Candidate-Countが0の場合はformal Candidate blockを1件も出力しないでください。Candidate-Countが1、2、3の場合は、それぞれCandidate 1まで、Candidate 2まで、Candidate 3までを連番で出力してください。番号飛び、重複、Candidate 4以降は禁止です。considered candidateをformal Candidate blockとして復活させてはいけません。

各Candidate block内では、次のfield labelをそれぞれ1回だけ出力してください。fieldの意味、内容、semantic quality基準は変更しないでください。

- Candidate
- Brief item
- Initial Question
- Reader Transformation BEFORE
- Reader Transformation AFTER
- Structural Question
- Insight Shift
- Take One Thing
- Human Context / Responsibility conflict
- Decision Space
- Evidence feasibility
- Overlap / Independence
- Provisional evaluation

`Recommended-Candidate`のallowed formatは、次の4種類だけです。

```text
NONE
Candidate 1
Candidate 2
Candidate 3
```

Candidate-Countが0の場合はformal Candidateがないことを明記し、Candidate Comparisonではformal candidatesなしとし、Candidate Light EvaluationsではGate-1-worthy candidateなしと分かる内容にしてください。considered candidatesの詳細をCandidate blockやCandidate Comparisonへ出力してはいけません。`Recommended-Candidate: NONE`、`Daily-Candidate-Outcome: NO_PUBLISH_CANDIDATE`、`Gate-1-Follow-Up: NONE`を使用してください。Candidate-Countが1〜3の場合は、formal CandidateだけをCandidate ComparisonとCandidate Light Evaluationsの比較対象にし、`Daily-Candidate-Outcome: CANDIDATES_FOR_HUMAN_REVIEW`、`Gate-1-Follow-Up: SOURCE_VERIFICATION_REQUIRED`を使用してください。Recommended-Candidateは実際に存在するformal Candidate blockの番号にしてください。Recommended-CandidateはHuman approvalを意味せず、`Human-Decision: PENDING`を維持してください。

### Required Measurement

`Measurement`には次を含めてください。

```text
Machine elapsed: <measured value or UNKNOWN>
Human active time: UNKNOWN
Rework count: 0
```

Human active timeを推測してはいけません。

## STOP Boundary

Gate 1 packageを出力したら停止してください。

Gate 1 package出力後に、Article generation、Source Verification、Human Read、Editorial Review、Build、Preview、Git、Publish、Memory、Observation Lens、Pilot、Workflow変更へ進んではいけません。

このPromptはGate 1 packageを作るためだけに使用します。Human Reviewの結果を待たずに、次の工程を開始してはいけません。
