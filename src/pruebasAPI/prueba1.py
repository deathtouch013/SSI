import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials(client_id='d46e12c5520d499780eb1944dd7c95ec',
client_secret='cf6d069a08fb4627bef889a6bdaf3b2b')
sp = spotipy.Spotify(auth_manager=auth_manager)

playlists = sp.user_playlist(user='xfy37pl20v1sk9vmuk3uaitcm')
print(playlists)