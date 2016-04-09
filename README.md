# animeDown 0.1
Script en python para descargar series de underanime.net.

No estoy afiliado con esa página, en ninguna forma, el uso de este script es solo para fines educativos.
Aún le queda mucho camino, esto es una prueba de concepto.

Este programa usa las dependencias:

lxml, mega.py, urldecode, requests

Podéis instalarlas con pip install.

#Uso

animeDown.py url_de_la_serie directorio_de_descarga

El script busca por la página, y crea un directorio con el nombre de la serie en la carpeta especificada, donde descarga los capítulos.

#Pendiente

* Añadir soporte para más páginas de descarga.
* Optimizar la librería para descargar de Mega.nz (quizás crear un módulo desde 0).
* Descargas paralelas.
* Soporte de búsqueda.
* Guardar configuración.
* Quizás una GUI, plug-ins y más cosillas...

