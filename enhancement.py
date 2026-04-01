import pygame

class Enhancement:
    def __init__(self, game, width, height, allies, slots):
        self.game = game
        self.width = width
        self.height = height
        self.allies = allies
        self.slots = slots # ex. [0,1,2]

        self.font_address = "assets/fonts/Yuji_Syuku/YujiSyuku-Regular.ttf"
        self.font1 = pygame.font.Font(self.font_address, 24)
        self.font2 = pygame.font.Font(self.font_address, 48)

        self.allies_img = [pygame.image.load(f"assets/images/characters/{a['name']}/move1.png") for a in self.allies]
        self.character_buttons_update()
        self.selected = -1
        self.allies_update()
        self.character_update()
        self.other_update()
        
    def character_buttons_update(self):
        self.character_buttons = [pygame.Rect(self.width * (100 - 10 * len(self.slots) + 1 + 20 * i) // 200, self.height - 95, self.width * 0.09, 90) for i in range(len(self.slots))]

    def allies_update(self):
        self.allies_rect = pygame.Rect(8, 6, self.width * 0.3 - 8, self.height * 0.8)
        self.allies_buttons = []
        for i in range(len(self.allies)):
            r = i % 3
            c = i // 3
            self.allies_buttons.append(pygame.Rect(self.width * 0.095 * r + 10, c * 100 + 10, self.width * 0.09, 90))
        self.character_img = [pygame.transform.scale(self.allies_img[i], (90 * a["size"][0] // a["size"][1], 90)) for i,a in enumerate(self.allies)]
        empty_rect = pygame.Surface((self.width * 0.09, 90))
        empty_rect.fill((128,128,128))
        self.character_img.append(empty_rect)
    
    def character_update(self):
        self.gold_text = self.font1.render(f"{self.game.coin} G", True, (0,0,0))

        self.character_rect = pygame.Rect(self.width * 0.3 + 8, 6, self.width * 0.5 - 16, self.height * 0.8)
        w, h = self.width * 0.15, self.height * 0.22
        self.character_window = pygame.Rect(self.width * 0.3 + 14, 10, w, h)
        if self.selected == -1:
            self.character_window_img = pygame.transform.scale(self.character_img[self.selected], (w, h))
        else:
            self.character_window_img = pygame.transform.scale(self.allies_img[self.selected], (h * self.character_img[self.selected].get_width() / self.character_img[self.selected].get_height(), h))
        
        if self.selected != -1:
            name = self.allies[self.selected]["name"]
            cost = self.game.data2["allies"][name]["cost"]
            enhancement = self.game.data2["allies"][name]["enhancement"]
            items = self.game.data2["allies"][name]["items"]
        else:
            cost = 0
            enhancement = {"magnification": 0,
                "first_wait": 0,
                "respawn": 0,
                "spawn_num": 0,
                "ability": {}}
            items = {
                "magnification": 1,
                "first_wait": 1,
                "respawn": 1,
                "spawn_num": 1,
                "ability": {}
            }
        self.magnification_text = self.font1.render(f"強化倍率：{enhancement['magnification'] * items['magnification']:.2f}倍", True, (0,0,0))
        self.magnification_button = pygame.Rect(self.width * 0.65, 10, self.width * 0.13, self.height * 0.05)
        self.magnification_button_text = self.font1.render(f"強化　{cost} G", True, (0,0,0))

        self.num_text = self.font1.render(f"個体数　：{int(enhancement['spawn_num'] * items['spawn_num'])}体", True, (0,0,0))
        self.num_button = pygame.Rect(self.width * 0.65, 10 + self.height * 0.055, self.width * 0.13, self.height * 0.05)
        self.num_button_text = self.font1.render(f"増加　{cost} G", True, (0,0,0))

        self.firstspawn_text = self.font1.render(f"初期待機：{enhancement['first_wait'] / 30 / items['first_wait']:.2f}秒", True, (0,0,0))
        self.firstspawn_button = pygame.Rect(self.width * 0.65, 10 + self.height * 0.11, self.width * 0.13, self.height * 0.05)
        self.firstspawn_button_text = self.font1.render(f"短縮　{cost} G", True, (0,0,0))
        
        self.respawn_text = self.font1.render(f"再生産　：{enhancement['respawn'] / 30 / items['respawn']:.2f}秒", True, (0,0,0))
        self.respawn_button = pygame.Rect(self.width * 0.65, 10 + self.height * 0.165, self.width * 0.13, self.height * 0.05)
        self.respawn_button_text = self.font1.render(f"短縮　{cost} G", True, (0,0,0))

    def other_update(self):
        self.gold_text = self.font1.render(f"{self.game.coin} G", True, (0,0,0))

        self.others_rect = pygame.Rect(self.width * 0.8, 6 + self.height * 0.07, self.width * 0.2 - 8, self.height * 0.6)

        name = self.allies[self.selected]["name"]
        cost = self.game.data2["costs"]
        other = self.game.data2
        self.castlehp_text = self.font1.render(f"城体力　　：{int(other['castle_hp'] * other['items']['castle_hp'])}", True, (0,0,0))
        self.castlehp_button = pygame.Rect(self.width * 0.83, 10 + self.height * 0.13, self.width * 0.14, self.height * 0.05)
        self.castlehp_button_text = self.font1.render(f"強化　{cost['castle_hp']} G", True, (0,0,0))

        self.slot_text = self.font1.render(f"スロット　：{other['slot'] + other['items']['slot']}枠", True, (0,0,0))
        self.slot_button = pygame.Rect(self.width * 0.83, 10 + self.height * 0.25, self.width * 0.14, self.height * 0.05)
        self.slot_button_text = self.font1.render(f"増加　{cost['slot']} G", True, (0,0,0))

        self.maxspawn_text = self.font1.render(f"出撃制限　：{int(other['max_spawn'] * other['items']['max_spawn'])}体", True, (0,0,0))
        self.maxspawn_button = pygame.Rect(self.width * 0.83, 10 + self.height * 0.37, self.width * 0.14, self.height * 0.05)
        self.maxspawn_button_text = self.font1.render(f"増加　{cost['max_spawn']} G", True, (0,0,0))

        self.reward_text = self.font1.render(f"クリア報酬：{int(other['reward'] * other['items']['reward'])}", True, (0,0,0))
        self.reward_button = pygame.Rect(self.width * 0.83, 10 + self.height * 0.49, self.width * 0.14, self.height * 0.05)
        self.reward_button_text = self.font1.render(f"増加　{cost['reward']} G", True, (0,0,0))

        self.start_button = pygame.Rect(self.width * 0.82, 10 + self.height * 0.68, self.width * 0.16, self.height * 0.11)
        self.start_button_text = self.font2.render(f"開戦", True, (0,0,0))
        


    def step(self):
        pass

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for i in range(len(self.slots)):
            pygame.draw.rect(screen, (255,255,255), self.character_buttons[i])
            screen.blit(self.character_img[self.slots[i]], self.character_buttons[i])
            pygame.draw.rect(screen, (0,0,0), self.character_buttons[i], width=4)

        pygame.draw.rect(screen, (50,255,50), self.allies_rect)
        for i in range(len(self.allies_buttons)):
            pygame.draw.rect(screen, (255,255,255), self.allies_buttons[i])
            color = (0,255,0) if i == self.selected else (0,0,0)
            screen.blit(self.character_img[i], self.allies_buttons[i])
            pygame.draw.rect(screen, color, self.allies_buttons[i], width=4)

        pygame.draw.rect(screen, (170,170,255), self.character_rect)
        pygame.draw.rect(screen, (255,255,255), self.character_window)
        screen.blit(self.character_window_img, self.character_window)
        pygame.draw.rect(screen, (0,0,0), self.character_window, width=4)

        screen.blit(self.magnification_text, (self.width * 0.45 + 20, 8))
        pygame.draw.rect(screen, (255,255,0), self.magnification_button)
        screen.blit(self.magnification_button_text, (self.magnification_button.centerx - self.magnification_button_text.get_width() // 2, self.magnification_button.centery - self.magnification_button_text.get_height() // 2))

        screen.blit(self.num_text, (self.width * 0.45 + 20, 8 + self.height * 0.055))
        pygame.draw.rect(screen, (255,255,0), self.num_button) 
        screen.blit(self.num_button_text, (self.num_button.centerx - self.num_button_text.get_width() // 2, self.num_button.centery - self.num_button_text.get_height() // 2))

        screen.blit(self.firstspawn_text, (self.width * 0.45 + 20, 8 + self.height * 0.11))
        pygame.draw.rect(screen, (255,255,0), self.firstspawn_button) 
        screen.blit(self.firstspawn_button_text, (self.firstspawn_button.centerx - self.firstspawn_button_text.get_width() // 2, self.firstspawn_button.centery - self.firstspawn_button_text.get_height() // 2))

        screen.blit(self.respawn_text, (self.width * 0.45 + 20, 8 + self.height * 0.165))
        pygame.draw.rect(screen, (255,255,0), self.respawn_button) 
        screen.blit(self.respawn_button_text, (self.respawn_button.centerx - self.respawn_button_text.get_width() // 2, self.respawn_button.centery - self.respawn_button_text.get_height() // 2))

        # others
        screen.blit(self.gold_text, (self.width * 0.9, 8 + self.height * 0))
        pygame.draw.rect(screen, (255,130,130), self.others_rect)

        screen.blit(self.castlehp_text, (self.castlehp_button.centerx - self.castlehp_text.get_width() // 2, self.castlehp_button.top - self.height * 0.06))
        pygame.draw.rect(screen, (255,255,0), self.castlehp_button) 
        screen.blit(self.castlehp_button_text, (self.castlehp_button.centerx - self.castlehp_button_text.get_width() // 2, self.castlehp_button.centery - self.castlehp_button_text.get_height() // 2))

        screen.blit(self.slot_text, (self.slot_button.centerx - self.slot_text.get_width() // 2, self.slot_button.top - self.height * 0.06))
        pygame.draw.rect(screen, (255,255,0), self.slot_button) 
        screen.blit(self.slot_button_text, (self.slot_button.centerx - self.slot_button_text.get_width() // 2, self.slot_button.centery - self.slot_button_text.get_height() // 2))

        screen.blit(self.maxspawn_text, (self.maxspawn_button.centerx - self.maxspawn_text.get_width() // 2, self.maxspawn_button.top - self.height * 0.06))
        pygame.draw.rect(screen, (255,255,0), self.maxspawn_button) 
        screen.blit(self.maxspawn_button_text, (self.maxspawn_button.centerx - self.maxspawn_button_text.get_width() // 2, self.maxspawn_button.centery - self.maxspawn_button_text.get_height() // 2))

        screen.blit(self.reward_text, (self.reward_button.centerx - self.reward_text.get_width() // 2, self.reward_button.top - self.height * 0.06))
        pygame.draw.rect(screen, (255,255,0), self.reward_button) 
        screen.blit(self.reward_button_text, (self.reward_button.centerx - self.reward_button_text.get_width() // 2, self.reward_button.centery - self.reward_button_text.get_height() // 2))

        pygame.draw.rect(screen, (255,255,0), self.start_button) 
        screen.blit(self.start_button_text, (self.start_button.centerx - self.start_button_text.get_width() // 2, self.start_button.centery - self.start_button_text.get_height() // 2))


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.character_buttons):
                if rect.collidepoint(event.pos):
                    if self.selected in self.slots:
                        pass
                    else:
                        self.slots[i] = self.selected
                    break
            for i, rect in enumerate(self.allies_buttons):
                if rect.collidepoint(event.pos):
                    self.selected = i
                    self.character_update()
                    break

            if self.magnification_button.collidepoint(event.pos):
                # print(12)
                if self.selected == -1:
                    return
                if self.game.coin < self.game.data2["allies"][self.allies[self.selected]["name"]]["cost"] * 1:
                    return
                self.game.coin -= self.game.data2["allies"][self.allies[self.selected]["name"]]["cost"] * 1
                self.game.data2["allies"][self.allies[self.selected]["name"]]["enhancement"]["magnification"] += 0.1
                self.character_update()
            if self.num_button.collidepoint(event.pos):
                if self.selected == -1:
                    return
                if self.game.coin < self.game.data2["allies"][self.allies[self.selected]["name"]]["cost"] * 1:
                    return
                self.game.coin -= self.game.data2["allies"][self.allies[self.selected]["name"]]["cost"] * 1
                self.game.data2["allies"][self.allies[self.selected]["name"]]["enhancement"]["spawn_num"] += 1
                self.character_update()
            if self.firstspawn_button.collidepoint(event.pos):
                if self.selected == -1:
                    return
                if self.game.coin < self.game.data2["allies"][self.allies[self.selected]["name"]]["cost"] * 1:
                    return
                self.game.coin -= self.game.data2["allies"][self.allies[self.selected]["name"]]["cost"] * 1
                self.game.data2["allies"][self.allies[self.selected]["name"]]["enhancement"]["first_wait"] /= 1.1
                self.character_update()
            if self.respawn_button.collidepoint(event.pos):
                if self.selected == -1:
                    return
                if self.game.coin < self.game.data2["allies"][self.allies[self.selected]["name"]]["cost"] * 1:
                    return
                self.game.coin -= self.game.data2["allies"][self.allies[self.selected]["name"]]["cost"] * 1
                self.game.data2["allies"][self.allies[self.selected]["name"]]["enhancement"]["respawn"] /= 1.1
                self.character_update()

            if self.castlehp_button.collidepoint(event.pos):
                if self.game.coin < self.game.data2["costs"]["castle_hp"]:
                    return
                self.game.data2["castle_hp"] += 50
                self.game.coin -= self.game.data2["costs"]["castle_hp"]
                self.other_update()
            if self.slot_button.collidepoint(event.pos):
                if self.game.coin < self.game.data2["costs"]["slot"]:
                    return
                self.game.data2["slot"] += 1
                self.game.slots.append(-1)
                self.game.coin -= self.game.data2["costs"]["slot"]
                self.other_update()
                self.character_buttons_update()
            if self.maxspawn_button.collidepoint(event.pos):
                if self.game.coin < self.game.data2["costs"]["max_spawn"]:
                    return
                self.game.data2["max_spawn"] += 1
                self.game.coin -= self.game.data2["costs"]["max_spawn"]
                self.other_update()
            if self.reward_button.collidepoint(event.pos):
                if self.game.coin < self.game.data2["costs"]["reward"]:
                    return
                self.game.data2["reward"] += 10
                self.game.coin -= self.game.data2["costs"]["reward"]
                self.other_update()
            
            if self.start_button.collidepoint(event.pos):
                self.game.change_scene("start")

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
        {"name": "わんーこ", "first_spawn": 300, "respawn_time": 120, "spawn_num": 5, "auto_spawn": False, "auto_respawn": True,"size": (320, 320)},
        {"name": "にょーろ", "first_spawn": 600, "respawn_time": 200, "spawn_num": 4, "auto_spawn": False, "auto_respawn": True,"size": (480, 320)},
        {"name": "にょーろ", "first_spawn": 600, "respawn_time": 200, "spawn_num": 4, "auto_spawn": False, "auto_respawn": True,"size": (480, 320)},
        {"name": "にょーろ", "first_spawn": 600, "respawn_time": 200, "spawn_num": 4, "auto_spawn": False, "auto_respawn": True,"size": (480, 320)},
        {"name": "にょーろ", "first_spawn": 600, "respawn_time": 200, "spawn_num": 4, "auto_spawn": False, "auto_respawn": True,"size": (480, 320)},
    ]
    enemies = [
        {"name": "ネーコ", "first_spawn": 360, "respawn_time": 120, "spawn_num": 7, "auto_spawn": True, "auto_respawn": True},
    ]
    enhance = Enhancement(None, screen_size[0], screen_size[1], allies, [0,1,-1,-1,-1,-1,-1,-1])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            enhance.handle_event(event)
        enhance.step()
        enhance.draw(screen)
        pygame.display.flip()
        clock.tick(30)