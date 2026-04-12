import pygame

class Select:
    def __init__(self, game, width, height, items):
        self.game = game
        self.width = width
        self.height = height
        self.n = len(items)
        self.items = items
        self.itme_rects = [pygame.Rect(self.width * (i + (i+1) / (self.n + 1)) // (self.n + 1), self.height * 3 // 10, self.width // (self.n + 1), self.height * 6 // 10) for i in range(self.n)]

        self.font_address = "assets/fonts/Yuji_Syuku/YujiSyuku-Regular.ttf"
        self.font1 = pygame.font.Font(self.font_address, 16)
        self.font2 = pygame.font.Font(self.font_address, 40)
        self.font3 = pygame.font.Font(self.font_address, 20)
        self.font4 = pygame.font.Font(self.font_address, 90)

        self.next_button = pygame.Rect(self.width * 0.75, self.height * 0.1, self.width * 0.2, self.height * 0.1)
        self.next_button_text = self.font2.render("これにする", True, (0,0,0))

        self.ally_item_names = [item["ally"]["name"] for item in self.items]
        self.ally_item_name_surfaces = [self.font3.render(name, True, (0,0,0)) for name in self.ally_item_names]
        self.enemy_item_names = [item["enemy"]["name"] for item in self.items]
        self.enemy_item_name_surfaces = [self.font3.render(name, True, (0,0,0)) for name in self.enemy_item_names]

        self.ally_items_texts = [self.text_wrap(item["ally"]["description"], self.font1, self.width // (self.n + 1)) for item in self.items]
        self.ally_items_text_surfaces = [[self.font1.render(line, True, (0, 0, 0)) for line in item_text] for item_text in self.ally_items_texts]
        self.enemy_items_texts = [self.text_wrap(item["enemy"]["description"], self.font1, self.width // (self.n + 1)) for item in self.items]
        self.enemy_items_text_surfaces = [[self.font1.render(line, True, (0, 0, 0)) for line in item_text] for item_text in self.enemy_items_texts]
        self.selected_index = -1
        

    # テキストを複数行にするための関数
    def text_wrap(self, text, font, max_width):
        words = text
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word

        if current_line:
            lines.append(current_line.strip())

        return lines

    def step(self):
        pass

    def draw(self, screen):
        screen.fill((255, 255, 255))
        text = self.font4.render("選ぶべし", True, (0, 0, 0))
        screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 7 - text.get_height() // 2))
        color = (150,150,150) if self.selected_index == -1 else (200,200,200)
        pygame.draw.rect(screen, color, self.next_button)
        screen.blit(self.next_button_text, (self.next_button.centerx - self.next_button_text.get_width() // 2, self.next_button.centery - self.next_button_text.get_height() // 2))

        for i in range(self.n):
            rect = self.itme_rects[i]
            color = (150, 150, 150) if i != self.selected_index else (200, 200, 200)
            pygame.draw.rect(screen, color, rect)
            screen.blit(self.ally_item_name_surfaces[i], (rect.centerx - self.ally_item_name_surfaces[i].get_width() // 2, rect.top))
            screen.blit(self.enemy_item_name_surfaces[i], (rect.centerx - self.enemy_item_name_surfaces[i].get_width() // 2, rect.top + self.height // 3))
            for j, text_surface in enumerate(self.ally_items_text_surfaces[i]):
                screen.blit(text_surface, (rect.left, rect.top + j * 20 + 40))
            for j, text_surface in enumerate(self.enemy_items_text_surfaces[i]):
                screen.blit(text_surface, (rect.left, rect.top + self.height // 3 + j * 20 + 40))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.itme_rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = i
                    break
            if self.next_button.collidepoint(event.pos):
                self.game.change_scene(self.selected_index)
        
if __name__ == "__main__":
    pygame.init()
    game = type("Game", (), {"width": 1200, "height": 800, "n": 3})()
    items = [
        {
            "ally": {"name": "味方アイテム1", "description": "効果: 体力回復"},
            "enemy": {"name": "敵アイテム1", "description": "効果: 攻撃力アップ"}
        },
        {
            "ally": {"name": "味方アイテム2", "description": "効果: 防御力アップ"},
            "enemy": {"name": "敵アイテム2", "description": "効果: 速度ダウン"}
        },
        {
            "ally": {"name": "味方アイテム3", "description": "効果: スキルクールダウン短縮"},
            "enemy": {"name": "敵アイテム3", "description": "効果: スキルクールダウン延長"}
        }
    ]
    select = Select(game, game.width, game.height,items)
    screen = pygame.display.set_mode((game.width, game.height))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            select.handle_event(event)

        select.step()
        select.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()