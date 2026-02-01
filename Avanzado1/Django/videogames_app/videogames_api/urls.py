from django.urls import path
from . import views 

urlpatterns = [
    path('games/',views.get_videogames, name="get_videogames"),
    path('game/', views.post_videogame, name="post_videogame"),
    path('game/<str:id>', views.handle_one_videogame, name="get_videogame")
]