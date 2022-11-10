from http import client
from unicodedata import name
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys

urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='d46e12c5520d499780eb1944dd7c95ec',
client_secret='cf6d069a08fb4627bef889a6bdaf3b2b'))
response = sp.artist_top_tracks(urn)

for track in response['tracks']:
    print(track['name'])