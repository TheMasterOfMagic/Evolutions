import sys
from pygame.locals import *
from object import *


TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER, TIMER_ELAPSE)


"——gen ants——"
if 1:
    for camp in Camp.camps:
        for n in range(camp.ant_number):
            x, y = Map.get_accessible_position()
            Ant(x, y, camp)


"——gen food——"
if 1:
    for n in range(FOOD_NUMBER):
        x, y = Map.get_accessible_position()
        Food(x, y)

game_over = False
while True:
    for event in pygame.event.get():
        if event.type == TIMER and not game_over:
            try:
                "——gen food——"
                Food.gen_random_food()
                "——objects' action——"
                for obj in Object.objects:
                    obj.act()
            except GameOverException:
                game_over = True
            "——render——"
            DISPLAYSURFACE.fill((0, 0, 0))
            Map.render()
            pygame.display.update()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
