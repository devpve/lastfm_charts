# -*- coding: utf-8 -*-
# Lastfm Charts por @pveres
# Tarefas
# - Adicionar range de datas
import json
import requests
import sys

# Constants
api_key = "f077aaf6db0522a7dd16a289d54f02f0"
original_stdout = sys.stdout # referencia para a saida padrao
debug = False
log_individual = True

# Classes 
class Track(object):
	def __init__(self, name, artist, playcount, ouvintes):
		self.name = name
		self.artist = artist
		self.playcount = playcount
		self.ouvintes = ouvintes

class TrackList(object):
	def __init__(self):
		self.track_list = []

	def find(self, track_artist, track_name):
		if self.track_list == []:
			return None
		else:
			for track in self.track_list:
				if track.artist == track_artist and track.name == track_name:
					return track

class Artist(object):
	def __init__(self, name, playcount, ouvintes):
		self.name = name
		self.playcount = playcount
		self.ouvintes = ouvintes

class ArtistList(object):
	def __init__(self):
		self.artist_list = []

	def find(self, artist_name):
		if self.artist_list == []:
			return None
		else:
			for artist in self.artist_list:
				if artist.name == artist_name:
					return artist

class Album(object):
	def __init__(self, name, artist, playcount, ouvintes):
		self.name = name
		self.artist = artist
		self.playcount = playcount
		self.ouvintes = ouvintes

class AlbumList(object):
	def __init__(self):
		self.album_list = []

	def find(self, album_artist, album_name):
		if self.album_list == []:
			return None
		else:
			for album in self.album_list:
				if album.artist == album_artist and album.name == album_name:
					return album

# Pegar usuários
FinalString = "\nUsuários Registrados:\n" 

if not debug:
	filename = input("Olá, me informe o arquivo com os usuários: ")
	with open(filename) as f:
		usernames = [line.rstrip('\n') for line in f]
	
	for user in usernames:
		FinalString += user + " "

else: 
	FinalString = "\nUsuários Registrados:\n" 
	usernames = ["pvepve", "caiino"]
	for user in usernames:
		FinalString += user + " " 


FinalString += "\n"

# Lista de faixas, álbuns e artistas da semana
track_list = TrackList()
album_list = AlbumList()
artist_list = ArtistList()

# Enquanto tiver usuários
for user in usernames:
	# se log individual estiver ativo
	if log_individual:
		StringIndividual = "Log individual de " + user + "\n"

	# #----------------------------------------------------------------------------------
	#  Pegar faixas da semana do usuário
	url_weekly_tracks = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklytrackchart&user=" + user + "&api_key="+ api_key+ "&format=json"
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

		found_track = track_list.find(track_artist, track_name)
		if found_track:
			found_track.playcount += track_playcount
			found_track.ouvintes.append(user)
		else:
			track_list.track_list.append(Track(track_name, track_artist, track_playcount, [user]))

	# #----------------------------------------------------------------------------------
	# # weekly artists
	url_weekly_artists = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyartistchart&user=" + user + "&api_key="+ api_key+ "&format=json"
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
	# weekly artists
	for artist in user_weekly_artists:
		artist_name = artist['name']
		artist_playcount = int(artist['playcount'])

		if log_individual:
			StringIndividual += str(i) + ": " + artist_name + ": " + str(artist_playcount) + "\n"
			i += 1

		found_artist = artist_list.find(artist_name)

		if found_artist:
			found_artist.playcount += artist_playcount
			found_artist.ouvintes.append(user)
		else:
			artist_list.artist_list.append(Artist(artist_name, artist_playcount, [user]))

	# #----------------------------------------------------------------------------------
	# # weekly albums
	url_weekly_albums = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyalbumchart&user=" + user + "&api_key="+ api_key+ "&format=json"
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

	# weekly albums
	for album in user_weekly_albums:
		album_name = album['name']
		album_artist = album['artist']['#text']
		album_playcount = int(album['playcount'])

		if log_individual:
			StringIndividual += str(i) + ": " + album_name + " by " + album_artist + ": " + str(album_playcount) + "\n"
			i += 1

		found_album = album_list.find(album_artist, album_name)
		if found_album:
			found_album.playcount += album_playcount
			found_album.ouvintes.append(user)
		else:
			album_list.album_list.append(Album(album_name, album_artist, album_playcount, [user]))

	if log_individual:
		with open(user + '_maisouvidas.txt', 'w') as f:
			sys.stdout = f # Change the standard output to the file we created.
			print(StringIndividual)
			sys.stdout = original_stdout # Reset the standard output to its original value




i = 1

FinalString += "\nTop 100 - Músicas\n"
track_list.track_list.sort(key = lambda track: track.playcount, reverse = True)

for track in track_list.track_list:   
	FinalString += str(i) + ": " + track.name + " by " + track.artist + ": " + str(track.playcount) + " | Ouvintes: " + str(len(track.ouvintes)) + "\n" + str(track.ouvintes) + "\n"
	i+=1
	if i > 100:
		break

i = 1
FinalString += "\nTop 100 - Artistas\n"
artist_list.artist_list.sort(key = lambda artist: artist.playcount, reverse = True)
for artist in artist_list.artist_list:
	FinalString += str(i) + ": " + artist.name + ": " + str(artist.playcount) + " | Ouvintes: " + str(len(artist.ouvintes)) + "\n" + str(artist.ouvintes) + "\n"
	i+=1
	if i > 100:
		break

i = 1
FinalString += "\nTop 100 - Álbuns\n"
album_list.album_list.sort(key = lambda album: album.playcount, reverse = True)
for album in album_list.album_list:
	FinalString += str(i) + ": " + album.name + " by " + album.artist + ": " + str(album.playcount) +" | Ouvintes: " + str(len(album.ouvintes)) + "\n" + str(album.ouvintes) + "\n" 
	i+=1
	if i > 100:
		break


with open('Top100.txt', 'w') as f:
	sys.stdout = f # Change the standard output to the file we created.
	print(FinalString)
	sys.stdout = original_stdout # Reset the standard output to its original value