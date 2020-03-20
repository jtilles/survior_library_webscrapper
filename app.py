import requests, bs4
import yaml

webpage = "http://www.survivorlibrary.com/library-download"
yamlFile = "survivor.yaml"



res = requests.get(webpage)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'lxml')

headers = soup.find_all('td')
categories = {}

# Get links for the pages of each subcategory
for header in headers:
    if header is None:
        continue
    try:
        category = header.a.text
        if category == "New Additions":
            continue
        categories[category] = {}
        categories[category]["link"] = webpage + header.a['href']
        categories[category]["books"] = []
        # "link"="test", "subject"="another test"}
# webpage + header.a['href'])
        # links.append(webpage + header.a['href'])
    except (TypeError, AttributeError) as er:
        # print("Type Error: %s" %er)
        pass

# Go through each subcategory link and download it's page to find all the links to the books.
for i, category in enumerate(categories):
    if i>2:
        print("Reached max number of searches")
        break
    print("Looking for %s: %s" %(category, categories[category]["link"]))
    res = requests.get(categories[category]["link"])
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    books = soup.find_all('tr')
    for book in books:
        if book is None:
            continue
        try:
            title, link = book.find_all('td')
            title = title.text
            link = webpage + categories[category]["link"] + link.a['href']
            print("\t%s:\t%s" %(title, link))
            # title = book.td.text
            # link = book.td.a['href']
            # print("Found %s:\t%s" %(title, link))
            categories[category]["books"].append({"title": title, "link": link})
        except (TypeError, AttributeError) as er:
            # print("Type Error: %s" %er) 
            pass




with open(yamlFile, 'w') as writeFile:
    yaml.dump(categories, writeFile)


