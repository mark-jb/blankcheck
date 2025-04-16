#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys

import logging

import http.client



replacements = { "main": {
        "23a": 22059,   # Fantastic Four 2004
        "23b": 9738,   # Fantastic Four 2004
        "23d": 166424, # Fantastic Four 2015
        "30": 10000002, # Star Wars: The Clone Wars
        "34": 11,      # Star Wars
        "35": 1891,   # Empire Strikes Back
        "37": 140607,  # The Force Awakens
        "45": 6947,   # The Village
        "52": 9303,   # Bound
        "54": 603,    # The Matrix
        "60": 10000040, # Sense8
        "62": 9749,   # Fletch
        "68": 10000080,  # Denim Invasion
        "69": 297761, # Suicide Squad
        "72": 222936, # Aloha
        "73": 10000020, # Roadies
        "77": 679,    # Aliens
        "79": 280,    # T2
        "82": 597,    # Titanic
        "85": 19995,  # Avatar
        "102": 74,    # War of the Worlds
        "103": 612,   # Munich
        "107": 72976, # Lincoln
        "110": 2778,  # Clifford
        "111": 297762, # Wonder Woman
        "116": 320,    # Insomnia
        "122": 10000004, # Talking Maul
        "130": 1089,   # Point Break
        "137": 141052, # Justice League
        "142": 12775,  # Flesh + Blood
        "143": 5548,  # Robert Cop
        "144": 861,   # Total Recall
        "151": 15698, # Running Scared
        "170": 10000100, #aFamily Dog
        "171b": 9261,  # The Wedding Banquet
        "173": 4584,  # Sense and Sensibility
        "174a": 76492, # Hotel Transylvania
        "177": 146,   # Crouching Tiger Hidden Dragon
        "184": 30091,  # Chosen: The Hire
        "185": 2300,  # Space Jam
        "186": 332562, # A Star is Born
        "197": 297802, # Aquaman
        "198": 268,   # Batman
        "200": 450465, # Glass
        "206": 869,   # Planet of the Apes
        "210": 12155, # Alice in Wonderland
        "214": 329996, # Dumbo
        "217": 11524,  # Thief
        "219": 11454,  # Manhunter
        "221": 949,   # Heat
        "223": 8489,   # Ali
        "224": 1538,   # Collateral
        "226a": 420818, # Lion King
        "226b": 536869, # Cats
        "227": 11322,  # Public Enemies
        "228": 10000003, # Miami Vice Pilot
        "232": 10515,  # Castle in the Sky
        "233": 8392,   # My Neighbour Totoro
        "237": 129,    # Spirited Away
        "244c": 86209, # Fighting Mad
        "249": 11300,  # Something Wild
        "252": 274,  # Silence Of the Lambs
        "254": 39437,  # Beloved
        "258a": 982,   # Manchurian Candidate
        "258b": 14462, # Manchurian Candidate
        "264": 9659,  # Mad Max
        "273": 10000060, # 20,000 feet
        "279": 2928,  # Michael
        "286": 241771, # Beyond the Lights
        "297": 686 ,  # Contact
        "302": 17979, # Christmas Carol
        "303": 87502, # Flight
        "304": 285783, # The Walk
        "309": 531219, # The Witches
        "311": 10144, # The Little Mermaid
        "312": 812,   # Aladdin
        "313": 11970, # The Lion King
        "316": 277834,# Moana
        "319": 40687, # Heartbreak Kid
        "326": 25624, # Rosewood
        "327a": 482,   # Shaft
        "327b": 479,   # Shaft (2000)
        "327c": 486131, # Shaft (2019)
        "331": 59965, # Abduction
        "333": 2778,  # Clifford
        "337": 17814, # Assault on Precinct 13
        "338": 948,  # Halloween
        "339": 790,  # The Fog
        "341a": 1091, # The Thing
        "342": 8769, # Christine
        "345": 8852,  # Prince of Darkness
        "346": 8337,  # They Live
        "349": 12122,  # Village of the Damned
        "355": 511809, # West Side Story
        "357": 123067, # Two Friends
        "368": 21627,  # Crimewave
        "369": 765,  # Evil Dead II
        "375": 2046, # The Gift
        "376": 557, # Spiderman
        "377": 558, # Spiderman 2
        "378": 559, # Spiderman 3
        "388": 247, # The Killing
        "391": 802, # Lolita
        "393": 532639, # pinocchio
        "395": 935,    # Dr Strangelove
        "406": 76600,  # Avatar 2
        "416": 13373,  # Millions
        "417": 1272,  # Sunshine
        "426b": 33015,  # Go West
        "427b": 961,    # The General
        "428a": 34847,  # College
        "430b": 262097, # Trio
        "433": 670,    # Oldboy
        "438": 22536, # Thirst
        "442": 8077,  # Alien 3
        "444": 2649,  # the game
        "447": 1949,  # Zodiac
        "450": 65754, # Dragon tatoo
        "453": 800158, # The Killer
        "459": 19610, # A Star Is Born
        "472": 913,   # The Thomas Crown Affair 
        "474": 11535, # Rollerball 
        "479": 4977,  # Paprika
        "481": 65066,  # Going in Style
        "482": 90,      # Beverly Hills Cop
        "494": 841,     # Dune
        "495": 917496,   # Beetlejuice 2
        "497": 10000051, # Twin Peaks season 1
        "503": 940139,   # Here
        "506": 10000053, # Twin Peaks the return 1-7
        "507": 10000054, # Twin Peaks the return 8
        "508": 10000055, # Twin Peaks the return 9-13
        "509": 10000056, # Twin Peaks the return 14-18
        "519": 873,      # The Color Purple
        "599": 537921,   # Fixed
        "109": 267935,      # The BFG
        "124": 374720,      # Dunkirk
        "129": 9491,      # Blue Steel
        "209": 13885,      # Sweeney Todd: The Demon Barber of Fleet Street
        "257": 495764,      # Birds of Prey
        "276": 41776,      # This Is My Life
        "360": 713,      # The Piano
        "367": 764,      # The Evil Dead
        "372": 12106,      # The Quick and The Dead
        "409": 9905,      # Shallow Grave
        "47": 8645,      # The Happening
        "522": 11352,      # Always
        "187": 9820,      # The Parent Trap
        "336": 1410,      # Dark Star
        "343": 9663,      # Starman
        "353": 45657,      # The Ward
        "362": 13787,      # Holy Smoke!
        "390": 967,      # Spartacus
        "420": 68727,      # Trance
        "423": 515195,      # Yesterday
        "43": 2675,      # Signs
        "456": 523607,      # Maestro
        "483": 453127,      # Midnight Run
        "50": 298312,      # The Visit
        "548": 10778,      # The Man Who Wasn't There
        "550": 1120368,      # Horizon: An American Saga - Chapter 2
        "602": 1100988,      # 28 Years Later
        "607": 1368337      # The Odyssey
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
        "50": 1891,     # The Empire Strikes Back
        "51": "1892",   # Return of the Jedi
        "55": "140607", # The Force Awakens
        "59": "136799", # Trolls
        "61": "9598",   # Babe
        "67": "954",    # Mission Impossible 1
        "69": "955",    # Mission Impossible 2
        "76": "348",    # Alien
        "78": "679",    # Aliens
        "80a": 10000070, # TftC: 1
        "80b": 10000071, # TftC: 2
        "80c": 10000072, # TftC: 3
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
        "130": 10000010,  # Top of the Lake
        "131": "425909", # Ghostbusters Afterlife
        "133": "603",    # The Matrix
        "134": 10000011,  # Top of the Lake season 2
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
        "194": 10000030, # Little Drummer Girl
        "201": 10000110, # Fincher Music Videos
        "213": 10000090, # T2: 3-D
        "223": "1498", # TMNT 1
        "225": 10000001, # Paranoia Agent
        "226": "1499", # TMNT 3 
        "227": "1273", # TMNT 4 
        "229": "98566", # TMNT 5 
        "237g": 10000207, # Dumbland
        "237i": 10000209, # Lady Blue Shanghai
        "240": 10000052,  # Twin Peaks season 2
        "245": 9833,      # The Phantom of the Opera
        "247": 536869,    # Cats
        "249b": 10000301, # Night
        "249c": 10000302, # Night
        "249d": 10000303, # Columbo 
        "252a": "85483",  # Something Evil
        "252b": "110747", # Savage
        "255a": 10000304, # Twilight Zone: Kick the Can
        "255b": 10000305, # Amazing Stories: Ghost Train
        "255c": 10000306,  # Amazing Stories: The Mission
        "13": 24428,      # The Avengers
        "162": 501170,      # Doctor Sleep
        "198": 710,      # GoldenEye
        "4": 1724,      # The Incredible Hulk
        "53a": 636,      # THX-1138
        "235": 11849,      # Dungeons & Dragons
        "237c": 44510,      # The Grandmother
        "242": 12545,      # Jesus Christ Superstar
        "260": 1924      # Superman
    }
}

