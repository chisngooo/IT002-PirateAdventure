from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from pygame.locals import MOUSEBUTTONDOWN
from data import Data
from support import *
from ui import UI
class Game:
    def __init__(self):
        '''
        Khởi tạo trò chơi với các thiết lập cơ bản bao gồm cửa sổ trò chơi, các biến thời gian và các bản đồ trò chơi
        '''
        # Khởi tạo cửa sổ trò chơi
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # Đặt caption cho cửa sổ trò chơi
        pygame.display.set_caption('Pirate Adventure')
        # Khởi tạo thuộc tính cơ bản cho trò chơi
        self.clock = pygame.time.Clock()
        self.showing_tutorial = False
        self.running = False  
        self.import_assets()  
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        # Load các bản đồ trò chơi
        
        self.tmx_maps = {
            0: load_pygame(join('tmx', 'map', 'map1_final.tmx')),
            1: load_pygame(join('tmx', 'map', 'map2_final.tmx')),
            2: load_pygame(join('tmx', 'map', 'map3_final.tmx')),
        }
        self.current_stage = Level(self.tmx_maps[1], self.level_frames,self.data)
        # Khởi tạo các nút trong Menu
        self.start_button = pygame.Rect(WINDOW_WIDTH // 2.3, WINDOW_HEIGHT // 1.8, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.tutorial_button = pygame.Rect(WINDOW_WIDTH // 2.3, WINDOW_HEIGHT // 1.8 + 75, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.quit_button = pygame.Rect(WINDOW_WIDTH // 2.3, WINDOW_HEIGHT // 1.8 + 150, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.back_button = pygame.Rect(WINDOW_WIDTH // 2.3 + 10, WINDOW_HEIGHT // 1.8 + 170, BUTTON_WIDTH, BUTTON_HEIGHT)

    def show_menu(self):
        '''
        Hiển thị Menu trò chơi và xử lý các sự kiện với click chuột
        '''
        while not self.running:  # Chỉ hiện Menu khi trò chơi chưa bắt đầu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    # Kiểm tra nút nào được nhấn
                    if self.start_button.collidepoint(event.pos):
                        self.running = True  # Bắt đầu trò chơi
                    elif self.tutorial_button.collidepoint(event.pos):
                        self.showing_tutorial = True  # Hiển thị hướng dẫn
                    elif self.quit_button.collidepoint(event.pos) and not self.showing_tutorial:
                        # Thoát trò chơi
                        pygame.quit()
                        sys.exit()
                    elif self.back_button.collidepoint(event.pos) and self.showing_tutorial:
                        # Nếu đang hiển thị Menu hướng dẫn và nhấn nút BACK thì trở lại Menu chính
                        self.showing_tutorial = False  # Trở lại Menu

            # Nếu Menu hướng dẫn không được hiển thị thì hiển thị Menu chính
            if not self.showing_tutorial:
                self.display_surface.blit(self.level_frames['menu'], (0, 0))
                self.draw_button("START", self.start_button)
                self.draw_button("TUTORIAL", self.tutorial_button)
                self.draw_button("QUIT", self.quit_button)
            else:  # Hiển thị Menu hướng dẫn và nút BACK
                self.display_surface.blit(self.level_frames['tutorial'], (0, 0))
                self.draw_button("BACK", self.back_button)

            pygame.display.update()
            self.clock.tick(45)  

    def draw_button(self, text, button):
        '''
        Vẽ nút với văn bản và màu được chỉ định
        '''
        mouse_pos = pygame.mouse.get_pos()
        # Đặt màu sắc dựa trên việc chuột có đang trỏ vào nút hay không 
        color = ('Black') if button.collidepoint(mouse_pos) else ('White')
        font = pygame.font.Font('tmx/graphics/ui/runescape_uf.ttf', 70)
    
        # Tạo hiệu ứng đậm hơn cho font chữ  
        text_surface_black = font.render(text, True, (0, 0, 0))
        text_rect_black = text_surface_black.get_rect(center=(button.centerx + 2, button.centery + 2))
        self.display_surface.blit(text_surface_black, text_rect_black)
    
        # Tạo chữ lên nút với màu được chỉ định
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=button.center)
        self.display_surface.blit(text_surface, text_rect)

    def import_assets(self):
        '''
        Import các assets của trò chơi từ các folder hoặc từ các folder lớn chứa các folder con và trong các folder có các hình ảnh được đánh số thứ tự để tạo animation cho sprite hoặc
        có thể là cả font chữ
        '''
        self.level_frames = {
            'flag': import_folder('tmx', 'graphics', 'level', 'flag'),
            'palms': import_sub_folders('tmx', 'graphics', 'level', 'palms'),
            'candle': import_folder('tmx', 'graphics', 'level', 'candle'),
            'window': import_folder('tmx', 'graphics', 'level', 'window'),
            'big_chain': import_folder('tmx', 'graphics', 'level', 'big_chains'),
            'small_chain': import_folder('tmx', 'graphics', 'level', 'small_chains'),
            'player': import_sub_folders('tmx', 'graphics', 'player', 'player2'),
            'boat': import_folder('tmx', 'graphics', 'objects', 'boat'),
            'menu': pygame.image.load('tmx/map/menu.png'),
            'tutorial': pygame.image.load('tmx/map/tutorial.png'),
            'tooth': import_folder('tmx', 'graphics', 'enemies', 'tooth', 'run'),
            'tooth_die': import_folder('tmx', 'graphics', 'enemies', 'tooth', 'die'),
            'shell': import_sub_folders('tmx', 'graphics', 'enemies', 'shell'),
            'pearl': import_image('tmx', 'graphics', 'enemies', 'bullets', 'pearl'),
            'items': import_sub_folders('tmx', 'graphics', 'items'),
            'particle': import_folder('tmx', 'graphics', 'effects', 'particle'),
        }
        self.font = pygame.font.Font('tmx/graphics/ui/runescape_uf.ttf', 40)
        self.ui_frames = {
            
            'coin': import_image('tmx', 'graphics', 'ui', 'coin'),
            'heart': import_folder('tmx', 'graphics', 'ui', 'heart'),
        }
    def run(self):
        '''
        Chạy trò chơi
        '''
        while True:
            if self.running:
                data_time = self.clock.tick(45) / 1000
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                self.current_stage.run(data_time)
                self.ui.update(data_time)
                
                pygame.display.update()
                
            else:
                self.show_menu()

if __name__ == '__main__':
    game = Game()
    game.run()
