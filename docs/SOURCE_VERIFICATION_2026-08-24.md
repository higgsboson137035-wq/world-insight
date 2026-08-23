# Source Verification — 2026-08-24

- Date: 2026-08-24
- Selected Topic: 責任者を替えれば組織は立て直るのか——戦時統治の機能継続をどう確かめるか

## Scope and Measurement

- Article / Initial Topic: `責任者を替えれば組織は立て直るのか——戦時統治の機能継続をどう確かめるか`
- Verification scope: Morning Editorial Meetingの決定的確認事項を、**一つの統治機能**について限定確認。別機能、別人物、戦況一般、人物評価、一般論へ拡張していない。
- Fixed function: **国際防衛パートナーとの合意・支援の実施調整（partner-agreement implementation）**。防空資源の配分や軍事能力の数量ではなく、交代前後で対外合意・支援実施を担当し、継続できるかだけを確認する。
- Measurement: 開始 2026-08-24 07:07:10 JST / 終了 2026-08-24 07:09:07 JST / 実所要時間 **1分57秒（117秒）**。
- Method: 一次資料を優先。Webページの確認は行ったが、記事Draft、Build、HTML生成、tests、Pipeline、morning.py変更、Git操作は行っていない。

## Decisive Check

判定対象は、次の一鎖である。

`交代前の担当主体 → 交代時点の未完了案件・期限・継続義務 → 交代後の責任主体 → 交代後の確認可能な継続行為`

### 1. 交代前の担当主体

- **Official / Primary:** ウクライナ国防省は、2026年7月16日付の公式発表で、ミハイロ・フェドロフが国防相在任中の実績として、複数回のRamstein会合、2026年の支援発表、欧州融資を軍事優先事項へ使う仕組みを挙げている。これは、国際防衛パートナーとの支援・合意実施調整がフェドロフ在任中の国防省の担当領域だったことを示す。
  Source: https://mod.gov.ua/news/mykhailo-fedorov-nazvav-22-kliuchovi-dosiahnennia-minoborony （16 Jul 2026, items 14–15）
- **Evidence Boundary:** これは「担当領域・在任中の実績」の証拠であり、個別の案件が交代時点で未完了だったことまでは示さない。

### 2. 交代時点の未完了案件・期限・継続義務

- **Official / Primary:** 国防省公式発表は、2026年7月17日にエフゲニー・フマラを国防相代行に任命し、大統領が「すべての進行中プログラム」の実施、なかでも「パートナーとの合意の迅速な実施」を継続するよう指示したと記録している。これは、交代時点に継続義務が存在したことの直接的な証拠である。
  Source: https://mod.gov.ua/en/news/evgeniy-khmara-appointed-acting-minister-of-defence-of-ukraine （17 Jul 2026）
- **Evidence Boundary:** 「進行中プログラム」「合意の迅速な実施」という義務は確認できるが、どの合意、期限、未完了項目が対象だったかはこの資料だけでは特定できない。

### 3. 交代後の責任主体

- **Official / Primary:** 同じ国防省公式発表は、フマラを国防相代行と記録する。さらに、最高議会の公式投票記録は、2026年8月19日にフマラの国防相任命案が可決されたことを記録し、議事録本文は7月20日から副大臣・代行を務めていたことを記録している。
  Sources: https://mod.gov.ua/en/news/evgeniy-khmara-appointed-acting-minister-of-defence-of-ukraine ; https://meeting.rada.gov.ua/work/vote/pz-20260819/sps （19 Aug 2026）
- **Evidence Boundary:** 代行から正式任命への責任主体の移転は確認できる。ただし、合意実施という固定機能について、内部の引継ぎ文書や案件台帳が公開されたことは確認できない。

### 4. 交代後に実際に確認できる継続行為

