from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(_):
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>📄 Mi Primera Página Django</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f0f8ff; }
            .container { max-width: 800px; margin: 0 auto; background: white; 
                        padding: 30px; border-radius: 10px; }
            nav a { margin-right: 15px; text-decoration: none; color: #007cba; }
        </style>
    </head>
    <body>
        <div class="container">
            <nav>
                <a href="/static-pages/">🏠 Home</a>
                <a href="/static-pages/about/">ℹ️ About</a>
                <a href="/static-pages/contact/">📧 Contact</a>
            </nav>
            
            <h1>🪑 ¡Bienvenido a Furniture Catalog!</h1>
            <p><strong>¿Qué es contenido estático?</strong></p>
            <ul>
                <li>✅ HTML completamente fijo</li>
                <li>✅ No consulta base de datos</li>
                <li>✅ Respuesta muy rápida</li>
                <li>✅ Ideal para landing pages</li>
            </ul>
            
            <p><em>Esta página está definida directamente en el código Python.</em></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def about(request):
    """Página About estática"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>📋 Acerca de</title>
        <style>body { font-family: Arial; margin: 40px; }</style>
    </head>
    <body>
        <h1>📋 Acerca del Catálogo de Muebles</h1>
        <p>Esta es una página estática creada con Django.</p>
        <p><strong>Características:</strong></p>
        <ul>
            <li>No usa base de datos</li>
            <li>HTML fijo definido en views.py</li>
            <li>Respuesta inmediata</li>
        </ul>
        <a href="/static-pages/home">← Volver al Home</a>
    </body>
    </html>
    """
    return HttpResponse(html_content)
