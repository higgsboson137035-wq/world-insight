# World Insight 2026-08-23 — Limited Source Verification

- **Date:** 2026-08-23
- **Selected Topic:** 関税の強さではなく、代替に必要な時間を測る——統合供給網の「貿易戦争」をどう判断するか
- **Daily Editorial:** `docs/DAILY_EDITORIAL_2026-08-23.md`
- **Article:** NOT CREATED
- **Source Verification:** **HOLD_C**
- **Case fixed before search:** 米加間の完成車（主としてHS 8703の乗用車）に対する関税と代替生産能力
- **Evidence cutoff:** 2026-08-23
- **Measurement:** 開始 2026-08-23 07:48:10 JST / 終了 2026-08-23 07:50:00 JST / 実所要時間 **1分50秒（110秒）**。
- **Scope:** 正式な関税条件、二国間依存量、代替能力または切替所要時間の三要素だけを、同一の完成車ケースで確認。別品目、企業コメントによる補完、広範な産業横断、Fallback探索は未実施。

## Executive Conclusion

**Source Verification: HOLD_C。** 完成車について、正式な関税条件と二国間依存量は一次資料で確認できた。一方、対象となる米加完成車フローを必要量・仕様・期限内に代替する能力、またはその切替所要時間を示す一次資料は確認できなかった。

カナダ政府資料は2025年4月9日から米国製車両に25%を課す条件を示す。米国の2026年7月20日Proclamationはカナダ産の一定品目へ追加50%を2026年8月19日から課すとしていたが、8月18日のProclamationが発効日を8月22日へ変更した。米国側の元の措置はSection 232対象品を除外するため、完成車そのものへの追加50%適用範囲はAnnexとの照合が必要であり、「全カナダ産完成車へ50%」とは書けない。

依存量については、Statistics Canadaが2024年のカナダ産乗用車・light truck輸出の93.4%が米国向けだったと公表している。米国Proclamationも、2025年4月から2026年3月の米国製motor vehicleの対カナダ輸出が前年同期の約259億ドルから約203億ドルへ22%減少したと記載する。ただし、これらは方向の異なるフローと異なる期間・定義であり、双方の依存度を同一分母で比較する一組ではない。

カナダの公的grant recordにはFord Oakville Assembly Complexの改修が2029年12月31日まで、完成後の年産能力が最大10万台とある。しかし、これはF-Series Super Duty向けの個別投資であり、今回のHS 8703乗用車フローを代替する能力でも、関税対象車両の切替時間でもない。この資料を核心Evidenceへ接続すると、別車種・別市場・別生産mandateを編集側で合成することになる。

したがって三要素は同一ケースで成立しない。Stop Conditionを適用し、別品目へ拡張せず停止する。

## 1. Decisive Check

### Required

同一の完成車ケースについて次の三要素を一組で確認する。

1. 発効済み／正式公表済みの関税条件
2. 米加間の品目別依存量
3. 代替生産能力、または必要量・仕様を満たすまでの切替所要時間

### Result: FAIL

| 要素 | 確認結果 | 判定 |
|---|---|---|
| 正式な関税条件 | カナダは2025年4月9日から、非CUSMA適合の米国製車両と、CUSMA適合車両の非加墨contentへ25%。米国の追加50%措置は2026年8月22日発効へ変更されたが、Section 232対象除外とAnnexがあり、全完成車への一律適用ではない | **確認。ただし適用範囲の限定が必要** |
| 二国間依存量 | 2024年のカナダ産passenger cars / light trucks輸出の93.4%が米国向け。別の米国公式文書には、米国製motor vehicleの対加輸出額が2025年4月〜2026年3月に約203億ドルとある | **部分確認。方向・期間・分母が揃わず、双方向の非対称性比較には不足** |
| 代替能力／切替所要時間 | 公的grant recordにOakville工場改修の2029年末までの工程と最大年産10万台はあるが、F-Series Super Duty向けで、HS 8703乗用車の代替能力・切替時間ではない | **不成立** |

**総合:** 三要素は同一品目・同一ケースで揃わない。核心であるSubstitution-latency mappingをEvidenceで実演できない。

## 2. Official Sources Reviewed

