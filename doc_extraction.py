# pip install Wikipedia-API
import wikipediaapi
import os, sys
import pandas as pd
from collections import deque
from datetime import datetime
from utils import *

lang = 'en'
categories = {'Science':0, 'Sports':1, 'Economy':2, 'Politics':3, 'Education':4, 'Health':5, 'Entertainment':6}
stopPhrases = ['list of', 'index of']

# lang = 'tr'
# categories = {'Bilim':0, 'Spor':1, 'Ekonomi':2, 'Siyaset':3, 'Eğitim':4, 'Sağlık':5, 'Eğlence':6}
# stopPhrases = ['listesi']

num_docs = 100
minSummaryLen = 100
maxCatQueueSize = 200
wiki_wiki = wikipediaapi.Wikipedia(lang)

# create a filter to be used in filtering the documents
myFilter = filter(minSummaryLen, stopPhrases)

data = pd.DataFrame()
for cat_str, cat_num in categories.items():
    cat = wiki_wiki.page("Category:{}".format(cat_str))
    # create a category queue to implement BFS, BFS is preferred in searching articles 
    # because DFS would go in depth and can quickly extract irrelevant articles
    catQueue = deque()
    catQueue.append(cat.categorymembers)
    countDocs = 0

    while len(catQueue) > 0 and countDocs < num_docs:
        cur_cat = catQueue.popleft() # queue is first in first out

        for doc in cur_cat.values():
            # if it is a category, add it to the category queue
            # second if prevents the queue from exploding
            if doc.ns == wikipediaapi.Namespace.CATEGORY and len(catQueue) < maxCatQueueSize:
                catQueue.append(doc.categorymembers)
            # if it is an article, add it to the database
            # second if applies the created filter
            elif doc.ns == wikipediaapi.Namespace.MAIN:
                if not myFilter.filterDocs(doc):
                    _id = doc.pageid
                    _title = doc.title
                    _text = doc.summary
                    # TODO: this takes some time if performed for all the links
                    _links = getTopKLinks(doc, k=3)
                    thisRow = pd.DataFrame({'pageid':[_id], 'title':[_title], 'category':[cat_str], 'label':[cat_num], 'language':[lang], 'text':[_text], 'links':[_links]})
                    data = pd.concat([data,thisRow], ignore_index=True, axis=0)
                    countDocs += 1
                    print("Categorty: {} -- doc #{}".format(cat_str, countDocs))
                    if countDocs >= num_docs:
                        break
            else:
                # it is neither category nor article, skip
                continue


file_name =  "{}{}.csv".format(lang, datetime.now().strftime("_%m_%d"))
save_folder = os.path.join(sys.path[0], 'datasets')
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
file_dir = os.path.join(save_folder, file_name)
data.to_csv(file_dir)


