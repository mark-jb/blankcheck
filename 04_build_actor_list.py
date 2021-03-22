#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys

def clean_cast_response(cast_list):
    """ return a list with only the actor data I want """
    #print('cleaning cast list')
    cast = set()
    for cast_member in cast_list:
#        print(cast_member)
        cast.add(cast_member['name'])
    return cast

def get_cast_from_id(movie_id):
    """ Get the cast of a movie in a dict from the movie id"""
    #print("searching for cast of movie id " + movie_id)
    url = 'https://api.themoviedb.org/3/movie/' + movie_id + '/credits?api_key=' + key
    response = requests.get(url)
    responsedict = response.json()
    cast = clean_cast_response(responsedict['cast'])
    #print(cast)
    #print(responsedict['cast'])
#    if len(responsedict['results']) > 0:
#        print('got results')
#        print(responsedict['results'])
#        return str(responsedict['results'][0])
    return cast

def get_cast_from_title(title):
    """ Get the cast of a movie in a dict from the movie title"""
    movie_id = get_movie_id(title)
    if not movie_id:
      print("No ID found")
      return
    get_cast_from_id(movie_id)


f = open("key", "r")
key = f.readline()
key = key.strip()

in_csv = 'movies.with.ids.csv'
out_meta = 'MetaActorSeries.combined'
out_actors = 'actors.combined.json'

master_cast_list = {}
master_movie_list = {}
# Read list of movies

with open(in_csv, mode='r') as csv_movielist:
    csv_reader = csv.DictReader(csv_movielist)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print('Column names are {:s}'.format(", ".join(row)))
        movie = row["movie"]
        ep_num = row["ep_num"]
        if row["feed"] == "main":
            master_movie_list[movie] = ep_num
        else:
            master_movie_list[movie] = "SF-" + ep_num
        #print('\t{:s} is episode {:s}.'.format(movie, ep_num))
        # search IDs of movie
        movie_id = row["movie_id"]
        print("Getting cast for movie ID {:s}".format(movie_id))
        movie_cast = get_cast_from_id(movie_id)
        for actor in movie_cast:
            print('Adding movie {:s} to actor {:s}'.format(movie, actor))
            if not actor in master_cast_list:
                master_cast_list[actor] = {}
                master_cast_list[actor]["movies"] = []
            master_cast_list[actor]["movies"].append(movie)
        line_count += 1
    print('Processed {:d} movies.'.format(line_count))

all_actors = list(master_cast_list.keys())
all_actors.sort()
#print(all_actors)

actorfile = open(out_actors, "w")
actorjson = json.dumps(master_cast_list)
actorfile.write(actorjson)
actorfile.close()

outfile = open(out_meta, "w")

printing_threshold = 3
for actor in all_actors:
    if len(master_cast_list[actor]["movies"]) < printing_threshold:
        continue
    outfile.write("\n==== " + actor + " ====\n")
    for movie in master_cast_list[actor]["movies"]:
        outfile.write(master_movie_list[movie] + ": " + movie + "\n")

outfile.close()
# for each movie, pull cast list
# for each cast member, insert movie title and episode # into a list


# response = requests.get(url)

# print(response.text)


