from django.urls import path
from . import views 
from django.views.generic import RedirectView

urlpatterns = [
    path('home/',RedirectView.as_view(url='/dynamic-pages/home/Juan'), name="home_template"),
    path('home/<str:name>',views.template_home, name="home_template_name"),
    path('games/', views.template_games, name="template_games")
]