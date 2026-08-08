# Insight Schema Design

## 1. 設計目的

Insight Schema は、World Insight の「1日1テーマ」を一つの `Insight` オブジェクトとして表現するための設計である。

これは記事データを保存するためだけのJSONではない。事実から問いへ進み、必要に応じて事実へ戻る、World Insightの思考モデルを表現するJSONである。読者へ結論を渡すのではなく、背景、制約、価値、責任、トレードオフ、不確実性を構造化し、読者自身の判断を支える。

本設計は、次の原則をデータ構造へ落とし込む。

- 世界には、答えより問いがある。
- 人は、結果だけでは理解できない。
- 理解は、判断より先にある。
- 理解しても、合意できないことがある。
- 理解することと正当化することは同じではない。
- 責任ある判断は、背景・制約・価値・責任を理解することから始まる。

## 2. 設計原則

### 結論をデータモデルに埋め込まない

`decision.available_options`に正解、推奨、勝者のフィールドを置かない。選択肢は便益、費用、負担主体、前提、リスク、責任の衝突を比較するために存在する。

### 理解と評価を分ける

`human_context`は、主体の判断が生まれる背景を理解する層である。行為の正当性を認定する層ではない。`understanding_is_not_justification`を必須の真偽値とし、サンプルでは常に `true` とする。将来のJSON Schemaでは `const: true` を検討する。

### 人を単純化しない

主体を受益者／負担者だけに分類しない。複数の動機、責任、制約、時間軸、公共利益、交渉力、声の強さを別々に保持する。職業倫理や公共善を美化せず、制度上の役割、組織利益、生活上の利益と併存できる構造にする。

### 事実と推論を追跡可能にする

判断材料は `source_ids` で出典へ接続する。出典側の `supports_fields` は、その出典が支えるフィールドをJSON Pointer形式で示す。仮説は `structural_issue` に置き、代替説明、反証、見解を変える条件を必ず伴わせる。

### 不確実性を欠落として扱わない

不確実性は削除すべきノイズではなく判断材料である。`decision_materials[].uncertainty`、`compass.uncertainties`、編集チェックで明示する。

### 表示と保存を分離する

JSONのすべてを公開HTMLへ表示する必要はない。特に `editorial_metadata` は内部品質管理を主目的とする。公開範囲は将来の表示仕様で決定する。

## 3. トップレベル構造

| フィールド | 型案 | 役割 |
|---|---|---|
| `schema_version` | string | データ構造の版。内容の改訂版とは分ける。 |
| `insight_id` | string | Insightの安定した一意識別子。 |
| `date` | string | 記事基準日。ISO 8601の `YYYY-MM-DD`。 |
| `title` | string | 今日のテーマを示す非誘導的な題名。 |
| `question` | string | 記事全体を導く中心的な問い。 |
| `thinking_skill` | object | 読者が持ち帰る思考技術と転用目標。 |
| `compass` | object | 用語、制度背景、時間軸、主要な緊張、不確実性を示す羅針盤。 |
| `summary` | object | 30秒要約。既知、未確定、考える理由を分ける。 |
| `decision_materials` | array | 読者の判断に必要な数値・制度・法律・外交条件など。 |
| `human_context` | object | 主体の背景、価値、制約、責任、複数動機、力関係。 |
| `decision` | object | 仮想閣議。責任ある役割から複数案を比較する。 |
| `what_if` | array | 条件変更による判断圧力の変化。 |
| `paradox` | array | 根拠を持つ合理的立場どうしの緊張。 |
| `shared_assumptions` | object | 共有された前提と、未検証・争われている前提。 |
| `structural_issue` | object | 「本当の論点」を断定せず仮説として扱う。 |
| `overlooked_perspective` | array | 声の弱い主体、時間外・地域外への影響など。 |
| `take_one_thing` | object | 別の問題へ持ち運べる一つの思考原則。 |
| `final_question` | object | 読者自身の判断基準を問う問いと任意の宿題。 |
| `sources` | array | 出典、時点、一次資料性、支援フィールド。 |
| `editorial_metadata` | object | Five-Year Testなどの内部品質確認。 |

