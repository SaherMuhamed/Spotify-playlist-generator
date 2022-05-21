import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

user_date_choice = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")
website_url = f"https://www.billboard.com/charts/hot-100/{user_date_choice}/"

CLIENT_ID = "3c101a62fd854a76a94e622a7941137f"
CLIENT_SECRET = "33caf15113e646ecaa67986ce94f3f89"

response = requests.get(url=website_url)

website_html = response.text
# print(website_html)

soup = BeautifulSoup(website_html, "html.parser")
all_songs = soup.find_all('h3', id='title-of-a-story', class_='a-no-trucate')
# print(all_songs)

songs_title = [song.getText().strip() for song in all_songs]
songs = songs_title[::-1]
# print(songs)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = user_date_choice.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{user_date_choice} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
