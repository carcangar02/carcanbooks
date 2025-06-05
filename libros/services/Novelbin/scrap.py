import cloudscraper
from bs4 import BeautifulSoup



def scrap_capitulo(enlace):
    pass










def scrap_libro_details(libro):
    titulo = libro.titulo
    titulo_enlace = titulo.strip().replace(" ", "-").lower()
    enlace = f"https://novelbin.com/b/{titulo_enlace}/"
    enlace_capitulos = f"https://novelbin.com/ajax/chapter-archive?novelId={titulo_enlace}"

    scraper = cloudscraper.create_scraper()
    response = scraper.get(enlace)

    scraper_capitulos = cloudscraper.create_scraper()
    response_capitulos = scraper_capitulos.get(enlace_capitulos)

    # Comprobar que la petición fue exitosa
    if response.status_code == 200:
        # Parsear el HTML con BeautifulSoup
        main = BeautifulSoup(response.text, 'html.parser')
        imagen = main.find('img', class_='lazy')
        titulo = main.find('h3', class_='title')


    if response_capitulos.status_code == 200:
        main = BeautifulSoup(response_capitulos.text, 'html.parser')
        capitulos_lista = main.find_all('a')
        capitulos_array = []
        for cap in capitulos_lista:
            capitulos_array.append({
                'title': cap.text.strip(),
                'href': cap['href']
            })

    info_libro = {
        'titulo': titulo.text,
        'foto': imagen['data-src'],
        'capitulos': capitulos_array
    }
    return info_libro ## OUT    info_libro{titulo, foto, capitulos[{title, href}] }










def scrap_busqueda(input):
    pass