## 4. 各フィールドの役割

### 識別・導入

- `schema_version`：v0.1設計サンプルでは `0.1-draft`。正式Schema公開前の草案であることを表す。
- `insight_id`：日付を変更しても参照が壊れない安定IDとする。
- `date`：ニュース発生日ではなくInsightの基準日。出来事の日付は判断材料に持たせる。
- `title`：結論や善悪を先取りしない。
- `question`：一つの正解を埋め込まず、判断条件を照らす。

### `thinking_skill`

`primary`、`secondary`、`transfer_goal`を持つ。記事のテーマそのものではなく、読者が他の問題にも転用できる思考技術を示す。

### `compass`

`context`、`key_terms`、`time_horizons`、`key_tensions`、`uncertainties`を持つ。「知っておきたいこと」を情報の羅列ではなく、分析の方向を見失わないための最小限の案内として表現する。

### `summary`

`thirty_second`、`known`、`uncertain`、`why_it_matters`を持つ。事実と不確実性を短い要約の中でも混同しない。

### `decision_materials`

各要素は次を持つ。

- `id`：内部参照用の識別子。
- `material_type`：`numeric`、`institutional`、`legal`、`diplomatic`、`historical`、`other`など。
- `label`：材料の名称。
- `value`：number、string、boolean、または将来定義する構造値。
- `unit`：数値単位。非数値は `not_applicable` を使用する案。
- `period_or_date`：対象期間または基準日。
- `significance`：なぜ読者の判断に関係するか。
- `uncertainty`：`level`、`description`、`what_could_resolve_it`。
- `source_ids`：`sources[].source_id`への参照。

数値以外も第一級の判断材料として扱う。制度上の責務、法律上の限界、政策波及の時間差などを文字列で保存できる。

### `decision`

`role`、`situation`、`responsibility`、`available_options`、`reader_prompt`を持つ。各optionは、`id`、`label`、`potential_benefits`、`potential_costs`、`who_benefits`、`who_bears_costs`、`assumptions`、`risks`、`responsibility_conflicts`を持つ。主体参照には可能な限りstakeholder IDを使う。

`selected_option`、`correct_option`、`recommended_option`は置かない。

### `what_if`

各シナリオは `scenario`、`changed_condition`、`why_it_matters`、`affected_stakeholders`、`decision_pressure`、`question_to_reader`を持つ。前提を変えたときに判断が更新されるかを試す。

### `paradox`

各要素は `tension` と複数の `positions` を持つ。各立場は `position`、`reasonable_because`、`assumptions`、`values_prioritized`、`responsibilities_prioritized`、`weaknesses`、`evidence_strength`を持つ。

公平性は機械的な両論併記ではない。明確な事実誤認、著しく弱い根拠、捏造、反証に応答しない主張、人権侵害や暴力を当然の前提として正当化する主張は、対等な合理的立場として登録しない。社会的影響がある場合は、`paradox.positions`ではなく検証対象や背景として記述できる。政治的立場そのものを理由に排除しない。

### `shared_assumptions`

`confirmed`、`contested`、`untested`を分ける。共有されているという事実と、その前提が正しいことを混同しない。

### `structural_issue`

`hypothesis`、`why_this_may_be_deeper`、`alternative_explanations`、`counterevidence`、`what_would_change_this_view`を必須候補とする。「本当の論点」を唯一の本質として断定せず、検証可能な仮説として保存する。

### `overlooked_perspective`

各要素は `perspective`、`why_overlooked`、`why_it_matters`、`related_stakeholders`を持つ案とする。

### `take_one_thing`

`principle`と`transfer_example`を持つ。記事の結論ではなく、別の問題に転用できる判断の道具である。

### `final_question`

`question_to_reader`、`reflection_prompt`、`homework`を持つ。記事を編集部の結論ではなく読者の問いで閉じる。

### `sources`

