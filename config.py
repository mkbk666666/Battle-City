"""
坦克大战游戏配置文件
包含游戏常量、颜色定义和方向常量
"""
from enum import Enum

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# 方向常量（使用枚举类型代替简单常量）
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

# 游戏状态
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

# 敌人参数
ENEMY_SPAWN_TIME = 600  # 每10秒生成新敌人
ENEMY_DIRECTION_CHANGE_CHANCE = 0.02  # 2%的几率改变方向
ENEMY_SHOOT_CHANCE = 0.01  # 1%的几率发射子弹

# 玩家参数
PLAYER_SPEED = 3
PLAYER_COOLDOWN = 30

# 子弹参数
BULLET_SPEED = 5
BULLET_DAMAGE = 25

# 墙壁参数
WALL_BREAKABLE_CHANCE = 0.7  # 70%的几率是可破坏的

# 爆炸效果参数
EXPLOSION_LIFETIME = 20

# 道具参数
POWER_UP_SPAWN_TIME = 900  # 每15秒生成一个道具
POWER_UP_MAX_COUNT = 3  # 场上最多同时存在的道具数量
POWER_UP_LIFETIME = 600  # 道具存在时间，10秒
POWER_UP_FLASH_INTERVAL = 10  # 道具闪烁间隔

# 道具效果参数
HEALTH_RESTORE_AMOUNT = 50  # 生命值恢复道具恢复的生命值
SPEED_BOOST_DURATION = 300  # 速度提升持续时间，5秒
SPEED_BOOST_MULTIPLIER = 1.5  # 速度提升倍数
SHIELD_DURATION = 300  # 护盾持续时间，5秒 