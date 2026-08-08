# World Insight Project Specification

## 文書の位置づけ

本書は、現時点における World Insight の正式なプロジェクト仕様である。理念や編集判断の詳細は各 Foundation 文書を正とし、本書はそれらを運用と開発へ接続する。

## 目的

ニュースを材料に、読者の判断力と思考力を鍛える。

World Insight は速報やニュースの網羅を目的としない。判断材料、異なる合理的立場、トレードオフ、前提、不確実性を整理し、最後の判断を読者に委ねる。

## World Brief との分離

- World Brief は「世界を知る」ためのものとする。
- World Insight は「世界を考える」ためのものとする。
- ブランド、サイト、公開物は分離する。
- World Brief 本体へ World Insight の機能や記事を混在させない。
- 将来、入力となるニュース候補のみ共有できる。ただし、選定、分析、編集、公開は World Insight 独自の基準で行う。

## 記事構成

記事は次の13セクションを基本形とする。テーマに応じて分量は調整できるが、読者の判断に必要な役割を無断で省略しない。詳細は [INSIGHT_EDITOR_GUIDE.md](INSIGHT_EDITOR_GUIDE.md) を正とする。

1. 今日のテーマ
2. 30秒要約
3. 判断資料
4. 知っておきたいこと
5. 利害関係者
6. 仮想閣議
7. What if?
8. 逆説探し
9. 共通前提
10. 本当の論点
11. 見落としやすい視点
12. Take One Thing
13. 今日の問い／今日の宿題

## Insight Pyramid

記事の分析には、次の七層を用いる。

1. Layer 1：事実
2. Layer 2：判断材料
3. Layer 3：利害関係者
4. Layer 4：トレードオフ
5. Layer 5：逆説
6. Layer 6：構造
7. Layer 7：問い

Layer 3 を中心的な層として扱い、主体の利益を金銭や単純な自己利益だけで説明しない。定義、分析方法、人間観の詳細は [THINKING_FRAMEWORK.md](THINKING_FRAMEWORK.md) を正とする。

## 編集原則

記事は、判断を押し付けず、対立を煽らず、事実と解釈を区別する。複数の合理的立場を公平に扱い、トレードオフ、不確実性、声が反映されにくい主体を明示する。二項対立や情報量で終わらず、読者自身の判断と、長く価値を持つ問いにつなげる。

編集原則、公平性、非誘導、品質基準の詳細は [EDITORIAL_CHARTER.md](EDITORIAL_CHARTER.md) を正とする。

## 情報源と制作運用

- 情報源、事実確認、引用、訂正は [SOURCE_POLICY.md](SOURCE_POLICY.md) に従う。
- 日々の記事制作は [EDITORIAL_WORKFLOW.md](EDITORIAL_WORKFLOW.md) に従う。
- 記事の具体的な書き方と公開前確認は [INSIGHT_EDITOR_GUIDE.md](INSIGHT_EDITOR_GUIDE.md) に従う。

## v0.1 の目標

- Foundation 文書を完成させる。
- HTMLプロトタイプを作成する。
- JSON入力形式を定義する。
- 最新記事を表示するページを作成する。
- 日付別アーカイブを作成する。
- Safariで表示を確認する。

## v0.1 でやらないこと

- ニュースの自動収集
- 完全自動の記事生成
- launchd による実行
- GitHub Pages の自動更新
- World Brief 本体の変更

## 現時点の実装状態

Foundation 文書と運用仕様を整備している段階であり、HTML、CSS、Python、JSON入力、公開環境は未実装である。
