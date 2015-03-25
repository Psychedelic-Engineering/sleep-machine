import sys, time, math
import gobject
gobject.threads_init()
import pygst
pygst.require('0.10')
import gst
from thread import start_new_thread


class AudioPlayer:
	def __init__(self):
		self.playing = False
		self.onProgress = None
		self.onStop = None
		# The pipeline
		self.pipeline = gst.Pipeline()
		# Create bus and connect several handlers
		#self.bus = self.pipeline.get_bus()
		#self.bus.add_signal_watch()
		#self.bus.enable_sync_message_emission()
		#self.bus.connect('message', self.on_message)
		#self.bus.connect('message::eos', self.on_eos)
		#self.bus.connect('message::tag', self.on_tag)
		#self.bus.connect('message::error', self.on_error)
		# Create elements
		self.srcdec     = gst.element_factory_make('uridecodebin')
		self.conv       = gst.element_factory_make('audioconvert')
		self.rsmpl      = gst.element_factory_make('audioresample')
		self.sink       = gst.element_factory_make('alsasink')
		self.queue      = gst.element_factory_make("queue", "queue")
		self.equalizer  = gst.element_factory_make("equalizer-3bands", "equalizer-3bands")
		self.panorama   = gst.element_factory_make("audiopanorama", "panorama")
		self.volume     = gst.element_factory_make("volume", "volume")
		# Connect handler for 'pad-added' signal
		self.srcdec.connect('pad-added', self.on_pad_added)
		self.pipeline.add(self.srcdec, self.conv, self.rsmpl, self.queue, self.equalizer, self.panorama, self.volume, self.sink)
		#gst.element_link_many(self.conv, self.rsmpl, self.queue, self.equalizer, self.panorama, self.volume, self.sink)
		gst.element_link_many(self.conv, self.volume, self.sink)
		self.apad = self.conv.get_pad('sink')
		self.progress = 0.0

	def on_pad_added(self, element, pad):
		caps = pad.get_caps()
		name = caps[0].get_name()
		if name == 'audio/x-raw-float' or name == 'audio/x-raw-int':
			if not self.apad.is_linked(): # Only link once
				pad.link(self.apad)

	def on_message(self, bus, msg):
		print 'on_message'

	def on_eos(self, bus, msg):
		print 'eos'
		self.pipeline.set_state(gst.STATE_NULL)

	def on_tag(self, bus, msg):
		taglist = msg.parse_tag()
		for key in taglist.keys():
			print '\t%s = %s' % (key, taglist[key])

	def on_error(self, bus, msg):
		error = msg.parse_error()
		print 'on_error:', error[1]
		self.mainloop.quit()

	def play(self, location):
		self.srcdec.set_property('uri', location)
		self.pipeline.set_state(gst.STATE_PLAYING)
		self.playing = True
		start_new_thread(self.onPlay, ())

	def stop(self):
		self.pipeline.set_state(gst.STATE_NULL)
		if self.onStop:
			self.onStop()
		self.playing = False

	def onPlay(self):
		while self.playing:
			if gst.STATE_VOID_PENDING in self.pipeline.get_state(gst.STATE_PLAYING):
				pos = self.pipeline.query_position(gst.FORMAT_TIME)
				dur = self.pipeline.query_duration(gst.FORMAT_TIME)
				self.progress = 1.0 * pos[0] / dur[0]
				if self.onProgress:
					self.onProgress(self.progress)
					#print "%d" % math.floor(100.0 * prog)
				time.sleep(0.1)
				if pos >= dur:
					self.stop()
					if self.onFinish:
						self.onFinish()
