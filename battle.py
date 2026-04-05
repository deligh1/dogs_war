import pygame
import battle_logic.battle

class Battle:
    def __init__(self, game, width, height, characters, castles, distance, background, allies, enemies, reward=100, ally_max_spawn=5, enemy_max_spawn=5):
        self.game = game
        self.width = width
        self.height = height
        self.battle = battle_logic.battle.battle(castles[0]["hp"], castles[1]["hp"], distance)
        self.ally_castle_img = pygame.transform.scale(pygame.image.load("assets/images/characters/ally_castle.png"), (self.width * 480 / distance, self.width * 960 / distance))
        self.enemy_castle_img = pygame.transform.scale(pygame.image.load("assets/images/characters/enemy_castle.png"), (self.width * 480 / distance, self.width * 960 / distance))
        self.characters = characters
        self.characters_dict = {c["name"]: c for c in characters}
        self.characters_images = {c["name"]: {
            "move":[pygame.transform.scale(pygame.image.load(f"assets/images/characters/{c['name']}/move{i+1}.png"), (self.width * c["size"][0] / distance, self.width * c["size"][1] / distance)) for i in range(c["move_count"][0])],
            "attack":[pygame.transform.scale(pygame.image.load(f"assets/images/characters/{c['name']}/attack{i+1}.png"), (self.width * c["size"][0] / distance, self.width * c["size"][1] / distance)) for i in range(c["attack_count"][0])],
            "kb":pygame.transform.scale(pygame.image.load(f"assets/images/characters/{c['name']}/kb.png"), (self.width * c["size"][0] / distance, self.width * c["size"][1] / distance))}
              for c in characters}
        self.death_img = pygame.transform.scale(pygame.image.load(f"assets/images/characters/death.png"), (self.width * 240 / distance, self.width * 360 / distance))
        self.distance = distance
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.allies = allies
        self.enemies = enemies

        self.spawns = {}
        self.spawns.update({a["name"]: a for a in allies})
        self.spawns.update({e["name"]: e for e in enemies})
        self.spawn_timers = {}
        self.spawn_timers_max = {}
        for a in allies:
            self.spawn_timers[a["name"]] = a["first_spawn"]
            self.spawn_timers_max[a["name"]] = a["first_spawn"]
        for e in enemies:
            self.spawn_timers[e["name"]] = e["first_spawn"]
            self.spawn_timers_max[e["name"]] = e["first_spawn"]
        self.spawned_num = {a["name"]: 0 for a in allies}
        self.spawned_num.update({e["name"]: 0 for e in enemies})
        self.ally_max_spawn = ally_max_spawn
        self.enemy_max_spawn = enemy_max_spawn
        self.ally_spawned = 0
        self.enemy_spawned = 0
        self.reward = reward

        self.font_address = "assets/fonts/Yuji_Syuku/YujiSyuku-Regular.ttf"
        self.font1 = pygame.font.Font(self.font_address, 30)
        self.font2 = pygame.font.Font(self.font_address, 80)

        self.character_buttons = [pygame.Rect(self.width * (100 - 10 * len(self.allies) + 1 + 20 * i) // 200, self.height - 95, self.width * 0.09, 90) for i in range(len(allies))]
        self.character_button_img = [pygame.transform.scale(pygame.image.load(f"assets/images/characters/{a['name']}/move1.png"), (90 * self.characters_dict[a["name"]]["size"][0] // self.characters_dict[a["name"]]["size"][1], 90)) for a in self.allies]
        self.gauge = [pygame.Rect(self.width * (100 - 10 * len(self.allies) + 3 + 20 * i) // 200, self.height - 25, self.width * 0.07, 10) for i in range(len(allies))]

        self.lose_button = pygame.Rect(self.width * 0.85, self.height * 0.05, self.width * 0.1, self.height * 0.1)
        self.lose_button_text = self.font1.render("投了", True, (0,0,0))
        self.bai10_button = pygame.Rect(self.width * 0.72, self.height * 0.05, self.width * 0.1, self.height * 0.1)
        self.bai10_button_text = self.font1.render("10倍速", True, (0,0,0))
        self.bai_button = pygame.Rect(self.width * 0.59, self.height * 0.05, self.width * 0.1, self.height * 0.1)
        self.bai_button_text = self.font1.render("倍速", True, (0,0,0))

        self.next_button_text = self.font1.render("次へ", True, (255, 255, 255))
        self.next_button_rect = self.next_button_text.get_rect()

    def step(self):
        self.auto_spawn()
        self.battle.step()
        for c in self.spawn_timers:
            if self.spawn_timers[c] > 0:
                self.spawn_timers[c] -= 1

    def auto_spawn(self):
        if self.battle.result != "ongoing":
            return
        for name, timer in self.spawn_timers.items():
            if timer <= 0 and self.spawned_num[name] < self.spawns[name]["spawn_num"]:
                if (self.spawns[name]["auto_respawn"] and self.spawned_num[name] > 0) or (self.spawns[name]["auto_spawn"] and self.spawned_num[name] == 0):
                    self.spawn_character(name=name)

    def spawn_character(self, *, id=None, name=None):
        if id is not None:
            name = self.characters[id]["name"]
        elif name is not None:
            pass
        else:
            raise ValueError("idかnameのどちらかを指定してください")
        
        if self.spawned_num[name] >= self.spawns[name]["spawn_num"]:
            return
        if self.spawn_timers[name] != 0:
            return
        if self.characters_dict[name]["params"][0] and self.ally_spawned >= self.ally_max_spawn:
            return
        if not self.characters_dict[name]["params"][0] and self.enemy_spawned >= self.enemy_max_spawn:
            return
        self.battle.spawn_character(name, *self.characters_dict[name]["params"])
        self.spawned_num[name] += 1
        self.spawn_timers[name] = self.spawns[name]["respawn_time"]
        self.spawn_timers_max[name] = self.spawns[name]["respawn_time"]
        if self.spawned_num[name] >= self.spawns[name]["spawn_num"]:
            self.spawn_timers[name] = -1
        if self.characters_dict[name]["params"][0]:
            self.ally_spawned += 1
        else:
            self.enemy_spawned += 1
    
    def count_spawned(self, characters):
        self.ally_spawned = 0
        self.enemy_spawned = 0
        for c in characters:
            if c["name"] == "ally_castle" or c["name"] == "enemy_castle":
                continue
            if c["isally"]:
                self.ally_spawned += 1
            else:
                self.enemy_spawned += 1

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        # screen.fill((255, 255, 255))
        data = self.battle.get()
        self.count_spawned(data["characters"])

        ally_castle_rect = self.ally_castle_img.get_rect()
        enemy_castle_rect = self.enemy_castle_img.get_rect()
        ally_castle_rect.bottomright = self.scaling(800, 0)
        enemy_castle_rect.bottomleft = self.scaling(self.distance - 800, 0)
        screen.blit(self.ally_castle_img, ally_castle_rect)
        screen.blit(self.enemy_castle_img, enemy_castle_rect)

        ally_castle_hp_text = self.font1.render(f"{data['ally_castle_hp']}", True, (0, 0, 0))
        enemy_castle_hp_text = self.font1.render(f"{data['enemy_castle_hp']}", True, (0, 0, 0))
        screen.blit(ally_castle_hp_text, (ally_castle_rect.left + 170, ally_castle_rect.top + 40))
        screen.blit(enemy_castle_hp_text, (enemy_castle_rect.left - 30, enemy_castle_rect.top + 40))
        # キャラクターの描画
        # print(len(data["characters"]))
        for c in data["characters"]:
            if c["name"] == "ally_castle" or c["name"] == "enemy_castle":
                continue
            img = None
            try:
                if c["state"] == "kb" or c["state"] == "back":
                    img = self.characters_images[c["name"]]["kb"]
                elif c["state"] == "attack":
                    # print(self.characters_dict[c["name"]]["attack_count"][2][c["timer"] % self.characters_dict[c["name"]]["attack_count"][1]])
                    img = self.characters_images[c["name"]]["attack"][self.characters_dict[c["name"]]["attack_count"][2][(c["timer"]-1) % self.characters_dict[c["name"]]["attack_count"][1]] - 1]
                elif c["state"] == "move":
                    # print(c["name"], c["timer"])
                    # print(self.characters_dict[c["name"]]["move_count"])
                    # print(self.characters_dict[c["name"]]["move_count"][2][c["timer"] % self.characters_dict[c["name"]]["move_count"][1]])
                    img = self.characters_images[c["name"]]["move"][self.characters_dict[c["name"]]["move_count"][2][(c["timer"]-1) % self.characters_dict[c["name"]]["move_count"][1]] - 1]
                elif c["state"] == "wait":
                    img = self.characters_images[c["name"]]["move"][0]
                elif c["state"] == "dead":
                    img = self.death_img
            except FileNotFoundError:
                img = None
            if img is not None:
                # img = pygame.transform.scale(img, (50, 50))
                rext = img.get_rect()
                if "x_offset" in self.characters_dict[c["name"]]:
                    x_offset = self.characters_dict[c["name"]]["x_offset"]
                else:
                    x_offset = 0
                if c["isally"]:
                    rext.bottomright = self.scaling(c["x"] + x_offset, c["y"])
                else:
                    rext.bottomleft = self.scaling(c["x"] - x_offset, c["y"])
                # rext.center = self.scaling(c["x"], c["y"])
                screen.blit(img, rext)
                # print(c["state"], c["timer"], c["kb_hp"], c["hp"])
            else:
                pygame.draw.circle(screen, (0, 0, 0), (self.scaling(c["x"], c["y"])), 25)

        if data["result"] == "ongoing":
            for i,c in enumerate(self.allies):
                pygame.draw.rect(screen, (255,255,255), self.character_buttons[i])
                pygame.draw.rect(screen, (0,0,0), self.character_buttons[i], width=4)
                screen.blit(self.character_button_img[i], self.character_buttons[i])
                spawn_able = self.spawn_timers[c["name"]] == 0
                overlay = pygame.Surface((self.character_buttons[i].width, self.character_buttons[i].height))
                overlay.set_alpha(0 if spawn_able else 128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, self.character_buttons[i])
                if self.spawn_timers[c["name"]] > 0:
                    pygame.draw.rect(screen, (0,0,0), self.gauge[i])
                    rect = self.gauge[i].copy()
                    rect.width *= (1 - self.spawn_timers[c["name"]] / self.spawn_timers_max[c["name"]])
                    pygame.draw.rect(screen, (0,255,0), rect)
            
            pygame.draw.rect(screen, (255,255,0), self.lose_button)
            screen.blit(self.lose_button_text, (self.lose_button.centerx - self.lose_button_text.get_width() // 2, self.lose_button.centery - self.lose_button_text.get_height() // 2))
            pygame.draw.rect(screen, (255,0,0) if self.game.bai == 2 else (255,255,0), self.bai_button)
            screen.blit(self.bai_button_text, (self.bai_button.centerx - self.bai_button_text.get_width() // 2, self.bai_button.centery - self.bai_button_text.get_height() // 2))
            pygame.draw.rect(screen, (255,0,0) if self.game.bai == 10 else (255,255,0), self.bai10_button)
            screen.blit(self.bai10_button_text, (self.bai10_button.centerx - self.bai10_button_text.get_width() // 2, self.bai10_button.centery - self.bai10_button_text.get_height() // 2))
        
        if data["result"] != "ongoing":
            if data["result"] == "ally_win":
                # 帯域を塗りつぶす
                overlay = pygame.Surface((self.width, self.height // 4))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, self.height // 2 - self.height // 8))
                result_text = self.font2.render("完全勝利！", True, (255, 255, 255))
                screen.blit(result_text, (self.width // 2 - result_text.get_width() // 2, self.height // 2 - result_text.get_height() // 2))
                # 報酬を表示
                reward_text = self.font1.render(f"クリア報酬: {self.reward} G", True, (255, 255, 255))
                screen.blit(reward_text, (self.width // 2 - reward_text.get_width() // 2, self.height // 2 + result_text.get_height() // 2))
            elif data["result"] == "enemy_win":
                    # 帯域を塗りつぶす
                overlay = pygame.Surface((self.width, self.height // 4))
                overlay.set_alpha(128) 
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, self.height // 2 - self.height // 8))
                result_text = self.font2.render("敗北...", True, (255, 255, 255))
                screen.blit(result_text, (self.width // 2 - result_text.get_width() // 2, self.height // 2 - result_text.get_height() // 2))
            
            self.next_button_rect.center = (self.width // 2, self.height // 2 + result_text.get_height())
            screen.blit(self.next_button_text, self.next_button_rect)
    
    def scaling(self, x, y):
        return x * self.width / self.distance, self.height - y * self.height / 1000 - 100
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.character_buttons):
                if rect.collidepoint(event.pos):
                    # print(i)
                    self.spawn_character(name=self.allies[i]["name"])
                    break
            if self.lose_button.collidepoint(event.pos):
                self.battle.result = "enemy_win"
            if self.bai_button.collidepoint(event.pos):
                if self.game.bai != 2:
                    self.game.bai = 2
                else:
                    self.game.bai = 1
            if self.bai10_button.collidepoint(event.pos):
                if self.game.bai != 10:
                    self.game.bai = 10
                else:
                    self.game.bai = 1
                
            if (res := self.battle.get()["result"]) != "ongoing" and self.next_button_rect.collidepoint(event.pos):
                if res == "ally_win":
                    self.game.coin += self.reward
                self.game.change_scene(res)

    def get(self):
        res = self.battle.get()
        return {
            "result": res["result"],
        }

if __name__ == "__main__":
    pygame.init()
    screen_size = (1200, 700)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    characters = [
        {"name": "ネーコ", "params": (False, 100,8,10,(140,-320,140),(8,10,30),False,3,[],0,0), "move_count": [2,14,[1,1,1,1,1,1,1,2,2,2,2,2,2,2]], "attack_count": [2,18,[1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2]], "size": (320, 320)},
        {"name": "わんーこ", "params": (True, 90,8,5,(110,-320,110),(8,8,40),False,3,[],0,0), "move_count": [3,16,[1,1,1,1,2,2,2,2,3,3,3,3,2,2,2,2]], "attack_count": [2,16,[1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2]], "size": (320, 320)},
        {"name": "にょーろ", "params": (True, 100,15,8,(110,-320,110),(8,8,30),False,3,[],0,0), "move_count": [2,14,[1,1,1,1,1,1,1,2,2,2,2,2,2,2]], "attack_count": [2,16,[1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2]], "size": (480, 320), "x_offset": 160},
    ]
    castles = [
        {"hp": 100},
        {"hp": 100},
    ]
    allies = [
        {"name": "わんーこ", "first_spawn": 300, "respawn_time": 120, "spawn_num": 5, "auto_spawn": False, "auto_respawn": True},
        {"name": "にょーろ", "first_spawn": 600, "respawn_time": 200, "spawn_num": 4, "auto_spawn": False, "auto_respawn": True},
    ]
    enemies = [
        {"name": "ネーコ", "first_spawn": 360, "respawn_time": 120, "spawn_num": 7, "auto_spawn": True, "auto_respawn": True},
    ]
    battle = Battle(None, screen_size[0], screen_size[1], characters, castles, 3000, "assets/images/back_grounds/back_ground1.png", allies, enemies)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            battle.handle_event(event)
        battle.step()
        battle.draw(screen)
        pygame.display.flip()
        clock.tick(60)

