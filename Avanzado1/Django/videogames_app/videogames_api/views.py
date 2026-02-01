from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import VideoGame

# Create your views here.
@api_view(['GET'])
def get_videogames(request):
    precio_min = request.GET.get("precio_min",1)
    try:
        precio_min = int(precio_min)
    except ValueError:
        return Response({"message":"El precio minimo debe ser un valor numerico"}, status=400)
    
    games = list(VideoGame.objects(precio__gte=precio_min).order_by("-creation_date"))
    games_seriazable = list(map(lambda g_item: g_item.as_dic(),games))

    return Response(games_seriazable, status=200)

@api_view(['POST'])
def post_videogame(request):
    body = request.data
    required_fields = ["nombre", "plataforma", "fecha", "genero", "clasificacion", "precio"]
    missing = [f for f in required_fields if f not in body]
    if missing:
        return Response({"message": f"Faltan campos: {', '.join(missing)}"}, status=400)
    try:
        new_videogame = VideoGame(
            nombre=body["nombre"],
            plataforma=body["plataforma"],
            fecha=int(body["fecha"]),
            genero=body["genero"],
            clasificacion=body["clasificacion"],
            precio=int(body["precio"]))
        new_videogame.save()    
    except (ValueError, TypeError) as e:
        return Response({"message": f"Tipos de datos invalidos: {str(e)}"}, status=400)
    
    return Response(new_videogame.as_dic(), status=201)

def get_videogame(_,id):
    try:
        videogame =  VideoGame.objects.get(id=id)
        return Response(videogame.as_dic(), status= 200)
    except VideoGame.DoesNotExist:
        return Response({"message": f"El videojuego con id: {id} no existe"}, status= 404)
 
def delete_videogame(_,id):
    try:
        videogame =  VideoGame.objects.get(id=id)
        data = videogame.as_dic()
        videogame.delete()
        return Response(data, status= 200)
    except VideoGame.DoesNotExist:
        return Response({"message": f"El videojuego con id: {id} no existe"}, status= 204)

@api_view(["GET","DELETE"])
def handle_one_videogame(request,id):
    if request.method== "GET":
        return get_videogame(request,id)
    else:
        return delete_videogame(request,id)