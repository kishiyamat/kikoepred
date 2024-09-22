import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Confusion Predictor! 👋")

st.sidebar.success("機能を選んでください")

st.markdown(
    """
    Confusion Predictor は難聴に関する
    研究の社会実装を目指したプロジェクトです。
    **👈 デモアプリや実験は左のサイドバーから選択できます。**
    ### 各ページの説明
    - app: このページです。
    - demo: 混合行列と単語から異聴を予測します。
    - experiement: psj2024の実験です。
"""
)