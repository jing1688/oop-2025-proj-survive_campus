# constants.py

# 畫面設定：此處放大到 1024×768
WIDTH   = 800
HEIGHT  = 600
FPS     = 60

# 玩家／建築尺寸
PLAYER_SIZE   = 40
BUILDING_SIZE = (120, 120)

# 顏色設定 (R, G, B)
BG_COLOR         = (144, 201, 120)
PLAYER_COLOR     = (0,   128, 255)
RESTAURANT_COLOR = (255, 165,   0)
CLASSROOM_COLOR  = (128,   0, 128)
CAT_COLOR        = (255, 180,   0)
GYM_COLOR      = (100, 100, 110) 
# 時間相關
HOURS_PER_MONTH = 40
TOTAL_MONTHS    = 4
MAX_HOURS       = HOURS_PER_MONTH * TOTAL_MONTHS  # 160

# 玩家初始與最大體力
ENERGY_MAX      = 100  

# 各種類建築的屬性集中表
BUILDING_INFO = {
    "restaurant": {
        "color": RESTAURANT_COLOR,
        "prompt": "進入餐廳？ (Y/N)",
        "effect": lambda p: (
            setattr(p, "energy", 10),
            setattr(p, "social",   p.social + 1),
            setattr(p, "health",   p.health - 1),
        ),
    },
    "gym": {
    "color": GYM_COLOR,
    "prompt": "要運動嗎？ (Y/N)",
    # 運動：Energy -15、Health +3
    "effect": lambda p: (
        setattr(p, "energy",   p.energy - 15),
        setattr(p, "health",   min(p.health_max, p.health + 3))
    ),
    },
    "classroom": {
        "color": CLASSROOM_COLOR,
        "prompt": "進入教室？ (Y/N)",
        "effect": lambda p: (
            setattr(p, "energy",   p.energy - 1),
            setattr(p, "academics",p.academics + 1),
            setattr(p, "health",   p.health - 1),
        ),
    },
    "cat": {
        "color": CAT_COLOR,
        "prompt": "要摸摸可愛的貓咪嗎？ (Y/N)",
        "effect": lambda p: None,
    },
    "library": {
        # "color": (0, 128, 0),  # 圖書館顏色
        "prompt": "要進入圖書館嗎？ (Y/N)",
        "effect": lambda p: (
            setattr(p, "energy",   p.energy - 1),
            setattr(p, "academics",p.academics + 2),
            setattr(p, "health",   p.health - 1),
        ),
    },
}

# 各種行動所需小時數
ACTION_HOURS = {
    "CAT_TOUCH":   2,
    "CAT_FEED":    4,
    "CAT_MEOW":    0.5,
    "CAT_IDLE":    0,
    "EAT":         2,
    "STUDY":       7,
    "EXAM":        3,
    "SLEEP_CLASS": 3,
}

# 路徑
NOTO_FONT_PATH    = "NotoSansTC-Regular.otf"
CAT_IMAGE_PATH    = "pictures/cat.png"
CAT_SOUND_PATH    = "sounds/Free_Cat_SFX_Meow2.wav"
GOBLIN_IMAGE_PATH = "pictures/goblin.png"
A_Building_Path   = "pictures/A_building.png"
GYM_IMAGE_PATH    = "pictures/gym_pixel.png"
LIBRARY_IMAGE_PATH = "pictures/library.gif"