from . import character
import random

class battle:
    def __init__(self, ally_castle_hp, enemy_castle_hp, distance):
        self.ally_castle_hp = ally_castle_hp
        self.enemy_castle_hp = enemy_castle_hp
        self.distance = distance
        self.characters = []

        self.ally_castle = character.character(self, True, "ally_castle", ally_castle_hp, 0, 0, (0, 0, 0), (0, 0, 0), False, 1e-10, [], 800, 0, 0, invalid=["back","stop","slow","down"])
        self.enemy_castle = character.character(self, False, "enemy_castle", enemy_castle_hp, 0, 0, (0, 0, 0), (0, 0, 0), False, 1e-10, [], distance-800, 0, 0, invalid=["back","stop","slow","down"])
        self.characters.append(self.ally_castle)
        self.characters.append(self.enemy_castle)
        self.result = "ongoing"

    def step(self):
        for c in self.characters:
            c.step()
        if self.result == "ongoing":
            if self.enemy_castle.hp <= 0:
                self.result = "ally_win"
            elif self.ally_castle.hp <= 0:
                self.result = "enemy_win"
    
    def spawn_character(self, name, isally, hp, ap, speed, range, attack_time, area, kb, ability, y, z, attribute=[]):
        if isally:
            x = 700
        else:
            x = self.distance - 700
        c = character.character(self, isally, name, hp, ap, speed, range, attack_time, area, kb, ability, x, y + random.randint(0,50), z + random.randint(0,50), attribute)
        self.characters.append(c)

    def get(self):
        return {
            "result": self.result,
            "ally_castle_hp": self.ally_castle.hp,
            "enemy_castle_hp": self.enemy_castle.hp,
            "distance": self.distance,
            "characters": [vars(c) for c in self.characters]
        }
