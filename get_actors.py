#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys

def get_movie_id_from_title(title):
    """ Get a movie id from the title"""
    print("getting movie id for " + title)
    enc_title = ul.quote_plus(title)
    print("encoded title as " + enc_title)
    
    url = 'https://api.themoviedb.org/3/search/movie?api_key=' + key + '&language=en-US&query=' + enc_title + '&page=1&include_adult=false'
    response = requests.get(url)
    responsedict = response.json()
    if len(responsedict['results']) > 0:
        print('got results')
        print('{:s} has ID: {:d}'.format(responsedict['results'][0]['original_title'],responsedict['results'][0]['id']))
        return str(responsedict['results'][0]['id'])
    return None

def clean_cast_response(cast_list)
    for cast_member in cast_list
        

def get_cast_from_id(movie_id):
    """ Get the cast of a movie in a dict from the movie id"""
    print("searching for cast of movie id " + movie_id)
    url = 'https://api.themoviedb.org/3/movie/' + movie_id + '/credits?api_key=' + key
    response = requests.get(url)
    responsedict = response.json()
    print(responsedict['cast'])
#    if len(responsedict['results']) > 0:
#        print('got results')
#        print(responsedict['results'])
#        return str(responsedict['results'][0])
    return None

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

# Read list of movies

with open('episodes.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print('Column names are {:s}'.format(", ".join(row)))
            line_count += 1
        print('\t{:s} is episode {:s}.'.format(row["movie"],row["ep_num"]))

        # search IDs of movie
        movie_id = get_movie_id_from_title(row["movie"])
        if movie_id:
            print("Getting cast for movie ID {:s}".format(movie_id))
            cast = get_cast_from_id(movie_id)
        # get_cast_from_title(row["movie"])


        line_count += 1
    print('Processed {:d} movies.'.format(line_count))


# for each movie, pull cast list
# for each cast member, insert movie title and episode # into a list

url = 'https://api.themoviedb.org/3/movie/550/credits?api_key=' + key
url = url.strip()
print(url)

# response = requests.get(url)

# print(response.text)


