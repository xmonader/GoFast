import os
from random import randrange, randint
import pygame
import time
import colors
from settings import DISPLAY_MODE, IMGS_DIR


class GameObject(pygame.sprite.Sprite):
    """
    sprite (for position, image, showing)
    """
    def set_image(self, image_name="racecar.png"):
        """
        Setting the underlying image.
        """
        img_path = os.path.join(IMGS_DIR, image_name)
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()

    def set_pos(self, pos=[0, 0]):
        """
        Setting the position (update the rect for the collision detection).
        """
        self.pos = list(pos)
        self.rect.center = self.pos

    def show_me(self, screen):
        """
        Blit the sprite on screen.
        """
        screen.blit(self.image, self.pos)

    def move_V(self, by=1):
        """
        Moves the sprite vertically by step.
        """
        self.set_pos((self.pos[0], self.pos[1]+by))

    def move_H(self, by):
        """
        Moves the sprite horizontally by step.
        """
        self.set_pos((self.pos[0]+by, self.pos[1]))

    @property
    def get_rect(self):
        self.rect.center = self.pos
        return self.rect

class BlockSprite(GameObject):
    """
    Block sprite (for positon, image, showing)
    """
    name = "Block"
    accel = 5
    
class CarSprite(GameObject):
    """ 
    Car sprite (for position, image, showing)
    """
    name = "Car"
    accel = 20

def get_screen():
    """
    Set display mode to settings.DISPLAY_MODE and return a screen.
    """
    return pygame.display.set_mode(DISPLAY_MODE)

clock = pygame.time.Clock()

def get_car_sprite(pos=(0, 0)):
    """
    Create a car sprite object.
    """
    car = CarSprite()
    car.set_image("racecar.png")
    car.set_pos(pos)
    return car

def get_block_sprite(pos=(0,0)):
    """
    Create a block sprite object.
    """
    block = BlockSprite()
    block.set_image("stoneblock.jpg")
    block.set_pos(pos)
    return block

def show_comic_text(screen, msg, pos=(0, 0)):
    """
    Shows a msg on screen at position pos
    @param screen Surface: screen to display text on.
    @param msg string: string to be displayed.
    @param pos tuple: x,y position.
    """
    font = pygame.font.SysFont("comicsansms", 72)
    text = font.render(msg, True, colors.ORANGE)
    screen.blit(text, pos)
    pygame.display.flip()

# GAME STATES. 
RUNNING = True
PAUSED = False    

# KEEP TRACK OF THE SCORE.
SCORE = 0

pygame.init()
screen = get_screen()
pygame.display.set_caption("Go Fast!!")
app_icon = pygame.image.load(os.path.join("assets", "images", "app_icon.png"))
pygame.display.set_icon(app_icon)

def gameloop():
    global RUNNING, PAUSED, SCORE
    RUNNING = True
    PAUSED = False

    car = get_car_sprite()
    car.set_pos((DISPLAY_MODE[0] / 2, 500))

    b = get_block_sprite()
    currentblockpos =  randint(0, DISPLAY_MODE[0]), 20 # we keep 20 of the height for our messages

    b.set_pos(currentblockpos)

    while RUNNING:
        if b.pos[1] > DISPLAY_MODE[1]: #reset the height value
            b.set_pos((randint(0, DISPLAY_MODE[0]), 20 ))
            SCORE += 1 #maybe we should increase the score if it already crossed the car Y pos no?
       
        b.move_V(b.accel)
        screen.fill(colors.WHITE)

        event = pygame.event.poll()
        #print("EVENT: ", event)
        if event.type == pygame.QUIT:
            RUNNING = False
        else:
            if event.type == pygame.KEYUP:
                carnewpos = car.pos
                if event.key == pygame.K_LEFT:
                    carnewpos[0] -= car.accel
                elif event.key == pygame.K_RIGHT:
                    carnewpos[0] += car.accel
                elif event.key == pygame.K_UP:
                    carnewpos[1] -= car.accel
                elif event.key == pygame.K_DOWN:
                    carnewpos[1] += car.accel
                car.set_pos(carnewpos)

            car.show_me(screen)
            b.show_me(screen)

            if pygame.sprite.collide_rect(car, b):
                show_comic_text(screen, "Game over!! you scored {}".format(SCORE))
                RUNNING = False
                time.sleep(1)
                SCORE = 0 
                gameloop()
            else:
                show_comic_text(screen, "Score: {}".format(SCORE))
            pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    gameloop()
