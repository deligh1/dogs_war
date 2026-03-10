import random

class character:
    def __init__(self, battle, isally, name, hp, ap, speed, range, attack_time, area, kb, ability, x, y, z, attribute = []):
        self.battle = battle # 戦闘オブジェクト
        self.isally = isally # 味方かどうか
        self.name = name # キャラクター名　画像ファイル名も兼任
        self.max_hp = hp # 最大体力
        self.ap = ap # 攻撃力
        self.speed = speed # 移動速度
        self.range = range # 射程　(感知、最小、最大)
        self.attack_time = attack_time # 攻撃関連の時間　(発生、硬直、待機)
        self.area = area # 範囲攻撃かどうか
        self.kb = kb # ノックバック回数
        self.ability = ability # 特殊能力　[{"name": "能力名", "value": [能力の値]}, ...]
        self.attribute = attribute

        self.hp = self.max_hp # 現在の体力
        self.x = x # 横
        self.y = y # 縦
        self.z = z # 奥行き
        self.state = "move" # キャラクターの状態　(move, wait, attack, kb, back, dead)
        self.status = {"stop": 0, "slow": 0, "down": 0, "back": 0} # 状態異常 {状態名: タイマー}
        self.kb_hp = self.hp - self.hp / self.kb # ノックバックのHP閾値
        self.timer = 0 # 攻撃のタイマー
        self.cooldown = 0 # 攻撃のクールダウン

    def step(self):
        # キャラクターを１フレーム進める
        if self.hp <= self.kb_hp and self.state != "dead" and self.state != "kb":
            self.state = "kb"
            self.timer = 0
            self.kb_hp = (self.hp - 1) // (self.max_hp / self.kb) * (self.max_hp / self.kb)
        elif self.status["back"] > 0: # 多分バグる
            self.state = "back"
        if (self.state == "move" or self.state == "wait") and self.search(self.battle.characters) and self.cooldown == 0:
            self.state = "attack"
            self.timer = 0
        if self.state == "move" and self.search(self.battle.characters) and self.cooldown > 0:
            self.state = "wait"
            self.timer = 0
        elif self.state == "wait" and not self.search(self.battle.characters):
            self.state = "move"
            self.timer = 0

        if self.state == "move":
            # 移動の処理
            dx = self.speed / 2 * (1 if self.isally else -1)
            if self.status["stop"] > 0:
                dx = 0
            elif self.status["slow"] > 0:
                dx = 0.25 * (1 if self.isally else -1)
            self.x += dx
            self.timer += 1
        elif self.state == "wait":
            self.timer += 1

        elif self.state == "attack":
            if self.status["stop"] > 0:
                pass
            else:
                if self.timer == self.attack_time[0]:
                    self.attack(self.battle.characters)
                    self.cooldown = self.attack_time[2]
                if self.timer == self.attack_time[0] + self.attack_time[1]:
                    self.state = "move"
                self.timer += 1
        elif self.state == "kb":
            if self.timer == 23:
                if self.hp <= 0:
                    self.state = "dead"
                    self.timer = 0
                else:
                    self.state = "move"
            else:
                self.x += -15 * (1 if self.isally else -1)
                self.y += ((7 - self.timer) * (0 <= self.timer <= 14) + (18 - self.timer) * (15 <= self.timer <= 21))
                self.timer += 1
        elif self.state == "back":
            if self.status["back"] == 0:
                self.state = "move"
            else:
                self.x += -15 * (1 if self.isally else -1)
        elif self.state == "dead":
            if self.timer == 60:
                self.battle.characters.remove(self)
            self.y += 20
            self.timer += 1

        # 状態異常のタイマーを減らす
        for key in self.status:
            if self.status[key] > 0:
                self.status[key] -= 1
        if self.cooldown > 0:
            self.cooldown -= 1
        # print(self.name, self.state, self.timer, self.cooldown)
        
    def search(self, characters):
        # 周囲のキャラクターを検索する
        targets = []
        for character in characters:
            if character.state == "move" or character.state == "attack" or character.state == "wait":
                if character.isally != self.isally and -320 <= (character.x - self.x) * (1 if self.isally else -1) <= self.range[0]:
                    # print((character.x - self.x) * (1 if self.isally else -1), self.name)
                    targets.append(character)
        return targets
    
    def attack(self, characters):
        # キャラクターを攻撃する
        targets = []
        min_distance = 1e10
        for character in characters:
            if character.state == "move" or character.state == "attack" or character.state == "wait":
                if character.isally != self.isally and self.range[1] <= (character.x - self.x) * (1 if self.isally else -1) <= self.range[2]:
                    if self.area:
                        targets.append(character)
                    else:
                        distance = (character.x - self.x) * (1 if self.isally else -1)
                        if distance < min_distance:
                            min_distance = distance
                            targets = [character]
        for character in targets:
            damage = self.ap * (0.5 if self.status["down"] else 1)
            for ability in self.ability:
                if ability["name"] == "meppo":
                    for attribute in ability["value"]:
                        if attribute in character.attribute:
                            damage *= 1.5
                if ability["name"] == "stop" and random.random < ability["value"][1]:
                    character.status["stop"] = ability["value"][0]
                elif ability["name"] == "slow" and random.random < ability["value"][1]:
                    character.status["slow"] = ability["value"][0]
                elif ability["name"] == "down" and random.random < ability["value"][1]:
                    character.status["down"] = ability["value"][0]
                elif ability["name"] == "back" and random.random < ability["value"][1]:
                    character.status["back"] = ability["value"][0]
            for ability in character.ability:
                if ability["name"] == "meppo":
                    for attribute in ability["value"]:
                        if attribute in self.attribute:
                            damage // 2
                if ability["name"] == "invalid" and random.random < ability["value"][1]:
                    damage = 0
            character.hp -= damage
        