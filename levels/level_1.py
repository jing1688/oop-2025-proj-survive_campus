# levels/level_01.py
from entities.building import Building
from constants import BUILDING_SIZE

def build_level(width: int, height: int) -> list[Building]:
    """
    傳回本關所有 Building 物件的 list
    """
    return [
        Building(100, 100, "restaurant"),   # 左上餐廳
        Building(width - 100 - BUILDING_SIZE[0],
                 height - 100 - BUILDING_SIZE[1],
                 "classroom"),              # 右下教室
        Building(80, height - 200, "cat"),  # 貓咪
    ]