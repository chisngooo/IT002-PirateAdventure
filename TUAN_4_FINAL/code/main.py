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
        Khoi tao tro choi voi cac thiet lap co ban bao gom cua so tro choi, cac bien thoi gian va cac ban do tro choi
        '''
        # Khoi tao cua so tro choi
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # Dat caption cho cua so tro choi
        pygame.display.set_caption('Pirate Adventure')
        # Khoi tao thuoc tinh co ban cho tro choi
        self.clock = pygame.time.Clock()
        self.showing_tutorial = False
        self.running = False  
        self.import_assets()  
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.game_over = False
        
        # Load cac ban do tro choi
        self.tmx_maps = {
            0: load_pygame(join('tmx', 'map', 'map1_final.tmx')),
            1: load_pygame(join('tmx', 'map', 'map2_final.tmx')),
            2: load_pygame(join('tmx', 'map', 'map3_final.tmx')),
        }
        self.load_map = 0 # ban do dau tien se duoc load
        self.current_stage = Level(self.tmx_maps[self.load_map], self.level_frames, self.audio_files,self.data)
        # Khoi tao cac nut trong Menu
        self.start_button = pygame.Rect(WINDOW_WIDTH // 2.3, WINDOW_HEIGHT // 1.8, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.tutorial_button = pygame.Rect(WINDOW_WIDTH // 2.3, WINDOW_HEIGHT // 1.8 + 75, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.quit_button = pygame.Rect(WINDOW_WIDTH // 2.3, WINDOW_HEIGHT // 1.8 + 150, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.back_button = pygame.Rect(WINDOW_WIDTH // 2.3 + 10, WINDOW_HEIGHT // 1.8 + 170, BUTTON_WIDTH, BUTTON_HEIGHT)
        # Khoi tao cac nut trong Game Over Menu
        self.play_again_button = pygame.Rect(WINDOW_WIDTH // 2.2, WINDOW_HEIGHT // 1.93 - 6, BUTTON_WIDTH  , BUTTON_HEIGHT )
        self.main_menu_button = pygame.Rect(WINDOW_WIDTH // 2.2, WINDOW_HEIGHT // 2+ 122, BUTTON_WIDTH , BUTTON_HEIGHT )
        # Chay nhac nen
        self.bg_music.play(-1)

    def show_menu(self):
        '''
        Hien thi Menu tro choi va xu ly cac su kien voi thao tac chuot
        '''
        while not self.running:  # khi tro choi chua chay thi hien thi Menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    # Kiem tra nut nao duoc nhan
                    if self.start_button.collidepoint(event.pos): 
                        self.reset_to_first_map()  # Dat lai tro choi khi nhan "Start"
                    elif self.tutorial_button.collidepoint(event.pos):
                        self.showing_tutorial = True  # Hien thi huong dan khi nhan "Tutorial"
                    elif self.quit_button.collidepoint(event.pos) and not self.showing_tutorial: 
                        # Thoat tro choi
                        pygame.quit()
                        sys.exit()
                    elif self.back_button.collidepoint(event.pos) and self.showing_tutorial:
                        # Neu dang hien thi Menu huong dan va nhan nut BACK thi tro lai Menu chinh
                        self.showing_tutorial = False  # Tro lai Menu

            # Neu Menu huong dan khong duoc hien thi thi hien thi Menu chinh
            if not self.showing_tutorial:
                self.display_surface.blit(self.level_frames['menu'], (0, 0))
                self.draw_button("START", self.start_button, 70)
                self.draw_button("TUTORIAL", self.tutorial_button, 70)
                self.draw_button("QUIT", self.quit_button, 70)
            else:  # Hien thi Menu huong dan va nut BACK
                self.display_surface.blit(self.level_frames['tutorial'], (0, 0))
                self.draw_button("BACK", self.back_button, 70)

            pygame.display.update()
            self.clock.tick(45)

    def show_game_over_menu(self):
        '''
        Hien thi Menu Game Over va xu ly cac su kien voi thao tac chuot
        '''
        while self.game_over:  # Chi hien Menu khi game over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    # Kiem tra nut nao duoc nhan
                    if self.play_again_button.collidepoint(event.pos):
                        self.reset_to_first_map()  # Choi lai tu ban do dau tien neu nhan nut "PLAY AGAIN"
                    elif self.main_menu_button.collidepoint(event.pos):
                        self.game_over = False  # Tro ve menu chinh neu nhan nut "MAIN MENU"
                        self.show_menu() # Hiển thị menu chính
                    

            # Hien thi Menu game over
            self.display_surface.blit(self.level_frames['game_over'], (0, 0))  # Hien thi anh game over
            self.draw_button("PLAY AGAIN", self.play_again_button, 50) # Hien thi nut "PLAY AGAIN"
            self.draw_button("MAIN MENU", self.main_menu_button, 50) # Hien thi nut "MAIN MENU"
            self.draw_coins() # Hien thi so coins da thu thap duoc
            pygame.display.update()
            self.clock.tick(45)

    def draw_button(self, text, button, font_size):
        '''
        Ve nut voi van ban va mau duoc chi dinh
        '''
        mouse_pos = pygame.mouse.get_pos()
        # Dat mau sac dua tren viec chuot co dang tro vao nut hay khong 
        color = ('Black') if button.collidepoint(mouse_pos) else ('White')
        font = pygame.font.Font('tmx/graphics/ui/runescape_uf.ttf', font_size)

        # Tao hieu ung dam hon cho font chu  
        text_surface_black = font.render(text, True, (0, 0, 0))
        text_rect_black = text_surface_black.get_rect(center=(button.centerx + 2, button.centery + 2))
        self.display_surface.blit(text_surface_black, text_rect_black)

        # Tao chu len nut voi mau duoc chi dinh
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=button.center)
        self.display_surface.blit(text_surface, text_rect)

    def draw_coins(self):
        '''
        Ve so coins da thu thap duoc len man hinh
        '''
        font = pygame.font.Font('tmx/graphics/ui/runescape_uf.ttf', 50)
    
        # Ve text voi mau duong vien
        outline_surface = font.render(f"Coins: {self.coins}", True, 'Black')
        outline_rect = outline_surface.get_rect(center=(WINDOW_WIDTH // 1.82, WINDOW_HEIGHT // 3.3 + 50))
    
        # Ve text chinh
        text_surface = font.render(f"Coins: {self.coins}", True, 'White')
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 1.82 - 2, WINDOW_HEIGHT // 3.3 + 50 - 2))
    
        # tao vien cho text
        self.display_surface.blit(outline_surface, outline_rect)
        self.display_surface.blit(text_surface, text_rect)

    def import_assets(self):
        '''
        Import cac assets cua tro choi tu cac folder hoac tu cac folder lon chua cac folder con va trong cac folder co cac hinh anh duoc danh so thu tu de tao animation cho sprite hoac
        co the la ca font chu
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
            'game_over': pygame.image.load('tmx/map/game_over.png'),
            'tooth': import_folder('tmx', 'graphics', 'enemies', 'tooth', 'run'),
            'tooth_die': import_folder('tmx', 'graphics', 'enemies', 'tooth', 'die'),
            'shell': import_sub_folders('tmx', 'graphics', 'enemies', 'shell'),
            'pearl': import_image('tmx', 'graphics', 'enemies', 'bullets', 'pearl'),
            'items': import_sub_folders('tmx', 'graphics', 'items'),
            'particle': import_folder('tmx', 'graphics', 'effects', 'particle'),
            'water_top': import_folder('tmx', 'graphics', 'level', 'water', 'top'),
            'water_body': import_image('tmx', 'graphics', 'level', 'water', 'body'),
            'bg_tiles' : import_folder_dict('tmx', 'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('tmx', 'graphics', 'level', 'clouds', 'small'),
            'cloud_large': import_image('tmx', 'graphics', 'level', 'clouds', 'large_cloud'),
        }
        self.font = pygame.font.Font('tmx/graphics/ui/runescape_uf.ttf', 40)
        self.ui_frames = {
            
            'coin': import_image('tmx', 'graphics', 'ui', 'coin'),
            'heart': import_folder('tmx', 'graphics', 'ui', 'heart'),
        }
        self.audio_files ={
            'gold': pygame.mixer.Sound('tmx/audio/gold.wav'),
            'diamond': pygame.mixer.Sound('tmx/audio/diamond.wav'),
            'skull': pygame.mixer.Sound('tmx/audio/skull.wav'),
            'complete': pygame.mixer.Sound('tmx/audio/complete.wav'),
            'pearl': pygame.mixer.Sound('tmx/audio/pearl.wav'),
            'death': pygame.mixer.Sound('tmx/audio/death.wav'),

        }
        self.bg_music = pygame.mixer.Sound('tmx/audio/drunken_tailor.mp3')
        self.bg_music.set_volume(0.3)

    def reset_game(self):
        '''
        Reset game 
        '''
        self.data = Data(self.ui)
        self.current_stage = Level(self.tmx_maps[self.load_map], self.level_frames,self.audio_files, self.data)
        self.coins = 0
        self.current_stage.completed = False
        self.showing_tutorial = False
        self.game_over = False
        self.running = True
        self.ui.reset_coins()  # Reset so coins ve 0

    def reset_to_first_map(self):
        '''
        Dat lai tro choi ve ban do dau tien di cung voi viec reset cac thong so co ban cua tro choi (reset game())
        '''
        self.load_map = 0
        self.reset_game()

    def run(self):
        '''
        Chay tro choi
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
                # Kiem tra neu data.health = -1 thi game over
                if self.data.health == -1:
                    self.running = False
                    self.game_over = True

                pygame.display.update()
                self.coins = self.data.coins
                if self.current_stage.completed:
                    self.load_map += 1
                    if self.load_map == 3:
                        print("You win!")
                        self.running = False
                        self.game_over = True
                    else:
                        self.current_stage = Level(self.tmx_maps[self.load_map], self.level_frames, self.audio_files, self.data)
            elif self.game_over:
                self.show_game_over_menu()
            else:
                self.show_menu()

if __name__ == '__main__':
    game = Game()

    game.run()
    
    
    
