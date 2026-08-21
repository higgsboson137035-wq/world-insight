# World Insight 2026-08-22 — Limited Source Verification

- **Date:** 2026-08-22
- **Selected Topic:** AIを使わせる前に、どの判断を任せられるか——検証能力と責任からAIリテラシーを考える
- **Daily Editorial:** `docs/DAILY_EDITORIAL_2026-08-22.md`
- **Article:** NOT CREATED
- **Source Verification:** **HOLD_C**
- **Evidence cutoff:** 2026-08-22 08:08:09 JST
- **Measurement:** 開始 2026-08-22 08:07:22 JST / 終了 2026-08-22 08:09:20 JST / 実所要時間 **1分58秒（118秒）**
- **Scope:** 決定的確認事項の限定検証のみ。Stop Conditionにより通常Source Verification、Fallback探索、記事Draft以降は未実施。

## Executive Conclusion

**Source Verification: HOLD_C。** 最有力の一次資料はCalifornia Department of Education（CDE）の公式`AI Guidance in Public Schools`（2025 Guidance）だった。同資料は、誤った／偏った出力を生む具体的sample activity、信頼できる情報源との照合を含む4段階rubric、誤りを修正して理由を問う別のsample activityを含む。

しかし、これらは一つの授業・評価設計として接続されていない。CDE資料から、同じ課題について「AIの誤りを発見 → 外部根拠と照合 → 生徒が訂正 → 訂正理由を説明 → 教師がrubricで評価」の全工程を確認できない。とくに、AI生成記事を批評する例とAccuracy rubricには、生徒が訂正版を作る工程、訂正理由を教師が採点するcriterionがない。誤分類を修正するGrade 7 activityには、外部根拠照合と教師用rubricがない。

一般方針、モデルpolicy、非公式・ベンダー教材、ニュース記事へ要件を継ぎ足すことは、Morning Meetingの「一つの公式教材・評価設計」という条件を満たさない。Stop Conditionを適用し、通常Source Verificationへ広げずInitial Topicを停止する。

## 1. Decisive Check

### Required

州政府、公立学区、教育委員会等の一つの公式カリキュラム／教材／評価設計から、次の5要素を一組として確認する。

1. AIが誤った出力をする具体的な課題
2. 生徒が外部根拠と照合する工程
3. 生徒が誤りを訂正する工程
4. なぜ訂正したかを説明する工程
5. それらを教師が評価する具体的基準

### Result: FAIL

| 必須要素 | CDE公式資料で確認できたこと | 一組としての判定 |
|---|---|---|
| 1. 具体的な誤出力 | Grade 5の`AI Historian`は片側資料だけからBoston Tea Partyを一面的に要約する。Grade 7の`Habitat ID` botは砂漠を`lifeless`と誤分類する。ELA例はAI生成記事のfacts、bias、evidence useを批評させる | **確認** |
| 2. 外部根拠との照合 | Accuracy rubricは、factsがreliable sourcesと一致するか、trusted source（books、websites、teachers）で主要事実を確認したかを問う | **確認**。ただし上記の特定課題に明示接続されない |
| 3. 生徒による訂正 | Grade 7 activityは誤分類を、健全な乾燥地の画像をtraining pileへ加えて修正する | **部分確認**。AI生成記事／Accuracy rubricの課題には訂正版作成がない |
| 4. 訂正理由の説明 | Grade 7 guiding questionは、botが失敗した理由と、新しい例がどう修正したかを問う | **部分確認**。外部根拠照合とrubric採点に接続されない |
| 5. 教師の具体的評価基準 | Accuracy rubricはVery accurate / Mostly accurate / Questionable / Unreliableの4段階とsource checkを示す | **部分確認**。訂正の質・訂正理由を採点するcriterionがない |

**総合:** 5要素は同一文書内に部分的に現れるが、**一つの公式教材・評価設計としては揃わない**。別課題・別表を編集側で結合すると、公開されていない授業設計を推論で作ることになるため不可。

## 2. Official Material Reviewed

### Official / Primary Source

