import streamlit as st
from util import load_model, load_word_freq, load_word_kana, all_phonemes
from note import note_intro, note_post, note_future
from distance_computer import DisanceComputer
from streamlit_ui import StreamlitUI

st.set_page_config(
    page_title="Kikoe Pred",
    page_icon=":ear:",
)
hide = '''
<style>
/* # https://qiita.com/papasim824/items/af2d18f3802e632ffa80 */
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
#MainMenu {
    visibility: hidden;
    display: none;
}
.appview-container .main .block-container {
    padding-top: 0rem;
    padding-right: 0rem;
    padding-left: 0rem;
    padding-bottom: 0rem;
}
.reportview-container {
    padding-top: 0rem;
    padding-right: 3rem;
    padding-left: 3rem;
    padding-bottom: 0rem;
}
header[data-testid="stHeader"] {
    z-index: -1;
}
div[data-testid="stToolbar"] {
    z-index: 100;
}
div[data-testid="stDecoration"] {
    z-index: 100;
}
</style>
'''
st.markdown(hide, unsafe_allow_html=True)

# TODO: Testの追加
# init model 
N = len(all_phonemes)
model = load_model()
word_freq = load_word_freq()
word_kana = load_word_kana()
vocabulary_size = len(word_freq)
freq = load_word_freq()

# init UI
slui = StreamlitUI()

# 単語の指定
slui.set_intended_word()

slui.choose_confusion_matrix_pattern()
slui.set_confusion_matrix(slui.cm_pattern, N)
dc = DisanceComputer(slui.confusion_matrix, model, freq, word_kana, N, 1000)
slui.size_note.write(note_intro(vocabulary_size))

slui.set_intended_speech(dc.word_to_phoneme)

slui.validate_intended_word(word_freq.keys())


# dcで計算しでdc.resultsを加工していく
dc.set_similarity_df(slui.intended_word)
dc.set_phoneme_dist(slui.intended_speech)
st.write("### Normalized")
st.write(note_post)
dc.assign_log()


st.write("### Results")
slui.set_weights()
dc.assign_score(slui.sim_w, slui.freq_w, slui.dist_w)
th = (slui.sim_w+slui.freq_w+slui.dist_w)*0.5 # 半分だけ見る
st.table(dc.results.query(f"score > {th}")
    .query("similarity<0.99")
    .sort_values(by='score', ascending=False)
    .head(10))
st.write("### Future Works")
st.write(note_future)