- **Official / Primary:** 2026年8月23日付の国防省サイトの最新記事一覧には、フマラによる「ウクライナと米国は長期的で相互利益のある防衛パートナーシップを構築すべき」と題する記事が掲載されている。また、国防省の8月4日公式発表は、国防省・参謀本部・総司令官間の調整を強化するため副大臣を任命したと記録する。
  Sources: https://mod.gov.ua/en/news/evgeniy-khmara-ukraine-and-the-united-states-should-build-a-long-term-mutually-beneficial-defense-partnership ; https://mod.gov.ua/en/news/ministry-of-defence-strengthens-its-team-with-new-appointments-to-advance-procurement-reform-and-objective-assessment-of-the-situation-within-the-defence-forces （4 Aug 2026）
- **Evidence classification:** **Unknown / Unconfirmed for the decisive chain.** 前者は記事タイトルの掲載を確認できるが、公開本文から、7月17日に指示された「既存のパートナー合意」のどれを、どの期限・成果物について継続実施したのかを接続できない。後者は調整体制の変更であり、固定した「合意実施」案件の継続行為とは別の制度変更である。
- **Reliable Reporting:** World BriefのAP要約は政治・軍事状況を伝えるが、固定機能の案件引継ぎを検証する資料としては用いない。
- **Inference:** 「後任が外交・防衛パートナーに関する発言をした」ことから、交代前の合意実施が継続したと推論することはできない。

## Evidence Chain Verdict

| Chain element | Verdict | Reason |
|---|---|---|
| 交代前の担当主体 | **成立** | フェドロフ在任中の国防省による対外支援・合意関連実績を公式資料で確認。 |
| 未完了案件・期限・継続義務 | **部分成立** | 「進行中プログラム」「パートナーとの合意を迅速に実施」という継続義務は公式資料で確認。ただし個別案件・期限は不明。 |
| 交代後の責任主体 | **成立** | フマラの代行任命、のちの国防相任命を公式資料で確認。 |
| 交代後の継続行為 | **不成立** | 対米パートナーシップ記事の掲載は確認できるが、同じ既存合意・期限・継続義務への実行として接続できない。 |

**決定的確認事項: 不成立。** 4点を同じ機能について一鎖で確認できないため、Stop Conditionを適用する。

## Evidence Boundary / Unknown

- 確認できるのは、フェドロフ在任中の担当領域の公式記録、交代時の継続義務、フマラへの責任移転までである。
- 未確認なのは、具体的な合意名、実施期限、交代時点の未完了成果物、引継ぎ記録、後任が同じ案件を実行した証拠、実施結果である。
- 「国防省が存続した」「後任が任命された」「後任がパートナーシップに言及した」だけでは機能継続成立としない。
- 防空弾、戦場の成果、戦況、支持率、人物の更迭理由は今回のEvidenceに含めない。

## Reader Transformation / Quality Reassessment

- Reader Transformation: **維持不可（C）**。人物交代、継続義務、後任の任命までは確認できるが、交代前の案件が後任の継続行為へ接続されず、今回の中心操作を実例で示せない。概念説明だけで補えば、人物評価または静的な権限表へ縮退する。
- Insight Shift: **C / HOLD**。Morning EditorialでA候補だった「人物交代から機能継続の証拠へ」は、核心の継続行為が欠けるため成立しない。
- Take One Thing: **未成立（FAIL相当）**。一般には他組織の引継ぎへ持ち運べる形式だが、今回の事例で「案件・期限・責任主体・継続行為」の連鎖を実演できないため、記事のTake One Thingとして採用しない。
- Overlap: **HIGH risk / HOLD**。Evidence不足を補うために権限主体の対応表を詳述するとPilot #5の静的な権限・実行・確認分離の再演になる。防空や軍事資源の継続性を補助線にするとPilot #3へ移る。人物の交代理由や後任評価へ移れば、Reader Transformation自体が失われる。

## Final Decision

**Article Decision: HOLD_C**

- Stop Condition: Applied。
- Additional search: **NOT PERFORMED**。別機能・別人物・一般論へ拡張していない。
- Fallback: **NOT PERFORMED**。次工程で人間確認後にのみ既存Fallback候補を再評価する。
- Article Draft / Build / HTML / tests / Pipeline / morning.py / Git: **NOT PERFORMED**。
