from multiprocessing import context
from os import access
from telnetlib import AO
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from usuarios.forms import LoginForm, RegisterForm
from django.contrib.auth.forms import UserCreationForm
from conciertos.models import TokenUsers

import spotipy
import ast
from spotipy.oauth2 import SpotifyOAuth
from pandas import DataFrame
import pandas as pd

# Create your views here.

def oauth_init():
    scope = ['user-read-recently-played']

    oauth = SpotifyOAuth(client_id='d46e12c5520d499780eb1944dd7c95ec', client_secret='cf6d069a08fb4627bef889a6bdaf3b2b',
    redirect_uri='http://127.0.0.1:8100/conciertos/', scope=scope)

    return oauth


def login_spotify(request):
    if request.user.is_authenticated == False:
        return redirect('/usuario')

    oauth = oauth_init()

    return redirect(oauth.get_authorize_url())



def get_latest_top_artists(request):
    user = User.objects.get(username=request.user)

    token = TokenUsers.objects.get(user=user)

    tokendict = ast.literal_eval(token.spotytoken)

    sp = spotipy.Spotify(auth=tokendict['access_token'])

    try:
        tracks = sp.current_user_recently_played(limit=50)
    except:
        return redirect('/conciertos/log_in')
        # oauth = oauth_init()
        # oauth.refresh_access_token(tokendict['access_token'])
        # newtoken = oauth.get_access_token()
        # sp = spotipy.Spotify(auth=newtoken)
        # token.spotytoken = newtoken
        # tracks = sp.current_user_recently_played(limit=50)

    artistas = []
    canciones = []
    i = 0
    x = 0
    columns = ['main_artist']

    for i in range(len(tracks['items'])):
        cancion = tracks['items'][i]['track']['name']

        j = 0
        artistas_cancion = []
        for j in range(len( tracks['items'][i]['track']['artists'])):
            if x < len( tracks['items'][i]['track']['artists']) and j > x:
                columns.append("artist"+str(j))
                x=j
            artistas_cancion.append(tracks['items'][i]['track']['artists'][j]['name'])

        canciones.append(cancion)
        artistas.append(artistas_cancion)

    data = {'cancion' : canciones, 'artistas' : artistas}

    print(columns)

    df = DataFrame(artistas, index=canciones, columns=columns)

    df.drop_duplicates(subset='main_artist')

    df1 = df.melt(var_name='columns', value_name='index')

    df2 = pd.crosstab(index=df1['index'], columns=df1['columns'])

    df2['total'] = df2.sum(axis=1)

    df3 = DataFrame(df2.sort_values('total', ascending=False).head().index)

    jsondata = df3['index'].to_list()

    return jsondata

def songs_artists(request):
    if request.user.is_authenticated == False:
        return redirect('/usuario')

    oauth = oauth_init()
    
    context = {}

    qdict = request.GET
    if qdict.__contains__('code'):
        code = qdict['code']
        token = oauth.get_access_token(code=code)

        #Obtenemos usuario logeao
        user = User.objects.get(username=request.user)

        try:
            u = TokenUsers.objects.get(user=user)
            u.spotytoken = token
        except:
            u = TokenUsers(spotytoken=token)
            u.user = user

        u.save()
        
    
    artistas = get_latest_top_artists(request)
    context = {'artistas': artistas}

    return render(request, 'conciertos/songs_artists.html', context)

def userinfo(request):
    if request.user.is_authenticated == False:
        return redirect('/usuario')

    return render(request, 'conciertos/userinfo.html')