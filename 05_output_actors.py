#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys

out_meta = 'MetaActorSeries.combined'
in_actors = 'actors.combined.json'

actorfile = open(in_actors, "r")
actorjson = json.load(actorfile)
actorfile.close()

#actors = sorted(actorjson.values(), key=lambda k: k["name"]) 
actors = sorted(actorjson.values(), key=lambda k: k["popularity"]) 
#print(actors)


outfile = open(out_meta, "w")

printing_threshold = 3
for actor in actors:
    if len(actor["movies"]) < printing_threshold:
        continue
    outfile.write("\n==== " + actor["name"] + " == " + str(actor["popularity"]) + "====\n")
    for movie in actor["movies"]:
        outfile.write(movie + "\n")

outfile.close()
# for each movie, pull cast list
# for each cast member, insert movie title and episode # into a list


# response = requests.get(url)

# print(response.text)


