from settings import *
from sprites import Sprite,MovingSprite, AnimatedSprite
from player import Player
from groups import AllSprite, CollisionSprite
from random import uniform
class Level:
    '''
    Khởi tạo và quản lý môi trường trò chơi, bao gồm các thiết lập cơ bản, cập nhật liên tục các sự kiện và xử lý tương tác giữa người chơi và trò chơi.
    '''
    def __init__(self,tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()

        # Khởi tạo all_sprites để quản lý tất cả các sprite trong trò chơi
        self.all_sprites = AllSprite()
        # Khởi tạo collision_sprites kế thừa từ lớp Group của pygame.sprite để quản lý các sprite va chạm trong trò chơi
        self.collision_sprites = CollisionSprite()
        # Khởi tạo môi trường trò chơi
        self.setup(tmx_map,level_frames)
        
    def setup(self,tmx_map,level_frames):
        '''
        Thiết lập môi trường cho trò chơi
        '''
        # Tạo sprite có tên BG, Terrain, Grass trong bản đồ Tiled
        for layer in ['BG','Terrain','Grass']: # lặp qua các layer BG, Terrain, Grass trong bản đồ Tiled
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles(): 
                groups = [self.all_sprites]
                if layer == 'Terrain':  # nếu layer là Terrain thì thêm vào nhóm collision_sprites 
                    groups.append(self.collision_sprites)
               
                match layer: # xác định các thứ tự vẽ trước sau của các sprite
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'Grass': z = Z_LAYERS['bg tiles'] 
                    case _: z = Z_LAYERS['main']
                Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,groups,z)
        
        # Tạo sprite có tên BG details trong bản đồ Tiled
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == 'static': # nếu tên của object trong layer BG details là static sprite được tạo là một Sprite
                Sprite((obj.x,obj.y),obj.image,self.all_sprites,z=Z_LAYERS['bg details'])
            else: # nếu tên của object trong layer BG details không phải là static thì sprite được tạo là một AnimatedSprite
                AnimatedSprite((obj.x,obj.y),level_frames[obj.name],self.all_sprites,z=Z_LAYERS['bg details'])

        # Tạo các sprite có tên Objects trong bản đồ Tiled
        for obj in tmx_map.get_layer_by_name('Objects'):
            # Nếu object có tên là player thì tạo ra một sprite Player
            if obj.name == 'player':
                self.player = Player(
                    pos = (obj.x,obj.y),
                    groups=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    frames=level_frames['player'])
            else: # Nếu object đó có tên không phải là player sprite được tạo ra là một Sprite hoặc AnimatedSprite
                if obj.name in ('barrel','crate'):
                    # object này là một Sprite
                    Sprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))
                else:
                    # object này là một AnimatedSprite
                    frames = level_frames[obj.name] if not 'palm'  in obj.name else level_frames['palms'][obj.name] 
                    groups = [self.all_sprites]
                    # xác định z index của sprite
                    z = Z_LAYERS['bg details'] 
                    
                    # tóc độ animation của sprite (nếu là palm thì tốc độ animation sẽ là một số ngẫu nhiên trong khoảng từ ANIMATION_SPEED-1 đến ANIMATION_SPEED+1 để đảm bảo các cây palm chuyển động không đồng đều )
                    animation_speed = ANIMATION_SPEED if not 'palm' in obj.name else ANIMATION_SPEED + uniform(-1,1) 
                    AnimatedSprite((obj.x,obj.y),frames,groups,z,animation_speed)
                
        # Tạo các sprite có tên Moving Objects trong bản đồ Tiled
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'boat': # chỉ xử lí mỗi boat vì trong Moving Objects chỉ có boat
                frames = level_frames['boat']
                groups = (self.all_sprites,self.collision_sprites) 
                if obj.width > obj.height: # xử lí hướng di chuyển của moving object nếu di chuyên theo chiều ngang
                    move_dir = 'x'
                    start_pos = (obj.x,obj.y+obj.height/2)
                    end_pos = (obj.x+obj.width,obj.y+obj.height/2)
                else: # xử lí hướng di chuyển của moving object nếu di chuyển theo chiều dọc
                    move_dir = 'y'
                    start_pos = (obj.x+obj.width/2,obj.y)
                    end_pos = (obj.x+obj.width/2,obj.y+obj.height)
                speed = obj.properties ['speed']
                MovingSprite(frames,groups,start_pos,end_pos,move_dir,speed,obj.properties['flip'])
    def run(self,data_time):
        '''
        Vòng lặp chạy trò chơi
        '''
        self.display_surface.fill('black')
        # Cập nhật tất cả các sprite trong all_sprites
        self.all_sprites.update(data_time)
        # Vẽ sprite player nằm ở giữa màn hình
        self.all_sprites.draw(self.player.hitbox_rect.center)
