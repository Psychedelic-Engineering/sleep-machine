from gstplayer import AudioPlayer
import time, logging, random
from scloud import SCloud

# Umbau zur Playlist Klasse
# Fade-In und Out in sec
# playlist-Suche nach Tag und NAme
# Max Playtime
# Playlistmanager klasse
# 	FindMatchingPlaylists(Mood/Activity)
# 	Next/PreviousPlaylist

class PlaylistSoundCloud:

	def __init__(self):
		self.volume = 0.0
		self.duration = 0.0
		self.startTime = 0
		self.sCloud = SCloud()
		self.playlists = self.sCloud.getPlaylists()
		self.player = AudioPlayer()
		self.player.onProgress = self.onProgress
		self.player.onFinish = self.onPlayerFinish
		self.playlist = []
		self.currentIndex = 0
		self.currentTrack = None
		self.playing = False

	def loadPlaylistByName(self, name):
		for pl in self.playlists:
			if pl.title == name:
				tracks = pl.tracks
				for track in tracks:
					self.playlist.append(track)

	def loadPlaylistByTags(self, taglist):
		for pl in self.playlists:
			if set(taglist).issubset( pl.tag_list.split(" ") ):
				tracks = pl.tracks
				for track in tracks:
					self.playlist.append(track)
			"""
			for tag in taglist:
				if tag in pl.tag_list:
					tracks = pl.tracks
					for track in tracks:
						self.playlist.append(track)
			"""

	def printPlaylist(self):
		print "Playlist:"
		for track in self.playlist:
			print "\t", track["title"]

	def clear(self):
		self.playlist = []
		print "STOP"

	def play(self):
		self.currentTrack = self.playlist[self.currentIndex]
		print "Playing: ", self.currentTrack["title"]
		stream_url = self.sCloud.client.get(self.currentTrack['stream_url'], allow_redirects=False)
		self.player.play(stream_url.location)
		self.playing = True

	def next(self):
		if self.currentIndex < (len(self.playlist)-1):
			self.player.stop()
			print "next: ", self.currentIndex, len(self.playlist)
			self.currentIndex += 1
			self.play()
		else:
			print "FINISHED"
			if self.onFinished:
				self.onFinished()

	def onProgress(self, prog):
		if self.volume <= 0.2:
			self.player.volume.set_property('volume', self.volume)
			self.volume += 0.01

	def onPlayerFinish(self):
		self.next()

	def stop(self):
		self.player.stop()
		self.playing = False

	def setVolume(self, volume):
		self.volume = volume
		self.player.volume.set_property('volume', self.volume)





"""
player.volume.set_property('volume', 0)
player.equalizer.set_property('band0', -20 )
player.equalizer.set_property('band1', -20 )
player.equalizer.set_property('band2', -20 )

for i in range(100):
    player.volume.set_property('volume', float(i)/100)
    time.sleep(0.1)
for i in range(-20,12):
    player.equalizer.set_property('band0', i )
    time.sleep(0.1)
for i in range(-20,12):
    player.equalizer.set_property('band1', i )
    time.sleep(0.1)
for i in range(-20,12):
    player.equalizer.set_property('band2', i )
    time.sleep(0.1)
"""

