# World Insight 2026-08-15 — Fallback Source Verification

- **Date:** 2026-08-15
- **Selected Topic:** 被害が増えたとき、対策を足す前にどの再発経路を閉じるか——民間被害をfailure patternとcontrol loopから考える
- **Daily Editorial:** `docs/DAILY_EDITORIAL_2026-08-15.md`
- **Initial Topic Verification:** `docs/SOURCE_VERIFICATION_2026-08-15.md`（HOLD_Cの履歴を保持。本書は置換しない）
- **Article:** NOT CREATED
- **Evidence cutoff:** 2026-08-15（日本時間）
- **Scope:** 唯一のFallback Source Verification。記事Draft、Editorial Review、Human Read、Build、HTML、Publish記録、Pipeline / Builder / template / CSS変更、Git操作は未実施。

## Executive Conclusion

**Source Verification: HOLD_C — civilian harmの増加、長距離missile・droneによる都市・住宅被害、warning・shelter・interception・rescue controlの存在、具体的な制度・設備変更は確認できる。しかし複数事案をdetectionからrescueまで同じ粒度で再構成できず、共通control breakpoint、変更との因果対応、変更後のclosure evidenceを確認できない。**

UN Human Rights Monitoring Mission in Ukraine（HRMMU）は、2026年6月に少なくとも293人死亡・1,990人負傷を確認し、長距離missile・droneが全casualtyの45%を占め、主に前線から離れたurban centresで被害を生んだと報告した。7月初めのKyiv攻撃については、74 missilesと約500 attack drones、住宅直撃、建物collapse、shelterに入って生存した家族を確認している。APは7月の437人死亡・2,610人負傷と、8月14日のSumy regionでjet-powered droneが住宅を攻撃し母子が死亡した事案を報じた。ただし2026年7月のHRMMU月次一次資料はEvidence cutoff時点で公式siteから取得できず、7月数値はReliable Reportingに留める。

複数事案には「long-range weapon / drone → populated area or home impact → collapse/fire → civilian casualty」というoutcome-level patternがある。しかし、個別事案ごとにdetection、interception attempt、warning timing、住民の受信・行動、shelterの距離・accessibility、impact、rescue response timeを連結した一次資料はない。住宅へ命中したことだけからinterception、warning、shelterのいずれかが失敗したとは判定できない。

Ukraineにはair-raid warning guidance、shelter制度、interception、emergency responseが存在する。2026年にはshelter法改正、7 shelter projects、Zaporizhzhiaのanti-drone routes・modular shelters、施設向けwarning guidance等の具体的変更も確認できる。しかし、これらは対象事案のafter-action reviewに基づくbreakpoint correctionとして対応付けられず、変更後の同条件比較、response time、shelter reach、casualty pathway reduction、audit結果も得られない。absence of later reported harmをclosureへ格上げできない。

したがって、独自のReader Transformation「反復経路 → breakpoint → control change → closure」は概念上8月14日号と異なるが、Evidence上は実行できない。記事化すれば、scenario・availabilityの一般評価、資源配分、control ownerのModule分解、原因と手段の適合へ戻るか、空欄を推測で埋めることになる。FallbackのStop Conditionを適用し、第三候補へ進まずNO_PUBLISHの人間確認へ送る。

## Verification Labels

- **Official / Primary Source:** HRMMU、Ukraine政府・議会、National Police、State Emergency Service、地方行政等の原資料。組織自身の集計・措置・説明であり、他のcontrolのfailureや因果を自動的に証明しない。
- **Reliable Reporting:** AP等が当局・現場取材に基づき報じた事項。一次資料を取得できない数値・事案詳細はこの分類に留める。
- **Analytical / Context:** 複数資料を比較するためのharm-pathway表や編集上の分類。公的な事故調査結果ではない。
- **Unconfirmed / Unknown:** 公開資料で確認できないtiming、行動、access、原因、before/after、closure。推測で埋めない。

## 1. Sources Reviewed

### Official / Primary Sources

