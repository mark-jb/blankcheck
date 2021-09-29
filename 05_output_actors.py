#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys
import argparse


def print_out(text):
    if args.screen:
        print(text)
    else:
        outfile.write(text + '\n')

out_dir = 'output'
out_meta = 'MetaActorSeries'
in_actors = 'actors.combined.json'
ignore = 'ignore.list'
split_files = True
print_metadata = False

parser = argparse.ArgumentParser()
parser.add_argument('--episode', help='episode number to filter on')
parser.add_argument('--actor', help='actor to filter on')
parser.add_argument('--movie', help='movie to filter on')
parser.add_argument('--threshold', help='only output actors with X movies or more')
parser.add_argument('--pop', help='sort by popularity', action="store_true")
parser.add_argument('--importance', help='sort by importance', action="store_true")
parser.add_argument('--alpha', help='sort by alphabetical (default)', action="store_true")
parser.add_argument('--nosplit', help='dont split into separate files by number', action="store_true", default=False)
parser.add_argument('--screen', help='output to screen', action="store_true")
parser.add_argument('--metadata', help='print metadata', action="store_true")
args = parser.parse_args()
split_files = not args.nosplit

if args.episode:
    print("Filtering on episode " + args.episode)
    args.screen = True
if args.actor:
    args.actor = args.actor.lower()
    print("Filtering on actor " + args.actor)
    args.screen = True
if args.movie:
    args.movie = args.movie.lower()
    print("Filtering on movie " + args.movie)
    args.screen = True
if args.metadata:
    print_metadata = args.metadata
if args.threshold:
    threshold = int(args.threshold)
else:
    threshold = 0
    if args.screen:
        threshold = 2
print("Minimum movies: " + str(threshold))
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
    for c_threshold in range(threshold, max_file):
        the_filename = out_dir + "/" + out_meta + "." + str(c_threshold).zfill(2)
        if not args.screen:
            outfile = open(the_filename, "w")
#        print(threshold)
        for actor in actors:
            if args.actor:
                if args.actor not in actor["name"].lower():
#                    print(actor)
                    continue
            if len(actor["movies"]) != c_threshold:
                if c_threshold != max_file - 1:
                    continue
                elif len(actor["movies"]) < c_threshold:
                    continue
            if args.episode:
                if len(list(filter(lambda ep_filter: args.episode in ep_filter.keys(), actor["movies_dict"]))) == 0:
                    continue
            if args.movie:
                if len(list(filter(lambda movie_filter: args.movie in ':'.join(list(movie_filter.values())).lower(), actor["movies_dict"]))) == 0:
                    continue
            actor_title = "\n==== " + actor["name"] + " ===="
            if print_metadata:
                actor_title = "\n==== " + actor["name"] + " ==== " + str(actor["importance"])
            print_out(actor_title)
            for movie in actor["movies"]:
                print_out(movie)
        if not args.screen:
            outfile.close()
else:
    the_filename = out_dir + "/" + out_meta + ".combined"
    outfile = open(the_filename, "w")
    for actor in actors:
        if len(actor["movies"]) < threshold:
            continue
#            outfile.write("\n==== " + actor["name"] + " ==== " + str(actor["popularity"]) + "\n")
        print_out("\n==== " + actor["name"] + " ==== " + str(actor["importance"]))
#            outfile.write("\n==== " + actor["name"] + " ====" + "\n")
        for movie in actor["movies"]:
            print_out(movie)
    outfile.close()


