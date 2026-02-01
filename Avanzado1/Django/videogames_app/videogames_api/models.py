from django.db import models
from datetime import datetime
from mongoengine import Document, StringField, IntField,DateTimeField
# Create your models here.

class VideoGame(Document):
    nombre = StringField(max_length=200, required= True)
    plataforma = StringField(max_length=50, required=True)
    fecha = IntField(min_value=1950, max_value=2100, required=True)
    genero = StringField(max_length=50, required=True)
    clasificacion = StringField(max_length=10, required=True)
    precio = IntField(min_value=1, required=True)
    creation_date = DateTimeField(default=datetime.now)
    author = StringField(max_length=20)
    
    meta = {
        'collection': "videogames",
        'ordering': ['-creation_date']
    }
    
    def as_dic(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "plataforma": self.plataforma,
            "fecha": self.fecha,
            "genero": self.genero,
            "clasificacion": self.clasificacion,
            "precio": self.precio
        }        
    
    def __str__(self):
        return f"{self.nombre} ({self.plataforma}, {self.fecha}) - {self.genero} - {self.clasificacion} - ${self.precio}"