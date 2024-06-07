from settings import *

class AllSprite(pygame.sprite.Group):
    '''
    Khởi tạo lớp Allsprite kế thừa từ lớp Group của pygame.sprite để quản lý tất cả các sprite trong trò chơi
    '''
    def __init__(self):
        
        super().__init__()
        self.display_surface = pygame.display.get_surface() 
        self.offset = vector(0,0) # Tạo một vector offset để xử lý vị trí của các sprite
    def draw(self, target_pos):
        '''
        Hiển thị các sprite trong trò chơi 
        '''
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2) # Tính toán offset x
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2) # Tính toán offset y
        for sprite in sorted(self, key= lambda sprite: sprite.z): # Sắp xếp các sprite theo thứ tự z và chạy vòng lặp để hiển thị các sprite
            offset_pos = sprite.rect.topleft + self.offset # Tính toán vị trí mới của sprite
            self.display_surface.blit(sprite.image, offset_pos) # Hiển thị sprite lên màn hình
class CollisionSprite(pygame.sprite.Group):
    '''
    Khởi tạo lớp CollisionSprite kế thừa từ lớp Group của pygame.sprite để quản lý các sprite va chạm trong trò chơi
    '''
    def __init__(self):
        super().__init__()
class ToothSprite(pygame.sprite.Group):
    '''
    Khởi tạo lớp ToothSprite kế thừa từ lớp Sprite của pygame.sprite để tạo sprite cho đối tượng Tooth
    '''
    def __init__(self):
        '''
        Khởi tạo sprite cho đối tượng Tooth
        '''
        super().__init__()
class DamageSprite(pygame.sprite.Group):
    '''
    Khởi tạo lớp DamageSprite kế thừa từ lớp Group của pygame.sprite để quản lý các sprite có thể gây sát thương trong trò chơi
    '''
    def __init__(self):
        super().__init__()
class PearlSprite(pygame.sprite.Group):
    '''
    Khởi tạo lớp PearlSprite kế thừa từ lớp Group của pygame.sprite để quản lý Pearl trong trò chơi 
    '''
    def __init__(self):
        super().__init__()
class ItemSprite(pygame.sprite.Group):
    '''
    Khởi tạo lớp ItemSprite kế thừa từ lớp Group của pygame.sprite để quản lý các sprite Item trong trò chơi
    '''
    def __init__(self):
        super().__init__()