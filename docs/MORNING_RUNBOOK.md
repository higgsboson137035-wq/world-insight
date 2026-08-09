# World Insight Morning Runbook

毎朝の作業入口は次のコマンドです。

```bash
cd ~/Workspace/world-insight
python3 scripts/morning.py
```

日付を指定する場合:

```bash
python3 scripts/morning.py --date 2026-08-10
```

Daily Editorialがない日に作業テンプレートを準備する場合だけ、`--prepare`を付けます。

```bash
python3 scripts/morning.py --date 2026-08-10 --prepare
```

## 標準手順

1. `morning.py`のWorld Brief、Daily Editorial、Gate状態を確認する。
2. 表示された`Next Action`を1つ実行する。
3. Candidate Topics、Scorecard、Source Verificationを人間が確認する。
4. Article DraftとEditorial Reviewを進める。
5. 必要な場合に`source .venv/bin/activate && python3 scripts/build.py`を実行する。
6. `python3 -m http.server 8000`でSafari / ChromeのLocal Previewを確認する。
7. Git Diff ReviewとFinal Approvalを記録する。
8. 最終承認後にのみ、Git操作と手動公開を行う。

`morning.py`は記事生成、Build、ブラウザ起動、commit、pushを行わない。品質Gateを通らない日は公開を保留することが正しい運用である。
