# World Insight 2026-08-20 — Source Verification

- Date: 2026-08-20
- Selected Topic: **AI投資は、期待ではなく回収能力へ変換されているか——株価調整を企業開示の連鎖で読む**
- Daily Editorial: `docs/DAILY_EDITORIAL_2026-08-20.md`
- Article: `articles/2026-08-20-ai-investment-recovery-chain.md`
- Evidence cutoff: 2026-08-20（日本時間）
- Scope: 決定的確認事項から開始。主要3社の比較可能な一次資料を確認し、成立後に必要な範囲のSource Verificationを実施。記事Draft、Editorial Review、Build、HTML、Pipeline / Builder / template / CSS変更、Git操作は未実施。

## Executive Conclusion

**Source Verification: PASS_B（限定条件付き）。**

決定的確認事項は成立した。MicrosoftのFY26 Q3（2026年3月31日終了）で、同一四半期のcapex、AI関連の需要・売上／利用実績、営業CFを接続できる。AlphabetのQ1 2026でも同様の数値を並べられるが、capexはAI専用でなく、Google Cloud売上もAIとcore GCPを含む。MetaのQ1 2026はcapexと営業CFは確認できるが、AI固有売上を分離開示しておらず、AI投資→AI売上→営業CFの連鎖は成立しない。

このため、**投資→稼働・需要→収益→営業CF**の各段階を確認済み事実として並べることはできるが、AI投資が営業CF増加を直接引き起こしたとは言えない。企業自身の定義・主張、混合セグメント、期間差、減価償却、顧客集中、将来投資の回収期間を明示する必要がある。記事の中心は企業優劣、買い／売り、株価評価、金利予想ではなく、Evidenceと期待の境界を読む操作に限定する。

## Verification Labels

- **Official / Primary:** SEC提出書類、企業Investor Relationsの決算リリース・決算説明会 transcript。企業が何を開示・主張したかを示す。
- **Reliable Reporting:** 今回の決定的確認には使用しない。World BriefのAP記事は市場反応の背景入力に留め、回収Evidenceにはしない。
- **Inference:** 同一期間の数値を並べて得る編集上の比較。因果の確定ではない。
- **Unknown / Unconfirmed:** AI専用capex、AI売上の会計定義、AI部分の営業CF、設備稼働率、顧客別採算、回収期間など。

## 1. Determinative Check — Microsoft

