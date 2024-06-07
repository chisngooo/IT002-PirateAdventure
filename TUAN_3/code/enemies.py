from settings import *
from random import choice
from timeeeeeeeee import Timer
from math import sin
class Tooth(pygame.sprite.Sprite):
    '''
    Khởi tạo lớp Tooth kế thừa từ lớp Sprite của pygame
    Lớp này tạo ra các đối tượng đồ họa là Tooth gồm các thiết lập cho Tooth như hình ảnh, vị trí, tốc độ, hướng di chuyển, và các đặc tính của Tooth
    '''
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        # Cài đặt hình ảnh cho Tooth
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft = pos) #Tạo hình chữ nhật bao quanh 

        self.z = Z_LAYERS['enemies'] #Thứ tự được vẽ là main
        # Cài đặt thuộc tính cho Tooth
        self.direction = choice((-1,1)) #Chọn ngẫu nhiên hướng di chuyển của Tooth là trái hoặc phải
        self.collisions_rects = [sprite.rect for sprite in collision_sprites] #Lấy tất cả các hình chữ nhật va chạm từ collision_sprites

        self.speed = 150 #Tốc độ di chuyển của Tooth
        self.hit_timer = Timer(850)
        self.dying = False

    def reverse(self):
        '''
        cài đặt hướng di chuyển của Tooth nếu chạm vào biên
        '''
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.activate()

    def die(self, tooth_die_frames):
        '''
        cài đặt hình ảnh cho Tooth khi chết
        '''
        self.frames = tooth_die_frames
        self.frame_index = 0
        self.dying = True
        Tooth.reverse(self)
        self.image = pygame.transform.flip(self.image, True, False) if self.direction > 0  else self.image
        
        
        

    def flicker(self):
        '''
        tạo hiệu ứng nhấp nháy cho Tooth khi bị nhân vật tấn công, trong thời gian này tooth sẽ không thể bị tấn công
        '''
        if self.hit_timer.active and sin(pygame.time.get_ticks() * 100 ) >= 0:
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf
    def update(self, data_time):
        '''
        câp nhật Tooth theo thời gian
        '''
        self.hit_timer.update()
        # Xử lí animation cho Tooth
        self.frame_index += ANIMATION_SPEED * data_time
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        

        if not self.dying:  # Nếu Tooth không chết
            # Di chuyển Tooth
            self.rect.x += self.direction * self.speed * data_time
            # Xử lí quay đầu cho Tooth khi di chuyển đến biên
            floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))  # Tạo hình chữ nhật nằm ở góc dưới bên phải của Tooth
            floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))  # Tạo hình chữ nhật nằm ở góc dưới bên trái của Tooth

            wall_rect = pygame.FRect(self.rect.topleft + vector(-1, 0), (self.rect.width + 2, 1))  # Tạo hình chữ nhật nằm ở phía trên Tooth 
            if (floor_rect_right.collidelist(self.collisions_rects) < 0 and self.direction > 0) or (floor_rect_left.collidelist(self.collisions_rects) < 0 and self.direction < 0) or (wall_rect.collidelist(self.collisions_rects) != -1):
                # Nếu Tooth chạm vào biên thì quay đầu
                self.direction *= -1

        self.flicker()

        if self.dying: # Nếu Tooth chết
            self.rect.x += self.direction * self.speed * data_time * 0.2
            self.frame_index += ANIMATION_SPEED * data_time + 0.2
            self.image = self.frames[int(self.frame_index % len(self.frames))]
            self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
            if self.frame_index >= len(self.frames):
                self.kill()
            self.rect.topleft = self.rect.topleft + vector(0, 1)
    
class Shell(pygame.sprite.Sprite):
    '''
    Khởi tạo lớp Shell kế thừa từ lớp Sprite của pygame
    Lớp này tạo ra các đối tượng đồ họa là Shell gồm các thiết lập cho Shell như hình ảnh, vị trí, tốc độ, hướng di chuyển, và các đặc tính của Shell
    '''
    def __init__(self, pos, frames, groups, reverse, player, create_pearl):
        super().__init__(groups)
        if reverse: #Nếu reverse = True thì lật ngược hình ảnh của Shell
            self.frames={}
            for key, surfs in frames.items():
                self.frames[key]=[pygame.transform.flip(surf, True, False) for surf in surfs]
            self.bullet_direction= -1 #Hướng của đạn
        else: #Nếu reverse = False thì giữ nguyên hình ảnh của Shell
            self.frames= frames 
            self.bullet_direction = 1 #Hướng của đạn
        # Cài đặt hình ảnh cho shell
        self.frame_index = 0
        self.state='idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        # Thiết lập thuộc tính cho Shell
        self.z=Z_LAYERS['enemies']
        self.player=player
        self.shoot_timer = Timer(2000)
        self.has_fired = False
        self.create_pearl = create_pearl 
    def reverse(self):
        '''
        Đảo hướng của Shell
        '''
        self.bullet_direction *= -1
    def state_management(self):
        '''
        Xử lí trạng thái của Shell
        '''
        player_pos, shell_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center) #Lấy vị trí của player và shell
        player_near = shell_pos.distance_to(player_pos) < 1000 # Kiểm tra xem player có gần shell không
        player_front = shell_pos.x < player_pos.x if self.bullet_direction > 0 else shell_pos.x > player_pos.x # Kiểm tra xem player có ở phía trước shell không 
        player_level = abs(shell_pos.y - player_pos.y) < 30 # Kiểm tra xem player có ở cùng một đường thẳng với shell không
        if player_near and player_front and player_level and not self.shoot_timer.active: # Nếu player gần shell và ở phía trước shell và cùng một đường thẳng với shell và shell không bắn
            self.state = 'fire' # Đặt trạng thái của shell là fire
            self.frame_index = 0 
            self.shoot_timer.activate()
    def update(self, data_time):
        '''
        Cập nhật shell theo thời gian
        '''
        self.shoot_timer.update() # Cập nhật thời gian bắn của shell
        self.state_management() # Câp nhật trạng thái của shell
        # Cap nhật animation cho shell
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
    Khởi tạo lớp Pearl kế thừa từ lớp Sprite của pygame
    Lớp này tạo ra các đối tượng đồ họa là Pearl gồm các thiết lập cho Pearl như hình ảnh, vị trí, tốc độ, hướng di chuyển, và các đặc tính của Pearl
    '''
    def __init__(self, pos, groups, surf, direction,speed):
        self.pearl = True
        super().__init__(groups)
        # Cài đặt hình ảnh cho Pearl
        self.image = surf 
        self.rect = self.image.get_frect(center = pos + vector(50 * direction,0))
        # Cài đặt thuộc tính cho Pearl
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main'] 
        self.timers = {'life time': Timer(4000), 'reverse': Timer(250)}
        self.timers['life time'].activate()
    def reverse(self):
        '''
        Kiêm tra xem Pearl có đang di chuyển không và đảo hướng di chuyển của Pearl
        '''
        if not self.timers['reverse'].active:
            self.direction *= -1
            self.timers['reverse'].activate()
        
    def update(self,data_time):
        '''
        Cập nhật Pearl theo thời gian
        '''
        for timer in self.timers.values():
            timer.update()
  
        self.rect.x += self.direction * self.speed * data_time
        if not self.timers['life time'].active:
            self.kill()