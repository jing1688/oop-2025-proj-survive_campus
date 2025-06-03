# entities/player.py

import pygame
from constants import PLAYER_SIZE, GOBLIN_IMAGE_PATH, ENERGY_MAX 

# --------------------------------------------
# 全域快取：玩家圖
_gob_surface = None

def get_goblin_surface():
    global _gob_surface
    if _gob_surface is None:
        tmp = pygame.image.load(GOBLIN_IMAGE_PATH).convert_alpha()
        _gob_surface = pygame.transform.smoothscale(tmp, (PLAYER_SIZE, PLAYER_SIZE))
    return _gob_surface

# --------------------------------------------
class Player:
    def __init__(self, x, y):
        """
        x, y 都是「世界座標」(world_x, world_y)，
        draw 時會扣掉 offset 才轉成螢幕座標。
        """
        self.rect         = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.health       = ENERGY_MAX
        self.health_max   = ENERGY_MAX
        self.money        = 4000
        self.energy       = 100
        self.social       = 0
        self.academics    = 0

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
        """
        offset = (cam_x, cam_y)：將世界座標轉成螢幕座標再畫圖。
        world_x - cam_x = 螢幕上的 x，world_y - cam_y = 螢幕上的 y。
        """
        cam_x, cam_y = offset
        draw_x = self.rect.x - cam_x
        draw_y = self.rect.y - cam_y
        surf = get_goblin_surface()
        screen.blit(surf, (draw_x, draw_y))
