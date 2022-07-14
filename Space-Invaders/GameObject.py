from __future__ import annotations
from Config import *
import pygame as pg
from typing import List, Union

# resize image
def image_resize(surf: pg.Surface, ratio: float):
    w, h = surf.get_size()
    new_surf = pg.transform.scale(surf, (int(w*ratio), int(h*ratio)))

    return new_surf

class Player:
    def __init__(self):
        self.surf = image_resize(pg.image.load("player.png").convert(), 0.1)
        self.rect = self.surf.get_rect(midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT-50))
        self.life = PLAYER_HP

    def shoot(self, bullets: List[Bullet]):
        bullet = Bullet(self)
        bullets.append(bullet)

class Enemy:
    def __init__(self, pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)):
        self.surf = image_resize(pg.image.load("enemy.png").convert(), 0.1)
        self.rect = self.surf.get_rect(center=pos)

    def shoot(self, bullets: List[Bullet]):
        bullet = Bullet(self)
        bullets.append(bullet)

class Bullet:
    def __init__(self, owner: Union[Enemy,Player]):
        self.surf = pg.Surface(BULLET_SIZE)
        self.owner = owner

        if isinstance(owner, Player):
            self.surf.fill(P_BULLET_COLOR)
            self.speed = -BULLET_SPEED
        elif isinstance(owner, Enemy):
            self.surf.fill(E_BULLET_COLOR)
            self.speed = BULLET_SPEED

        self.rect = self.surf.get_rect(center = owner.rect.center)