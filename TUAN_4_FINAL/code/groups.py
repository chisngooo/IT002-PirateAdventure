from settings import *
from sprites import Sprite, Cloud
from random import randint, choice
from timeeeeeeeee import Timer

class AllSprite(pygame.sprite.Group):
    '''
    Khoi tao lop AllSprite ke thua tu lop Group cua pygame.sprite de quan ly tat ca cac sprite trong tro choi
    '''
    def __init__(self, width, height, clouds, horizon_line, bg_tile=None, top_limit=0):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector(0, 0)  # Tao mot vector offset de xu ly vi tri cua cac sprite
        self.width = width * TILE_SIZE  # Tinh toan chieu rong cua man hinh
        self.height = height * TILE_SIZE  # Tinh toan chieu cao cua man hinh
        # Tao bien cho man hinh
        self.borders = {
            'left': 0,  # Bien trai cua man hinh co gia tri la 0
            'right': -self.width + WINDOW_WIDTH,  # Gia tri bien phai cua man hinh duoc tinh tu chieu rong cua man hinh game - chieu rong cua map
            'top': top_limit,  # Bien tren cua man hinh duoc tinh tu top_limit lay tu tiled map
            'bottom': -self.height + WINDOW_HEIGHT  # Bien duoi cua man hinh duoc tinh tu chieu cao cua man hinh game - chieu cao cua map
        }
        # Tao bien sky de xac dinh man hinh la hinh nen hay bau troi
        self.sky = not bg_tile
        # Tao bien horizon_line de xac dinh duong chan troi
        self.horizon_line = horizon_line
        if bg_tile:
            for col in range(width):
                for row in range(-int(top_limit / TILE_SIZE) - 1, height):
                    x, y = col * TILE_SIZE, row * TILE_SIZE
                    Sprite((x, y), bg_tile, self, -1)
        else:  # Neu man hinh la bau troi
            # Tao bien large_cloud de xac dinh hinh anh cua dam may lon
            self.large_cloud = clouds['large']
            # Tao bien small_cloud de xac dinh hinh anh cua dam may nho
            self.small_cloud = clouds['small']
            # Huong cua cloud
            self.cloud_direction = -1
            # Xu ly dam may lon
            self.large_cloud_speed = 50
            self.large_cloud_x = 0
            self.large_cloud_tiles = int(self.width / self.large_cloud.get_width()) + 2
            self.large_cloud_width, self.large_cloud_height = self.large_cloud.get_size()
            # Xu ly dam may nho
            self.cloud_timer = Timer(2500, self.create_cloud, True)
            self.cloud_timer.activate()
            for cloud in range(20):
                pos = (randint(0, self.width), randint(self.borders['top'], self.horizon_line))
                surf = choice(self.small_cloud)
                Cloud(pos, surf, self)
    
    def camera_constraint(self):
        '''
        Xu ly vi tri cua camera de khong cho camera di chuyen ra khoi map
        '''
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']  # Xu ly vi tri cua camera theo chieu ngang ben trai
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']  # Xu ly vi tri cua camera theo chieu ngang ben phai
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']  # Xu ly vi tri cua camera theo chieu doc ben duoi
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']  # Xu ly vi tri cua camera theo chieu doc ben tren
    
    def draw_sky(self):
        '''
        Ve bau troi
        '''
        self.display_surface.fill('#ddc6a1')  # Tao mau nen cho bau troi
        # Tinh toan vi tri cua duong chan troi
        horizon_pos = self.horizon_line + self.offset.y
        # Tao mau xanh cho bien (phia tren duong chan troi)
        sea_rect = pygame.FRect(0, horizon_pos, WINDOW_WIDTH, WINDOW_HEIGHT - horizon_pos)
        pygame.draw.rect(self.display_surface, '#92a9ce', sea_rect)
        # Ve duong chan troi
        pygame.draw.line(self.display_surface, '#f5f1de', (0, horizon_pos), (WINDOW_WIDTH, horizon_pos), 4)
    
    def draw_large_cloud(self, data_time):
        '''
        Ve dam may lon
        '''
        self.large_cloud_x += self.cloud_direction * self.large_cloud_speed * data_time  # Tinh toan vi tri cua dam may lon
        if self.large_cloud_x <= -self.large_cloud_width:  # Neu dam may lon di chuyen ra khoi man hinh thi dat lai vi tri cua no
            self.large_cloud_x = 0
        for cloud in range(self.large_cloud_tiles):  # Ve cac dam may lon
            left = self.large_cloud_x + self.large_cloud_width * cloud + self.offset.x
            top = self.horizon_line - self.large_cloud_height + self.offset.y
            self.display_surface.blit(self.large_cloud, (left, top))
    
    def create_cloud(self):
        '''
        Tao dam may nho
        '''
        pos = (randint(self.width + 500, self.width + 600), randint(self.borders['top'], self.horizon_line))
        surf = choice(self.small_cloud)
        Cloud(pos, surf, self)
    
    def draw(self, target_pos, data_time):
        '''
        Hien thi cac sprite trong tro choi
        '''
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)  # Tinh toan offset x
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)  # Tinh toan offset y
        self.camera_constraint()  # Xu ly vi tri cua camera
        if self.sky:
            self.cloud_timer.update()
            self.draw_sky()
            self.draw_large_cloud(data_time)
        for sprite in sorted(self, key=lambda sprite: sprite.z):  # Sap xep cac sprite theo thu tu z va chay vong lap de hien thi cac sprite
            offset_pos = sprite.rect.topleft + self.offset  # Tinh toan vi tri moi cua sprite
            self.display_surface.blit(sprite.image, offset_pos)  # Hien thi sprite len man hinh

class CollisionSprite(pygame.sprite.Group):
    '''
    Khoi tao lop CollisionSprite ke thua tu lop Group cua pygame.sprite de quan ly cac sprite va cham trong tro choi
    '''
    def __init__(self):
        super().__init__()

class ToothSprite(pygame.sprite.Group):
    '''
    Khoi tao lop ToothSprite ke thua tu lop Sprite cua pygame.sprite de tao sprite cho doi tuong Tooth
    '''
    def __init__(self):
        '''
        Khoi tao sprite cho doi tuong Tooth
        '''
        super().__init__()

class DamageSprite(pygame.sprite.Group):
    '''
    Khoi tao lop DamageSprite ke thua tu lop Group cua pygame.sprite de quan ly cac sprite co the gay sat thuong trong tro choi
    '''
    def __init__(self):
        super().__init__()

class PearlSprite(pygame.sprite.Group):
    '''
    Khoi tao lop PearlSprite ke thua tu lop Group cua pygame.sprite de quan ly Pearl trong tro choi
    '''
    def __init__(self):
        super().__init__()

class ItemSprite(pygame.sprite.Group):
    '''
    Khoi tao lop ItemSprite ke thua tu lop Group cua pygame.sprite de quan ly cac sprite Item trong tro choi
    '''
    def __init__(self):
        super().__init__()
