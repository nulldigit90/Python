
import urllib2
import re
import sys
import os

def findInPage(page):
  for line in page:
    if '.mp4' in line and 'file=' in line:
      found = re.search('file=".*"',line)
      if found:
        url = found.group()[6:-1]
        name = re.search(r'\w+\.mp4', url).group()
        return (name, url)
      else:
        sys.exit()

def getPage():
  resp = urllib2.urlopen(site)
  page = resp.readlines()
  resp.close()
  return page

def saveVid(file_name, url):
  BUFF_SIZE = 1024*14
  progress = 0
  p = urllib2.urlopen(url)

  with open(file_name, "wb") as f:
    while True:
      buff = p.read(BUFF_SIZE)
      if not buff:
        break
      f.write(buff)
  f.close()


if __name__ == '__main__':
  url = "https://www.youtube.com/v/NgWn7zbgxZ4"
  n = "pickle"
  print "saving..."
  saveVid(n, url)
  print "done"
