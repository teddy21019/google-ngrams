from getngrams import getNgrams

url,content,df = getNgrams(
    query="Dawes Plan",
    corpus="German 2012",
    startYear=1900,
    endYear=2000,
    caseInsensitive= False,
    smoothing=2
    )
print(content)