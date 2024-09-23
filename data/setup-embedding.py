import os
import pickle
import requests
from tqdm import tqdm
from gensim.models import KeyedVectors, Word2Vec

# word2vec
filename = "20170201.tar.bz2"
url = f"http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/data/{filename}"
model_dir = 'entity_vector/entity_vector.model.bin'
new_model_dir = 'new_entity_vector.model.bin'

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    with open(filename, 'wb') as file:
        for data in tqdm(response.iter_content(block_size), total=total_size // block_size, unit='KiB', desc="Downloading"):
            file.write(data)

def extract_file(filename):
    os.system(f"tar -xvjf {filename}")
    os.remove(filename)

def load_model(model_dir):
    model = KeyedVectors.load_word2vec_format(model_dir, binary=True)
    return model

from tqdm import tqdm

def filter_model(model, word_freq):
    # 必要な語彙とそのインデックスを取得する
    words = list(word_freq.keys())
    indices = []
    selected_words = []
    
    for word in tqdm(words, desc="Filtering words"):
        if word in model.key_to_index:
            indices.append(model.key_to_index[word])
            selected_words.append(word)
    
    # 必要な語彙とベクトルを取得する
    selected_vectors = model.vectors[indices]
    
    # 新しいモデルを作成する
    new_model = Word2Vec(vector_size=model.vector_size, min_count=1)
    new_model.build_vocab([selected_words])
    
    # 新しいモデルにベクトルを追加する
    new_model.wv.vectors = selected_vectors
    new_model.wv.index_to_key = selected_words
    new_model.wv.key_to_index = {word: i for i, word in enumerate(selected_words)}

    return new_model



# ファイルが存在しない場合のみダウンロードを実行
if not os.path.exists(model_dir):
    if not os.path.exists(filename):
        print("ファイルをダウンロードしています...")
        download_file(url, filename)
        print("ファイルのダウンロードが完了しました。解凍しています...")
        extract_file(filename)

    # モデルのロード含めて30秒程度かかる
    print("Word2Vecモデルを読み込んでいます...")
    model = load_model(model_dir)
    print("Word2Vecモデルが正常に読み込まれました。")
else:
    print("モデルファイルは既に存在します。")
    model = load_model(model_dir)

# word_freqを読み込む
with open("word_freq.pkl", "rb") as f:
    word_freq = pickle.load(f)

# モデルをフィルタリングして新しいモデルを生成
print("Word2Vecモデルをフィルタリングしています...")
new_model = filter_model(model, word_freq)

# 新しいモデルを保存
print(f"新しいWord2Vecモデルを{new_model_dir}に保存しています...")
new_model.save(new_model_dir)
print("新しいWord2Vecモデルが正常に保存されました。")
