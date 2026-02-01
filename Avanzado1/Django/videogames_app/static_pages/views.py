from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(_):
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>🎮 VideoGames Catalog</title>
        <style>
            body {
                font-family: Arial, Helvetica, sans-serif;
                margin: 0;
                background: #0f172a;
                color: #e5e7eb;
            }
            header {
                background: #020617;
                padding: 20px;
                text-align: center;
            }
            nav a {
                margin: 0 15px;
                color: #38bdf8;
                text-decoration: none;
                font-weight: bold;
            }
            nav a:hover {
                text-decoration: underline;
            }
            .container {
                max-width: 900px;
                margin: 40px auto;
                background: #020617;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(0,0,0,.4);
            }
            ul li {
                margin-bottom: 8px;
            }
            footer {
                text-align: center;
                margin-top: 40px;
                color: #94a3b8;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>🎮 VideoGames Catalog</h1>
            <nav>
                <a href="/dynamic-pages/home">Home</a>
                <a href="/static-pages/about/">About</a>
                <a href="/static-pages/contact/">Contact</a>
            </nav>
        </header>

        <div class="container">
            <h2>Bienvenido 👋</h2>
            <p>Esta es una página <strong>estática</strong> creada directamente desde una vista Django.</p>

            <h3>Características</h3>
            <ul>
                <li>✅ HTML embebido en Python</li>
                <li>✅ No usa base de datos</li>
                <li>✅ Ideal para landing pages</li>
                <li>✅ Respuesta rápida</li>
            </ul>

            <p><em>Perfecta para aprender cómo Django sirve contenido sin templates.</em></p>
        </div>

        <footer>
            © 2026 · Django Static Pages Demo
        </footer>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def about(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>ℹ️ About</title>
        <style>
            body {
                font-family: Arial, Helvetica, sans-serif;
                margin: 0;
                background: #020617;
                color: #e5e7eb;
            }
            .container {
                max-width: 800px;
                margin: 60px auto;
                background: #020617;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(0,0,0,.4);
            }
            a {
                color: #38bdf8;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ℹ️ Acerca del Proyecto</h1>
            <p>Este proyecto demuestra cómo Django puede servir contenido estático sin usar templates.</p>

            <h3>Detalles técnicos</h3>
            <ul>
                <li>HTML definido en <code>views.py</code></li>
                <li>No usa base de datos</li>
                <li>No usa archivos HTML externos</li>
                <li>Ideal para ejemplos educativos</li>
            </ul>

            <p>
                <a href="/static-pages/home">← Volver al Home</a>
            </p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)
