import requests
import json
import importlib
import os
import sys
from dotenv import load_dotenv

#set variable to current path to locate .env file
path = os.path.abspath(os.path.dirname(__file__))

#load environment file with api token, assign client object
load_dotenv(os.path.join(path, '.env'))

#this import statement is necessary because the directory with the champion ids has a dash
championlibrary = importlib.import_module('League-Champion-ID.getChampionNameByID', None)
getChampionNameByID = championlibrary.get_champions_name

#declare api key, obtained from .env file
RiotAPIKey = os.getenv("RIOT_TOKEN")

# declare summoner name array and set input to nothing
summoner_names = []
new_summoner = ''

#user selects region for API endpoint
region_code = input("1. Brazil\n2. Europe North\n3. Europe West\n4. Japan \
    \n5. Korea\n6. Latin America North\n7. Latin America South \
    \n8. North America\n9. Oceania\n10. Turkey\n11. Russia\nType the number for your region: ")

#defining region dict for endpoint URL and assign region code to variable
region = {
    "1":  "br1",
    "2":  "eun1",
    "3":  "euw1",
    "4":  "jp1",
    "5":  "kr",
    "6":  "la1",
    "7":  "la2",
    "8":  "na1",
    "9":  "oc1",
    "10": "tr1",
    "11": "ru",
}
url_code = region.get(region_code)

# loop through as many summoners as user requires, or exit
while new_summoner != 0:
    new_summoner = input("Enter a summoner name, or press enter to finish: ")

    #casefold summoner string for reliability
    new_summoner = new_summoner.casefold()

    #exit if user enters without typing
    if len(new_summoner) == 0:
        break

    #if string exists, append to array of summoners
    if new_summoner != 0:
        summoner_names.append(new_summoner)

#loop through every summoner and retrieve data for every summoner name
for i in range(len(summoner_names)):

    #declare summoner api endpoint to obtain encrypted summoner ID, and current summoner in array
    SummonerUrl = "https://"+url_code+".api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    summoner = summoner_names[i]

    #declare and execute summoner API call
    try:
        url = SummonerUrl+summoner
        headers = {'X-Riot-Token': RiotAPIKey,}
        response = requests.get(url = url, headers=headers,)
        user = json.loads(response.text)

        #print summoner name from API call if found
        print ("\n9Name: "+user['name'])
        
    #error handling, print summoner name     
    except KeyError:
        if(response.status_code == 404):
            print("Summoner: "+summoner+" not found.")
            continue
        if(response.status_code == 403):
            print("Check API key!")
            break

    print ("Summoner Level: "+str(user['summonerLevel']))

    #declare encrypted summoner and account ids for use with other endpoints
    summoner_id = user['id']
    account_id = user['accountId']

    #declare league url
    LeagueUrl = "https://"+url_code+".api.riotgames.com/lol/league/v4/entries/by-summoner/"

    #declare and execute league API call
    url = LeagueUrl+summoner_id
    headers = {'X-Riot-Token': RiotAPIKey,}
    response = requests.get(url = url, headers=headers,)

    league = json.loads(response.text)
    print ("Tier: "+str(league[0]['tier']))
    print ("LP: "+str(league[0]['leaguePoints']))
    print ("Wins: "+str(league[0]['wins']))
    print ("Losses: "+str(league[0]['losses']))
    if str(league[0]['hotStreak']) == "True":
        print("Hot Streak?: Yes")
    else:
        print("Hot Streak?: No")
    if str(league[0]['veteran']) == "True":
        print("Veteran?: Yes\n")
    else:
        print("Veteran: No\n")    

    #declare champion url
    ChampionUrl = "https://"+url_code+".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"

    #declare and execute champion API call
    url = ChampionUrl+summoner_id
    headers = {'X-Riot-Token': RiotAPIKey,}
    response = requests.get(url = url, headers=headers,)

    #print top 10 summoner champion info from API call, handle summoner found but no/expired champions
    try:
        champion = json.loads(response.text)
        for j in range(10):
            championid = champion[j]['championId']
            print ("Champion: "+str(getChampionNameByID(championid)))
            print ("Mastery Level: "+str(champion[j]['championLevel']))
            print ("Mastery Points: "+str(champion[j]['championPoints']))
            #if statement to sort true and false chest granting to yes and no
            if str(champion[j]['chestGranted']) == "True":
                print("Chest earned?: Yes\n")
            else:
                print("Chest earned?: No\n")

    except IndexError:
        print("No champions found!")
        continue

    #declare total mastery levels url
    MasteryUrl = "https://"+url_code+".api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/"

    #declare and execute mastery API call
    url = MasteryUrl+summoner_id
    headers = {'X-Riot-Token': RiotAPIKey,}
    response = requests.get(url = url, headers=headers,)
    
    #print total mastery level
    mastery = json.loads(response.text)
    print ("Total mastery level: "+str(mastery))
