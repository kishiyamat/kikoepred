---
title: "個人の異聴傾向を考慮した「聞き間違えやすい語」の予測—単語分散表現と確率、編集距離の応用—"
author: "著者名"
date: "2024年9月22日"
---

# 個人の異聴傾向を考慮した「聞き間違えやすい語」の予測--—単語分散表現と確率、編集距離の応用---

## 著者名
岸山 健(東京大学)
野口 大斗(東京医科歯科大学)
黄 竹佑(名古屋学院大学)

2024年9月28日

---

## Abstract

本研究では、「渋谷-日比谷」などに見られる聞き間違えやすい語のペアを抽出する報告
をもとに、個人差を反映した上で語レベルの異聴を予測するモデルを提案・検証する。すで
に辞書と音声の分析から聞き間違えやすい語を抽出する報告は存在するが、個人差を反映
できない点が課題であった。本研究では、入力の音素に対して知覚された音素を記述する
「異聴行列」として個人差を取り込んだ。この行列を本研究では「編集距離」の計算時に考
慮した。編集距離では、文字列の変換に必要な操作の回数がコストとして示される。例えば、
「sibuya→hibiya」の音素列のコストは 2 となる。ここで s を h と知覚する異聴行列を持
つ個人を反映するには、s→h のコストを 0 とする。その結果、コストは低くなり聞き間違
える度合いの個人差を反映できる。
実験では、要旨版 Wikipedia コーパスの 206,060 語の頻度を抽出し、「渋谷-日比谷」や
「拍手-握手」など報告の多い 10 例の異聴ペアを対象に以下の操作を行った。まず、対象
の語と近い意味を持つ語を分散表現により抽出し、意味の近い語彙を活性化するプライミ
ングを表現した。その語彙の中で、(i)異聴行列に基づいた編集距離と(ii)抽出した頻度に
より、音の距離が近く、頻度の高い語を異聴の予測とした。
結果として、報告された事例は特殊な地名や固有名詞の一部を除いて再現された。再現さ
れた例には「二子玉川→二俣川」、再現されなかった例には「千駄ヶ谷→センター街」があ
る。異聴行列を使わずに編集距離だけでも異聴は再現可能であったが、異聴行列に基づき異
なる予測が得られた。これは、より多くのデータセットでの評価の必要性を示すものの、言
語の背景や個人差に基づく異聴傾向を組み込んだ予測の実現性を示した。本研究の結果は、
難聴者の個別対応を含む言語訓練や対話の新たなアプローチに有意義な示唆を提供する。

## Demo Site

以下のウェブサイトで論文のデモを利用できます。

http://www.kikoepred.com/
