import requests 
import os

async def get_player_details(player_tag):
  url = 'https://cocproxy.royaleapi.dev/v1/players/%23'
  COC_API_KEY = os.getenv('COC_API_KEY')
  response = await requests.get(url + player_tag, header = {'Authorization': f'Bearer {COC_API_KEY}'})
  if(response.statusCode == 200):
    player_data = response.json()
    return player_data
  else:
    raise Exception("Error fetching player data")
