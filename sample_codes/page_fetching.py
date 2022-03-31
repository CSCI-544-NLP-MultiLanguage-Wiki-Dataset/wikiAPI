# pip install Wikipedia-API
import wikipediaapi

print('--> Creating a wikipedia API object in English')
wiki_wiki = wikipediaapi.Wikipedia('en')
print('Object created...')


print('--> Getting a sample page')
page_py = wiki_wiki.page('Python_(programming_language)')
print('Page is fetched...')
print('Page exists {}'.format(page_py.exists()))

## Variables of the webpage
print('Page type: {}'.format(type(page_py)))

# Categories
print('Number of categories: {}'.format(len(page_py.categories)))
print('Top 5 categories: ')
count = 0 
for k,v in page_py.categories.items():
    print('-- {}'.format(k))
    count += 1
    if count == 5:
        break

# Title
print('Title: {}'.format(page_py.title))

# Whole text
print('Whole text len: {}'.format(len(page_py.text)))

# Summary
print('Page summary len: {}'.format(len(page_py.summary)))
print('Page summary: {}'.format(page_py.summary))

# Links
print('Number of links: {}'.format(len(page_py.links)))
print('Top 5 links: ')
count = 0
linked_pages = []
for k,v in page_py.links.items():
    print('-- title: {}, page: {}'.format(k, v))
    linked_pages.append(v)
    count += 1
    if count == 5:
        break

# check the linked pages information
for a_page in linked_pages:
    print('## Language: {} \n ## Title: {} \n ## Summary: {} \n\n\n'.format(a_page.language, a_page.title, a_page.summary))
