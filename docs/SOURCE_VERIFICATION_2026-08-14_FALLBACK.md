# World Insight 2026-08-14 — Fallback Source Verification

- **Date:** 2026-08-14
- **Selected Topic:** 稀な危険への防護を、平均効果だけで選んでよいか——宇宙放射線防護を「効く場面・外れる場面・使える条件」から考える
- **Daily Editorial:** `docs/DAILY_EDITORIAL_2026-08-14.md`
- **Initial Topic Verification:** `docs/SOURCE_VERIFICATION_2026-08-14.md`（HOLD_Cの履歴を保持。本書は置換しない）
- **Article:** `articles/2026-08-14-scenario-callable-performance.md`
- **Evidence cutoff:** 2026-08-14（日本時間）
- **Scope:** 唯一のFallback Source Verification。記事、Review、Build、HTML、Publish、Pipeline追加修正、Git操作は未実施。

## Executive Conclusion

**Source Verification: PASS_B — scenario差とdeployabilityを一次資料から具体化でき、限定条件付きで独立した判断能力が成立する。**

報道の「約60%低減」は、Artemis Iで大規模な太陽粒子事象（SPE）を実測して得た全身・全状況の平均ではない。Artemis Iでは大規模SPEが発生しなかったため、研究者はOrionがinner Van Allen beltを通過した際のphantom測定でMonte Carlo modelを検証し、そのmodelへ歴史的SPEのsolar energetic proton spectrumを入力した。seat 3/4付近のOrion条件で推定したeffective doseは、1972年8月型で233.6から89.4 mSv（61.8%低減）、1989年10月型で249.9から149.4 mSv（40.2%低減）だった。同じvest、同じ宇宙船位置でもparticle spectrumが違えば約22 percentage pointsの性能差がある。

AstroRadは全身suitでもhelmetでもなく、female phantomのlungs、stomach、uterus、spine等の測定と、radiosensitive organs/tissuesへのselective shieldingを用いるtorso garmentである。従って「被曝を60%減らす」を頭部、四肢、EVA、全方向、galactic cosmic rays（GCR）、すべての性別・体格・臓器へ一般化できない。報告値は個別臓器doseでなく、modelled effective doseである。

利用可能性も性能と別に確認できる。AstroRadは約26 kg。ISSのCHARGE試験では運動、range of motion、日常作業、睡眠等を有人評価し、NASA資料は搭乗作業の約75%を完了できた一方、hips、shoulders、neckのrange of motion制限を記録した。これは「動ける／動けない」の二択ではなく、危険時にどのtaskをvest着用のまま継続できるかがcoverageの一部であることを示す。ただしdonning time、SPE警告から必要着用までの時間、全mission task別成績、量産cost、保管volume、配布・訓練は公開一次資料から確定できない。

独自の中心操作は「平均だけを見るな」ではなく、**Effective protection = Scenario-specific dose reduction × body/organ coverage × timely usability**として、同じ装備の性能をevent spectrum、場所、身体coverage、利用可能taskで読み直すことにある。Pilot #3の資源配分・残余risk・回復時間、2026-08-13の原因仮説と政策手段の適合とは中心操作が異なる。ただし記事が「どのriskを残すか」または複数手段のPolicy-Tool Fitへ広がれば差は消えるためPASS_Bとする。

## Verification Labels

- **Confirmed Fact:** NASA、DLR、査読論文・学会paper等で確認したmission、測定、model、数値、試験結果。
- **Official / Researcher Statement:** NASA、研究機関、研究者が説明した目的・解釈。独立した効果確認と同一ではない。
- **Reliable Reporting:** AP等が論文・関係者取材に基づき報じた情報。一次資料で確認できない細部はここに残す。
- **Inference:** 複数資料から導く編集上の判断枠組み。物理式、NASA運用基準、医学的助言として扱わない。
- **Unconfirmed:** 公開一次資料で確認できない運用・費用・個人差・将来採用事項。

## 1. Sources Reviewed

### Primary / Official / Research

