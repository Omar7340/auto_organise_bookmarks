#!/user/bin/env python3 -tt
"""
Module documentation.
"""

# Imports
import sys
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests as req
import progressbar
#import os

# Global variables

# Class declarations

# Function declarations

def parse(filename):
    bookmarks = []
    with open(filename, "r") as f:
        content = bs(f, "lxml")

        for item in content.find_all("a"):
            bookmarks.append({"label": item.text, "url": item['href']})
    
    return bookmarks

def save_data(dataframe):
    dataframe.to_csv("bookmarks.csv", escapechar="\\")

def clean_html(html):
    html = bs(html, "html.parser")
    if html.script != None:
        html.script.clear()
    return html.text

def extend_bookmarks_with_content(bookmarks):
    result = []
    with progressbar.ProgressBar(max_value=len(bookmarks)) as bar:
        i = 0
        for item in bookmarks:
            content = "None"
            try:
                if not( "http://" in item["url"] or "https://" in item["url"]):
                    if "file://" in item["url"]:
                        content = "local file"
                    else:
                        content = "not a valid url"
                else:
                    content = req.get(item["url"], timeout=5).text
                    content = clean_html(content)
            except req.exceptions.ConnectionError:
                print(f"Connection Error on " + str(item["url"]))
                content = "Connection Error"
            except req.exceptions.TooManyRedirects:
                print(f"TooManyRedirects Error on " + str(item["url"]))
                content = "Too Many Redirects Error"
            except req.exceptions.Timeout:
                print(f"Timeout Error on " + str(item["url"]))
                content = "Timeout Error"

            item["content"] = content
            result.append(item)
            i+=1
            bar.update(i)
    
    return result


def main():
    bookmarks = parse("entry_exports/favoris_09_03_2023.html")
    bookmarks = extend_bookmarks_with_content(bookmarks)
    df = pd.DataFrame.from_dict(bookmarks)
    save_data(df)
    
# Main body
if __name__ == '__main__':
    main()