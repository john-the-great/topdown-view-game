import pygame, sys
from pygame.locals import *

def main():
    WINDOW_SIZE = (600, 400)
    window = pygame.display.set_mode(WINDOW_SIZE)
    RES = (150, 100)
    game_surf = pygame.Surface(RES)

    clock = pygame.time.Clock()
    fps_cap = 10_000
    rel_fps = 60

    while 1:
        dt = clock.tick(fps_cap) * .001 * rel_fps

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        upscaled_surf = pygame.transform.scale(
            game_surf, WINDOW_SIZE
        )
        window.blit(upscaled_surf, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    main()