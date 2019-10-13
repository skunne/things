#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup

def open_film(url_film):
	#page_film = urllib3.urlopen(url_alaffiche)
	#soup_film = BeautifulSoup(page_alaffiche, 'html.parser')
	#print(url_film)
	#soup_film = BeautifulSoup(page_film, 'html.parser')
	#print(page_film)
	with urllib.request.urlopen(url_film) as response:
		try:
			page_film = response.read().decode('utf-8')
			if (page_film.find('Chine') != -1 or page_film.find('Hong Kong') != -1 or page_film.find('Singapour') != -1):
				print(url_film)
		except UnicodeDecodeError:
			print('Probleme d encodage: ' + url_film)


def get_nombre_de_pages(soup):
	divs = soup.find_all('div')
	for div in divs:
		if ('class' in div.attrs) and (div['class'] == 'dayNav'):
			select = div.find('select')
			options = select.find_all('option')
			nombre_de_pages = 1
			for option in options:
				nombre_de_pages = max(nombre_de_pages, int(option['value']))
			return(nombre_de_pages)
	default_nb_pages = 50
	print('Erreur lors du calcul du nombre de pages. La valeur '+str(default_nb_pages)+' a ete utilisee par defaut.')
	return(default_nb_pages)

def open_alaffiche_unepage(url_alaffiche):
	with urllib.request.urlopen(url_alaffiche) as response:
		page_alaffiche = response.read()
	soup_alaffiche = BeautifulSoup(page_alaffiche, 'html.parser')
	films = soup_alaffiche.find_all('div')
	for film in films:
		if ('itemtype' in film.attrs) and (film['itemtype'] == "http://schema.org/Movie"):
			blockurl_film = film.a
			url_film = blockurl_film['href']
			url_film = 'https://www.offi.fr' + url_film
			open_film(url_film)
	return(soup_alaffiche)

def open_alaffiche():
	url_alaffiche = 'http://www.offi.fr/cinema/a-laffiche.html?npage='
	soup = open_alaffiche_unepage(url_alaffiche + '1')
	nombre_de_pages = get_nombre_de_pages(soup)
	for npage in range(2, nombre_de_pages):
		print(npage)
		open_alaffiche_unepage(url_alaffiche + str(npage))

open_alaffiche()
