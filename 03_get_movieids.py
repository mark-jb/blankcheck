#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys



replacements = { "main": {
        "23b": "9738",   # Fantastic Four 2004
        "23d": "166424", # Fantastic Four 2015
        "37": "140607",  # The Force Awakens
        "52": "9303",   # Bound
        "72": "222936", # Aloha
        "69": "297761", # Suicide Squad
        "102": "74",    # War of the Worlds
        "107": "72976", # Lincoln
        "110": "2778",  # Clifford
        "111": "297762", # Wonder Woman
        "130": "1089",   # Point Break
        "137": "141052", # Justice League
        "142": "12775",  # Flesh + Blood
        "143": "5548",  # Robert Cop
        "144": "861",   # Total Recall
        "151": "15698", # Running Scared
        "174a": "76492", # Hotel Transylvania
        "177": "73344", # Crouching Tiger Hidden Dragon
        "198": "268",   # Batman
        "206": "869",   # Planet of the Apes
        "210": "12155", # Alice in Wonderland
        "214": "329996", # Dumbo
        "217": "11524",  # Thief
        "219": "11454",  # Manhunter
        "223": "8489",   # Ali
        "224": "1538",   # Collateral
        "226a": "420818", # Lion King
        "226b": "536869", # Cats
        "227": "11322", # Public Enemies
        "237": "129",   # Spirited Away
        "249": "11300", # Something Wild
        "254": "39437", # Beloved
        "258": "14462", # Manchurian Candidate
        "264": "9659", # Mad Max
        "279": "2928", # Michael
        "303": "87502", # Flight
        "312": "812",   # Aladdin
        "318": "40687", # Heartbreak Kid
        "325": "25624", # Rosewood
        "326a": "482",   # Shaft
        "326b": "479",   # Shaft (2000)
        "326c": "486131", # Shaft (2019)
        "330": "59965", # Abduction
        "332": "2778",  # Clifford
        "336": "17814", # Assault on Precinct 13
        "337": "948",  # Halloween
        "338": "790",  # The Fog
        "340": "1091", # The Thing
        "345": "8337"  # They Live
    },
    "patreon": {
        "8": "10195",   # Thor
        "22": "118340", # Guardians Vol 1
        "44": "348350", # Solo
        "55": "140607", # The Force Awakens
        "61": "9598",   # Babe
        "67": "954",    # Mission Impossible 1
        "76": "348",    # Alien
        "115": "40047", # Elvis
        "113": "564",    # The Mummy
        "118": "9334",   # The Scorpion King
        "117": "282035"  # The Mummy 2017
    }
}


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
        #print('{:s} ({:s}) has ID: {:d}'.format(responsedict['results'][0]['original_title'],responsedict['results'][0]['release_date'],responsedict['results'][0]['id']))
        return responsedict['results'][0]
    return None


def get_movie_data_from_id(movie_id):
    """ Get a movie details from id"""
    url = 'https://api.themoviedb.org/3/movie/' + movie_id + '?api_key=' + key
    response = requests.get(url)
    responsedict = response.json()
    return responsedict


f = open("key", "r")
key = f.readline()
key = key.strip()

in_csv = 'movies.cleaned.csv'
out_csv = 'movies.with.ids.csv'

new_master_list = []
failures = []
# Read list of movies

with open(in_csv, mode='r') as csv_movielist:
    csv_reader = csv.DictReader(csv_movielist)
    line_count = 0
        
    for row in csv_reader:
        out_row = row.copy
        if line_count == 0:
            print('Column names are {:s}'.format(", ".join(row)))
        movie = row["movie"]

        # search IDs of movie
        if row["ep_num"] in replacements[row["feed"]]:
            print("   OVERRIDE:")
            movie_data = get_movie_data_from_id(replacements[row["feed"]][row["ep_num"]])
        else:
            movie_data = get_movie_data_from_title(movie)
        if movie_data:
            row["movie_id"] = movie_data['id']
            row["release_date"] = movie_data['release_date']
            row["movie_original_title"] = movie_data['original_title']
            print('{:s} ({:s}) has ID: {:d}'.format(movie_data['original_title'],movie_data['release_date'],movie_data['id']))
            if (movie != movie_data['original_title']):
                print("\tWARNING: '{:s}' does not match ({:s} {:s})".format(movie,row["feed"],row["ep_num"]))
            new_master_list.append(row)
        else:
            print("\tWARNING: Movie '{:s}' not found".format(movie))
            failures.append(movie)

        line_count += 1
    print('Processed {:d} movies.'.format(line_count))

with open(out_csv, 'w') as f:
    writer = csv.writer(f, new_master_list[0].keys())
    writer.writerow(new_master_list[0].keys())
    for e in new_master_list:
        writer.writerow(e.values())

print("\nFailures:")
for fail in failures:
    print(fail)
