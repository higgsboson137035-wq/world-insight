# World Insight 2026-08-13 Fallback — Source Verification

- **Date:** 2026-08-13
- **Selected Topic:** 同じインフレ率でも、原因が違えば何を誰の政策で扱うのか——複合指標と政策手段の適合を考える
- **Daily Editorial:** `docs/DAILY_EDITORIAL_2026-08-13.md`
- **Initial Topic Verification:** `docs/SOURCE_VERIFICATION_2026-08-13.md`（HOLD_Cの履歴を維持。本書は置換しない）
- **Article:** `articles/2026-08-13-policy-tool-fit.md`
- **Evidence cutoff:** 2026-08-13（日本時間）
- **Scope:** Fallback TopicのSource Verificationのみ。記事、Editorial Review、Build、HTML、Pipelineコード、Git操作は未実施。

## Executive Conclusion

**Source Verification: PASS_B — Policy-Tool Fitは独立した判断フレームとして成立するが、原因寄与を確定せず、Pilot #2の金利判断・更新規則へ戻らない条件で記事化可能。**

BLSの2026年7月CPI原表は、World Briefの総合前年比3.4%、前月の3.5%、コア前年比2.5%を確認する。加えて、総合前月比は季節調整済みで+0.1%、コア前月比は+0.2%だった。7月単月ではshelterが+0.1%で月次総合上昇の約3分の2を占め、energyは−1.5%だった。一方、前年比ではenergyが+14.7%、gasolineが+24.6%、foodが+3.0%、shelterが+3.2%、services less energy servicesが+3.0%だった。したがって、同じ「3.4%」だけでは、月次方向、前年比水準、項目別の動き、ウェイトを区別できない。

しかしBLS CPIは消費者が支払う価格変化を測る指数であり、原油、戦争、関税、AI設備投資、半導体、賃金、為替、生産性等の因果寄与を自動的に識別する資料ではない。BLS表から確認できるのは各項目の価格変化とrelative importance等であり、World Briefが挙げた「原油高、関税、AIインフラ投資に伴う半導体価格上昇」の寄与率は確認できない。特に7月単月のenergyは低下しているため、「原油高が7月CPIを前月比で押し上げた」とは書けない。他方、前年比energy上昇が総合前年比をcoreより上にした一因だという算術的説明は可能である。

FRBの法定目的は最大雇用と物価安定で、FOMCの主手段はfederal funds rateの目標レンジである。政策金利は短期金利・金融環境を通じて家計・企業の支出、総需要、雇用、物価へ作用する。原油を生産し、関税率を変更し、港湾・半導体工場・住宅を直接増やす権限ではない。したがって、供給制約や相対価格変化そのものと、それが需要、期待、賃金・価格設定へ波及する部分を分けることには公式資料上の根拠がある。

関税は大統領・USTR・議会が法的根拠ごとに関与し、エネルギー緊急対応では大統領とEnergy Secretary、歳出・税では議会と行政府、競争法執行ではFTC・DOJ、供給能力政策では議会の予算と所管省庁が別々の手段を持つ。各手段は届く原因、時間差、副作用が異なる。このため、**「一つの集計指標に一つの強い手段」ではなく、原因仮説、担当権限、到達経路、時間差、副作用を対応付ける**Policy-Tool Fitは検証フレームとして成立する。

Pilot #2との重複は**MEDIUM-LOW**。同じ金融政策・物価領域を扱うテーマ重複は高いが、Pilot #2は不確実な未来について政策ミスの費用と判断更新条件を管理した。Fallbackは将来の金利方向を決めず、観測済みの集計指標を分解し、原因仮説ごとに異なる主体・手段の到達範囲と副作用を割り当てる。Source Verification後もこの差は成立する。ただし記事がFOMCのA/B/C、次の統計待ち、利上げ・利下げ、更新条件へ戻ればHOLD_Cとなる。

最終判定はPASS_Bとする。Insight Shiftは独立した判断操作としてA候補だが、個別原因の因果寄与と手段効果には未確認部分が多い。記事では因果を結論にせず、読者が検証する欄を増やす方法として提示する。

