import pygame as pg
from config import WIN, MEGAMAN_STANDING_STILL

class LRSpriteSheet(pg.sprite.Sprite):
    """docstring for LRSpriteSheet
    - LR stands for left and right which means our sprite
    can only move in horizontal direction
    - [!NOTE] that each Sprite required two attributes: spr.image and spr.rect
    """
    def __init__(self, *groups, file: str, cols: int, rows: int, pos: tuple[int]):
        super(LRSpriteSheet, self).__init__(*groups)  # same as self.add(*groups)
        self.cols = cols
        self.rows = rows
        self.x, self.y = pos
        self.direction = pg.Vector2()
        self.facing_right = False
        self.facing_left = not self.facing_right
        print(self.facing_left)
        self.speed = 900
        # loading image files
        self.sheet = pg.image.load(file).convert_alpha(WIN)
        self.flipped_sheet = pg.transform.flip(self.sheet, True, False)
        self.standing_still_image = pg.image.load(
            MEGAMAN_STANDING_STILL
        ).convert_alpha(WIN)
        self.flipped_standing_still_image = pg.transform.flip(
            self.standing_still_image, True, False
        )
        # get the correct image at initialization
        self.image = self.get_default_direction(cols, rows)
        self.smallest_rect = self.image.get_bounding_rect()
        self.image = self.image.subsurface(self.smallest_rect)
        self.image = self.scale_factor(self.image, sw=3, sh=3)
        # self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect  = self.image.get_rect(
            center = (self.x, self.y)
            )
    def scale_factor(self, old_img: pg.Surface, sw: int=5, sh: int=5) -> pg.Surface:
        new_w = old_img.get_width() // sw
        new_h = old_img.get_height() // sh
        new_img = pg.transform.smoothscale(
            old_img, 
            (new_w, 
            new_h)
        )
        return new_img
    def strip_image(self, raw_img: pg.Surface, 
        cols: int, rows: int) -> list[pg.Rect]:
        """strip our entire spritesheet to individual frames (pg.Rect)"""
        img_w = raw_img.get_width() // cols
        img_h = raw_img.get_height() // rows
        img_ls = []  # empty list containing pg.Rect specs for each frame
        for i in range(rows):
            for j in range(cols):
                left = j * img_w
                top  = i * img_h
                img_ls.append(pg.Rect(left, top, img_w, img_h))
        # print(len(img_ls)==10) should be True
        return img_ls
    def get_default_direction(self, cols: int, rows: int):
        if self.facing_left:  # move left (also facing left)
            # default will be the fifth frame from the rightmost handside in the image sheet has been flipped
            self.index = 4
            self.images = self.strip_image(self.flipped_sheet, cols, rows)
            self.image = self.flipped_sheet.subsurface(self.images[self.index])
        elif self.facing_right:  # move right (also facing right)
            self.index = 0  # default will be the first frame in the images list
            self.images = self.strip_image(self.sheet, cols, rows)
            self.image = self.sheet.subsurface(self.images[self.index])
        print(self.image)  # the image haven't been scaled yet.
        return self.image
    def get_changed_direction(self):
        if self.direction.x < 0:
            self.image = self.flipped_sheet.subsurface(self.images[self.index])
            self.smallest_rect = self.image.get_bounding_rect()
            self.image = self.image.subsurface(self.smallest_rect)
            self.image = self.scale_factor(self.image)
            self.rect  = self.image.get_rect(
                center = self.rect.center
            )
        elif self.direction.x > 0:
            self.image = self.sheet.subsurface(self.images[self.index])
            self.smallest_rect = self.image.get_bounding_rect()
            self.image = self.image.subsurface(self.smallest_rect)
            self.image = self.scale_factor(self.image)
            self.rect  = self.image.get_rect(
                center = self.rect.center
            )
        else:
            # because our standalone sprite has a dimensions
            # different from our sprite's dimensions from the spritesheet
            # try to scale it to fit each individual sprites
            if self.facing_left:
                self.image = self.flipped_standing_still_image
            elif self.facing_right:
                self.image = self.standing_still_image
            self.smallest_rect = self.image.get_bounding_rect()
            self.image = self.image.subsurface(self.smallest_rect)
            self.image = self.scale_factor(self.image, sw=4, sh=4)
            self.rect  = self.image.get_rect(
                center = self.rect.center
                )

    def update_correspond_image(self):
        # update each individual images
        self.get_changed_direction()
    def animated(self):
        """
        - default sheet (facing-right)
        [[0],[>],[>],[>],[>],  # start at 0 index and go forward
         [>],[>],[>],[>],[>]]
        - flipped sheet (facing-left)
        [[0],[<],[<],[<],[4],  # starting index is 4 and go backward
         [5],[<],[<],[<],[9]]
        """
        if self.direction.x < 0:
            # gets coressponding index for the flipped sheet horizontally!
            self.index -= 1
            if self.index < 0:
                self.index = 9
                if self.index < 5:  # this frame at the leftmost handside of row 2 (last frame of the left animation sprite sheet)
                    self.index = 4  # start frame will be the fifth frame on the rightmost handside of column 1
        elif self.direction.x > 0:
            self.index += 1
            if self.index > len(self.images)-1:  # last frame reached
                self.index = 0  # animation loop
        else:
            if self.facing_left:
                self.image = self.flipped_standing_still_image
            elif self.facing_right:
                self.image = self.standing_still_image
        self.update_correspond_image()
    def move(self, dt):
        self.rect = self.rect.move(self.speed * self.direction * dt)
    def constraints(self):
        WIN_RECT = WIN.get_rect()
        if self.rect.left <= WIN_RECT.left:
            self.rect.left = WIN_RECT.left
        elif self.rect.right >= WIN_RECT.right:
            self.rect.right = WIN_RECT.right
    def update(self, dt):
        self.animated()
        self.move(dt)
        self.constraints()
        # print('The dimensions of each sprite is: %ix%i'%(self.rect.w, self.rect.h))
        half_right_length = WIN.get_rect().right - self.rect.centerx
        half_left_length = abs(WIN.get_rect().left - self.rect.centerx)
        HALF_SCREEN = WIN.get_rect().centerx
        # if half_right_length < HALF_SCREEN:
        #     print('rightmost of the screen reach.')
        # elif half_left_length < HALF_SCREEN:
        #     print('leftmost of the screen reach.')
        # else:
        #     print('in the middle of the screen.')
