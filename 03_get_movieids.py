#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys

import logging

import http.client



replacements = { "main": {
        "23a": "22059",   # Fantastic Four 2004
        "23b": "9738",   # Fantastic Four 2004
        "23d": "166424", # Fantastic Four 2015
        "34": "11",      # Star Wars
        "37": "140607",  # The Force Awakens
        "45": "6947",   # The Village
        "52": "9303",   # Bound
        "54": "603",    # The Matrix
        "62": "9749",   # Fletch
        "72": "222936", # Aloha
        "77": "679",    # Aliens
        "79": "280",    # T2
        "82": "597",    # Titanic
        "85": "19995",  # Avatar
        "69": "297761", # Suicide Squad
        "102": "74",    # War of the Worlds
        "103": "612",   # Munich
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
        "173": "4584",  # Sense and Sensibility
        "174a": "76492", # Hotel Transylvania
        "177": "146",   # Crouching Tiger Hidden Dragon
        "185": "2300",  # Space Jam
        "198": "268",   # Batman
        "200": "450465", # Glass
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
        "233": "8392",   # My Neighbour Totoro
        "237": "129",    # Spirited Away
        "244c": "86209", # Fighting Mad
        "249": "11300",  # Something Wild
        "252": "274",  # Silence Of the Lambs
        "254": "39437",  # Beloved
        "258a": "982",   # Manchurian Candidate
        "258b": "14462", # Manchurian Candidate
        "264": "9659",  # Mad Max
        "279": "2928",  # Michael
        "297": "686" ,  # Contact
        "302": "17979", # Christmas Carol
        "303": "87502", # Flight
        "304": "285783", # The Walk
        "309": "531219", # The Witches
        "311": "10144", # The Little Mermaid
        "312": "812",   # Aladdin
        "313": "11970", # The Lion King
        "316": "277834",# Moana
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
        "345": "8852",  # Prince of Darkness
        "346": "8337",  # They Live
        "349": "12122",  # Village of the Damned
        "355": "511809", # West Side Story
        "357": "123067", # Two Friends
        "368": "21627",  # Crimewave
        "369": "765",  # Evil Dead II
        "375": "2046", # The Gift
        "376": "557", # Spiderman
        "377": "558", # Spiderman 2
        "378": "559", # Spiderman 3
        "388": "247", # The Killing
        "391": "802", # Lolita
        "393": "532639", # pinocchio
        "395": "935",    # Dr Strangelove
        "406": "76600",  # Avatar 2
        "416": "13373",  # Millions
        "426b": "33015",  # Go West
        "428a": "34847",  # College
        "430b": "262097", # Trio
        "433": "670",    # Oldboy
        "438": "22536", # Thirst
        "442": "8077",  # Alien 3
        "444": "2649",  # the game
        "450": "65754", # Dragon tatoo
        "459": "19610", # A Star Is Born
        "474": "11535",  # Rollerball 
        "479": "4977",  # Paprika
        "487": "841",  # Dune
        "503": "537921", # Fixed
        "504": "940139" # Here
    },
    "patreon": {
        "2": "1726",    # Iron Man
        "3": "1927",    # Hulk
        "8": "10195",   # Thor
        "22": "118340", # Guardians Vol 1
        "25": "102899", # Ant-Man
        "28": "284052", # Doctor Strange
        "34": "284054", # Black Panther
        "37": "363088", # Ant Man 2
        "44": "348350", # Solo
        "46": "330459", # Rogue One
        "48": "11",     # Star Wars
        "51": "1892",   # Return of the Jedi
        "55": "140607", # The Force Awakens
        "59": "136799", # Trolls
        "61": "9598",   # Babe
        "67": "954",    # Mission Impossible 1
        "69": "955",    # Mission Impossible 2
        "76": "348",    # Alien
        "78": "679",    # Aliens
        "105": "24021", # Twilight Eclipse
        "115": "564",   # The Mummy
        "117": "40047", # Elvis
        "121a": "9334",  # Body Bags
        "121b": "31578", # The Scorpion King
        "120": "282035", # The Mummy 2017
        "122": "11395",  # the Santa Clause
        "126": "620",    # Ghostbusters
        "128": "2978",   # Ghostbusters 2
        "129": "43074",  # Ghostbusters 2016
        "131": "425909", # Ghostbusters Afterlife
        "133": "603",    # The Matrix
        "139": "109428", # Evil dead 2013
        "141": "2661",   # Batman 1966
        "148": "209112", # Batman v Superman
        "149": "209112", # Batman v Superman
        "150": "88496",  # Liza with a Z
        "152": "414906", # The Batman
        "153": "363676", # Sully
        "155": "682",    # The Man with the Golden Gun
        "171": "11667",  # Street Fighter
        "172": "607",    # MIB
        "174": "608",    # MIB2
        "181": "123024", # Olympicss
        "182": "871",    # Planet of the Apes
        "184a": "51471",   # Buster Keaton Shorts
        "184b": "23282",   # Buster Keaton Shorts
        "184c": "46510",   # Buster Keaton Shorts
        "184d": "51362",   # Buster Keaton Shorts
        "184e": "38742",   # Buster Keaton Shorts
        "184f": "45807",   # Buster Keaton Shorts
        "189": "299",    # Ocean's 11 (1960)
        "192": "161",    # Ocean's 11
        "225": "1498", # TMNT 1
        "227": "1000001", # Paranoia Agent
        "228": "1499", # TMNT 3 
        "229": "1273", # TMNT 4 
        "231": "98566" # TMNT 5 
    }
}

def get_movie_data_from_id(movie_id):
    """ Get a movie details from id"""
    url = 'https://api.themoviedb.org/3/movie/' + movie_id + '?api_key=' + key
    response = session.get(url)
    responsedict = response.json()
    return responsedict


def get_movie_data_from_title(title):
    """ Get a movie id from the title"""
    #print("getting movie id for " + title)
    enc_title = ul.quote_plus(title)
    #print("encoded title as " + enc_title)
    
    url = 'https://api.themoviedb.org/3/search/movie?api_key=' + key + '&language=en-US&query=' + enc_title + '&page=1&include_adult=false'
    response = session.get(url)
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
in_existing_csv = 'movies.with.ids.csv'
out_csv = 'movies.with.ids.csv'

new_master_list = []
failures = []
id_map = {}

debug = False
if debug:
    # Dubug logging
    http.client.HTTPConnection.debuglevel = 1
    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

# Open persistent session:
session = requests.Session()


# Read in the existing movieIDs if we are skipping done stuff [IN PROGRESS]
with open(in_existing_csv, mode='r') as csv_idlist:
    csv_reader = csv.DictReader(csv_idlist)
    for row in csv_reader:
        print('Caching {:s} -> {:s}'.format(row["feed"]+row["ep_num"], row["movie_id"]))
        id_map[row["feed"]+row["ep_num"]] = row["movie_id"]

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
            row["vote_average"] = movie_data['vote_average']
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

columns = ["date","feed","ep_num","title","movie","guest","movie_id","movie_original_title","release_date","vote_average"]

with open(out_csv, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    for e in new_master_list:
        writer.writerow(e)

print("\nFailures:")
for fail in failures:
    print(fail)
     