def get_movie_data_from_id(movie_id):
    """ Get a movie details from id"""
    if int(movie_id) >= 10000000:
        print("Returning TV moviedata")
        return {'release_date': '9999-09-09', 'id':movie_id, 'vote_average': 0, 'vote_count': 0, 'original_title': 'Television override'}
    url = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '?api_key=' + key
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
id_map_old = {}
id_map_new = {}

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
        id_map_old[row["feed"]+row["ep_num"]] = int(row["movie_id"])
        id_map[int(row["movie_id"])] = row["movie"]

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
            print("   OVERRIDE {}-{}:".format(row["feed"],row["ep_num"]))
            movie_data = get_movie_data_from_id(replacements[row["feed"]][row["ep_num"]])
        else:
            movie_data = get_movie_data_from_title(movie)
        if movie_data:
            row["movie_id"] = movie_data['id']
            row["movie_original_title"] = movie_data['original_title']
            row["vote_average"] = movie_data['vote_average']
            row["vote_count"] = movie_data['vote_count']
            if 'runtime' in movie_data:
                row["runtime"] = movie_data['release_date']
            else:
                row["runtime"] = 0
            if 'release_date' in movie_data:
                row["release_date"] = movie_data['release_date']
            else:
                row["release_date"] = "9999-09-09"
            print('{:s} [{:s}] ({:s}) has ID: {:d}'.format(row['movie_original_title'],movie,row['release_date'],row['movie_id']))
            if (movie != movie_data['original_title']):
                print("\tWARNING: '{:s}' does not match ({:s} {:s})".format(movie,row["feed"],row["ep_num"]))
            new_master_list.append(row)
            id_map_new[row["feed"]+row["ep_num"]] = int(row["movie_id"])
            id_map[int(row["movie_id"])] = row["movie_original_title"]
        else:
            print("\tWARNING: Movie '{:s}' not found".format(movie))
            failures.append(movie)

        line_count += 1
    print('Processed {:d} movies.'.format(line_count))