**Primary sources:** [Microsoft FY26 Q3 earnings call transcript](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q3)、[FY26 Q3 performance](https://www.microsoft.com/en-us/Investor/earnings/FY-2026-Q3/performance)、[Intelligent Cloud performance](https://www.microsoft.com/en-us/Investor/earnings/FY-2026-Q3/intelligent-cloud-performance)、[SEC Form 10-Q（2026-03-31）](https://www.sec.gov/Archives/edgar/data/789019/000119312526191507/msft-20260331.htm)。

| 段階 | 同一期間に確認できたEvidence | 境界 |
|---|---|---|
| 投資（capex） | FY26 Q3 capex **$31.9B**。約3分の2が短寿命資産（主にGPU・CPU）、残りは15年以上の収益化を支える長寿命資産。cash paid for PP&Eは**$30.9B**。 | capex全額がAI専用ではない。データセンター、クラウド、更新投資を含む。 |
| 稼働・需要 | Microsoft Cloud revenue **$54.5B、前年比29%**。Azure and other cloud services **+40%**。AI・非AIの消費を含み、需要が供給能力を上回ると説明。M365 Copilot paid seats **20M超**、AI business annual revenue run rate **$37B超**。 | ARRは企業定義のrun-rateでGAAP revenueではない。Azure売上はAI専用でない。Copilot seatsは利用・売上の完全な代替ではない。 |
| 収益 | 全社Revenue **$82.9B**、Operating income **$38.4B**。Microsoft Cloud gross margin **66%**。 | Operating incomeは全社・複数事業の数値で、AI投資への帰属は開示されない。 |
| キャッシュ回収 | Cash flow from operations **$46.7B（前年比26%増）**。会社説明では主にcloud billings and collectionsが増加。Free cash flow **$15.8B**。 | OCF増加をAI投資の直接効果とは言わない。FCFはOCFからcapex等を差し引いた別指標。 |

**連鎖の判定:** `投資（capex） → 稼働・需要（Azure消費、Copilot有料席、AI ARR） → 収益（Cloud／全社） → OCF` を、同一四半期の開示で**部分的に再構成できる**。ただし、各段階の定義が完全に同一ではなく、因果は会社説明を超えて推論しない。決定的確認事項は成立。

## 2. Determinative Check — Alphabet

**Primary sources:** [Alphabet Q1 2026 results（SEC Exhibit 99.1）](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000043/googexhibit991q12026.htm)、[Q1 2026 earnings transcript](https://storage.googleapis.com/magi-store/earnings/GOOGL/2026-04-29_Q1_FY2026/03_outputs/transcript.html)。

| 段階 | 同一期間に確認できたEvidence | 境界 |
|---|---|---|
| 投資（capex） | Q1 2026 purchases of property and equipment **$35.674B**。会社の2026年capex見通しは$180〜190B。 | PP&EはAI computeだけでなく、全社technical infrastructureを含む。 |
| 稼働・需要 | Google Cloud revenue **$20.0B、前年比63%**。開示上、GCPのenterprise AI Solutions／enterprise AI Infrastructure／core GCPが寄与。Geminiモデルは顧客APIで**毎分16B超tokens**、Gemini Enterprise paid monthly active usersは前四半期比40%増。 | Cloud revenueとtokensはAI専用売上ではない。利用量から利益・回収を直接導けない。 |
| 収益 | 全社Revenue **$109.896B**、Operating income **$39.696B**。 | 全社数値であり、AI設備への帰属は不明。 |
| キャッシュ回収 | Net cash provided by operating activities **$45.790B**。Free cash flow **$10.116B**（OCF−PP&E）。 | OCFは全社の営業活動。AI投資がOCFを増やした直接証拠ではない。 |

**連鎖の判定:** Microsoftと同様に、需要・収益・OCFを並べられるが、AI専用capexとAI専用revenueは分離されないため、**PASS_Bの補強Evidence**に留める。

## 3. Determinative Check — Meta

**Primary source:** [Meta Q1 2026 results](https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/)。

| 項目 | 確認できたEvidence | 判定 |
|---|---|---|
| capex | Capital expenditures（finance lease元本を含む）**$19.84B**。2026年見通し$125〜145B。 | 確認可能。ただしAI専用ではない。 |
| AI需要／売上 | AIへの投資・モデル、AI glasses等の利用・開発説明はある。総Revenue **$56.311B**、広告Revenue **$55.024B**は確認できる。 | AI固有売上を分離できず、広告RevenueをAI売上と扱えない。 |
| OCF | Cash flow from operating activities **$32.226B**、FCF **$12.386B**。 | 確認可能。AI部分への帰属は不可。 |

**連鎖の判定:** capexとOCFはあるが、AI需要／AI売上と同一企業・同一期間で接続する会計的な実績がない。決定的確認事項をMeta単独では満たさない。これは全体のHOLD_C条件ではなく、企業別のEvidence Boundaryである。Microsoftで少なくとも一社の連鎖が成立しているため、全体判定はPASS_B。

## 4. Accounting and Definition Boundaries

- **Revenue:** GAAP売上。Microsoft Cloud、Azure、Google Cloud、Meta広告など範囲が異なる。
- **Operating income:** 収益性の会計指標。Microsoft／Alphabet／Metaの全社またはセグメント数値で、AI投資への直接帰属ではない。
- **Operating Cash Flow (OCF):** 営業活動からの現金。Microsoftはcloud billings and collections、Alphabet・Metaは全社営業活動。AI投資の回収額ではない。
- **Free Cash Flow (FCF):** 企業定義を確認し、原則OCF−capexとして扱う。Microsoft $15.8B、Alphabet $10.116B、Meta $12.386BはOCFと混同しない。
- **AI business ARR:** Microsoftの**$37B超**はannual revenue run rateという会社開示で、期間確定GAAP revenueではない。
- **AI revenue / demand:** MicrosoftはAI ARR、Azure／Copilotの利用・有料席を開示。AlphabetはCloudのAI Solutions／Infrastructure寄与、tokens、Gemini Enterprise利用を開示。MetaはAI固有売上を分離していない。
- **Capex:** Microsoftはfinance leasesを含むcapexとcash PP&Eを併記。Metaもfinance lease元本を含む。AlphabetのQ1表はPP&E購入。横並びの単純比較をしない。

## 5. Depreciation, Capacity, and Time Horizon

- Microsoftは短寿命GPU／CPUと15年以上の長寿命資産を区別し、投資期間と回収期間が一致しないことを示す。AI設備の個別稼働率・減価償却額はこの限定確認では未分離。
- Alphabetは2025年の減価償却が$21.1Bへ増え、2026年は増加率が加速すると説明している。これは投資の費用化時間差を示すが、AI専用回収を意味しない。
- Metaはインフラ費用増の背景に減価償却・データセンター運営費・外部cloud費用を挙げるが、AI部分の減価償却は未分離。
- 3社とも、AI設備の稼働率、顧客別粗利、契約単位のAI採算、投資回収期間を完全には開示していない。MicrosoftはRPO $627B（OpenAIを含む場合の影響あり）を示すが、AI capexの回収証明ではない。

## 6. Evidence Boundary / Unknown / Unconfirmed

### Evidenceで言えること

1. 3社とも大規模なAI関連またはAIを含むインフラ投資を行っている。
2. Microsoftでは、同一四半期に投資、AI需要・利用、Cloud／AI関連の会社指標、全社OCFを並べられる。
3. Alphabetでは、AIを含むCloud成長、利用指標、PP&E、OCFを同一四半期で並べられる。
4. Metaでは、AIを含むインフラ投資と全社OCFは確認できるが、AI固有売上は分離できない。

### 言えないこと

- AI capexの何ドルがAI売上・AI利益・OCFを生んだか。
- OCF増加がAI投資によって直接生じたこと。
- 企業間のAI売上や回収速度の優劣。
- 株価調整が投資回収の失敗を意味すること。
- 経営者の「需要が強い」「投資は回収できる」という主張が独立に証明されたこと。

## 7. Overlap Re-evaluation

**Overlap: LOW〜MEDIUMを維持。**

- Pilot #2型の金利方向、政策ミスの費用、次に何が出れば更新するかは扱わない。
- 8/13型の原因仮説→Policy-Tool Fitは扱わない。
- 単純な企業業績ランキング、AI株の買い／売り、割高／割安判定は扱わない。
- 中心操作は、企業開示の異なる定義を明示し、**期待→投資→稼働・需要→収益→キャッシュ回収のどこまでが実演済みか**を区別すること。これは過去Insightの判断操作と重複しない。

## 8. Reader Transformation and Article Boundary

- Before: 株価変動、capex増加、AI需要の強い発言を一つの「AI成功」または「AIバブル」物語へまとめる。
- After: Revenue、Operating income、OCF、FCF、AI ARR／利用、capexを定義・期間ごとに分け、回収連鎖の確認済み部分と期待部分を分離する。
- **Reader Transformation verdict: PASS_B。** Microsoftで連鎖を実演でき、Alphabetで比較境界を示せる。ただしAI専用会計の空欄が大きいため、完全な因果実証（PASS_A）ではない。
- 記事化条件: 企業の主張とGAAP数値を分離し、同一期間の比較表を中心に置く。因果は「会社はこう説明する」「数値はここまで示す」に限定する。

## 9. Stop Condition / Article Decision

- 決定的確認事項は成立したため、HOLD_Cの早期停止は適用しない。
- ただし記事Draftで、AI専用capex・AI専用OCF・企業間の回収速度を推定し始めた場合、または中心が投資推奨、株価評価、金利予想、Policy-Tool Fit、単純業績比較、AIバブル論へ変質した場合は**PASS_Bを撤回しHOLD_C**とする。
- **Article Decision: PASS_B。** 記事Draftへ進める状態。ただし記事Draft自体は本工程では作成しない。