各出典は `source_id`、`source_type`、`organization`、`title`、`url`、`published_at`、`accessed_at`、`primary_source`、`supports_fields`を持つ。

- `source_type`は `government`、`central_bank`、`international_organization`、`statistics_agency`、`company_official`、`academic`、`news_media`、`other`などを想定する。
- `published_at`と`accessed_at`はISO 8601形式を想定する。
- `primary_source`は、その主張またはデータに対する一次資料かを表す。公式発表の正しさを保証する値ではない。
- `supports_fields`はJSON Pointerの配列とし、裏付ける範囲を追跡可能にする。

### `editorial_metadata`

`five_year_test`、`fairness_check`、`human_context_check`、`uncertainty_check`、`source_check`、`responsibility_check`、`notes`を持つ。各チェックは少なくとも `status` と `notes` を持ち、Five-Year Testは判定根拠も保持する。

これは公開記事本文とは別の編集品質メタデータであり、公開HTMLに必ず表示する項目ではない。ただし、将来、透明性のため一部を公開する可能性はある。

## 5. `human_context` の詳細

### オブジェクト構造

`human_context`は次を持つ。

- `framing`：人を結果だけで説明しないための編集上の焦点。
- `understanding_is_not_justification`：理解と正当化を分ける原則。
- `stakeholders`：主体ごとの文脈。
- `relationships`：主体間の利益衝突、依存、調整可能領域。

### stakeholder

各stakeholderは最低限、次を持つ。

| フィールド | 型案 | 意味 |
|---|---|---|
| `id` | string | 他フィールドから参照する安定ID。 |
| `name` | string | 主体名。個人に限らず集団・制度を含む。 |
| `role` | string | 問題の中で担う役割。 |
| `what_they_protect` | array[string] | 守ろうとする生活、権利、信頼、制度など。 |
| `values` | array[string] | 判断で優先し得る価値。 |
| `background` | array[string] | 経験、状況、制度的背景。 |
| `constraints` | array[string] | 選択を制約する条件。 |
| `responsibilities` | array[string] | 誰に対して何を負うか。 |
| `motivations` | array[object] | `type`と`description`を持つ複数動機。 |
| `incentives` | array[string] | 制度や市場が促す行動。 |
| `fears_or_risks` | array[string] | 恐れる損失や負うリスク。 |
| `short_term_interests` | array[string] | 近い時間軸で守る利益。 |
| `long_term_interests` | array[string] | 長期的に守る利益。 |
| `negotiating_power` | object | `level`、`sources`、`limits`。 |
| `voice_strength` | object | `level`、`channels`、`barriers`。 |
| `who_they_are_accountable_to` | array[string] | 説明責任の相手。 |
| `possible_compromises` | array[string] | 条件付きで受け入れ得る調整。 |
| `non_negotiables` | array[string] | 譲れない責任・権利・限界。 |
| `public_interest_dimension` | object | `contribution`、`tension_with_private_interest`、`long_term_social_effect`。 |

`motivations.type`は、`professional_ethics`、`public_good`、`benefit_to_others`、`mission`、`norm`、`institutional_role`、`mutual_aid`、`long_term_social_stability`、`material_interest`、`belonging`などを想定する。列挙は排他的ではなく、同じ主体に複数を許す。

### relationships

主体単体の記述だけでは衝突や落とし所が見えないため、次を持つ関係オブジェクトを置く。

- `stakeholder_ids`
- `relationship_type`：`conflict`、`dependency`、`accountability`、`possible_coalition`など。
- `interests_in_tension`
- `power_asymmetry`
- `possible_landing_zone`

この構造により、「誰が得るか」ではなく、なぜ利益が衝突し、どこに政治・制度・交渉による調整余地があるかを表現する。

## 6. Insight Pyramidとの対応

