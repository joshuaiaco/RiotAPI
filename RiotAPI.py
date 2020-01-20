import requests
import json
import importlib

#this import statement is necessary because the directory with the champion ids has a dash
championlibrary = importlib.import_module('League-Champion-ID.getChampionNameByID', None)
getChampionNameByID = championlibrary.get_champions_name

#declare api key
APIKey = "RGAPI-e626a976-6862-43bb-9ccb-91c69236fd21"

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

        #print summoner info from API call, assign encrypted UUID
        print ("Name: "+user['name'])
        
    #error handling    
    except KeyError:
        if(response.status_code == 404):
            print("Summoner: "+summoner+" not found.")
            continue
        if(response.status_code == 403):
            print("Likely bad API key!")

    print ("Summoner Level: "+str(user['summonerLevel']))
    summoner_id = user['id']

    #declare champion url
    ChampionUrl = "https://oc1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"

    #declare and execute champion API call
    url = ChampionUrl+summoner_id
    headers = {'X-Riot-Token': APIKey,}
    response = requests.get(url = url, headers=headers,)

    #print top 10 summoner champion info from API call
    champion = json.loads(response.text)
    for j in range(10):
        championid = champion[j]['championId']
        print ("Champion: "+str(getChampionNameByID(champion[j]['championId'])))
        print ("Summoner Level: "+str(champion[j]['championPoints']))