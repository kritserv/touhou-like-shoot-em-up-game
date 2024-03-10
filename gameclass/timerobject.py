import time

class Timer():
	def __init__(self):
		self.start_time = 0
		self.elapsed_time = 0
		self.is_paused = True

	def start(self):
		if self.is_paused:
			self.start_time = time.time()
			self.is_paused = False

	def pause(self):
		if not self.is_paused:
			self.elapsed_time += time.time() - self.start_time
			self.is_paused = True

	def resume(self):
		if self.is_paused:
			self.start_time = time.time()
			self.is_paused = False

	def reset(self):
		self.start_time = 0
		self.elapsed_time = 0
		self.is_paused = True

	def restart(self):
		self.reset()
		self.start()

	def toggle_pause(self):
		if self.is_paused:
			self.resume()
		else:
			self.pause()

	def get_elapsed_time(self):
		if self.is_paused:
			return round(self.elapsed_time)
		else:
			return round(self.elapsed_time + time.time() - self.start_time)