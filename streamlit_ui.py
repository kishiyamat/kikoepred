
import plotly.express as px
import itertools
import pandas as pd
import streamlit as st
import pandas as pd
from util import ordered
from note import note_cm, intend_note, note_all

class StreamlitUI:
    def __init__(self):
        st.write("## Kikoe Pred")
        self.size_note = st.empty()
        st.write("### Phoneme Confusion Matrix Visualization")
        
    def choose_confusion_matrix_pattern(self):
        st.write(note_cm)
        self.cm_pattern_radio = st.empty()
        self.plot_cm = st.empty()
        self.confusion_matrix = None
        cm_pattern = self.cm_pattern_radio.radio(
            "confusion matrix の種類",
            [
                "none: 全て1 (ベースライン)",
                "simple: 単純な混合行列でktshの4種類が区別できません。",
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

    @staticmethod
    def show_confusion_matrix(confusion_matrix, N):
        fig = px.imshow(
            confusion_matrix,
            labels=dict(x="Stimulus", y="Response", color="Ratio"),
            x=ordered,
            y=ordered,
            color_continuous_scale="Viridis"
        )
        fig.update_layout(
            title="Phoneme Confusion Matrix",
            xaxis=dict(tickmode='array', tickvals=list(
                range(N)), ticktext=ordered),
            yaxis=dict(tickmode='array', tickvals=list(
                range(N)), ticktext=ordered),
            coloraxis_colorbar=dict(
                title="Ratio",
                x=0.73,  # X軸からの距離を調整
                y=0.5,   # Y軸の中央に配置
                len=0.9,  # レジェンドの長さを調整
                thickness=20,  # レジェンドの幅を調整
            ),
        )
        st.plotly_chart(fig)

    @staticmethod
    def draw_sim_freq_aud(df):
        # Similarity のヒストグラム
        res_s_1, res_f_1, res_d_1  = st.columns(3)
        fig_similarity = px.histogram(df, x='similarity', nbins=10, title='Histogram of Similarity')
        res_s_1.plotly_chart(fig_similarity)

        fig_freq = px.histogram(df, x='freq', nbins=10, title='Histogram of Frequency')
        res_f_1.plotly_chart(fig_freq)

        fig_audio_distance = px.histogram(df, x='phoneme_dist', nbins=10, title='Histogram of Phoneme Distance')
        res_d_1.plotly_chart(fig_audio_distance)

        res_s_2, res_f_2, res_d_2  = st.columns(3)
        res_s_2.plotly_chart(fig_similarity)

        fig_freq = px.histogram(df, x='freq_log_norm', nbins=10, title='Histogram of Frequency (log)')
        res_f_2.plotly_chart(fig_freq)

        fig_audio_distance = px.histogram(df, x='phoneme_sim_norm', nbins=10, title='Histogram of 1-(Phoneme Distance/Max Phonemes)')
        res_d_2.plotly_chart(fig_audio_distance)

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
