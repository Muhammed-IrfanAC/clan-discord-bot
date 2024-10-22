import requests
import os

async def get_player_details(player_tag):
    url = 'https://cocproxy.royaleapi.dev/v1/players/%23'
    COC_API_KEY = os.getenv('COC_API_KEY')
    try:
        response = requests.get(url + player_tag[1:], headers={'Authorization': f'Bearer {COC_API_KEY}'})
        response.raise_for_status()
        player_data = response.json()
        return player_data
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"Check the tag you entered. Bitch!") 
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"{req_err}")
    except Exception as e:
        raise Exception(f"{e}")
