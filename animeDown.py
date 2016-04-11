#!/usr/bin/python
# -*- coding: utf-8 -*-
from mega import Mega
from lxml import html
from url_decode import urldecode
import sys, os, requests, urllib, Tkinter, tkFileDialog

#version to display
version = 'animeDown v0.4.1 alpha by Shakku\n'

class Episode:
	def __init__(self, name, num, url):
		self.name = name
		self.num = num
		self.url = url

class Anime:
	def __init__(self, name, url, num):
		self.name = name
		self.url = url
		self.num = num

#checks arguments and displays usage
def CheckArgs(args):
	if len(args) != 3:
		print version
		print 'Uso: ' + args[0] + '  Link Dirección de la carpeta'
		sys.exit(1)
	return

def Clear():
	if os.name == "posix":
		os.system('clear')
	else:
		os.system('cls')
	return

#http request
def GetUrl(Url):
	try:
		page = requests.get(Url)
	except:
		print '[!] Error! No se pudo conectar!'
		sys.exit(1)
	page = html.fromstring(page.content)
	return page

#checks directory
def CheckDir(Dir):
	if not os.path.exists(Dir):
		print '[!] Comprueba la carpeta!'
		sys.exit(1)
	return

#gets the name of the anime
def GetTitle(url):
	page = GetUrl(url)
	title = page.xpath('//*[@id="hen-info"]/div/div/div[1]/div/div/h3/text()')
	return title[0]

#function to get all links from the page and return an object list
def GetEpisodes(url):
	page = GetUrl(url)
	#Get all the raw links and episode names and put them on a list.
	rawLinks = page.xpath('//*[@id="holder-nav"]/li/a/@onclick')
	epNames = page.xpath('//*[@id="holder-nav"]/li/a/span/text()')

	#check links
	epNumber = len(rawLinks)
	if epNumber != len(epNames):
		print '[!] Error, faltan links en esta serie!'
		sys.exit(1)

	#Create the episodes list
	episodes = []

	#Iterate through results and extract links
	for n in range(0, epNumber):
		cutLinks = rawLinks[n].split("'")
		link = cutLinks[1] + urldecode(cutLinks[3])

		#Create episode object, set attributes and append to episodes list
		episode = Episode(epNames[n], n + 1, link)
		episodes.append(episode)
	return episodes

def SearchEngine(search):
	searchUrl = 'https://www.underanime.net/?s='
	search = urllib.quote(search)
	page = GetUrl(searchUrl + search)
	animeLinks = page.xpath('//*/div/div/div/div[@class="base_inner h255 loading"]/a/@href')
	animeNames = page.xpath('//*/div/div/div/div[@class="base_inner h255 loading"]/a/@title')
	
	#check links, todo better
	linkNum = len(animeLinks)
	if linkNum != len(animeNames):
		print '[!] Error, links ausentes!'
		sys.exit(1)

	#create anime list
	animeList = []

	for n in range(0, linkNum):
		anime = Anime(animeNames[n], animeLinks[n], n)
		animeList.append(anime)
	return animeList

def SearchInput():
	while True:
		Clear()
		print version
		search = raw_input('Introduce tu busqueda: ')
		result = SearchEngine(search)
		if result != []:
			return result
		else:
			print '[!] No se encontro nada. Presiona enter para volver a buscar.'
			raw_input()

def DisplayResult(results):
	while True:
		Clear()
		print version
		print 'Selecciona el anime que deseas descargar:'
		for result in results:
			n = str(result.num)
			print '[' + n + '] ' + result.name
		choice = raw_input('\nIntroduce un numero: ')
		if choice.isdigit():
			choice = int(choice)
			if choice >= len(results):
				print '[!] Error! Introduce un numero dentro del rango.'
				raw_input()
			else:
				return choice
		else:
			print '[!] Error! Introduce un numero!'
			raw_input()
		


#main function
def main():
	#display search menu
	result = SearchInput()

	#show found series
	choice = DisplayResult(result)

	#get title and episode objects
	title = GetTitle(result[choice].url)
	episodes = GetEpisodes(result[choice].url)
	numEpisodes = len(episodes)

	#create directory for saving anime

	w = Tkinter.Tk()
	w.withdraw()

	path = tkFileDialog.askdirectory()

	if not os.path.exists(path):
		print '[!] Error, quitting!'
		sys.exit(1)

	#Bugfix for naming folders on windows
	folderName = title.translate(None, '"<>:/\\|?*')

	#Creating the folder
	savePath = os.path.join(path, folderName)
	if not os.path.exists(savePath):
		os.mkdir(savePath)

	#create Mega downloader object
	mega = Mega({'verbose': True})

	#Starting download...
	Clear()
	print version
	print '[*] Descargando ' + title + ' en ' + savePath
	print '[*] ' + str(numEpisodes) + ' capitulos en cola...'

	#iterate through episodes list and download
	for episode in episodes:
		print '[*] Capitulo numero ' + str(episode.num) + ' descargando...'
		try:
			mega.download_url(episode.url, savePath)
		except:
			print '[!] Error! Saliendo!'
			exit(1)
		print '[*] Capitulo ' + str(episode.num) + ' descargado!'
	return

	#Finish and exit if no errors
	print '[*] Descarga terminada! Presiona enter para salir.'
	raw_input()
	sys.exit(0)

main()


