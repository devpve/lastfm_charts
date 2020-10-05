# -*- coding: utf-8 -*-
# Lastfm Charts por @pveres
# Tasks
# - Add date range
# - Add individual .csv
import json
import requests
import sys
import shutil
import os
import csv
from date_convert import *
from lastfm_classes import *

# Constants
debug = False
log_individual = False
log_format = '2'
api_key = "f077aaf6db0522a7dd16a289d54f02f0"
original_stdout = sys.stdout # reference to the standard output

# Display simple menu
if not debug:
	print("LASTFM.CHARTS by @paulovgf on GitHub")
	option = input("MENU\n 1 - Weekly chart\n 2 - Individual chart\n 3 - Register new user\n 4 - Remove user\n")

	if option == "1":
		
		log = input("Individual logs attached? [Y/n]")
		
		if log == "Y" or log == "y":
			log_individual = True
			log_format = input("Log format\n 1 - txt\n 2 - csv")


		filename = input("Please input the usernames filename: ")
		with open(filename) as f:
			usernames = [line.rstrip('\n') for line in f]

		start = input("Please inform the start date (YYYY-MM-DD-HH-MM): ")
		date_start = convert_date(start)
		end = input("Please inform the end date (YYYY-MM-DD-HH-MM): ")
		date_end = convert_date(end)
		

else: 
	usernames = ["pvepve", "caiino"]

	start = "2020-09-13-00-00"
	date_start = convert_date("2020-09-13-00-00")
	end = "2020-09-20-23-59"
	date_end = convert_date("2020-09-20-23-59")


track_list = TrackList()
album_list = AlbumList()
artist_list = ArtistList()


for user in usernames:

	# se log individual estiver ativo
	if log_individual:
		StringIndividual = "Log individual de " + user + "\n"

		if log_format == '2':
			with open('Resultados/musicas/' + user + '_' + start + '_' + end + '.csv', 'w', newline='') as f:
				fieldnames = ['Música', 'Artista', 'Scrobbles']
				thewriter = csv.DictWriter(f, fieldnames = fieldnames)
				thewriter.writeheader()


	# #-------------------------------------------------------------	---------------------
	#  Pegar faixas da semana do usuário
	url_weekly_tracks = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklytrackchart&user=" + user + "&from=" + date_start + "&to=" + date_end + "&api_key="+ api_key+ "&format=json"
	user_weekly_tracks = requests.get(url_weekly_tracks)
	if (user_weekly_tracks.status_code != 200):
		print("Erro filha")
		break

	# register user tracks
	user_weekly_tracks = user_weekly_tracks.json()
	user_weekly_tracks = user_weekly_tracks['weeklytrackchart']['track']
	
	if log_individual:
		StringIndividual += "Top Músicas \n"
		i = 1
	# weekly tracks
	for track in user_weekly_tracks:
		track_artist = track['artist']['#text']
		track_name = track['name']
		track_playcount = int(track['playcount'])

		if log_individual:
			StringIndividual += str(i) + ": " + track_name + " by " + track_artist + ": " + str(track_playcount) + "\n"
			i += 1

			if log_format == '2':
				with open('Resultados/musicas/' + user + '_' + start + '_' + end + '.csv', 'a', newline='') as f:
					fieldnames = ['Música', 'Artista', 'Scrobbles']
					thewriter = csv.DictWriter(f, fieldnames = fieldnames)
					thewriter.writerow({
						'Música': track_name,
						'Artista': track_artist,
						'Scrobbles': str(track_playcount),
					}
					)

		found_track = track_list.find(track_artist, track_name)
		if found_track:
			found_track.playcount += track_playcount
			found_track.ouvintes.append(user)
		else:
			track_list.track_list.append(Track(track_name, track_artist, track_playcount, [user]))

	# #----------------------------------------------------------------------------------
	# # weekly artists
	url_weekly_artists = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyartistchart&user=" + user + "&from=" + date_start + "&to=" + date_end + "&api_key="+ api_key+ "&format=json"
	user_weekly_artists = requests.get(url_weekly_artists)
	if (user_weekly_artists.status_code != 200):
		print("Erro filha")
		break

	# register user tracks
	user_weekly_artists = user_weekly_artists.json()
	user_weekly_artists = user_weekly_artists['weeklyartistchart']['artist']

	if log_individual:
		StringIndividual += "\n Top Artistas \n"
		i = 1

		if log_format == '2':
			with open('Resultados/artistas/' + user + '_' + start + '_' + end + '.csv', 'w', newline='') as f:
				fieldnames = ['Artista', 'Scrobbles']
				thewriter = csv.DictWriter(f, fieldnames = fieldnames)
				thewriter.writeheader()


	# weekly artists
	for artist in user_weekly_artists:
		artist_name = artist['name']
		artist_playcount = int(artist['playcount'])

		if log_individual:
			StringIndividual += str(i) + ": " + artist_name + ": " + str(artist_playcount) + "\n"
			i += 1

			if log_format == '2':
				with open('Resultados/artistas/' + user + '_' + start + '_' + end + '.csv', 'a', newline='') as f:
					fieldnames = ['Artista', 'Scrobbles']
					thewriter = csv.DictWriter(f, fieldnames = fieldnames)
					thewriter.writerow({
						'Artista': artist_name,
						'Scrobbles': str(artist_playcount),
					}
					)

		found_artist = artist_list.find(artist_name)

		if found_artist:
			found_artist.playcount += artist_playcount
			found_artist.ouvintes.append(user)
		else:
			artist_list.artist_list.append(Artist(artist_name, artist_playcount, [user]))

	# #----------------------------------------------------------------------------------
	# # weekly albums
	url_weekly_albums = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyalbumchart&user=" + user + "&from=" + date_start + "&to=" + date_end + "&api_key="+ api_key+ "&format=json"
	user_weekly_albums = requests.get(url_weekly_albums)
	if (user_weekly_albums.status_code != 200):
		print("Erro filha")
		break

	# register user tracks
	user_weekly_albums = user_weekly_albums.json()
	user_weekly_albums = user_weekly_albums['weeklyalbumchart']['album']

	if log_individual:
		StringIndividual += "\n Top Álbuns \n"
		i = 1

		if log_format == '2':
			with open('Resultados/albuns/' + user + '_' + start + '_' + end + '.csv', 'w', newline='') as f:
				fieldnames = ['Álbum', 'Artista', 'Scrobbles']
				thewriter = csv.DictWriter(f, fieldnames = fieldnames)
				thewriter.writeheader()

	# weekly albums
	for album in user_weekly_albums:
		album_name = album['name']
		album_artist = album['artist']['#text']
		album_playcount = int(album['playcount'])

		if log_individual:
			StringIndividual += str(i) + ": " + album_name + " by " + album_artist + ": " + str(album_playcount) + "\n"
			i += 1

			if log_format == '2':
				with open('Resultados/albuns/' + user + '_' + start + '_' + end + '.csv', 'a', newline='') as f:
					fieldnames = ['Álbum', 'Artista', 'Scrobbles']
					thewriter = csv.DictWriter(f, fieldnames = fieldnames)
					thewriter.writerow({
						'Álbum': album_name,
						'Artista': album_artist,
						'Scrobbles': str(album_playcount),
					}
					)

		found_album = album_list.find(album_artist, album_name)
		if found_album:
			found_album.playcount += album_playcount
			found_album.ouvintes.append(user)
		else:
			album_list.album_list.append(Album(album_name, album_artist, album_playcount, [user]))

	if log_individual and log_format == '1':
		with open('Resultados/' + user + '_' + start + '_' + end + '.txt', 'w') as f:
			sys.stdout = f # Change the standard output to the file we created.
			print(StringIndividual)
			sys.stdout = original_stdout # Reset the standard output to its original value



