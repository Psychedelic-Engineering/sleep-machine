
import soundcloud

class SCloud:
	def __init__(self):
		self.client = soundcloud.Client(
			client_id="19235142ccf477578ca8804cc52c1301",
			client_secret="27c6d4b04bbc78ba4c320895419d8895",
			username="zorkmeister",
			password="zorkmeister"
		)

	def getPlaylists(self):
		return self.client.get('/users/zorkmeister/playlists')

	def getPlaylist(self, pl_id):
		#return ("https://ia600402.us.archive.org/27/items/Thunder_849/Thunderstorm1.mp3",)
		#return ('file:///home/pi/music/Thunderstorm1.mp3',)
		#return ("https://ia600400.us.archive.org/22/items/IcyRain/RAIN002editEQ.m4a",)
		playlist = self.client.get('/users/zorkmeister/playlists/%s' % pl_id)
		tracks = []

		for t in playlist.tracks:
			track = self.client.get('/tracks/%s' % t['id'])
			stream_url = self.client.get(track.stream_url, allow_redirects=False)

			tracks.append(stream_url.location)
		return tracks