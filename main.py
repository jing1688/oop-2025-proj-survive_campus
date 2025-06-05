import pygame
import sys
from pygame.locals import *

from constants import *
from utils.font_loader import get_font
from entities.player import Player
from entities.building import Building
from ui.hud import draw_hud
from ui.prompt import draw_prompt, draw_end, draw_choices
from endings import check_game_over
from levels import LEVELS

PLAYER_SPEED = 3

# ----------------------------- 初始化 -----------------------------
pygame.mixer.init()
CAT_SOUND = pygame.mixer.Sound(CAT_SOUND_PATH)

# 世界尺寸（與 LEVELS 建立時一致）
WORLD_W, WORLD_H = 2000, 2000

# 迷你地圖參數
MINIMAP_W, MINIMAP_H = 180, 180
MINIMAP_MARGIN      = 10
MINIMAP_BG          = (230, 230, 230)
MINIMAP_EDGE        = (50,  50,  50)
MINIMAP_PLAYER_COL  = (0,   120, 255)
MINIMAP_BUILD_COL   = (200, 120,   0)
MINIMAP_SCALE_X     = MINIMAP_W / WORLD_W
MINIMAP_SCALE_Y     = MINIMAP_H / WORLD_H

# dead‑zone 邊界 (玩家距螢幕邊多少像素才開始滾動)
EDGE_X = WIDTH // 3
EDGE_Y = HEIGHT // 3

# ------------------------------------------------------------------
# 迷你地圖繪製函式
# ------------------------------------------------------------------

def draw_minimap(screen: pygame.Surface, player, buildings):
    # 位置：螢幕右上角
    rect = pygame.Rect(
        WIDTH - MINIMAP_W - MINIMAP_MARGIN,
        MINIMAP_MARGIN,
        MINIMAP_W,
        MINIMAP_H,
    )
    pygame.draw.rect(screen, MINIMAP_BG,   rect)
    pygame.draw.rect(screen, MINIMAP_EDGE, rect, 2)

    # 繪製建築物 (小橘方塊)
    for b in buildings:
        bx = b.rect.centerx * MINIMAP_SCALE_X + rect.left
        by = b.rect.centery * MINIMAP_SCALE_Y + rect.top
        br = pygame.Rect(0, 0, 6, 6)
        br.center = (int(bx), int(by))
        pygame.draw.rect(screen, MINIMAP_BUILD_COL, br)

    # 繪製玩家 (小藍圓)
    px = player.rect.centerx * MINIMAP_SCALE_X + rect.left
    py = player.rect.centery * MINIMAP_SCALE_Y + rect.top
    pygame.draw.circle(screen, MINIMAP_PLAYER_COL, (int(px), int(py)), 4)

