# World Insight — Draft

**Title:** その防護性能は、必要な瞬間に呼び出せるか
**Date:** 2026-08-14
**Insight ID:** 2026-08-14-scenario-callable-performance
**Category:** 科学・宇宙・安全設計
**Thinking Skill:** 平均性能を、scenario、coverage、location、availability、critical taskから「必要時に呼び出せる性能」へ読み替える
**Estimated Reading Time:** 7〜9分
**Reflection Status:** Pending
**Draft Status:** Fallback Source Verification PASS_Bに基づく通常号Draft。未公開。

## Today's Question

> **あなたが長期宇宙飛行の防護策を決めるなら、累積曝露の低減、重大な太陽粒子事象での臓器防護、緊急時のtask継続のどれを優先し、どの「守れない場面」を許容しますか。**

「被曝を約60%減らす」と聞けば安心に見える。しかし、どの危険、場所、身体範囲で成立するのか。警報後に装着し、必要な作業を続けられるのか。

数字が正確でも、必要な瞬間に呼び出せるとは限らない。この記事ではheadline性能を、**Scenario-callable performance——必要なscenario・範囲・作業条件で呼び出せる性能**へ読み替える。

## Quick Choices

### A：累積曝露を抑える

**最優先するもの：** mission全体で受ける放射線量を下げ、長期的な健康riskを抑えること

### B：重大SPE時の臓器防護を優先する

**最優先するもの：** 稀でも深刻なsolar particle event（SPE）で、高感受性の臓器・組織を守ること

### C：緊急時のtask継続を優先する

**最優先するもの：** 防護を身につけたまま、移動、保守、医療対応など必要な作業を続けること

まだ正解は決めない。Aは短時間の極端事象、Bは未知の粒子条件や未被覆部位、Cは必要な線量低減を見落とし得る。Scenario-callable performanceはCの別名ではなく、三案共通の点検フレームである。

## 30-Second Brief

### Confirmed Facts

- NASAの無人月周回mission Artemis Iでは、放射線防護vestを着けたfemale torso phantom「Zohar」と、着けない「Helga」がOrionに搭載された。
- Artemis I飛行中に大規模SPEは起きていない。研究者は飛行測定で放射線輸送modelを検証し、歴史的SPEをmodelへ入力した。
- Orionのseat 3/4付近で、effective doseは1972年型SPEで**61.8%**、1989年型で**40.2%**低減すると推定された。
- AstroRadは全身suitではなく、torsoの高感受性臓器・組織を選択的に守る設計である。
- NASAのISS人間工学資料は、vest着用で搭乗作業のおよそ75%を完了できた一方、腰、肩、首の可動域制限を記録した。未完了taskの内訳は確認できない。

### Reliable Reporting

APはvestを約26kgと報じ、2026年8月にScience Advancesで研究が発表されたこと、Artemis IIには搭載されなかったことを伝えた。これらは本稿で一次資料上の効果量やNASAの正式採用決定へ格上げしない。

### The Decision

争点は、その数字が成立する条件と、危険時に必要taskを維持できるかである。

## Decision Materials

### 1. 60%は、実際のsolar stormを測った数字ではない——Confirmed Fact

Artemis Iは2022年の無人月周回missionだった。MARE実験では二つのfemale torso phantomにdetectorを置き、ZoharだけがAstroRadを着用した。

ただし飛行中にmajor SPEは起きていない。研究者はOrionがinner Van Allen beltを通過した際の測定値でMonte Carlo simulationを検証した。simulationと測定の差は、M-42 detectorで−2.2±12.5%、CADで−3.1±14.9%だった。この±値はvestの防護率の幅ではなく、**model validationにおける測定との差**である。

歴史的なsolar energetic proton条件を検証済みmodelへ入力した結果が、1972年型と1989年型の推定である。実際の巨大stormで60%防いだ結果ではない。

### 2. 同じvestでも、scenarioが変われば61.8%と40.2%に分かれる——Confirmed Model Estimates

Orionのseat 3/4付近で、1972年8月型SPEのeffective doseは233.6 mSvから89.4 mSvへ、**61.8%低下**すると推定された。1989年10月型では249.9 mSvから149.4 mSvへ、**40.2%低下**だった。

