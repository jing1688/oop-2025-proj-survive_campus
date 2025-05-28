from constants import MAX_HOURS
# endings.py
# MAX_HOURS = 160     # 或直接 import constants 裡的

def check_game_over(player, hours_spent):
    # 1) 即時失敗判定（餓暈/累倒）同舊

    # 2) 時間還沒用完 → 遊戲繼續
    if hours_spent < MAX_HOURS:
        return False, None

    # 3) 用完 160h → 依成績等決定結局
    for e in FINAL_ENDINGS:
        if e["condition"](player, hours_spent):
            return True, e
    return False, None

EARLY_FAILS = [
    {"key": "餓暈", "condition": lambda p, h: p.fullness <= 0,  "image": None},
    {"key": "累到虛脫", "condition": lambda p, h: p.health <= -10, "image": None},
]

FINAL_ENDINGS = [
    {"key": "你線代無力，微積分不精\n物件導向反應遲鈍，微分方程知識鬆散\n沒一個科目像樣！", 
     "condition": lambda p, h: p.grade < 3,
     "image": "pictures/bad_end1.png"},
    # {"key": "AAA", "condition": lambda p, i: True, "image": None},   # default
]

def check_game_over(player, hours_spent):
    # 1) 即時失敗
    for e in EARLY_FAILS:
        if e["condition"](player, hours_spent):
            return True, e

   # 2) 時間還沒用完 → 遊戲繼續
    if hours_spent < MAX_HOURS:
        return False, None

    # 3) 用完 160h → 依成績等決定結局
    for e in FINAL_ENDINGS:
        if e["condition"](player, hours_spent):
            return True, e
    return False, None

