import wikipediaapi

def getTopKLinks(doc, k=3):
    links = []
    counter = 0
    for link in doc.links.values():
        if link.ns == wikipediaapi.Namespace.MAIN:
            links.append(link.pageid)
            counter += 1
        if counter >= k:
            break
    return links