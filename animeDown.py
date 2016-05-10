#!/usr/bin/python
# -*- coding: utf-8 -*-
from mega import Mega
from lxml import html
from url_decode import urldecode
import sys, os, requests, urllib, Tkinter, tkFileDialog, codecs

#version to display
version = 'animeDown v0.5.1 alpha by Shakku\n'

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
		print "[!] Error! Can't connect!"
		return False
	page = html.fromstring(page.content)
	return page

#function to get all links from the page and return an object list
def GetEpisodes(url):
	page = GetUrl(url)
	#Get all the raw links and episode names and put them on a list.
	rawLinks = page.xpath('//*[@id="holder-nav"]/li/a/@onclick')
	epNames = page.xpath('//*[@id="holder-nav"]/li/a/span/text()')

	#check links
	epNumber = len(rawLinks)
	if epNumber != len(epNames):
		print '[!] Error, links missing!'
		return False

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
		print '[!] Error, some links missing!'
		return False

	#create anime list
	animeList = []

	for n in range(0, linkNum):
		anime = Anime(animeNames[n].encode(sys.stdout.encoding, errors='replace'), animeLinks[n], n)
		animeList.append(anime)
	return animeList

def SearchInput():
	while True:
		Clear()
		print version
		search = raw_input('Input your search: ')
		result = SearchEngine(search)
		if result != []:
			return result
		else:
			print '[!] Nothing found. Press enter to try again.'
			raw_input()

def DisplayResult(results):
	while True:
		Clear()
		print version
		print 'Check the anime you want to download: '
		for result in results:
			n = str(result.num)
			print '[' + n + '] ' + result.name
		choice = raw_input('\nIntroduce a number: ')
		if choice.isdigit():
			choice = int(choice)
			if choice >= len(results):
				print '[!] Error! Input a number that is on the list.'
				raw_input()
			else:
				return choice
		else:
			print '[!] Error! Input a number!'
			raw_input()
		


#main function
def main():
	#display search menu
	result = SearchInput()

	#show found series
	choice = DisplayResult(result)

	#get title and episode objects
	title = result[choice].name
	episodes = GetEpisodes(result[choice].url)
	numEpisodes = len(episodes)

	#create directory for saving anime

	w = Tkinter.Tk()
	w.withdraw()

	path = tkFileDialog.askdirectory()

	if not os.path.exists(path):
		print '[!] Error, quitting!'
		return

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
	print '[*] Downloading ' + title + ' in ' + savePath
	print '[*] ' + str(numEpisodes) + ' episodes waiting for download...'

	#iterate through episodes list and download
	count = 0
	for episode in episodes:
		print '[*] Episode number ' + str(episode.num) + ' downloading...'
		try:
			mega.download_url(episode.url, savePath)
			print '[*] Episode ' + str(episode.num) + ' downloaded!'
			count = count + 1
		except:
			print '[!] Error! Could not download! Skipping!'

	#Finish and exit if no errors
	print '[*] ' + str(count) + ' chapters downloaded successfully!'
	raw_input()
	return


if __name__ == "__main__":
        while True:
                main()

