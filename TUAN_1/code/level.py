from settings import *
from sprites import Sprite
from player import Player

class Level:
    '''
    Khởi tạo và quản lý môi trường trò chơi, bao gồm các thiết lập cơ bản, cập nhật liên tục các sự kiện và xử lý tương tác giữa người chơi và trò chơi.
    '''
    def __init__(self,tmx_map):
        self.display_surface = pygame.display.get_surface()

        ##GROUPS
        # Tạo một nhóm mới để chứa tất cả các sprites
        self.all_sprites = pygame.sprite.Group()
        # Tạo một nhóm mới để chứa các collision sprites
        self.collison_sprites = pygame.sprite.Group()
        # Gọi hàm setup để thiết lập môi trường trò chơi
        self.setup(tmx_map)
        
    def setup(self,tmx_map):
        '''
        Thiết lập môi trường cho trò chơi
        '''
        # Tạo các sprite Terrain
        for x,y,surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,(self.all_sprites,self.collison_sprites))
        
        # Tạo các sprite Objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            # Nếu obj.name là player thì tạo ra một sprite Player
            if obj.name == 'player':
                Player((obj.x,obj.y),self.all_sprites,self.collison_sprites)
                
    def run(self,data_time):
        '''
        Vòng lặp chạy trò chơi
        '''
        self.display_surface.fill('black')
        # Cập nhật tất cả các sprite trong all_sprites
        self.all_sprites.update(data_time)
        # Vẽ tất cả các sprite trong all_sprites lên màn hình
        self.all_sprites.draw(self.display_surface)
