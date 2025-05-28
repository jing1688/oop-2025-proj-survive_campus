import os, pygame
from constants import NOTO_FONT_PATH

def get_font(size=32):
    if os.path.exists(NOTO_FONT_PATH):
        return pygame.font.Font(NOTO_FONT_PATH, size)
    return pygame.font.SysFont("Microsoft JhengHei", size)