#!python2

import json
import unicodedata

in_file = "trumpLocal.json"
out_file = "trumpLocalFiltered.json"

with open(in_file, "r") as f, open(out_file, "w") as result:

    trump_count = 0
    trump_data = []
    coord_count = 0
    for line in f:
        data = json.loads(line)
        if "coordinates" in data or "geo" in data:
            coord_count += 1
            # print(unicodedata.normalize('NFKD', data["text"]).encode('ascii', 'ignore'))

        if any(x in data["text"].lower() for x in ["trump", "rally"]):
            result.write(line)
            trump_count += 1
            # print(unicodedata.normalize('NFKD', data["text"]).encode('ascii', 'ignore'))
        else:
            d = data["entities"]
            if isinstance(d, basestring):
                d = json.loads(d)
            
            if d["hashtags"]:
                for hashtag in d["hashtags"]:
                    if any(x in hashtag["text"].lower() for x in ("trump", "gop", "election2016", "wakeupamerica", "makeamericagreatagain")):
                        result.write(line)
                        trump_count += 1
                        # print(unicodedata.normalize('NFKD', data["text"]).encode('ascii', 'ignore'))
            elif "user_mentions" in d:
                for user in d["user_mentions"]:
                    if "realDonaldTrump" == user["screen_name"]:
                        result.write(line)
                        trump_count += 1
                        # print(unicodedata.normalize('NFKD', data["text"]).encode('ascii', 'ignore'))

    print("Trump tweets " + str(trump_count))
    print("Geo-tagged tweets " + str(coord_count))
