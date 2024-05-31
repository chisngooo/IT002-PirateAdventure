from settings import *
from timeeeeeeeee import Timer

class Player(pygame.sprite.Sprite):
    '''
    Tạo lớp Player kế thừ từ lớp Sprite của pygame
    Đây là lớp tạo ra nhân vật chính trong trò chơi, xử lý các đặc điểm về vị trí, hình ảnh, va chạm và tương tác của nhân vật với môi trường trò chơi.
    '''
    def __init__(self, pos,  groups,collision_sprites,frames):
        '''
        Khởi tạo nhân vật chính với vị trí và các thuộc tính cơ bản 
        '''
        # Thiết lập các thuộc tính cơ bản cho nhân vật
        super().__init__(groups)
        self.z = Z_LAYERS['main']

        # Khởi tạo các frame hình ảnh của nhân vật
        self.frames, self.frame_index = frames, 0
        # Xác định trạng thái của nhân vật và hướng nhìn của nhân vật
        self.state, self.facing_right = 'idle', True
        # Xác định hình ảnh của nhân vật
        self.image = self.frames[self.state][self.frame_index]
        
        #resize hình ảnh
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-76,-82)
        # Lưu lại vị trí cũ của nhân vật để xử lý va chạm
        self.old_rect = self.hitbox_rect.copy()
        # Khởi tạo các thuộc tính liên quan đến hanh động của nhân vật
        self.direction = vector(0,0)
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jump_height = 650
        self.gravity_activated = False
        self.attacking = False
        # Khởi tạo các thuộc tính liên quan đến va chạm
        self.collision_sprites = collision_sprites
        self.on_surface = {
            'floor': False,
            'left' : False,
            'right': False
        }
        # Khởi tạo các thuộc tính liên quan đến moving object
        self.platform = None
        
        # Khởi tạo các thời gian
        self.timer = {
            'attack block': Timer(1000),
        }
        
    def input(self):
        '''
        Xử lí dữ liệu đầu vào từ bàn phím.
        Nếu người chơi nhấn phím mũi tên trái hoặc phải thì nhân vật sẽ di chuyển theo hướng tương ứng.
        Nếu người chơi nhấn phím mũi tên lên thì nhân vật sẽ nhảy
        '''
        keys = pygame.key.get_pressed() # Lấy trạng thái của các phím trên bàn phím
        input_vector = vector(0,0) # Tạo một vector để xác định hướng di chuyển của nhân vật
        if keys[pygame.K_LEFT]: # Nếu người chơi nhấn phím mũi tên trái
            input_vector.x -= 1 
            self.facing_right = False
        if keys[pygame.K_RIGHT]: # Nếu người chơi nhấn phím mũi tên phải
            input_vector.x += 1
            self.facing_right = True
        if keys[pygame.K_SPACE]: # Nếu người chơi nhấn phím SPACE
            self.attack()

        if input_vector:
            # nếu người chơi nhấn cả 2 phím mũi tên trái và phải cùng lúc thì nhân vật sẽ đứng yên
            self.direction.x = input_vector.normalize().x
        else:
            # nếu không có phím nào được nhấn thì nhân vật sẽ đứng yên
            self.direction.x =  input_vector.x
        
        if keys[pygame.K_UP]: # Nếu người chơi nhấn phím mũi tên lên
            self.jump = True
    def attack(self):
        '''
        Xử lý hành động tấn công của nhân vật
        '''
        if not self.timer['attack block'].active: # Nếu hành động tấn công không bị block
            # Kích hoạt hành động tấn công
            self.attacking = True
            self.frame_index = 0
            self.timer['attack block'].activate() # Block hành động tấn công trong một khoảng thời gian
    def move(self, data_time):
        '''
        Di chuyển nhân vật theo hướng và tốc độ đã được xác định
        '''
        # Di chuyển theo chiều ngang (trục X)
        self.hitbox_rect.x += self.direction.x * self.speed * data_time
        self.collision('horizontal')
        # Di chuyển theo chiều dọc (trục Y)
        keys = pygame.key.get_pressed() # Lấy trạng thái của các phím trên bàn phím
        if self.gravity_activated or keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]: # Nếu gravity_activated = True hoặc người chơi nhấn phím SPACE hoặc phím mũi tên lên hoặc xuống hoặc trái hoặc phải
            # sẽ kích hoạt trạng thái di chuyển cho nhân vật
            self.direction.y += self.gravity/2 * data_time
            self.hitbox_rect.y += self.direction.y * data_time
            self.direction.y += self.gravity/2 * data_time
            
            self.gravity_activated = True  

        if self.jump: # Nếu nhân vật nhảy
            if self.on_surface['floor']: # Nếu nhân vật đang đứng trên mặt đất
                self.direction.y = -self.jump_height # Nhân vật sẽ nhảy lên trên
                self.hitbox_rect.bottom -= 1
            self.jump = False
        # Cập nhật vị trí của nhân vật
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
    def platform_move(self,data_time):
        '''
        Di chuyển nhân vật theo platform (moving objects)
        '''
        if self.platform: 
            # nếu nhân vật đang đứng trên platform thì nhân vật sẽ di chuyển theo platform
            self.hitbox_rect.topleft += self.platform.direction * (self.platform.speed) * data_time
    def check_contact(self):
        '''
        Kiểm tra xem nhân vật có đang tiếp xúc với mặt đất hay không
        '''
        # Tạo một hình chữ nhật ở dưới, trái, phải nhân vật để kiểm tra va chạm với mặt đất
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft,(self.hitbox_rect.width,2))
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(0,self.hitbox_rect.height/4),(2,self.hitbox_rect.height/2))
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2,self.hitbox_rect.height/4),(-2,self.hitbox_rect.height/2))
        # Tạo một list chứa các hình chữ nhật của các sprite va chạm  
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        
        # Kiểm tra va chạmp
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False
        
        self.platform = None
        # Kiểm tra xem nhân vật có đang đứng trên platform hay không
        sprites =  self.collision_sprites.sprites() 
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite
                
    def collision(self,axis):
        '''
        Xử lý va chạm giữa nhân vật và các vật thể khác trong môi trường trò chơi
        '''
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal': # Xử lý va chạm theo chiều ngang
                    # Nếu nhân vật va chạm với sprite từ bên trái nhân vật sẽ dừng lại ngay bên phải sprite
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.rect.right):
                        self.hitbox_rect.left = sprite.rect.right

                    # Nếu nhân vật va chạm với sprite từ bên phải nhân vật sẽ dừng lại ngay bên trái sprite
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.rect.left):
                        self.hitbox_rect.right = sprite.rect.left

                else: # Xử lý va chạm theo chiều dọc
                    # Nêu nhân vật va chạm với sprite từ trên xuống dưới thì nhân vật sẽ dừng lại ngay trên sprite
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top)>= int(sprite.rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                    # Nếu nhân vật va chạm với sprite từ dưới lên trên thì nhân vật sẽ dừng lại ngay dưới sprite
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0
    def update_timer(self):
        '''
        Cập nhật tất cả các timer trong nhân vật
        '''
        for timer in self.timer.values():
            timer.update()
    def animate(self,data_time):
        '''
        Xử lý animation của nhân vật
        '''
        self.frame_index += ANIMATION_SPEED * data_time # Tính toán frame tiếp theo của nhân vật
        # Lưu trạng thái trước đó
        self.previous_state = self.state
        
        # Sau khi hoàn thành hành động 'attack', đặt trạng thái trở lại trạng thái trước đó
        if self.state == 'attack' and self.frame_index >= len(self.frames[self.state]):
            self.state = self.previous_state
        # Xác định hình ảnh của nhân vật
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        # Lật hình ảnh của nhân vật nếu nhân vật đang nhìn về bên trái còn không thì không lật
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
        # Nếu nhân vật đang tấn công và frame_index lớn hơn độ dài của frames[state] thì kết thúc hành động tấn công
        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False
    def get_state(self):
        '''
        Lấy trạng thái của nhân vật
        '''
    
        if self.on_surface['floor']: # Nếu nhân vật đang đứng trên mặt đất
            if self.attacking: # Nếu nhân vật đang tấn công
                self.state = 'attack'
            else: # Nếu nhân vật không tấn công
                self.state = 'idle' if self.direction.x == 0 else 'run' # Nếu nhân vật đứng yên thì trạng thái là 'idle' còn không thì là 'run'
        else: # Nếu nhân vật không đứng trên mặt đất
            if self.attacking:  # Nếu nhân vật đang tấn công
                self.state = 'attack' # Trạng thái là 'attack'
            else: # Nếu nhân vật không tấn công
                self.state = 'jump' if self.direction.y < 0 else 'fall' # Nếu nhân vật đang nhảy thì trạng thái là 'jump' còn không thì là 'fall'
        
    
    def update(self,data_time):
        '''
        Câp nhật trạng thái của nhân vật
        
        '''
        self.old_rect = self.hitbox_rect.copy()
        self.update_timer()

        self.input()
        self.move(data_time)
        self.platform_move(data_time)
        self.check_contact()
        self.get_state()
        self.animate(data_time)

        
         