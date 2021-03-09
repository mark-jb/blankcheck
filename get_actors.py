#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys

def get_movie_id_from_title(title):
    """ Get a movie id from the title"""
    #print("getting movie id for " + title)
    enc_title = ul.quote_plus(title)
    #print("encoded title as " + enc_title)
    
    url = 'https://api.themoviedb.org/3/search/movie?api_key=' + key + '&language=en-US&query=' + enc_title + '&page=1&include_adult=false'
    response = requests.get(url)
    responsedict = response.json()
#    print(responsedict)
    if len(responsedict['results']) > 0:
        #print('got results')
        print('{:s} ({:s}) has ID: {:d}'.format(responsedict['results'][0]['original_title'],responsedict['results'][0]['release_date'],responsedict['results'][0]['id']))
        return str(responsedict['results'][0]['id'])
    print("\tWARNING: Movie '{:s}' not found".format(title))
    return None

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
print(key)

master_cast_list = {}
master_movie_list = {}
# Read list of movies

with open('episodes.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print('Column names are {:s}'.format(", ".join(row)))
        movie = row["movie"]
        ep_num = row["ep_num"]
        master_movie_list[movie] = ep_num
        #print('\t{:s} is episode {:s}.'.format(movie, ep_num))
        # search IDs of movie
        movie_id = get_movie_id_from_title(movie)
        if movie_id:
            #print("Getting cast for movie ID {:s}".format(movie_id))
            movie_cast = get_cast_from_id(movie_id)
            for actor in movie_cast:
                #print('Adding movie {:s} to actor {:s}'.format(movie, actor))
                if not actor in master_cast_list:
                    master_cast_list[actor] = []
                master_cast_list[actor].append(movie)
        # get_cast_from_title(row["movie"])


        line_count += 1
    print('Processed {:d} movies.'.format(line_count))

all_actors = list(master_cast_list.keys())
all_actors.sort()
#print(all_actors)

actorfile = open("actors.json", "w")
actorjson = json.dumps(master_cast_list)
actorfile.write(actorjson)
actorfile.close()

outfile = open("MetaActorSeries", "w")

printing_threshold = 1
for actor in all_actors:
    if len(master_cast_list[actor]) < printing_threshold:
        continue
    outfile.write("\n==== " + actor + " ====\n")
    for movie in master_cast_list[actor]:
        outfile.write("Episode " + master_movie_list[movie] + ": " + movie + "\n")

outfile.close()
# for each movie, pull cast list
# for each cast member, insert movie title and episode # into a list


# response = requests.get(url)

# print(response.text)


