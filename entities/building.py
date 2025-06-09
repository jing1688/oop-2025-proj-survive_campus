# entities/building.py

import pygame
from constants import *
# --------------------------------------------
# 全域快取：貓咪圖片
_cat_surface = None

def get_cat_surface():
    global _cat_surface
    if _cat_surface is None:
        temp = pygame.image.load(CAT_IMAGE_PATH).convert_alpha()
        # 如果你想要 50×50 大小，可以改成 (50, 50)
        # 但通常建築大小跟 BUILDING_SIZE 一致較好：
        _cat_surface = pygame.transform.smoothscale(temp, BUILDING_SIZE)
    return _cat_surface

# 全域快取：其他自訂建築圖 (A_Building_Path)
_building_surface = None

def get_build_surface():
    global _building_surface
    if _building_surface is None:
        temp = pygame.image.load(A_Building_Path).convert_alpha()
        _building_surface = pygame.transform.smoothscale(temp, BUILDING_SIZE)
    return _building_surface
def get_gym_surface():
    surf = pygame.image.load(GYM_IMAGE_PATH).convert_alpha()
    return pygame.transform.smoothscale(surf, BUILDING_SIZE)

def get_library_surface():
    surf = pygame.image.load(LIBRARY_IMAGE_PATH).convert_alpha()
    return pygame.transform.smoothscale(surf, BUILDING_SIZE) 

def get_club_surface():
    surf = pygame.image.load(CLUB_IMAGE_PATH).convert_alpha()
    return pygame.transform.smoothscale(surf, BUILDING_SIZE)

def get_McDonald_surface():
    surf = pygame.image.load(McDonald_IMAGE_PATH).convert_alpha()
    # 假設沒有餐廳圖片，返回一個空的 Surface
    return pygame.transform.smoothscale(surf, BUILDING_SIZE)
def get_house_surface():
    surf = pygame.image.load(HOUSE_IMAGE_PATH).convert_alpha()
    return pygame.transform.smoothscale(surf, BUILDING_SIZE)

def get_door_surface():
    surf = pygame.image.load(DOOR_IMAGE_PATH).convert_alpha()
    return pygame.transform.smoothscale(surf, BUILDING_SIZE)
# --------------------------------------------
class Building:
    def __init__(self, x, y, kind):
        """
        x, y = 世界座標 (world_x, world_y)
        kind: "cat" / "restaurant" / "classroom" / 其他
        """
        self.kind        = kind
        self.rect        = pygame.Rect(x, y, *BUILDING_SIZE)
        self.detect_rect = self.rect.inflate(10, 10)

    def interact(self, player):
        """
        每次互動扣 1 點體力；若為 cat，回傳 "meow" 事件。
        否則執行 BUILDING_INFO[kind]["effect"] 的效果。
        """
        

        if self.kind == "cat":
            return "meow"
        BUILDING_INFO[self.kind]["effect"](player)
        return None

    def draw(self, screen, offset):
        """
        offset = (cam_x, cam_y)，表示鏡頭偏移量。
        world_x - cam_x  = 螢幕上的 x
        world_y - cam_y  = 螢幕上的 y
        """
        cam_x, cam_y = offset
        draw_x = self.rect.x - cam_x
        draw_y = self.rect.y - cam_y

        if self.kind == "cat":
            surf = get_cat_surface()
            screen.blit(surf, (draw_x, draw_y))
        elif self.kind == "gym":
            surf = get_gym_surface()
            screen.blit(surf, (draw_x, draw_y))
        elif self.kind == "library":
            surf = get_library_surface()
            screen.blit(surf, (draw_x, draw_y))
        elif self.kind == "club":
            surf = get_club_surface()
            screen.blit(surf, (draw_x, draw_y))
        elif self.kind == "McDonald":
            surf = get_McDonald_surface()
            screen.blit(surf, (draw_x, draw_y))
        elif self.kind == "house":
            surf = get_house_surface()
            screen.blit(surf, (draw_x, draw_y))
        elif self.kind == "door":
            surf = get_door_surface()
            screen.blit(surf, (draw_x, draw_y))
        else:
            surf = get_build_surface()
            screen.blit(surf, (draw_x, draw_y))
        
        #若未來要依 kind 畫不同圖，請在這裡改成：
        # elif self.kind == "classroom":
        #     surf = get_classroom_surface()
        # else:
        #     surf = get_build_surface()
        # screen.blit(surf, (draw_x, draw_y))
