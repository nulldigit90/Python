'''Search movie titles and get ratings, release year, simple plot.
intended for an irc bot, but can be used where ever.
Author: techb
Date: July 18 2015

If you use this, give me credit for my part, else use at your own free will.'''

import json
import urllib

def getMovieInfo(title):
    titlesplit = title.lower().strip().split() #oh may lol
    # if the movie title is more than one word,
    # join it so the url can use it, else just nothing
    if len(titlesplit) > 1:
        newtitle = "+".join(titlesplit)
    else:
        newtitle = titlesplit[0]
        
    url = "http://www.omdbapi.com/?t=%s&plot=short&r=json" % newtitle
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    if data['Response'] == 'True':
        return (data['Title'],
                data['Year'],
                data['imdbRating'],
                data['Plot'])
    else:
        return (False, "Movie: %s not found, check spelling?" % title)
    
# Example usage
movie_title = raw_input("Movie to search: ")
data = getMovieInfo(movie_title)
if data[0] != False:
    for info in data:
        print info
else:
    print data[1]
        
