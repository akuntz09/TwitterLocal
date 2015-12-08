#!python2

import json

in_file = "trumpGlobal2.json"
out_file = "trumpGlobal2NoRT.json"

with open(in_file, "r") as f, open(out_file, "w") as result:

    no_retweets = []
    rt_count = 0
    for line in f:
        data = json.loads(line)
        if data.get("retweeted") or not data["text"].startswith("RT @"):
            result.write(line + "\n")
        else:
            rt_count += 1

    print("Retweets count " + str(rt_count))
