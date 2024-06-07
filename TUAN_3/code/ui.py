from settings import *
from sprites import AnimatedSprite
from random import randint
from timeeeeeeeee import Timer


class UI:
    def __init__(self, font, frames):
        '''
        khởi tạo class UI để hiển thị thông tin về số mạng và số tiền của người chơi
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
        Tạo số mạng cho người chơi
        '''
        for sprite in self.sprites:
            sprite.kill()
        for health in range(amount):
            x = 20 + health * (self.heart_surf_width + self.heart_padding)
            y = 10
            Heart((x, y), self.heart_frames, self.sprites)

    def display_text(self):
        '''
        Hiển thị số tiền của người chơi
        '''
        text_surf = self.font.render(str(self.coin_amount), False, 'white')
        text_rect = text_surf.get_rect(topright=(1280 - 34, 20))
        self.display_surface.blit(text_surf, text_rect)
        coin_rect = self.coin_surf.get_rect(center=text_rect.bottomleft).move(-20, -20)
        self.display_surface.blit(self.coin_surf, coin_rect)

    def show_coins(self, amount):
        '''
        khởi tạo số tiền của người chơi
        '''
        self.coin_amount = amount

    def update(self, data_time):
        '''
        cập nhật thông tin số mạng và số tiền của người chơi
        '''
        self.sprites.update(data_time)
        self.sprites.draw(self.display_surface)
        self.display_text()

class Heart(AnimatedSprite):
    '''
    class Heart kế thừa từ AnimatedSprite để tạo ra frame cho heart và hiển thị lên màn hình
    '''
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.active = False

    def animate(self, data_time):
        '''
        tạo animation cho heart
        '''
        self.frame_index += ANIMATION_SPEED * data_time
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.active = False
            self.frame_index = 0

    def update(self, data_time):
        '''
        cập nhật thông tin cho heart
        '''
        if self.active:
            self.animate(data_time)
        else:
            if randint(0, 150) == 1:
                self.active = True
