from django.db import models

# Create your models here.

class Game:
    # **kwargs Materials(name= , descrition= ..... )
    def __init__(self,dic):
        self.name = dic["name"]
        self.description = dic["description"]
        self.price_starting = dic["price_starting"]
        self.platforms = dic["platforms"]
        
        
def create_games(dic):
    return list(map( lambda e: Game(e), dic) )

GAMES = create_games([
    {
        "name": "The Legend of Zelda: Breath of the Wild",
        "description": "Explora un mundo abierto lleno de aventuras y secretos.",
        "price_starting": 59900,
        "platforms": "Nintendo Switch"
    },
    {
        "name": "God of War Ragnarok",
        "description": "Acompaña a Kratos y Atreus en una épica aventura en la mitología nórdica.",
        "price_starting": 69900,
        "platforms": "PS5, PS4"
    },
    {
        "name": "Cyberpunk 2077",
        "description": "Un RPG futurista de mundo abierto con acción y narrativa profunda.",
        "price_starting": 49900,
        "platforms": "PC, PS5, Xbox Series X"
    },
    {
        "name": "Minecraft",
        "description": "Construye y explora mundos infinitos en modo creativo o supervivencia.",
        "price_starting": 29900,
        "platforms": "PC, PS5, Xbox, Switch, Mobile"
    }
])