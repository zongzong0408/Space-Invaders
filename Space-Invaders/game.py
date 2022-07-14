from __future__ import annotations          # fix the typing annotation for class
from typing import List, Tuple, Sequence, Union
from Config import *
from Controller import *
from GameObject import *
import pygame as pg

"""
Helper Functions
"""
# resize image
def image_resize(surf: pg.Surface, ratio: float):
    w, h = surf.get_size()
    new_surf = pg.transform.scale(surf, (int(w*ratio), int(h*ratio)))

    return new_surf


# show shoot statusbar
def show_shoot_statusbar(current: int, bound: int, screen: pg.Surface):
    if current == bound-1:
        status_bar = pg.Surface((SCREEN_WIDTH, 10))
        status_bar.fill((255, 0, 0))
        screen.blit(status_bar, (0, SCREEN_HEIGHT-20))
    elif current > 0:
        status_bar = pg.Surface((int(SCREEN_WIDTH*current/(bound-1)), 10))
        status_bar.fill((0, 255, 0))
        screen.blit(status_bar, (0, SCREEN_HEIGHT-20))

    pg.draw.line(screen, (0, 255, 0), (0, SCREEN_HEIGHT-20), (SCREEN_WIDTH, SCREEN_HEIGHT-20))


# show player life
def show_life_status(life: int, screen: pg.Surface):
    padding = 10

    for i in range(life):
        life_surface = image_resize(pg.image.load("player.png").convert(), 0.05)
        screen.blit(life_surface, (SCREEN_WIDTH - (padding + life_surface.get_width()) * (i+1), 0))


# generate all enemies
def generate_enemy(enemies: List[Enemy]):
    generate_origin = pg.Vector2(60, 60)
    padding_x, padding_y = 75, 60
    for j in range(ENEMY_Y_COUNT):
        for i in range(ENEMY_X_COUNT):
            enemy = Enemy(generate_origin + pg.Vector2(i * padding_x, j * padding_y))
            enemies.append(enemy)


"""
Initialize & Global Variables
"""
pg.init()
pg.display.set_caption("Space Invaders")
pg.display.set_icon(pg.image.load("enemy.png"))

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
score = 0
shoot_thres = 1                             # 按幾下才能發射
w_space_count = 0                           # 按了幾下空白鍵

player = Player()

enemies = []
bullets = []

font = pg.font.SysFont("Arial", 20)

pg.time.set_timer(ENEMYSHOOT_EVENT, ENEMY_SHOOT_TIME)

pg.time.set_timer(ENEMYMOVE_EVENT, ENEMY_MOVE_TIME_MAX)

running = True

"""
Game Loop
"""
while running:
    # 如果無敵人在場上
    if len(enemies) == 0:
        # 生成敵人
        generate_enemy(enemies) 
        # 重設 movements (複製)
        movements = ENEMY_MOVEMENT_SET.copy() 
        # 重設敵人移動計時器
        pg.time.set_timer(ENEMYMOVE_EVENT, ENEMY_MOVE_TIME_MAX) 

    # 處理事件
    for event in pg.event.get():            # 取得事件
        if event.type == pg.QUIT:           # 關閉視窗
            running = False                 # 停止遊戲

        elif event.type == pg.KEYDOWN:      # 處理鍵盤按鍵按下的事件
            if event.key == pg.K_SPACE:     # 按下空白鍵
                w_space_count, shoot_thres = handle_player_shoot(player, bullets, w_space_count, shoot_thres) # 玩家射擊
            elif event.key == pg.K_ESCAPE:  # 按下 escape
                running = False

        # 敵人移動
        elif event.type == ENEMYMOVE_EVENT:
            # 取得敵人下一步，並更新 movements
            # movements 會循環
            movement = get_enemy_movement(movements)
            for enemy in enemies:
                enemy_move(enemy, movement)

        # 敵人射擊 (隨機)
        # 取得 [0, 1) 之間的隨機數字，若大於 ENEMY_SHOOT_PROBABILITY 則發射
            if random.random() > ENEMY_SHOOT_PROBABILITY:
                enemy_shoot(bullets, enemies)

    # 取得按下的按鍵
    pressed_keys = pg.key.get_pressed()

    # 更新所有物件的位置
    player_move(player.rect, pressed_keys)  # 更新玩家位置
    bullets_to_remove = []                  # 紀錄要刪除的子彈
    for bullet in bullets:                  # 更新所有子彈位置
        if not bullet_move(bullet):         # 回傳是否超出邊界
            bullets_to_remove.append(bullet)# 待刪除

    for bullet in bullets_to_remove:        # 刪除子彈
        bullets.remove(bullet)

    # 偵測碰撞
    # 檢查玩家子彈碰到敵人 / 敵人子彈碰到玩家
    score = detect_bullet_collision(score, player, bullets, enemies)

    # 判斷遊戲是否結束
    if game_over(player, enemies):
        running = False

    # 畫背景、物件
    screen.fill(BACKGROUND_COLOR)
    screen.blit(player.surf, player.rect)

    for enemy in enemies:
        screen.blit(enemy.surf, enemy.rect)
    for bullet in bullets:
        screen.blit(bullet.surf, bullet.rect)

    score_surface = font.render('Score: {}'.format(score), False, TEXT_COLOR)
    screen.blit(score_surface, SCORE_POS)
    show_life_status(player.life, screen)
    show_shoot_statusbar(w_space_count, shoot_thres, screen)

    pg.display.flip()

    clock.tick(40)

print("Score: {}".format(score))