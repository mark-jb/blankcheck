#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys
import argparse


def print_out(text):
    if args.screen:
        print(text.strip())
    else:
        outfile.write(text)

out_dir = 'output'
out_meta = 'MetaActorSeries'
in_actors = 'actors.combined.json'
ignore = 'ignore.list'
split_files = True
print_metadata = False

parser = argparse.ArgumentParser()
parser.add_argument('--episode', help='episode number to filter on')
parser.add_argument('--pop', help='sort by popularity', action="store_true")
parser.add_argument('--importance', help='sort by importance', action="store_true")
parser.add_argument('--alpha', help='sort by alphabetical (default)', action="store_true")
parser.add_argument('--nosplit', help='dont split into separate files by number', action="store_true", default=False)
parser.add_argument('--screen', help='output to screen', action="store_true")
args = parser.parse_args()
split_files = not args.nosplit

if args.episode:
    print("Filtering on episode " + args.episode)

actorfile = open(in_actors, "r")
actorjson = json.load(actorfile)
actorfile.close()


actors = sorted(actorjson.values(), key=lambda k: k["name"]) 
for actor in actors:
    combo_importance = actor["popularity"] * len(actor["movies"])
    actor["importance"] = combo_importance
if args.importance:
    print("Sorting by importance")
    actors = sorted(actors, key=lambda k: k["importance"]) 
elif args.pop:
    print("Sorting by popularity")
    actors = sorted(actors, key=lambda k: k["popularity"]) 
#actors = sorted(actors, key=lambda k: k["popularity"]) 
#print(actors)

ignorefile = open(ignore, "r")

if split_files:
    max_file = 21
    for threshold in range(max_file):
        the_filename = out_dir + "/" + out_meta + "." + str(threshold).zfill(2)
        if not args.screen:
            outfile = open(the_filename, "w")
        print(threshold)
        for actor in actors:
            if len(actor["movies"]) != threshold:
                if threshold != max_file - 1:
                    continue
                elif len(actor["movies"]) < threshold:
                    continue
            if args.episode:
                if len(list(filter(lambda ep_filter: ep_filter.keys() == args.episode, actor["movies_dict"]))) == 0:
                    continue
#            outfile.write("\n==== " + actor["name"] + " ==== " + str(actor["popularity"]) + "\n")
            actor_title = "\n==== " + actor["name"] + " ====" + "\n"
            if print_metadata:
                actor_title = "\n==== " + actor["name"] + " ==== " + str(actor["importance"]) + "\n"
            print_out(actor_title)
            for movie in actor["movies"]:
                print_out(movie + "\n")
        if not args.screen:
            outfile.close()
else:
    threshold = 0
    the_filename = out_dir + "/" + out_meta + ".combined"
    outfile = open(the_filename, "w")
    for actor in actors:
        if len(actor["movies"]) < threshold:
            continue
#            outfile.write("\n==== " + actor["name"] + " ==== " + str(actor["popularity"]) + "\n")
        print_out("\n==== " + actor["name"] + " ==== " + str(actor["importance"]) + "\n")
#            outfile.write("\n==== " + actor["name"] + " ====" + "\n")
        for movie in actor["movies"]:
            print_out(movie + "\n")
    outfile.close()


