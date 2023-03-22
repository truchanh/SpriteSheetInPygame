import pygame as pg
import os

# settting up the project working directories
maindir = os.path.abspath(__file__)
projdir = os.path.dirname(maindir)
imgdir = os.path.join(projdir, 'img')
# getting image absolute files path
MEGAMAN_SPRITESHEET = os.path.join(imgdir, 'sprites_megaman_running.png')
MEGAMAN_STANDING_STILL = os.path.join(imgdir, 'megaman_standing_still.png')
TILE_PATH = os.path.join(imgdir, 'tile_0002.png')
# map set up
LEVEL = [
'............',
'............',
'............',
'............',
'.....x......',
'============',
'............',
'............'
]
# basic set up video modes
FPS = 60
TILESIZE = 72
WINW, WINH = TILESIZE * len(LEVEL[0]), TILESIZE * len(LEVEL)
pg.display.set_caption('megaman running clone with python and pygame:3')
WIN = pg.display.set_mode((WINW, WINH))  # main display surface for our game
WIN_RECT_CENTER = WIN.get_rect().centerx, WIN.get_rect().centery
TILE_IMG = pg.image.load(
	TILE_PATH
	).convert_alpha(WIN)
TILE_IMG = pg.transform.scale(TILE_IMG,
	(TILE_IMG.get_width()*4, TILE_IMG.get_height()*4)
	)
CLK = pg.time.Clock()
# customise the timer for our player
MEGAMAN_TIMER = pg.event.custom_type()
pg.time.set_timer(MEGAMAN_TIMER, 60)