| Layer | 主なJSONフィールド |
|---|---|
| Layer 1：事実 | `summary.known`、`decision_materials`、`sources` |
| Layer 2：判断材料 | `compass`、`decision_materials` |
| Layer 3：利害関係者 | `human_context` |
| Layer 4：トレードオフ | `decision.available_options`、`human_context.relationships` |
| Layer 5：逆説 | `paradox`、`what_if` |
| Layer 6：構造 | `structural_issue`、`shared_assumptions` |
| Layer 7：問い | `question`、`final_question`、`thinking_skill` |

対応は一方向ではない。例えば、`structural_issue.counterevidence`から`decision_materials`や`sources`へ戻って仮説を検証する。

## 7. 記事13セクションとの対応

| 記事セクション | 主なJSONフィールド |
|---|---|
| 1. 今日のテーマ | `title`、`question` |
| 2. 30秒要約 | `summary` |
| 3. 判断資料 | `decision_materials`、`sources` |
| 4. 知っておきたいこと | `compass` |
| 5. 利害関係者 | `human_context` |
| 6. 仮想閣議 | `decision` |
| 7. What if? | `what_if` |
| 8. 逆説探し | `paradox` |
| 9. 共通前提 | `shared_assumptions` |
| 10. 本当の論点 | `structural_issue` |
| 11. 見落としやすい視点 | `overlooked_perspective` |
| 12. Take One Thing | `take_one_thing`、`thinking_skill` |
| 13. 今日の問い／今日の宿題 | `final_question` |

## 8. 必須／任意フィールド案

### v0.1でトップレベル必須とする案

指定されたトップレベル20フィールドをすべて必須候補とする。内容がない場合も、構造上意味のある空配列を許すかはJSON Schema化時に個別判断する。重要な分析を安易に省略させないため、`human_context`、`decision_materials`、`decision`、`structural_issue`、`sources`、`editorial_metadata`は空オブジェクトを許可しない案とする。

### ネスト内で必須とする案

- stakeholderの指定19フィールドすべて
- decision optionの指定9フィールドすべて
- what-ifの指定6フィールドすべて
- paradox positionの指定7フィールドすべて
- structural issueの指定5フィールドすべて
- sourceの指定9フィールドすべて
- editorial checkの `status` と `notes`

### 任意候補

- `final_question.homework`
- `take_one_thing.transfer_example`
- 表示専用の短縮文、翻訳、画像、音声
- 編集上の自由記述メモ

任意であっても、欠落と「該当なし」を区別する方法は将来定義する。

## 9. 将来のJSON Schema化方針

1. サンプルを複数テーマで試し、過不足を記録する。
2. JSON Schema Draft 2020-12を候補とし、正式な採用版を決める。
3. `$defs`にstakeholder、source、decision option、editorial checkなどを分離する。
4. ID形式、ISO 8601、列挙値、最小配列数、参照整合性を定義する。
5. `value`の型を `oneOf` で定義し、非数値材料を損なわないようにする。
6. `understanding_is_not_justification`を `const: true` とするか検討する。
7. JSON Schemaで検証できない `source_ids` と `supports_fields` の参照整合性は、別の検証仕様として定義する。
8. schema versionとコンテンツrevisionを分離し、移行方針を決める。

## 10. v0.1では扱わないもの

- 正式な `schema.json`
- 自動ニュース収集と自動記事生成
- AI APIや生成プロンプトの保存形式
- HTML、CSS、JavaScriptの表示仕様
- 多言語、画像、音声、動画
- 読者アカウント、回答保存、投票、推薦
- World Briefとの自動連携
- 記事改訂履歴と訂正履歴の完全なデータモデル
- デジタル署名、コンテンツハッシュ、出典アーカイブ
- 公開用フィールドと内部フィールドの厳密なアクセス制御

## 現時点の未決事項

- `value`の複合型と単位表現の標準
- stakeholder、source、materialのID命名規則
- `evidence_strength`、`negotiating_power.level`、チェック`status`の正式な列挙値
- 空配列、`null`、フィールド省略の意味
- 出典が複数フィールドの一部だけを支える場合の粒度
- 公開HTMLへ出す`editorial_metadata`の範囲
- 訂正・更新・コンテンツrevisionのモデル
