import requests, bs4
import yaml, os, sys
import argparse

# webpage = "http://www.survivorlibrary.com/library-download"
# yamlFile = "survivor.yaml"


def getLinks(webpage):
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

        except (TypeError, AttributeError) as er:
            pass

    # Go through each subcategory link and download it's page to find all the links to the books.
    for i, category in enumerate(categories):
        # if i>2:
        #     print("Reached max number of searches")
        #     break
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
                link =  "http://www.survivorlibrary.com" + link.a['href']
                print("\t%s:\t%s" %(title, link))
                categories[category]["books"].append({"title": title, "link": link})
            except (TypeError, AttributeError, ValueError) as er:
                pass


    return categories

#  Writes all the categories and links to a YAML file so websites don't have to be scrapped everytime
def writeYamlFile(data, yamlFile):
    with open(yamlFile, 'w') as writeFile:
        writeFile.write(yaml.dump(data, default_flow_style=False))

# Gets all information out of yaml file and download all book links
def downloadFiles(yamlFile):
    print("importing data from yaml file: %s" %(yamlFile))

    numBooks = getBookCount(yamlFile)
    print("Going to try and fetch %d books from %s" %(numBooks, webpage))
    
    count = 0
    with open(yamlFile) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    rootDirectory = "./survivors_library/"
    if not os.path.exists(rootDirectory):
        os.mkdir(rootDirectory)

    for category in data:
        directoryPath = rootDirectory + category.replace(" ", "_").rstrip()
        if not os.path.exists(directoryPath):
            print("Making Directory: %s" %(directoryPath))
            os.mkdir(directoryPath)
        for i, book in enumerate(data[category]["books"]):
            # Create filename of pdf to download
            filename = directoryPath + "/" + data[category]["books"][i]["title"].replace('"', "") + ".pdf"
            count += 1
            # Check if the book is already downloaded, if it is, skip it
            if os.path.exists(filename):
                print("Skipping Book %d/%d: %s, already downloaded" %(count, numBooks, data[category]["books"][i]["title"]))
                continue
            
            print("Downloading Book %d of %d:\t%s | %s\t(%d of %d)" %(i+1, len(data[category]["books"]), category, book["title"], count, numBooks))
            try:
                link = data[category]["books"][i]["link"]
                r = requests.get(link, allow_redirects=True)
            
                # Download and write to file 1KB at a time
                with open(filename, 'wb') as newFile:
                    for chunk in r.iter_content(1000):
                        newFile.write(chunk)
            except OSError:
                print("ERROR - invalid filename: %s" %filename)

def getBookCount(yamlFile):
    with open(yamlFile) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    count = 0
    for category in data:
        count += len(data[category]["books"])
    return count


if __name__ == "__main__":
    webpage = "http://www.survivorlibrary.com/library-download"
    yamlFile = "survivor.yaml"
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", help="downloads new links and enters into survivor.yaml", action="store_true")
    args = parser.parse_args()
    update_files = False
    
    # If download flag is present or yamlFile doesn't exist, download new index
    if (args.update) or (not os.path.exists(yamlFile)):
        print("Downloading New Index and saving to %s" %yamlFile)
        data = getLinks(webpage)
        writeYamlFile(data, yamlFile)    

    downloadFiles(yamlFile)