#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys

out_dir = 'output'
out_meta = 'MetaActorSeries'
in_actors = 'actors.combined.json'
ignore = 'ignore.list'
split_files = True
print_metadata = False
actorfile = open(in_actors, "r")
actorjson = json.load(actorfile)
actorfile.close()

actors = sorted(actorjson.values(), key=lambda k: k["name"]) 
for actor in actors:
    combo_importance = actor["popularity"] * len(actor["movies"])
    actor["importance"] = combo_importance
#actors = sorted(actors, key=lambda k: k["importance"]) 
#actors = sorted(actors, key=lambda k: k["popularity"]) 
#actors = sorted(actors, key=lambda k: k["popularity"]) 
#print(actors)

ignorefile = open(ignore, "r")


if split_files:
    max_file = 21
    for threshold in range(max_file):
        the_filename = out_dir + "/" + out_meta + "." + str(threshold).zfill(2)
        outfile = open(the_filename, "w")
        print(threshold)
        for actor in actors:
            if len(actor["movies"]) != threshold:
                if threshold != max_file - 1:
                    continue
                elif len(actor["movies"]) < threshold:
                    continue
#            outfile.write("\n==== " + actor["name"] + " ==== " + str(actor["popularity"]) + "\n")
            if print_metadata:
                outfile.write("\n==== " + actor["name"] + " ==== " + str(actor["importance"]) + "\n")
            else:
                outfile.write("\n==== " + actor["name"] + " ====" + "\n")
            for movie in actor["movies"]:
                outfile.write(movie + "\n")
        outfile.close()
else:
    threshold = 0
    the_filename = out_dir + "/" + out_meta + ".combined"
    outfile = open(the_filename, "w")
    for actor in actors:
        if len(actor["movies"]) < threshold:
            continue
#            outfile.write("\n==== " + actor["name"] + " ==== " + str(actor["popularity"]) + "\n")
        outfile.write("\n==== " + actor["name"] + " ==== " + str(actor["importance"]) + "\n")
#            outfile.write("\n==== " + actor["name"] + " ====" + "\n")
        for movie in actor["movies"]:
            outfile.write(movie + "\n")
    outfile.close()


