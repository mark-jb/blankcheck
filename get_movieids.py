#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys



replacements = { "main": {
        "52": "9303",
        "72": "222936",
        "107": "72976",
        "111": "297762",
        "130": "1089",
        "137": "141052",
        "143": "5548",
        "144": "861",
        "177": "73344",
        "198": "268",
        "206": "869",
        "210": "12155",
        "214": "329996",
        "217": "11524",
        "224": "1538",
        "226": "420818",
        "237": "129",
        "264": "9659",
        "279": "2928",
        "303": "87502",
    },
    "patreon": {
        "8": "10195",
        "22": "118340",
        "67": "954",
        "76": "348"
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

        if row["ep_num"] in replacements[row["feed"]]:
            row["movie_id"] = replacements[row["feed"]][row["ep_num"]]
            row["release_date"] = ""
            row["movie_original_title"] = movie
            print("OVERRIDE for {:s}".format(movie))
            new_master_list.append(row)
        else:
            # search IDs of movie
            movie_data = get_movie_data_from_title(movie)
            if movie_data:
                row["movie_id"] = movie_data['id']
                row["release_date"] = movie_data['release_date']
                row["movie_original_title"] = movie_data['original_title']
                if (movie != movie_data['original_title']):
                    print("\tWARNING: '{:s}' does not match ({:s} {:s})".format(movie,row["feed"],row["ep_num"]))
                print('{:s} ({:s}) has ID: {:d}'.format(movie_data['original_title'],movie_data['release_date'],movie_data['id']))
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