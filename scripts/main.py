import pygame, sys
from pygame.locals import *
from player import Player
from process_world import MapC
pygame.init()

pl = Player()

def main():
    WINDOW_SIZE = (600, 400)
    window = pygame.display.set_mode(WINDOW_SIZE)
    RES = (150, 100)
    game_surf = pygame.Surface(RES)

    clock = pygame.time.Clock()
    fps_cap = 10_000
    rel_fps = 60
    ticks = 0
    time = 0

    world_data_dir = 'data/world/'
    image_dir = 'images/world/'
    wp = MapC(world_data_dir + 'tiles', image_dir, [150, 110, 100])
    wp.convert_tile_size(16)
    wp.animated_water = True
    wp.slice_chunks()
    if wp.animated_water:
        wp.slice_animated_chunks()

    tscroll = [0, 0]

    while 1:
        dt = clock.tick(fps_cap) * .001 * rel_fps

        tscroll[0] += (((pl.rect.x-pl.size/2 - tscroll[0]) - (WINDOW_SIZE[0]/10)))/10 * dt
        tscroll[1] += (((pl.rect.y-pl.size/2 - tscroll[1]) - (WINDOW_SIZE[1]/10)))/10 * dt
        scroll = tscroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        #show fps
        ticks += 1
        time += 1 * dt
        if time >= rel_fps:
            print(f'fps: {ticks}')
            time = 0
            ticks = 0

        game_surf.fill((0, 0, 0))
        rect_list = wp.show_map(
            game_surf, [pl.rect.x, pl.rect.y], dt, scroll
            )
        wp.show_folliage(game_surf, [pl.rect.x, pl.rect.y], scroll)

        pl.colli(rect_list, dt)

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.MOUSEBUTTONDOWN:
                    match event.button:
                        case 4:
                            if pl.curr_tool < pl.tool_amount:
                                pl.curr_tool += 1
                        case 5:
                            if pl.curr_tool > 0:
                                pl.curr_tool -= 1

        pl.animate(game_surf, dt, scroll)
        pl.process_tools(game_surf)

        #for rect in rect_list:
          #  pygame.draw.rect(game_surf, (255, 0, 0), (
            #    rect[0]-scroll[0], rect[1]-scroll[1],
              #  16, 16), 1)
        upscaled_surf = pygame.transform.scale(
            game_surf, WINDOW_SIZE
        )
        window.blit(upscaled_surf, (0, 0))

        pygame.display.update()

if __name__ == '__main__':
    main()