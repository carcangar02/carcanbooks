from django.shortcuts import render
from django.http import JsonResponse
from .models import Libreria, Libro
import importlib
import json

def librerias_menu(request):
    librerias = Libreria.objects.values('pk', 'nombre')

    info_libros = []
    libros_qs = Libro.objects.all()

    # Si hay una librería seleccionada, filtra por ella



    for libro in libros_qs:
        try:
            extension_scrap = importlib.import_module(f'libros.services.{libro.extension.nombre}.scrap')
            libro_scrapped = extension_scrap.scrap_libro_details(libro)
            info_libros.append({
                'id': libro.id,
                'titulo': libro.titulo,
                'foto': libro_scrapped['foto'],
                'libreria': libro.libreria_id
            })
        except Exception as e:
            print(e)

    context = {
        'librerias': list(librerias),
        'info_libros': json.dumps(info_libros),
    }
    return render(request, 'libros/librerias_menu.html', context)


