import streamlit as st
import pandas as pd
from getngrams import corpora, getNgrams
import matplotlib.pyplot as plt

st.write("# Google N-gram to CSV")
st.write("""(Original work by https://github.com/econpy/google-ngrams.
This is an updated version since Google changed its code.)\n
Retrieve data from Google Ngram viewer.
""")

query = st.text_input(label="Query")

year_range = st.slider("Year", min_value=1700, max_value=2019, value=(1900, 2019))

corpus = st.selectbox("Corpus", options = corpora.keys(), index = 6)

case_sensitive = st.checkbox("Sensitive to Case?", value=True)

smoothing = st.slider("Smoothing Parameter", min_value=0, max_value=50, value = 2)

word_case = 'Sensitve' if case_sensitive else "Insensitive"
filename = f"{query}-{year_range[0]}-{year_range[1]}-{smoothing}-{word_case}.csv"

if st.button("Create"):
    _,__,df = getNgrams(
        query=query,
        corpus=corpus,
        startYear=year_range[0],
        endYear=year_range[1],
        caseInsensitive= not case_sensitive,
        smoothing=smoothing
    )
    fig, ax = plt.subplots()
    df.plot(kind = 'line', ax=ax)
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download CSV",
                       df.to_csv(),
                       file_name=filename,
                       mime='text/csv')