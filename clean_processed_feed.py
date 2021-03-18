#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys
import re

new_list = []
main_ep_nums_delete = [2,3,4,5,6,7,8,9,10,11,14,15,16,17,18,19,20,21,22,25,26,27,28,29,30,31,32,33,39,83,86,89,90,91,122,125,158,170,228,263]
patreon_ep_nums_delete = [1,5,14,20,21,27,30,33,39,45,47,49,59,65,77,80,89]

main_replacements = {
        "1": ["The Phantom Menace"],
        "12": ["The Judge"],
        "13": ["Attack of the Clones"],
        "23": ["The Fantastic Four", "Fant4stic"],
        "24": ["Revenge of the Sith"],
        "34": ["Star Wars: A New Hope"],
        "35": ["The Empire Strikes Back"],
        "36": ["Return of the Jedi"],
        "37": ["The Force Awakens"],
        "38": ["The Star Wars Holiday Special"],
        "40": ["Praying with Anger", "Wide Awake"],
        "53": ["Batman v Superman: Dawn of Justice"],
        "80": ["Jack Reacher", "Jack Reacher: Never Go Back"],
        "84": ["Aliens of the Deep", "Ghosts of the Abyss"],
        "171": ["Pushing Hands", "The Wedding Banquet"],
        "174": ["Hotel Transylvania", "Hotel Transylvania 2", "Hotel Transylvania 3"],
        "194": ["Wreck-it Ralph", "Ralph Breaks the Internet"],
        "244": ["Caged Heat","Crazy Mama","Fighting Mad"],
        "245": ["Citizens Band","Last Embrace"],
        "246": ["Melvin and Howard"],
        "260": ["A Master Builder", "Playmobil: The Movie"]
        }
patreon_replacements = {
        "53": ["THX-1138", "American Graffiti"],
        "93": ["The Return of Jafar","Aladdin and the King of Thieves"]
        }

def clean_main(episode):
    if int(episode["ep_num"]) in main_ep_nums_delete: return []
    if "Blank Check Awards" in episode["movie"]: return []
    if "Mailbag" in episode["movie"]: return []
    if "March Madness" in episode["movie"]: return []
    if int(episode["ep_num"]) == 40: episode["guest"] = ""

    episodes = []
    if episode["ep_num"] in main_replacements.keys():
        for title in main_replacements[episode["ep_num"]]:
            e = episode.copy()
            e["movie"] = title
            episodes.append(e)
    else:
        episodes.append(episode)
    for e in episodes: print("Main feed:", e["ep_num"], e["movie"])

    return episodes

def clean_patreon(episode):
    if int(episode["ep_num"]) in patreon_ep_nums_delete: return []
    if "Blank Check Awards" in episode["movie"]: return []
    if "Mailbag" in episode["movie"]: return []
    if "March Madness" in episode["movie"]: return []
    episodes = []
    if episode["ep_num"] in patreon_replacements.keys():
        for title in patreon_replacements[episode["ep_num"]]:
            e = episode.copy()
            e["movie"] = title
            episodes.append(e)
    else:
        episodes.append(episode)
    for e in episodes: print("Patreon feed:", e["ep_num"], e["movie"])
    return episodes

def title_clean(episode):
    split_title = re.split('( with )', episode["title"])
    episode["movie"] = split_title[0]
    episode["guest"] = split_title[2] if len(split_title) > 1 else ""
    if episode["feed"] == "main":
        for e in clean_main(episode):
            new_list.append(e)
    elif episode["feed"] == "patreon":
        for e in clean_patreon(episode):
            new_list.append(e)


f = open("key", "r")
key = f.readline()
key = key.strip()
print(key)

in_csv = 'feed.processed.csv'
out_csv = 'episodes.cleaned.csv'

# Read list of movies

with open(in_csv, mode='r') as csv_episodelist:
    csv_reader = csv.DictReader(csv_episodelist)
    for row in csv_reader:
        title_clean(row)


with open('movies.cleaned.csv', 'w') as f:
    writer = csv.writer(f, new_list[0].keys())
    writer.writerow(new_list[0].keys())
    for e in new_list:
        print(e)
        writer.writerow(e.values())
