import os, sys
import pandas as pd
from statistics import mean, stdev
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})

loadFileName = 'en_04_17.csv'
mainDir = os.path.join(sys.path[0], 'datasets')
filePath = os.path.join(mainDir, loadFileName)

# setup the save dir
saveDir = os.path.join(mainDir, loadFileName.split('.')[0])
if not os.path.exists(saveDir):
    os.makedirs(saveDir)

# load the dataset
data = pd.read_csv(filePath)

# print the column names
for col in data.columns:
    print(col)

# category extraction
categoriesAll = data['category'].tolist()
categoryDict = {}
for cat in categoriesAll:
    if cat not in categoryDict:
        categoryDict[cat] = 0
    categoryDict[cat] += 1

print("Number of categories: {}".format(len(categoryDict)))
print("Categories: {}".format(categoryDict))

# text extraction
textAll = data['text'].tolist()
textLenAll = []
for text in textAll:
    textLenAll.append(len(text))

meanText = mean(textLenAll)
stdText = 2*stdev(textLenAll)/(len(textLenAll)**(1/2))
print("Average text len: {:.3f} characters".format(meanText))

# link extraction
linkAll = data['links'].tolist()
linkLenAll = []
for link in linkAll:
    link = link.strip('][').split(', ')
    linkLenAll.append(len(link))

meanLink = mean(linkLenAll)
stdLink = 2*stdev(linkLenAll)/(len(linkLenAll)**(1/2))
print("Average number of links: {:.3f}".format(meanLink))

# category bar plot
fig = plt.figure(figsize=(16, 12), dpi=160)

catNamePlot = []
catNumPlot = []
for k, v in categoryDict.items():
    catNamePlot.append(k)
    catNumPlot.append(v)
plt.bar(catNamePlot, catNumPlot)

plt.title('Number of documents in each category')
plt.xlabel('Categories')
plt.ylabel('Number of documents')

figName = 'categories.png'
figPath = os.path.join(saveDir, figName)
plt.savefig(figPath)

# summary bar plot
fig = plt.figure(figsize=(9, 12), dpi=160)

plt.bar([1], [meanText], yerr=[stdText], error_kw=dict(lw=5, capsize=8, capthick=3))

plt.title('Text statistics')
plt. xticks([1], " ")
plt.ylabel('Number of characters')

figName = 'textStats.png'
figPath = os.path.join(saveDir, figName)
plt.savefig(figPath)

# summary bar plot
fig = plt.figure(figsize=(9, 12), dpi=160)

plt.bar([1], [meanLink], yerr=[stdLink], error_kw=dict(lw=5, capsize=8, capthick=3))

plt.title('Reference statistics')
plt. xticks([1], " ")
plt.ylabel('Number of references')

figName = 'referenceStats.png'
figPath = os.path.join(saveDir, figName)
plt.savefig(figPath)
