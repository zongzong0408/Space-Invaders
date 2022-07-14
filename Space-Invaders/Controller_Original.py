import pygame as pg
import random
from Config import *
from GameObject import *
from typing import List, Union, Tuple, Sequence

"""
    Helper Functions
"""
def is_player_bullet(bullet) -> bool:
    return isinstance(bullet.owner, Player)


def is_enemy_bullet(bullet) -> bool:
    return isinstance(bullet.owner, Enemy)


def enemy_move(enemy: Enemy, movement: Tuple[int, int]) -> None:
    """
        依照 movement 來移動敵人位置
    """
    enemy.rect.move_ip(ENEMY_SPEED * pg.Vector2(movement))


def bullet_move(bullet: Bullet) -> bool:
    """
        依照 bullet.speed 來移動子彈位置
    """
    check = in_border_check(bullet.rect, (0, bullet.speed))
    if check:
        bullet.rect.move_ip(0, bullet.speed)

    return check


"""
    基本
"""
def in_border_check(rect: pg.Rect, movement: Tuple) -> bool:
    """
        檢查 Rect 在移動後，是否有在螢幕內
    """
    # TODO: 在螢幕內就 return True，否則 return False
    return True


def check_collision(a: pg.Rect, b: pg.Rect) -> bool:
    """
        檢查兩個 Rect 是否有碰撞發生
    """
    # TODO: a 與 b 碰撞就 return True，否則 return False
    return False


def player_move(rect: pg.Rect, pressed_keys: Sequence) -> None:
    """
        依照 pressed_keys 來移動玩家位置
    """
    # TODO: 依照按鍵調整 movement 變數
    movement = (0, 0)

    # TODO: 檢查邊界

    # 移動
    rect.move_ip(movement)


def handle_player_shoot(player: Player, bullets: List[Bullet], w_space_count: int, shoot_thres: int) -> Tuple[int, int]:
    """
        處理玩家射擊，並回傳新的 w_space_count, shoot_thres
        射第 n 發需要按下 n 次空白鍵
    """

    # TODO: 更新 w_space_count, shoot_thres，若可以射擊則呼叫 player.shoot(bullets)

    return w_space_count, shoot_thres


# generate bullet from enemies
def enemy_shoot(bullets: List[Enemy], enemies: List[Enemy]) -> None:
    """
        隨機挑選敵人進行射擊
    """
    # TODO: 從 enemies 中隨機挑選一個發射子彈，可以呼叫 enemy.shoot(bullets)


def set_enemy_movement_timer(enemies: List[Enemy]) -> None:
    """
        依據剩餘敵人數量，計算敵人移動時間間隔
        以線性的方式調整，最大為 ENEMY_MOVE_TIME_MAX；最小為 ENEMY_MOVE_TIME_MIN，取整數
    """
    # TODO: 將下方之 ENEMY_MOVE_TIME_MAX 改為計算新的間隔時間
    new_time = ENEMY_MOVE_TIME_MAX

    # 設定計時器
    pg.time.set_timer(ENEMYMOVE_EVENT, new_time)


def get_enemy_movement(movements: List[tuple]) -> Tuple[int, int]:
    """
        回傳 movements 的第一個元素，然後將其放入 movements 的最後以達到循環
    """
    # TODO: 將下方的 movement 改為 movements 第一個元素，然後使 movements 循環
    movement = (0, 0)

    return movement


def detect_bullet_collision(score: int, player: Player, bullets: List[Bullet], enemies: List[Enemy]) -> int:
    """
        檢查玩家子彈碰到敵人 / 敵人子彈碰到玩家，回傳新分數

        如果玩家子彈打到敵人:
            1. 得分 (+ SCORE)
            2. 刪除敵人
            3. 刪除子彈
            4. 更新敵人移動計時器

        如果敵人子彈打到玩家:
            1. 扣除玩家一條命
            2. 刪除子彈
    """
    # TODO: 檢查所有子彈是否打到玩家/敵人，並執行相關動作
    # hint: 可以用 is_player_bullet() 跟 is_enemy_bullet() 判斷是誰的子彈

    # 回傳分數
    return score


def game_over(player: Player, enemies: List[Enemy]) -> bool:
    """
        判斷遊戲結束，條件:
            1. 玩家血量 <= 0
            2. 任一敵人觸底
    """
    # TODO: 判斷遊戲結束，若結束則回傳 True
    return False