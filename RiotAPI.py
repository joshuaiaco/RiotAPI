import requests
import json
import importlib

#this import statement is necessary because the directory with the champion ids has a dash
championlibrary = importlib.import_module('League-Champion-ID.getChampionNameByID', None)
getChampionNameByID = championlibrary.get_champions_name

#declare api key
APIKey = "RGAPI-562068f7-42f9-436d-a6cd-a1ce729472ef"

# declare summoner name array and set input to nothing
summoner_names = []
new_summoner = ''

# loop through as many summoners as user requires, or exit
while new_summoner != 'exit':
    new_summoner = input("Enter a summoner name, or type exit to finish: ")

    #casefold summoner string for fun and to exit on EXIT or ExIt or EXiT
    new_summoner = new_summoner.casefold()

    #if string is not, in fact, exit, append to array of summoners
    if new_summoner != 'exit':
        summoner_names.append(new_summoner)

#loop through every summoner and retrieve data for every summoner name
for i in range(len(summoner_names)):

    #declare summoner api endpoint to obtain encrypted summoner ID, and current summoner in array
    SummonerUrl = "https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    summoner = summoner_names[i]

    #declare and execute summoner API call
    try:
        url = SummonerUrl+summoner
        headers = {'X-Riot-Token': APIKey,}
        response = requests.get(url = url, headers=headers,)
        user = json.loads(response.text)

        #print summoner name from API call if found
        print ("Name: "+user['name'])
        
    #error handling, print summoner name     
    except KeyError:
        if(response.status_code == 404):
            print("Summoner: "+summoner+" not found.")
            continue
        if(response.status_code == 403):
            print("Check API key!")
            break

    print ("Summoner Level: "+str(user['summonerLevel']))

    #declare encrypted summoner id for use with other endpoints
    summoner_id = user['id']

    #declare league url
    LeagueUrl = "https://oc1.api.riotgames.com/lol/league/v4/entries/by-summoner/"

    #declare and execute league API call
    url = LeagueUrl+summoner_id
    headers = {'X-Riot-Token': APIKey,}
    response = requests.get(url = url, headers=headers,)

    league = json.loads(response.text)
    print ("Tier: "+str(league[0]['tier']))
    print ("LP: "+str(league[0]['leaguePoints']))
    print ("Wins: "+str(league[0]['wins']))
    print ("Losses: "+str(league[0]['losses'])) 
    print ("Hot Streak?: "+str(league[0]['hotStreak']))
    print ("Veteran?: "+str(league[0]['veteran']))
    print ("")
    

    #declare champion url
    ChampionUrl = "https://oc1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"

    #declare and execute champion API call
    url = ChampionUrl+summoner_id
    headers = {'X-Riot-Token': APIKey,}
    response = requests.get(url = url, headers=headers,)

    #print top 10 summoner champion info from API call, handle summoner found but no/expired champions
    try:
        champion = json.loads(response.text)
        for j in range(10):
            championid = champion[j]['championId']
            print ("Champion: "+str(getChampionNameByID(championid)))
            print ("Mastery Level: "+str(champion[j]['championLevel']))
            print ("Mastery Points: "+str(champion[j]['championPoints']))
            print ("Chest earned?: "+str(champion[j]['chestGranted']))
            print("")
    except IndexError:
        print("No champions found!")
        continue

    #declare total mastery levels url
    MasteryUrl = "https://oc1.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/"

    #declare and execute mastery API call
    url = MasteryUrl+summoner_id
    headers = {'X-Riot-Token': APIKey,}
    response = requests.get(url = url, headers=headers,)
    
    #print total mastery level
    mastery = json.loads(response.text)
    print ("Total mastery level: "+str(mastery))