1. [Department of Finance Canada — List of vehicle products from the United States subject to 25 per cent tariffs effective April 9, 2025](https://www.canada.ca/en/department-finance/news/2025/04/list-of-vehicle-products-from-the-united-states-subject-to-25-per-cent-tariffs-effective-april-9-2025.html)
   - 25%の条件、発効日、HS 8703の対象line、CUSMA適合車両のcontent条件を確認。
2. [White House — Imposing Additional Duties to Offset Canadian Discrimination … Motor Vehicles, July 20, 2026](https://www.whitehouse.gov/presidential-actions/2026/07/imposing-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-motor-vehicles/)
   - カナダ措置に関する米政府の記述、米国追加措置の率・対象制約、対加輸出額の期間比較を確認。当事者政府による法的措置と主張であり、因果評価を独立事実とは扱わない。
3. [White House — Temporary Suspension … Alcoholic Beverages, Dairy, and Motor Vehicles, August 18, 2026](https://www.whitehouse.gov/presidential-actions/2026/08/temporary-suspension-of-additional-duties-to-offset-canadian-discrimination-against-the-commerce-of-the-united-states-with-respect-to-alcoholic-beverages-dairy-and-motor-vehicles/)
   - 追加措置の発効日が2026年8月22日へ変更されたことを確認。
4. [Statistics Canada — Canadian international merchandise trade, January 2025](https://www150.statcan.gc.ca/n1/daily-quotidien/250306/dq250306a-eng.pdf)
   - 2024年のカナダ産passenger cars / light trucks輸出の93.4%が米国向けとの公表値を確認。
5. [Government of Canada Open Government — Grant Agreement 515512](https://search.open.canada.ca/grants/record/ic%2C033-2025-2026-Q4-515512%2Ccurrent)
   - Oakville Assembly Complex改修のwork phaseが2029年12月31日まで、期待能力が最大年10万台であることを確認。ただし今回の代替能力には数えない。

## 3. Evidence Boundary

### Confirmed / Official

- カナダ政府は2025年4月9日から、指定された米国製車両に25%の関税措置を発効させた。
- 米国の2026年7月20日Proclamationによる追加措置は、8月18日のProclamationで発効日が2026年8月22日へ変更された。
- 米国措置にはSection 232対象品の除外とAnnexによる対象指定がある。
- Statistics Canadaは、2024年のカナダ産passenger cars / light trucks輸出の93.4%が米国向けだったと公表した。
- Oakvilleの特定改修projectは2029年末までのwork phaseと最大年10万台という期待結果を持つ。

### Official Claim / Interested Government Position

- 米国Proclamationは、カナダ措置が米国commerceを差別し、米国製motor vehicleの対加輸出減少を生じさせたと位置付ける。関税条件と記載された輸出額は確認対象にできるが、差別性・因果・公共利益の評価は米国政府の立場である。

### Inference Not Adopted

- 93.4%という輸出集中から、カナダが米国より弱い、または米国が短期間で代替できるとは推論しない。
- Oakvilleの10万台を、米国向け乗用車輸出やカナダの米国車輸入の代替量に算入しない。
- 輸入先の増加を、同じ仕様・価格・数量での切替完了時間とは扱わない。

## 4. Unknown / Unconfirmed

- 2026年8月23日時点で、Annex IIの各HTS lineとSection 232除外を適用した後、どのカナダ産完成車が米国の追加50%を実際に負担するか。
- 同一HS・同一期・同一分母で見た、米国側とカナダ側それぞれの完成車依存率。
- 関税対象となる具体的model、原産content、quota利用状況、実際の実効税率。
- 既存在庫が何日・何週間の需要を満たせるか。
- 非米国／非カナダ工場が、対象modelと同等の規格・認証・価格帯を何台、いつまでに供給できるか。
- 生産mandate移管、supplier認証、tooling、労働力、物流、販売認証に要する時間。
- Oakville projectが関税対象フローの代替に寄与するか。
- 関税が輸出減少のどの割合を因果的に説明するか。

## 5. Overlap Reassessment

- **Morning評価 MEDIUM → HIGH risk。** Substitution-latency mappingを独立させる核心は、代替完了までの時間を同じケースで示すことだった。確認できたEvidenceは関税条件と輸出集中までで、切替時間は空欄のままである。
- この状態で記事化すると、Pilot #3の「残余リスクと回復期限」をEvidenceなしに通商へ移すか、Pilot #4の「移行中の依存」を一般論として再演する可能性が高い。
- 「輸出の93.4%が米国向け」を中心にすると、依存度ランキングまたは供給網分散の一般論へ縮退し、今回初めて提供する判断能力にならない。

## 6. Reader Transformation Verdict

**維持不可。** Beforeの「関税率・報復額を見る」から「代替完了時間で実効レバレッジを見る」への移動には、少なくとも一つのケースで切替時間をEvidenceとして埋める必要がある。現資料で示せるのは、正式条件と輸出集中までである。

「代替には時間がかかるはず」という一般論、企業コメント、別車種の工場改修を使えばAfterを説明できるが、それは今回の同一ケースから導いたReader Transformationではない。Insight ShiftはMorningのA候補から**C**へ下げる。Take One Thingの一般的な携帯性は残るが、今回のニュースからEvidenceで獲得できないため記事化根拠には使わない。

## 7. Stop Condition Application

次は行わない。

- 別品目・別HS codeへの探索
- 自動車部品、エネルギー、農産物等への拡張
- 企業コメントによる在庫・切替時間の補完
- 個別model・工場を横断する無制限調査
- Candidate 2・3への自動Fallback
- Article Draft以降

## 8. Final Decision

**Article Decision: HOLD_C**

- 三要素は同一ケースで成立しない。
- Initial Topicを停止する。
- Fallback Attemptsは0のまま維持する。
- Daily Resultは、FallbackまたはNO_PUBLISHを人間が別途判断するまで`IN_PROGRESS`とする。
- 記事Draft、Build、HTML生成、Pipeline変更は行わない。
