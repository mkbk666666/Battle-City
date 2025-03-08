import pygame
import sys
import random
import time
import os
from pygame.locals import *
from config import *  # 导入配置文件中的常量

# 初始化pygame
pygame.init()

# 尝试初始化音频系统，如果失败则禁用音频
try:
    pygame.mixer.init()
    audio_enabled = True
    print("音频系统初始化成功")
except:
    audio_enabled = False
    print("警告：音频系统初始化失败，游戏将在无声模式下运行")

# 加载音效
def load_sound(filename):
    if not audio_enabled:
        return None
        
    # 检查sounds文件夹是否存在，如果不存在则创建
    if not os.path.exists('sounds'):
        try:
            os.makedirs('sounds')
            print("创建sounds文件夹")
        except:
            print("无法创建sounds文件夹")
            return None
    
    sound_path = os.path.join('sounds', filename)
    # 检查音效文件是否存在
    if not os.path.exists(sound_path):
        print(f"警告：音效文件不存在: {sound_path}")
        return None
        
    try:
        sound = pygame.mixer.Sound(sound_path)
        return sound
    except:
        print(f"警告：无法加载音效: {sound_path}")
        return None

# 加载背景音乐
def load_music(filename):
    if not audio_enabled:
        return False
        
    # 检查sounds文件夹是否存在
    if not os.path.exists('sounds'):
        print("警告：sounds文件夹不存在，无法加载背景音乐")
        return False
    
    music_path = os.path.join('sounds', filename)
    # 检查音乐文件是否存在
    if not os.path.exists(music_path):
        print(f"警告：背景音乐文件不存在: {music_path}")
        return False
        
    try:
        pygame.mixer.music.load(music_path)
        return True
    except:
        print(f"警告：无法加载背景音乐: {music_path}")
        return False

# 游戏音效
sounds = {
    'shoot': load_sound('shoot.wav'),
    'explosion': load_sound('explosion.wav'),
    'hit': load_sound('hit.wav'),
    'power_up': load_sound('power_up.wav'),
    'game_over': load_sound('game_over.wav'),
    'level_up': load_sound('level_up.wav')
}

# 播放音效的函数
def play_sound(sound_name):
    if not audio_enabled:
        return
        
    if sound_name in sounds and sounds[sound_name]:
        try:
            sounds[sound_name].play()
        except:
            pass  # 忽略播放失败的情况

# 尝试加载背景音乐
background_music_loaded = load_music('background.mp3')

# 游戏对象基类
class GameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        pass

