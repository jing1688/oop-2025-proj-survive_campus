from constants import *
from constants import HOURS_PER_MONTH, MAX_HOURS, TOTAL_MONTHS
def draw_hud(screen, font, player, hours_spent):
    month = min(hours_spent // HOURS_PER_MONTH + 1, TOTAL_MONTHS)
    remain= MAX_HOURS - hours_spent
    txt = f"Month:{month}/{TOTAL_MONTHS}  Hour used:{hours_spent:.1f} /{MAX_HOURS}  Left:{remain:.1f}"
    # …照你原本方式 render 到畫面 …


#####目前的數值（飽足度、睡眠度、社交值、成績）和已經進行的互動次數，顯示在畫面左上角。
#####之後要隱藏，測試的時候確保數值更改正常