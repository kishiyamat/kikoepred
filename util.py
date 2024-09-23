import gensim
from dataclasses import dataclass
import pickle
import numpy as np
import re
import streamlit as st

# 読み仮名からローマ字への変換辞書
# 「チャ」は ti_ya となる程度の単純さ
kana_to_romaji = {
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
    'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
    'サ': 'sa', 'シ': 'si', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
    'ザ': 'za', 'ジ': 'zi', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
    'タ': 'ta', 'チ': 'ti', 'ツ': 'tu', 'テ': 'te', 'ト': 'to',
    'ダ': 'da', 'ヂ': 'di', 'ヅ': 'du', 'デ': 'de', 'ド': 'do',
    'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
    'ハ': 'ha', 'ヒ': 'hi', 'フ': 'hu', 'ヘ': 'he', 'ホ': 'ho',
    'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
    'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
    'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
    'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
    'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
    'ワ': 'wa', 'ヲ': 'wo', 'ン': 'N',
    # よう音
    'ャ': '_ya', 'ュ': '_yu', 'ョ': '_yo',
    # 小文字のものも設けた方が良い
    'ァ': '_xa', 'ィ': '_xi', 'ゥ': '_xu', 'ェ': '_xe', 'ォ': '_xo',
    # ヴァ は vu_xa のようになる。_xや_yはモーラを形成しない
    'ヴ': 'vu',
    'ッ': 'Q', 'ー': ':',
}
ordered = [
    'p', 'b', 't', 'd', 'k', 'g', 's', 'z', 'h', 'm', 'n', 'r', 'y', 'w', 'v',  # others
    'a', 'i', 'u', 'e', 'o',  # single
    'Q', ':', 'N',  # single
    '_y', '_x',  # others
]
single = filter(lambda k_v: len(k_v[1]) == 1, kana_to_romaji.items())
single = list(map(lambda t: t[1], single))
others = set([v[:-1] for _, v in kana_to_romaji.items() if len(v) > 1])
all_phonemes = list(filter(len, others)) + single
assert set(all_phonemes) == set(ordered)

# パターンは、すべての音素を"|"で連結して生成
# all_phonemes の中の要素のみで最長マッチ
phoneme_pattern = "|".join(sorted(all_phonemes, key=len, reverse=True))

def decompose_string(s: str, pattern) -> list[str]:
    return re.findall(pattern, s)

@st.cache_data
def load_model():
    model_dir = 'data/new_entity_vector.model.bin'
    model = gensim.models.Word2Vec.load(model_dir)
    return model


@st.cache_data
def load_word_freq():
    # pkl形式で保存したCounterオブジェクトを読み込む
    # https://github.com/kishiyamat/la-kentei-yaminabe/blob/main/notebooks/talking_aid_word_freq.ipynb
    with open("data/word_freq.pkl", "rb") as f:
        return pickle.load(f)


@st.cache_data
def load_word_kana():
    with open("data/word_kana.pkl", "rb") as f:
        return pickle.load(f)

def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

def generate_grid_search_space(step=10):
    grid_search_space = []
    for a in np.arange(0, 100 + step, step):
        for b in np.arange(0, 100 - a + step, step):
            c = 100 - a - b
            if c >= 0:
                grid_search_space.append([a, b, c])
    return grid_search_space


@dataclass
class Result:
    cm_pattern: str
    sim_w: int
    freq_w: int
    pdist_w: int
    n_prime: int
    intended: str
    expected: str
    found: bool = False
    is_first: bool = False
    score: float = 0


assert set(all_phonemes) == set(ordered)