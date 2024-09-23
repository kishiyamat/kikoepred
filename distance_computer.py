import numpy as np
import pandas as pd
import pandas as pd
from util import kana_to_romaji, phoneme_pattern, decompose_string

class DisanceComputer:
    def __init__(self, confusion_matrix, language_model, freqency, word_kana, tokenizer, N, TOP_N=1000):
        self.confusion_matrix = confusion_matrix
        self.language_model = language_model
        self.freqency =freqency
        self.word_kana =word_kana
        self.tokenizer = tokenizer
        self.TOP_N =TOP_N
        self.N = N
        cm = self.confusion_matrix.copy()
        for i in range(self.N):
            # i,iを処理した段階で分母が1になるので変数を作る(ターゲットの認識を分母とする)
            denom = cm.iat[i, i]
            for j in range(self.N):
                cm.iat[j, i] = cm.iat[j, i] / denom
        self.confusion_matrix_norm  = cm
        self.results = pd.DataFrame([], columns=["entity", "similarity", "freq", "phoneme_dist", "phoneme", "score"])

    def get_token(self, word):
        # TODO: これもさっさと辞書にするなりして外に出す
        # 単語をトークンに分割
        # トークンの品詞情報を取得して返す
        return self.tokenizer.tokenize(word).__next__()

    def get_pos(self, token):
        return token.part_of_speech.split(",")[0]

    def get_infl(self, token):
        return token.infl_form

    def cost_phoneme(self, stim, resp):
        # こちらは編集コスト: 同じ知覚なら0
        # 一般的にsrc->tgtだが、
        # 論文に合わせてCMは列にstim(src)を持たせている
        return 1-self.confusion_matrix_norm.loc[resp, stim]

    def compute_distance(self, s1: list[str], s2: list[str]):
        len_s1, len_s2 = len(s1), len(s2)
        dp = [[0 for _ in range(len_s2 + 1)] for _ in range(len_s1 + 1)]
        for i in range(len_s1 + 1):
            for j in range(len_s2 + 1):
                # 1. initialize
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                # 2. dynamic programming
                else:
                    # 違う時のコストを払う。
                    cost = self.cost_phoneme(s1[i-1], s2[j-1])
                    insert = dp[i][j - 1] + 1
                    delete = dp[i - 1][j] + 1
                    replace = dp[i - 1][j - 1] + cost
                    dp[i][j] = min(insert, delete, replace)
        # 3. results
        return dp[len_s1][len_s2]

    def word_to_phoneme(self, word, pattern=phoneme_pattern) -> list[str]:
        kana = self.word_kana.get(word, "")
        romaji = "".join([kana_to_romaji.get(k, "") for k in kana])
        word_to_phoneme = decompose_string(romaji, pattern)
        return word_to_phoneme

    def candidates(self, intended_word: str):
        # https://teratail.com/questions/362402
        return [(intended_word, 1)] + self.language_model.wv.most_similar(intended_word, topn=self.TOP_N)

    def set_similarity_df(self, intended_word: str):
        self.results[["entity", "similarity"]] = self.candidates(intended_word)
        # 無駄な記号の削除: 青山_(東京都港区) -> 青山
        self.results["entity"] = self.results["entity"].str.split("_").str[0]
        self.results["entity"] = self.results["entity"].str.replace(r'[^\w]', '', regex=True)
        # similarity
        self.results = self.results.groupby('entity')['similarity'].mean().reset_index()
        self.results = self.results.sort_values(by='similarity', ascending=False).reset_index(drop=True)

    def set_phoneme_dist(self, intended_speech):
        # 3. 音素に変換し、距離を計算
        df = self.results
        df["phoneme"] = df["entity"].apply(lambda x: self.word_to_phoneme(x, phoneme_pattern))
        self.max_phonemes = max(df["phoneme"].apply(len))

        df["freq"] = df["entity"].apply(lambda x: self.freqency.get(x, 0))
        df["phoneme_dist"] = df["phoneme"].apply(lambda p: self.compute_distance(s1=intended_speech, s2=p))
        df["phoneme"] = df["phoneme"].apply(lambda l: "".join(l))
        self.results = df

    def assign_log(self):
        df = self.results
        # 0--1
        df['freq_log_norm'] = np.log1p(df['freq'])/np.log1p(max(df['freq']))
        # 0--1
        df['phoneme_sim_norm'] = 1-(df['phoneme_dist']/self.max_phonemes)
        self.results = df

    def assign_score(self, sim_w, freq_w, dist_w):
        df = self.results
        df["score"]= (
            df['similarity']*sim_w+
            df['freq_log_norm']*freq_w+
            df['phoneme_sim_norm']*dist_w)
        self.results = df