track_list.track_list.sort(key = lambda track: track.playcount, reverse = True)
artist_list.artist_list.sort(key = lambda artist: artist.playcount, reverse = True)
album_list.album_list.sort(key = lambda album: album.playcount, reverse = True)

# shutil.rmtree("Resultados")

# os.mkdir("/home/pv/Documents/Python/Lastfm Charts/Resultados")
# os.mkdir("/home/pv/Documents/Python/Lastfm Charts/Resultados/musicas")
# os.mkdir("/home/pv/Documents/Python/Lastfm Charts/Resultados/artistas")
# os.mkdir("/home/pv/Documents/Python/Lastfm Charts/Resultados/albuns")

# Escrevendo no csv
with open('Resultados/musicas/0_musicas_' + start + '_' + end + '.csv', 'w', newline='') as f:
	fieldnames = ['Nome', 'Artista', 'Scrobbles', 'Ouvintes', 'Quem Ouviu']
	thewriter = csv.DictWriter(f, fieldnames = fieldnames)
	thewriter.writeheader()

	for track in track_list.track_list:
		thewriter.writerow({
			'Nome': track.name, 
			'Artista': track.artist, 
			'Scrobbles': str(track.playcount),
			'Ouvintes': str(len(track.ouvintes)),
			'Quem Ouviu': str(track.ouvintes)
		}
		)



# Escrevendo no csv
with open('Resultados/artistas/0_artistas_' + start + '_' + end + '.csv', 'w', newline='') as f:
	fieldnames = ['Artista', 'Scrobbles', 'Ouvintes', 'Quem Ouviu']
	thewriter = csv.DictWriter(f, fieldnames = fieldnames)
	thewriter.writeheader()

	for artist in artist_list.artist_list:
		thewriter.writerow({
			'Artista': artist.name, 
			'Scrobbles': str(artist.playcount),
			'Ouvintes': str(len(artist.ouvintes)),
			'Quem Ouviu': str(artist.ouvintes)
		}
		)



# Escrevendo no csv
with open('Resultados/albuns/0_albuns_' + start + '_' + end + '.csv', 'w', newline='') as f:
	fieldnames = ['Album', 'Artista', 'Scrobbles', 'Ouvintes', 'Quem Ouviu']
	thewriter = csv.DictWriter(f, fieldnames = fieldnames)
	thewriter.writeheader()

	for album in album_list.album_list:
		thewriter.writerow({
			'Album': album.name, 
			'Artista': album.artist,
			'Scrobbles': str(album.playcount),
			'Ouvintes': str(len(album.ouvintes)),
			'Quem Ouviu': str(album.ouvintes)
		}
		)
