import os
import requests
from time import sleep
from pprint import pprint
# import config with variables user, key
import config

def get_playing(previous):
    global latest_track
    base_url = "http://ws.audioscrobbler.com/2.0/"
    method = "user.getrecenttracks"
    user = config.user
    key = config.key
    data_format = "json"
    payload = {"method": method,
               "user": user,
               "api_key": key,
               "format": data_format}
    r = requests.get(base_url, payload)
    data = r.json()
    try:
        latest_track = data['recenttracks']['track'][0]
    except KeyError:
        track = "Nothing Playing"
        print "updating file {0}".format(track)
        with open(os.path.normpath("scrobble-output.txt"), "w") as f:
            f.write(track)

    try:
        if latest_track['@attr']['nowplaying'] == 'true':
            artist = latest_track['artist']['#text'].encode('utf-8')
            song = latest_track['name'].encode('utf-8')
            scrobble = "Now Playing: {0} by {1}".format(song, artist)
            if scrobble != previous:
                print "updating file {0}".format(scrobble)
                with open(os.path.normpath("scrobble-output.txt"), "w") as f:
                    f.write(scrobble)
            return scrobble
    except KeyError:
        pass

previous = "None"
running = True
while running:
    previous = get_playing(previous)
    sleep(5)
