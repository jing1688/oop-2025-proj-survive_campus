# ui/hud.py

import pygame
from constants import HOURS_PER_MONTH, MAX_HOURS

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

# 中文年級名稱 (可自行擴充到大二/大三……)
GRADE_NAME = ["大一", "大二", "大三", "大四", "研一", "研二"]

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
    hb_left = MARGIN_L
    hb_top  = screen.get_height() - HEALTH_MARGIN_BOTTOM - HEALTH_LABEL_H
    health_label_rect = pygame.Rect(
        hb_left, hb_top, HEALTH_LABEL_W, HEALTH_LABEL_H
    )
    pygame.draw.rect(screen, LABEL_BG,   health_label_rect)
    pygame.draw.rect(screen, LABEL_EDGE, health_label_rect, EDGE_W)
    hp_lbl = font.render("體力", True, LABEL_FG)
    hp_rect = hp_lbl.get_rect(center=health_label_rect.center)
    screen.blit(hp_lbl, hp_rect)

    # 畫體力格子 (藍色代表剩餘，紅色代表已耗盡)
    start_x = health_label_rect.right + HEALTH_BOX_GAP
    start_y = health_label_rect.top
    cur_hp  = max(0, min(player.health, player.health_max))
    max_hp  = player.health_max

    # 藍色格子：剩餘
    for i in range(cur_hp):
        r = pygame.Rect(
            start_x + i * (HEALTH_BOX_W + HEALTH_BOX_GAP),
            start_y, HEALTH_BOX_W, HEALTH_BOX_H
        )
        pygame.draw.rect(screen, LABEL_BG,   r)
        pygame.draw.rect(screen, LABEL_EDGE, r, EDGE_W)

    # 紅色格子：耗盡
    for j in range(max_hp - cur_hp):
        idx = cur_hp + j
        r = pygame.Rect(
            start_x + idx * (HEALTH_BOX_W + HEALTH_BOX_GAP),
            start_y, HEALTH_BOX_W, HEALTH_BOX_H
        )
        pygame.draw.rect(screen, (200, 30, 30), r)
        pygame.draw.rect(screen, LABEL_EDGE,     r, EDGE_W)