Vestなしの推定doseは1989年型の方が高いが、低減率は1972年型の方が大きい。危険の大きさだけで防護率の順位は決まらない。Particle spectrumとshieldingの組合せによる可能性はあるが、詳しい寄与は最新論文全文で確認できずInferenceに留める。

二つのscenarioは「平均の誤差」ではない。同じ装備の価値が、危険の性質によって変わる具体例である。そして二例のうち低い40.2%を、未知scenarioのworst caseとも呼べない。

### 3. Effective doseは、全身を均等に守ったという意味ではない——Confirmed Coverage / Known Unknowns

AstroRadはhelmetやfull-body suitではなく、高感受性のtorso臓器・組織を狙うselective shieldingである。Active detectorは表面・vest外側のほか、lung、stomach、uterus、spine等に置かれた。

Effective doseは臓器・組織の影響を重み付けしてまとめる量であり、「身体のどこでも61.8%下がる」という地図ではない。頭部、四肢、眼、皮膚、個々の骨髄部位などの結果を、本稿の資料だけで埋めることはできない。

推定はOrion内部のseat 3/4付近に基づく。構造、向き、座席、姿勢が違うEVA、月面、別の宇宙船へ移せない。主対象はSPEのsolar energetic protonsで、長期GCRへ同じ率を使えない。

### 4. 防護できても、必要なtaskを呼び出せるとは限らない——Confirmed Human-Factors Boundary

物理性能と人が使えることは別に試験する必要がある。ISSでは宇宙飛行士がvestを着け、運動、可動域、日常作業を評価した。

NASAの2023年資料は、およそ75%のonboard activitiesを完了できたとする一方、hips、shoulders、neckの可動域が制限されたと記録する。これは「75%だから実用的」という合格点ではない。「25%はできなかった」という単純な裏返しでもない。taskの選び方、完了の質、未完了taskの内訳、その中に緊急時のcritical taskが含まれるかを確認できないからである。

APが報じた約26kgは、microgravityでもinertia、打上げmass、収納volumeを伴う。警報から装着までの時間、全crew分の保管、fit、疲労・熱、訓練、costはUnconfirmedである。

## Human Context

### 宇宙飛行士

守るのは将来の健康だけではない。SPE中の機器確認やcrew支援には身体を動かす必要があり、高いshieldingと可動性は別々の安全条件である。

### Mission commanderとcrew

限られた時間に、shelterへ留まるか、vestを着て作業するかを選ぶ可能性がある。ただし運用手順は未確認で、警報、装着、人数、taskの優先順位が必要になる。

### Mission plannersとengineers

Vest、spacecraft shielding、storm shelter、他の安全装備を同じmission制約へ置き、mass、収納、mobilityを比較する。ただし具体的な配分とcostは未確認である。

### Medical・radiation protection teams

臓器感受性、event spectrum、期間、個人差を評価する。Female phantomの結果を全体格・性別へ移さず、未被覆部位を空欄に残す。

### 将来missionのcrew

試験時と将来missionのtaskが違えば、過去の「使えた」は再現しない。未来のcrewを平均値内の仮想の一人として扱わない。

## Decision Space

性能を次の六欄で点検する。

| 確認欄 | 今回確認できること | 空欄に残すこと |
|---|---|---|
| **Scenario / hazard** | 1972年型と1989年型SPE | 未知spectrum、major SPEの実飛行試験 |
| **Coverage** | torsoの高感受性臓器・組織を選択防護 | 全身・個別臓器の全range |
| **Location** | Orion seats 3/4付近 | EVA、月面、別spacecraft |
| **Availability** | ISSで有人着用試験を実施 | 警報余裕、保管、全crewへの配備 |
| **Critical-task compatibility** | 約75%の搭乗作業、腰・肩・首のROM制限 | 未完了taskと緊急時重要度 |
| **Failure mode** | spectrum差、部分coverage、ROM制限を確認対象にできる | actual failureの発生率、真のworst case |

六欄は一つのscoreへ足し合わせない。一欄がdecision-limitingなら、他で埋め合わせられない。線量を下げても唯一必要な操作ができなければ、そのtaskでは性能を呼び出せない。

空欄だけで装備を退けず、追加試験やfit改善で次に埋める欄を決めることもできる。

## Virtual Cabinet

### A：累積曝露を抑える

