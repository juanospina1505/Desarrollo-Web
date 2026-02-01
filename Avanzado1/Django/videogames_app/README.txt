README.txt
==========

Proyecto: VideoGames API (Django + MongoEngine)
Autor: Juan Camilo Ospina Ospina

------------------------------------------------------------
1) Requisitos
------------------------------------------------------------
- Docker Desktop instalado y funcionando
- Puerto 8000 libre en el equipo
- (Opcional) Git, si se clona desde un repositorio

------------------------------------------------------------
2) Estructura esperada
------------------------------------------------------------
La carpeta entregada debe llamarse:
videogames_app/
│
├─ dynamic_pages/        -> Páginas dinámicas
├─ static_pages/         -> Páginas estáticas
├─ videogames_api/       -> API REST (videojuegos)
├─ videogames_app/       -> Configuración principal de Django
├─ Dockerfile
├─ manage.py
├─ README.txt
├─ requirements.txt

NOTA:
- Este proyecto usa MongoDB Atlas (cloud).
- La conexión a la base de datos ya esta configurada en el codigo fuente.

------------------------------------------------------------
3) Levantar el proyecto con Docker
------------------------------------------------------------
Abra una terminal dentro de la carpeta "videogames_app" y ejecute:

1) Generar imagen del proyecto en Docker
    docker build -t videogames_app:v1 .

2) Generar el contenedor
    docker run -d -p 8000:8000 --name videogames_app videogames_app:v1
    
    NOTA:
    - Si desea trabajar la aplicación en otro puerto en el comando anterior 
    cambiar el puerto de la izquierda por el de su preferencia.

3) Validar en un navegador
    En el navegador acceder a la URL:http://localhost:8000//dynamic-pages/home

------------------------------------------------------------
4) Probar la API (Endpoints)
------------------------------------------------------------
NOTA: Las rutas pueden variar según urls.py, pero normalmente se usan:

- Listar videojuegos (GET)
  http://localhost:8000/api/games/

- Listar con filtro por precio mínimo (GET)
  http://localhost:8000/api/games/?price_min=100000

- Crear videojuego (POST)
  http://localhost:8000/api/game/

Ejemplo de body JSON para POST:

{
  "name": "It Takes Two",
  "platform": "PS5",
  "release_year": 2021,
  "genre": "Adventure",
  "classification": "+12",
  "price": 150000
}

- Buscar un videojuego en particular (GET)
http://localhost:8000/api/game/697d393720ee563857f54d2d

- Eliminar un videojuego en concreto (DELETE)
http://localhost:8000/api/game/697d393720ee563857f54d2d

NOTA:
- Todos los endpoint los encuentra tambien en la pagina principal del aplicativo:
    http://localhost:8000//dynamic-pages/home
  Hay estan todas las tarjetas con las diferentes opciones a elegir.

============================================================
FIN
============================================================