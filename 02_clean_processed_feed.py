#!/usr/bin/python3

import json
import requests
import csv
import urllib.parse as ul
import sys
import re
import string

new_list = []

ep_nums_delete = {
        "main": [2,3,4,5,6,7,8,9,10,11,14,15,16,17,18,19,20,21,22,25,26,27,28,29,31,32,33,39,83,86,89,90,91,125,158,263,461],
        "patreon": [1,5,14,20,21,27,30,33,39,45,47,49,65,77,89,101,114,118,124,142,147,149,165,187,190,191,199,208,290],
        "crit": [1]
        }

replacements = {
        "main": {
            "1": ["Star Wars: The Phantom Menace"],
            "12": ["The Judge"],
            "13": ["Star Wars: Attack of the Clones"],
            "23": ["The Fantastic Four", "Fantastic Four", "Fantastic Four: Rise of the Silver Surfer", "Fant4stic"],
            "24": ["Star Wars: Revenge of the Sith"],
            "30": ["Star Wars: The Clone Wars"],
            "34": ["Star Wars: A New Hope"],
            "35": ["Star Wars: The Empire Strikes Back"],
            "36": ["Star Wars: Return of the Jedi"],
            "37": ["Star Wars: The Force Awakens"],
            "38": ["The Star Wars Holiday Special"],
            "40": ["Praying with Anger", "Wide Awake"],
            "53": ["Batman v Superman: Dawn of Justice"],
            "80": ["Jack Reacher", "Jack Reacher: Never Go Back"],
            "84": ["Aliens of the Deep", "Ghosts of the Abyss"],
            "171": ["Pushing Hands", "The Wedding Banquet"],
            "174": ["Hotel Transylvania", "Hotel Transylvania 2", "Hotel Transylvania 3"],
            "176": ["Ride with the Devil"],
            "194": ["Wreck-it Ralph", "Ralph Breaks the Internet"],
            "226": ["Lion King", "Cats"],
            "244": ["Caged Heat","Crazy Mama","Fighting Mad"],
            "245": ["Citizens Band","Last Embrace"],
            "246": ["Melvin and Howard"],
            "258": ["The Manchurian Candidate","The Manchurian Candidate"],
            "260": ["A Master Builder", "Playmobil: The Movie"],
            "327": ["Shaft","Shaft","Shaft"],
            "341": ["The Thing","The Thing from Another World"],
            "387": ["Fear and Desire","Killer's Kiss"],
            "450": ["The Girl with the Dragon Tattoo"],
            "457": ["Wonka","Aquaman and the Lost Kingdom"],
            "471": ["Die Hard with a Vengeance"],
            "500": ["Goodrich","Joker: Folie à Deux"]
            },
        "patreon": {
            "3": ["Hulk Live"],
            "53": ["THX-1138", "American Graffiti"],
            "65": ["Toy Story of Terror","Toy Story That Time Forgot","Small Fry","Hawaiian Vacation","Partysaurus Rex"],
            "69": ["Mission: Impossible II"],
            "70": ["Mission: Impossible III"],
            "79": ["Alien3"],
            "80": ["Tales from the Crypt: And All Through the Night","Tales from the Crypt: Yellow","Tales from the Crypt: You, Murderer"],
            "83": ["Armageddon"],
            "93": ["The Return of Jafar","Aladdin and the King of Thieves"],
            "98": ["Ömer the Tourist in Star Trek"],
            "110": ["F9"],
            "121": ["The Scorpion King", "Body Bags"],
            "145": ["Old Dogs"],
            "148": ["Batman v Superman: Dawn of Justice - Ultimate Edition"],
            "150": ["Liza with a Z"],
            "153": ["Sully"],
            "155": ["The Man with the Golden Gun"],
            "184": ["The Cook","One Week","The High Sign","The Playhouse","Cops","The Balloonatic"],
            "197": ["Alien vs. Predator", "Alien vs. Predator: Requiem"],
            "228": ["Hot Dogs for Gauguin","Hot Tomorrows"],
            "238": ["Six Men Getting Sick","The Alphabet","The Grandmother","The Amputee","The Cowboy and the Frenchman","Premonition Following an Evil Deed","Dumbland","Rabbits","Lady Blue Shanghai","What Did Jack Do?"],
            "250": ["Amblin","Night Gallery: Eyes","Night Gallery: Make Me Laugh","Columbo: Murder by the Book"],
            "253": ["Something Evil","Savage"],
            "260": ["Twilight Zone: Kick the Can","Amazing Stories: Ghost Train","Amazing Stories: The Mission"],
            "277": ["King Ralph"]
            },
        "crit": {
            "4": ["F1"],
            "5": ["Train Dreams"]
            }
        }

def clean(episode, feed):
    episodes = []
    if episode["ep_num"] in replacements[feed].keys():
        for title, letter in zip(replacements[feed][episode["ep_num"]], string.ascii_lowercase):
            e = episode.copy()
            if len(replacements[feed][episode["ep_num"]]) > 1:
                e["ep_num"] = e["ep_num"] + letter
            e["movie"] = title
            episodes.append(e)
    elif "/" in episode["movie"]:
        for title, letter in zip(episode["movie"].split("/"), string.ascii_lowercase):
            e = episode.copy()
            e["ep_num"] = e["ep_num"] + letter
            e["movie"] = title.strip()
            episodes.append(e)
    else:
        if int(episode["ep_num"]) in ep_nums_delete[feed]: return []
        if "Blank Check Awards" in episode["movie"]: return []
        if "Mailbag" in episode["movie"]: return []
        if "March Madness" in episode["movie"]: return []
        if "MARCH MADNESS" in episode["movie"]: return []
        if "Fanfare" in episode["movie"]: return []
        if "Spreadmaster" in episode["movie"]: return []
        if "Burger Report" in episode["movie"]: return []
        # Okay, this is an episode to add
        episodes.append(episode)
    for e in episodes: print("Episode:",e["feed"], e["ep_num"], e["movie"])
    return episodes

def title_clean(episode):
    if  episode["feed"] == "crit":
        working_title = re.sub("Critical Darlings: ", "", episode["title"])
        split_title = re.split('( with )', working_title)
        episode["guest"] = split_title[2].strip() if len(split_title) > 1 else ""
        split_title = re.split('( And The )', split_title[0].strip())
        episode["movie"] = split_title[0].strip()

    else:
        split_title = re.split('( with )', episode["title"])
        episode["movie"] = split_title[0].strip()
        episode["guest"] = split_title[2] if len(split_title) > 1 else ""
    for e in clean(episode, episode["feed"]):
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

columns = ["date","feed","ep_num","title","movie","guest"]

with open('movies.cleaned.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns, lineterminator='\n')
    writer.writeheader()
    for e in new_list:
        print(e)
        writer.writerow(e)
