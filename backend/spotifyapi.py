import requests
import json

# access token: BQBLHfCL6sBGOW3VvVQPGEUWnGgm-897jDcSDzSu1CXc4_MGTmyLXUstDogUGxLsSwvJjX8hsjmA7XctpVAkGsc6IzaTC1byXTzrPdEpLlonoRivkQOkRqG-l4P9QuHRMf9WdmA677_jK_dKIETpO1LVfBNWrmFpsx5rrSJ2TRDjWwzxDCnl0ODWww
# token_type=Bearer

# Define client_id and redirect_uri
client_id = 'cc28f1f810774c558c6d3894c1986c69'
client_secret = 'b1b30a613dc242a8be830f66858c2210'

global current_token

token_reloaded = False

special_token = 'BQA2C8HX1wFdItDwBaWd1o_DNex5t0B4b-cXu3NSJQplKEaifVRiDYrtQRU-s-bxQZV6fy10CxK9W9ahU_n423nm2bBhgUXbtkFPAxuu3T5MgrmSX6V1OF2r9V7-QoJK2GBK3V8dcDMyYi7-ZIOURSAyf_JJPLRa33pY_smrbUrD_j18Vu9JBR3ecUojJyRbeBcUY2SF_eUNc4ASS4U8JmKiRw'

with open('backend/token.txt', 'r') as file:
    current_token = file.read()
    file.close()


previous_tokens = []

redirect_uri = 'http://127.0.0.1:5500/frontend/index.html'  # Ensure this matches your registered redirect URI exactly

# decrepit?
def get_req():
  # Define the authorization endpoint and parameters
  auth_url = 'https://accounts.spotify.com/authorize'
  params = {
      'response_type': 'code',
      'client_id': client_id,
      'scope': 'user-read-private user-read-email',
      'redirect_uri': redirect_uri,
      'state': 'aaaaaaaaaaaaaaaa'
  }

  # Send the GET request
  response = requests.get(auth_url, params=params)

  # Check the status code
  if response.status_code == 200:
      print("Open this URL in your browser to authenticate:")
      print(response.url)
  else:
      print(f"Error {response.status_code}: {response.text}")

def post_req_for_token():
    url = 'https://accounts.spotify.com/api/token'
    data = {
        "grant_type": 'client_credentials',
        'client_id': 'cc28f1f810774c558c6d3894c1986c69',
        'client_secret': 'b1b30a613dc242a8be830f66858c2210'
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Send the POST request
    response = requests.post(url, data=data, headers=headers)

    # Check the status code
    if response.status_code == 200:
        print("Token fetched successfully!")
        print(response.json())  # The response contains the access token
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")

def reload_token():
    response = post_req_for_token()
    token = response.get('access_token')
    print("Token: " + token)

    with open('backend/token.txt', 'w') as file:
        file.write(token)
        file.close()

    previous_tokens.append(token)


def get_track_info():
    header = {
        "Authorization": "Bearer " + current_token
    }

    response = requests.get('https://api.spotify.com/v1/tracks/2TpxZ7JUBn3uw46aR7qd6V', headers=header)

    # Check the status code
    if response.status_code == 200:
        print("Token fetched successfully!")
        print(response.json())  # The response contains the access token
    else:
        print(f"Error {response.status_code}: {response.text}")

def search():
    # URL and parameters
    url = 'https://api.spotify.com/v1/search'

    # Query parameters
    # Options: artist, track, year, upc, tag:hipster, tag:new, isrc, and genre

    params = {
        'q': 'ME!%20artist:Taylor%20Swift',
        'type': 'album'
    }

    # Headers
    headers = {
        'Authorization': 'Bearer ' + current_token
    }

    # Send the GET request
    response = requests.get(url, headers=headers, params=params)

    # Check the status code
    if response.status_code == 200:
        print("Search result:")
        print(json.dumps(response.json(), indent=" "))  # The response contains the access token
    else:
        print(f"Error {response.status_code}:")
        print(response.json)
        print(response.url)
        print("Reloading token, trying again ...")
        reload_token()

def get_track(id):
    url = f'https://api.spotify.com/v1/tracks/{id}'
    headers = {
        'Authorization': "Bearer " + current_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Result:")
        print(json.dumps(response.json(), indent=" "))
        print(response.url)
    else:
        print(f"Error {response.status_code}:")
        print(json.dumps(response.json(), indent=" "))
        print(response.url)


def get_playlist(id):
    url = f'https://api.spotify.com/v1/playlists/{id}'
    headers = {
        'Authorization': "Bearer " + current_token
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Result:")
        print(json.dumps(response.json(), indent=" "))
        print(response.url)
    else:
        print(f"Error {response.status_code}:")
        print(json.dumps(response.json(), indent=" "))
        print(response.url)

def request_user_authentication():
    # URL and parameters
    url = f'https://accounts.spotify.com/authorize'

    # Query parameters
    # Options: artist, track, year, upc, tag:hipster, tag:new, isrc, and genre

    params = {
        'client_id': client_id,
        'response_type': 'token',
        'redirect_uri': 'http://127.0.0.1:5500/frontend/index.html',
        'scope': 'playlist-modify-public'
    }

    # Send the GET request
    response = requests.get(url, params=params)

    # Check the status code
    if response.status_code == 200:
        print("Result:")
        print(response.url)
    else:
        print(f"Error {response.status_code}:")
        print(json.dumps(response.json(), indent=" "))
        print(response.url)

def get_current_user_profile():
    url = 'https://api.spotify.com/v1/me'

    header = {
        'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'
    }


def create_playlist(song_ids):
    # URL and parameters
    user_id = 'kirsty.erica'

    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'

    # Query parameters
    # Options: artist, track, year, upc, tag:hipster, tag:new, isrc, and genre
    
    payload = {
        'name': 'Your AI Playlist',
        'description': 'palysit',
        'public': True
    }

    # Headers
    headers = {
        'Authorization': 'Bearer ' + special_token,
        'Content-Type': 'application/json'
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check the status code
    if 200 <= response.status_code <= 299:
        data = response.json()

        print("Search result:")
        print(json.dumps(data, indent=" "))  # The response contains the access token
        
        playlist_id = data.get("id")
        playlist_link = data.get("external_urls", {}).get("spotify")

        print(playlist_id, playlist_link, "\n!")

        # add all songs
        add_all_songs_to_playlist(
            song_ids,
            playlist_id
        )

        return playlist_link
    else:
        print(f"Error {response.status_code}:")
        print(json.dumps(response.json(), indent=" "))
        print(response.url)

    # TODO return playlist details

def add_all_songs_to_playlist(songs: list, playlist_id: str):
    
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    # Headers
    headers = {
        'Authorization': 'Bearer ' + special_token,
        'Content-Type': 'application/json'
    }

    payload = {
        "uris": songs
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check the status code
    if response.status_code == 200:
        print("Search result:")
        print(json.dumps(response.json(), indent=" "))  # The response contains the access token
    else:
        print(f"Error {response.status_code}:")
        print(json.dumps(response.json(), indent=" "))
        print(response.url)



# request_user_authentication()

# create_playlist()

# add all songs

# post_req_for_token()