| Source | Establishes | Limit |
|---|---|---|
| [Houri et al., First Data-Based Evaluation of AstroRad, IAC-2024 paper 90503](https://dl.iafastro.directory/event/IAC-2024/paper/90503/) | phantom、detector位置、model validation、1972/1989 SPE effective-dose推定、61.8%/40.2% | Conference paper。2026 Science Advances全文を検索で取得できず、最新論文の全table・査読詳細は未確認 |
| [NASA, Artemis I overview—MARE](https://www.nasa.gov/reference/artemis-i-2/) | NASA、DLR、ISA、Lockheed Martinの協力、Zohar/Helga、vest試験目的 | 最新効果量は示さない |
| [NASA, Artemis I Space Radiation Research](https://www.nasa.gov/general/artemis-i-space-radiation-research-to-help-moon-mars-explorers/) | 2体のfemale phantom、5,600超のpassive sensors、34 active detectors、storm shelter外での活動可能性という目的 | 実際のSPE時運用を実証しない |
| [NASA, Artemis I radiation measurements](https://www.nasa.gov/missions/artemis/artemis-1/artemis-i-radiation-measurements-validate-orion-safety-for-astronauts/) | Orion内固定detectorとMARE phantom、spacecraft orientationによるdose variation | AstroRadの2026推定値の全文ではない |
| [Nature, Space radiation measurements during Artemis I](https://doi.org/10.1038/s41586-024-07927-7) | Orion内の放射線場、orientation・shieldingによる差、female phantomを含む測定基盤 | 大規模SPEなし。AstroRadの最新SPE効果そのものが主題ではない |
| [DLR, MARE project](https://www.dlr.de/en/me/research-and-transfer/projects-and-studies/mare) | female phantomとdetectors、vest有無のexperiment design | headline効果と有人運用性を示さない |
| [NASA ISS status report, May 2023](https://www.nasa.gov/wp-content/uploads/2023/10/nac-may2023-iss-final3-tagged.pdf) | 約75%のonboard tasks完了、hips/shoulders/neckのrange-of-motion制限、minor structural modifications | sample、task一覧、統計的不確実性が資料抜粋では不明 |
| [NASA ISS daily report, 29 Jan 2021](https://www.nasa.gov/blogs/stationreport/2021/01/29/iss-daily-summary-report-1-29-2021/) | vest着用でexerciseを実施 | performance qualityや長時間緊急運用を示さない |
| [NASA ISS daily report, 8 Jun 2022](https://www.nasa.gov/?p=775286) | vest有無でrange-of-motion testを実施 | 詳細scoreを示さない |
| [ISS National Laboratory, AstroRad case study](https://issnationallab.org/case_study/wearable-radiation-shielding-astrorad-vest/) | mobility、fit、comfort、exercise、daily tasksの評価、design refinement | 開発支援機関のcase studyであり、全raw dataはない |

### Reliable Reporting

| Source | Reports | Limit |
|---|---|---|
| [AP, 12 Aug 2026](https://apnews.com/article/13e453c3e0502c0b0b3786b7fbc1a5cd) | Science Advances発表、26 kg、target organs、1972型約60%・1989型約40%、Artemis II非搭載、ISS comfort/function test | 論文全文・model input・task dataの代替ではない |
| [Space.com, 12 Aug 2026](https://www.space.com/space-exploration/artemis/artemis-i-radiation-vest-astrorad-protect-astronauts-moon-mars-missions) | 開発者によるselective coverage、hours-long use、sleep、storm shelterとの比較説明 | 企業・共著者statementを独立実証へ格上げしない |

## 2. Today's News and Experiment

### Confirmed Facts

1. MAREはNASA Artemis I（2022年11–12月、約26日）で、Orion内の2体のlife-size female torso phantom、Helga（unshielded）とZohar（AstroRad着用）を飛行させた。
2. 計画時NASA資料では2体に5,600超のpassive sensorsと34 active radiation detectorsを搭載した。
3. AstroRadはStemRadとLockheed Martinが開発し、NASA、DLR、Israel Space Agency等がMAREへ参加・資金提供した。
4. vestはtorsoのradiosensitive organs/tissuesへ異なる厚さのhydrogen-rich shieldingを配置するselective designで、全身suitやhelmetではない。
5. MAREのactive detectorsはphantom表面・vest外側のkey locations、および両phantomの各lung、stomach、uterus、spineに配置された。IAC paperのmodel validation sampleはM-42 N=16、CAD N=18。
6. Artemis Iではmajor SPEが発生しなかった。実飛行中に「1972年型stormをvestあり／なしで直接測定」したのではない。
7. 研究者はinner Van Allen belt transitの測定でtransport simulationを検証した。simulationとmeasurementのpercent differenceはM-42で−2.2±12.5%、CADで−3.1±14.9%。これはvest効果のrangeではなく**model validation差**である。
8. 検証modelへsolar energetic protonsを入力し、Orion seats 3/4付近で、1972年8月型SPEのeffective doseを233.6→89.4 mSv（−61.8%）、1989年10月型を249.9→149.4 mSv（−40.2%）と推定した。
9. ISS上では有人のcomfort/human-factors試験が行われ、exercise、range of motion、日常task等をvest有無で評価した。NASAの2023資料は約75%のonboard-task categoriesを完了でき、hips、shoulders、neckにrange-of-motion制限があったとする。

### Reliable Reporting

- APは2026年8月12日、Science Advancesに新研究が発表され、1972型で約60%、1989型で約40%のdose reductionを示したと報じた。
- APはvestを約57 lb / 26 kg、lungs、stomach、bone marrow、breasts、ovaries等をtargetにすると報じた。個別臓器別の最新数値は論文全文で確認できていない。
- APは短期・space制約を理由にArtemis IIへ搭載されず、将来missionでの採用可能性があると報じた。NASAの正式採用決定ではない。

### Inference

- 「60%」は単一の平均性能ではなく、一つのhistorical spectrum、Orion内位置、phantom/model、effective-dose weightingを組み合わせたscenario estimateと読むべきである。
- 防護の実効性はdose reductionだけでなく、危険発生時にdonningでき、必要taskを継続でき、守る必要のある部位がcoverage内にあることへ依存する。
- ISS task completion 75%は「実用性75%」ではない。task selection、completion quality、緊急時優先taskを確認しなければoperational readinessへ変換できない。

### Unconfirmed

- 2026 Science Advances論文のDOI、全本文、peer-review history、全supplementary tables（検索結果で同定できなかった）。
- detector全5,600個の部位別distribution、vest下とvest外の全range、個別臓器別dose reduction。
- sex、body size、anatomy、fitによる性能差。female phantom一組からpopulation distributionは得られない。
- head、arms、legs、eyes、skin、specific bone-marrow sites等の未被覆部位別risk。
- donning/doffing time、収納volume、保管場所、crewごとのfit、訓練時間、unit cost、missionへのmass/volume trade。
- SPE warning lead timeと、vest装着完了までのoperational margin。
- vest着用で完了できなかった約25%のtask内訳、mission-criticality、completion quality、疲労・heat・長時間wearの定量値。
- Orion storm shelterとvestを同じ条件で比較した独立数値、併用時の追加効果。
- NASAによるflight-certified operational equipmentとしての採用、future mission搭載決定。

## 3. What the “Average” Contains

| Requested dimension | Verified content | Missing / limit |
|---|---|---|
| What average? | 1972/1989 historical SPE spectrumを用いた**modelled effective dose**のvest有無比較 | 全mission平均、全身absorbed dose平均、actual storm measurementではない |
| Scenario count | 公開conference resultで明示されるhistorical SPEは2件 | Science Advances全文の追加scenario数は未確認 |
| Measurement positions | surfaces/vest exterior、lungs、stomach、uterus、spine。seats 3/4 vicinity | 全5,600 sensorの位置別結果は未取得 |
| Body parts | targeted radiosensitive torso organs/tissues。female phantom | 全身coverageでない。個別organ effectのfull tableは未確認 |
| Radiation | Artemis validationはinner Van Allen belt、projectionはsolar energetic protons / SPE | GCR全般、EVA、surface habitat、neutron/secondary componentsへの一般化不可 |
| Time | historical event-integrated effective dose estimate。Artemis I約26日 | peak dose rate、donning timing、partial wear、event途中装着は不明 |
| Individual variation | female anatomical phantom pair | n=1 shielded vs n=1 unshielded anatomy。sex/size/fit variationは不明 |
| Distribution/range | scenario間で61.8% vs 40.2%。model validation差±12.5/14.9% | 後者をprotection uncertaintyと解釈不可。部位別range/worst case未確認 |
| Worst case | 2例中は1989型が低減率40.2%で低い | 未知のSPE spectrum、より高energy event、uncovered organ、EVAが真のworst caseかは未確認 |

**Finding:** 「平均値の内側」は統計的な個人分布だけではない。event spectrum、spacecraft shielding/orientation、seat location、organ weighting、garment coverage、装着状態の条件付き結果である。

## 4. Scenario Differences and Coverage

### Scenario difference

- 1972型: unvested 233.6 mSv、vested 89.4 mSv、61.8% reduction。
- 1989型: unvested 249.9 mSv、vested 149.4 mSv、40.2% reduction。
- unvested doseは1989型の方が高い一方、percentage reductionは1972型の方が大きい。初期hazard magnitudeだけではshield benefitの割合が決まらない。
- 理由の詳細はfull paperで確認できないが、historical SPEごとのparticle energy spectrumが異なり、shielding effectivenessが変わることと整合する。因果説明はInferenceに留める。

### Coverage

- **Whole body:** NO。torso-focused vestでhelmet/full-body suitではない。
- **Organs:** lungs、stomach、uterus、spineにinternal active detectors。報道・design explanationはbone marrow、breasts、ovaries等のradiosensitive tissuesをtargetとする。
- **Direction:** vestはsolid-angle coverageを最大化するとするが、全方向一様ではない。Orion structure、orientation、seat、body postureもincoming fieldを変える。
- **Radiation type:** 主用途はSPEのsolar energetic protons。Artemis I validation fieldとhistorical SPE simulationを分ける。GCR長期防護への同じ割合の一般化は不可。
- **Location:** Orion seats 3/4 vicinity。lunar surface、Gateway、Mars transit、EVAへ同じ数値を移さない。

## 5. Availability / Deployability

| Condition | Confirmed | Limit / failure mode |
|---|---|---|
| Pre-wear / donning | ISSで複数crewが着用しexercise・daily tasks・sleep等を評価 | 緊急donning time、self-donning、サイズ別時間は未確認 |
| Warning time | SPEはunpredictableという運用前提 | actual warning lead timeと装着marginは未確認。高energy particlesが先着すればfailureになり得るが本資料では定量不可 |
| Mass | 約26 kg（AP/開発者情報） | microgravityでもinertia、launch mass、storage volumeは消えない。mission allocationは未確認 |
| Mobility | 約75%のonboard activities完了。hips/shoulders/neckにROM restriction | 残る25%のtask、emergency response、fine motor work、fatigueは不明 |
| Wear duration | 有人ISS testing、sleepを含む使用報告。hours-longを想定との研究者statement | continuous duration、thermal load、hygiene、individual toleranceの定量値なし |
| Storage / distribution | Orion phantomへ搭載できた | crew全員分の収納、取り出し位置、inspection、maintenanceは不明 |
| Training | ISS test protocolで運動・ROM・task評価 | operational training requirementは不明 |
| Cost | 未確認 | vest mass/volumeとspacecraft shielding/shelterのopportunity costを比較不可 |

**Deployability verdict: PASS_B.** 有人環境でtask・mobilityを試験し、具体的な制限を確認できるため単なる机上性能ではない。しかしemergency availabilityを確定するには警報、donning、収納、crew全員、critical-task別の空欄が大きい。

## 6. Extreme Events and Failure Modes

1. **Spectrum mismatch:** 1972型と1989型で効果率が大きく異なる。未知eventのenergy spectrumがvest shieldingへ不利ならheadline率を下回り得る。
2. **No actual major SPE:** Artemis Iはmajor SPEを経験していない。modelが測定fieldで一致しても、extreme SPE projectionにはmodel/physics/input uncertaintyが残る。
3. **Partial-body failure:** 頭部・四肢等の未被覆部分またはtarget外organがdecision-limitingなら、effective-dose平均が良くても必要なprotectionにならない可能性。
4. **Late availability:** 警告から装着までが短い、vestが遠い、crew分不足、fit不良ならphysical capabilityを呼び出せない。
5. **Task incompatibility:** neck/shoulder/hip restrictionにより、緊急task、maintenance、medical response等ができなければmission riskを別経路で増やす。
6. **Location transfer:** Orion seat内の数値をEVA、lunar surface、別spacecraftへ移すとshielding geometryを失う。
7. **Hazard substitution:** SPEを強く守っても長期GCRを同率で解決しない。
8. **Extreme-only overfit:** 重い・厚いdesignをrare worst caseだけへ最適化すると、収納、daily operations、crew全員への配備、他安全装備のmassを圧迫し得る。具体的mission tradeはUnconfirmed。

## 7. A/B/C Fairness

### A — 累積曝露を抑える

- Rational value: cancer等のstochastic long-term riskに関わるmission全体の累積doseを下げる。
- What it sees: 頻度・durationを含む総負担。
- What it misses: 短時間のacute SPE、uncovered organ、model外event。
- Cost: 長時間wearまたは常設shieldingならmass、mobility、task burdenが積み上がる。
- Failure condition: 平均doseは下がってもdecision-limiting extreme eventやorgan doseが閾値を越える。

### B — 重大SPE時の臓器防護を優先する

- Rational value: rareだが高線量のeventでacute・long-term harmを抑える。
- What it sees: event spectrumとradiosensitive organ coverage。
- What it misses: GCR、未被覆部位、通常運用、未知spectrum。
- Cost: rare event専用の26 kg equipment、storage、fit、training、他shieldingとのmass/volume competition。
- Failure condition: actual eventがdesign spectrumと異なる、警告・装着が間に合わない、critical taskができない。

### C — 緊急時のtask継続を優先する

- Rational value: shelterに固定されず、mission-critical actionを続ける可能性。
- What it sees: donning、mobility、task completion、wear duration。
- What it misses: 「使える」がdoseを十分下げるとは限らず、未被覆organ・unknown eventを見落とす。
- Cost: shielding thicknessを減らしてmobilityを得ればdose protectionを失い得る。task trial、training、crew-specific fitが必要。
- Failure condition: taskはできてもdose reductionが不足、または75%というaggregateが本当に必要な25%を隠す。

### Revision

元のA「平均被曝」は平均値を正解視するように読めるため、**A「累積曝露を抑える」**へ修正する。Bは**「重大SPE時の臓器防護」**、Cは**「緊急時のtask継続」**とし、いずれも独立した目的、blind spot、failure conditionを持たせる。Cは現実的正解ではなく、dose不足という固有failureを持つ。

## 8. Overlap Audit

### Pilot #3 — Residual Risk and Recovery Time

- Theme overlap: **LOW〜MEDIUM**。安全保障ではないが、稀なriskと防護資源を扱う。
- Judgment overlap: **MEDIUM**。どのscenario・部位が未被覆かはresidual riskに触れる。
- Difference: Pilot #3は希少資源を複数戦域へ配り、他者へ残すrisk、将来選択肢、再調達・回復期限を決めた。本Fallbackはvestを誰へ配るか、在庫、回復期限を扱わず、**一つの性能値をscenario × coverage × timely usabilityへ再定義する測定・運用判断**が中心。
- Stop boundary: crew間配分、vest数、mission優先順位、回復期限が中心ならPilot #3の再演としてHOLD_C。

### 2026-08-13 — Policy-Tool Fit

- Theme overlap: **LOW**。物価政策とspace radiation。
- Judgment overlap: **MEDIUM-LOW**。条件を分けて手段が届くか見る一般操作は共通。
- Difference: 8月13日号は集計値から原因仮説を識別し、正式主体・政策手段・time lag・side effectを割り当てた。本Fallbackは原因を推定せず、**既に同じ防護具でもhazard spectrumと利用状態によってeffective performanceが変わることを、scenario-specific estimateとhuman-factors evidenceで読む。** 複数政策手段の割当ではない。
- Stop boundary: vest、shelter、warning、mission designを原因別に割り当てる記事へ広げればPolicy-Tool FitになりHOLD_C。

## 9. Thinking Trap and Reader Transformation

### Thinking Trap

- Candidate: **平均値の罠**
- Evaluation: **PASS_B**
- Not sufficient: 「平均は分布を隠す」「外れ値も見よう」だけでは一般論であり不採用。
- Specific operation: **同じ装備のheadline値を、(1) hazard spectrum別のdose reduction、(2) protected/unprotected anatomy、(3) location/orientation、(4) timely donning、(5) critical-task completionへ展開し、最もdecision-relevantなcellが平均と逆の判断を示さないか確認する。**
- Evidence anchor: 61.8% vs 40.2%、torso-selective coverage、major SPE非遭遇、task completion約75%とneck/shoulder/hip restriction。
- Limitation: Science Advances全文とtask-level raw dataがないため、failure distributionを完全には作れない。

### Reader Transformation

- Before: 「約60%低減」をvestの総合的な有効性として読む。
- After: 数字のscenario、radiation spectrum、spacecraft location、body/organ coverage、model/measurement境界を確認し、さらに**危険時に装着して必要taskを実行できる範囲までをeffective protectionに含める。**
- Independent ability: **Scenario-callable performanceを読む。** laboratory/model performanceと、必要な瞬間に呼び出せるperformanceを一つの評価へ結ぶ。
- Level candidate: **3〜4 / PASS_B。** 新しい操作は成立するが、運用データの空欄が多く完全なcoverage mapにはならない。

## 10. Insight Shift and Final Decision

### Insight Shift

1. Initial premise: 高い平均低減率の防護具ほど安全である。
2. Why insufficient: 同じvestでもhistorical SPEで61.8%と40.2%に分かれ、全身を覆わず、実flightでmajor SPEを経験せず、有人taskには可動域制限があった。
3. New view: **防護性能を一つの数字でなく、scenario-specific dose reduction × body/organ coverage × timely usabilityとして読む。**
4. Changed question: 「何％減らすか」から、「どのevent・部位・場所でその数字が成立し、警告後に装着して必要taskを続けられるか」へ。

- Evidence quality: **B**
- Independence: **A候補だが境界条件付き**
- **Final Insight Shift: B**

### Final Decision

**PASS_B**

- Article may be drafted next: **YES, but not in this step.**
- NO_PUBLISH required now: **NO**
- Initial Topic HOLD_C retained: **YES**
- Fallback Attempts: **1 / limit reached**

### Article Conditions

1. 「60%」をactual SPE measurement、全身平均、全radiation protectionと書かない。
2. 1972型61.8%と1989型40.2%、major SPE非遭遇、model validationとSPE projectionを必ず同じ説明単位に置く。
3. torso-selective coverageと未確認部位を明示し、female phantom pairをpopulation distributionへ一般化しない。
4. task completion約75%を「実用性75%」と書かず、ROM restrictionとtask内訳未確認を併記する。
5. A/B/Cは累積曝露、重大SPE臓器防護、緊急task継続へ修正し、Cを正解化しない。
6. vest配分、残余risk・回復期限を中心にしてPilot #3へ戻らない。
7. 複数対策を原因・主体・手段へ割り当てて8月13日Policy-Tool Fitへ戻らない。
8. Science Advances全文が記事Draft前にも取得できなければ、IAC paperとNASA資料をConfirmed coreにし、2026論文の追加主張をAP/Unconfirmedへ限定する。

### Stop Condition

記事段階で上記境界を守れず、中心が一般的な「平均だけを見るな」、Pilot #3のrisk配分、または8月13日号のPolicy-Tool Fitへ戻る場合は、FallbackをHOLD_Cへ戻し、第三候補へ進まず`Daily Result: NO_PUBLISH`の人間確認へ進む。
