import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
        }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数こうかとんまたは爆弾のRect
    戻り値：真理値タプル（横判定結果，縦判定結果）
    画面内ならTrue画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20 ,20)) # 空のSurface
    bb_img.set_colorkey((0, 0, 0)) # 爆弾の四隅を透過させる
    pg.draw.circle(bb_img, (250, 0, 0), (10, 10), 10)#爆弾の色
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):# こうかとんと爆弾が重なっていたら
            GO(screen)
            
           


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0] # yoko
                sum_mv[1] += tpl[1] # tate

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
             vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(86)
def GO(screen): 
    # screen = pg.display.set_mode((WIDTH, HEIGHT)) 
    black_rect = pg.Surface((WIDTH, HEIGHT))  
    #black_rect.fill((0, 0, 0))  
    pg.draw.rect(black_rect, (0, 0, 0,),(0, 0, 1100,650))
    black_rect.set_alpha(128)
    screen.blit(black_rect, (0, 0))
    cry_img = pg.transform.rotozoom(pg.image.load("fig/6.png"), 0, 0.9)  
    cry_rect = cry_img.get_rect(center=(WIDTH // 2 - 250, HEIGHT // 2 ))  
    screen.blit(cry_img, cry_rect) 
    cry_img2 = pg.transform.rotozoom(pg.image.load("fig/6.png"), 0, 0.9)  
    cry_rect2 = cry_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 ))  
    screen.blit(cry_img2, cry_rect2) 
    
    font = pg.font.Font(None, 80)  
    text = font.render("GAME OVER", True, (255, 0, 0))  
    screen.blit(text, [350, 300])  
    pg.display.update()
    time.sleep(5)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
