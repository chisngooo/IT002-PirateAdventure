from settings import *
from timeeeeeeeee import Timer
from math import sin
import threading

class Player(pygame.sprite.Sprite):
    '''
    Tao lop Player ke thua tu lop Sprite cua pygame
    Day la lop tao ra nhan vat chinh trong tro choi, xu ly cac dac diem ve vi tri, hinh anh, va cham va tuong tac cua nhan vat voi moi truong tro choi.
    '''
    def __init__(self, pos,  groups, collision_sprites, frames, data):
        '''
        Khoi tao nhan vat chinh voi vi tri va cac thuoc tinh co ban 
        '''
        # Thiet lap cac thuoc tinh co ban cho nhan vat
        super().__init__(groups)
        self.z = Z_LAYERS['main']
        self.data = data
        
        # Khoi tao cac frame hinh anh cua nhan vat
        self.frames, self.frame_index = frames, 0
        # Xac dinh trang thai cua nhan vat va huong nhin cua nhan vat
        self.state, self.facing_right = 'idle', True
        # Xac dinh hinh anh cua nhan vat
        self.image = self.frames[self.state][self.frame_index]
        
        # resize hinh anh
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-76, -82)
        # Luu lai vi tri cu cua nhan vat de xu ly va cham
        self.old_rect = self.hitbox_rect.copy()
        # Khoi tao cac thuoc tinh lien quan den hanh dong cua nhan vat
        self.direction = vector(0, 0)
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jump_height = 650
        self.gravity_activated = False
        self.attacking = False
        self.die = False

        # Khoi tao cac thuoc tinh lien quan den va cham
        self.collision_sprites = collision_sprites
        self.on_surface = {
            'floor': False,
            'left': False,
            'right': False
        }
        # Khoi tao cac thuoc tinh lien quan den moving object
        self.platform = None
        
        # Khoi tao cac thoi gian
        self.timer = {
            'attack block': Timer(600),
            'hit': Timer(1300),
            'die': Timer(500)
        }
        # Khoi tao am thanh cho nhan vat
        self.damage_sound = pygame.mixer.Sound('tmx/audio/damage.wav')
        self.attack_sound = pygame.mixer.Sound('tmx/audio/attack.wav')
        self.jump_sound = pygame.mixer.Sound('tmx/audio/jump.wav')
        self.jump_sound.set_volume(0.1)
        self.die_sound = pygame.mixer.Sound('tmx/audio/death.wav')
        self.die_sound.set_volume(0.3)
        self.sound = False
    def input(self):
        '''
        Xu ly du lieu dau vao tu ban phim.
        Neu nguoi choi nhan phim mui ten trai hoac phai thi nhan vat se di chuyen theo huong tuong ung.
        Neu nguoi choi nhan phim mui ten len thi nhan vat se nhay
        '''
        keys = pygame.key.get_pressed()  # Lay trang thai cua cac phim tren ban phim
        input_vector = vector(0, 0)  # Tao mot vector de xac dinh huong di chuyen cua nhan vat
        if keys[pygame.K_LEFT]:  # Neu nguoi choi nhan phim mui ten trai
            input_vector.x -= 1
            self.facing_right = False
        if keys[pygame.K_RIGHT]:  # Neu nguoi choi nhan phim mui ten phai
            input_vector.x += 1
            self.facing_right = True
        if keys[pygame.K_SPACE]:  # Neu nguoi choi nhan phim SPACE
            self.attack()

        if input_vector:
            # neu nguoi choi nhan ca 2 phim mui ten trai va phai cung luc thi nhan vat se dung yen
            self.direction.x = input_vector.normalize().x
        else:
            # neu khong co phim nao duoc nhan thi nhan vat se dung yen
            self.direction.x = input_vector.x
        
        if keys[pygame.K_UP]:  # Neu nguoi choi nhan phim mui ten len
            self.jump = True

    def attack(self):
        '''
        Xu ly hanh dong tan cong cua nhan vat
        '''
        if not self.timer['attack block'].active:  # Neu hanh dong tan cong khong bi block
            # Kich hoat hanh dong tan cong
            self.attacking = True
            self.frame_index = 0

            self.timer['attack block'].activate()  # Block hanh dong tan cong trong mot khoang thoi gian
            self.attack_sound.play()

    def move(self, data_time):
        '''
        Di chuyen nhan vat theo huong va toc do da duoc xac dinh
        '''
        # Di chuyen theo chieu ngang (truc X)
        self.hitbox_rect.x += self.direction.x * self.speed * data_time
        self.collision('horizontal')
        # Di chuyen theo chieu doc (truc Y)
        keys = pygame.key.get_pressed()  # Lay trang thai cua cac phim tren ban phim
        if self.gravity_activated or keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:  # Neu gravity_activated = True hoac nguoi choi nhan phim SPACE hoac phim mui ten len hoac xuong hoac trai hoac phai
            # se kich hoat trang thai di chuyen cho nhan vat
            self.direction.y += self.gravity / 2 * data_time
            self.hitbox_rect.y += self.direction.y * data_time
            self.direction.y += self.gravity / 2 * data_time
            
            self.gravity_activated = True  

        if self.jump:  # Neu nhan vat nhay
            if self.on_surface['floor']:  # Neu nhan vat dang dung tren mat dat
                self.direction.y = -self.jump_height  # Nhan vat se nhay len tren
                self.hitbox_rect.bottom -= 1
                self.jump_sound.play()
            self.jump = False
        # Cap nhat vi tri cua nhan vat
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def platform_move(self, data_time):
        '''
        Di chuyen nhan vat theo platform (moving objects)
        '''
        if self.platform:
            # neu nhan vat dang dung tren platform thi nhan vat se di chuyen theo platform
            self.hitbox_rect.topleft += self.platform.direction * (self.platform.speed) * data_time

    def check_contact(self):
        '''
        Kiem tra xem nhan vat co dang tiep xuc voi mat dat hay khong
        '''
        # Tao mot hinh chu nhat o duoi, trai, phai nhan vat de kiem tra va cham voi mat dat
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2))
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4), (-2, self.hitbox_rect.height / 2))
        # Tao mot list chua cac hinh chu nhat cua cac sprite va cham  
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        
        # Kiem tra va cham
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False
        
        self.platform = None
        # Kiem tra xem nhan vat co dang dung tren platform hay khong
        sprites = self.collision_sprites.sprites() 
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite

    def collision(self, axis):
        '''
        Xu ly va cham giua nhan vat va cac vat the khac trong moi truong tro choi
        '''
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':  # Xu ly va cham theo chieu ngang
                    # Neu nhan vat va cham voi sprite tu ben trai nhan vat se dung lai ngay ben phai sprite
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.rect.right):
                        self.hitbox_rect.left = sprite.rect.right

                    # Neu nhan vat va cham voi sprite tu ben phai nhan vat se dung lai ngay ben trai sprite
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.rect.left):
                        self.hitbox_rect.right = sprite.rect.left

                else:  # Xu ly va cham theo chieu doc
                    # Neu nhan vat va cham voi sprite tu tren xuong duoi thi nhan vat se dung lai ngay tren sprite
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                    # Neu nhan vat va cham voi sprite tu duoi len tren thi nhan vat se dung lai ngay duoi sprite
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0
    
    def animate(self, data_time):
        '''
        Xu ly animation cua nhan vat
        '''
        self.frame_index += ANIMATION_SPEED * data_time  # Tinh toan frame tiep theo cua nhan vat
        # Luu trang thai truoc do
        self.previous_state = self.state
        
        # Sau khi hoan thanh hanh dong 'attack', dat trang thai tro lai trang thai truoc do
        if self.state == 'attack' and self.frame_index >= len(self.frames[self.state]):
            self.state = self.previous_state
        # Xac dinh hinh anh cua nhan vat
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        
        # Lat hinh anh cua nhan vat neu nhan vat dang nhin ve ben trai con khong thi khong lat
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        # Neu nhan vat dang tan cong va frame_index lon hon do dai cua frames[state] thi ket thuc hanh dong tan cong
        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False
        if self.die and self.frame_index >= len(self.frames[self.state]):
            self.image = self.frames['die'][3]
            timer = threading.Timer(0.5, lambda: setattr(self.data, 'health', self.data.health - 1))
            timer.start()  

    def get_state(self):
        '''
        Lay trang thai cua nhan vat
        '''
        if self.data.health <= 0:
            self.state = 'die'
            self.die = True
            if not self.sound:
                self.die_sound.play()
                self.sound = True
        else:
            if self.on_surface['floor']:  # Neu nhan vat dang dung tren mat dat
                if self.attacking:  # Neu nhan vat dang tan cong
                    self.state = 'attack'
                else:  # Neu nhan vat khong tan cong
                    self.state = 'idle' if self.direction.x == 0 else 'run'  # Neu nhan vat dung yen thi trang thai la 'idle' con khong thi la 'run'
            else:  # Neu nhan vat khong dung tren mat dat
                if self.attacking:  # Neu nhan vat dang tan cong
                    self.state = 'attack'  # Trang thai la 'attack'
                else:  # Neu nhan vat khong tan cong
                    self.state = 'jump' if self.direction.y < 0 else 'fall'  # Neu nhan vat dang nhay thi trang thai la 'jump' con khong thi la 'fall'
        
    def get_damage(self):
        '''
        Xu ly khi nhan vat nhan sat thuong
        '''
        if not self.timer['hit'].active:
            self.data.health -= 1
            self.damage_sound.play()
            self.timer['hit'].activate()
            
    def flicker(self):
        '''
        Tao hieu ung nhap nhay cho nhan vat khi nhan vat nhan sat thuong, trong thoi gian nay nhan vat se khong nhan sat thuong nua
        '''
        if self.timer['hit'].active and sin(pygame.time.get_ticks() * 200) >= 0:
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf

    def update_timer(self):
        '''
        Cap nhat tat ca cac timer trong nhan vat
        '''
        for timer in self.timer.values():
            timer.update()

    def update(self, data_time):
        '''
        Cap nhat trang thai cua nhan vat
        '''
        self.old_rect = self.hitbox_rect.copy()
        self.update_timer()

        self.input()
        self.move(data_time)
        self.platform_move(data_time)
        self.check_contact()
        self.get_state()
        self.animate(data_time)
        self.flicker()