columns = ["date","feed","ep_num","title","movie","guest","movie_id","movie_original_title","release_date","vote_average","vote_count","runtime"]

if failures:
    print("\nFailures:")
    for fail in failures:
        print(fail)

intersection_ids = sorted(id_map_new.keys() & id_map_old.keys())
#print(id_map_old)
#print(id_map_new)
#print(id_map)
#print(intersection_ids)
print("Audit of Changes:")
for episode in intersection_ids:
    if id_map_new[episode] != id_map_old[episode]:
        print("{} is changed from {}: {} to {}: {}".format(episode, id_map_old[episode], id_map[id_map_old[episode]], id_map_new[episode], id_map[id_map_new[episode]]))

for episode, movie_id in id_map_new.items():
    if episode not in intersection_ids:
        print("{} is added. ID {}: {}".format(episode, id_map_new[episode], id_map[id_map_new[episode]]))

for episode, movie_id in id_map_old.items():
    if episode not in intersection_ids:
        print("{} is removed. ID {}: {}".format(episode, id_map_old[episode], id_map[id_map_old[episode]]))
        
write_it = input("Write changes? (y/n)")
if write_it.lower() == "y":
    print("\nWriting Changes\n")
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for e in new_master_list:
            writer.writerow(e)
else:
    print("Not writing changes")
    print("To prevent changes, put the following in 03_get_movie_ids.py")
    for episode in intersection_ids:
        if id_map_new[episode] != id_map_old[episode]:
            print('        "{}": {},      # {}'.format(episode, id_map_old[episode], id_map[id_map_old[episode]]))
