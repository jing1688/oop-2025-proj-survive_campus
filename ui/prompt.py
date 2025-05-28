# ui/prompt.py
import pygame
from constants import WIDTH, HEIGHT
import textwrap
def draw_choices(screen, font, choices, topleft=None):
    """
    在畫面上顯示一組選項列表 choices = [(label, text), ...]。
    topleft: (x,y) 決定起始位置，若 None，則預設放右上。
    """
    padding = 8
    # 計算起始座標
    if topleft is None:
        x0 = WIDTH - padding
        y0 = padding
    else:
        x0, y0 = topleft

    for label, txt in choices:
        line_surf = font.render(f"{label}. {txt}", True, (255,255,255))
        bg = pygame.Surface((line_surf.get_width()+padding, line_surf.get_height()+padding))
        bg.set_alpha(150)
        bg.fill((0,0,0))
        # 貼背景和文字
        screen.blit(bg, (x0 - bg.get_width(), y0))
        screen.blit(line_surf, (x0 - line_surf.get_width(), y0 + padding//2))
        y0 += line_surf.get_height() + padding


def draw_prompt(screen, font, text, feedback=False):
    """
    畫一行提示文字，預設置底部中央，可透過 feedback 參數將位置提升。
    feedback=True 時文字顯示在畫面上方 20%。
    """
    surf = font.render(text, True, (255,255,255))
    bg = pygame.Surface((surf.get_width()+10, surf.get_height()+10))
    bg.set_alpha(150)
    bg.fill((0,0,0))
    x = (WIDTH - surf.get_width()) // 2
    if feedback:
        y = int(HEIGHT * 0.2)
    else:
        y = HEIGHT - surf.get_height() - 50
    screen.blit(bg, (x-5, y-5))
    screen.blit(surf, (x, y))
    
def draw_end(screen, font, msg1, msg2, bg=(200,200,200), wrap_width=40, y_start=None):
    """
    清空畫面並顯示結束訊息，支援手動換行或自動換行。
    y_start: 第一行文字的起始 y 座標，若 None 則用 HEIGHT//4。
    """
    screen.fill(bg)
    # 如果傳了 y_start 就用它，否則預設從 1/4 高度開始
    y = HEIGHT//4 if y_start is None else y_start

    for text, color in [(msg1, (255,0,0)), (msg2, (0,0,0))]:
        if "\n" in text:
            lines = text.split("\n")
        else:
            import textwrap
            lines = textwrap.wrap(text, wrap_width)
        for line in lines:
            surf = font.render(line, True, color)
            x = (WIDTH - surf.get_width())//2
            screen.blit(surf, (x, y))
            y += surf.get_height() + 5
        y += 10

    pygame.display.flip()
    return y