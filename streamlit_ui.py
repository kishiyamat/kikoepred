import itertools
import pandas as pd
import streamlit as st
import pandas as pd
from util import ordered
from note import note_cm, intend_note, note_all

class StreamlitUI:
    def __init__(self):
        st.write("## Kikoe Pred")
        st.write("日本音声学会2024で公開した研究のデモです。要旨: [https://kishiyamat.github.io/kikoepred](https://kishiyamat.github.io/kikoepred) ")
        self.size_note = st.empty()
        
    def choose_confusion_matrix_pattern(self):
        st.write("### Confusion Matrix")
        st.write(note_cm)
        self.cm_pattern_radio = st.empty()
        self.plot_cm = st.empty()
        self.confusion_matrix = None
        cm_pattern = self.cm_pattern_radio.radio(
            "confusion matrix の種類",
            [
                "simple: 単純な混合行列でktshの4種類が区別できません。",
                "none: 全て1 (ベースライン)",
                "shitara1972-L3-kths-all: 設楽(1972)のL3",
                "shitara1972-L3-kths: 設楽(1972)のL3でkthsが困難なケース",
            ])
        self.cm_pattern, _ = cm_pattern.split(":")

    @staticmethod
    def get_confusion_matrix(cm_pattern, N):
        confusion_matrix = pd.DataFrame(0, index=ordered, columns=ordered)
        if cm_pattern =="none":
            for i in range(N):
                confusion_matrix.iat[i, i] = 1
        elif cm_pattern =="shitara1972-L3-kths":
            uploaded_file = "data/confusion_matrix/confusion_matrix_l3_kths - confusion_matrix.csv"
            confusion_matrix = pd.read_csv(uploaded_file, index_col=0)
        elif cm_pattern =="shitara1972-L3-kths-all":
            uploaded_file = "data/confusion_matrix/confusion_matrix_l3_kths - consonant_vowel.csv"
            confusion_matrix = pd.read_csv(uploaded_file, index_col=0)
        elif cm_pattern =="simple":
            combinations = []
            combinations += list(itertools.product("ktsh", repeat=2))
            combinations = list(filter(lambda ij: ij[0] != ij[1], combinations))
            for i in range(N):
                confusion_matrix.iat[i, i] = 1
            for stim, res in combinations:
                # 論文に合わせてCMは列にstim(src)を持たせている
                confusion_matrix.loc[res, stim] += 1
        return confusion_matrix

    def set_confusion_matrix(self, cm_pattern, N):
        self.confusion_matrix = StreamlitUI.get_confusion_matrix(cm_pattern, N) 

    def set_intended_word(self):
        st.write("### Intended Word")
        self.intended_input_field = st.empty()
        self.intended_word = ""
        self.intended_word = self.intended_input_field.text_input(intend_note, placeholder="例: 日比谷")

    def set_intended_speech(self, word_to_phoneme: callable):
        self.intended_speech = word_to_phoneme(self.intended_word)

    def validate_intended_word(self, vocab):
        if not len(self.intended_word.strip()):
            st.warning(f"{intend_note}を入力し、ここをタップ/クリックください。")
            st.write("")
            st.stop()
        if not self.intended_word in vocab:
            st.warning(f"すみません、まだ辞書に含められていない語彙です。{intend_note}を入力し、ここをタップ/クリックください。")
            st.write("")
            st.stop()

    def set_weights(self):
        st.write("#### Similarity/Frequency/Distance")
        st.write(note_all)
        res_s_w, res_f_w, res_d_w  = st.columns(3)
        self.sim_w = res_s_w.slider("Estimate for similarity (default: 10)", 0, 100, 10)
        self.freq_w = res_f_w.slider("Estimate for frequency (10)", 0, 100, 10)
        self.dist_w = res_d_w.slider("Estimate for audio similarity (80)", 0, 100, 80)
