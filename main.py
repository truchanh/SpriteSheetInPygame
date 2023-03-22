import pygame as pg
from config import *
from spritesheet import LRSpriteSheet

pg.init()


# create groups for managing sprites
player = pg.sprite.GroupSingle()
# let's instantiate our first LRSpriteSheet
LRSpriteSheet(
    player,
    file=MEGAMAN_SPRITESHEET,
    cols=5, rows=2,
    pos=(WIN_RECT_CENTER)
)

def keydown_events(key):
    """when the user hold down a key"""
    if key == pg.K_RIGHT:
        player.sprite.direction.x = 1
        player.sprite.facing_right = True
        player.sprite.facing_left = False
    elif key == pg.K_LEFT:
        player.sprite.direction.x = -1
        player.sprite.facing_left = True
        player.sprite.facing_right = False

def keyup_events(key):
    """when the user unpress a key from begin pressed"""
    if key == pg.K_RIGHT:
        # when we release the right arrow key, our player stop moving
        # (stop the right running animation)
        # but still facing right
        player.sprite.direction.x = 0
        player.sprite.facing_right = True
        player.sprite.facing_left = False
    elif key == pg.K_LEFT:
        # when we release the left arrow key, our player stop moving
        # (stop the left running animation)
        # but still facing left
        player.sprite.direction.x = 0
        player.sprite.facing_left = True
        player.sprite.facing_right = False


if __name__ == '__main__':
    done = False
    while not done:
        time_delta = CLK.tick(FPS) / 1000.0
        pg.display.flip()
        for e in pg.event.get():
            if e.type == pg.WINDOWCLOSE:
                done = True
            elif e.type == MEGAMAN_TIMER:
                player.update(time_delta)
            elif e.type == pg.KEYDOWN:
                keydown_events(e.key)
            elif e.type == pg.KEYUP:
                keyup_events(e.key)
        WIN.fill('magenta')
        # now let's draw everything we have onto the screen

        ####### don't remove this comment-outed line ########
        # pg.draw.rect(WIN, 'white', player.sprite.rect, 0) #
        #####################################################
        player.draw(WIN)
    pg.quit()
