#!/usr/bin/python3

import csv
import xml.etree.ElementTree as ET
import json
import requests
import urllib.parse as ul
import sys
import datetime
from datetime import timezone

episodes=[]

def add_feed(filename, shortform, dateformat):
    print("Starting ", filename)
    tree = ET.parse(filename)
    root = tree.getroot()
    ep_num=1
    items = root.findall('.//item')
    for episode in reversed(items):
        date = episode.find('.//pubDate')
        title = episode.find('.//title')
        if title.text == 'Blank Check with Griffin & David Trailer':
            continue
        #print(date.text, title.text)
        date = datetime.datetime.strptime(date.text, dateformat)
        date = date.replace(tzinfo=timezone.utc)
        #print(date)
        ep = {}
        ep["date"] = date.isoformat()
        ep["feed"] = shortform
        ep["ep_num"] = str(ep_num)
        ep["title"] = title.text
        ep_num += 1
        #print(ep)
        episodes.append(ep)

def getDate(e):
    return e["date"]
    
def main():
    add_feed("rss.main", "main", '%a, %d %b %Y %H:%M:%S %z')
    add_feed("rss.patreon", "patreon", '%a, %d %b %Y %H:%M:%S %Z')
    episodes.sort(key=getDate)

    columns = ["date","feed","ep_num","title"]
    with open('feed.processed.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = columns, lineterminator='\n')
        writer.writeheader()
        for e in episodes:
          #  print(e["date"].isoformat() + ',' + e["feed"] + ',' + str(e["num"]) + ',' + e["title"])
            print(e)
            writer.writerow(e)


if __name__ == "__main__":
    main()
