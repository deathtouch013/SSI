import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'user-follow-read'
ranges = ['short_term', 'medium_term', 'long_term']

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='d46e12c5520d499780eb1944dd7c95ec',
client_secret='cf6d069a08fb4627bef889a6bdaf3b2b',redirect_uri='http://127.0.0.1:8100',scope=scope))

results = sp.current_user_followed_artists(limit=50)
print(results)
 