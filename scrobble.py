import os
import requests
from time import sleep
from pprint import pprint
# import config with variables user, key - rename sample-config.py as config.py with your settings
import config

# set vars
output_filename = "scrobble-output.txt"

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
    # print "http status:", r.status_code
    # pprint(data)

    try:
        latest_track = data['recenttracks']['track'][0]
    except KeyError:
        pass

    # check if latest track is playing now
    playing = latest_track.get('@attr')
    if playing is None:
        scrobble = 'Now Playing: Nothing'
    else:
        artist = latest_track['artist']['#text'].encode('utf-8')
        song = latest_track['name'].encode('utf-8')
        scrobble = "Now Playing: {0} by {1}".format(song, artist)

    if scrobble != previous:
        print "{0}, updating file".format(scrobble)
        with open(os.path.normpath(output_filename), "w") as f:
            f.write(scrobble)
    # else:
        # print "{}, not updating file".format(scrobble)
    return scrobble

previous = "None"
# main loop
running = True
while running:
    previous = get_playing(previous)
    # update every 10 seconds
    sleep(10)
