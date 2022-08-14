#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys
import argparse
import time
import re

def print_out(text):
    if args.tofile:
        outfile.write(text + '\n')
    else:
        print(text)

def print_actor(actor):
    actor_title = "\n==== " + actor["name"] + " ===="
    if print_metadata:
        if args.pop:
            actor_title = actor_title + " " + str(actor["popularity"])
        else:
            actor_title = actor_title + " " + str(actor["importance"])
    print_out(actor_title)
    for movie in actor["movies_dict"]:
        for key in movie:
            print_out(key + ': ' + movie[key])

def actor_in_episode(actor, ep_num):
    if len(list(filter(lambda ep_filter: ep_num in ep_filter.keys(), actor["movies_dict"]))) == 0:
        return False
    return True

def actor_in_movie(actor, movie_name):
    if len(list(filter(lambda movie_filter: movie_name in ':'.join(list(movie_filter.values())).lower(), actor["movies_dict"]))) == 0:
        return False
    return True

def actor_in_actorlist(actor, actlist):
    if actor["name"].lower() in actlist:
        return True
    return False

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
parser.add_argument('--min', help='only output actors with X movies or more')
parser.add_argument('--max', help='only output actors with X movies or less')
parser.add_argument('--pop', help='sort by popularity', action="store_true")
parser.add_argument('--main', help='only Main feed', action="store_true")
parser.add_argument('--patreon', help='only Patreon feed', action="store_true")
parser.add_argument('--importance', help='sort by importance', action="store_true")
parser.add_argument('--alpha', help='sort by alphabetical (default)', action="store_true")
parser.add_argument('--ignore', help='ignore actors in ignorelist', action="store_true")
parser.add_argument('--split', help='split into separate files by number', action="store_true", default=False)
parser.add_argument('--tofile', help='output to file', action="store_true")
parser.add_argument('--metadata', help='print metadata', action="store_true")
parser.add_argument('--year', help='print movie years', action="store_true")
args = parser.parse_args()
split_files = args.split

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
if args.min:
    threshold_min = int(args.min)
else:
    if args.tofile:
        threshold_min = 0
    else:
        threshold_min = 2
if args.max:
    threshold_max = int(args.max)
else:
    threshold_max = 10000
print("Minimum movies: " + str(threshold_min))
actorfile = open(in_actors, "r")
actorjson = json.load(actorfile)
actorfile.close()

# SORT
actors = sorted(actorjson.values(), key=lambda k: k["name"]) 
for actor in actors:
    combo_importance = round(actor["popularity"] * len(actor["movies_dict"]), 2)
    actor["importance"] = combo_importance
if args.importance:
    print("Sorting by importance")
    actors = sorted(actors, key=lambda k: k["importance"]) 
elif args.pop:
    print("Sorting by popularity")
    actors = sorted(actors, key=lambda k: k["popularity"]) 
#actors = sorted(actors, key=lambda k: k["popularity"]) 
#print(actors)


# FILTER
if args.actor:
    actors = list(filter(lambda actor_filter: args.actor in actor_filter["name"].lower(), actors))
if args.episode:
    actors = list(filter(lambda actor_filter: actor_in_episode(actor_filter, args.episode), actors))
if args.movie:
    actors = list(filter(lambda actor_filter: actor_in_movie(actor_filter, args.movie), actors))
if args.ignore:
    ignorefile = open(ignore, "r")
    ignore_actor_list = []
    for line in ignorefile:
        clean_actor = re.sub(r'^\d+,', '', line).strip().lower()
        if not clean_actor:
            continue
    #    print(clean_actor)
        if clean_actor == '=====':
            break
        ignore_actor_list.append(clean_actor)
    print(ignore_actor_list)
    actors = list(filter(lambda actor_filter: actor_filter["name"].lower() not in ignore_actor_list, actors))


if split_files:
    max_file = 21
    for c_threshold in range(threshold_min, min(max_file,threshold_max+1)):
        the_filename = out_dir + "/" + out_meta + "." + str(c_threshold).zfill(2)
        if args.tofile:
            outfile = open(the_filename, "w")
#        print(threshold)
        for actor in actors:
            if len(actor["movies_dict"]) != c_threshold:
                if c_threshold != max_file - 1:
                    continue
                elif len(actor["movies_dict"]) < c_threshold:
                    continue
            print_actor(actor)
        if args.tofile:
            outfile.close()
else:
    the_filename = out_dir + "/" + out_meta + ".combined"
    if args.pop:
        the_filename = the_filename + ".popularity"
    elif args.importance:
        the_filename = the_filename + ".importance"
    else:
        the_filename = the_filename + ".alphabetical"
    if args.tofile:
        outfile = open(the_filename, "w")
    for actor in actors:
        if (len(actor["movies_dict"]) < threshold_min) or (len(actor["movies_dict"]) > threshold_max):
            continue
        print_actor(actor)
    if args.tofile:
        outfile.close()


