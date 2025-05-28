# import pygame
# from constants import BUILDING_SIZE, RESTAURANT_COLOR, CLASSROOM_COLOR

# class Building:
#     def __init__(self, x, y, kind):
#         self.rect = pygame.Rect(x, y, *BUILDING_SIZE)
#         self.detect_rect = self.rect.inflate(10, 10)
#         self.kind = kind  # "restaurant" or "classroom"

#     def interact(self, player):
#         player.sleepiness -= 1

#         if self.kind == "restaurant":
#             player.fullness = 10
#             player.social  += 1
#         elif self.kind == "classroom":
#             player.fullness -= 1
#             player.grade    += 1
#         elif self.kind == "cat":                       # ★ 新增
#             pass                     



#         # 其他屬性不動

#     def draw(self, screen):
#         color = RESTAURANT_COLOR if self.kind=="restaurant" else CLASSROOM_COLOR
#         pygame.draw.rect(screen, color, self.rect)
import pygame
from constants import BUILDING_SIZE, BUILDING_INFO, CAT_IMAGE_PATH

# --- 載入、快取圖片 ---
_cat_surface = None
def get_cat_surface():
    global _cat_surface
    if _cat_surface is None:
        img = pygame.image.load(CAT_IMAGE_PATH).convert_alpha()
        _cat_surface = pygame.transform.smoothscale(img, BUILDING_SIZE)
    return _cat_surface



class Building:
    def __init__(self, x, y, kind):
        self.kind = kind  # "restaurant", "classroom" 或 "cat"
        self.rect = pygame.Rect(x, y, *BUILDING_SIZE)
        self.detect_rect = self.rect.inflate(10, 10)

    def interact(self, player):
        # 通用：每次互動都消耗睡眠度
        player.sleepiness -= 1

        if self.kind == "cat":
            # 只回傳事件，由 main.py 控制播放音效 & 不改其他屬性
            return "meow"
        # 其它建築使用 BUILDING_INFO 表格裡的 effect
        BUILDING_INFO[self.kind]["effect"](player)
        return None

    def draw(self, screen):
        if self.kind == "cat":
            # 圖片繪製
            screen.blit(get_cat_surface(), self.rect)
        else:
            # 色塊繪製
            color = BUILDING_INFO[self.kind]["color"]
            pygame.draw.rect(screen, color, self.rect)