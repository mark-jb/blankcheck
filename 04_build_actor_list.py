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
        print(cast_member)
        cast.add(cast_member['name'])
    return cast



def get_cast_from_id(movie_id):
    """ Get the cast of a movie in a dict from the movie id"""
    #print("searching for cast of movie id " + movie_id)
    url = 'https://api.themoviedb.org/3/movie/' + movie_id + '/credits?api_key=' + key
    response = session.get(url)
    responsedict = response.json()
    #cast = clean_cast_response(responsedict['cast'])
    cast = responsedict['cast']
    return cast

def get_cast_from_title(title):
    """ Get the cast of a movie in a dict from the movie title"""
    movie_id = get_movie_id(title)
    if not movie_id:
      print("No ID found")
      return
    get_cast_from_id(movie_id)

def get_actor_id(actor):
    """ Get actor id from name """
    if actor in actor_name_to_id:
        return actor_name_to_id[actor]
    if not len(actor_name_to_id) == len(master_cast_list):
        # print("refresh actor name to id map")
        for actor_id, actor_info in master_cast_list.items():
            actor_name_to_id[actor_info["name"]] = actor_id
        if actor in actor_name_to_id:
            # print("Actor found after refresh")
            return actor_name_to_id[actor]
    # print("Manual actor not found, adding...")
    actor_new = {}
    actor_new["original_name"] = actor
    actor_new["movies_dict"] = []
    actor_new["movies_ep_id"] = []
    actor_new["name"] = actor
    actor_new["info"] = {}
    actor_new["popularity"] = 1
    master_cast_list[actor] = actor_new


    return actor

def create_actor(actor_id, actor):
    name = actor["name"]
    master_cast_list[actor_id] = {}
    master_cast_list[actor_id]["name"] = name
    master_cast_list[actor_id]["info"] = actor
    master_cast_list[actor_id]["popularity"] = actor["popularity"]
    # If the *name* is in the list, it's manual and should be converted
    if name in master_cast_list:
        # print("Convert {:s} to actor_id".format(name))
        master_cast_list[actor_id]["movies_dict"] = master_cast_list[name]["movies_dict"]
        master_cast_list[actor_id]["movies_ep_id"] = master_cast_list[name]["movies_ep_id"]
        actor_name_to_id[name] = actor_id
        del master_cast_list[name]
    else: # no conversion, just create
        # print("Create new actor {:s}".format(name))
        master_cast_list[actor_id]["movies_dict"] = []
        master_cast_list[actor_id]["movies_ep_id"] = []

f = open("key", "r")
key = f.readline()
key = key.strip()

session = requests.Session()

in_csv = 'movies.with.ids.csv'
in_castlist_csv = 'manual.castlist.csv'
out_meta = 'MetaActorSeries.combined'
out_actors = 'actors.combined.json'
out_movies = 'movies.json'

master_cast_list = {}
manually_added_cast_list = []
actor_name_to_id = {}
master_movie_list = {}
manual_castlist = {}
# Read list of movies

# Process the manual castlist
with open(in_castlist_csv, mode='r') as csv_castlist:
    csv_reader = csv.DictReader(csv_castlist)
    for row in csv_reader:
        movie_id = row["movie_id"]
        if not movie_id in manual_castlist:
            manual_castlist[movie_id] = []
        manual_castlist[movie_id].append(row["name"])
       
# print(manual_castlist)


with open(in_csv, mode='r') as csv_movielist:
    csv_reader = csv.DictReader(csv_movielist)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print('Column names are {:s}'.format(", ".join(row)))
        movie = row["movie"]
        ep_num = row["ep_num"]
        movie_dict = {}
        if row["feed"] == "main":
            ep_id = ep_num
        else:
            ep_id = "SF-" + ep_num
        movie_with_ep = ep_id + ": " + movie
        movie_dict[ep_id] = movie
        master_movie_list[ep_id] = row
        #print('\t{:s} is episode {:s}.'.format(movie, ep_num))
        # search IDs of movie
        movie_id = row["movie_id"]
        print("Getting cast for {:s} ID {:s}".format(movie, movie_id))
        if int(movie_id) < 10000000: # don't bother if TV
            movie_cast = get_cast_from_id(movie_id)
            for actor in movie_cast:
                print('Adding movie {:s} to actor {:s}'.format(movie, actor["name"]))
                actor_id = actor["id"]
                if not actor["id"] in master_cast_list:
                    create_actor(actor_id, actor)
                master_cast_list[actor_id]["movies_dict"].append(movie_dict)
                master_cast_list[actor_id]["movies_ep_id"].append(ep_id)
        # Manual cast list check
        if movie_id in manual_castlist.keys():
            print("Add override cast")
            for actor_name in manual_castlist[movie_id]:
                actor_id = get_actor_id(actor_name)
                # print("{} - {:s}".format(actor_id,actor_name))
                if not actor_id == 0:
                    # print("Actor ID: {} type: {}".format(actor_id, type(actor_id)))
                    master_cast_list[actor_id]["movies_dict"].append(movie_dict)
                    master_cast_list[actor_id]["movies_ep_id"].append(ep_id)

        line_count += 1
    print('Processed {:d} movies.'.format(line_count))

all_actors = list(master_cast_list.keys())
#all_actors.sort()
#print(all_actors)

actorfile = open(out_actors, "w")
actorjson = json.dumps(master_cast_list)
actorfile.write(actorjson)
actorfile.close()

moviefile = open(out_movies, "w")
moviejson = json.dumps(master_movie_list)
moviefile.write(moviejson)
moviefile.close()

