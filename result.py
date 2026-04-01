import pygame

class Result:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height

        self.font_address = "assets/fonts/Yuji_Syuku/YujiSyuku-Regular.ttf"
        self.font1 = pygame.font.Font(self.font_address, 70)
        self.font2 = pygame.font.Font(self.font_address, 40)

        self.result_text = self.font1.render(f"{self.game.stage} / {len(self.game.data['stages'][self.game.mode])}", True, (0,0,0))
        self.title_text = self.font2.render("タイトルへ", True, (0,0,0))
        self.title_text_rect = self.title_text.get_rect()
        self.title_text_rect.center = (self.width // 2, self.height * 0.7)

    def step(self):
        pass

    def draw(self, screen):
        screen.fill((255,255,255))
        pygame.draw.rect(screen, (255,255,0), (self.width * 0.1, self.height * 0.1, self.width * 0.8, self.height * 0.8))
        screen.blit(self.result_text, (self.width // 2 - self.result_text.get_width(), self.height * 0.2))
        screen.blit(self.title_text, self.title_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.title_text_rect.collidepoint(event.pos):
                self.game.change_scene("return")

if __name__ == "__main__":
    import random
    a = "{character}"
    b = "{character} 取得"
    print(a in b)