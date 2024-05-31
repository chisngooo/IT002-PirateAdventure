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