| Source | Establishes | Limit |
|---|---|---|
| [HRMMU, Protection of Civilians — June 2026](https://ukraine.ohchr.org/en/Protection-of-Civilians-in-Armed-Conflict-June-2026) | 293 killed、1,990 injured、long-range weapons 45%、weapon category・region別集計 | 個別事案のwarning、shelter、interception、rescue chainを示さない |
| [HRMMU, Kyiv attack, 2 Jul 2026](https://ukraine.ohchr.org/en/Civilian-Casualties-Soar-as-Ukraine-Comes-Under-the-Deadliest-Attack-in-Weeks-UN-Human-Rights-Monitors-Say) | 74 missiles、約500 drones、住宅直撃・collapse、shelterへ入った家族の生存、ongoing rescue | shelter利用者と非利用者の比較、warning時刻、interception、response timeは不明 |
| [HRMMU, Kyiv attack, 6 Jul 2026](https://ukraine.ohchr.org/en/Another-Deadly-Overnight-Attack-in-Kyiv-Amid-Rising-Civilian-Casualties) | long-range missiles・dronesによるurban harmの継続pattern、impact siteとhospital follow-up | control breakpointやafter-action changeを特定しない |
| [National Police, Sumy attacks, 3 Jul 2026](https://su.npu.gov.ua/news/piat-liudei-zahynulo-sered-iakykh-dytyna-politsiia-dokumentuie-naslidky-vorozhykh-obstriliv-sumshchyny) | droneが住宅へ命中し4人死亡等、複数communityのdamage・casualty | detection、warning、resident action、shelter、response timingなし |
| [National Police, Sumy attacks, 4 Jul 2026](https://npu.gov.ua/news/4-liudyny-zahynuly-sered-nykh-dytyna-shche-45-osib-zokrema-9-ditei-poraneni-cherez-vorozhi-ataky-na-sumshchyni-politsiia-dokumentuie-naslidky) | drones・guided bombs、住宅・病院・学校等のdamage、police・rescuersの現場活動 | 各casualtyとcontrol chainを対応付けない |
| [National Police, Sumy drone strike, 20 Jul 2026](https://npu.gov.ua/news/politsiia-dokumentuie-naslidky-ataky-rosiiskoho-bezpilotnyka-po-sumakh-sered-trokh-postrazhdalykh-dvoie-ditei) | apartment impact、children injured、police response、shelter/two-wall guidance | guidanceが攻撃前に届いたか、実行されたか、結果を変えたか不明 |
| [National Police, Seredyna-Buda rescue, 12 Feb 2026](https://npu.gov.ua/news/ataka-rosiiskykh-bezpilotnykiv-po-sumshchyni-politseiski-riatuvaly-liudei-pid-chas-povtornoi-zahrozy) | house impacts、fire、evacuation、repeat-drone warning中にfamilyをbasementへ移動、hospitalization | 同一event内のsuccessful response例。system-level changeやlater closureではない |
| [Sumy Regional Administration, drone detection, 21 Jul 2026](https://www.sumy.sm.gov.ua/index.php/uk/8-novini/28536-za-tizhden-u-nebi-nad-sumshchinoyu-viyavili-1090-vorozhikh-bezpilotnikiv) | 一週間で1,090 drones検知、900超をdestroy/suppress、83%と報告 | target、撃墜地点、debris、civilian outcomeを対応付けず、17%をfailureとも呼べない |
| [Ukraine law No. 4778-IX, 10 Feb 2026](https://zakon.rada.gov.ua/laws/show/4778-20) | warning system維持・modernization、public/mobile shelters、civil-protection制度の具体的改正 | 多くは2026-09-08施行予定。本件後の変更でもclosure結果でもない |
| [Interior Ministry, seven shelter projects, 12 Feb 2026](https://mvs.gov.ua/news/miznarodna-koaliciia-ukrittiv-civilnogo-zaxistu-praciuje-zatverdzeno-7-projektiv-zi-zvedennia-ta-modernizaciyi-ukrittiv) | Sumy等を含む7 shelter construction/modernization projectsの承認 | completion、利用率、casualty effect、incident linkage不明 |
| [Zaporizhzhia Regional Administration, passive protection, 23 Jun 2026](https://www.zoda.gov.ua/news/79572/kompleksniy-pasivniy-zahist-zaporizhzhya-antidronovi-shlyahi%2C-ukrittya-ta-bezpeka-kritichnoji-infrastrukturi.html) | anti-drone routes、modular shelters、infrastructure protectionの導入 | Sumy/Kyiv事案と別地域。before/after outcome・closureなし |
| [Civil Protection Research Institute, shelter standards, 23 Jun 2026](https://indcz.dsns.gov.ua/news/bezpecnisi-ukrittia-ta-nadiine-sporiadzennia-iak-onovliuiutsia-standarti-civilnogo-zaxistu) | backup ventilation等の具体的shelter standard研究・承認段階 | 実装・効果・incident-driven changeを示さない |
| [Shostka City Council, drone-attack guidance, 13 Jul 2026](https://shostka-rada.gov.ua/uvaga-pravyla-povedinky-gromadyan-pid-chas-atak-bpla/) | shelter移動、windows回避、lift禁止、all-clearまで待機等のguidance | 到達率、理解、遵守、outcomeなし |

### Reliable Reporting

| Source | Reports | Limit |
|---|---|---|
| [AP, Russian drones kill a woman and 9-year-old son, 14 Aug 2026](https://apnews.com/article/66f000409c6648239936b628a9eae0f5) | Sumy regionでjet-powered droneがhomeを攻撃、29歳女性と9歳息子死亡、父・祖母を含む4人負傷、7月437 killed / 2,610 injured | exact locality、warning、shelter、interception、response time、HRMMU July原表を示さない |

### Analytical / Context

- 「attack → detection/interception → warning → civilian response → shelter → impact → rescue」というchainは本検証の編集用モデルであり、Ukraine当局の正式incident-classificationではない。
- HRMMUが確認する反復patternはweapon use、populated-area exposure、casualty outcomeのlevelである。control breakpointの反復patternではない。
- 83% detection/destruction/suppressionとcivilian casualtiesは母集団、場所、target、期間が異なり、単純なfailure rateや防護効果へ変換できない。

## 2. Repeated Harm Pathway

### What can be confirmed

1. **Repeated attack type:** HRMMUはlong-range missiles・dronesがurban centresでcivilian casualtiesの主要因であることを確認する。
2. **Repeated exposed object:** Kyiv、Sumy等でresidential buildings・homesへのdirect impactまたはdamageが複数記録される。
3. **Repeated harm mechanism after impact:** building collapse、fire、debris、direct blastによりdeath・injury・trapped residentsが生じる事案がある。
4. **Rescue presence:** police、rescuers、medical teamsがimpact後に活動した事案は確認できる。

### What cannot be confirmed as a common pathway

| Chain stage | Cross-incident evidence | Finding |
|---|---|---|
| Attack | weapon categoryとmass attackは複数資料にある | **CONFIRMED at aggregate level** |
| Detection | Sumyのaggregate detection数のみ | **NOT LINKED to casualty incidents** |
| Interception | destroy/suppress aggregateのみ | **NOT LINKED; no shared failure finding** |
| Warning issued | general alert・guidanceは存在 | **INCIDENT TIMING UNKNOWN** |
| Warning received | 個人別・建物別記録なし | **UNKNOWN** |
| Civilian response | Kyivの一familyがshelterへ入った例 | **ISOLATED EXAMPLE, no common pattern** |
| Shelter availability | 制度・project・guidanceは確認 | **INCIDENT-SPECIFIC AVAILABILITY UNKNOWN** |
| Shelter accessibility | distance、mobility、opening、capacityのincident dataなし | **UNKNOWN** |
| Impact | residential impact・collapse・fireが複数 | **CONFIRMED** |
| Rescue / medical | 現場活動・hospitalizationは複数 | **PRESENCE CONFIRMED; timing/effect unknown** |

**Repeated Harm Pathway verdict: INSUFFICIENT.** 共通して確認できるのはweaponがpopulated area・residential objectへ到達し、impact後にcasualtyが生じるoutcome-level sequenceまでである。warning-to-shelter、interception、rescueのどこが繰り返し破断したかは確認できない。

## 3. Control Breakpoint

| Control | Existence | Function confirmed | Possible non-function | Evidence-insufficient boundary |
|---|---|---|---|---|
| Detection | Sumyで週1,090 drones検知と報告 | aggregate detectionは機能 | casualty eventがundetectedだった可能性はあるが推測 | individual track、radar coverage、warning linkage不明 |
| Interception / suppression | 900超、83%をdestroy/suppressと当局報告 | aggregate actionは機能 | non-intercepted weaponがimpactした可能性はある | target別engagement、debris harm、counterfactual outcome不明 |
| Warning | national/local alertとguidanceが存在 | alertsが発出される制度は確認 | warning不足・短時間の可能性はある | event timestamp、receipt、lead time不明 |
| Warning-to-shelter connection | 行動guidanceと責任者algorithmが存在 | Kyivの一familyのshelter利用・生存例 | connectionが切れた事案を推測不可 | reach、understanding、travel time、compliance不明 |
| Shelter availability | law、projects、modular/public shelter policy | 個別shelterの存在例はあり得る | casualty buildingに適切なshelterがなかった可能性 | address-level map、capacity、open status不明 |
| Shelter accessibility | accessibilityを含むpolicy direction | 今回事案での機能確認なし | mobility、locked door、distance等は全て仮説 | user-level access dataなし |
| Rescue / emergency response | police、DSNS、medical responseが存在 | 現場活動、evacuation、hospitalizationは確認 | delayやcapacity不足の可能性はある | dispatch/arrival/extrication/transport time、preventable death不明 |

**Control Breakpoint verdict: NOT IDENTIFIABLE.** 被害が発生したことは、上流controlのfailureを一意に示さない。兵器量・軌道・debris、住宅直撃、退避不能、shelter性能、救助限界等の複数説明を区別できない。

## 4. Control Change

### Concrete changes or deployments confirmed

- Law No. 4778-IXはwarning system modernization、public-access/mobile shelters、safety centres等を制度化した。ただし多くの施行は2026年9月予定。
- Interior MinistryはSumyを含む地域の7 shelter projectsを承認した。
- Zaporizhzhiaはanti-drone routes、modular shelters、critical-infrastructure protectionの導入を公表した。
- Civil Protection Research Instituteはbackup ventilation等のshelter standard研究を承認段階へ進めた。
- Local authoritiesはdrone attack・air alert時の具体的guidanceを公表した。

### Boundary

これらは単なる「改善する」発言より具体的だが、検証対象のSumy/Kyiv casualty incidentsに対するafter-action correctionとしては確認できない。どのdocumented breakpointに対応したか、implementation completion、coverage、利用、maintenance、before/after outcomeがない。

**Control Change verdict: PARTLY CONFIRMED AS SYSTEM ACTIVITY; NOT LINKED TO VERIFIED BREAKPOINT.**

## 5. Closure Evidence

### Required evidence searched for

- 同程度の後続attackで同じchainが再発しなかったというmatched comparison。
- detection-to-warning、warning-to-shelter、dispatch-to-arrival等のresponse-time改善。
- shelter到達率、open/usable rate、accessibility、occupancy、survival outcomeの改善。
- 同一weapon・地域・building typeでのcasualty pathway reduction。
- official after-action review、audit、exercise evaluationによるcorrective action closure。

### Finding

**NONE / NOT FOUND.** Project approval、law adoption、guidance publication、aggregate interception、個別successful rescueはclosureではない。後続被害が報じられていないことも、attack exposure、reporting、母集団が一致しないためclosure evidenceにしない。

## 6. Evidence Boundary

### Supported

- civilian casualty増加とlong-range weapon / droneの寄与。
- populated area・residential buildingへの反復impact。
- warning、shelter、interception、rescue controlの制度上・aggregate上の存在。
- 一部の具体的law、project、guidance、infrastructure deployment。

### Unsupported

- 複数casualty incidentsに共通するwarning/interception/shelter/rescue breakpoint。
- casualty発生から特定control failureを逆算すること。
- control changeが特定incident analysisに応答したという因果。
- change後に同じharm pathwayが閉じたという効果。
- 7月の437 / 2,610を2026年7月HRMMU原表で直接確認すること。

### Core causal boundary

記事の中心因果「反復するbreakpointを特定し、control変更がそれを閉じた」は**未確認**である。確認できるのはhazard/outcome patternとcontrol activityが並存することまでで、両者を因果chainとして接続できない。

## 7. Overlap Audit

### 2026-08-14 Scenario-callable performance

- Conceptual difference: 8月14日は装備性能をscenario、coverage、availability、critical taskへ展開。本候補はactual incidentsからbreakpoint、change、closureを追う。
- Evidence result: actual incident chainを再構成できず、比較可能なのはweapon scenario、shelter availability、interception aggregateへ偏る。
- **Re-evaluation: HIGH drift risk.** Evidence不足を埋めると8月14日のscenario / availability / failure mode評価へ戻る。

### Pilot #3 — residual risk and recovery

- interception、shelter、rescueのどこを優先するかを論じるとscarce protection resourceの配分になる。
- **Re-evaluation: MEDIUM〜HIGH drift risk.** Breakpointを立証できないため、A/B/Cが実質的に資源配分へ戻る。

### Pilot #5 — implementation modules

- detection、warning、shelter、rescueを主体・資源・確認者へ分けるとModule mappingになる。
- **Re-evaluation: MEDIUM drift risk.** closure loopを資料で作れず、system decompositionだけが残る。

### 2026-08-13 Policy-Tool Fit

- casualty原因へinterception、guidance、shelter、rescueを対応付ければ原因仮説と手段適合になる。
- **Re-evaluation: HIGH drift risk.** verified breakpointとclosureがないため、候補を維持するほどPolicy-Tool Fitへ戻る。

**Overall Overlap: HIGH in evidence-constrained execution.** 独自操作は概念上成立するが、今回のEvidenceでは実行できず、既存操作へのdriftを防げない。

## 8. Reader Transformation and Stop Condition

### Reader Transformation

- Proposed: casualty count → repeated pathway → breakpoint → change → closure evidence。
- Evidence-supported portion: casualty count → repeated weapon / residential-impact outcome pattern。
- Unsupported portion: common control breakpoint → linked change → closure。

**Reader Transformation verdict: C / NOT MAINTAINABLE.** 最も重要な後半三段階が空欄であり、記事の独自性をEvidenceで支えられない。

### Stop Condition application

1. 共通control failure pattern: **NOT CONFIRMED**。
2. control breakpoint: **NOT IDENTIFIABLE**。
3. concrete system activity: **PARTLY CONFIRMED**だがbreakpointとのlinkなし。
4. closure evidence: **NONE / NOT FOUND**。
5. overlap boundary: **NOT MAINTAINABLE under available evidence**。

## 9. Final Decision

**Article Decision: HOLD_C**

- Article may be drafted next: **NO**。
- Initial Topic HOLD_C retained: **YES**。
- Fallback Attempts: **1 / limit reached**。
- Third candidate allowed: **NO**。
- Daily Result: **NO_PUBLISH candidate / human confirmation pending**。

### Workflow consequence

- Article Draft、Editorial Review、Human Read、Build、HTML、Publish記録を作成しない。
- `Daily Result: NO_PUBLISH`として記録し、`NO_PUBLISH Confirmation: PENDING`を保持する。
- 人間がNO_PUBLISHを確認するまで公開作業へ進まない。
