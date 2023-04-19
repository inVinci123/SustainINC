import pygame

ben_anim: dict
grass_tile: pygame.Surface

def load_assets(game_scale):
    global ben_anim, grass_tile
    ben_anim = {
        "w": {
            "idle": [pygame.transform.scale(pygame.image.load("./Assets/back_idle_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/back_idle_2.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/back_idle_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/back_idle_2.png"), (80*game_scale, 80*game_scale))],
            "walk": [pygame.transform.scale(pygame.image.load("./Assets/back_walk_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/back_walk_2.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/back_walk_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/back_walk_2.png"), (80*game_scale, 80*game_scale))]
        },
        "s": {
            "idle": [pygame.transform.scale(pygame.image.load("./Assets/front_idle_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/front_idle_2.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/front_idle_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/front_idle_2.png"), (80*game_scale, 80*game_scale))],
            "walk": [pygame.transform.scale(pygame.image.load("./Assets/front_walk_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/front_walk_2.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/front_walk_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/front_walk_2.png"), (80*game_scale, 80*game_scale))]
        },
        "d": {
            "idle": [pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/right_idle_2.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/right_idle_2.png"), (80*game_scale, 80*game_scale))],
            "walk": [pygame.transform.scale(pygame.image.load("./Assets/right_walk_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/right_walk_2.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale))]
        },
        "a": {
            "idle": [pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/left_idle_2.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/left_idle_2.png"), (80*game_scale, 80*game_scale))],
            "walk": [pygame.transform.scale(pygame.image.load("./Assets/left_walk_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale)),
                     pygame.transform.scale(pygame.image.load("./Assets/left_walk_2.png"), (80*game_scale, 80*game_scale)), 
                     pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale))]
        }
    }
    grass_tile = pygame.transform.scale(pygame.image.load("Assets/grass_tile_big.png"), (256*game_scale, 256*game_scale))