# 坦克类
class Tank(GameObject):
    def __init__(self, x, y, direction, speed, color, is_player=False):
        super().__init__(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.direction = direction
        self.speed = speed
        self.base_speed = speed  # 保存基础速度
        self.color = color
        self.is_player = is_player
        self.health = 100
        self.cooldown = 0
        self.cooldown_time = PLAYER_COOLDOWN if is_player else PLAYER_COOLDOWN * 2  # 发射子弹的冷却时间
        self.shield = 0  # 护盾持续时间
        self.speed_boost = 0  # 速度提升持续时间
    
    def update(self):
        # 更新冷却时间
        if self.cooldown > 0:
            self.cooldown -= 1
        
        # 更新护盾持续时间
        if self.shield > 0:
            self.shield -= 1
        
        # 更新速度提升持续时间
        if self.speed_boost > 0:
            self.speed_boost -= 1
            if self.speed_boost <= 0:
                self.speed = self.base_speed  # 恢复基础速度
        
        # 更新位置
        super().update()
    
    def apply_power_up(self, power_type):
        # 播放道具音效
        play_sound('power_up')
        
        if power_type == "health":
            self.health = min(100, self.health + HEALTH_RESTORE_AMOUNT)
        elif power_type == "speed":
            self.speed_boost = SPEED_BOOST_DURATION
            self.speed = self.base_speed * SPEED_BOOST_MULTIPLIER
        elif power_type == "shield":
            self.shield = SHIELD_DURATION
    
    def move(self, direction=None):
        if direction is not None:
            self.direction = direction
        
        # 根据方向移动
        if self.direction == Direction.UP:
            self.y -= self.speed
        elif self.direction == Direction.RIGHT:
            self.x += self.speed
        elif self.direction == Direction.DOWN:
            self.y += self.speed
        elif self.direction == Direction.LEFT:
            self.x -= self.speed
        
        # 边界检查
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        if self.y < 0:
            self.y = 0
        elif self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
        
        # 更新矩形位置
        self.update()
    
    def shoot(self):
        if self.cooldown <= 0:
            self.cooldown = self.cooldown_time
            # 根据坦克方向确定子弹的初始位置
            if self.direction == Direction.UP:
                bullet_x = self.x + self.width // 2 - 2
                bullet_y = self.y - 5
            elif self.direction == Direction.RIGHT:
                bullet_x = self.x + self.width
                bullet_y = self.y + self.height // 2 - 2
            elif self.direction == Direction.DOWN:
                bullet_x = self.x + self.width // 2 - 2
                bullet_y = self.y + self.height
            else:  # LEFT
                bullet_x = self.x - 5
                bullet_y = self.y + self.height // 2 - 2
            
            # 播放射击音效
            play_sound('shoot')
            
            return Bullet(bullet_x, bullet_y, self.direction, BULLET_SPEED, self.is_player)
        return None
    
    def draw(self, screen):
        # 绘制坦克主体
        pygame.draw.rect(screen, self.color, self.rect)
        
        # 绘制坦克炮管
        if self.direction == Direction.UP:
            pygame.draw.rect(screen, self.color, (self.x + self.width // 2 - 2, self.y - 5, 4, 5))
        elif self.direction == Direction.RIGHT:
            pygame.draw.rect(screen, self.color, (self.x + self.width, self.y + self.height // 2 - 2, 5, 4))
        elif self.direction == Direction.DOWN:
            pygame.draw.rect(screen, self.color, (self.x + self.width // 2 - 2, self.y + self.height, 4, 5))
        elif self.direction == Direction.LEFT:
            pygame.draw.rect(screen, self.color, (self.x - 5, self.y + self.height // 2 - 2, 5, 4))
        
        # 绘制生命值条
        health_width = (self.width * self.health) // 100
        pygame.draw.rect(screen, RED, (self.x, self.y - 5, self.width, 3))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 5, health_width, 3))
        
        # 如果有护盾，绘制护盾效果
        if self.shield > 0:
            shield_rect = pygame.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4)
            pygame.draw.rect(screen, BLUE, shield_rect, 2)  # 绘制蓝色边框表示护盾

# 子弹类
class Bullet(GameObject):
    def __init__(self, x, y, direction, speed, is_player_bullet):
        super().__init__(x, y, 4, 4)
        self.direction = direction
        self.speed = speed
        self.is_player_bullet = is_player_bullet
    
    def update(self):
        # 根据方向移动
        if self.direction == Direction.UP:
            self.y -= self.speed
        elif self.direction == Direction.RIGHT:
            self.x += self.speed
        elif self.direction == Direction.DOWN:
            self.y += self.speed
        elif self.direction == Direction.LEFT:
            self.x -= self.speed
        
        # 更新矩形位置
        super().update()
    
    def is_out_of_bounds(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or
                self.y < 0 or self.y > SCREEN_HEIGHT)
    
    def draw(self, screen):
        if self.is_player_bullet:
            pygame.draw.rect(screen, YELLOW, self.rect)
        else:
            pygame.draw.rect(screen, RED, self.rect)

# 墙壁类
class Wall(GameObject):
    def __init__(self, x, y, is_breakable=False):
        super().__init__(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.is_breakable = is_breakable
        self.health = 100 if is_breakable else float('inf')
    
    def hit(self, damage=BULLET_DAMAGE):
        if self.is_breakable:
            self.health -= damage
            return self.health <= 0
        return False
    
    def draw(self, screen):
        if self.is_breakable:
            color = GRAY  # 灰色可破坏墙
        else:
            color = DARK_GRAY  # 深灰色不可破坏墙
        pygame.draw.rect(screen, color, self.rect)

# 爆炸效果类
class Explosion(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.lifetime = EXPLOSION_LIFETIME
        self.current_frame = 0
    
    def update(self):
        self.current_frame += 1
        return self.current_frame >= self.lifetime
    
    def draw(self, screen):
        # 简单的爆炸动画
        size = int(BLOCK_SIZE * (1 - self.current_frame / self.lifetime))
        x_offset = (BLOCK_SIZE - size) // 2
        y_offset = (BLOCK_SIZE - size) // 2
        pygame.draw.rect(screen, RED, (self.x + x_offset, self.y + y_offset, size, size))

# 道具类
class PowerUp(GameObject):
    def __init__(self, x, y, power_type):
        super().__init__(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.type = power_type
        self.lifetime = POWER_UP_LIFETIME
        self.flash_timer = 0
        self.visible = True
    
    def update(self):
        super().update()
        self.lifetime -= 1
        
        # 闪烁效果，每10帧切换一次可见性
        self.flash_timer += 1
        if self.flash_timer >= POWER_UP_FLASH_INTERVAL:
            self.flash_timer = 0
            self.visible = not self.visible
        
        # 返回是否应该移除道具
        return self.lifetime <= 0
    
    def draw(self, screen):
        if not self.visible:
            return
            
        if self.type == "health":
            # 绘制生命值恢复道具
            pygame.draw.rect(screen, GREEN, self.rect)
            pygame.draw.rect(screen, RED, (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
        elif self.type == "speed":
            # 绘制速度提升道具
            pygame.draw.rect(screen, BLUE, self.rect)
            pygame.draw.rect(screen, WHITE, (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
        elif self.type == "shield":
            # 绘制护盾道具
            pygame.draw.rect(screen, YELLOW, self.rect)
            pygame.draw.circle(screen, BLUE, (self.x + self.width // 2, self.y + self.height // 2), self.width // 3)

# 游戏主类
class TankGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('坦克大战')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Microsoft YaHei', 36)
        # 为游戏结束文字使用更大更醒目的字体
        try:
            self.game_over_font = pygame.font.SysFont('SimHei', 48, bold=True)
        except:
            # 如果无法加载SimHei字体，则使用其他中文字体
            try:
                self.game_over_font = pygame.font.SysFont('Microsoft YaHei', 48, bold=True)
            except:
                # 如果所有中文字体都无法加载，使用系统默认字体
                self.game_over_font = pygame.font.SysFont(None, 48, bold=True)
        
        # 初始化游戏状态
        self.state = GameState.MENU
        
        # 初始化游戏变量
        self.player = None
        self.enemies = []
        self.bullets = []
        self.walls = []
        self.explosions = []
        self.power_ups = []
        self.power_up_timer = 0
        self.score = 0
        self.level = 1
        self.game_over = False
        self.enemy_spawn_timer = 0
        
        # 播放背景音乐
        if audio_enabled and background_music_loaded:
            try:
                pygame.mixer.music.set_volume(0.5)  # 设置音量
                pygame.mixer.music.play(-1)  # -1表示循环播放
            except:
                print("警告：无法播放背景音乐")
    
    def reset_game(self):
        # 初始化游戏状态
        self.player = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * BLOCK_SIZE, Direction.UP, PLAYER_SPEED, GREEN, True)
        self.enemies = []
        self.bullets = []
        self.walls = []
        self.explosions = []
        self.power_ups = []
        self.power_up_timer = 0
        self.score = 0
        self.level = 1
        self.game_over = False
        self.enemy_spawn_timer = 0
        self.state = GameState.PLAYING
        
        # 确保背景音乐正在播放
        if audio_enabled and background_music_loaded:
            try:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
            except:
                print("警告：无法播放背景音乐")
        
        # 创建初始敌人
        self.spawn_enemies(3)
        
        # 创建地图
        self.create_map()
    
    def create_map(self):
        # 创建边界墙
        for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
            self.walls.append(Wall(x, 0))
            self.walls.append(Wall(x, SCREEN_HEIGHT - BLOCK_SIZE))
        
        for y in range(BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE):
            self.walls.append(Wall(0, y))
            self.walls.append(Wall(SCREEN_WIDTH - BLOCK_SIZE, y))
        
        # 创建随机障碍物
        for _ in range(30):
            x = random.randint(1, (SCREEN_WIDTH // BLOCK_SIZE) - 2) * BLOCK_SIZE
            y = random.randint(1, (SCREEN_HEIGHT // BLOCK_SIZE) - 4) * BLOCK_SIZE
            
            # 确保不会在玩家坦克位置创建墙
            if abs(x - self.player.x) > BLOCK_SIZE * 2 or abs(y - self.player.y) > BLOCK_SIZE * 2:
                is_breakable = random.random() < WALL_BREAKABLE_CHANCE
                self.walls.append(Wall(x, y, is_breakable))
    
    def spawn_enemies(self, count):
        for _ in range(count):
            # 随机位置生成敌人
            while True:
                x = random.randint(1, (SCREEN_WIDTH // BLOCK_SIZE) - 2) * BLOCK_SIZE
                y = random.randint(1, (SCREEN_HEIGHT // BLOCK_SIZE) // 2) * BLOCK_SIZE
                
                # 确保不会与其他物体重叠
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                if not any(wall.rect.colliderect(rect) for wall in self.walls) and \
                   not any(enemy.rect.colliderect(rect) for enemy in self.enemies):
                    break
            
            direction = random.choice(list(Direction))
            self.enemies.append(Tank(x, y, direction, 1, RED))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_r and self.state == GameState.GAME_OVER:
                    print("R键被按下，重置游戏")
                    self.reset_game()
                elif event.key == K_SPACE:
                    if self.state == GameState.MENU:
                        self.reset_game()  # 从菜单开始游戏
                    elif self.state == GameState.PLAYING:
                        bullet = self.player.shoot()
                        if bullet:
                            self.bullets.append(bullet)
                elif event.key == K_p:  # 添加暂停/继续功能
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                        # 暂停背景音乐
                        if audio_enabled and background_music_loaded:
                            try:
                                pygame.mixer.music.pause()
                            except:
                                pass
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                        # 恢复背景音乐
                        if audio_enabled and background_music_loaded:
                            try:
                                pygame.mixer.music.unpause()
                            except:
                                pass
    
    def handle_player_movement(self):
        if self.state != GameState.PLAYING:
            return
        
        keys = pygame.key.get_pressed()
        moved = False
        
        # 保存当前位置
        old_x, old_y = self.player.x, self.player.y
        
        if keys[K_UP]:
            self.player.direction = Direction.UP
            self.player.move()
            moved = True
        elif keys[K_RIGHT]:
            self.player.direction = Direction.RIGHT
            self.player.move()
            moved = True
        elif keys[K_DOWN]:
            self.player.direction = Direction.DOWN
            self.player.move()
            moved = True
        elif keys[K_LEFT]:
            self.player.direction = Direction.LEFT
            self.player.move()
            moved = True
        
        # 检查碰撞
        if moved:
            for wall in self.walls:
                if self.player.rect.colliderect(wall.rect):
                    # 发生碰撞，恢复位置
                    self.player.x, self.player.y = old_x, old_y
                    self.player.update()
                    break
            
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy.rect):
                    # 发生碰撞，恢复位置
                    self.player.x, self.player.y = old_x, old_y
                    self.player.update()
                    break
    
    def update_enemies(self):
        if self.state != GameState.PLAYING:
            return
            
        for enemy in self.enemies:
            # 保存当前位置
            old_x, old_y = enemy.x, enemy.y
            
            # 随机改变方向和移动
            if random.random() < ENEMY_DIRECTION_CHANGE_CHANCE:
                enemy.direction = random.choice(list(Direction))
            
            enemy.move()
            
            # 检查碰撞
            collision = False
            for wall in self.walls:
                if enemy.rect.colliderect(wall.rect):
                    collision = True
                    break
            
            for other_enemy in self.enemies:
                if enemy != other_enemy and enemy.rect.colliderect(other_enemy.rect):
                    collision = True
                    break
            
            if enemy.rect.colliderect(self.player.rect):
                collision = True
            
            if collision:
                # 发生碰撞，恢复位置并随机选择新方向
                enemy.x, enemy.y = old_x, old_y
                enemy.update()
                enemy.direction = random.choice(list(Direction))
            
            # 随机发射子弹
            if random.random() < ENEMY_SHOOT_CHANCE:
                bullet = enemy.shoot()
                if bullet:
                    self.bullets.append(bullet)
    
    def update_bullets(self):
        if self.state != GameState.PLAYING:
            return
            
        # 更新所有子弹
        i = 0
        while i < len(self.bullets):
            bullet = self.bullets[i]
            bullet.update()
            
            # 检查是否出界
            if bullet.is_out_of_bounds():
                self.bullets.pop(i)
                continue
            
            # 检查子弹与墙壁的碰撞
            wall_hit = False
            for j, wall in enumerate(self.walls):
                if bullet.rect.colliderect(wall.rect):
                    wall_hit = True
                    # 播放击中音效
                    play_sound('hit')
                    # 如果墙是可破坏的，检查是否被摧毁
                    if wall.hit(BULLET_DAMAGE):
                        self.explosions.append(Explosion(wall.x, wall.y))
                        self.walls.pop(j)
                        # 播放爆炸音效
                        play_sound('explosion')
                    break
            
            if wall_hit:
                self.bullets.pop(i)
                continue
            
            # 检查子弹与坦克的碰撞
            if bullet.is_player_bullet:  # 玩家子弹
                for j, enemy in enumerate(self.enemies):
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.health -= BULLET_DAMAGE
                        self.explosions.append(Explosion(bullet.x, bullet.y))
                        self.bullets.pop(i)
                        # 播放击中音效
                        play_sound('hit')
                        
                        if enemy.health <= 0:
                            self.explosions.append(Explosion(enemy.x, enemy.y))
                            self.enemies.pop(j)
                            self.score += 100
                            # 播放爆炸音效
                            play_sound('explosion')
                            
                            # 如果所有敌人都被消灭，进入下一关
                            if len(self.enemies) == 0:
                                self.level += 1
                                self.spawn_enemies(min(3 + self.level, 10))
                                # 播放升级音效
                                play_sound('level_up')
                        break
                else:
                    i += 1
            else:  # 敌人子弹
                if bullet.rect.colliderect(self.player.rect):
                    # 如果玩家有护盾，不扣血但护盾减少
                    if self.player.shield > 0:
                        self.player.shield = max(0, self.player.shield - 100)  # 护盾减少
                    else:
                        self.player.health -= BULLET_DAMAGE
                    
                    self.explosions.append(Explosion(bullet.x, bullet.y))
                    self.bullets.pop(i)
                    # 播放击中音效
                    play_sound('hit')
                    
                    if self.player.health <= 0:
                        self.explosions.append(Explosion(self.player.x, self.player.y))
                        self.state = GameState.GAME_OVER
                        self.game_over = True
                        # 播放游戏结束音效
                        play_sound('game_over')
                        # 停止背景音乐
                        if audio_enabled and background_music_loaded:
                            try:
                                pygame.mixer.music.stop()
                            except:
                                pass
                else:
                    i += 1
    
    def update_explosions(self):
        # 更新所有爆炸效果
        i = 0
        while i < len(self.explosions):
            if self.explosions[i].update():
                self.explosions.pop(i)
            else:
                i += 1
    
    def draw(self):
        if self.state == GameState.MENU:
            self.draw_menu()
            return
            
        # 绘制背景
        self.screen.fill(BLACK)
        
        # 绘制墙壁
        for wall in self.walls:
            wall.draw(self.screen)
        
        # 绘制道具
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        
        # 绘制子弹
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # 绘制坦克
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # 绘制爆炸效果
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        # 绘制分数和等级
        score_text = self.font.render(f'分数: {self.score}', True, WHITE)
        level_text = self.font.render(f'等级: {self.level}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        
        # 如果游戏暂停，显示暂停信息
        if self.state == GameState.PAUSED:
            # 创建半透明背景
            overlay = pygame.Surface((SCREEN_WIDTH, 100))
            overlay.set_alpha(180)  # 设置透明度
            overlay.fill(BLACK)
            overlay_rect = overlay.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(overlay, overlay_rect)
            
            # 使用醒目的字体和颜色
            paused_text = self.game_over_font.render('游戏暂停', True, YELLOW)
            continue_text = self.font.render('按P键继续', True, WHITE)
            
            # 设置文本位置
            paused_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            
            # 绘制文本
            self.screen.blit(paused_text, paused_rect)
            self.screen.blit(continue_text, continue_rect)
        
        # 如果游戏结束，显示游戏结束信息
        elif self.state == GameState.GAME_OVER:
            # 创建半透明背景
            overlay = pygame.Surface((SCREEN_WIDTH, 100))
            overlay.set_alpha(180)  # 设置透明度
            overlay.fill(BLACK)
            overlay_rect = overlay.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(overlay, overlay_rect)
            
            # 使用更醒目的字体和颜色
            game_over_text = self.game_over_font.render('游戏结束!', True, RED)
            restart_text = self.font.render('按R键重新开始', True, YELLOW)
            
            # 设置文本位置
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            
            # 绘制文本
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # 更新显示
        pygame.display.flip()
    
    def draw_menu(self):
        # 绘制菜单背景
        self.screen.fill(BLACK)
        
        # 绘制游戏标题
        title_font = pygame.font.SysFont('SimHei', 64, bold=True)
        title_text = title_font.render('坦克大战', True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_text, title_rect)
        
        # 绘制开始游戏提示
        start_text = self.font.render('按空格键开始游戏', True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)
        
        # 绘制操作说明
        controls_text1 = self.font.render('方向键: 移动坦克', True, GREEN)
        controls_text2 = self.font.render('空格键: 发射子弹', True, GREEN)
        controls_text3 = self.font.render('P键: 暂停游戏', True, GREEN)
        controls_text4 = self.font.render('ESC键: 退出游戏', True, GREEN)
        
        controls_rect1 = controls_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        controls_rect2 = controls_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        controls_rect3 = controls_text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))
        controls_rect4 = controls_text4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180))
        
        self.screen.blit(controls_text1, controls_rect1)
        self.screen.blit(controls_text2, controls_rect2)
        self.screen.blit(controls_text3, controls_rect3)
        self.screen.blit(controls_text4, controls_rect4)
        
        # 更新显示
        pygame.display.flip()
    
    def run(self):
        while True:
            self.clock.tick(FPS)  # 使用配置文件中的FPS
            
            # 处理事件
            self.handle_events()
            
            # 处理玩家移动
            self.handle_player_movement()
            
            if self.state == GameState.PLAYING:
                # 更新敌人
                self.update_enemies()
                
                # 更新子弹
                self.update_bullets()
                
                # 更新道具
                self.update_power_ups()
                
                # 生成新敌人
                self.enemy_spawn_timer += 1
                if self.enemy_spawn_timer >= ENEMY_SPAWN_TIME and len(self.enemies) < 5 + self.level:
                    self.spawn_enemies(1)
                    self.enemy_spawn_timer = 0
            
            # 更新爆炸效果
            self.update_explosions()
            
            # 绘制游戏
            self.draw()

    def spawn_power_up(self):
        # 随机选择道具类型
        power_type = random.choice(["health", "speed", "shield"])
        
        # 随机位置生成道具
        while True:
            x = random.randint(1, (SCREEN_WIDTH // BLOCK_SIZE) - 2) * BLOCK_SIZE
            y = random.randint(1, (SCREEN_HEIGHT // BLOCK_SIZE) - 2) * BLOCK_SIZE
            
            # 确保不会与其他物体重叠
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            if not any(wall.rect.colliderect(rect) for wall in self.walls) and \
               not any(enemy.rect.colliderect(rect) for enemy in self.enemies) and \
               not self.player.rect.colliderect(rect) and \
               not any(power_up.rect.colliderect(rect) for power_up in self.power_ups):
                break
        
        # 创建道具
        self.power_ups.append(PowerUp(x, y, power_type))
        
    def update_power_ups(self):
        if self.state != GameState.PLAYING:
            return
            
        # 更新道具生成计时器
        self.power_up_timer += 1
        if self.power_up_timer >= POWER_UP_SPAWN_TIME and len(self.power_ups) < POWER_UP_MAX_COUNT:
            self.spawn_power_up()
            self.power_up_timer = 0
        
        # 更新所有道具
        i = 0
        while i < len(self.power_ups):
            if self.power_ups[i].update():
                self.power_ups.pop(i)
            else:
                # 检查玩家是否拾取道具
                if self.player.rect.colliderect(self.power_ups[i].rect):
                    self.player.apply_power_up(self.power_ups[i].type)
                    self.power_ups.pop(i)
                else:
                    i += 1

# 运行游戏
if __name__ == "__main__":
    game = TankGame()
    game.run()