from settings import *
from sprites import AnimatedSprite
from random import randint
from timeeeeeeeee import Timer


class UI:
    def __init__(self, font, frames):
        '''
        Khoi tao class UI de hien thi thong tin so mang va so tien cua nguoi choi
        '''
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

        # Khởi tạo các frame cho heart
        self.heart_frames = [pygame.transform.scale(frame, (int(frame.get_width() * 1.5), int(frame.get_height() * 1.5))) for frame in frames['heart']]
        self.heart_surf_width = self.heart_frames[0].get_width()
        self.heart_padding = 15

        # Khởi tạo các biến để hiển thị coin
        self.coin_amount = 0
        self.coin_timer = Timer(1000)
        self.coin_surf = frames['coin']

    def create_health(self, amount):
        '''
        Tao so mang cho nguoi choi
        '''
        for sprite in self.sprites:
            sprite.kill()
        for health in range(amount):
            x = 20 + health * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x, y), self.heart_frames, self.sprites)

    def display_text(self):
        '''
        Hien thi so tien cua nguoi choi
        '''
        text_surf = self.font.render(str(self.coin_amount), False, 'white')
        text_rect = text_surf.get_rect(topright=(1280 - 34, 20))
        self.display_surface.blit(text_surf, text_rect)
        coin_rect = self.coin_surf.get_rect(center=text_rect.bottomleft).move(-20, -20)
        self.display_surface.blit(self.coin_surf, coin_rect)

    def show_coins(self, amount):
        '''
        Khoi tao so tien cua nguoi choi
        '''
        self.coin_amount = amount

    def reset_coins(self):
        '''
        Dat lai so tien cua nguoi choi ve 0
        '''
        self.coin_amount = 0

    def update(self, data_time):
        '''
        Cap nhat thong tin so mang va so tien cua nguoi choi
        '''
        self.sprites.update(data_time)
        self.sprites.draw(self.display_surface)
        self.display_text()
class Heart(AnimatedSprite):
    '''
    class Heart ke thua tu lop AnimatedSprite de tao ra cac doi tuong do hoa la Heart trong tro choi
    '''
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False

    def animate(self, data_time):
        '''
        tao animation cho Heart
        '''
        self.frame_index += ANIMATION_SPEED * data_time
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0

    def update(self, data_time):
        '''
        cap nhat Heart theo thoi gian
        '''
        if self.active:
            self.animate(data_time)
        else:
            if randint(0, 150) == 1:
                self.active = True
