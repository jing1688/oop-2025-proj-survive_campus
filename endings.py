# endings.py －－放在 constants 之後匯入
from constants import MAX_HOURS

# ─────────────────────────────
# 1. 即時失敗（立刻 Game-Over）
# ─────────────────────────────
EARLY_FAILS = [
    # 餓暈：能量歸零
    {"key": "你餓暈在校園角落⋯⋯", "condition": lambda p, h: p.energy <= -10, "image": None},
    # 累到虛脫：健康過低
    {"key": "你累到虛脫，被送進保健室", "condition": lambda p, h: p.health <= -10, "image": None},
]

# ─────────────────────────────
# 2. 期末（160h）結局
#    依照圖片中的五條規則，從 A → E 依序判斷
# ─────────────────────────────
FINAL_ENDINGS = [
    # 結局 A ─ 超級大學生
    {
        "key": "結局A  超級大學生",
        "condition": lambda p, h:
            (p.academics + p.social + p.health + p.finance) / 4 >= 80
            and p.explore >= 60,
        "image": "pictures/ending_A.png",   # 若還沒準備好圖，改成 None
    },

    # 結局 B ─ 平穩的大學生生活
    {
        "key": "結局B  平穩的大學生生活",
        "condition": lambda p, h: (
            (p.academics + p.social + p.health) / 3 >= 50
            and min(p.academics, p.social, p.health) < 80      # 至少有一科 < 80
        ),
        "image": "pictures\OIP.jpg",
    },

    # 結局 C ─ 孤單結局
    {
        "key": "結局C  孤單結局",
        "condition": lambda p, h: p.social < 30 and p.academics >= 50,
        "image": "pictures/ending_C.png",
    },

    # 結局 D ─ 被二一邊緣
    {
        "key": "結局D  被二一邊緣",
        "condition": lambda p, h: p.academics < 30,
        "image": "pictures/bad_end1.png",
    },

    # 結局 E ─ 不能生活（健康或金錢崩盤）
    {
        "key": "結局E  不能生活",
        "condition": lambda p, h: p.health < 25 or p.money < -2000,
        "image": "pictures/ending_E.png",
    },
]

# ─────────────────────────────
# 3. 統一的判定函式
# ─────────────────────────────
def check_game_over(player, hours_spent):
    """回傳 (bool game_over, dict ending)。"""
    # ──(1) 立刻失敗──
    for e in EARLY_FAILS:
        if e["condition"](player, hours_spent):
            return True, e

    # ──(2) 時間還沒用完 → 遊戲繼續──
    if hours_spent < MAX_HOURS:
        return False, None

    # ──(3) 用完 160h → 比對最終結局──
    for e in FINAL_ENDINGS:
        if e["condition"](player, hours_spent):
            return True, e

    # 理論上不會走到這，但保險用
    return True, {
        "key": "時間到了，但你的狀態相當微妙……", 
        "image": None
    }
