#!/usr/bin/python
# -*- coding: utf-8 -*-
from mega import Mega
from lxml import html
from url_decode import urldecode
import sys, os, requests


class Episode:
	def __init__(self, name, num, url):
		self.name = name
		self.num = num
		self.url = url

def CheckArgs(args):
	if len(args) != 3:
		print 'UnderAnime Downloader v0.1 by Shakku\n'
		print 'Uso: ' + args[0] + '  Link Dirección de la carpeta'
		sys.exit(1)
	return

def GetUrl(Url):
	try:
		page = requests.get(Url)
	except:
		print 'Comprueba el link!'
		sys.exit(1)
	return page

def CheckDir(Dir):
	if not os.path.exists(Dir):
		print 'Comprueba la carpeta!'
		sys.exit(1)
	return

def GetTitle(page):
	title = page.xpath('//*[@id="hen-info"]/div/div/div[1]/div/div/h3/text()')
	return title[0]

def GetEpisodes(page):
	#Get all the raw links and episode names and put them on a list.
	rawLinks = page.xpath('//*[@id="holder-nav"]/li/a/@onclick')
	epNames = page.xpath('//*[@id="holder-nav"]/li/a/span/text()')

	#check links
	epNumber = len(rawLinks)
	if epNumber != len(epNames):
		print 'Error, faltan links en esta serie!'
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

def main():
	CheckArgs(sys.argv)
	url = sys.argv[1]
	path = sys.argv[2]

	#Get page
	page = GetUrl(url)
	page = html.fromstring(page.content)

	#get title and episode objects
	title = GetTitle(page)
	episodes = GetEpisodes(page)
	numEpisodes = len(episodes)

	#create directory for saving anime
	savePath = os.path.join(path, title)
	if not os.path.exists(savePath):
		os.mkdir(savePath)

	#create Mega downloader object
	mega = Mega()

	#Starting download...
	print 'UnderAnime Downloader v0.1 by Shakku\n'
	print '[*] Descargando ' + title + ' en ' + savePath
	print '[*] ' + str(numEpisodes) + ' capítulos en cola...'

	#iterate through episodes list and download
	for episode in episodes:
		print '[*] Capítulo número ' + str(episode.num) + ' descargando...'
		try:
			mega.download_url(episode.url, savePath)
		except:
			print '[!] Error! Saliendo!'
			exit(1)
		print '[*] Capítulo ' + str(episode.num) + ' descargado!'
	return

	#Finish and exit if no errors
	print '[*] Descarga terminada!'
	sys.exit(0)

main()

	



