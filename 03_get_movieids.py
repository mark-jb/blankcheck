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
        "54": "603",    # The Matrix
        "72": "222936", # Aloha
        "77": "679",    # Aliens
        "69": "297761", # Suicide Squad
        "102": "74",    # War of the Worlds
        "107": "72976", # Lincoln
        "110": "2778",  # Clifford
        "111": "297762", # Wonder Woman
        "116": "320",    # Insomnia
        "130": "1089",   # Point Break
        "137": "141052", # Justice League
        "142": "12775",  # Flesh + Blood
        "143": "5548",  # Robert Cop
        "144": "861",   # Total Recall
        "151": "15698", # Running Scared
        "174a": "76492", # Hotel Transylvania
        "177": "146",   # Crouching Tiger Hidden Dragon
        "185": "2300",  # Space Jam
        "198": "268",   # Batman
        "206": "869",   # Planet of the Apes
        "210": "12155", # Alice in Wonderland
        "214": "329996", # Dumbo
        "217": "11524",  # Thief
        "219": "11454",  # Manhunter
        "221": "949",   # Heat
        "223": "8489",   # Ali
        "224": "1538",   # Collateral
        "226a": "420818", # Lion King
        "226b": "536869", # Cats
        "227": "11322",  # Public Enemies
        "232": "10515",  # Castle in the Sky
        "233": "8392",  # My Neighbour Totoro
        "237": "129",   # Spirited Away
        "249": "11300", # Something Wild
        "254": "39437", # Beloved
        "258": "14462", # Manchurian Candidate
        "264": "9659", # Mad Max
        "279": "2928", # Michael
        "303": "87502", # Flight
        "312": "812",   # Aladdin
        "313": "11970",   # Aladdin
        "319": "40687", # Heartbreak Kid
        "326": "25624", # Rosewood
        "327a": "482",   # Shaft
        "327b": "479",   # Shaft (2000)
        "327c": "486131", # Shaft (2019)
        "331": "59965", # Abduction
        "333": "2778",  # Clifford
        "337": "17814", # Assault on Precinct 13
        "338": "948",  # Halloween
        "339": "790",  # The Fog
        "341": "1091", # The Thing
        "346": "8337",  # They Live
        "355": "511809",  # West Side Story
        "357": "123067" # Two Friends
    },
    "patreon": {
        "2": "1726",    # Iron Man
        "8": "10195",   # Thor
        "22": "118340", # Guardians Vol 1
        "44": "348350", # Solo
        "48": "11",     # Star Wars
        "55": "140607", # The Force Awakens
        "61": "9598",   # Babe
        "67": "954",    # Mission Impossible 1
        "76": "348",    # Alien
        "78": "679",    # Aliens
        "115": "564",   # The Mummy
        "117": "40047", # Elvis
        "120a": "9334",  # The Scorpion King
        "120b": "31578",  # The Scorpion King
        "119": "282035", # The Mummy 2017
        "125": "620",    # Ghostbusters
        "127": "2978",   # Ghostbusters 2
        "128": "43074",  # Ghostbusters 2016
        "130": "425909", # Ghostbusters Afterlife
        "131": "603",    # The Matrix
#        "130": "350050" # They
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
            movie_data = get_movie_data_from_id(replacements[row["feed"]][row["ep_num"]])
            print("   OVERRIDE:")
        else:
            movie_data = get_movie_data_from_title(movie)
        if movie_data:
            row["movie_id"] = movie_data['id']
            row["movie_original_title"] = movie_data['original_title']
            if 'release_date' in movie_data:
                row["release_date"] = movie_data['release_date']
            else:
                row["release_date"] = "9999-09-09"
            print('{:s} [{:s}] ({:s}) has ID: {:d}'.format(row['movie_original_title'],movie,row['release_date'],row['movie_id']))
            if (movie != movie_data['original_title']):
                print("\tWARNING: '{:s}' does not match ({:s} {:s})".format(movie,row["feed"],row["ep_num"]))
            new_master_list.append(row)
        else:
            print("\tWARNING: Movie '{:s}' not found".format(movie))
            failures.append(movie)

        line_count += 1
    print('Processed {:d} movies.'.format(line_count))

columns = ["date","feed","ep_num","title","movie","guest","movie_id","movie_original_title","release_date"]

with open(out_csv, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    for e in new_master_list:
        writer.writerow(e)

print("\nFailures:")
for fail in failures:
    print(fail)
