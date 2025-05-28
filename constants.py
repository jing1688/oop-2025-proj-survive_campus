# 畫面設定
WIDTH         = 800
HEIGHT        = 600
FPS           = 60

# 玩家／建築尺寸
PLAYER_SIZE   = 40
BUILDING_SIZE = (60, 60)

# 顏色設定 (R, G, B)
BG_COLOR         = (144, 201, 120)
PLAYER_COLOR     = (0,   128, 255)
RESTAURANT_COLOR = (255, 165,   0)
CLASSROOM_COLOR  = (128,   0, 128)
CAT_COLOR        = (255, 180,   0)  # 若未使用可留作備用

HOURS_PER_MONTH = 40
TOTAL_MONTHS    = 4
MAX_HOURS       = HOURS_PER_MONTH * TOTAL_MONTHS  # 160

# 各種類建築的屬性集中表
BUILDING_INFO = {
    "restaurant": {
        "color": RESTAURANT_COLOR,
        "prompt": "進入餐廳？ (Y/N)",
        "effect": lambda p: (
            setattr(p, "fullness", 10),
            setattr(p, "social",   p.social + 1),
            setattr(p, "health", p.health - 1),
        ),
    },
    "classroom": {
        "color": CLASSROOM_COLOR,
        "prompt": "進入教室？ (Y/N)",
        "effect": lambda p: (
            setattr(p, "fullness",  p.fullness - 1),
            setattr(p, "grade",     p.grade + 1),
            setattr(p, "health", p.health - 1),
        ),
    },
    "cat": {
        "color": CAT_COLOR,
        "prompt": "要摸摸可愛的貓咪嗎？ (Y/N)",
        # effect 仍可留空或同步使用 building.interact 的回傳處理
        "effect": lambda p: None,
    },
}

ACTION_HOURS = {
    "CAT_TOUCH":  1,
    "CAT_FEED":   1,
    "CAT_MEOW":   0.5,
    "CAT_IDLE":   0,      # 不做事

    "EAT":        2,
    "STUDY":      3,
    "EXAM":       4,
    "SLEEP_CLASS":1,
}


# 路徑
NOTO_FONT_PATH  = "NotoSansTC-Regular.otf"
CAT_IMAGE_PATH  = "pictures/cat.png"
CAT_SOUND_PATH  = "sounds/Free_Cat_SFX_Meow2.wav"
GOBLIN_IMAGE_PATH = "pictures/goblin.png"  # 假設有哥布林圖片