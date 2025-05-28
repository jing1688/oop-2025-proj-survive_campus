
import pygame
from constants import PLAYER_SIZE, PLAYER_COLOR,GOBLIN_IMAGE_PATH

def get_goblin_surface():
    # 這裡可以加入 Goblin 的圖片載入邏輯
    global _goblin_surface
    if _cat_surface is None:
        img = pygame.image.load(GOBLIN_IMAGE_PATH).convert_alpha()
        _cat_surface = pygame.transform.smoothscale(img, BUILDING_SIZE)
    return _goblin_surface
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.fullness = 10
        self.sleepiness = 10
        self.social = 0
        self.grade = 0

    def move(self, dx, dy, bounds, obstacles):
        # 移動 + 邊界檢查 + 障礙物碰撞
        old = self.rect.topleft
        self.rect.move_ip(dx, dy)
        self.rect.clamp_ip(bounds)
        if any(self.rect.colliderect(o.rect) for o in obstacles):
            self.rect.topleft = old

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)