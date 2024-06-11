from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Item, ParticleEffectSprite
from player import Player
from groups import AllSprite, CollisionSprite, ToothSprite, DamageSprite, PearlSprite, ItemSprite
from enemies import Tooth, Shell, Pearl
from random import uniform

class Level:
    '''
    Khoi tao va quan ly moi truong tro choi, bao gom cac thiet lap co ban, cap nhat lien tuc cac su kien va xu ly tuong tac giua nguoi choi va tro choi.
    '''
    def __init__(self, tmx_map, level_frames, audio_files, data):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        # Lay chieu rong va chieu cao cua ban do Tiled
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        # Lay properties cua layer Data trong ban do Tiled
        tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
        if tmx_level_properties['bg']: # neu co bg thi lay bg_tile tu level_frames
            bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
        else: # neu khong co bg thi bg_tile = None
            bg_tile = None
        # Khoi tao all_sprites de quan ly tat ca cac sprite trong tro choi
        self.all_sprites = AllSprite(
            width = tmx_map.width,
            height = tmx_map.height,
            bg_tile = bg_tile,
            top_limit = tmx_level_properties['top_limit'],
            clouds = {'large': level_frames['cloud_large'], 'small': level_frames['cloud_small']},
            horizon_line = tmx_level_properties['horizon_line']
        )
        # Khoi tao collision_sprites ke thua tu lop Group cua pygame.sprite de quan ly cac sprite va cham trong tro choi
        self.collision_sprites = CollisionSprite()
        # Khoi tao tooth_sprites de quan ly cac Tooth
        self.tooth_sprites = ToothSprite()
        # Khoi tao damage_sprites de quan ly cac sprite co the gay sat thuong
        self.damage_sprites = DamageSprite()
        # Khoi tao pearl_sprites de quan ly cac Pearl
        self.pearl_sprites = PearlSprite()
        # Khoi tao item_sprites de quan ly cac Item
        self.item_sprites = ItemSprite()
        # Khoi tao moi truong tro choi
        self.setup(tmx_map, level_frames)
        # Lay cac frame tu level_frames
        self.pearl_surf = level_frames['pearl']
        self.particle_frames = level_frames['particle']
        self.tooth_die_frames = level_frames['tooth_die']
        # Thiet lap trang thai hoan thanh level
        self.completed = False
        # Am thanh trong tro choi
        self.gold_sound = audio_files['gold']
        self.gold_sound.set_volume(0.2)
        self.diamond_sound = audio_files['diamond']
        self.diamond_sound.set_volume(0.2)
        self.skull_sound = audio_files['skull']
        self.skull_sound.set_volume(0.2)
        self.pearl_sound = audio_files['pearl']
        self.death_sound = audio_files['death']
        self.death_sound.set_volume(0.4)
        self.complete_sound = audio_files['complete']
        self.complete_sound.set_volume(0.2)
        self.level_complete_timer = None

    def setup(self, tmx_map, level_frames):
        '''
        Thiet lap moi truong cho tro choi
        '''
        # Tao sprite co ten BG, Terrain, Grass trong ban do Tiled
        for layer in ['BG', 'Terrain', 'Grass']: # lap qua cac layer BG, Terrain, Grass trong ban do Tiled
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain':  # neu layer la Terrain thi them vao nhom collision_sprites
                    groups.append(self.collision_sprites)

                match layer: # xac dinh cac thu tu ve truoc sau cua cac sprite
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'Grass': z = Z_LAYERS['bg tiles']
                    case _: z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        # Tao sprite co ten BG details trong ban do Tiled
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == 'static': # neu ten cua object trong layer BG details la static sprite duoc tao la mot Sprite
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z = Z_LAYERS['bg details'])
            else: # neu ten cua object trong layer BG details khong phai la static thi sprite duoc tao la mot AnimatedSprite
                AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites, z = Z_LAYERS['bg details'])

        # Tao cac sprite co ten Objects trong ban do Tiled
        for obj in tmx_map.get_layer_by_name('Objects'):
            # Neu object co ten la player thi tao ra mot sprite Player
            if obj.name == 'player':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    groups = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    frames = level_frames['player'],
                    data = self.data
                )
            else: # Neu object do co ten khong phai la player sprite duoc tao ra la mot Sprite hoac AnimatedSprite
                if obj.name in ('barrel', 'crate'):
                    # object nay la mot Sprite
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
                else:
                    # object nay la mot AnimatedSprite
                    frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
                    groups = [self.all_sprites]
                    # xac dinh z index cua sprite
                    z = Z_LAYERS['bg details']
                    
                    # toc do animation cua sprite (neu la palm thi toc do animation se la mot so ngau nhien trong khoang tu ANIMATION_SPEED-1 den ANIMATION_SPEED+1 de dam bao cac cay palm chuyen dong khong dong deu )
                    animation_speed = ANIMATION_SPEED if not 'palm' in obj.name else ANIMATION_SPEED + uniform(-1, 1)
                    AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)
                if obj.name == 'flag':
                    self.level_finish_rect = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))
        # Tao cac sprite co ten Moving Objects trong ban do Tiled
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'boat': # chi xu li moi boat vi trong Moving Objects chi co boat
                frames = level_frames['boat']
                groups = (self.all_sprites, self.collision_sprites)
                if obj.width > obj.height: # xu li huong di chuyen cua moving object neu di chuyen theo chieu ngang
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else: # xu li huong di chuyen cua moving object neu di chuyen theo chieu doc
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed, obj.properties['flip'])
        # Tao cac sprite co ten Enemies trong ban do Tiled
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth': # neu ten cua object trong layer Enemies la tooth thi tao ra Tooth
                Tooth((obj.x, obj.y), level_frames['tooth'], (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)
            if obj.name == 'shell': # neu ten cua object trong layer Enemies la shell thi tao ra Shell
                Shell(
                    pos = (obj.x, obj.y),
                    frames = level_frames['shell'],
                    groups = (self.all_sprites, self.collision_sprites),
                    reverse = obj.properties['reverse'],
                    player = self.player,
                    create_pearl = self.create_pearl
                )
        # Tao cac sprite co ten Items trong ban do Tiled
        for obj in tmx_map.get_layer_by_name('Items'):
            self.item = Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)
        # Tao cac sprite co ten Water trong ban do Tiled
        for obj in tmx_map.get_layer_by_name('Water'):
            rows = int(obj.height / TILE_SIZE)
            cols = int(obj.width / TILE_SIZE)
            for row in range(rows):
                for col in range(cols):
                    x = obj.x + col * TILE_SIZE
                    y = obj.y + row * TILE_SIZE
                    if row == 0: # neu row = 0 thi tao ra song nuoc o tren
                        AnimatedSprite((x, y), level_frames['water_top'], (self.all_sprites), Z_LAYERS['water'])
                    else: # neu row != 0 thi tao ra nuoc binh thuong
                        Sprite((x, y), level_frames['water_body'], (self.all_sprites), Z_LAYERS['water'])
    
    def create_pearl(self, pos, direction):
        '''
        tao ra mot Pearl theo vi tri va huong di chuyen duoc chi dinh
        '''
        Pearl(pos, (self.all_sprites, self.damage_sprites, self.pearl_sprites), self.pearl_surf, direction, 400)
        self.pearl_sound.play()

    def pearl_collision(self):
        '''
        xu ly va cham giua Pearl va cac sprite khac
        '''
        for sprite in self.collision_sprites: # lap qua cac sprite trong collision_sprites
            sprite = pygame.sprite.spritecollide(sprite, self.pearl_sprites, True) # kiem tra xem co va cham giua sprite va cac Pearl khong
            if sprite: # neu co va cham
                ParticleEffectSprite((sprite[0].rect.center), self.particle_frames, self.all_sprites) # tao ra hieu ung va cham

    def hit_collision(self):
        '''
        xu ly va cham giua nguoi choi va cac sprite co the gay sat thuong
        '''
        for sprite in self.damage_sprites: # lap qua cac sprite trong damage_sprites
            if sprite.rect.colliderect(self.player.hitbox_rect): # kiem tra xem co va cham giua nguoi choi va cac sprite co the gay sat thuong khong
                self.player.get_damage() # neu co va cham thi nguoi choi bi gay sat thuong
                
                if hasattr(sprite, 'pearl'): # neu sprite co thuoc tinh pearl
                    sprite.kill() # xoa sprite pearl
                    ParticleEffectSprite((sprite.rect.center), self.particle_frames, self.all_sprites) # tao hieu ung va cham

    def item_collision(self):
        '''
        xu ly va cham giua nguoi choi va cac Item
        '''
        if self.item_sprites: # neu co item_sprites
            item_sprites = [item for item in self.item_sprites if self.player.hitbox_rect.colliderect(item.rect)] # kiem tra xem co va cham giua nguoi choi va cac Item khong
            for item in item_sprites:
                # neu co va cham thi nguoi choi nhat Item do va item bien mat, tao hieu ung va cham
                item.kill()
                item_sprites[0].activate()
                ParticleEffectSprite((item.rect.center), self.particle_frames, self.all_sprites)
                if item.item_type == 'silver': # neu item la gold (em luoi doi ten silver) thi phat am thanh gold
                    self.gold_sound.play()
                if item.item_type == 'diamond': # neu item la diamond thi phat am thanh diamond
                    self.gold_sound.play()
                if item.item_type == 'skull': # neu item la skull thi phat am thanh skull
                    self.skull_sound.play()
                
    def attack_collision(self):
        '''
        xu ly va cham giua nguoi choi va cac sprite co the bi tan cong
        '''
        for target in self.pearl_sprites.sprites() + self.tooth_sprites.sprites(): # lap qua cac sprite trong pearl_sprites va tooth_sprites
            # kiem tra xem co va cham giua nguoi choi va cac sprite co the bi tan cong khong
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target: # neu co va cham va nguoi choi dang tan cong
                if hasattr(target, 'pearl'): # neu target co thuoc tinh pearl
                    target.reverse() # dao huong cua target la pearl
                else: # neu target la tooth
                    if not target.hit_timer.active: # neu target khong trong trang thai bi tan cong (hit_timer khong active)
                        
                        if not hasattr(target, 'hit_count'): 
                            target.hit_count = 0
                        target.hit_count += 1 # tang hit_count len 1

                        if target.hit_count == 1: # neu hit_count = 1 thi dao huong cua target (tooth)
                            target.reverse() 
                        elif target.hit_count >= 2: # neu hit_count >= 2 thi target (tooth) chet
                            
                            target.die(self.tooth_die_frames)
                            
                        else: 
                            target.flicker()
                        target.hit_timer.activate()
                
    def check_constraint(self):
        '''
        Kiem tra rang buoc cua nguoi choi trong tro choi, neu nguoi choi cham vao bien thi nguoi choi se khong the di tiep,
        neu nguoi choi rot xuong bien thi nguoi choi se chet, neu nguoi choi cham vao co thi level se hoan thanh
        '''
        # Kiem tra truong hop nguoi choi cham vao bien trai, phai
        if self.player.hitbox_rect.left <= 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >= self.level_width:
            self.player.hitbox_rect.right = self.level_width
        # Kiem tra truong hop nguoi choi rot xuong bien
        if self.player.hitbox_rect.bottom > self.level_bottom:
            self.death_sound.play()
            self.data.health = -1
        # Kiem tra truong hop nguoi choi cham vao co
        if self.player.hitbox_rect.colliderect(self.level_finish_rect):
            if self.level_complete_timer is None:  # Neu timer chua duoc dat
                self.level_complete_timer = 1.0  # Dat timer cho 1 giay
                self.complete_sound.play()
            
    def run(self, data_time):
        '''
        Vong lap chay tro choi
        '''
        self.display_surface.fill('black')
        # Cap nhat tat ca cac sprite trong all_sprites
        self.all_sprites.update(data_time)
        # xu ly va cham giua cac sprite
        self.pearl_collision()
        self.hit_collision()
        self.item_collision()
        self.attack_collision()
        self.check_constraint()

        # Xu ly timer hoan thanh level
        if self.level_complete_timer is not None:
            self.level_complete_timer -= data_time
            if self.level_complete_timer <= 0:
                self.completed = True

        # Ve sprite player nam o giua man hinh
        self.all_sprites.draw(self.player.hitbox_rect.center, data_time)
