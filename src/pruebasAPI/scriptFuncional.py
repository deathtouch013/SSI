
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pandas import DataFrame
import pandas as pd
import numpy as np


scope = ['user-read-recently-played']

oauth = SpotifyOAuth(client_id='d46e12c5520d499780eb1944dd7c95ec', client_secret='cf6d069a08fb4627bef889a6bdaf3b2b',
redirect_uri='http://127.0.0.1:8100', scope=scope)

sp = spotipy.Spotify(auth_manager=oauth)

#print(oauth.get_cached_token())

tracks = sp.current_user_recently_played(limit=50)

artistas = []
canciones = []
ids = []
i = 0
x = 0
columns = ['main_artist']

datos_artistas = []

for i in range(len(tracks['items'])):
    cancion = tracks['items'][i]['track']['name']

    j = 0
    artistas_cancion = []
    ids_cancion = []
    for j in range(len( tracks['items'][i]['track']['artists'])):
        if x < len( tracks['items'][i]['track']['artists']) and j > x:
            columns.append("artist"+str(j))
            x=j
        artistas_cancion.append(tracks['items'][i]['track']['artists'][j]['name'])
        ids_cancion.append(tracks['items'][i]['track']['artists'][j]['id'])

    #data.append({tracks['items'][i]['track']['name'], tracks['items'][i]['track']['artists'][0]['name']})
    canciones.append(cancion)
    artistas.append(artistas_cancion)
    ids.append(ids_cancion)

data = {'cancion' : canciones, 'artistas' : artistas}

df = DataFrame(artistas, index=canciones, columns=columns)

dfid = DataFrame(ids, index=canciones, columns=columns)

print(dfid)

df.drop_duplicates(subset='main_artist')

df1 = df.melt(var_name='columns', value_name='index')

df2 = pd.crosstab(index=df1['index'], columns=df1['columns'])

df2['total'] = df2.sum(axis=1)

df3 = DataFrame(df2.sort_values('total', ascending=False).head().index)

#print(df3['index'].to_list())

#print(df2['total'].sort_values(ascending=False).head(10).to_json())
#print(df3)

# shows = sp.search("Melendi", type='show')

# print(shows)