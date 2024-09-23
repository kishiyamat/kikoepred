import spacy

# Ginzaモデルをロード(読みを取得する目的)
nlp = spacy.load('ja_ginza')

def word_to_kana(text: str) -> str:
    # ローマ字→カナへの変換
    # TODO: ここはモデルに依存する。よくテストする
    doc = nlp(text)
    kana_list = []
    for sent in doc.sents:
        for token in sent:
            # 漢字→カナ
            kana_list.extend(token.morph.get("Reading"))
    return "".join(kana_list)