- **守る価値:** mission全体の線量と長期的健康riskを下げる。
- **合理性:** 稀なeventだけでなく、時間とともに積み上がる曝露を判断へ含められる。
- **Blind spot:** 短時間の重大SPEや、特定臓器・未被覆部位の上限を平均へ隠し得る。
- **費用・制約:** 長時間着用や常設shieldingなら、mobility、mass、収納、他装備への負担が続く。
- **Failure condition:** 累積doseは下がっても、重大scenarioのdecision-limitingな臓器doseまたはtask制約を越える。

### B：重大SPE時の臓器防護を優先する

- **守る価値:** 稀でも深刻なeventで、高感受性臓器・組織への大きな曝露を抑える。
- **合理性:** 1972年型のようなscenarioでは、大幅なeffective-dose低減が推定されている。
- **Blind spot:** 未知spectrum、頭部・四肢等のcoverage外、GCR、日常運用を見落とし得る。
- **費用・制約:** rare event用装備のmass、収納、fit、訓練が必要。他装備とのtrade-offは未確認である。
- **Failure condition:** actual eventが想定と異なる、装着が間に合わない、守る必要のある部位がcoverage外にある。

### C：緊急時のtask継続を優先する

- **守る価値:** shelterに留まるだけでなく、危険中にもmission-criticalな行動を続ける。
- **合理性:** ISSで実際に着用し、運動や日常作業を評価した証拠がある。
- **Blind spot:** 「作業できる」ことは、必要な臓器dose低減を保証しない。
- **費用・制約:** mobilityを得るためshieldingを薄くすれば防護を失い得る。crew別fitとtask別試験が要る。
- **Failure condition:** 多くのtaskを完了できても、本当に必要な一つがROM制限でできない。またはtaskはできても線量低減が不足する。

三案は併用し得るが、どのscenarioを先に守り、どの空白とfailure conditionを受け入れるかは選ぶ必要がある。

## What If?

最初のA/B/Cを、条件を一つずつ変えて選び直す。

- 未知SPEで低減率が想定より低ければ、Bの優先順位は上がるか、別の防護が必要になるか。
- Missionを制約する部位がcoverage外なら、AとBのどちらを選び直すか。
- 警報後に装着できても必要な首・肩の動作ができなければ、Cを上げるか、それともtaskを変えるか。
- Orion内の数値を月面EVAへ移せず、SPE対策がGCRや別装備の余力を減らすなら、最初の順位を維持するか。

選択が変わったら、六欄の**scenario、coverage、location、availability、critical task、failure mode**のどこがdecision-limitingになったかを確認する。変わらない場合も、どの空欄を受け入れたかを言葉にする。これらは発生済みの失敗ではなく、設計・運用で確認すべきfailure modeである。

## Paradox

防護具を厚くすれば、放射線に対する物理性能は上がり得る。しかし動けなくなれば、必要な瞬間の防護価値は下がり得る。反対に、どんなtaskもできる軽い装備でも、必要な臓器doseを下げられなければ防護具として足りない。

精密な平均ほど一般化しやすく見える逆説もある。Effective doseは有用だが、一つの数字がcoverage、location、装着状態を消すことがある。

## Shared Assumptions

- 60%低減なら、身体のどこでも60%守られる。
- 大きいstormほど、同じ割合で防げる。
- modelが実測と合えば、極端事象も実測済みである。
- 着用できれば、緊急taskも遂行できる。
- Orion内の性能は、EVAや月面でも同じである。
- SPEを防げれば、長期GCRも同じ割合で防げる。

Modelだから無意味、部分防護だから無効でもない。どの条件で数字を使えるかを問う。

## Structural Question

### 仮説：防護性能は「どれだけ効くか」ではなく、「必要なscenarioで呼び出せるか」まで含めて測るべきではないか

平均性能が同じでも、scenario、coverage、location、availability、critical taskが違えば実効価値は変わる。Headline率が低くても、重要なscenarioで確実に使える方が価値を持つ場合がある。

この仮説が弱まる条件もある。第一に、hazardが十分均一で、身体・場所・taskによる性能差が小さい場合。第二に、装備が常時自動的に機能し、deployabilityを別に問う必要がない場合。第三に、平均値が既にworst-relevant scenario、coverage、availabilityを保守的に含み、個別欄を分けても判断が変わらない場合である。

