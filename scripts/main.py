import pygame, sys
from pygame.locals import *
from player import Player

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

    while 1:
        dt = clock.tick(fps_cap) * .001 * rel_fps
        ticks += 1
        time += 1 * dt
        if time >= rel_fps:
            print(f'fps: {ticks}')
            time = 0
            ticks = 0

        game_surf.fill((0, 0, 0))

        pl.movement(dt)

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        pl.animate(game_surf, dt)

        upscaled_surf = pygame.transform.scale(
            game_surf, WINDOW_SIZE
        )
        window.blit(upscaled_surf, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    main()