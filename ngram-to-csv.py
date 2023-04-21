from click import option
import streamlit as st
import pandas as pd
from getngrams import corpora, getNgrams
import matplotlib.pyplot as plt

st.write("# Google N-gram to CSV")
st.write("""(Credit to https://github.com/econpy/google-ngrams for the original work.
This is an updated version since Google changed its code.)\n
Use this website to easily extract data from the [Google Ngram Viewer](https://books.google.com/ngrams/info).
""")

st.markdown('---')

query = st.text_input(label="Enter your query:", value="housing bubble")

year_range = st.slider("Select the time period:", min_value=1700, max_value=2019, value=(1900, 2019))

with st.expander("Other options", expanded=False):

    corpus = st.selectbox("Select the corpus", options = corpora.keys(), index = 6)

    case_sensitive = st.checkbox("Sensitive to Case?", value=True)

    smoothing = st.slider("Smoothing Parameter (Moving average)", min_value=0, max_value=50, value = 2)

word_case = 'Sensitve' if case_sensitive else "Insensitive"
filename = f"{query}-{year_range[0]}-{year_range[1]}-{smoothing}-{word_case}.csv"

if st.button("Create") and query is not "":
    url,content,df = getNgrams(
        query=query,
        corpus=corpus,
        startYear=year_range[0],
        endYear=year_range[1],
        caseInsensitive= not case_sensitive,
        smoothing=smoothing
    )
    if not df.empty:
        st.write(f"Preview on [Google Ngram Viewer]({url})")
        fig, ax = plt.subplots()
        df.plot(kind = 'line', ax=ax)
        st.plotly_chart(fig, use_container_width=True)

        st.download_button("Download CSV",
                        df.to_csv(),
                        file_name=filename,
                       mime='text/csv')
    else:
        st.write("No data available!")