1. [California Department of Education — Artificial Intelligence: 2025 Guidance](https://www.cde.ca.gov/ci/pl/aiincalifornia.asp)
   - CDEとCalifornia Public Schools Artificial Intelligence Working GroupによるTK–12公式Guidance。
   - AI Literacy for Students、grade別sample activities、Academic Integrity and Responsible Use、AI output evaluation rubricを確認。
2. [California Department of Education — AI Guidance in Public Schools（PDF）](https://www.cde.ca.gov/ci/pl/documents/aiguidance.pdf)
   - pp.15–16: `AI Historian`、`Habitat ID`等のsample activitiesとguiding questions。
   - pp.27–28: Accuracy / Relevance / Clarity / Fairnessの4段階AI-output evaluation rubric。
   - p.29: AI-generated articleをfacts、bias、evidence use、voiceからcritiqueするELA/media-literacy例。
3. [California Department of Education — Model Policy: Artificial Intelligence in Education](https://www.cde.ca.gov/ci/pl/aipolicy.asp)
   - source triangulation、mismatch detection、staffによるAI-output verification、educator of recordが最終評価権限を保持する方針を確認したが、具体的な生徒課題と採点rubricではないため核心Evidenceに数えない。

### Reliable Reporting

4. [Associated Press — Schools are starting to teach AI literacy, Aug. 21, 2026](https://apnews.com/article/4fb9f2c0240993499870f4f204bf41c1)
   - World Briefの入口。Charleston County School Districtの研修・生徒course、誤ったworld map、fabricated studies、情報を常にverifyするというcourse guidanceを報じる。
   - District公式の課題本文と評価rubricを確認できないため、5要素の代替にしない。

## 3. Evidence Boundary

### Official / Primary Source

- CDEはAI outputのaccuracy、relevance、clarity、fairnessを4段階で見るsample rubricを公式Guidanceに掲載している。
- Accuracyはreliable/trusted sourcesとの照合を判断材料にする。
- CDEは誤分類・偏った出力を扱うgrade別sample activitiesと、失敗理由を問うguiding questionsを掲載している。
- CDE Model Policyは、AIがcritical thinkingやrequired academic workを代替すべきでないこと、staffのAI output verification、最終gradeはeducator of recordが決定することを示す。

### Reliable Reporting

- APはCharleston County School DistrictのAI literacy courseが、AIの具体的誤りやfabricated studiesを示し、事実情報をverifyするよう教えると報じる。
- AP記事だけでは、授業の完全な手順、訂正課題、説明課題、教師の採点基準を確認できない。

### Inference

- CDEのsample activityとAccuracy rubricを教師が組み合わせれば、Morning Meetingの5工程に近い授業を設計できる可能性はある。
- しかしCDEがその組合せを一つの授業・評価設計として公開したとは言えない。この組合せを既成事実として記事化しない。

### Unknown / Unconfirmed

- CDEまたはCaliforniaの公立学区が、5工程を一組にした完成済みlesson plan／student worksheet／teacher scoring rubricを実施しているか。
- Charleston County School Districtのstudent courseに、生徒自身による訂正、訂正理由の説明、教師採点rubricが含まれるか。
- 生徒が実際にAIの誤りをどの程度発見・訂正できるか。
- 教師が実際にどの程度監督・評価できるか、必要な時間・研修・class size上の制約。
- AI literacy教育の学力、批判的思考、誤情報耐性への因果効果。
- AI利用が学力を向上または低下させるか。
- 学校・家庭間のAI access格差の規模と、今回の具体的授業への影響。
- privacy / safety、評価公平性、教師・保護者・生徒のHuman Contextを今回の中心設計へつなぐ十分な事実。決定的確認事項不成立のため通常検証へ進まず未確認のまま残す。

## 4. Overlap / Reader Transformation Verdict

- **2026-08-14 overlap: MEDIUM → HIGH risk。** Morning Meetingでは、AI性能ではなく人間側の検証責任と委任境界に限定すれば独立可能とした。しかし確認できた公式Evidenceは、AI outputをaccuracy／relevance／clarity／fairnessという条件別rubricで評価する設計が中心である。記事をこのEvidenceだけで成立させると、8/14の「平均性能をscenario、coverage、availability、critical taskへ展開する」操作を、AI outputのtask別評価へ移す方向へdriftする。
- **Verification-before-delegation mapping:** **Evidence不成立。** `失敗 → 検知者 → 照合根拠 → 訂正説明 → 最終責任`の全欄を一つの公式授業・評価設計から埋められない。Model Policyから教師の最終責任を、別rubricから生徒の照合を継ぎ足すことはできるが、それは公式に確認されたmappingではなく編集上の合成になる。
- **Reader Transformation:** **維持できない。** 「AI出力を信頼できる資料と照合する」はEvidenceで示せるが、「操作可能性と委任可能性を分け、検証能力と責任に応じて委任境界を決める」まで実演できない。一般的なAI欠点一覧やtask別性能比較へ縮退させない。

## 5. Stop Condition Application

決定的確認事項が不成立のため、次へは進まない。

- 州別の広範な横断調査
- 海外事例
- AI教育効果研究
- privacy / safety、access格差、Human Contextの通常Source Verification
- 非公式教材・ベンダー教材による不足要素の補完
- Candidate 2・3への自動Fallback
- 新規Fallback探索
- 記事Draft以降

## 6. Final Decision

**Article Decision: HOLD_C**

- 決定的確認事項は不成立。
- Initial Topicを停止する。
- Candidate 2・3へFallbackしない。
- 新規Fallbackを探索しない。
- `Daily Result: NO_PUBLISH`、`NO_PUBLISH Confirmation: CONFIRMED`としてEditorial dayを終了する。
- 記事Draft、Editorial Review、Human Read、Build、HTML生成、index/archive、Pipeline等は変更しない。
