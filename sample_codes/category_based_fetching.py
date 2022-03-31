# pip install Wikipedia-API
import wikipediaapi

def print_categorymembers(categorymembers, level=0, max_level=1):
        for c in categorymembers.values():
            print("Depth: {} -- Title: {} -- Namespace (TYPE): {}".format("*" * (level + 1), c.title, c.ns))
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)

print('--> Creating a wikipedia API object in English')
wiki_wiki = wikipediaapi.Wikipedia('en')
print('Object created...')

cat = wiki_wiki.page("Category:Physics")

print("Category members: Category:Physics")
print_categorymembers(cat.categorymembers)