from settings import *

class Sprite(pygame.sprite.Sprite): 
    '''
    Khởi tạo lớp Sprite kế thừa từ lớp Sprite của pygame 
    Lớp này tạo ra các đối tượng đồ họa trong trò chơi như nhân vật, vật phẩm, môi trường, v.v...
    '''
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE,TILE_SIZE)), groups = None, z = Z_LAYERS['bg tiles']):
        '''
        Khởi tạo sprite với vị trí, hình ảnh, các nhóm thuộc tính của sprite và thứ tự được vẽ lên màn hình
        '''
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z
class AnimatedSprite(Sprite): 
    '''
    Khởi tạo lớp AnimatedSprite kế thừa từ lớp Sprite
    Lớp này tạo ra các đối tượng đồ họa có hiệu ứng chuyển động (Animation) trong trò chơi
    '''
    def __init__(self, pos, frames, groups, z = Z_LAYERS['bg tiles'], animation_speed = ANIMATION_SPEED):
        '''
        Khởi tạo AnimatedSprite với vị trí, các frame hình ảnh, các nhóm thuộc tính của sprite và thứ tự được vẽ lên màn hình và tốc độ animation
        '''
        self.frames, self.frame_index = frames, 0
        super().__init__(pos,self.frames[self.frame_index],groups,z)
        self.animation_speed = animation_speed
    def animate(self,data_time):
        '''
        Xử lí animation cho sprite
        '''
        self.frame_index += self.animation_speed * data_time
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
    def update(self,data_time):
        '''
        Cập animation của sprite đảm bảo sprite chuyển động liên tục
        '''
        self.animate(data_time)
class MovingSprite(AnimatedSprite): 
    '''
    Khởi tạo lớp MovingSprite kế thừa từ lớp AnimatedSprite
    Lớp này tạo ra các đối tượng đồ họa có khả năng di chuyển trong trò chơi
    '''
    def __init__(self, frames,groups, start_pos, end_pos, move_dir, speed, flip = False):
        super().__init__(start_pos,frames,groups)
        if move_dir == 'x': # nếu hướng di chuyển của moving object là theo chiều ngang
            self.rect.midleft = start_pos # đặt vị trí bắt đầu của moving object ở giữa bên trái
        else: # nếu hướng di chuyển của moving object là theo chiều dọc
            self.rect.midtop = start_pos # đặt vị trí bắt đầu của moving object ở giữa phía trên
        # lưu vị trí bắt đầu và vị trí cuối cùng của moving object
        self.start_pos = start_pos
        self.end_pos = end_pos
        # khởi tạo các thuộc tính di chuyển của moving object
        self.moving = True
        self.speed = speed
        # xác định hướng di chuyển của moving object
        self.direction = vector(1,0) if move_dir == 'x' else vector(0,1)
        self.move_dir = move_dir
        # xác định hướng flip của moving object
        self.flip = flip
        self.reverse = {'x': False, 'y': False}

    def check_border(self):
        """
        kiểm tra xem moving object đã đến vị trí cuối cùng chưa, nếu đã đến thì đổi hướng di chuyển
        """

        if self.move_dir == 'x': # nếu hướng di chuyển của moving object là theo chiều ngang
            # nếu moving object đến vị trí cuối cùng bên phải thì đổi hướng di chuyển
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_pos[0]
            # nếu moving object đến vị trí cuối cùng bên trái thì đổi hướng di chuyển
            if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_pos[0]
            # lưu trạng thái hướng di chuyển của moving object
            self.reverse['x'] = True if self.direction.x < 0 else False
        else: # nếu hướng di chuyển của moving object là theo chiều dọc
            # nếu moving object đến vị trí cuối cùng bên dưới thì đổi hướng di chuyển
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            # nếu moving object đến vị trí cuối cùng bên trên thì đổi hướng di chuyển
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]
            # lưu trạng thái hướng di chuyển của moving object
            self.reverse['y'] = True if self.direction.y > 0 else False

    def update(self,data_time):
        """
        cập nhật vị trí của moving object
        """
        self.old_rect = self.rect.copy()
        
        self.rect.topleft+=self.direction * self.speed * data_time # di chuyển moving object theo hướng và tốc độ đã xác định
        self.check_border() # kiểm tra xem moving object đã đến vị trí cuối cùng chưa

        self.animate(data_time) # cập nhật animation của moving object
        if self.flip: 
            # nếu flip = True thì moving object sẽ bị lật ngược theo hướng di chuyển
            self.image = pygame.transform.flip(self.image,self.reverse['x'],self.reverse['y'])
        