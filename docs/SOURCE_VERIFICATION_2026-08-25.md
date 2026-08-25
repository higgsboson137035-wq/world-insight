# Source Verification — 2026-08-25

- Date: 2026-08-25
- Selected Topic: 二次制裁が予告されたとき、いつ行動を変えるべきか——政策時刻と自分の決定期限を分ける
- Article Decision: **HOLD_C**

## Scope and Measurement

- Verification scope: Morning Editorial Meetingの決定的確認事項だけを、World Briefが参照した2026年8月24日の米国の対イラン措置（`Operation Economic Outcast`）について限定確認した。
- Allowed source family: 当該措置の米財務省／OFAC公式発表、その発表が直接参照する法的文書、その措置に直接対応するFAQ／General License。措置特定のためWhite House公式発表も確認した。
- Excluded: 別の制裁事例、別企業、別国、市場反応、海上報復、中国との関係、原油価格、一般的な制裁制度、専門家コメント。
- Measurement: 開始 2026-08-25 20:25:06 JST / 終了 2026-08-25 20:25:49 JST / wall-clock **43秒** / active time **43秒**。ユーザー待ち・離席はなく、推測による控除はしていない。
- Not performed: Article Draft、Editorial Review、Human Read、Build、HTML生成、tests、Pipeline変更、Git stage / commit / push。

## Fixed Official Source Family

