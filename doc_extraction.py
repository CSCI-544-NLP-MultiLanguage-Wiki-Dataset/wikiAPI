# pip install Wikipedia-API
import wikipediaapi
import os, sys
import pandas as pd
from collections import deque
from datetime import datetime
from utils import *

lang = 'en'
categories = ['Science', 'Sports', 'Economy', 'Politics', 'Education', 'Health', 'Entertainment']
stopPhrases = ['list of', 'index of']
categoryNumsToRun = [1,2,3]

# lang = 'tr'
# categories = ['Bilim', 'Spor', 'Ekonomi', 'Siyaset', 'Eğitim', 'Sağlık', 'Eğlence']
# stopPhrases = ['listesi']

num_docs = 1000
minSummaryLen = 100
maxCatQueueSize = 200
switch_append = "append" # append or create a dataset

# either create a new dataset or append to a previously created one
if switch_append == "append":
    file_name = "en_04_18.csv"
else:
    file_name =  "{}{}.csv".format(lang, datetime.now().strftime("_%m_%d"))

# setup the paths
save_folder = os.path.join(sys.path[0], 'datasets')
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
file_dir = os.path.join(save_folder, file_name)

# if appending a dataset, load it
if switch_append == "append":
    data = pd.read_csv(file_dir)
else:
    data = pd.DataFrame()

wiki_wiki = wikipediaapi.Wikipedia(lang)

# create a filter to be used in filtering the documents
myFilter = filter(minSummaryLen, stopPhrases)

for cat_num in categoryNumsToRun: # range(len(categories)):
    cat_str = categories[cat_num]
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
                    # _links = getTopKLinks(doc, k=3)
                    _links = getCitations(doc, lang)
                    thisRow = pd.DataFrame({'pageid':[_id], 'title':[_title], 'category':[cat_str], 'label':[cat_num], 'language':[lang], 'text':[_text], 'links':[_links]})
                    data = pd.concat([data,thisRow], ignore_index=True, axis=0)
                    countDocs += 1
                    print("Categorty: {} -- doc #{} -- title: {}".format(cat_str, countDocs, _title))
                    if countDocs >= num_docs:
                        break
            else:
                # it is neither category nor article, skip
                continue

    data.to_csv(file_dir)


