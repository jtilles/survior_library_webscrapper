# Survivor Library Web Scrapper

This is a an example app for me to practice web scrapping.  I will first webscrape all the URLs from [The Survivor Library](http://www.survivorlibrary.com/) and then proceed to download them in a logical folder structure, matching that of the site.

# Use
1. Download the repo and make sure python is installed (python 3.8 was tested)
2. Install the requirements using the following command:
```
python pip install -r requirements.txt
```
3. Run the app using the command:
```
python ./app.py
```
4. Creates a subfolder for each subcategory and then puts the pdf in the subfolder.

## FOLDER STRUCTURE
* survivors_library
    * Accounting
        * 20th Century Bookkeeping and Accounting 1922.pdf
        * Accounting Methods of Banks 1920.pdf
    * Aeroplanes
        * Book A
        * Book B
    * Airships
        * Book A
        * Book B

## Updating resources
The script will only scrape the website for links to new content if there is not an existing ```survivor.yaml```.  To force an update use the command line flag *--update* when calling the program.  Example:
```
python ./app.py --update
```
