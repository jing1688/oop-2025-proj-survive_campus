import pygame, sys
from pygame.locals import *
from constants import *
from utils.font_loader import get_font
from entities.player import Player
from entities.building import Building
from ui.hud import draw_hud
from ui.prompt import draw_prompt, draw_end, draw_choices
from endings import check_game_over
from levels import LEVELS


##====參數====##
PLAYER_SPEED=3
# 初始化 mixer
pygame.mixer.init()
CAT_SOUND = pygame.mixer.Sound(CAT_SOUND_PATH)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Campus RPG MVP")
    clock = pygame.time.Clock()

    font_big = get_font(32)
    font_small = get_font(24)

    player = Player(WIDTH//2, HEIGHT//2)
    buildings = LEVELS[0](WIDTH, HEIGHT)

    hours_spent = 0      # 累計已花費的時間（小時）
    game_over = False
    ending = None

    submenu_kind = None  # 'cat', 'restaurant', 'classroom', or None
    feedback_text = ""
    feedback_timer = 0

    classroom_choices = [("1","讀書"),("2","考試"),("3","睡覺")]
    cat_choices = [("1","摸牠"),("2","餵牠"),("3","喵喵喵"),("4","不做事")]

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type in (QUIT, KEYDOWN) and e.key == K_ESCAPE:
                pygame.quit(); sys.exit()

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
                submenu_kind = None
                game_over, ending = check_game_over(player, hours_spent)
                feedback_timer = FPS
                if game_over:
                    # 跳出主迴圈
                    break

            if submenu_kind is None and e.type == KEYDOWN:
                near = next((b for b in buildings if player.rect.colliderect(b.detect_rect)), None)
                if near:
                    if e.key == K_y:
                        submenu_kind = near.kind
                    elif e.key == K_n:
                        feedback_text = ""
                        feedback_timer = 0

        if game_over:
            break

        screen.fill(BG_COLOR)
        for b in buildings:
            b.draw(screen)
        player.draw(screen)
        draw_hud(screen, font_small, player, hours_spent)

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

        keys = pygame.key.get_pressed()
        dx = (keys[K_RIGHT] or keys[K_d]) - (keys[K_LEFT] or keys[K_a])
        dy = (keys[K_DOWN] or keys[K_s]) - (keys[K_UP] or keys[K_w])
        player.move(dx*PLAYER_SPEED, dy*PLAYER_SPEED, screen.get_rect(), buildings)

# 結局畫面
        # 1) 準備文字和字型
    msg1     = ending['key']
    msg2     = f"最終 社交:{player.social}  成績:{player.academics}"
    end_font = get_font(24)

    # 2) 清屏並由 10% 處開始繪製（自動換行／手動換行）
    screen.fill((200, 200, 200))
    start_y  = int(HEIGHT * 0.10)
    bottom_y = draw_end(
        screen,
        end_font,
        msg1,
        msg2,
        bg=(200,200,200),
        wrap_width=40,
        y_start=start_y
    )

    # 3) 如果有圖片，就按 bottom_y＋10px 的位置貼上，且縮放到螢幕一半大小
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

    # 4) 等待玩家按鍵或關閉
    while True:
        e = pygame.event.wait()
        if e.type in (QUIT, KEYDOWN):
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()