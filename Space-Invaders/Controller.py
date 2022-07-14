from re import M
import pygame as pg
import random
from Config import *
from GameObject import *
from typing import List, Union, Tuple, Sequence
"""
    Helper Functions
    TODO :
    期望清單：讓敵人可走到底
            ：玩家有慣性移動、擊中特效
"""

hacker_mode = False                         # 如你所見，只要把這個變數調成True就會變成無敵狀態 + 子彈無限

class Effect:
    def __init__(self, bullets: List[Bullet]):
        self.bullets = bullets

    def shoot(self, owner: Union[Enemy,Player], color: Tuple[int, int, int]):
        bullet = Bullet(owner)
        # 消失時間
        bullet.disappearing_time =  random.randint(10,100) 
        X, Y = random.randint(-10,10), random.randint(-10,10)
        bullet.acceleration  = acceleration_controller(speed=BULLET_SPEED, rate_reduction=random.randint(75,90), X_K=X, Y_K=Y)
        # 粒子效果大小
        bullet.surf = pg.Surface( (random.randint(2,5),random.randint(2,5)) ) 
        # 顏色調變
        color_random = (color[0]*random.random(), color[1]*random.random(), color[2]*random.random())
        bullet.surf.fill( color_random )    # 填充顏色
        # 定位並建立rect
        bullet.rect = bullet.surf.get_rect(center = bullet.owner.rect.center) 
        bullet.owner = self                 # 以子彈的角度來看，效果器是發射者
        self.bullets.append(bullet)         # 加入子彈列

    def explode(self, owner: Union[Enemy,Player], color: Tuple[int, int, int], quantity: int):
        for _ in range(quantity):
            self.shoot(owner, color)
        
class acceleration_controller():
    def __init__(self, X_K=0, Y_K=0, speed = 1, speed_limit = 999, rate_reduction = 0.2):
        self.X_K = X_K
        self.Y_K = Y_K
        self.speed = speed
        self.speed_limit = speed_limit
        self.rate_reduction = rate_reduction

    def renew(self):
        if self.X_K != 0:
            self.X_K *= self.rate_reduction / 100
        if self.Y_K != 0:
            self.Y_K *= self.rate_reduction / 100
        self.movement = (int(self.speed*self.X_K), int(self.speed*self.Y_K))

    def accelerate(self, move: Union[int,int]):
        # X_can_move
        if abs(self.X_K) <= self.speed_limit: 
            self.X_K += move[0]
        # Y_can_move
        if abs(self.Y_K) <= self.speed_limit: 
            self.Y_K += move[1]


class enemy_movement_controller():
    '''
        更高級的敵人移動
        功能 ： 敵人如果邊邊被打掉讓他可以走到底才會往下移動。
        筆記 : 恆移 1 向下 3  格式：(X:int,Y:int) 
    '''
    def __init__(self, enemies: List[Enemy]):
        self.toward_right =  True           # 面相右邊
        self.movement = (1,0)               # 初始先往右走
        self.already_drops = False          # 需要向下
        self.enemies = enemies

    def left_right_calculate(self):
        enemies_width = [enemy.rect.x for enemy in self.enemies]
        enemies_width.sort()
        # 計算坐左邊位置
        X_left = enemies_width[0] - ENEMY_SPEED 
        # 計算坐右邊位置
        X_right = enemies_width[-1] + 65 + ENEMY_SPEED 

        return X_left, X_right

    def renew(self):
        X_left, X_right =  self.left_right_calculate()
        # 如果超出了螢幕且還沒往下走過
        if (X_left <= 0 or X_right >= SCREEN_WIDTH) and not(self.already_drops): 
            # 改成要往下走
            self.already_drops = True 
            self.movement = (0, 3)

            return

        if self.already_drops:              # 已經往下走了
            self.already_drops = False      # 改成還沒往下走
            # 面朝為反向
            self.toward_right = not(self.toward_right) 
            # 向面朝放向移動
            self.movement = (int(self.toward_right)*2-1, 0) 

            return

def is_player_bullet(bullet) -> bool:
    return isinstance(bullet.owner, Player)

def is_enemy_bullet(bullet) -> bool:
    return isinstance(bullet.owner, Enemy)


def enemy_move(enemy, movement: Tuple[int, int]) -> None:
    """
        TODO: 高級蝦趴之敵人彈幕移動
        依照 movement 來移動敵人位置
    """
    enemy.rect.move_ip(ENEMY_SPEED * pg.Vector2(movement))

def bullet_move(bullet: Bullet) -> bool:
    """
        依照 bullet.speed 來移動子彈位置
    """
    if isinstance(bullet.owner, Effect):    # 這裡是粒子效果的移動
        acceleration = bullet.acceleration
        acceleration.renew()
        X,Y = acceleration.X_K, acceleration.Y_K
        # 可以移動
        check = in_border_check(bullet.rect, (X,Y))  
        if check:
            bullet.rect.move_ip((X,Y)) 
    else:  
        # 這裡是一般子彈的移動
        # 檢查移動
        check = in_border_check(bullet.rect, (0, bullet.speed))  
        if check:
            bullet.rect.move_ip(0, bullet.speed) 

    return check


"""
    標準
"""
def in_border_check(rect: pg.Rect, movement: Tuple) -> bool:
    """
        檢查 Rect 在移動後，是否有在螢幕內
    """
    if rect.left + movement[0] < 0 or rect.right + movement[0] > SCREEN_WIDTH:
        return False
    return True


