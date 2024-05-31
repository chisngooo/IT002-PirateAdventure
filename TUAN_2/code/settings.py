import pygame, sys
from pygame.math import Vector2 as vector
'''
Khởi tạo các thuộc tính cơ bản cho trò chơi
Bao gồm:
    WINDOW_WIDTH, WINDOW_HEIGHT: Kích thước cửa sổ trò chơi
    BUTTON_WIDTH, BUTTON_HEIGHT: Kích thước của các nút trong Menu trò chơi
    TILE_SIZE: Kích thước của mỗi ô trong trò chơi
    ANIMATION_SPEED: The speed of the animation in the game
    Z_LAYERS: một dictionary lưu các lớp khác nhau gồm các tên và số thứ tự tương ứng với cách vẽ các sprite trong game.
'''
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
TILE_SIZE = 64
ANIMATION_SPEED = 6
Z_LAYERS = {
	'bg': 0,
	'cloud': 1,
	'bg tiles': 2,
	'bg details': 3,
	'main': 4,
	'water': 5,
	'grass': 6
}
