from settings import *
from random import randint

class Sprite(pygame.sprite.Sprite): 
    '''
    Khoi tao lop Sprite ke thua tu lop Sprite cua pygame 
    Lop nay tao ra cac doi tuong do hoa trong tro choi nhu nhan vat, vat pham, moi truong, v.v...
    '''
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE,TILE_SIZE)), groups = None, z = Z_LAYERS['bg tiles']):
        '''
        Khoi tao sprite voi vi tri, hinh anh, cac nhom thuoc tinh cua sprite va thu tu duoc ve len man hinh
        '''
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z

class AnimatedSprite(Sprite): 
    '''
    Khoi tao lop AnimatedSprite ke thua tu lop Sprite
    Lop nay tao ra cac doi tuong do hoa co hieu ung chuyen dong (Animation) trong tro choi
    '''
    def __init__(self, pos, frames, groups, z = Z_LAYERS['bg tiles'], animation_speed = ANIMATION_SPEED):
        '''
        Khoi tao AnimatedSprite voi vi tri, cac frame hinh anh, cac nhom thuoc tinh cua sprite va thu tu duoc ve len man hinh va toc do animation
        '''
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed

    def animate(self, data_time):
        '''
        Xu ly animation cho sprite
        '''
        self.frame_index += self.animation_speed * data_time
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, data_time):
        '''
        Cap nhat animation cua sprite dam bao sprite chuyen dong lien tuc
        '''
        self.animate(data_time)

class Item(AnimatedSprite):
    '''
    Khoi tao lop Item ke thua tu lop AnimatedSprite
    Lop nay tao ra cac doi tuong do hoa la Item trong tro choi 
    '''
    def __init__(self, item_type, pos, frames, groups, data):
        super().__init__(pos, frames, groups)
        self.rect.center = pos  # dat vi tri cua item o giua
        self.item_type = item_type  # xac dinh loai item
        self.data = data  # luu du lieu cua item

    def activate(self):		
        '''
        Kich hoat item khi nguoi choi va cham voi item
        voi item_type la silver: tang 5 coins, diamond: tang 50 coins, skull: tang 1 mang
        '''
        if self.item_type == 'silver':
            self.data.coins += 1
        if self.item_type == 'diamond':
            self.data.coins += 15
        if self.item_type == 'skull':
            self.data.health += 1

class ParticleEffectSprite(AnimatedSprite):
    '''
    Khoi tao lop ParticleEffectSprite ke thua tu lop AnimatedSprite
    Lop nay tao ra cac doi tuong do hoa la ParticleEffect trong tro choi lam nhiem vu tao hieu ung cho cac vat the trong tro choi khi va cham
    (cac items khi nguoi choi nhat, cac vat the khi bi ban trung)
    '''
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.z = Z_LAYERS['main']

    def animate(self, data_time):
        '''
        Tao animation cho ParticleEffect
        '''
        self.frame_index += self.animation_speed * data_time
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

class MovingSprite(AnimatedSprite): 
    '''
    Khoi tao lop MovingSprite ke thua tu lop AnimatedSprite
    Lop nay tao ra cac doi tuong do hoa co kha nang di chuyen trong tro choi
    '''
    def __init__(self, frames, groups, start_pos, end_pos, move_dir, speed, flip = False):
        super().__init__(start_pos, frames, groups)
        if move_dir == 'x':  # neu huong di chuyen cua moving object la theo chieu ngang
            self.rect.midleft = start_pos  # dat vi tri bat dau cua moving object o giua ben trai
        else:  # neu huong di chuyen cua moving object la theo chieu doc
            self.rect.midtop = start_pos  # dat vi tri bat dau cua moving object o giua phia tren
        # luu vi tri bat dau va vi tri cuoi cung cua moving object
        self.start_pos = start_pos
        self.end_pos = end_pos
        # khoi tao cac thuoc tinh di chuyen cua moving object
        self.moving = True
        self.speed = speed
        # xac dinh huong di chuyen cua moving object
        self.direction = vector(1, 0) if move_dir == 'x' else vector(0, 1)
        self.move_dir = move_dir
        # xac dinh huong flip cua moving object
        self.flip = flip
        self.reverse = {'x': False, 'y': False}

    def check_border(self):
        '''
        Kiem tra xem moving object da den vi tri cuoi cung chua, neu da den thi doi huong di chuyen
        '''
        if self.move_dir == 'x':  # neu huong di chuyen cua moving object la theo chieu ngang
            # neu moving object den vi tri cuoi cung ben phai thi doi huong di chuyen
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_pos[0]
            # neu moving object den vi tri cuoi cung ben trai thi doi huong di chuyen
            if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_pos[0]
            # luu trang thai huong di chuyen cua moving object
            self.reverse['x'] = True if self.direction.x < 0 else False
        else:  # neu huong di chuyen cua moving object la theo chieu doc
            # neu moving object den vi tri cuoi cung ben duoi thi doi huong di chuyen
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            # neu moving object den vi tri cuoi cung ben tren thi doi huong di chuyen
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]
            # luu trang thai huong di chuyen cua moving object
            self.reverse['y'] = True if self.direction.y > 0 else False

    def update(self, data_time):
        '''
        Cap nhat vi tri cua moving object
        '''
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * data_time  # di chuyen moving object theo huong va toc do da xac dinh
        self.check_border()  # kiem tra xem moving object da den vi tri cuoi cung chua
        self.animate(data_time)  # cap nhat animation cua moving object
        if self.flip: 
            # neu flip = True thi moving object se bi lat nguoc theo huong di chuyen
            self.image = pygame.transform.flip(self.image, self.reverse['x'], self.reverse['y'])

class Cloud(Sprite):
    '''
    Khoi tao lop Cloud ke thua tu lop Sprite
    Lop nay tao ra cac doi tuong do hoa la Cloud trong tro choi
    '''
    def __init__(self, pos, surf, groups, z = Z_LAYERS['cloud']):
        super().__init__(pos, surf, groups, z)
        self.speed = randint(50, 120)  # toc do di chuyen cua cloud lay ngau nhien tu 50 den 120
        self.direction = -1  # huong di chuyen cua cloud tu phai qua trai
        self.rect.midbottom = pos

    def update(self, data_time):
        '''
        Cap nhat vi tri cua cloud theo thoi gian
        '''
        self.rect.x += self.speed * self.direction * data_time
        if self.rect.right <= 0:
            self.kill()
