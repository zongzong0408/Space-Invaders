from __future__ import annotations          # fix the typing annotation for class
import pygame as pg
from typing import List, Tuple, Sequence

"""
Constant
"""
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (0, 0, 0)                # rgb for black

SCORE = 100

PLAYER_SPEED = 5

ENEMY_X_COUNT = 6
ENEMY_Y_COUNT = 3
ENEMY_SPEED = 5
ENEMY_MOVEMENT_SET = [(1,0)] * 35 + [(0, 3)] + [(-1, 0)] * 35 + [(0, 3)]
ENEMY_MOVE_TIME_MAX = 750
ENEMY_MOVE_TIME_MIN = 50


"""
Helper Functions
"""
# resize image
def image_resize(surf: pg.Surface, ratio: float):
    w, h = surf.get_size()
    new_surf = pg.transform.scale(surf, (int(w*ratio), int(h*ratio)))

    return new_surf

# generate all enemies
def generate_enemy(enemies: List[Enemy]):
    generate_origin = pg.Vector2(60, 60)
    padding_x, padding_y = 75, 60
    for j in range(ENEMY_Y_COUNT):
        for i in range(ENEMY_X_COUNT):
            enemy = Enemy(generate_origin + pg.Vector2(i * padding_x, j * padding_y))
            enemies.append(enemy)


"""
Game Object
"""
class Player:
    def __init__(self):
        self.surf = image_resize(pg.image.load("player.png").convert(), 0.1)
        self.rect = self.surf.get_rect(midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT-50))

    # update the position by keyboard input
    def update(self, pressed_keys):
        player_move(self.rect, pressed_keys)


class Enemy:
    def __init__(self, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)):
        self.surf = image_resize(pg.image.load("enemy.png").convert(), 0.1)
        self.rect = self.surf.get_rect(center=pos)

    def update(self, movement):
        self.rect.move_ip(ENEMY_SPEED * pg.Vector2(movement))


"""
Initialize & Global Variables
"""
pg.init()
pg.display.set_caption("Space Invaders")
pg.display.set_icon(pg.image.load("enemy.png"))

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()

player = Player()
enemies = []

font = pg.font.SysFont("Arial", 20)

running = True

"""
Homework Practice
"""
def in_border_check(rect: pg.Rect, movement: Tuple):
    """
    二：邊界判斷
    檢查 Rect 在經過 movement 移動後，是否有在螢幕內
    """
    # TODO: 在螢幕內就 return True，否則 return False
    in_border = True
    if rect.left + movement[0] < 0:         # 檢查左界
        in_border = False  

    # SCREEN_WIDTH, SCREEN_HEIGHT

    return in_border

def player_move(rect: pg.Rect, pressed_keys: Sequence):
    """
    一：玩家移動
    依照 pressed_keys 來移動玩家位置
    """

    # TODO: 依照按鍵調整 movement 變數
    movement = (0, 0)                       # 玩家的平移量

    if pressed_keys[pg.K_LEFT]:             # 如果左方向鍵有被按下
        movement = (-PLAYER_SPEED, 0)


    # TODO: 檢查邊界，如果在邊界內才能移動
    rect.move_ip(movement)                  # 根據 movement 平移 rect


def kill_first_enemy(enemies: List[Enemy]):
    """
    三：enemies
    刪除 enemies 中第一個元素
    """
    # hint: enemies 是個 list
    

    # TODO: 取得 enemies 第一個元素，刪除它


def game_over(enemies: List[Enemy]):
    """
    四：遊戲結束
    條件: 敵人全部消失
    """
    # TODO: 判斷遊戲結束，若結束則回傳 True
    return False

"""
Game Loop
"""
while running:
    # 如果無敵人在場上
    if len(enemies) == 0:
        generate_enemy(enemies)             # 生成敵人

    # 處理事件
    for event in pg.event.get():            # 取得事件
        if event.type == pg.QUIT:           # 關閉視窗
            running = False                 # 停止遊戲

        elif event.type == pg.KEYDOWN:      # 處理鍵盤按鍵按下的事件
            if event.key == pg.K_SPACE:     # 按下空白鍵
                kill_first_enemy(enemies)
            elif event.key == pg.K_ESCAPE:  # 按下 escape
                running = False

    # 取得按下的按鍵
    pressed_keys = pg.key.get_pressed()

    # 更新所有物件的位置
    player.update(pressed_keys)             # 更新玩家位置


    # 判斷遊戲是否結束
    if game_over(enemies):
        running = False

    # 畫背景、物件
    screen.fill(BACKGROUND_COLOR)
    screen.blit(player.surf, player.rect)

    for enemy in enemies:
        screen.blit(enemy.surf, enemy.rect)


    pg.display.flip()

    clock.tick(40)
