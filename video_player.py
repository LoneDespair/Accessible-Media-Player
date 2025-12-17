from kivymd.app import MDApp
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.window import Window
from kivy.clock import Clock
from expression_detector import ExpressionDetector

class AccessibleVideoPlayer(MDApp):
	title = "Group 7: Accessible Video Player"

	# Changes the buttons' appearance 
	def change_buttons(self):
		self.player.image_volumehigh = "assets/volume_high.png"
		self.player.image_volumemedium = "assets/volume_low.png"
		self.player.image_volumelow = "assets/volume_low.png"
		self.player.image_volumemuted = "assets/volume_muted.png"
		self.player.image_play = "assets/play.png"
		self.player.image_pause = "assets/pause.png"
		self.player.image_stop = "assets/stop.png"

	# Setup the window and video player
	def build(self):
		self.detector = ExpressionDetector()
		self.theme_cls.theme_style = "Dark"
		self.icon = "assets/icon.png"
		self.auto_control = True

		self.player = VideoPlayer(state="play", options={"fit_mode": "contain"})
		self.change_buttons()
		self.player.volume = 0.5

		Window.bind(on_dropfile=lambda _, filename:
			setattr(self.player, "source", filename.decode("utf-8"))
		)
		
		Clock.schedule_interval(self.player_control, 1 / 10)
		return self.player

	# Video player controls using face expressions
	def player_control(self, _):
		if self.detector.update_frame() is None:
			return

		if self.detector.mouth_open():
			self.auto_control = not self.auto_control

			if self.player.state == "play":
				self.player.state = "pause"
			elif self.player.state == "pause":
				self.player.state = "play"

		if self.auto_control:
			if self.detector.detect_face():
				self.player.state = "play"
			else:
				self.player.state = "pause"

		if self.detector.head_tilt() == "Left":
			self.player.volume = max(0, self.player.volume - 0.02)
		elif self.detector.head_tilt() == "Right":
			self.player.volume = min(self.player.volume + 0.02, 100)

		if self.detector.head_tilt() == "Center":
			percentage = self.player.position / self.player.duration
			if self.detector.head_dir() == "Left":
				self.player.seek(percentage - 0.01)
			elif self.detector.head_dir() == "Right":
				self.player.seek(percentage + 0.01)

AccessibleVideoPlayer().run()
