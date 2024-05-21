from settings import *

class Sprite(pygame.sprite.Sprite):
    '''
    Một lớp tạo ra các đối tượng đồ họa trong trò chơi và cung cấp các tính năng xử lý sprite cơ bản, bao gồm việc kiểm tra va chạm giữa các sprites, cập nhật vị trí và trạng thái của sprite, và vẽ sprite lên màn hình.
    '''
    def __init__(self, pos, surf, groups):
        '''
        Khởi tạo một sprite mới với vị trí và hình ảnh được chỉ định
        '''
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.image.fill('white')
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        
    