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
    ??????????????????
    ?????? Rect ????????? movement ?????????????????????????????????
    """
    # TODO: ??????????????? return True????????? return False
    in_border = True
    if rect.left + movement[0] < 0:         # ????????????
        in_border = False  

    # SCREEN_WIDTH, SCREEN_HEIGHT

    return in_border

def player_move(rect: pg.Rect, pressed_keys: Sequence):
    """
    ??????????????????
    ?????? pressed_keys ?????????????????????
    """

    # TODO: ?????????????????? movement ??????
    movement = (0, 0)                       # ??????????????????

    if pressed_keys[pg.K_LEFT]:             # ??????????????????????????????
        movement = (-PLAYER_SPEED, 0)


    # TODO: ?????????????????????????????????????????????
    rect.move_ip(movement)                  # ?????? movement ?????? rect


def kill_first_enemy(enemies: List[Enemy]):
    """
    ??????enemies
    ?????? enemies ??????????????????
    """
    # hint: enemies ?????? list
    

    # TODO: ?????? enemies ???????????????????????????


def game_over(enemies: List[Enemy]):
    """
    ??????????????????
    ??????: ??????????????????
    """
    # TODO: ??????????????????????????????????????? True
    return False

"""
Game Loop
"""
while running:
    # ????????????????????????
    if len(enemies) == 0:
        generate_enemy(enemies)             # ????????????

    # ????????????
    for event in pg.event.get():            # ????????????
        if event.type == pg.QUIT:           # ????????????
            running = False                 # ????????????

        elif event.type == pg.KEYDOWN:      # ?????????????????????????????????
            if event.key == pg.K_SPACE:     # ???????????????
                kill_first_enemy(enemies)
            elif event.key == pg.K_ESCAPE:  # ?????? escape
                running = False

    # ?????????????????????
    pressed_keys = pg.key.get_pressed()

    # ???????????????????????????
    player.update(pressed_keys)             # ??????????????????


    # ????????????????????????
    if game_over(enemies):
        running = False

    # ??????????????????
    screen.fill(BACKGROUND_COLOR)
    screen.blit(player.surf, player.rect)

    for enemy in enemies:
        screen.blit(enemy.surf, enemy.rect)


    pg.display.flip()

    clock.tick(40)
