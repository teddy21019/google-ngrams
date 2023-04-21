#!/usr/bin/env python
# -*- coding: utf-8 -*
from pandas import DataFrame  # http://github.com/pydata/pandas
import requests               # http://github.com/kennethreitz/requests
from bs4 import BeautifulSoup
import json
corpora = {'American English 2019': 'eng_us_2019',
           'American English 2012': 'eng_us_2012',
           'American English 2009': 'eng_us_2009',
           'British English 2019': 'eng_gb_2019',
           'British English 2012': 'eng_gb_2012',
           'British English 2009': 'eng_gb_2009',
           'English 2019': 'eng_2019',
           'English 2012': 'eng_2012',
           'English 2009': 'eng_2009',
           'English Fiction 2019': 'eng_fiction_2019',
           'English Fiction 2012': 'eng_fiction_2012',
           'English Fiction 2009': 'eng_fiction_2009',
           'English One Million': 'eng_1m_2009',
           'Chinese 2019': 'chi_sim_2019',
           'Chinese 2012': 'chi_sim_2012',
           'Chinese 2009': 'chi_sim_2009',
           'French 2019': 'fre_2019',
           'French 2012': 'fre_2012',
           'French 2009': 'fre_2009',
           'German 2019': 'ger_2019',
           'German 2012': 'ger_2012',
           'German 2009': 'ger_2009',
           'Hebrew 2019': 'heb_2019',
           'Hebrew 2012': 'heb_2012',
           'Hebrew 2009': 'heb_2009',
           'Spanish 2019': 'spa_2019',
           'Spanish 2012': 'spa_2012',
           'Spanish 2009': 'spa_2009',
           'Russian 2019': 'rus_2019',
           'Russian 2012': 'rus_2012',
           'Russian 2009': 'rus_2009',
           'Italian 2019': 'ita_2019',
           'Italian 2012': 'ita_2012'}

def getNgrams(query, corpus, startYear, endYear, smoothing, caseInsensitive):
    params = dict(content=query, year_start=startYear, year_end=endYear,
                  corpus=corpora[corpus], smoothing=smoothing,
                  case_insensitive=caseInsensitive)
    if params['case_insensitive'] is False:
        params.pop('case_insensitive')
    req = requests.get('http://books.google.com/ngrams/graph', params=params)

    if req.status_code == 200:
        data_script = BeautifulSoup(req.text).select("#ngrams-data")[0].string
        data = json.loads(data_script)
        data = {d['ngram']: d['timeseries']
                for d in data }
        df = DataFrame(data)
        df.index = list(range(startYear, endYear+1))
    else:
        df = DataFrame()
    return req.url, params['content'], df