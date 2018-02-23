import sys
from pygame.locals import *
from map import *


TIMER = pygame.USEREVENT + 1
RENDER_TIMER = TIMER + 1
pygame.time.set_timer(TIMER, TIMER_ELAPSE)
pygame.time.set_timer(RENDER_TIMER, 40)


Camp((255, 0, 0), 1, 0)
Camp((255, 255, 0), 1, 0)
Camp((128, 0, 255), 1, 0)
"——gen obstacles——"
if 1:
    Map.gen_obstacles()

Map.calc_accessible_neighbours()

"——gen ants——"
if 1:
    for camp in Camp.camps:
        empty_positions = Map.get_random_empty_positions(camp.ant_number)
        for x, y in empty_positions:
            Ant(x, y, camp)

game_over = False
while True:
    for event in pygame.event.get():
        if event.type == TIMER and not game_over:
            try:
                "——gen food——"
                if 1:
                    Food.gen_food()
                "——odors float——"
                Map.block_give_odor()
                Map.block_receive_odor()
                "——objects' action——"
                shuffle(Object.objects)
                for obj in Object.objects:
                    obj.act()
            except GameOverException:
                game_over = True
                print("游戏结束")
        elif event.type == RENDER_TIMER:
            "——render——"
            DISPLAYSURFACE.fill((0, 0, 0))
            Map.render()
            for bar in Bar.bars:
                bar.render()
            pygame.display.update()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
