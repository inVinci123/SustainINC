import pygame

ben_anim: dict[str, dict[str, list[pygame.Surface]]]
melon_anim: dict[str, dict[str, list[pygame.Surface]]]
grass_tile: pygame.Surface

normal_font: dict[int, pygame.font.Font]


def load_assets(game_scale):
    global ben_anim, melon_anim, grass_tile, normal_font
    
    back_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/back_idle_1.png"), (80*game_scale, 80*game_scale))
    back_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/back_idle_2.png"), (80*game_scale, 80*game_scale))
    back_walk_1 = pygame.transform.scale(pygame.image.load("./Assets/back_walk_1.png"), (80*game_scale, 80*game_scale))
    back_walk_2 = pygame.transform.scale(pygame.image.load("./Assets/back_walk_2.png"), (80*game_scale, 80*game_scale))

    front_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/front_idle_1.png"), (80*game_scale, 80*game_scale))
    front_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/front_idle_2.png"), (80*game_scale, 80*game_scale))
    front_walk_1 = pygame.transform.scale(pygame.image.load("./Assets/front_walk_1.png"), (80*game_scale, 80*game_scale))
    front_walk_2 = pygame.transform.scale(pygame.image.load("./Assets/front_walk_2.png"), (80*game_scale, 80*game_scale))
    
    right_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/right_idle_1.png"), (80*game_scale, 80*game_scale))
    right_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/right_idle_2.png"), (80*game_scale, 80*game_scale))
    right_walk_1 = pygame.transform.scale(pygame.image.load("./Assets/right_walk_1.png"), (80*game_scale, 80*game_scale))
    right_walk_2 = pygame.transform.scale(pygame.image.load("./Assets/right_walk_2.png"), (80*game_scale, 80*game_scale))

    left_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/left_idle_1.png"), (80*game_scale, 80*game_scale))
    left_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/left_idle_2.png"), (80*game_scale, 80*game_scale))
    left_walk_1 = pygame.transform.scale(pygame.image.load("./Assets/left_walk_1.png"), (80*game_scale, 80*game_scale))
    left_walk_2 = pygame.transform.scale(pygame.image.load("./Assets/left_walk_2.png"), (80*game_scale, 80*game_scale))

    ben_anim = {
        "w": {
            "idle": [back_idle_1, back_idle_1, back_idle_2, back_idle_2],
            "walk": [back_walk_1, back_walk_2, back_walk_1, back_walk_2]
        },
        "s": {
            "idle": [front_idle_1, front_idle_1, front_idle_2, front_idle_2],
            "walk": [front_walk_1, front_walk_2, front_walk_1, front_walk_2]
        },
        "d": {
            "idle": [right_idle_1, right_idle_1, right_idle_2, right_idle_2],
            "walk": [right_walk_1, right_idle_1, right_walk_2, right_idle_1]
        },
        "a": {
            "idle": [left_idle_1, left_idle_1, left_idle_2, left_idle_2],
            "walk": [left_walk_1, left_idle_1, left_walk_2, left_idle_1]
        }
    }

    melon_anim = ben_anim
    grass_tile = pygame.transform.scale(pygame.image.load("Assets/grass_tile_big.png"), (256*game_scale, 256*game_scale))

    normal_font = {
        8: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(8*game_scale)),
        12: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(12*game_scale)),
        14: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(14*game_scale)),
        16: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(16*game_scale)),
        18: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(18*game_scale)),
        24: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(24*game_scale)),
    }