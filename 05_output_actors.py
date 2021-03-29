#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys

out_dir = 'output'
out_meta = 'MetaActorSeries'
in_actors = 'actors.combined.json'

actorfile = open(in_actors, "r")
actorjson = json.load(actorfile)
actorfile.close()

actors = sorted(actorjson.values(), key=lambda k: k["name"]) 
actors = sorted(actors, key=lambda k: k["popularity"]) 
#print(actors)

max_file = 21
for threshold in range(max_file):
    the_filename = out_dir + "/" + out_meta + "." + str(threshold)
    outfile = open(the_filename, "w")
    print(threshold)
    for actor in actors:
        if len(actor["movies"]) != threshold:
            if threshold != max_file - 1:
                continue
            elif len(actor["movies"]) < threshold:
                continue
        outfile.write("\n==== " + actor["name"] + " ==== " + str(actor["popularity"]) + "\n")
        for movie in actor["movies"]:
            outfile.write(movie + "\n")
    outfile.close()


