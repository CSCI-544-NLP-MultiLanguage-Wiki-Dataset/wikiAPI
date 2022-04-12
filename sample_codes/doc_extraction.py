# pip install Wikipedia-API
import wikipediaapi
import os, sys
import pandas as pd

lang = 'en'
categories = {'Science':0, 'Sports':1, 'Economy':2, 'Politics':3, 'Education':4, 'Health':5, 'Entertainment':6}
num_docs = 10
wiki_wiki = wikipediaapi.Wikipedia(lang)

data = pd.DataFrame()
for c, l in categories.items():
    cat = wiki_wiki.page("Category:{}".format(c))
    count = 0
    for doc in cat.categorymembers.values():
        text = doc.summary
        label = c
        label_code = l
        thisRow = pd.DataFrame({'text':[text], 'category':[label], 'label':[label_code], 'language':[lang]})
        data = pd.concat([data,thisRow], ignore_index=True, axis=0)
        count += 1
        if count > num_docs - 1 :
            break
file_name = "{}.csv".format(lang)
file_dir = os.path.join(sys.path[0], file_name)
data.to_csv(file_dir)