def check_collision(a: pg.Rect, b: pg.Rect) -> bool:
    """
        檢查兩個 Rect 是否有碰撞發生
    """
    return pg.Rect.colliderect(a,b)


# 玩家的加速度控制器
P_acceleration = acceleration_controller(speed=PLAYER_SPEED, speed_limit=1, rate_reduction=90) 
def player_move(rect: pg.Rect, pressed_keys: Sequence) -> None:
    """
        依照 pressed_keys 來移動玩家位置
    """
    P_acceleration.renew()

    if pressed_keys[pg.K_LEFT] :            # 如果左方向鍵有被按下
        P_acceleration.accelerate((-0.5,0))
    if pressed_keys[pg.K_RIGHT] :           # 如果左方向鍵有被按下
        P_acceleration.accelerate((0.5,0))

    movement = P_acceleration.movement      # 玩家的飄移量

    if in_border_check(rect, movement):     # 檢查邊界
        rect.move_ip(movement)              # 移動
        
def handle_player_shoot(player: Player, bullets: List[Bullet], w_space_count: int, shoot_thres: int) -> Tuple[int, int]:
    """
        處理玩家射擊，並回傳新的 w_space_count, shoot_thres
        射第 n 發需要按下 n 次空白鍵
    """
    w_space_count += 1
    global hacker_mode

    if shoot_thres == w_space_count:        # 次數達標
        player.shoot(bullets)               # 射擊
        # 射擊所需閥值提升
        shoot_thres += 1 * int(not(hacker_mode)) 
        w_space_count = 0                   # 點及次數歸零

    return w_space_count, shoot_thres


# generate bullet from enemies
def enemy_shoot(bullets: List[Enemy], enemies: List[Enemy]) -> None:
    """
        隨機挑選敵人進行射擊
    """
    horizontal_enemy = dict()
    for enemy in enemies:
        # 用X當作key Y軸會以時間軸覆蓋 所以最後值就是最低的一個
        horizontal_enemy[enemy.rect.x] = enemy 
        # 隨機選出1排
    key = random.choice(list(horizontal_enemy.keys())) 
    horizontal_enemy[key].shoot(bullets)    # 此排最低發射子彈
    
def set_enemy_movement_timer(enemies: List[Enemy]) -> None:
    """
        依據剩餘敵人數量，計算敵人移動時間間隔
        以線性的方式調整，最大為 ENEMY_MOVE_TIME_MAX；最小為 ENEMY_MOVE_TIME_MIN，取整數
    """
    new_time = 1 + len(enemies) * 41
    # 設定計時器
    pg.time.set_timer(ENEMYMOVE_EVENT, new_time)

enemy_movement = None                       # 初始化

def get_enemy_movement(movements:List[Union[int,int]]) -> Tuple[int, int]:
    """ 
        這是更高級的移動
        功能：敵人如果邊邊被打掉讓他可以走到底。
        計算敵人是否碰到牆壁以及移動方向，回傳 movement
    """
    global enemy_movement
    if enemy_movement != None:              # 有敵人移動控制器時
        enemy_movement.renew()              # 刷新控制器
        return enemy_movement.movement      # 回傳控制器之移動數值
    return (1,0)                            # 沒有控制器就先往右走

effecter = None                             # 啟動時的初始化

def detect_bullet_collision(score: int, player: Player, bullets: List[Bullet], enemies: List[Enemy]) -> int:
    """
        檢查玩家子彈碰到敵人，敵人子彈碰到玩家，回傳新分數
        如果玩家子彈打到敵人:
            1. 得分 (+ SCORE)
            2. 刪除敵人
            3. 刪除子彈
            4. 更新敵人移動計時器

        如果敵人子彈打到玩家:
            1. 扣除玩家一條命
            2. 刪除子彈
    """
    global effecter 
    if effecter == None:                    # 如果他還未被定義
        effecter = Effect(bullets)          # 取用效果器
    
    bullets_to_remove = []

    for bullet in bullets:
        if is_player_bullet(bullet):        # 子彈是玩家的
            for enemy in enemies:
                # 擊中敵人
                if check_collision(bullet.rect, enemy.rect): 
                    score += SCORE
                    enemies.remove(enemy)
                    set_enemy_movement_timer(enemies)
                    effecter.explode(enemy, (255,255,255), 30)
                    # 加入刪除子彈清單
                    bullets_to_remove.append(bullet) 

        if is_enemy_bullet(bullet):         # 子彈是敵人的
            # 擊中己方
            if check_collision(bullet.rect,player.rect): 
                # 加入刪除子彈清單
                bullets_to_remove.append(bullet) 
                effecter.explode(player, (255,0,0), 45)
                if not(hacker_mode):
                    player.life -= 1
        # 如果是效果                    
        if isinstance(bullet.owner, Effect): 
            # 時間如果沒了
            if bullet.disappearing_time <= 0: 
                # 加入刪除清單
                bullets_to_remove.append(bullet)
            else:
                bullet.disappearing_time -= 1

    for bullet in bullets_to_remove:        # 刪除子彈
        bullets.remove(bullet)

    return score                            # 回傳分數

def game_over(player: Player, enemies: List[Enemy]) -> bool:
    """
        判斷遊戲結束，條件:
            1. 玩家血量 <= 0
            2. 任一敵人觸底
    """
    global enemy_movement
    
    if enemy_movement == None:
        # 同創建並同步
        enemy_movement = enemy_movement_controller(enemies) 
    if player.life <= 0:
        return True

    for enemy in enemies:
        if enemy.rect.y + 65 >= SCREEN_HEIGHT:
            return True

    return False