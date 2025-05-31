# ui/hud.py
import pygame
from constants import HOURS_PER_MONTH, TOTAL_MONTHS, MAX_HOURS

# --- 外觀參數 ----------------------------------------------------
LABEL_BG   = (58, 110, 200)   # 標籤與數值共用底色 (藍色)
LABEL_FG   = (255, 255, 255)  # 字體顏色 (白色)
LABEL_EDGE = (0,   0,   50)   # 外框顏色 (深藍/黑)
EDGE_W     = 2                # 外框線寬

# 版面：左上角留 10px 邊距，標籤方塊固定尺寸
MARGIN_L, MARGIN_T = 10, 10
LABEL_W,  LABEL_H  = 80, 38        # 「月份」方塊寬高
VALUE_W,  VALUE_H  = 220, 38       # 右邊數值方塊寬高
GAP_X = 12                         # 標籤與數值方塊之間的水平間距

# 先備好中文年級對照 (自己要幾年就塞幾個)
GRADE_NAME = ["大一"]

def draw_hud(screen: pygame.Surface,
             font:   pygame.font.Font,
             player,
             hours_spent: float) -> None:
    """在左上角畫一組『月份』Label + 動態值的 HUD。"""

    # ------- 計算目前「第幾月 / 第幾年 (年級)」 -------------------
    # 0-based index：0 → 第 1 月 …  (假設一學年 12 個月可自行拆成季或學期)
    month_idx  = int(hours_spent) // HOURS_PER_MONTH
    month_in_y = month_idx % 12 + 1          # 1~12
    year_idx   = month_idx // 12             # 0 → 大一、1 → 大二 ...
    year_idx   = min(year_idx, len(GRADE_NAME) - 1)
    grade_txt  = GRADE_NAME[year_idx]
    
    # 要顯示的文字
    value_txt = f"{grade_txt}/{month_in_y}月"

    # ------- 畫左側「月份」方塊 -----------------------------------
    label_rect = pygame.Rect(MARGIN_L, MARGIN_T, LABEL_W, LABEL_H)
    pygame.draw.rect(screen, LABEL_BG,   label_rect)               # 底
    pygame.draw.rect(screen, LABEL_EDGE, label_rect, EDGE_W)       # 框

    label_surf = font.render("月份", True, LABEL_FG)
    label_surf_rect = label_surf.get_rect(center=label_rect.center)
    screen.blit(label_surf, label_surf_rect)

    # ------- 畫右側「年級 / 月份」方塊 ------------------------------
    value_rect = pygame.Rect(
        label_rect.right + GAP_X, label_rect.top, VALUE_W, VALUE_H
    )
    pygame.draw.rect(screen, LABEL_BG,   value_rect)
    pygame.draw.rect(screen, LABEL_EDGE, value_rect, EDGE_W)

    value_surf = font.render(value_txt, True, LABEL_FG)
    value_surf_rect = value_surf.get_rect(center=value_rect.center)
    screen.blit(value_surf, value_surf_rect)

    # （如果還想要畫飽足度等測試資訊，可再另開一小行或丟到別的函式）