## Verification Labels

- **Confirmed Fact:** BLS、Federal Reserve、法令・所管機関等の一次資料で確認できる制度・数値。
- **Official Statement / Official Explanation:** 公的機関が説明する目的、制度、作用経路。個別の因果効果を自動的に証明しない。
- **Reliable Reporting:** AP等が取材により報じた解釈・背景。一次資料の代替にしない。
- **Inference:** 複数資料から導く編集上の仮説。寄与率・効果量を事実として扱わない。
- **Unconfirmed:** 公開資料で確認できない原因寄与、時間差、効果量、動機。

## 1. Sources Reviewed

### Primary / Official

| Source | Establishes | Limit |
|---|---|---|
| [BLS, Consumer Price Index Summary, July 2026](https://www.bls.gov/news.release/cpi.nr0.htm) | 総合・コアの月次／前年比、主要項目、季節調整、technical note、relative importance | 価格変化の経済的原因を特定しない |
| [BLS, Relative Importance and Weight Information](https://www.bls.gov/cpi/tables/relative-importance/) | 消費支出ウェイト、年次更新、relative importanceの意味 | 因果寄与ではない |
| [BLS, Seasonal Adjustment FAQ](https://www.bls.gov/cpi/seasonal-adjustment/questions-and-answers.htm) | 季節調整の目的、X-13ARIMA-SEATS、集計方法、用途 | 経済ショックの因果を除去する処理ではない |
| [BLS, Using Seasonally Adjusted and Unadjusted Data](https://www.bls.gov/cpi/seasonal-adjustment/using-seasonally-adjusted-data.htm) | 短期分析と契約用途の使い分け、改定、2026年の調整状況 | 将来値や構造原因を示さない |
| [Federal Reserve, Monetary Policy](https://www.federalreserve.gov/monetarypolicy.htm) | 法定目的、FOMC資料、政策手段一覧 | 個別物価項目への寄与を示さない |
| [Federal Reserve, The Fed Explained—Monetary Policy](https://www.federalreserve.gov/aboutthefed/fedexplained/monetary-policy.htm) | 金利→金融環境→家計・企業支出→活動・雇用・物価という作用経路 | 供給制約そのものを直接変更するとは説明していない |
| [FOMC, Statement on Longer-Run Goals, reaffirmed Jan. 27, 2026](https://www.federalreserve.gov/monetarypolicy/files/fomc_longerrungoals.pdf) | 最大雇用、物価安定、PCE 2%、政策の主手段、幅広い条件を考慮 | 次回政策方向を本検証の中心にしない |
| [Federal Reserve, Monetary and Fiscal Policy FAQ](https://www.federalreserve.gov/faqs/money_12855.htm) | 財政政策は議会と行政府、Fedは財政政策を決めない | 個別歳出・税政策の効果は別途検証が必要 |
| [USTR, Section 301 action, July 23, 2026](https://www.ustr.gov/about/policy-offices/press-office/press-releases/2026/july/ustr-takes-action-forced-labor-section-301-investigations) | 大統領の指示、USTR調査・決定、関税率・除外等の実例 | 7月CPIへの寄与率を示さない |
| [DOE, Strategic Petroleum Reserve](https://www.energy.gov/hgeo/opr/strategic-petroleum-reserve) | EPCA条件下の大統領による緊急放出、Energy Secretaryによる限定exchange | 小売価格への効果量を保証しない |
| [CRS, Congress’s Power Over Appropriations](https://www.congress.gov/crs-product/R46417) | 議会の歳出権、行政府の執行制約 | 個別財政策がインフレへ与える純効果を示さない |
| [FTC, Anticompetitive Practices](https://www.ftc.gov/enforcement/anticompetitive-practices) | FTC Act等に基づく反競争行為への法執行 | 一般的物価上昇を直接設定する機関ではない |

### Reliable Reporting

| Source | Reports | Limit |
|---|---|---|
| [AP, July 2026 CPI](https://apnews.com/article/150e179a6c6b3182ba05cedf0188394b) | CPI鈍化、戦争・原油、関税、AI関連投資、FRB判断に関する取材・解釈 | BLS原表では原因寄与を確認できない。見出し上の原因をConfirmed Factにしない |

## 2. BLS July 2026 CPI Verification

### 2.1 Headline and core

| Measure | July 2026 | Basis | Status |
|---|---:|---|---|
| CPI-U all items, month-over-month | **+0.1%** | Seasonally adjusted | Confirmed |
| CPI-U all items, June month-over-month | **−0.4%** | Seasonally adjusted | Confirmed |
| CPI-U all items, 12 months ending July | **+3.4%** | Not seasonally adjusted | Confirmed |
| CPI-U all items, 12 months ending June | **+3.5%** | Not seasonally adjusted | Confirmed |
| All items less food and energy, month-over-month | **+0.2%** | Seasonally adjusted | Confirmed |
| All items less food and energy, 12 months ending July | **+2.5%** | Not seasonally adjusted | Confirmed |
| Core, 12 months ending June | **+2.6%** | Not seasonally adjusted | Confirmed |

### 2.2 Major components

| Component | July m/m SA | July y/y NSA | Verification finding |
|---|---:|---:|---|
| Food | +0.1% | +3.0% | Monthly and yearly increase |
| Energy | −1.5% | +14.7% | Monthly decline and high yearly increase coexist |
| Gasoline | −2.9% | +24.6% | Period choice reverses the immediate narrative |
| Electricity | +0.1% | +4.2% | Energy aggregate components differ |
| Utility gas | +0.7% | +4.3% | Same aggregate contains different monthly directions |
| Core commodities | +0.2% | +0.8% | Modest yearly increase relative to services |
| Services less energy services | +0.2% | +3.0% | Broad services remain above core commodities |
| Shelter | +0.1% | +3.2% | BLS says roughly two-thirds of monthly all-items increase |
| Medical care services | +0.6% | +2.7% | One of July’s rising service components |
| Transportation services | +0.3% | +2.9% | Monthly increase despite gasoline decline |

### 2.3 World Brief cross-check

| World Brief statement | Result |
|---|---|
| July all-items CPI +3.4% y/y | **MATCHES BLS** |
| June all-items CPI +3.5% y/y | **MATCHES BLS** |
| Core +2.5% y/y | **MATCHES BLS** |
| Inflation slowed slightly | **Supported only for the y/y rates:** headline 3.5→3.4, core 2.6→2.5 |
| Oil, tariffs, AI infrastructure / semiconductor prices are mixed causes | **Not established by BLS CPI release; Reliable Reporting / hypothesis only** |
| Reduced need for additional rate hikes | **Policy interpretation, not a BLS fact** |

### 2.4 Seasonal adjustment

1. BLS reports monthly changes primarily on a seasonally adjusted basis and 12-month changes before seasonal adjustment.
2. Seasonal adjustment removes recurring seasonal patterns such as weather, production cycles, model changeovers, holidays, and sales; it does not identify whether war, tariffs, wages, or productivity caused the remaining change.
3. BLS uses X-13ARIMA-SEATS. For 2026, selected series are directly adjusted and aggregates may be built from adjusted components.
4. Seasonally adjusted data can be revised annually for five years. CPI-U and CPI-W unadjusted indexes are final on release; the seasonal series have the stated revision treatment.
5. Month-over-month SA and year-over-year NSA answer different questions and must not be placed in one causal sentence without labeling the bases.

### 2.5 Weights and method

1. CPI-U measures price changes for goods and services purchased by urban consumers, covering over 90% of the U.S. population as defined by BLS; it does not include every population group.
2. Component changes are aggregated using expenditure weights representing their importance in the relevant population’s spending.
3. Beginning with January 2023 indexes, BLS updates spending weights annually using expenditure data from two years earlier. The 2026 basket therefore reflects the applicable annual update, not a real-time July expenditure share.
4. Relative importance changes as component prices move and is not identical to a structural causal contribution.
5. BLS samples prices; CPI is a statistical estimate with sampling and non-sampling considerations.

## 3. Cause Attribution

### 3.1 What the CPI release can establish

- Which published components rose or fell over the specified period.
- Their monthly and 12-month percentage changes.
- Their relative importance and, for selected aggregates, BLS’s arithmetic description such as shelter accounting for roughly two-thirds of the July monthly all-items increase.
- That July energy prices fell from June but remained substantially above July 2025.
- That core services and core goods had materially different year-over-year rates.

### 3.2 What it cannot establish by itself

- Why each seller changed a price.
- The share of CPI inflation caused by war, crude oil, tariffs, AI investment, semiconductor scarcity, wages, exchange rates, productivity, market power, or expectations.
- Whether a price change is temporary, persistent, a relative-price adjustment, or a generalized inflation process.
- Whether removing one policy would reverse the observed index by a specified amount.

### 3.3 Cause-by-cause classification

| Candidate cause | Confirmed observation | Inference that may be tested | Unconfirmed / cannot claim |
|---|---|---|---|
| Crude oil / war | Consumer energy −1.5% m/m, +14.7% y/y; gasoline −2.9% m/m, +24.6% y/y | Earlier oil shock can be consistent with high y/y energy and falling July m/m | Exact war/oil contribution to headline CPI; that oil raised July m/m CPI |
| Tariffs | USTR confirms 2026 tariff actions and exemptions under Section 301 | Tariffs can alter landed input/consumer prices, with pass-through depending on margins, exchange rates, sourcing, demand | Contribution to July CPI, incidence between importers/sellers/consumers, timing by CPI item |
| AI infrastructure / semiconductor demand | BLS reports relevant consumer categories but CPI is not a direct index of data-center investment | Investment demand or equipment scarcity could affect selected prices and electricity demand over time | AP/Brief’s causal contribution to July CPI; CPI does not directly measure most capital equipment purchases |
| Supply constraints | Item dispersion and sharp energy moves are consistent with sector-specific shocks | Capacity, logistics, inventories, regulation may constrain supply | Which constraint caused which CPI movement without production/import/inventory evidence |
| Shelter / rent | Shelter +0.1% m/m, +3.2% y/y and about two-thirds of monthly increase | Housing supply, leases, financing, measurement lags may matter | Exact division among supply, demand, mortgage rates, zoning, measurement lag from CPI alone |
| Services | Services less energy +0.2% m/m, +3.0% y/y | Labor costs, demand, rents, productivity and margins may contribute | Wage-driven share or demand-driven share from CPI alone |
| Wages | Not measured as a causal variable in CPI | Wage growth can affect costs and demand; prices can also affect wage demands | Direction and magnitude of wage-price causality without ECI/AHE/productivity and identification |
| Exchange rates | Not identified in CPI release | Exchange rates may alter import costs with incomplete and delayed pass-through | July contribution and incidence without trade-price and firm data |
| Productivity | Not identified in CPI release | Productivity can change unit costs and capacity | Short-run CPI contribution without productivity/unit labor cost evidence |
| Base effects | 12-month rate mechanically depends on July 2025 comparison; monthly and yearly energy directions differ | Base comparison helps explain why y/y stays high while m/m falls | Calling base effects an economic cause of current prices; it is a comparison effect |
| Expectations / second-round effects | CPI alone does not measure expectations | Persistent broad price and wage setting may transmit an initial shock | Existence and size without surveys, market measures, wages and broader price distributions |

### Attribution verdict

**PASS_B:** 原因候補を分類し、必要な追加資料を示すことはできる。しかし2026年7月CPIの原因寄与を一次資料だけで確定することはできない。記事は「原因を分解する」ではなく、より正確には**「原因仮説を分け、各仮説に必要な証拠と適合手段を照合する」**と書く。

## 4. Federal Reserve

### Confirmed mandate and authority

1. CongressはFedへ最大雇用と物価安定を追求する金融政策上の目的を与えている。moderate long-term interest ratesも法文上の目標に含まれる。
2. FOMCが金融政策スタンスを決め、主手段はfederal funds rateのtarget rangeである。
3. 実施手段にはinterest on reserve balances、overnight reverse repurchase operations等があり、状況に応じlarge-scale asset purchasesやforward guidanceも用い得る。
4. FOMCは長期的にPCE price indexで2%を物価安定と最も整合的と判断する。記事が扱うCPI 3.4%とFedの正式な長期目標指標を混同しない。

### Direct reach and indirect reach

| Reach | Finding |
|---|---|
| Direct institutional control | Policy rate target, reserve-related administered rates, balance-sheet operations and communication within legal authority |
| Primary transmission | Short-term interest rates and broader financial conditions |
| Indirect economic effects | Household and business spending, investment, hiring, aggregate demand, expectations, employment and inflation |
| Not direct production authority | Crude-oil production, tariff schedules, ports, housing construction, semiconductor fabrication, firm-specific prices |
| Supply/relative-price limit | Monetary policy can influence aggregate demand and propagation, but cannot directly create the scarce input or reverse the physical disruption |
| Secondary effects | By affecting demand and expectations, policy can influence whether an initial relative-price shock spreads or persists; exact effect and lag are uncertain |

### Editorial limit

「Fedには供給ショックへ何もできない」も強すぎる。供給そのものへ直接届かなくても、需要、期待、金融条件、二次波及に作用し得る。逆に「Fedが物価を安定させる責任を持つ」ことから、全項目の原因を直接除去できるとはいえない。

## 5. Other Policy Actors and Tools

| Policy area | Formal decision makers | What can change | Potential target | Timing | Main side effects / limits |
|---|---|---|---|---|---|
| Tariffs / trade remedies | Congress sets trade law; President and USTR exercise delegated authorities such as Section 301 under statutory procedures | Duty rate, product/country coverage, exclusions, timing, negotiations | Import prices, sourcing incentives, foreign practices | Border collection may change quickly; contracts, inventories, sourcing adjust with lags | Consumer/input costs, retaliation, domestic producer protection, sourcing shifts; CPI pass-through unconfirmed |
| Energy emergency tools | President under EPCA conditions; Energy Secretary for limited exchanges; Congress sets law/funding | SPR emergency sales/exchanges, reserve policy | Physical crude availability and disruption buffers | Release can be operationally faster than new production; delivery/logistics still matter | Reserve depletion, fiscal gains/losses, weak targeting, limited effect on global price |
| Fiscal policy | Congress taxes and appropriates; Administration implements enacted law within authority | Taxes, transfers, subsidies, procurement, public investment | Disposable income, aggregate demand, vulnerable households, selected supply capacity | Transfers may be faster; infrastructure/capacity takes years | Deficits, demand stimulus, targeting errors, administrative burden, distributional effects |
| Competition enforcement | FTC and DOJ under competition statutes; courts adjudicate | Investigations, enforcement, remedies against unlawful conduct | Anticompetitive restraints, exclusion, mergers, price fixing | Investigations/litigation often slow | Does not lower competitive-market prices by command; remedies case-specific; false positives/uncertainty |
| Housing / supply policy | Federal, state and local actors have different land-use, finance, tax, infrastructure authorities | Permits/zoning at local/state level; federal finance, grants, tax incentives | Housing capacity, financing and shelter costs | Construction and rule changes have long lags | Fiscal cost, local externalities, interest-rate sensitivity, geographic mismatch |
| Industrial / semiconductor capacity | Congress funds/authorizes; Commerce and other agencies administer programs; firms make investment/production decisions | Grants, tax incentives, permitting, procurement, research support | Capacity, resilience, technology investment | Multi-year | Fiscal cost, allocation risk, capacity cycles; most capital equipment is not directly CPI consumption |
| Labor / workforce | Congress, Labor Department, states, education institutions, employers | Training, immigration law/policy within authority, labor standards, participation supports | Labor supply, matching, skills, unit costs over time | Medium/long | Budget cost, distribution, implementation capacity; wage-price causality not one-way |
| Monetary policy | FOMC | Financial conditions and aggregate demand stance | Broad demand, expectations and propagation | Long and variable lags | Employment, investment, housing, exchange rate and financial stability effects; weak item targeting |

### Authority finding

「政府」が一つの政策束を持つわけではない。Congress、President/USTR、FOMC、DOE、FTC/DOJ、州・自治体、企業は異なる法的権限を持つ。Policy-Tool Fitには原因だけでなく、**誰が合法的・実務的に動かせるか**を含める必要がある。

## 6. Policy-Tool Fit Evaluation

### Hypothesis

> 一つの集計指標に異なる原因が混在するとき、一つの強い政策手段だけで対応すると、原因と手段のミスマッチが生じ得る。

### What supports it as a verification frame

1. CPIは多数項目を支出ウェイトで集計し、7月にはenergy、shelter、core goods、servicesが異なる方向・速度で動いた。
2. Fed、USTR、DOE、Congress、FTC等は異なる正式権限と作用経路を持つ。
3. 金融政策は広い金融環境・需要へ作用する一方、関税率や物理供給を直接変更しない。
4. SPRは物理的な石油供給途絶へ近いが、家賃・医療サービス・広範な需要には直接届かない。
5. 競争法は違法な反競争行為へ届くが、競争的市場の一般的インフレを価格統制する制度ではない。

### Counterevidence and limits

1. 原因別手段は常に優れるわけではない。原因の特定が遅い、不正確、行政的に複雑、政治的に配分される可能性がある。
2. 個別ショックでも期待や賃金・価格設定へ広がれば、集計的な金融政策が必要になり得る。
3. 複数主体へ責任を分けると、調整失敗、時間遅れ、相互に相殺する政策を生み得る。
4. 観測された項目と経済的原因は一対一ではない。一つの原因が複数項目へ、一つの項目が複数原因へ結びつく。
5. 「強い一手」を否定する結論にしてはならない。広い需要・期待の問題には広い手段が適合し得る。

### Verdict

**PASS as a decision frame, not as a causal fact.** 次の6欄を埋める方法として成立する。

1. 観測された項目・期間
2. 原因仮説
3. 仮説を識別する証拠
4. 正式な政策主体と手段
5. 到達経路・時間差
6. 他項目・主体への副作用

原因仮説と手段を一対一で固定せず、空欄と競合仮説を残す。

## 7. Thinking Trap Evaluation

### Candidate

**相関と因果の混同**

### Concrete connection

- 戦争、関税、AI投資とCPIが同時期に動いても、CPI原表は因果寄与を識別しない。
- 7月energyのm/m低下とy/y上昇は、期間を省くと反対の物語を作れる具体例になる。
- 「原因」と判断する前に、項目、期間、比較対象、ウェイト、政策導入時期、pass-through、代替説明を確認する。
- 原因仮説を誤れば、届かない手段を選ぶため、TrapがPolicy-Tool Fitへ直接つながる。

### Verdict

**PASS_B.** 一般的な注意書きではなく、原因仮説→識別証拠→適合手段という記事の中心操作へ接続できる。ただし「相関は因果でない」で終わればFAIL。具体例として原油、関税、AI/半導体、shelterの証拠境界を示す必要がある。

## 8. Pilot #2 Overlap Gate

### Strict comparison

| Dimension | Pilot #2 | Fallback after verification |
|---|---|---|
| Initial object | 雇用・物価・不確実性の下のFOMC判断 | CPIという複合指標と複数政策主体 |
| Core uncertainty | 将来の雇用・物価、統計改定、政策ミス | 現在の項目変化の原因識別、手段の到達範囲 |
| Core operation | 誤りの費用を比較し、判断更新条件を事前に決める | 原因仮説、識別証拠、正式主体、手段、時間差、副作用を対応付ける |
| Central choice | 雇用対応／待つ／物価安定 | 集計手段／原因別手段／相対価格を許容し波及を抑える |
| Transfer | 不確実な判断で更新規則を先に置く | 集計指標に対する介入の手段適合を点検する |
| Failure mode | 次のデータでどう判断を変えるかへ戻る | 原因を断定する、または各機関の手段を列挙するだけになる |

### Overlap test results

- 「次の利上げ／利下げ」は中心に置かない: **PASS**
- 「次の統計を待つ」をB案にしない: **PASS**
- 「何が変われば判断更新」をInsightの中心にしない: **PASS**
- 「政策ミスの費用比較」をStructural Questionにしない: **PASS**
- CPIと金融政策というテーマ重複: **HIGH**
- Reader operationの重複: **LOW〜MEDIUM**

### Verdict

**MEDIUM-LOW — 独立したReader Transformationを構築可能。**

差は資料追加前の言葉だけでなく、一次資料の構造にも表れた。BLSは項目・期間・ウェイトを分け、Federal Reserve、USTR、DOE、Congress、FTCは異なる正式手段を持つ。この証拠を使えば、更新規則でなくPolicy-Tool Fitを実行できる。

ただし記事の大半がFOMCの次の判断、追加利上げの可能性、次回統計に向けば、差は消える。その場合はEditorial Reviewを待たずHOLD_Cへ戻す。

## 9. Reader Transformation and Insight Shift

### Reader Transformation

- **Before:** CPIを一つの政策信号として読み、上昇なら金融引締め、鈍化なら待機・緩和と直結させる。
- **After:** 集計値を観測項目と期間へ分け、原因仮説ごとに識別証拠、正式な担当主体、届く政策手段、時間差、副作用を確認する。
- **Independence:** **PASS_A候補。** Pilot #2の更新規則とは異なる操作として成立する。

### Insight Shift

**評価: A（記事化全体は証拠制約によりPASS_B）**

推奨方向:

> 物価指標を政策への一つの信号として読むのではなく、まず項目・期間・ウェイトを分け、原因仮説ごとに必要な証拠と、その原因へ届く正式な主体・手段・時間差・副作用を対応付ける。良い物価判断は「最も強い手段」より、原因と手段の適合を検証する。

限定:

- 原因と手段が一対一に対応すると断定しない。
- 個別政策の組合せが常に金融政策より良いとしない。
- CPIはFedの正式な2%長期目標指標であるPCEと同一ではない。
- 「複数原因」は確認できる項目分散と候補仮説を意味し、寄与率確定を意味しない。

## 10. Impact on Today's Question and Quick Choices

### Today's Question

**修正要否: MINOR REVISION REQUIRED**

Morning案は「需要、エネルギー、関税、設備・供給制約が混ざる」と原因を既知のように置く。Source Verificationでは一部の原因寄与が未確認なので、「原因仮説」に変更する。

推奨修正版:

> **あなたが物価対策を束ねる責任者なら、同じCPIに異なる項目と原因仮説が混在するとき、何を確認して担当主体と手段を割り当て、何を金融政策だけには任せませんか。**

### Quick Choices

**修正要否: MINOR REVISION REQUIRED**

- **A 集計的な波及抑制を優先:** 広い金融条件で需要・期待・二次波及へ対応する。供給原因へ直接届くとは書かない。
- **B 原因仮説ごとの手段適合を優先:** 識別証拠が揃う範囲で、関税、エネルギー、供給、競争、財政等を担当主体へ割り当てる。常に精密・迅速とはしない。
- **C 相対価格の調整を許容し、脆弱性保護を優先:** 一時的変化を全面相殺せず、対象支援と波及監視へ絞る。「何もしない」と表現しない。

公平性条件:

- Aを粗い誤策、Bを賢い正解、Cを放置として描かない。
- Aには原因を外す費用、Bには誤診・調整遅延・財政配分の費用、Cには持続化・期待波及を見逃す費用を置く。

## 11. Confirmed / Reporting / Inference / Unconfirmed Summary

### Confirmed Facts

- July all-items CPI: +0.1% m/m SA, +3.4% y/y NSA.
- Core CPI: +0.2% m/m SA, +2.5% y/y NSA.
- Shelter +0.1% m/m and about two-thirds of monthly headline increase.
- Energy −1.5% m/m and +14.7% y/y; gasoline −2.9% m/m and +24.6% y/y.
- BLS uses expenditure weights and distinguishes SA monthly from NSA yearly data.
- Fed acts mainly through financial conditions and aggregate demand, not direct physical supply or tariff authority.
- Other policy areas have different formal decision makers and time horizons.

### Reliable Reporting

- AP attributes the broader inflation environment to war/oil, tariffs and AI-related investment pressures and discusses implications for Fed decisions.
- Those causal attributions remain reporting/analysis unless separately established.

### Inference

- High y/y energy with falling m/m energy is consistent with a past shock fading at the margin while remaining in the annual comparison.
- A single broad instrument may be poorly targeted to a sector-specific physical or legal cause, while still affecting propagation.
- Matching a hypothesized cause to a tool can reduce one mismatch but create coordination, timing and distribution problems.

### Unconfirmed

- Exact causal contributions of oil, tariffs, AI investment, semiconductors, wages, exchange rates, productivity, margins and market power to July CPI.
- Pass-through magnitudes and lags for 2026 tariffs.
- Effect size of SPR, fiscal, antitrust, housing or industrial measures on the July inflation path.
- Whether July’s moderation is temporary or persistent.
- The policy mix that would minimize inflation and employment costs.

## 12. Final Verdict and Article Conditions

### Final verdict

**PASS_B**

### Conditions for article drafting

1. BLS values must distinguish m/m SA from y/y NSA and state the period every time direction could be ambiguous.
2. World Brief’s 3.4%, 3.5%, 2.5% may be used as confirmed; oil/tariff/AI causal attribution may not be upgraded beyond Reliable Reporting / hypothesis without additional evidence.
3. Write “原因仮説を分ける,” not “原因を特定した.”
4. Center the six-part Policy-Tool Fit operation: observation, hypothesis, identifying evidence, authority/tool, lag, side effects.
5. Keep FOMC rate direction, waiting for the next data, update conditions and policy-error costs outside the center; otherwise HOLD_C.
6. Distinguish CPI from the PCE index used for the FOMC’s longer-run 2% objective.
7. Do not imply the Fed can directly fix supply, or that it is powerless against propagation and expectations.
8. Do not present targeted policy as automatically superior; include diagnosis, coordination, fiscal and timing costs.
9. Thinking Trap must use concrete period/component examples and connect misattribution to tool mismatch.
10. Use the revised Today's Question and neutralized A/B/C wording above.

### Stop / no-publish threshold

- 原因寄与を推測で確定する必要が生じる。
- 記事の中心が追加利上げ・利下げ、次の統計、更新条件、政策ミスの費用へ戻る。
- Bを正解としてA/Cを藁人形化する。
- Policy-Tool Fitが機関・政策の列挙だけで、読者が実行できる判断手順にならない。

いずれかに該当する場合、FallbackもHOLD_Cとし、別候補へ自動切替せず2026-08-13はNO_PUBLISHを提案する。

## Verification Record

- Initial Topic HOLD_C preserved: **YES**
- BLS headline/core values verified: **YES**
- Monthly/yearly and SA/NSA separated: **YES**
- Weights/method reviewed: **YES**
- Cause attribution limited: **YES**
- Fed mandate/tools/transmission separated: **YES**
- Other policy authorities separated: **YES**
- Policy-Tool Fit: **PASS as verification frame**
- Pilot #2 overlap: **MEDIUM-LOW**
- Reader Transformation: **PASS_A candidate**
- Insight Shift: **A**
- Thinking Trap: **PASS_B**
- Source Verification: **PASS_B**
- Proceed to drafting: **COMPLETED — `articles/2026-08-13-policy-tool-fit.md`**
- Independent Editorial Review / Build / HTML / Pipeline code / Git operations: **NOT PERFORMED**