AstroRadではscenario差、selective coverage、ROM制限が確認できるが、公開資料だけで全欄は完成しない。

## Insight Shift

### 1. 読者が持ちやすい前提

防護具の価値は、平均またはheadlineの低減率で比べられる。

### 2. なぜその前提だけでは足りないのか

同じvestでもscenarioで推定率が違い、全身を覆わず、有人試験には可動域制限があった。

### 3. 新しい見方

**防護性能を一つの率ではなく、scenario別の低減 × 身体・臓器coverage × 必要時のavailabilityとして読む。さらに、critical taskと両立するときにだけ「呼び出せる性能」として数える。**

これは万能な式ではない。各要素を機械的に掛けるのではなく、どの条件が判断を制限しているかを見つけるPASS_Bの点検法である。

### 4. 問いはどう変わるか

「何%被曝を減らすか」から、**「どのhazard・身体範囲・場所でその数字が成立し、警報後に装着して必要taskを維持できるか」**へ変わる。

## Thinking Trap

### 平均値の罠

平均を見ること自体が罠ではない。罠は、条件付きの性能を、どの条件でも呼び出せる総合点へ変えてしまうことにある。

避けるため、同じheadline性能を持つ案でも、次の四条件を入れ替えて比較する。

1. **Scenario:** hazardの強さだけでなく、spectrumやdurationが変わったらどうなるか。
2. **Coverage:** 守る身体部位・方向・場所を変えたらどうなるか。
3. **Availability:** 警報、保管、fit、装着時間を入れても使えるか。
4. **Critical task:** 唯一必要な作業を維持できるか。

一つを変えただけで選択が逆転するなら、平均値は結論ではなく入口である。

## Take One Thing

> **平均性能を見たら、scenarioとcoverageを変えて外れ方を確かめ、必要な瞬間に必要なtaskと両立して呼び出せるかを問う。**

災害用電源、医療機器、cybersecurity、保険、避難計画でも、平均性能と必要な瞬間の性能は一致しないことがある。

## Final Question

最初に選んだA/B/Cを、いま選び直すならどうするだろう。

> **あなたの選択を逆転させるscenario、coverageの空白、availabilityの制約、critical taskを一つずつ挙げると、どの防護を優先しますか。**

## Reflection

**Status: Pending**

半年後・1年後に、headline性能ではなく空欄がどう埋まったかを見る。

- 2026 Science Advances論文の全scenario・臓器別結果を確認できたか。
- SPE spectrum別の低減率は追加されたか。40.2%を下回る重要scenarioはあったか。
- Head、limbs、eyes等のcoverageと、体格・性別・fitによる差は測られたか。
- ISS試験で未完了だったtaskの内訳と、critical-task別評価は公開されたか。
- Donning time、警報余裕、収納、crew全員への配備、長時間着用は検証されたか。
- NASAは将来missionで採用したか。採用しなかった場合、性能、mass、space、scheduleのどれが判断を変えたか。

採否だけでなく、当時どのscenario、coverage、availability、taskが空欄で、その扱いが妥当だったかを振り返る。

## Sources

### Official / Primary / Research Sources

