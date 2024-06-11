from settings import *
from random import choice
from timeeeeeeeee import Timer
from math import sin
class Tooth(pygame.sprite.Sprite):
    '''
    Khoi tao lop Tooth ke thua tu lop Sprite cua pygame
    Lop nay tao ra cac doi tuong do hoa la Tooth gom cac thiet lap cho Tooth nhu hinh anh, vi tri, toc do, huong di chuyen, va cac dac tinh cua Tooth
    '''
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        # Cai dat hinh anh cho Tooth
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft = pos) #Tao hinh chu nhat bao quanh 

        self.z = Z_LAYERS['enemies'] #Thu tu duoc ve la main
        # Cai dat thuoc tinh cho Tooth
        self.direction = choice((-1,1)) #Chon ngau nhien huong di chuyen cua Tooth la trai hoac phai
        self.collisions_rects = [sprite.rect for sprite in collision_sprites] #Lay tat ca cac hinh chu nhat va cham tu collision_sprites

        self.speed = 150 #Toc do di chuyen cua Tooth
        self.hit_timer = Timer(850)
        self.dying = False
        # Am thanh khi Tooth chet
        self.tooth_die_sound = pygame.mixer.Sound('tmx/audio/tooth.wav')
        self.tooth_die_sound.set_volume(0.1)
    def reverse(self):
        '''
        cai dat huong di chuyen cua Tooth neu cham vao bien
        '''
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.activate()

    def die(self, tooth_die_frames):
        '''
        cai dat hinh anh cho Tooth khi chet
        '''
        self.frames = tooth_die_frames
        self.frame_index = 0
        self.dying = True
        Tooth.reverse(self)
        self.image = pygame.transform.flip(self.image, True, False) if self.direction > 0  else self.image
        
        

    def flicker(self):
        '''
        tao hieu ung nhap nhay cho Tooth khi bi nhan vat tan cong, trong thoi gian nay tooth se khong the bi tan cong
        '''
        if self.hit_timer.active and sin(pygame.time.get_ticks() * 100 ) >= 0:
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf
    def update(self, data_time):
        '''
        cap nhat Tooth theo thoi gian
        '''
        self.hit_timer.update()
        # Xu li animation cho Tooth
        self.frame_index += ANIMATION_SPEED * data_time
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        

        if not self.dying:  # Neu Tooth khong chet
            # Di chuyen Tooth
            self.rect.x += self.direction * self.speed * data_time
            # Xu li quay dau cho Tooth khi di chuyen den bien
            floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))  # Tao hinh chu nhat nam o goc duoi ben phai cua Tooth
            floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))  # Tao hinh chu nhat nam o goc duoi ben trai cua Tooth

            wall_rect = pygame.FRect(self.rect.topleft + vector(-1, 0), (self.rect.width + 2, 1))  # Tao hinh chu nhat nam o phia tren Tooth 
            if (floor_rect_right.collidelist(self.collisions_rects) < 0 and self.direction > 0) or (floor_rect_left.collidelist(self.collisions_rects) < 0 and self.direction < 0) or (wall_rect.collidelist(self.collisions_rects) != -1):
                # Neu Tooth cham vao bien thi quay dau
                self.direction *= -1

        self.flicker()

        if self.dying: # Neu Tooth chet
            self.tooth_die_sound.play() #Phat am thanh khi Tooth chet
            self.rect.x += self.direction * self.speed * data_time * 0.2
            self.frame_index += ANIMATION_SPEED * data_time + 0.2
            self.image = self.frames[int(self.frame_index % len(self.frames))]
            self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
            if self.frame_index >= len(self.frames):
                self.kill()
            self.rect.topleft = self.rect.topleft + vector(0, 1)
    
