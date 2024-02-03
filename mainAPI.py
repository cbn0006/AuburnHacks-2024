import requests
from requests import get
import base64
import json


def get_access_token(client_id, client_secret):
    token_url = "https://accounts.spotify.com/api/token"
    auth_headers = f"{client_id}:{client_secret}"
    encoded_auth_headers = base64.b64encode(auth_headers.encode()).decode()

    auth_payload = {
        "grant_type": "client_credentials",
    }

    headers = {"Authorization": f"Basic {encoded_auth_headers}"}

    response = requests.post(token_url, data=auth_payload, headers=headers)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(
            f"Failed to retrieve access token. Status code: {response.status_code}, Response: {response.text}"
        )
        return None


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    artist_id = json_result.get("artists", {}).get("items", [{}])[0].get("id")

    return artist_id


def search_related_artist(token, artist_id, limit=5):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    related_artists = json_result.get("artists", [])[:limit]
    artist_names = [artist.get("name") for artist in related_artists]
    return artist_names


def main():
    # Replace these with your own values
    client_id = "fcf64bb0ff3d47298a54df28088d4f75"
    client_secret = "bab82d0743d74edcb3f18d24fc5953d3"

    access_token = get_access_token(client_id, client_secret)

    artist_id = search_for_artist(access_token, "ACDC")
    related_artist = search_related_artist(access_token, artist_id)

    print(related_artist)


if __name__ == "__main__":
    main()
