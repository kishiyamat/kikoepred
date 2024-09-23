def note_intro(vocab_size):
    return f"""
    1. 想定している・されていた語を入力
    1. 対象のconfusion matrixを取得します
    1. 意味のベクトルから似た語を取得します
    1. 確率と音の近さを考慮します
    1. 意味、確率、音の近さでランキングします

    補足
    1. 速度を優先しているので語彙数は{vocab_size}です。
    """

note_cm = """
サンプルとして、文字列 "ksth" を識別しない組み合わせをデカルト積で作成しています。
つまり、/kisi/と/siki/は同じということになります。
"""

note_post = """
- similarity: as is
- freq_log_norm: log(freq)/max(log(freq))
- audio_distance_norm: audio_distance/max(max_phonemes)
"""
intend_note = "想定している、されていた単語"
note_all = """
- 頻度は全て1を足しておく。
"""
note_future = """
- STの人が思いつく聞き間違いのリストの再現
- 同音異漢字を除去
- 品詞を考慮 (PSJ2024では実施済み)
- モックの混合行列のより正確なバージョン
- より大きな辞書の利用
- パラメータの設定
- ピッチの考慮
- モーラの考慮
- 差分の位置の考慮 (冒頭・末尾は軽く)
- 単語だけでなく文を考慮
- 頻度重すぎ
"""