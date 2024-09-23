import os
import pickle
from tqdm import tqdm
from util import word_to_kana

# word_freqを読み込む
word_freq_path = "word_freq.pkl"
with open(word_freq_path, "rb") as f:
    word_freq = pickle.load(f)

# word_kana.pklのパス
output_path = "word_kana.pkl"

print(word_to_kana("渋谷"))

# word_kana.pklが存在するかチェック
if os.path.exists(output_path):
    print(f"{output_path} は既に存在します。処理をスキップします。")
else:
    # word2phonemeを適用し、結果を辞書にする
    word_kana = {}
    for word in tqdm(word_freq.keys(), desc="Processing words"):
        word_kana[word] = word_to_kana(word)
    
    # pkl形式で保存
    with open(output_path, "wb") as f:
        pickle.dump(word_kana, f)
    
    print(f"{output_path} に保存されました。")

