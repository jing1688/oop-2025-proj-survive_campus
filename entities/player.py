import pygame
from constants import PLAYER_SIZE, GOBLIN_IMAGE_PATH

# 模組層級暫存
_goblin_surface = None

def get_goblin_surface():
    global _goblin_surface
    if _goblin_surface is None:
        img = pygame.image.load(GOBLIN_IMAGE_PATH).convert_alpha()
        # 依 PLAYER_SIZE 或你想要的尺寸縮放
        _goblin_surface = pygame.transform.smoothscale(img, (PLAYER_SIZE, PLAYER_SIZE))
    return _goblin_surface

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.fullness = 10
        self.sleepiness = 10
        self.social = 0
        self.grade = 0
        self.money = 4000
        self.explore=0

    def move(self, dx, dy, bounds, obstacles):
        old = self.rect.topleft
        self.rect.move_ip(dx, dy)
        self.rect.clamp_ip(bounds)
        if any(self.rect.colliderect(o.rect) for o in obstacles):
            self.rect.topleft = old

    def draw(self, screen):
        # 用 blit 畫哥布林圖
        goblin_surf = get_goblin_surface()
        screen.blit(goblin_surf, self.rect.topleft)
