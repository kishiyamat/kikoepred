run:
	streamlit run app.py
config:
	streamlit config show
html:
	pandoc README.md -o index.html

