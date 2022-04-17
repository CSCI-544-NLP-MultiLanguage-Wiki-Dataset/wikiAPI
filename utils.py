import wikipediaapi
import requests
from bs4 import BeautifulSoup

def getCitations(doc, lang, k = None):
    '''
    getCitations function returns the references in the summary.
    '''
    if lang == 'en':
        rq = f"https://en.wikipedia.org/?curid={doc.pageid}"
    elif lang == 'tr':
        rq = f"https://tr.wikipedia.org/?curid={doc.pageid}"
    req = requests.get(rq)
    soup = bs(req.text, "html.parser")
    main = soup.find("div", {"class": "mw-parser-output"})
    toc = main.find("div", {"id":"toc"})
    links = []
    for tag in main:
        if tag == toc:
            break
        if tag.name == 'p':
            links.extend(list(map(lambda x: x.get('href'), tag.find_all('a'))))

    final_links = list(filter(lambda x: x[:5] == '/wiki', links))

    return final_links

def getTopKLinks(doc, k=3):
    '''
    getTopKLinks function returns the first k internal references (not citations)
    given a wikipedia page. This code can be later updated to extract only the links
    in the summary
    '''
    links = []
    counter = 0
    for link in doc.links.values():
        if link.ns == wikipediaapi.Namespace.MAIN:
            links.append(link.pageid)
            counter += 1
        if counter >= k:
            break
    return links

class filter:
    def __init__(self, minSummaryLen, stopPhrases):
        self.minSummaryLen = minSummaryLen
        self.stopPhrases = stopPhrases

    def filterDocs(self, doc):
        '''
        Some wikipedia pages are different than others. For example some pages are too
        short or repetitive or just list of things rather than explaination of a given 
        subject. filterDocs function detects such cases and prevent us adding them into 
        the dataset.
        '''
        lenCond = len(doc.summary) < self.minSummaryLen

        _title = doc.title.lower()        
        stopCond = False
        for phrase in self.stopPhrases:
            if _title.find(phrase) != -1:
                stopCond = True
        
        if lenCond or stopCond:
            return True                         # true means we will filter this doc out
        return False
