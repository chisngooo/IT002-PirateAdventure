from settings import *
from timeeeeeeeee import Timer

class Player(pygame.sprite.Sprite):
    '''
    Tạo lớp Player kế thừ từ lớp pygame.sprite.Sprite
    Đây là lớp tạo ra nhân vật chính trong trò chơi, xử lý các đặc điểm về vị trí, hình ảnh, va chạm và tương tác của nhân vật với môi trường trò chơi.
    '''
    def __init__(self, pos,  groups,coliision_sprites):
        '''
        Khởi tạo nhân vật chính với vị trí và các thuộc tính cơ bản
        '''
        super().__init__(groups)
        self.image = pygame.Surface((48,56))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft=pos)
        # Lưu lại vị trí cũ của nhân vật để xử lý va chạm
        self.old_rect = self.rect.copy()
        # Khởi tạo các thuộc tính liên quan đến chuyển động
        self.direction = vector(0,0)
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jump_height = 650
        self.gravity_activated = False

        # Khởi tạo các thuộc tính liên quan đến va chạm
        self.collision_sprites = coliision_sprites
        self.on_surface = {
            'floor': False,
        }

        # Khởi tạo các thời gian
        self.timer = {

        }
    def input(self):
        '''
        Xử lí dữ liệu đầu vào từ bàn phím.
        Nếu người chơi nhấn phím mũi tên trái hoặc phải thì nhân vật sẽ di chuyển theo hướng tương ứng.
        Nếu người chơi nhấn phím mũi tên lên thì nhân vật sẽ nhảy
        '''
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if input_vector:
            self.direction.x = input_vector.normalize().x
        else:
            self.direction.x =  input_vector.x
        
        if keys[pygame.K_UP]:
            self.jump = True
    def move(self, data_time):
        '''
        Di chuyển nhân vật theo hướng và tốc độ đã được xác định
        '''
        # Di chuyển theo chiều ngang (trục X)
        self.rect.x += self.direction.x * self.speed * data_time
        self.collision('horizontal')
        # Di chuyển theo chiều dọc (trục Y)
        keys = pygame.key.get_pressed()
        if self.gravity_activated or keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.direction.y += self.gravity/2 * data_time
            self.rect.y += self.direction.y * data_time
            self.direction.y += self.gravity/2 * data_time
            self.collision('vertical')
            self.gravity_activated = True  
        # Nếu nhân vật đang nhảy thì nhân vật sẽ di chuyển theo hướng và tốc độ đã được xác định
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
            self.jump = False
    def check_contact(self):
        '''
        Kiểm tra xem nhân vật có đang tiếp xúc với mặt đất hay không
        '''
        # Tạo một hình chữ nhật ở dưới nhân vật để kiểm tra va chạm với mặt đất
        floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width,2))
        # Tạo một list chứa các hình chữ nhật của các sprite va chạm  
        colide_rects = [sprite.rect for sprite in self.collision_sprites ]

        # Kiểm tra va chạm
        self.on_surface['floor'] = True if floor_rect.collidelist(colide_rects) >= 0 else False
        
    def collision(self,axis):
        '''
        Xử lý va chạm giữa nhân vật và các vật thể khác trong môi trường trò chơi
        '''
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal': # Xử lý va chạm theo chiều ngang
                    # Nếu nhân vật va chạm với sprite từ bên trái nhân vật sẽ dừng lại ngay bên phải sprite
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.rect.right:
                        self.rect.left = sprite.rect.right

                    # Nếu nhân vật va chạm với sprite từ bên phải nhân vật sẽ dừng lại ngay bên trái sprite
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.rect.left:
                        self.rect.right = sprite.rect.left

                else: # Xử lý va chạm theo chiều dọc
                    # Nêu nhân vật va chạm với sprite từ trên xuống dưới thì nhân vật sẽ dừng lại ngay trên sprite
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    # Nếu nhân vật va chạm với sprite từ dưới lên trên thì nhân vật sẽ dừng lại ngay dưới sprite
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
    def update_timer(self):
        '''
        Cập nhật tất cả các timer trong nhân vật
        '''
        for timer in self.timer.values():
            timer.update()
    def update(self,data_time):
        '''
        Câp nhật trạng thái của nhân vật
        
        '''
        self.old_rect = self.rect.copy()
        self.update_timer()

        self.input()
        self.move(data_time)
        self.check_contact()


        