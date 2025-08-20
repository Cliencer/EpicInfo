import requests
import math
import json
import time
import re
from slugify import slugify
from strsimpy.optimal_string_alignment import OptimalStringAlignment
from rich.progress import Progress
steamAppid = {}
epic2steam = {}
nameList = []

test = {}

useCache = True
osa = OptimalStringAlignment()
def handleEpicName(name):
    index = name.find("--")
    if index != -1:
        return name[:index]

    index = name.rfind('-')
    if index == -1:
        return name
    suffix = name[index + 1:]
    if len(suffix) != 6:
        return name
    try:
        int(suffix, 16)
        return name[:index]
    except ValueError:
        return name

def handleSteamName(name):
    index = name.find("--")
    if index != -1:
        return name[:index]

    index = name.rfind('-')
    if index == -1:
        return name
    suffix = name[index + 1:]
    if len(suffix) != 6:
        return name
    try:
        int(suffix, 16)
        return name[:index]
    except ValueError:
        return name   
def strSimilar(str,list):
    minDistance = 9999999
    out = ""
    for comp in list:
        if comp.find(str) == 0:
            return list[comp]
    return out
    #     dis = osa.distance(str,comp)
    #     if dis < minDistance:
    #         minDistance = dis
    #         out = comp
    #     if dis <= 1:
    #         return comp
    # if minDistance > len(out)/4:
    #     return ""
    # return out

if not useCache:
    res1 = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v1/?format=json')
    res1 = res1.json()
    res1 = res1["applist"]["apps"]["app"]
    res2 = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v2/?format=json')
    res2 = res2.json()
    res2 = res2["applist"]["apps"]
    try:
        for game in res1:
            steamAppid[slugify(game["name"])] = game["appid"]
        for game in res2:
            if not game["appid"] in steamAppid.values():
                steamAppid[slugify(game["name"])] = game["appid"]
    except:
        print(game)
        pass
    steamAppid.pop("")
    with open('steamAppid.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(steamAppid))
else:
    with open('steamAppid.json', 'r', encoding='utf-8') as f:
        steamAppid = json.loads(f.read())

with open('namespace.json', 'r', encoding='utf-8') as f:
    namespace = json.loads(f.read())
with open('offerid.json', 'r', encoding='utf-8') as f:
    offerid = json.loads(f.read())

steamAppid.pop("")
nameList = steamAppid.keys()



with Progress() as progress:  
    task = progress.add_task("Processing...", total=len(namespace)+len(offerid)) 
    for hash in namespace:
        name = handleEpicName(namespace[hash])
        if steamAppid.get(name) != None:
            epic2steam[namespace[hash]] = steamAppid[name]
        else:
            epic2steam[namespace[hash]] = strSimilar(namespace[hash],steamAppid)
        progress.update(task, advance=1)
    for hash in offerid:
        name = handleEpicName(offerid[hash])
        if steamAppid.get(name) != None:
            epic2steam[offerid[hash]] = steamAppid[name]
        else:
            epic2steam[offerid[hash]] = strSimilar(offerid[hash],steamAppid)
        progress.update(task, advance=1)

with open('epic2steam.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(epic2steam))
print("Down!")
