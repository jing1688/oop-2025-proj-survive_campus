# ui/hud.py

import pygame
from constants import HOURS_PER_MONTH, MAX_HOURS,ENERGY_BLUE, ENERGY_RED,HEIGHT

# --- 外觀參數 ----------------------------------------------------
LABEL_BG     = (58, 110, 200)   # 所有藍底
LABEL_FG     = (255, 255, 255)  # 白字
LABEL_EDGE   = (0,   0,   50)   # 邊框深藍
EDGE_W       = 2                # 邊框粗細

MARGIN_L, MARGIN_T = 10, 10
# 「月份」Label 大小
LABEL_W, LABEL_H  = 80, 38
# 「年級/月份」值方塊大小
VALUE_W, VALUE_H  = 180, 38
GAP_X             = 12

# 第二列：可支配時間／金錢 大小
INFO_W, INFO_H    = 180, 38
INFO_GAP_Y        = 10  # 可支配時間、金錢之間的垂直間距

# 最下方：體力血條
HEALTH_LABEL_W, HEALTH_LABEL_H = 80, 30
HEALTH_BOX_W,   HEALTH_BOX_H   = 30, 30
HEALTH_BOX_GAP                  = 5
HEALTH_MARGIN_BOTTOM            = 10

ENERGY_LABEL_W, ENERGY_LABEL_H = 80, 30
BLOCK_SIZE      = 22                 # 能量小方塊邊長
BLOCK_GAP       = 3
ENERGY_MARGIN_B = 10

# 中文年級名稱 (可自行擴充到大二/大三……)
GRADE_NAME = ["大一", "大二", "大三", "大四", "研一", "研二"]

# ------- 能量（10 格，藍＝有，紅＝空） -------
def _draw_energy_blocks(surf, x, y, energy):
    """
    energy: int 0~100，畫 10 個 16×16 小方塊
    """
    blocks = 10
    size   = 16
    gap    = 2
    filled = max(0, min(energy // 10, blocks))   # 0~10

    for i in range(blocks):
        col = ENERGY_BLUE if i < filled else ENERGY_RED
        rect = pygame.Rect(
            x + i * (size + gap), y, size, size
        )
        pygame.draw.rect(surf, col, rect)
        pygame.draw.rect(surf, (30,30,30), rect, 1)   # 邊框

def draw_hud(screen: pygame.Surface,
             font:   pygame.font.Font,
             player,
             hours_spent: float) -> None:
    """
    左上：
      (1) 月份 Label  + 年級/月份 值方塊
      (2) 可支配時間、金錢 值方塊
    最下方：
      (3) 體力血條
    """
    # --- (1) 計算年級／月份 ---
    START_MONTH = 9  # 從 9 月開學
    month_idx   = int(hours_spent) // HOURS_PER_MONTH
    abs_idx     = (START_MONTH - 1) + month_idx
    month_in_y  = abs_idx % 12 + 1
    year_idx    = abs_idx // 12
    year_idx    = min(year_idx, len(GRADE_NAME) - 1)
    grade_txt   = GRADE_NAME[year_idx]
    month_txt   = f"{grade_txt}/{month_in_y}月"

    # --- (2a) 左上「月份」Label ---
    label_rect = pygame.Rect(MARGIN_L, MARGIN_T, LABEL_W, LABEL_H)
    pygame.draw.rect(screen, LABEL_BG,   label_rect)
    pygame.draw.rect(screen, LABEL_EDGE, label_rect, EDGE_W)
    lbl_surf = font.render("月份", True, LABEL_FG)
    lbl_rect = lbl_surf.get_rect(center=label_rect.center)
    screen.blit(lbl_surf, lbl_rect)

    # --- (2b) 左上「年級/月份」值方塊 ---
    value_rect = pygame.Rect(
        label_rect.right + GAP_X, MARGIN_T, VALUE_W, VALUE_H
    )
    pygame.draw.rect(screen, LABEL_BG,   value_rect)
    pygame.draw.rect(screen, LABEL_EDGE, value_rect, EDGE_W)
    val_surf = font.render(month_txt, True, LABEL_FG)
    val_rect = val_surf.get_rect(center=value_rect.center)
    screen.blit(val_surf, val_rect)

    # --- (3a) 左上：剩餘時間 ---
    used_this_month   = int(hours_spent) % HOURS_PER_MONTH
    remain_this_month = max(0, HOURS_PER_MONTH - used_this_month)
    time_txt = f"{remain_this_month}h"

    info1_rect = pygame.Rect(
        value_rect.right + GAP_X,   # ↙︎  改：連在月份值方塊右邊
        MARGIN_T,                   # ↙︎  改：與月份同一列
        INFO_W, INFO_H
    )
    pygame.draw.rect(screen, LABEL_BG,   info1_rect)
    pygame.draw.rect(screen, LABEL_EDGE, info1_rect, EDGE_W)
    t_lbl = font.render("剩餘時間", True, LABEL_FG)
    screen.blit(
        t_lbl,
        (info1_rect.left + 8,
         info1_rect.top + (INFO_H - t_lbl.get_height()) // 2)
    )
    t_val = font.render(time_txt, True, LABEL_FG)
    screen.blit(
        t_val,
        (info1_rect.right - 8 - t_val.get_width(),
         info1_rect.top + (INFO_H - t_val.get_height()) // 2)
    )

    # --- (3b) 左上第二列往下：金錢 ---
    money_txt = f"{player.money} $"
    info2_rect = pygame.Rect(
        MARGIN_L,
        info1_rect.bottom + INFO_GAP_Y,
        INFO_W, INFO_H
    )
    pygame.draw.rect(screen, LABEL_BG,   info2_rect)
    pygame.draw.rect(screen, LABEL_EDGE, info2_rect, EDGE_W)
    m_lbl = font.render("金錢", True, LABEL_FG)
    screen.blit(
        m_lbl,
        (info2_rect.left + 8,
         info2_rect.top + (INFO_H - m_lbl.get_height()) // 2)
    )
    m_val = font.render(money_txt, True, LABEL_FG)
    screen.blit(
        m_val,
        (info2_rect.right - 8 - m_val.get_width(),
         info2_rect.top + (INFO_H - m_val.get_height()) // 2)
    )

    # --- (4) 最下方：體力血條 ---
    energy_y = HEIGHT - ENERGY_MARGIN_B - ENERGY_LABEL_H
    energy_lbl_rect = pygame.Rect(MARGIN_L, energy_y, ENERGY_LABEL_W, ENERGY_LABEL_H)
    pygame.draw.rect(screen, LABEL_BG,   energy_lbl_rect)
    pygame.draw.rect(screen, LABEL_EDGE, energy_lbl_rect, EDGE_W)
    screen.blit(font.render("體力", True, LABEL_FG),
                font.render("體力", True, LABEL_FG).get_rect(center=energy_lbl_rect.center))

    # 能量 10 格
    _draw_energy_blocks(
        screen,
        x = energy_lbl_rect.right + BLOCK_GAP,
        y = energy_lbl_rect.top + (ENERGY_LABEL_H - BLOCK_SIZE)//2,
        energy = player.energy
    )

