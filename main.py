import os
import spotipy
import requests
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

chosen_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{chosen_date}/")
response.raise_for_status()

soup = BeautifulSoup(response.text, features="html.parser")

scraped_song_titles = soup.select(selector="li ul li h3")
songs_names = [song.get_text().strip() for song in scraped_song_titles]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="https://example.com/",
                                               scope="playlist-modify-private"))

song_uris = []
year = chosen_date.split("-")[0]
USER_ID = sp.current_user()["id"]

for song in songs_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"(+) {song} doesn't exist in Spotify. Skipped.")

billboard_playlist_generator = sp.user_playlist_create(user=USER_ID, name=f"{chosen_date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=billboard_playlist_generator["id"], items=song_uris)
