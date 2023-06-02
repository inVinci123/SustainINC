import pygame, json

# animation dictionaries of all characters
ben_anim: dict[str, dict[str, list[pygame.Surface]]]
melon_anim: dict[str, dict[str, list[pygame.Surface]]]
dani_anim: dict[str, dict[str, list[pygame.Surface]]]
gutters_anim: dict[str, dict[str, list[pygame.Surface]]]
grater_anim: dict[str, dict[str, list[pygame.Surface]]]
feast_anim: dict[str, dict[str, list[pygame.Surface]]]
jesos_anim: dict[str, dict[str, list[pygame.Surface]]]
sahara_anim: dict[str, dict[str, list[pygame.Surface]]]
inv_anim: dict[str, dict[str, list[pygame.Surface]]]
grass_tile: pygame.Surface

# font and buildings
normal_font: dict[int, pygame.font.Font]
buildings: dict[str, pygame.Surface]

# city bg
gallet_city: pygame.Surface


# load colliders from the json file (overlain on the city)
with open("./Assets/collider_data.json", "r") as col_data:
    colliders = json.load(col_data)["colliders"]

def load_assets(game_scale):
    """ load every single asset according to the game scale """
    global ben_anim, dani_anim, melon_anim, gutters_anim, jesos_anim, sahara_anim, inv_anim, feast_anim, grater_anim, grass_tile, normal_font, buildings, gallet_city

    gallet_city = pygame.transform.scale(pygame.image.load("./Assets/gallet_city.png"), (5120*game_scale, 5120*game_scale))

    buildings = {
        "SustainINC": pygame.transform.scale(pygame.image.load("./Assets/Buildings/SustainINC.png"), (470*game_scale, 560*game_scale))
    }
    
    # player animation
    back_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/ben/back_idle_1.png"), (80*game_scale, 80*game_scale))
    back_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/ben/back_idle_2.png"), (80*game_scale, 80*game_scale))
    back_walk_1 = pygame.transform.scale(pygame.image.load("./Assets/ben/back_walk_1.png"), (80*game_scale, 80*game_scale))
    back_walk_2 = pygame.transform.scale(pygame.image.load("./Assets/ben/back_walk_2.png"), (80*game_scale, 80*game_scale))

    front_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/ben/front_idle_1.png"), (80*game_scale, 80*game_scale))
    front_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/ben/front_idle_2.png"), (80*game_scale, 80*game_scale))
    front_walk_1 = pygame.transform.scale(pygame.image.load("./Assets/ben/front_walk_1.png"), (80*game_scale, 80*game_scale))
    front_walk_2 = pygame.transform.scale(pygame.image.load("./Assets/ben/front_walk_2.png"), (80*game_scale, 80*game_scale))
    
    right_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/ben/right_idle_1.png"), (80*game_scale, 80*game_scale))
    right_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/ben/right_idle_2.png"), (80*game_scale, 80*game_scale))
    right_walk_1 = pygame.transform.scale(pygame.image.load("./Assets/ben/right_walk_1.png"), (80*game_scale, 80*game_scale))
    right_walk_2 = pygame.transform.scale(pygame.image.load("./Assets/ben/right_walk_2.png"), (80*game_scale, 80*game_scale))

    left_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/ben/left_idle_1.png"), (80*game_scale, 80*game_scale))
    left_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/ben/left_idle_2.png"), (80*game_scale, 80*game_scale))
    left_walk_1 = pygame.transform.scale(pygame.image.load("./Assets/ben/left_walk_1.png"), (80*game_scale, 80*game_scale))
    left_walk_2 = pygame.transform.scale(pygame.image.load("./Assets/ben/left_walk_2.png"), (80*game_scale, 80*game_scale))
    
    # player animation dict
    ben_anim = {
        "w": {
            "idle": [back_idle_1, back_idle_1, back_idle_2, back_idle_2],
            "walk": [back_walk_1, back_walk_2, back_walk_1, back_walk_2],
        },
        "s": {
            "idle": [front_idle_1, front_idle_1, front_idle_2, front_idle_2],
            "walk": [front_walk_1, front_walk_2, front_walk_1, front_walk_2],
        },
        "d": {
            "idle": [right_idle_1, right_idle_1, right_idle_2, right_idle_2],
            "walk": [right_walk_1, right_idle_1, right_walk_2, right_idle_1],
        },
        "a": {
            "idle": [left_idle_1, left_idle_1, left_idle_2, left_idle_2],
            "walk": [left_walk_1, left_idle_1, left_walk_2, left_idle_1],
        }
    }

    # grater thunderburg
    grater_left_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/grater/left_idle_1.png"), (80*game_scale, 80*game_scale))
    grater_left_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/grater/left_idle_2.png"), (80*game_scale, 80*game_scale))

    grater_right_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/grater/right_idle_1.png"), (80*game_scale, 80*game_scale))
    grater_right_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/grater/right_idle_2.png"), (80*game_scale, 80*game_scale))
    
    grater_anim = {
        "w": {
            "idle": [grater_right_idle_1, grater_right_idle_1, grater_right_idle_2, grater_right_idle_2]
        },
        "s": {
            "idle": [grater_left_idle_1, grater_left_idle_1, grater_left_idle_2, grater_left_idle_2]
        },
        "d": {
            "idle": [grater_right_idle_1, grater_right_idle_1, grater_right_idle_2, grater_right_idle_2]
        },
        "a": {
            "idle": [grater_left_idle_1, grater_left_idle_1, grater_left_idle_2, grater_left_idle_2]
        }
    }

    # melon usk
    melon_left_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/melon/left_idle_1.png"), (80*game_scale, 80*game_scale))
    melon_left_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/melon/left_idle_2.png"), (80*game_scale, 80*game_scale))

    melon_right_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/melon/right_idle_1.png"), (80*game_scale, 80*game_scale))
    melon_right_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/melon/right_idle_2.png"), (80*game_scale, 80*game_scale))

    melon_anim = {
        "w": {
            "idle": [melon_right_idle_1, melon_right_idle_1, melon_right_idle_2, melon_right_idle_2]
        },
        "s": {
            "idle": [melon_left_idle_1, melon_left_idle_1, melon_left_idle_2, melon_left_idle_2]
        },
        "d": {
            "idle": [melon_right_idle_1, melon_right_idle_1, melon_right_idle_2, melon_right_idle_2]
        },
        "a": {
            "idle": [melon_left_idle_1, melon_left_idle_1, melon_left_idle_2, melon_left_idle_2]
        }
    }

    # Mr Dani
    dani_left_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/dani/left_idle_1.png"), (80*game_scale, 80*game_scale))
    dani_left_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/dani/left_idle_2.png"), (80*game_scale, 80*game_scale))

    dani_right_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/dani/right_idle_1.png"), (80*game_scale, 80*game_scale))
    dani_right_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/dani/right_idle_2.png"), (80*game_scale, 80*game_scale))
    
    dani_anim = {
        "w": {
            "idle": [dani_right_idle_1, dani_right_idle_1, dani_right_idle_2, dani_right_idle_2]
        },
        "s": {
            "idle": [dani_left_idle_1, dani_left_idle_1, dani_left_idle_2, dani_left_idle_2]
        },
        "d": {
            "idle": [dani_right_idle_1, dani_right_idle_1, dani_right_idle_2, dani_right_idle_2]
        },
        "a": {
            "idle": [dani_left_idle_1, dani_left_idle_1, dani_left_idle_2, dani_left_idle_2]
        }
    }

    # Mr Gutters

    gutters_left_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/gutters/left_idle_1.png"), (80*game_scale, 80*game_scale))
    gutters_left_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/gutters/left_idle_2.png"), (80*game_scale, 80*game_scale))

    gutters_right_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/gutters/right_idle_1.png"), (80*game_scale, 80*game_scale))
    gutters_right_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/gutters/right_idle_2.png"), (80*game_scale, 80*game_scale))
    
    gutters_anim = {
        "w": {
            "idle": [gutters_right_idle_1, gutters_right_idle_1, gutters_right_idle_2, gutters_right_idle_2]
        },
        "s": {
            "idle": [gutters_left_idle_1, gutters_left_idle_1, gutters_left_idle_2, gutters_left_idle_2]
        },
        "d": {
            "idle": [gutters_right_idle_1, gutters_right_idle_1, gutters_right_idle_2, gutters_right_idle_2]
        },
        "a": {
            "idle": [gutters_left_idle_1, gutters_left_idle_1, gutters_left_idle_2, gutters_left_idle_2]
        }
    }

    # buff jesos
    jesos_left_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/jesos/left_idle_1.png"), (80*game_scale, 80*game_scale))
    jesos_left_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/jesos/left_idle_2.png"), (80*game_scale, 80*game_scale))

    jesos_right_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/jesos/right_idle_1.png"), (80*game_scale, 80*game_scale))
    jesos_right_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/jesos/right_idle_2.png"), (80*game_scale, 80*game_scale))
    
    jesos_anim = {
        "w": {
            "idle": [jesos_right_idle_1, jesos_right_idle_1, jesos_right_idle_2, jesos_right_idle_2]
        },
        "s": {
            "idle": [jesos_left_idle_1, jesos_left_idle_1, jesos_left_idle_2, jesos_left_idle_2]
        },
        "d": {
            "idle": [jesos_right_idle_1, jesos_right_idle_1, jesos_right_idle_2, jesos_right_idle_2]
        },
        "a": {
            "idle": [jesos_left_idle_1, jesos_left_idle_1, jesos_left_idle_2, jesos_left_idle_2]
        }
    }

    # Mr Feast 6001
    feast_left_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/feast/left_idle_1.png"), (80*game_scale, 80*game_scale))
    feast_left_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/feast/left_idle_2.png"), (80*game_scale, 80*game_scale))

    feast_right_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/feast/right_idle_1.png"), (80*game_scale, 80*game_scale))
    feast_right_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/feast/right_idle_2.png"), (80*game_scale, 80*game_scale))
    
    feast_anim = {
        "w": {
            "idle": [feast_right_idle_1, feast_right_idle_1, feast_right_idle_2, feast_right_idle_2]
        },
        "s": {
            "idle": [feast_left_idle_1, feast_left_idle_1, feast_left_idle_2, feast_left_idle_2]
        },
        "d": {
            "idle": [feast_right_idle_1, feast_right_idle_1, feast_right_idle_2, feast_right_idle_2]
        },
        "a": {
            "idle": [feast_left_idle_1, feast_left_idle_1, feast_left_idle_2, feast_left_idle_2]
        }
    }

    # Sahara (Amazon) Employee
    sahara_left_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/sahara/left_idle_1.png"), (80*game_scale, 80*game_scale))
    sahara_left_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/sahara/left_idle_2.png"), (80*game_scale, 80*game_scale))

    sahara_right_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/sahara/right_idle_1.png"), (80*game_scale, 80*game_scale))
    sahara_right_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/sahara/right_idle_2.png"), (80*game_scale, 80*game_scale))
    
    sahara_anim = {
        "w": {
            "idle": [sahara_right_idle_1, sahara_right_idle_1, sahara_right_idle_2, sahara_right_idle_2]
        },
        "s": {
            "idle": [sahara_left_idle_1, sahara_left_idle_1, sahara_left_idle_2, sahara_left_idle_2]
        },
        "d": {
            "idle": [sahara_right_idle_1, sahara_right_idle_1, sahara_right_idle_2, sahara_right_idle_2]
        },
        "a": {
            "idle": [sahara_left_idle_1, sahara_left_idle_1, sahara_left_idle_2, sahara_left_idle_2]
        }
    }

    # inv, the cool guy
    inv_left_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/inv/left_idle_1.png"), (80*game_scale, 80*game_scale))
    inv_left_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/inv/left_idle_2.png"), (80*game_scale, 80*game_scale))

    inv_right_idle_1 = pygame.transform.scale(pygame.image.load("./Assets/inv/right_idle_1.png"), (80*game_scale, 80*game_scale))
    inv_right_idle_2 = pygame.transform.scale(pygame.image.load("./Assets/inv/right_idle_2.png"), (80*game_scale, 80*game_scale))
    
    inv_anim = {
        "w": {
            "idle": [inv_right_idle_1, inv_right_idle_1, inv_right_idle_2, inv_right_idle_2]
        },
        "s": {
            "idle": [inv_left_idle_1, inv_left_idle_1, inv_left_idle_2, inv_left_idle_2]
        },
        "d": {
            "idle": [inv_right_idle_1, inv_right_idle_1, inv_right_idle_2, inv_right_idle_2]
        },
        "a": {
            "idle": [inv_left_idle_1, inv_left_idle_1, inv_left_idle_2, inv_left_idle_2]
        }
    }
    
    # reload the font accordingly (rounded to the nearest integer)
    normal_font = {
        8: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(8*game_scale)),
        12: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(12*game_scale)),
        14: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(14*game_scale)),
        16: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(16*game_scale)),
        18: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(18*game_scale)),
        24: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(24*game_scale)),
        30: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(30*game_scale)),
        50: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(50*game_scale)),
        64: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(64*game_scale)),
        100: pygame.font.Font("Assets/Fonts/ApercuMonoProMedium.ttf", int(100*game_scale))
    }