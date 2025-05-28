# endings.py
MAX_INTERACTIONS = 10

EARLY_FAILS = [
    {"key": "餓暈", "condition": lambda p, i: p.fullness <= 0,  "image": None},
    {"key": "累到虛脫", "condition": lambda p, i: p.health <= -10, "image": None},
]

FINAL_ENDINGS = [
    {"key": "你線代無力，微積分不精\n物件導向反應遲鈍，微分方程知識鬆散\n沒一個科目像樣！", 
     "condition": lambda p, i: p.grade < 3,
     "image": "pictures/1662286848503.png"},
    # {"key": "AAA", "condition": lambda p, i: True, "image": None},   # default
]

def check_game_over(player, interactions):
    # 1) 即時失敗
    for e in EARLY_FAILS:
        if e["condition"](player, interactions):
            return True, e

    # 2) 未達互動上限 → 遊戲繼續
    if interactions < MAX_INTERACTIONS:
        return False, None

    # 3) 期末結局
    for e in FINAL_ENDINGS:
        if e["condition"](player, interactions):
            return True, e

    return False, None