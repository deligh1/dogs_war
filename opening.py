import pygame

class Opening:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height

        self.font_address = "assets/fonts/Yuji_Syuku/YujiSyuku-Regular.ttf"
        self.font1 = pygame.font.Font(self.font_address, 36)
        self.font2 = pygame.font.Font(self.font_address, 88)

        self.background_address = "assets/images/back_grounds/opening_bg.png"
        self.background = pygame.image.load(self.background_address)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.title_text = self.font2.render("わんこ大戦争", True, (0,0,0))
        self.title_text_rect = self.title_text.get_rect()
        self.title_text_rect.center = (self.width // 2, self.height * 0.3)

        self.start_button = pygame.Rect(self.width * 0.35, self.height * 0.6, self.width * 0.3, self.height * 0.1)
        self.start_button_text = self.font1.render("はじめる", True, (0,0,0))

    def step(self):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.title_text, self.title_text_rect)
        pygame.draw.rect(screen, (250,250,0), self.start_button)
        screen.blit(self.start_button_text, (self.start_button.centerx - self.start_button_text.get_width() // 2, self.start_button.centery - self.start_button_text.get_height() // 2))


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                self.game.change_scene("start")

if __name__ == "__main__":
    import random

    chugoku = ["TOTTORI", "SHIMANE", "OKAYAMA", "HIROSHIMA", "YAMAGUCHI"]
    chugoku_rnd = chugoku[:]
    kansei = [False] * 5
    n = [-1] * 5
    nn = [0] * 5
    flag = True
    count = 0
    while True:
        count += 1
        for i in range(5):
            s = list(chugoku[i])
            random.shuffle(s)
            chugoku_rnd[i] = "".join(s)
        if flag:
            print(*chugoku_rnd)
        for i in range(5):
            if not kansei[i] and chugoku[i] == chugoku_rnd[i]:
                kansei[i] = True
                n[i] = count
                flag = False
            nn[i] += 1
        if kansei[0] and kansei[1] and kansei[2] and kansei[3] and kansei[4]:
            break
    print(n,nn)
    