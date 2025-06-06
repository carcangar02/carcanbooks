from django.shortcuts import render
from django.http import JsonResponse
from .models import Libreria, Libro, Capitulos
import importlib
import json

def librerias_menu(request):
    librerias = Libreria.objects.values('pk', 'nombre')

    info_libros = []
    libros_qs = Libro.objects.prefetch_related('capitulos').all()




    for libro in libros_qs:
        try:
            num_caps_db = len(libro.capitulos.all())

            extension_scrap = importlib.import_module(f'libros.services.{libro.extension.nombre}.scrap')
            libro_scrapped = extension_scrap.scrap_libro_details(libro)
            info_libros.append({
                'id': libro.id,
                'titulo': libro.titulo,
                'foto': libro_scrapped['foto'],
                'libreria': libro.libreria_id
            })
            num_caps_web = len(libro_scrapped['capitulos'])
            if num_caps_db != num_caps_web and num_caps_web > 0:
                diferencia = num_caps_web - num_caps_db
                for cap in libro_scrapped['capitulos'][-diferencia:]:
                    if 'href' in cap and 'title' in cap:
                        nuevo_capitulo = Capitulos(
                            enlace=cap['href'],
                            libro=libro,
                            titulo=cap['title'],
                            visto=False
                        )
                        nuevo_capitulo.save()
                    else:
                        print(f"Capítulo sin enlace o título en libro {libro.titulo} (ID {libro.id}): {cap}")




        except Exception as e:
            print(f"Error procesando el libro {libro.titulo} (ID {libro.id}): {e}")


    context = {
        'librerias': list(librerias),
        'info_libros': json.dumps(info_libros),
    }
    return render(request, 'libros/librerias_menu.html', context)










def libro_details(request, libro_id):
    try:
        librerias  = Libreria.objects.values('pk', 'nombre')
        if libro_id is not None:
            libro = Libro.objects.get(pk=libro_id)
            capitulos = libro.capitulos.all().values('id', 'titulo', 'enlace', 'visto')
            extension_scrap = importlib.import_module(f'libros.services.{libro.extension.nombre}.scrap')
            libro_scrapped = extension_scrap.scrap_libro_details(libro)

            info_libro = {
                'titulo': libro_scrapped['titulo'],
                'foto': libro_scrapped['foto'],
                'capitulos':libro_scrapped['capitulos'],
                'libreria': libro.libreria.nombre,
                'extension': libro.extension.nombre
            }

            context = {
                'librerias': list(librerias),
                'libro': info_libro,
                'capitulos': json.dumps(list(capitulos)),
            }


            return render(request, "libros/libro_details.html" , context)
        else:
            return JsonResponse({'error': 'No se proporcionó un ID de libro válido.'}, status=400)
    except Exception as e:
      pass








def lector(request, capitulo_id):
    try:
        capitulo = Capitulos.objects.get(pk=capitulo_id)
        extension_scrap = importlib.import_module(f'libros.services.{capitulo.libro.extension.nombre}.scrap')
        contenido_capitulo = extension_scrap.scrap_capitulo(capitulo.enlace)
        context = {
            'capitulo': capitulo,
            'contenido': contenido_capitulo,
        }
        return render(request, "libros/lector.html", context)
    except Capitulos.DoesNotExist:
        return JsonResponse({'error': 'Capítulo no encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)