# entities/player.py
from acitivies.club import Club
import pygame
from constants import PLAYER_SIZE, GOBLIN_IMAGE_PATH, ENERGY_MAX,BOY_IMAGE_PATH

# --------------------------------------------
# 全域快取：玩家圖
_gob_surface = None

def get_goblin_surface():
    global _gob_surface
    if _gob_surface is None:
        tmp = pygame.image.load(GOBLIN_IMAGE_PATH).convert_alpha()
        _gob_surface = pygame.transform.smoothscale(tmp, (PLAYER_SIZE, PLAYER_SIZE))
    return _gob_surface

# 新增：男生圖片快取
_boy_surface = None
def get_boy_surface():
    global _boy_surface
    if _boy_surface is None:
        tmp = pygame.image.load(BOY_IMAGE_PATH).convert_alpha()
        _boy_surface = pygame.transform.smoothscale(tmp, (PLAYER_SIZE, PLAYER_SIZE))
    return _boy_surface
# --------------------------------------------
class Player:
    def __init__(self, x, y):
        """
        x, y 都是「世界座標」(world_x, world_y)，
        draw 時會扣掉 offset 才轉成螢幕座標。
        """
        self.rect         = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.health       = 0
        self.money        = 0
        self.energy       = 100
        self.energy_max   = ENERGY_MAX
        self.social       = 0
        self.academics    = 0
        self.explore      = 0
        self.finance      = 0
        self.club = Club(self)
    def move(self, dx, dy, bounds, obstacles):
        """
        dx, dy = 世界座標增量（速度 * 時間）
        bounds: pygame.Rect (螢幕範圍，用來 clamp)
        obstacles: 建築物列表，用來檢查碰撞。
        """
        old = self.rect.topleft
        self.rect.move_ip(dx, dy)
        self.rect.clamp_ip(bounds)
        if any(self.rect.colliderect(o.rect) for o in obstacles):
            self.rect.topleft = old

    def draw(self, screen, offset):
        cam_x, cam_y = offset
        draw_x = self.rect.x - cam_x
        draw_y = self.rect.y - cam_y

        # 條件：health 或 academics > 20 就換帥哥
        if self.health > 20 or self.academics > 20:
            surf = get_boy_surface()
        else:
            surf = get_goblin_surface()

        screen.blit(surf, (draw_x, draw_y))