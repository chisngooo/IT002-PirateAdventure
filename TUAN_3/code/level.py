from settings import *
from sprites import Sprite,MovingSprite, AnimatedSprite, Item, ParticleEffectSprite
from player import Player
from groups import AllSprite, CollisionSprite, ToothSprite, DamageSprite, PearlSprite, ItemSprite
from enemies import Tooth,Shell, Pearl
from random import uniform

class Level:
    '''
    Khởi tạo và quản lý môi trường trò chơi, bao gồm các thiết lập cơ bản, cập nhật liên tục các sự kiện và xử lý tương tác giữa người chơi và trò chơi.
    '''
    def __init__(self,tmx_map, level_frames,data):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        # Khởi tạo all_sprites để quản lý tất cả các sprite trong trò chơi
        self.all_sprites = AllSprite()
        # Khởi tạo collision_sprites kế thừa từ lớp Group của pygame.sprite để quản lý các sprite va chạm trong trò chơi
        self.collision_sprites = CollisionSprite()
        # Khởi tạo tooth_sprites để quản lý các Tooth
        self.tooth_sprites = ToothSprite()
        # Khởi tạo damage_sprites để quản lý các sprite có thể gây sát thương
        self.damage_sprites = DamageSprite()
        # Khởi tạo pearl_sprites để quản lý các Pearl
        self.pearl_sprites = PearlSprite()
        # Khởi tạo item_sprites để quản lý các Item
        self.item_sprites = ItemSprite()
        # Khởi tạo môi trường trò chơi
        self.setup(tmx_map,level_frames)
        # Lấy các frame từ level_frames
        self.pearl_surf = level_frames['pearl']
        self.particle_frames = level_frames['particle']
        self.tooth_die_frames = level_frames['tooth_die']

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
                    frames=level_frames['player'],
                    data=self.data)
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
        # Tạo các sprite có tên Enemies trong bản đồ Tiled
        for obj in tmx_map.get_layer_by_name('Enemies'): 
            if obj.name == 'tooth': # nếu tên của object trong layer Enemies là tooth thì tạo ra  Tooth
                Tooth((obj.x,obj.y),level_frames['tooth'],(self.all_sprites,self.damage_sprites, self.tooth_sprites),self.collision_sprites)
            if obj.name == 'shell': # nếu tên của object trong layer Enemies là shell thì tạo ra  Shell
                Shell(
                    pos=(obj.x,obj.y),
                    frames =level_frames['shell'],
                    groups=(self.all_sprites,self.collision_sprites),
                    reverse=obj.properties['reverse'],
                    player=self.player,
                    create_pearl=self.create_pearl)
        # Tạo các sprite có tên Items trong bản đồ Tiled
        for obj in tmx_map.get_layer_by_name('Items'):
            Item(obj.name,(obj.x+TILE_SIZE/2,obj.y+TILE_SIZE/2),level_frames['items'][obj.name],(self.all_sprites,self.item_sprites),self.data)

    def create_pearl(self,pos,direction):
        '''
        tạo ra một Pearl theo vị trí và hướng di chuyển được chỉ định
        '''
        Pearl(pos,(self.all_sprites,self.damage_sprites,self.pearl_sprites),self.pearl_surf,direction,400)
    def pearl_collision(self):
        '''
        xử lý va chạm giữa Pearl và các sprite khác
        '''
        for sprite in self.collision_sprites: # lặp qua các sprite trong collision_sprites
            sprite = pygame.sprite.spritecollide(sprite,self.pearl_sprites,True) # kiểm tra xem có va chạm giữa sprite và các Pearl không
            if sprite: # nếu có va chạm
                ParticleEffectSprite((sprite[0].rect.center), self.particle_frames, self.all_sprites) # tạo ra hiệu ứng va chạm
    def hit_collision(self):
        '''
        xử lý va chạm giữa người chơi và các sprite có thể gây sát thương
        '''
        for sprite in self.damage_sprites: # lặp qua các sprite trong damage_sprites
            if sprite.rect.colliderect(self.player.hitbox_rect): # kiểm tra xem có va chạm giữa người chơi và các sprite có thể gây sát thương không
                self.player.get_damage() # nếu có va chạm thì người chơi bị gây sát thương
                if hasattr(sprite,'pearl'): # nếu sprite có thuộc tính pearl 
                    sprite.kill() # xóa sprite pearl
                    ParticleEffectSprite((sprite.rect.center), self.particle_frames, self.all_sprites) # tạo hiệu ứng va chạm
    def item_collision(self):
        '''
        xử lý va chạm giữa người chơi và các Item
        '''
        if self.item_sprites: # nếu có item_sprites
            item_sprites = [item for item in self.item_sprites if self.player.hitbox_rect.colliderect(item.rect)] # kiểm tra xem có va chạm giữa người chơi và các Item không
            for item in item_sprites:
                # nếu có va chạm thì người chơi nhặt Item đó và item biến mất, tạo hiệu ứng va chạm
                item.kill()
                item_sprites[0].activate()
                ParticleEffectSprite((item.rect.center), self.particle_frames, self.all_sprites)
    def attack_collision(self):
        '''
        xu ly va chạm giữa người chơi và các sprite có thể bị tấn công
        '''
        for target in self.pearl_sprites.sprites() + self.tooth_sprites.sprites(): # lặp qua các sprite trong pearl_sprites và tooth_sprites
            # kiểm tra xem có va chạm giữa người chơi và các sprite có thể bị tấn công không
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target: # nếu có va chạm và người chơi đang tấn công
                if hasattr(target, 'pearl'): # nếu target có thuộc tính pearl
                    target.reverse() # đảo hướng của target là pearl
                else: # nếu target là tooth
                    if not target.hit_timer.active: # nếu target không trong trạng thái bị tấn công (hit_timer không active)
                        
                        if not hasattr(target, 'hit_count'): 
                            target.hit_count = 0
                        target.hit_count += 1 # tăng hit_count lên 1

                        if target.hit_count == 1: # nếu hit_count = 1 thì đảo hướng của target (tooth)
                            target.reverse() 
                        elif target.hit_count >= 2: # nếu hit_count >= 2 thì target (tooth) chết
                            
                            target.die(self.tooth_die_frames)
                            
                        else: 
                            target.flicker()
                        target.hit_timer.activate()
                

    def run(self,data_time):
        '''
        Vòng lặp chạy trò chơi
        '''
        self.display_surface.fill('black')
        # Cập nhật tất cả các sprite trong all_sprites
        self.all_sprites.update(data_time)
        # xử lý va chạm giữa các sprite
        self.pearl_collision()
        self.hit_collision()
        self.item_collision()
        self.attack_collision()
        # Vẽ sprite player nằm ở giữa màn hình
        self.all_sprites.draw(self.player.hitbox_rect.center)
        