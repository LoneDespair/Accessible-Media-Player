import cv2
import mediapipe as mp
import math
import time

class ExpressionDetector:
	face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
	webcam = cv2.VideoCapture(0)
	wait_amt = 1.5

	def __init__(self):
		self.action = {
			"start": {
				"detect_face": time.time(),
				"head_tilt": time.time(),
				"head_dir": time.time(),
				"mouth_open": time.time(),
				"eyebrow_raise": time.time(),
				"left_wink": time.time(),
			},
			"dur": {
				"detect_face": 0,
				"head_tilt": 0,
				"head_dir": 0,
				"mouth_open": 0,
				"eyebrow_raise": 0,
				"left_wink": 0,
			},
			"prev": {
				"head_tilt": "Center",
				"head_dir": "Center",
			},
		}

	# Get an image from the webcam
	def update_frame(self):
		success, frame = self.webcam.read()
		if not success:
			print("Empty camera frame.", flush=True)
			return

		frame = cv2.flip(frame, 1)
		frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		self.h, self.w, _ = frame.shape
		self.results = self.face_mesh.process(frame_rgb)
		return True

	# Gives the positions on the landmarks in the face mesh
	def get_position(self, landmarks):
		if not self.results or not self.results.multi_face_landmarks:
			return

		face_landmarks = self.results.multi_face_landmarks[0]
		position = dict()

		for parts in landmarks:
			landmarks_norm = face_landmarks.landmark[landmarks[parts]]
			x = int(landmarks_norm.x * self.w)
			y = int(landmarks_norm.y * self.h)
			position[parts] = (x, y)

		return position

	# Computes the duration of an action and tells if it should trigger
	def triggered(self, action, state, valid_states):
		if self.action["prev"][action] in valid_states:
			self.action["dur"][action] = time.time() - self.action["start"][action]
			if self.action["dur"][action] > self.wait_amt:
				return True
		else:
			self.action["prev"][action] = state

		return False

	# If there's a face mesh
	def detect_face(self):
		if self.results is None:
			return False

		if self.results.multi_face_landmarks:
			self.action["start"]["detect_face"] = time.time()
		else:
			self.action["dur"]["detect_face"] = time.time() - self.action["start"]["detect_face"]
			if self.action["dur"]["detect_face"] > self.wait_amt:
				return False

		return True

	# Tells where the head is tilted
	def head_tilt(self, threshold=20):
		pos = self.get_position({"left_eye": 33, "right_eye": 263})
		if pos is None:
			return "Center"

		delta_y = pos["right_eye"][1] - pos["left_eye"][1]
		delta_x = pos["right_eye"][0] - pos["left_eye"][0]
		tilt = math.degrees(math.atan2(delta_y, delta_x))

		if tilt < -threshold:
			if self.triggered("head_tilt", "Left", ("Left", "Right")):
				return "Left"
		elif tilt > threshold:
			if self.triggered("head_tilt", "Right", ("Left", "Right")):
				return "Right"
		else:
			self.action["prev"]["head_tilt"] = "Center"
			self.action["start"]["head_tilt"] = time.time()

		return "Center"

	# Tells where the head is turned
	def head_dir(self, threshold=20):
		pos = self.get_position({"left_eye": 33, "right_eye": 263, "nose": 1})
		if pos is None:
			return "Center"

		nose_position = pos["nose"][0] - (pos["left_eye"][0] + pos["right_eye"][0]) // 2
		if nose_position < -threshold:
			if self.triggered("head_dir", "Left", ("Left", "Right")):
				return "Left"
		elif nose_position > threshold:
			if self.triggered("head_dir", "Right", ("Left", "Right")):
				return "Right"
		else:
			self.action["prev"]["head_dir"] = "Center"
			self.action["start"]["head_dir"] = time.time()

		return "Center"