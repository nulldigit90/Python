import urllib
import urllib.request
from bs4 import BeautifulSoup

def define(word):
    url = "http://dictionary.reference.com/browse/" + word
    try:
        info = urllib.request.urlopen(url)
        soup = BeautifulSoup(info.read(), "lxml")
        defset = soup.find_all("div", class_="def-content")
        if defset:
            out = "Def: %s" % defset[0].contents[0].strip()
            more = "More found %s%s" % (url, word)
            print(out)
            print(more)
    except urllib.error.HTTPError as e:
        print("404 word not found")
        
w = input("Word to define: ")
define(w)
