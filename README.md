---
title: "個人の異聴傾向を考慮した「聞き間違えやすい語」の予測—単語分散表現と確率、編集距離の応用—"
author: "岸山 健"
date: "2024-09-28"
---

# 個人の異聴傾向を考慮した「聞き間違えやすい語」の予測<br>--—単語分散表現と確率、編集距離の応用---

<div style="text-align: center;">
<p>岸山 健(東京大学) 野口 大斗(東京医科歯科大学) 黄竹佑(名古屋学院大学)<br>
kishiyama.t@gmail.com, noguchih425@gmail.com,<br>
huangcy.ut@gmail.com</p>
</div>

## Demo Site
[http://www.kikoepred.com/](http://www.kikoepred.com/)

## Abstract

本研究では、「渋谷--日比谷」などに見られる聞き間違えやすい語のペアを抽出する報告をもとに、
個人差を反映した上で語レベルの異聴を予測するモデルを提案・検証する。
すでに辞書と音声の分析から聞き間違えやすい語を抽出する報告は存在するが、
個人差を反映できない点が課題であった。
本研究では、入力の音素に対して知覚された音素を記述する「異聴行列」として個人差を取り込んだ。
この行列を本研究では「編集距離」の計算時に考慮した。
編集距離では、文字列の変換に必要な操作の回数がコストとして示される。
例えば、「sibuya→hibiya」の音素列のコストは 2 となる。
ここで s を h と知覚する異聴行列を持つ個人を反映するには、s→h のコストを 0 とする。
その結果、コストは低くなり聞き間違える度合いの個人差を反映できる。

実験では、要旨版 Wikipedia コーパスの 206,060 語の頻度を抽出し、
「渋谷--日比谷」や「拍手--握手」など報告の多い 10 例の異聴ペアを対象に以下の操作を行った。
まず、対象の語と近い意味を持つ語を分散表現により抽出し、
意味の近い語彙を活性化するプライミングを表現した。
その語彙の中で、(i)異聴行列に基づいた編集距離と(ii)抽出した頻度により、
音の距離が近く、頻度の高い語を異聴の予測とした。
結果として、報告された事例は特殊な地名や固有名詞の一部を除いて再現された。
再現された例には「二子玉川→二俣川」、再現されなかった例には「千駄ヶ谷→センター街」がある。
異聴行列を使わずに編集距離だけでも異聴は再現可能であったが、
異聴行列に基づき異なる予測が得られた。
これは、より多くのデータセットでの評価の必要性を示すものの、
言語の背景や個人差に基づく異聴傾向を組み込んだ予測の実現性を示した。
本研究の結果は、難聴者の個別対応を含む言語訓練や対話の新たなアプローチに有意義な示唆を提供する。

## 免責事項

本アプリケーション「聞こえ予測シミュレーター」（以下「本アプリケーション」）は、
音声知覚に関する研究目的で作成されたものであり、
使用に際して以下の免責事項に同意したものとみなされます。

1. **提供情報の正確性について**: 
   本アプリケーションは音声知覚に関するデータを基にした予測を提供しますが、すべての結果が正確かつ完全であることを保証するものではありません。予測結果に基づく判断は、自己責任で行ってください。
2. **医療的アドバイスの代替について**: 
   本アプリケーションは、医療的な診断や治療のために設計されたものではありません。聴覚に関する問題や健康に関する懸念がある場合は、適切な専門医に相談してください。
3. **使用に関する責任**: 
   本アプリケーションの使用により生じた損害やトラブルについて、開発者および運営者は一切の責任を負いません。本アプリケーションを使用することによって生じるいかなる直接的・間接的な損害や不利益についても、すべて利用者の自己責任となります。
4. **アプリケーションの変更および中止**: 
   本アプリケーションの仕様、提供内容、機能などは、予告なく変更・中止することがあります。開発者は、これに関連して発生する損害について責任を負いません。
5. **バグや改善点の報告について**: 
   本アプリケーションのバグや改善点などについては、[GitHubの専用ページ](https://github.com/kishiyamat/kikoepred/issues) より報告をお願いします。報告された内容は可能な範囲で対応いたしますが、すべての報告に対応できることを保証するものではありません。
6. **著作権について**: 
   本アプリケーションおよびその内容に関する著作権は、開発者および関連する第三者に帰属します。無断での複製、配布、改変などは法律で禁止されています。
