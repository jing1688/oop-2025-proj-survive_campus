# entities/building.py

import pygame
from constants import *

# --------------------------------------------
# 全域快取：已載入並縮放好的 Surface
_surface_cache: dict[str, pygame.Surface] = {}
# --------------------------------------------

_KIND2PATH = {
    "cat"      : CAT_IMAGE_PATH,
    "gym"      : GYM_IMAGE_PATH,
    "library"  : LIBRARY_IMAGE_PATH,
    "club"     : CLUB_IMAGE_PATH,
    "McDonald" : McDonald_IMAGE_PATH,
    "house"    : HOUSE_IMAGE_PATH,
    "door"     : DOOR_IMAGE_PATH,
    # 其餘未知類型走 fallback
}
_FALLBACK_PATH = A_Building_Path

def get_surface(kind: str) -> pygame.Surface:
    """
    回傳對應 kind 的建築圖；已做大小縮放與快取。
    若 kind 不在表中 → 使用 _FALLBACK_PATH。
    """
    if kind in _surface_cache:
        return _surface_cache[kind]

    # 圖檔路徑
    path = _KIND2PATH.get(kind, _FALLBACK_PATH)
    surf = pygame.image.load(path).convert_alpha()
    surf = pygame.transform.smoothscale(surf, BUILDING_SIZE)

    _surface_cache[kind] = surf
    return surf


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
        cam_x, cam_y = offset
        draw_pos = (self.rect.x - cam_x, self.rect.y - cam_y)

        surf = get_surface(self.kind)
        screen.blit(surf, draw_pos)
        
        #若未來要依 kind 畫不同圖，請在這裡改成：
        # elif self.kind == "classroom":
        #     surf = get_classroom_surface()
        # else:
        #     surf = get_build_surface()
        # screen.blit(surf, (draw_x, draw_y))
