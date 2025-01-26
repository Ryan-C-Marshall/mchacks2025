import requests
import base64
import json

# Define client_id and redirect_uri
client_id = 'cc28f1f810774c558c6d3894c1986c69'
client_secret = 'b1b30a613dc242a8be830f66858c2210'

global current_token

token_reloaded = False

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

def reload_token(callback:callable=None, args:list=None):
    if token_reloaded:
        print("Already reloaded token. There is another error.")
    else:
        token_reloaded = True

    response = post_req_for_token()
    token = response.get('access_token')
    print("Token: " + token)

    with open('backend/token.txt', 'w') as file:
        file.write(token)
        file.close()

    current_token = token
    previous_tokens.append(token)

    if callback is not None:
        if args is not None:
            callback(*args)
        else:
            callback()


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
        # reload_token(callback=get_reccomendations,args=[])

search()
# post_req_for_token()