# ------------------------------------------------------------------
# 主迴圈
# ------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Campus RPG MVP")
    clock = pygame.time.Clock()

    font_big   = get_font(32)
    font_small = get_font(24)

    # 初始玩家放在世界中心 (WORLD_W/2, WORLD_H/2)
    player    = Player(WORLD_W // 2, WORLD_H // 2)
    buildings = LEVELS[0](WORLD_W, WORLD_H)

    hours_spent   = 0
    game_over     = False
    ending        = None

    submenu_kind   = None  # 'cat' / 'restaurant' / 'classroom'
    feedback_text  = ""
    feedback_timer = 0

    last_month_idx = -1

    classroom_choices = [("1","讀書"),("2","考試"),("3","睡覺")]
    cat_choices       = [("1","摸牠"),("2","餵牠"),("3","喵喵喵"),("4","不做事")]

    # 攝影機初始位置
    cam_x = 0
    cam_y = 0

    while True:
        # --------------------------------------------------
        # 事件處理
        # --------------------------------------------------
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # 子選單操作
            if submenu_kind and e.type == KEYDOWN:
                if submenu_kind == 'cat':
                    if e.key == K_1:
                        hours_spent += ACTION_HOURS["CAT_TOUCH"]
                        feedback_text = "他不想讓你摸"
                    elif e.key == K_2:
                        hours_spent += ACTION_HOURS["CAT_FEED"]
                        feedback_text = "你沒有貓糧"
                    elif e.key == K_3:
                        hours_spent += ACTION_HOURS["CAT_MEOW"]
                        feedback_text = "喵？"
                        CAT_SOUND.play()
                    elif e.key == K_4:
                        hours_spent += ACTION_HOURS["CAT_IDLE"]
                        feedback_text = ""
                elif submenu_kind == 'restaurant':
                    if e.key == K_y:
                        hours_spent += ACTION_HOURS["EAT"]
                        player.health -= 1
                        player.energy = 10
                        player.social += 1
                        feedback_text = "你吃得很開心！"
                    else:
                        feedback_text = "你決定先離開"
                elif submenu_kind == 'classroom':
                    if e.key == K_1:
                        hours_spent += ACTION_HOURS["STUDY"]
                        player.health -= 1
                        player.academics += 1
                        feedback_text = "上課"
                    elif e.key == K_2:
                        hours_spent += ACTION_HOURS["EXAM"]
                        player.health -= 2
                        player.academics += 2
                        feedback_text = "考試"
                    elif e.key == K_3:
                        hours_spent += ACTION_HOURS["SLEEP_CLASS"]
                        player.health += 2
                        feedback_text = "睡著了"
                elif submenu_kind == 'gym':
                    if e.key == K_y:
                        hours_spent += 3           # 時間 +3h
                        player.energy -= 15        # energy -15
                        player.health = min(player.health_max, player.health + 3)
                        feedback_text = "你大汗淋漓，感覺更健康！"
                    else:
                        feedback_text = "你決定先離開"
                elif submenu_kind == 'library':
                    if e.key == K_y:
                        hours_spent += 5           # 時間 +3h
                        player.energy -= 25        # energy -15
                        player.academics += 4
                        if hours_spent >= 60 and hours_spent<=80:
                            feedback_text = "你發現要被當了。你決定一個晚上，一隻筆，一台平板，創造奇蹟"
                        else:
                            feedback_text = "即便現在不是期中考周，你的人生仍只剩圖書館"
                    else:
                        feedback_text = "你決定先離開"
                submenu_kind = None

                # --------- 跨月檢查 ---------
                current_month_idx = int(hours_spent) // HOURS_PER_MONTH
                if current_month_idx != last_month_idx:
                    player.health = player.health_max
                    player.money  += 4000
                    last_month_idx = current_month_idx

                game_over, ending = check_game_over(player, hours_spent)
                feedback_timer   = FPS
                if game_over:
                    break

            # 進入子選單？
            if submenu_kind is None and e.type == KEYDOWN:
                near = next((b for b in buildings if player.rect.colliderect(b.detect_rect)), None)
                if near:
                    if e.key == K_y:
                        submenu_kind = near.kind
                    elif e.key == K_n:
                        feedback_text   = ""
                        feedback_timer  = 0

        if game_over:
            break

        # --------------------------------------------------
        # 攝影機 dead‑zone 計算
        # --------------------------------------------------
        # 玩家距離螢幕邊 EDGE_X/EDGE_Y 以內，鏡頭才移動
        # 先把玩家世界座標轉成目前螢幕座標
        scr_x = player.rect.centerx - cam_x
        scr_y = player.rect.centery - cam_y

        if scr_x < EDGE_X:
            cam_x = max(0, player.rect.centerx - EDGE_X)
        elif scr_x > WIDTH - EDGE_X:
            cam_x = min(WORLD_W - WIDTH, player.rect.centerx - (WIDTH - EDGE_X))

        if scr_y < EDGE_Y:
            cam_y = max(0, player.rect.centery - EDGE_Y)
        elif scr_y > HEIGHT - EDGE_Y:
            cam_y = min(WORLD_H - HEIGHT, player.rect.centery - (HEIGHT - EDGE_Y))

        # --------------------------------------------------
        # 畫面更新
        # --------------------------------------------------
        screen.fill(BG_COLOR)

        # 建築物
        for b in buildings:
            b.draw(screen, (cam_x, cam_y))

        # 玩家
        player.draw(screen, (cam_x, cam_y))

        # HUD
        draw_hud(screen, font_small, player, hours_spent)

        # 迷你地圖
        draw_minimap(screen, player, buildings)

        # 子選單 / 提示 / Feedback
        near = next((b for b in buildings if player.rect.colliderect(b.detect_rect)), None)
        if submenu_kind == 'cat':
            draw_choices(screen, font_small, cat_choices, topleft=(WIDTH//2-80, HEIGHT//2-80))
        elif submenu_kind == 'restaurant':
            draw_prompt(screen, font_big, "你要吃東西嗎？ (Y/N)")
        elif submenu_kind == 'classroom':
            draw_choices(screen, font_small, classroom_choices, topleft=(WIDTH//2-100, HEIGHT//2-80))
        elif near:
            draw_prompt(screen, font_big, BUILDING_INFO[near.kind]['prompt'])

        if feedback_timer > 0 and feedback_text:
            draw_prompt(screen, font_big, feedback_text, feedback=True)
            feedback_timer -= 1

        pygame.display.flip()
        clock.tick(FPS)

        # --------------------------------------------------
        # 玩家移動
        # --------------------------------------------------
        keys = pygame.key.get_pressed()
        dx = (keys[K_RIGHT] or keys[K_d]) - (keys[K_LEFT] or keys[K_a])
        dy = (keys[K_DOWN] or keys[K_s]) - (keys[K_UP] or keys[K_w])
        player.move(dx * PLAYER_SPEED, dy * PLAYER_SPEED, pygame.Rect(0, 0, WORLD_W, WORLD_H), buildings)

    # --------------------------------------------------
    # 結局畫面
    # --------------------------------------------------
    msg1     = ending['key']
    msg2     = f"最終 社交:{player.social}  成績:{player.academics}"
    end_font = get_font(24)

    screen.fill((200, 200, 200))
    start_y  = int(HEIGHT * 0.10)
    bottom_y = draw_end(
        screen, end_font, msg1, msg2,
        bg=(200,200,200), wrap_width=40, y_start=start_y
    )

    if ending.get('image'):
        img   = pygame.image.load(ending['image']).convert_alpha()
        max_w = int(WIDTH  * 0.5)
        max_h = int(HEIGHT * 0.5)
        w, h  = img.get_size()
        scale = min(max_w / w, max_h / h, 1)
        if scale < 1:
            img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
        img_rect = img.get_rect(midtop=(WIDTH//2, bottom_y + 10))
        screen.blit(img, img_rect)
        pygame.display.flip()

    while True:
        e = pygame.event.wait()
        if e.type in (QUIT, KEYDOWN):
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()