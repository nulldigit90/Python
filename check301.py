# requires requests lib
# - pip install requests

import requests
import sys

def redirectTest(url):
    with open("no_redirects.txt", "w") as no_redirect:
        try:
            r = requests.head(url, allow_redirects=False)
            if (r.status_code == 301):
                print("+ %s :: %d" % (url, r.status_code))
            else:
                print("- WARNING: %s :: %d" % (url, r.status_code))
                no_redirect.write("%s :: %d\n" % (url, r.status_code))

        except requests.exceptions.RequestException as e:
            print("! Error with request: %s :: %s" % (url, e))


def load_urls(urlfile):
    # clean urls of white space and remove empty lines
    # this does not prepend http/https to urls missing them
    clean_urls = []
    with open(urlfile) as f:
        urllist = f.readlines()
    for i in urllist:
        i = i.strip()
        if i:
            clean_urls.append(i)

    return (clean_urls)

args = sys.argv
if len(args) < 2:
    print("! Error: Missing arguments.\n\nUsage: python check301.py urls.txt")
else:
    try:
        l = load_urls(args[1])
        for i in l:
            redirectTest(i)
    except Exception, e:
        print("Something went wrong: %s" % e)
