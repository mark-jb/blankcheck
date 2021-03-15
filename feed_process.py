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
        #print(date.text, title.text)
        date = datetime.datetime.strptime(date.text, dateformat)
        date = date.replace(tzinfo=timezone.utc)
        print(date)
        ep = {}
        ep["date"] = date
        ep["title"] = title.text
        ep["num"] = ep_num
        ep["feed"] = shortform
        ep_num += 1
        #print(ep)
        episodes.append(ep)

def getDate(e):
    return e["date"]
    
def main():
    add_feed("rss", "EP", '%a, %d %b %Y %H:%M:%S %z')
    add_feed("rsspatreon", "BCSF", '%a, %d %b %Y %H:%M:%S %Z')
    episodes.sort(key=getDate)
    for episode in episodes:
        print(episode["feed"], episode["num"], episode["title"])


if __name__ == "__main__":
    main()
