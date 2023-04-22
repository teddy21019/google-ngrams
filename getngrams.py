#!/usr/bin/env python
# -*- coding: utf-8 -*
from pandas import DataFrame  # http://github.com/pydata/pandas
import requests               # http://github.com/kennethreitz/requests
from bs4 import BeautifulSoup
import json
corpora = {'American English 2019': 'en-US-2019',
           'American English 2012': 'en-US-2012',
           'American English 2009': 'en-US-2009',
           'British English 2019': 'en-GB-2019',
           'British English 2012': 'en-GB-2012',
           'British English 2009': 'en-GB-2009',
           'English 2019': 'en-2019',
           'English 2012': 'en-2012',
           'English 2009': 'en-2009',
           'English Fiction 2019': 'en-fiction-2019',
           'English Fiction 2012': 'en-fiction-2012',
           'English Fiction 2009': 'en-fiction-2009',
           'English One Million': 'en-1M-2009',
           'Chinese 2019': 'zh-Hans-2019',
           'Chinese 2012': 'zh-Hans-2012',
           'Chinese 2009': 'zh-Hans-2009',
           'French 2019': 'fr-2019',
           'French 2012': 'fr-2012',
           'French 2009': 'fr-2009',
           'German 2019': 'de-2019',
           'German 2012': 'de-2012',
           'German 2009': 'de-2009',
           'Hebrew 2019': 'iw-2019',
           'Hebrew 2012': 'iw-2012',
           'Hebrew 2009': 'iw-2009',
           'Spanish 2019': 'es-2019',
           'Spanish 2012': 'es-2012',
           'Spanish 2009': 'es-2009',
           'Russian 2019': 'ru-2019',
           'Russian 2012': 'ru-2012',
           'Russian 2009': 'ru-2009',
           'Italian 2019': 'it-2019',
           'Italian 2012': 'it-2012'}

def getNgrams(query, corpus, startYear, endYear, smoothing, caseInsensitive):
    params = dict(content=query, year_start=startYear, year_end=endYear,
                  corpus=corpora[corpus], smoothing=smoothing,
                  case_insensitive=caseInsensitive)
    if params['case_insensitive'] is False:
        params.pop('case_insensitive')
    req = requests.get('http://books.google.com/ngrams/graph', params=params)

    if req.status_code == 200:
        data_script = BeautifulSoup(req.text, features="html.parser").select("#ngrams-data")[0].string
        data = json.loads(data_script)
        data = {d['ngram']: d['timeseries']
                for d in data }
        df = DataFrame(data)
        df.index = list(range(startYear, endYear+1))
    else:
        df = DataFrame()
    return req.url, params['content'], df