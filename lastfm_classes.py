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