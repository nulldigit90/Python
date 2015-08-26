# UrbanDictonary module adapted from
# https://github.com/EvilzoneLabs/BeastBot/blob/sqlite/src/inc/modules/urban.py

import urllib.request
import json

def urban(word):
    word = word.strip()
    try:
        url = 'http://api.urbandictionary.com/v0/define?term=' + word
        info = urllib.request.urlopen(url)
        try:
            data = json.loads(info.read().decode("utf-8"))
            definition = data['list'][0]['definition'].replace("\n", " ").replace("\r", "")
            output = word + ": " + definition
            return output
        except IndexError:
            return "No def, try again"
        except Exception as e:
            print(e)
                
    except Exception as e:
        print(e)
        
def main(nick, comargs, chan, send):
    w = comargs.strip()
    define = urban(w)
    send.put(define)
