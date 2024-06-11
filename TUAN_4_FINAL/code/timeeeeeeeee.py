# code được tham khảo từ: https://www.youtube.com/watch?v=WViyCAa6yLI (time: 1:25:26)
from pygame.time import get_ticks

class Timer:
	'''
	class Timer dung de tao cac thoi gian cho cac su kien trong game
	'''
	def __init__(self, duration, func = None, repeat = False):
		self.duration = duration
		self.func = func
		self.start_time = 0
		self.active = False
		self.repeat = repeat
	def activate(self):
		'''
		kich hoat timer de bat dau dem thoi gian
		'''
		self.active = True
		self.start_time = get_ticks()
	def deactivate(self):
		'''
		ngung kiem tra thoi gian
		'''
		self.active = False
		self.start_time = 0
		if self.repeat:
			self.activate()
	def update(self):
		'''
		cap nhat thoi gian
		
		'''
		current_time = get_ticks()
		if current_time - self.start_time >= self.duration:
			if self.func and self.start_time != 0:
				self.func()
			self.deactivate()
