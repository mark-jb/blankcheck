#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys

def get_movie_data_from_title(title):
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
        return responsedict['results'][0]
    print("\tWARNING: Movie '{:s}' not found".format(title))
    return None



f = open("key", "r")
key = f.readline()
key = key.strip()
print(key)

in_csv = 'movies.cleaned.short.csv'
out_csv = 'movies.with.ids.csv'

new_master_list = []
# Read list of movies

with open(in_csv, mode='r') as csv_movielist:
    csv_reader = csv.DictReader(csv_movielist)
    line_count = 0
        
    for row in csv_reader:
        if line_count > 10:
            continue
        out_row = row.copy
        if line_count == 0:
            print('Column names are {:s}'.format(", ".join(row)))
        movie = row["movie"]
        # search IDs of movie
        movie_data = get_movie_data_from_title(movie)
        if movie_data:
            row["movie_id"] = movie_data['id']
            row["release_date"] = movie_data['release_date']
            new_master_list.append(row)

        line_count += 1
    print('Processed {:d} movies.'.format(line_count))

with open(out_csv, 'w') as f:
    writer = csv.writer(f, new_master_list[0].keys())
    writer.writerow(new_master_list[0].keys())
    for e in new_master_list:
        writer.writerow(e.values())
