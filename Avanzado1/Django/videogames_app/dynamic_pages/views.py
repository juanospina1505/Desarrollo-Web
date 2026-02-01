from django.shortcuts import render
from . import models

# Create your views here.

def template_home(request, name):
    context = {
        'titulo_pagina' : "VideoGames APP Django",
        'mi_nombre': name,
        'show_api_endpoints': True
    }
    return render(request,'base.html',context)

def template_games(request):
    context = {
        'games': models.GAMES
    }
    return render(request,'games.html',context)