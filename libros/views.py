from django.shortcuts import render
from django.http import JsonResponse
from .models import Libreria, Libro
import importlib

def librerias_menu(request):
    librerias = Libreria.objects.values('pk', 'nombre')
    libreria_seleccionada = request.GET.get('libreria')  # id seleccionada desde el GET

    info_libros = []
    libros_qs = Libro.objects.filter(libreria_id=1)

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
        'librerias': librerias,
        'info_libros': info_libros,
        'libreria_seleccionada': libreria_seleccionada,
    }
    return render(request, 'libros/librerias_menu.html', context)

def cargar_libros_por_libreria(request):
    libreria_id = request.GET.get('libreria_id')
    libros_qs = Libro.objects.filter(libreria_id=libreria_id)

    info_libros = []
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

    return JsonResponse(info_libros, safe=False)