- [Houri et al., First Data-Based Evaluation of the Radiation Protection Capabilities of the AstroRad Vest as Flown Onboard Artemis I, IAC-2024](https://dl.iafastro.directory/event/IAC-2024/paper/90503/)
- [NASA, Artemis I—MARE investigation](https://www.nasa.gov/reference/artemis-i-2/)
- [NASA, Artemis I Space Radiation Research to Help Moon, Mars Explorers](https://www.nasa.gov/general/artemis-i-space-radiation-research-to-help-moon-mars-explorers/)
- [NASA, Artemis I Radiation Measurements Validate Orion Safety for Astronauts](https://www.nasa.gov/missions/artemis/artemis-1/artemis-i-radiation-measurements-validate-orion-safety-for-astronauts/)
- [Nature, Space radiation measurements during the Artemis I lunar mission](https://doi.org/10.1038/s41586-024-07927-7)
- [DLR, Matroshka AstroRad Radiation Experiment](https://www.dlr.de/en/me/research-and-transfer/projects-and-studies/mare)
- [NASA, International Space Station Status, May 2023](https://www.nasa.gov/wp-content/uploads/2023/10/nac-may2023-iss-final3-tagged.pdf)
- [NASA ISS Daily Summary Report, January 29, 2021](https://www.nasa.gov/blogs/stationreport/2021/01/29/iss-daily-summary-report-1-29-2021/)
- [NASA ISS Daily Summary Report, June 8, 2022](https://www.nasa.gov/?p=775286)
- [ISS National Laboratory, Wearable Radiation Shielding](https://issnationallab.org/case_study/wearable-radiation-shielding-astrorad-vest/)

### Reliable Reporting

- [Associated Press, Radiation vest tested on NASA moonshot can cut astronauts’ exposure in solar storms, study suggests, August 12, 2026](https://apnews.com/article/13e453c3e0502c0b0b3786b7fbc1a5cd)
- [Space.com, Radiation-shielding vest aced Artemis I lunar test, August 12, 2026](https://www.space.com/space-exploration/artemis/artemis-i-radiation-vest-astrorad-protect-astronauts-moon-mars-missions)

### Source Boundary

Artemis Iはmajor SPEを実測していない。61.8%と40.2%は、飛行測定で検証したmodelへ歴史的SPEを入力したeffective-dose推定である。約26kg、2026年Science Advances発表、対象臓器の追加説明、Artemis II非搭載はAP等の報道として扱う。最新論文全文、部位別全結果、個人差、donning time、警告余裕、収納・cost、未完了taskの内訳はUnconfirmedである。

Source Verificationの正式記録は`docs/SOURCE_VERIFICATION_2026-08-14_FALLBACK.md`。Initial Topicは`docs/SOURCE_VERIFICATION_2026-08-14.md`でHOLD_Cとなり、本稿には採用していない。

## Editor Notes — Not for Publication

### Source Verification PASS_Bの扱い

- Major SPEを実測したとは書かず、measurement-validated modelによる二つのhistorical scenario推定に限定した。
- Effective doseを全身・全放射線・全場所へ一般化せず、selective torso coverageとOrion locationを明示した。
- ISSの約75%を実用性scoreまたは25%失敗へ変換せず、task内訳未確認とROM制限を併記した。
- Failure modesを発生済みの事故でなく、設計・運用上の確認項目として扱った。
- Scenario-callable performanceをCの推奨理由にせず、A/B/C共通の点検フレームにした。

### Reader Transformation

- **Before:** Headlineの防護率を装備の総合性能として読む。
- **After:** Scenario、hazard、coverage、location、availability、critical taskを確認し、必要な瞬間に呼び出せる範囲だけをeffective protectionとして数える。
- **Level候補:** 3〜4。独立操作は成立するが、task内訳、donning、個人差等の空欄が残る。

### Draft Self-Assessment

- **Is it true?:** PASS_B候補。実測、model validation、scenario projection、報道、Inference、Unconfirmedを分離した。Science Advances全文未取得の限界を維持。
- **Is it fair?:** PASS候補。宇宙飛行士、crew、planners、engineers、medical teams、将来crewの異なる負担を、心理推測なしに配置した。
- **Is it useful?:** PASS候補。六欄と四条件比較は、災害電源、医療機器、cybersecurity等へ移植可能。
- **A/B/C Fairness:** PASS候補。A、B、Cすべてに守る価値、合理性、blind spot、費用、failure conditionがある。Cを共通フレームまたは正解にしていない。
- **Reader Transformation:** PASS_B候補。平均論からScenario-callable performanceへ移るが、万能理論とはしていない。
- **Insight Shift:** B候補。Source Verification評価を維持。
- **Thinking Trap:** PASS_B候補。「平均を見るな」で終わらず、scenario、coverage、availability、critical taskを変えて選択逆転を探す操作にした。
- **Take One Thing:** PASS候補。一文で他分野へ持ち運べる。
- **Pilot #3 overlap:** MEDIUMだが境界維持。配分、残余risk、回復時間、将来選択肢を中心にしていない。
- **2026-08-13 overlap:** MEDIUM-LOW。原因仮説、識別証拠、主体・手段割当ではなく、同一装備の条件付き実効性能を中心にした。
- **Independent Editorial Review:** NOT PERFORMED。
- **Build / HTML / Git operations:** NOT PERFORMED。
