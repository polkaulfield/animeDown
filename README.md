# animeDown 0.4 Alpha
Programa en python para descargar series de underanime.net.

No estoy afiliado con esa página, en ninguna forma, el uso de este script es solo para fines educativos.
Aún le queda mucho camino, esto es una prueba de concepto.
El script busca por la página, y crea un directorio con el nombre de la serie en la carpeta especificada, donde descarga los capítulos.

#Uso
Los usuarios de windows podéis usar el el script o el ejecutable ya precompilado con pyinstaller, que no necesita dependencias. Los usuarios de Linux, BSD y OSX os toca bajar las dependencias :)

Este programa usa las dependencias:
* lxml
* mega.py
* urldecode
* requests
* tk

Podéis instalarlas con pip install.
En Ubuntu si tira error, instalad la libreria tk con el comando: 
sudo apt-get install python-tk

#Changelog
0.4 Algunos bugs arreglados.
0.3 Añadido sistema de búsquedas y GUI para seleccionar la carpeta de descargas, algunos bugs arreglados.

#Pendiente

* Añadir soporte para más páginas de descarga.
* Optimizar la librería para descargar de Mega.nz (quizás crear un módulo desde 0).
* Descargas paralelas.
* Soporte de búsqueda.
* Guardar configuración.
* Quizás una GUI, plug-ins y más cosillas...

