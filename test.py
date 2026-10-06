import pygame
import json

from battle import Battle

class Game:
    def __init__(self):
        self.bai = 1

    def load(self):
        with open("data/data.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.ally_characters = {c["name"]: c for c in self.data["characters"]["allies"]}
        self.enemy_characters = {c["name"]: c for c in self.data["characters"]["enemies"]}
        self.items = self.data["items"]
        self.enemy_enhancements = self.data["enemy_enhancements"]

if __name__ == "__main__":
    game = Game()
    game.load()

    pygame.init()
    screen_size = (1200, 700)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    ally_names = ["わんーこ","にょーろ","クマせんせー"]
    enemy_names = ["ネーコ"]
    characters = [
        # {"name": "ネーコ", "params": (False, 100,8,10,(140,-320,140),(8,10,30),False,3,[],0,0), "move_count": [2,14,[1,1,1,1,1,1,1,2,2,2,2,2,2,2]], "attack_count": [2,18,[1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2]], "size": (320, 320)},
        # {"name": "わんーこ", "params": (True, 90,8,5,(110,-320,110),(8,8,40),False,3,[],0,0), "move_count": [3,16,[1,1,1,1,2,2,2,2,3,3,3,3,2,2,2,2]], "attack_count": [2,16,[1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2]], "size": (320, 320)},
        # {"name": "にょーろ", "params": (True, 100,15,8,(110,-320,110),(8,8,30),False,3,[],0,0), "move_count": [2,14,[1,1,1,1,1,1,1,2,2,2,2,2,2,2]], "attack_count": [2,16,[1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2]], "size": (480, 320), "x_offset": 160},
    ]
    for name in ally_names:
        characters.append(game.ally_characters[name])
    for name in enemy_names:
        characters.append(game.enemy_characters[name])
        print(characters)
    castles = [
        {"hp": 100},
        {"hp": 100},
    ]
    # allies = [
    #     {"name": "わんーこ", "first_spawn": 300, "respawn_time": 120, "spawn_num": 5, "auto_spawn": False, "auto_respawn": True},
    #     {"name": "にょーろ", "first_spawn": 600, "respawn_time": 200, "spawn_num": 4, "auto_spawn": False, "auto_respawn": True},
    # ]
    # enemies = [
    #     {"name": "ネーコ", "first_spawn": 360, "respawn_time": 120, "spawn_num": 7, "auto_spawn": True, "auto_respawn": True},
    # ]
    allies = []
    for name in ally_names:
        allies.append({"name": name, "first_spawn": 30, "respawn_time": 300, "spawn_num": 5, "auto_spawn": True, "auto_respawn": True})
    enemies = []
    for name in enemy_names:
        enemies.append({"name": name, "first_spawn": 30, "respawn_time": 300, "spawn_num": 5, "auto_spawn": True, "auto_respawn": True})
    distance = 4600
    battle = Battle(game, screen_size[0], screen_size[1], characters, castles, distance, "assets/images/back_grounds/back_ground1.png", allies, enemies)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            battle.handle_event(event)
        for _ in range(game.bai):
            battle.step()
        battle.draw(screen)
        pygame.display.flip()
        clock.tick(30)

