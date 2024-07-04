import spotipy
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

#Spotify API
SPOTIFY_API = os.environ['SPOTIFY_ID']
SPOTIFY_KEY = os.environ['SPOTIFY_SECRET']
SPOTIFY_REDIRECT_URI = os.environ['SPOTIFY_REDIRECT_URI']

response = requests.get("https://www.billboard.com/charts/hot-100/")
soup = BeautifulSoup(response.text, "html.parser")

#Get the song names and the week of the playlist
song_names_spans = soup.select("li ul li h3")
week_tag = soup.find(class_="pmc-paywall")

week = week_tag.find("p").get_text()
song_names = [song.getText().strip() for song in song_names_spans]

#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private playlist-modify-public",
        redirect_uri=SPOTIFY_REDIRECT_URI,
        client_id=SPOTIFY_API,
        client_secret=SPOTIFY_KEY,
        show_dialog=True,
        cache_path="token.txt",
        username="Mihnea",
    )
)
#Get user id
user_id = sp.current_user()["id"]

playlist_dict = sp.user_playlists(user = user_id, limit=50, offset=0)["items"][0]
### TBD Search for the playlist in the user info and if there is the playlist delete it and create it after
print(playlist_dict)


#Create spotify playlist
playlist = sp.user_playlist_create(user=user_id,
                        name=week,
                        public=True,
                        collaborative=False,
                        description='This playlist will generate automatically based on the week bilboard')

#Get playlist id
playlist_id = playlist["id"]

#Add song to the playlist
for song_name in song_names:
    song_tag = sp.search(q=song_name, type="track")
    song_uri = [song_tag["tracks"]["items"][0]["uri"]]

    sp.playlist_add_items(playlist_id=playlist_id, items=song_uri, position=None)










