import pygame
import json
import copy
import random

import opening
import item_select
import enhancement
import battle
import result

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("わんこ大戦争")
        self.clock = pygame.time.Clock()

        self.change_scene("return")

        self.font_address = "assets/fonts/Yuji_Syuku/YujiSyuku-Regular.ttf"
        self.font1 = pygame.font.Font(self.font_address, 30)

        self.bai = 1

    def load(self):
        with open("data/data.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.ally_characters = {c["name"]: c for c in self.data["characters"]["allies"]}
        self.enemy_characters = {c["name"]: c for c in self.data["characters"]["enemies"]}
        self.items = self.data["items"]
        self.enemy_enhancements = self.data["enemy_enhancements"]
    
    def load2(self):
        with open("data/data2.json", "r", encoding="utf-8") as f:
            self.data2 = json.load(f)
        for i in (self.data2["allies"]):
            self.data2["allies"][i]["status"] = copy.deepcopy(self.ally_characters[i])
        self.slots = [0]
        self.stage = 0
        self.allies = [{"name":a, "size":self.ally_characters[a]["size"]} for a in self.data2["allies"]]
        self.coin = 50
        self.n = 3
        

    def loop(self):
        self.running = True
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
                self.scene.handle_event(event)
            for _ in range(self.bai):
                self.scene.step()
            self.scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

    def change_scene(self, key):
        print(key)
        if key == "return":
            self.load()
            self.load2()
            self.scene = opening.Opening(self, self.width, self.height)
            self.state = "opening"
        elif self.state == "opening":
            if key == "start":
                items = self.shaffle_items()
                self.scene = item_select.Select(self, self.width, self.height, items)
                self.state = "item_select"
        elif self.state == "item_select":
            self.selected_item(self.now_items[key])
            self.scene = enhancement.Enhancement(self, self.width, self.height, self.allies, self.slots)
            self.state = "enhancement"
        elif self.state == "enhancement":
            if key == "start":
                self.scene = battle.Battle(self, self.width, self.height, *self.ready_battle())
                self.state = "battle"
        elif self.state == "battle":
            self.bai = 1
            if key == "ally_win":
                self.stage += 1
                if self.stage == len(self.data["stages"]):
                    self.scene = result.Result(self, self.width, self.height)
                    self.state = "result"
                else:
                    items = self.shaffle_items()
                    self.scene = item_select.Select(self, self.width, self.height, items)
                    self.state = "item_select"
            if key == "enemy_win":
                self.scene = result.Result(self, self.width, self.height)
                self.state = "result"
    
    def shaffle_items(self):
        self.now_items = []
        while len(self.now_items) < self.n:
            r = random.choice(self.items)
            if random.random() < r["percent"]:
                if "{character}" in r["name"]:
                    shoji = [i["name"] for i in self.allies]
                    if r["effect"] == "character_unlock":
                        a = [i["name"] for i in self.data["characters"]["allies"] if i["name"] not in shoji]
                    else:
                        a = [i["name"] for i in self.data["characters"]["allies"] if i["name"] in shoji]
                    c = random.choice(a)
                    rr = copy.deepcopy(r)
                    rr["name"] = r["name"].replace("{character}", c)
                    rr["value"][0] = r["value"][0].replace("{character}", c)
                    rr["description"] = r["description"].replace("{character}", c)
                    r = rr
                    # print(c,rr)
                
                e = random.choice(self.enemy_enhancements)
                self.now_items.append({"ally": r, "enemy": e})

        # items = [
        # {
        #     "ally": {"name": "味方アイテム1", "description": "効果: 体力回復"},
        #     "enemy": {"name": "敵アイテム1", "description": "効果: 攻撃力アップ"}
        # }]
        # print(items)
        return self.now_items
    
    def selected_item(self, items):
        item = items["ally"]
        if item["effect"] == "money":
            self.coin += item["value"]
        elif item["effect"] == "choice_increase":
            self.n += 1
        elif item["effect"] == "character_unlock":
            self.data2["allies"][item["value"][0]] = {}
            self.data2["allies"][item["value"][0]]["status"] = self.ally_characters[item["value"][0]]
            self.data2["allies"][item["value"][0]]["enhancement"] = self.ally_characters[item["value"][0]]["etc"]["enhancement"]
            self.data2["allies"][item["value"][0]]["items"] = {
                "magnification": 1,
                "first_wait": 1,
                "respawn": 1,
                "spawn_num": 1,
                "ability": {}
            }
            self.data2["allies"][item["value"][0]]["cost"] = self.ally_characters[item["value"][0]]["etc"]["cost"]
            self.data2["allies"][item["value"][0]]["auto_spawn"] = True
            self.data2["allies"][item["value"][0]]["auto_respawn"] = True
            self.allies.append({"name": item["value"][0], "size": self.ally_characters[item["value"][0]]["size"]})
        elif item["effect"] == "character_upgrade":
            self.data2["allies"][item["value"][0]]["items"]["magnification"] *= item["value"][1]
    
    def ready_battle(self):
        # magnification注意
        stage = self.data["stages"][self.stage]

        characters = []
        for i in self.slots:
            chara = copy.deepcopy(self.data2["allies"][self.allies[i]["name"]]["status"])
            print(chara)
            magnification = self.data2["allies"][self.allies[i]["name"]]["enhancement"]["magnification"] * self.data2["allies"][self.allies[i]["name"]]["items"]["magnification"]
            chara["params"][1] = int(chara["params"][1] * magnification)
            chara["params"][2] = int(chara["params"][2] * magnification)
            characters.append(chara)
        for i in range(len(stage["enemies"])):
            name = stage["enemies"][i]
            chara = self.enemy_characters[name]
            chara["params"][1] *= stage["level"][i] + self.data2["enemies"][name] + 4
            chara["params"][1] //= 5
            chara["params"][2] *= stage["level"][i] + self.data2["enemies"][name] + 4
            chara["params"][2] //= 5
            characters.append(chara)

        castles = [{"hp":int(self.data2["castle_hp"] * self.data2["items"]["castle_hp"])},
                   {"hp":stage["castle_hp"] + self.data2["enemies"]["城体力"] * 1000}]
        distance = stage["distance"]
        background = f"assets/images/back_grounds/{stage['background']}"

        allies = [{"name":self.allies[i]["name"], "first_spawn":self.data2["allies"][self.allies[i]["name"]]["enhancement"]["first_wait"] // self.data2["allies"][self.allies[i]["name"]]["items"]["first_wait"],
                   "respawn_time":self.data2["allies"][self.allies[i]["name"]]["enhancement"]["respawn"] // self.data2["allies"][self.allies[i]["name"]]["items"]["respawn"],
                   "spawn_num":int(self.data2["allies"][self.allies[i]["name"]]["enhancement"]["spawn_num"] * self.data2["allies"][self.allies[i]["name"]]["items"]["spawn_num"]),
                   "auto_spawn":self.data2["allies"][self.allies[i]["name"]]["auto_spawn"],
                   "auto_respawn":self.data2["allies"][self.allies[i]["name"]]["auto_respawn"]} for i in self.slots]
        enemies = [{"name":name, "first_spawn":stage["spawns"][i][0], "respawn_time":stage["spawns"][i][1] // (0.9 ** self.data2["enemies"]["再生産"]),
                    "spawn_num":stage["spawns"][i][2], "auto_spawn":True, "auto_respawn":True} for i,name in enumerate(stage["enemies"])]
        
        ally_max_spawn = int(self.data2["max_spawn"] * self.data2["items"]["max_spawn"])
        enemy_max_spawn = stage["max_spawn"]
        reward = int(self.data2["reward"] * self.data2["items"]["reward"])
        # print(characters)
        return characters, castles, distance, background, allies, enemies, reward, ally_max_spawn, enemy_max_spawn


if __name__ == "__main__":
    game = Game(1200,700)
    game.loop()