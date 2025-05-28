from constants import *
def draw_hud(screen, font, player, interactions):
    text = f"飽足:{player.fullness} 睡眠:{player.sleepiness} 社交:{player.social} 成績:{player.grade} 互動:{interactions}/10"
    surf = font.render(text, True, (0,0,0))
    screen.blit(surf, (10,10))

#####目前的數值（飽足度、睡眠度、社交值、成績）和已經進行的互動次數，顯示在畫面左上角。
#####之後要隱藏，測試的時候確保數值更改正常