1. [The White House, “Operation Economic Outcast: Total Isolation of the Iranian Regime,” 24 Aug 2026](https://www.whitehouse.gov/releases/2026/08/operation-economic-outcast-total-isolation-of-the-iranian-regime/)
   - 公式発表は、Treasuryが同日Operationを開始したこと、digital assets・technology・gold・aviation・shippingを対象とする五つのsectoral sanctions determinationsが同日発出されたこと、secondary sanctions riskを広げることを述べる。
   - ただし発表本文は、各determination本文、対象となる具体的行為の法的定義、個別の発動条件、国別期限、wind-down、例外・許可へリンクしていない。
2. [OFAC Recent Actions](https://ofac.treasury.gov/recent-actions)
   - 限定確認時点に表示された最新一覧では、2026年8月18日までの項目を確認できたが、8月24日の当該措置に対応するRecent Action、determination、FAQ、General Licenseを確認できなかった。
3. [OFAC Iran Sanctions program page](https://ofac.treasury.gov/sanctions-programs-and-country-information/iran-sanctions)
   - 限定確認時点のRecent Actions欄は2026年8月7日までで、当該措置の五つのdetermination、FAQ、General Licenseを確認できなかった。

過去のIran sanctions authorities、別日付のGeneral License、一般FAQは、今回の同一公式文書群ではないため五要素の穴埋めに使用していない。

## Verification Table

| 要素 | 判定 | 確認できたこと | 確認できないこと | 公式Source |
|---|---|---|---|---|
| 1. 措置の現在の法的状態 | **Partial** | White Houseは、Treasuryが8月24日にOperationを開始し、五つのsectoral determinationsを同日発出したと公式に述べる。単なる将来構想だけではない。 | determination本文を確認できず、各sectorへの指定権限が発出時点で直ちに有効なのか、追加の個別designation／determinationを要するのかを本文から確定できない。 | White House 2026-08-24、OFAC Recent Actions、OFAC Iran Sanctions page |
| 2. 対象行為 | **Partial** | 対象sectorはdigital assets、technology、gold、aviation、shipping。公式発表はeconomic engagement、money laundering facilitation、business with Iranがsecondary sanctions riskへさらされると述べる。 | 法的に対象となる`operate in`、services、`significant transaction`等の具体的行為、対象者、知識要件、重要性基準を当該determination本文から確認できない。政治的に広い表現を法的対象範囲と同一視できない。 | White House 2026-08-24 |
| 3. 発動条件または日付 | **Partial** | Operation開始日とdeterminations発出日は2026年8月24日。公式発表は`Beginning today`と述べる。 | 個々の外国主体に制裁が発動する法的条件、各国に与えるとされた具体的期限、指定・執行までの手続や日付を確認できない。`The clock just started ticking`は期限そのものではない。 | White House 2026-08-24 |
| 4. 取引終了等の猶予 | **Not Confirmed** | なし。 | 国別・取引別のwind-down期間、終了期限、既存取引の扱いを当該公式文書群から確認できない。 | White House 2026-08-24、OFAC当該資料は確認できず |
| 5. 例外・許可の有無 | **Not Confirmed** | なし。 | 当該五sector determinationsに直接対応する例外、General License、個別許可、humanitarian carve-outの有無・条件を確認できない。別日付のIran General Licenseは接合していない。 | White House 2026-08-24、OFAC当該資料は確認できず |

## Decisive Check

**決定的確認事項: 不成立。**

五要素は同一の公式文書群から一組として成立しない。政策発表から、Operation開始、sector、secondary sanctions risk拡大という政策側の時計の入口は確認できる。しかし、法的対象行為と個別発動条件はPartial、猶予と例外・許可はNot Confirmedである。Stop Conditionを適用し、一般的なIran制裁制度、過去のGeneral License、別の制裁事例へ調査を広げていない。

## Evidence Boundary

### Official / Primary

- White Houseは2026年8月24日にOperation開始を発表した。
- White Houseは、同日、digital assets、technology、gold、aviation、shippingを対象とする五つのsectoral sanctions determinationsが発出され、secondary sanctions riskを広げると述べた。
- 同発表は`Beginning today`、`The clock just started ticking`と述べるが、後者は法的期限の記載ではない。
- 限定確認時点のOFAC Recent Actions／Iran Sanctions pageでは、当該8月24日文書群を確認できなかった。

### Reliable Reporting

- World Brief／その参照報道は、各国に関係見直しの猶予を与えたうえで二次制裁を導入する構えと要約している。
- この「各国の猶予」は当該公式文書群から具体的期限・法的条件として確認できず、核心Evidenceには使用しない。

### Inference

- sectoral determinationが発出されたことから、すべての当該sector取引が同日自動的に禁止されたとは推論しない。
- `The clock just started ticking`から、企業・国別のwind-down期限を推定しない。
- 強い政治的警告から、執行日、指定確率、銀行・企業の先回り対応を推定しない。

### Unknown / Unconfirmed

- 五つのsectoral determinationの本文と各法的根拠・effective date。
- 制裁対象となる具体的行為、対象者、knowledge／significance基準。
- 各国・各取引に対する具体的な発動条件、通知日、終了期限。
- wind-downの有無、期間、既存取引の扱い。
- 当該措置に直接対応するFAQ、General License、humanitarianその他の例外・許可。
- 個々の意思決定者の契約、在庫、決済、供給上の取消不能時刻。
- 民間金融機関・企業が実際にいつ、どの取引を先回り停止するか。

## Decision-clock Separation / Quality Reassessment

- Policy-side clock: **部分成立**。2026年8月24日のOperation開始とsectoral determinations発出までは確認できるが、法的発動条件、猶予、例外を含む時計は完成しない。
- Decision-maker-side irreversible clock: **不成立**。今回の限定公式資料から、特定の意思決定者の契約期限、在庫、決済、供給判断が取消不能になる時刻は確認できない。推測で補わない。
- Reader Transformation: **維持不可**。政策側と意思決定者側の二つの時計をEvidenceで並べられず、準備／保留／停止の切替を具体的に実演できない。
- Insight Shift: **C / HOLD_C**。Morning段階のA候補を維持しない。政治的警告と法的状態を分ける入口は得られたが、Decision-clock separation全体は成立しない。
- Take One Thing: **未成立（FAIL相当）**。一般的な携帯可能性はあるが、今回のEvidenceで二つの時計を具体的に実演できないため成立候補として維持しない。
- Overlap reassessment: **HIGH risk / HOLD**。Evidence不足を一般的な制裁権限で補えばPilot #5／8月24日候補の権限・実行経路へ、情報更新規則で補えばPilot #2へ、猶予・退出期間の一般論で補えばPilot #4／8月23日の代替時間へdriftする。独立した判断能力をEvidenceで維持できない。

## Final Decision

**Source Verification: HOLD_C**

- Stop Condition: **APPLIED**。
- Additional search: **NOT PERFORMED**。不足判明後、指定された周辺領域や別制度へ拡張していない。
- Fallback: **NOT PERFORMED**。自動移行せず、人間確認を待つ。
- Daily Result: **IN_PROGRESS**。当日のNO_PUBLISHまたは一度だけのFallback再評価は別の人間判断である。
- Next Action: **Human confirmation required: 一度だけ既存候補をFallback再評価するか、NO_PUBLISHを確認する。**
