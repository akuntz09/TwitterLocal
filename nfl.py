#!python2

import json
import unicodedata

in_file = "nflLocal.json"
out_file = "nflLocalFiltered.json"

with open(in_file, "r") as f, open(out_file, "w") as result:

    terms = ("browns", "cleveland", "baltimore", "ravens", "football", "game", "espn", "hartline", "gameday", "MNF", "BALvsCLE", "MondayNightFootball", "Manziel", "flacco", "schaub")

    nfl_count = 0
    nfl_data = []
    coord_count = 0
    for line in f:
        data = json.loads(line)
        if "coordinates" in data or "geo" in data:
            coord_count += 1
            # print(unicodedata.normalize('NFKD', data["text"]).encode('ascii', 'ignore'))

        if any(x in data["text"].lower() for x in terms):
            result.write(line)
            nfl_count += 1
            # print(unicodedata.normalize('NFKD', data["text"]).encode('ascii', 'ignore'))
        else:
            d = data["entities"]
            if isinstance(d, basestring):
                d = json.loads(d)
            
            if d["hashtags"]:
                for hashtag in d["hashtags"]:
                    if any(x in hashtag["text"].lower() for x in terms):
                        result.write(line)
                        nfl_count += 1
                        # print(unicodedata.normalize('NFKD', data["text"]).encode('ascii', 'ignore'))
            elif "user_mentions" in d:
                for user in d["user_mentions"]:
                    if any(x == user["screen_name"] for x in ("brianhartline", "espn", "browns", "ravens", "BalSportsReport")):
                        result.write(line)
                        nfl_count += 1
                        # print(unicodedata.normalize('NFKD', data["text"]).encode('ascii', 'ignore'))

    print("NFL tweet s" + str(nfl_count))
    print("Geo-tagged tweets " + str(coord_count))
