
import pygame
from constants import PLAYER_SIZE, PLAYER_COLOR

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