class Shell(pygame.sprite.Sprite):
    '''
    Khoi tao lop Shell ke thua tu lop Sprite cua pygame
    Lop nay tao ra cac doi tuong do hoa la Shell gom cac thiet lap cho Shell nhu hinh anh, vi tri, toc do, huong di chuyen, va cac dac tinh cua Shell
    '''
    def __init__(self, pos, frames, groups, reverse, player, create_pearl):
        super().__init__(groups)
        if reverse: #Neu reverse = True thi lat nguoc hinh anh cua Shell
            self.frames={}
            for key, surfs in frames.items():
                self.frames[key]=[pygame.transform.flip(surf, True, False) for surf in surfs]
            self.bullet_direction= -1 #Huong cua dan
        else: #Neu reverse = False thi giu nguyen hinh anh cua Shell
            self.frames= frames 
            self.bullet_direction = 1 #Huong cua dan
        # Cai dat hinh anh cho shell
        self.frame_index = 0
        self.state='idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        # Thiet lap thuoc tinh cho Shell
        self.z=Z_LAYERS['enemies']
        self.player=player
        self.shoot_timer = Timer(2000)
        self.has_fired = False
        self.create_pearl = create_pearl 
    def reverse(self):
        '''
        Dao huong cua Shell
        '''
        self.bullet_direction *= -1
    def state_management(self):
        '''
        Xu li trang thai cua Shell
        '''
        player_pos, shell_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center) #Lay vi tri cua player va shell
        player_near = shell_pos.distance_to(player_pos) < 1000 # Kiem tra xem player co gan shell khong
        player_front = shell_pos.x < player_pos.x if self.bullet_direction > 0 else shell_pos.x > player_pos.x # Kiem tra xem player co o phia truoc shell khong 
        player_level = abs(shell_pos.y - player_pos.y) < 30 # Kiem tra xem player co o cung mot duong thang voi shell khong
        if player_near and player_front and player_level and not self.shoot_timer.active: # Neu player gan shell va o phia truoc shell va cung mot duong thang voi shell va shell khong ban
            self.state = 'fire' # Dat trang thai cua shell la fire
            self.frame_index = 0 
            self.shoot_timer.activate()
    def update(self, data_time):
        '''
        Cap nhat shell theo thoi gian
        '''
        self.shoot_timer.update() # Cap nhat thoi gian ban cua shell
        self.state_management() # Cap nhat trang thai cua shell
        # Cap nhat animation cho shell
        self.frame_index += ANIMATION_SPEED * data_time
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]     
            #fire
            if self.state == 'fire' and int(self.frame_index) == 3 and not self.has_fired:
                self.create_pearl(self.rect.center,self.bullet_direction)
                self.has_fired = True
        else:
            self.frame_index = 0
            if self.state == 'fire':
                self.state = 'idle'
                self.has_fired = False
class Pearl(pygame.sprite.Sprite):
    '''
    Khoi tao lop Pearl ke thua tu lop Sprite cua pygame
    Lop nay tao ra cac doi tuong do hoa la Pearl gom cac thiet lap cho Pearl nhu hinh anh, vi tri, toc do, huong di chuyen, va cac dac tinh cua Pearl
    '''
    def __init__(self, pos, groups, surf, direction,speed):
        self.pearl = True
        super().__init__(groups)
        # Cai dat hinh anh cho Pearl
        self.image = surf 
        self.rect = self.image.get_frect(center = pos + vector(50 * direction,0))
        # Cai dat thuoc tinh cho Pearl
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main'] 
        self.timers = {'life time': Timer(1500), 'reverse': Timer(250)}
        self.timers['life time'].activate()
    def reverse(self):
        '''
        Kiem tra xem Pearl co dang di chuyen khong va dao huong di chuyen cua Pearl
        '''
        if not self.timers['reverse'].active:
            self.direction *= -1
            self.timers['reverse'].activate()
        
    def update(self,dt):
        '''
        Cap nhat Pearl theo thoi gian
        '''
        for timer in self.timers.values():
            timer.update()
  
        self.rect.x += self.direction * self.speed * dt
        if not self.timers['life time'].active:
            self.kill()
