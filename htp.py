import pygame

class Htp:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.page = 0

        self.font_address = "assets/fonts/Yuji_Syuku/YujiSyuku-Regular.ttf"
        self.font1 = pygame.font.Font(self.font_address, 36)
        self.font2 = pygame.font.Font(self.font_address, 24)
        self.font3 = pygame.font.Font(self.font_address, 20)

        self.background_address = ["assets/images/screenshots/select.png",
                                   "assets/images/screenshots/enhancement00.png",
                                   "assets/images/screenshots/enhancement01.png",
                                   "assets/images/screenshots/enhancement02.png",
                                   "assets/images/screenshots/enhancement02.png",
                                   "assets/images/screenshots/battle.png",
                                   "assets/images/screenshots/gray.png"]
        self.backgrounds = [pygame.image.load(i) for i in self.background_address]
        self.backgrounds = [pygame.transform.scale(i, (self.width*0.8, self.height*0.8)) for i in self.backgrounds]
        self.black_rect = pygame.Rect(self.width * 0.1 - 10, self.height * 0, self.width * 0.8 + 20, self.height * 0.8 + 20)

        self.title_text = self.font2.render("わんこ大戦争", True, (0,0,0))
        self.title_text_rect = self.title_text.get_rect()
        self.title_text_rect.center = (self.width // 2, self.height * 0.3)

        self.start_button_prev = pygame.Rect(self.width * 0.05, self.height * 0.85, self.width * 0.1, self.height * 0.1)
        self.start_button_prev_text = self.font1.render("前へ", True, (0,0,0))
        self.start_button_next = pygame.Rect(self.width * 0.85, self.height * 0.85, self.width * 0.1, self.height * 0.1)
        self.start_button_next_text = self.font1.render("次へ", True, (0,0,0))

        self.text = ["強化内容を選択し、「これにする」を押します。","上側に自陣の強化、下側に敵陣の強化が書いてあります。",
                     "編成と、Gを使用しての強化ができます。","所持Gは右上、編成は下に表示されています。",
                     "左上のキャラクターを選択すると、","枠の色が変わり強化できるようになります。",
                     "キャラクターを選択した状態でスロットのキャラクターをクリックすると、","スロットのキャラクターを上書きできます。",
                     "「開戦」をクリックするとバトルに進みます。","",
                     "バトルは自動で進みます。","右上のボタンで倍速、10倍速、投了ができます。",
                     "単語の説明です。",""]
        self.text1 = [self.font2.render(i, True, (0,0,0)) for i in self.text[0::2]]
        self.text2 = [self.font2.render(i, True, (0,0,0)) for i in self.text[1::2]]

        self.setumei = ["強化倍率 : 体力・攻撃力に掛かる倍率",
                        "出撃数 : そのキャラクターが出撃される数",
                        "初期待機 : 一体目が出撃されるまでの待機時間",
                        "再生産 : 二体目以降の待機時間",
                        "城体力 : 城の体力。自陣側の城が攻撃を受けて0になると敗北、敵陣側の城を攻撃して0にすると勝利",
                        "スロット : 編成の一つの枠の事",
                        "出撃制限 : 同時にステージ上に存在できる味方の最大数。これを超えて出撃する事はできない。",
                        "報酬 : 勝利した際に得られるゴールドの事",
                        "めっぽう強い : 特定の敵に対してのダメージを軽減し、攻撃を増幅する",
                        "動きを止める : 攻撃時、一定確率で攻撃した敵の動きを一定時間止める",
                        "ふっとばす : 攻撃時、敵を後ろに吹っ飛ばす"]
        self.setumei_texts = []
        self.setumei_rect = []
        for i, text in enumerate(self.setumei):
            self.setumei_texts.append(self.font3.render(text, True, (0,0,0)))
            self.setumei_rect.append(pygame.Rect(self.width * 0.1, self.height * (0.02 + 0.06 * i), self.width, self.height))
        self.img_path = ["assets/images/characters/わんーこ/move1.png",
                         "assets/images/characters/ネーコ/move1.png",
                         "assets/images/characters/タンクネーコ/move1.png"]
        scales = [i*self.width//1200 for i in [160,160,320]]
        self.imgs = []
        for ii, i in enumerate(self.img_path):
            img = pygame.image.load(i)
            x, y = img.get_size()
            self.imgs.append(pygame.transform.scale(img, (x * scales[ii] // y, scales[ii])))

    def step(self):
        pass

    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0,0,0), self.black_rect)

        screen.blit(self.backgrounds[self.page], (self.width * 0.1, 10))
        # screen.blit(self.title_text, self.title_text_rect)
        pygame.draw.rect(screen, (250,250,0) if self.page > 0 else (128,128,128), self.start_button_prev)
        screen.blit(self.start_button_prev_text, (self.start_button_prev.centerx - self.start_button_prev_text.get_width() // 2, self.start_button_prev.centery - self.start_button_prev_text.get_height() // 2))
        pygame.draw.rect(screen, (250,250,0), self.start_button_next)
        screen.blit(self.start_button_next_text, (self.start_button_next.centerx - self.start_button_next_text.get_width() // 2, self.start_button_next.centery - self.start_button_next_text.get_height() // 2))

        text_rect = self.text1[self.page].get_rect()
        text_rect.center = (self.width // 2, self.height * 0.88)
        screen.blit(self.text1[self.page], text_rect)
        text_rect = self.text2[self.page].get_rect()
        text_rect.center = (self.width // 2, self.height * 0.92)
        screen.blit(self.text2[self.page], text_rect)

        def scale(x,y,w,h):
            return (self.width * x, self.height * y, self.width * w, self.height * h)
        color = (0,0,255)
        if self.page == 0:
            pass
        if self.page == 1:
            pass
        if self.page == 2:
            pygame.draw.ellipse(screen, color, scale(0.08,0.04,0.28,0.15), 10)
        if self.page == 3:
            pygame.draw.ellipse(screen, color, scale(0.45,0.69,0.1,0.15), 10)
        if self.page == 4:
            pygame.draw.ellipse(screen, color, scale(0.74,0.48,0.16,0.21), 10)
        if self.page == 5:
            pass
        if self.page == 6:
            for i in range(len(self.setumei)):
                screen.blit(self.setumei_texts[i], self.setumei_rect[i])
            screen.blit(self.imgs[0], (self.width * 0.53, self.height * 0.65))
            screen.blit(self.imgs[1], (self.width * 0.73, self.height * 0.56))
            screen.blit(self.imgs[2], (self.width * 0.76, self.height * 0.38))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_prev.collidepoint(event.pos):
                if self.page != 0:
                    self.page -= 1
            if self.start_button_next.collidepoint(event.pos):
                if self.page == len(self.background_address) - 1:
                    self.game.change_scene("return")
                else:
                    self.page += 1

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
    