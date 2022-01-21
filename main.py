import pygame
import random
import math
pygame.init()

WINDOW_SIZE = (1100, 550)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Shooter")

# Game Background
bg = pygame.image.load("BG.png")
bg = pygame.transform.scale(bg, WINDOW_SIZE)

# Game Logo
gameLogo = pygame.image.load("MenuPage/defeatTheZombiesLogo.png")
gameLogo = pygame.transform.scale(gameLogo, (219, 263))

# Menu Background
menuBg = pygame.image.load("MenuPage/graveYardPic (not made by me).png")
menuBg = pygame.transform.scale(menuBg, WINDOW_SIZE)

# Rules Page Background
rulesBg = pygame.image.load("RulesPage/rulesBg.png")
rulesBg = pygame.transform.scale(rulesBg, WINDOW_SIZE)

# Game Controls
gameControls = pygame.image.load("RulesPage/shooterGameControls.png")
gameControls = pygame.transform.scale(gameControls, (274, 328))

# Hand Sprites
rightFacingHands = pygame.image.load("Hands/rightFacingHands.png")
rightFacingHands = pygame.transform.scale(rightFacingHands, (480, 480))
leftFacingHands = pygame.image.load("Hands/leftFacingHands.png")
leftFacingHands = pygame.transform.scale(leftFacingHands, (480, 480))

# Pistol Sprites
rightFacingPistol = pygame.image.load("Pistol/rightFacingPistol.png")
rightFacingPistol = pygame.transform.scale(rightFacingPistol, (384, 384))
leftFacingPistol = pygame.image.load("Pistol/leftFacingPistol.png")
leftFacingPistol = pygame.transform.scale(leftFacingPistol, (384, 384))


class Player:
    def __init__(self):
        self.health = 100
        self.score = 0
        self.lives = 3
        self.livesImg = pygame.image.load("heart.png")

        with open("highScore.txt", "r") as f:
            self.highScore = int(f.read())

    def displayDetails(self):
        if self.score > self.highScore:
            self.highScore = self.score

        if self.health <= 0:
            self.lives -= 1
            self.health = 100 - abs(self.health)

        if self.lives == 0:
            gameOver()

        # Score Labels
        font = pygame.font.SysFont("Arial", 30, "bold")
        window.blit(font.render(f"SCORE:{self.score}", True, (0, 0, 0)), (5, 5))
        window.blit(font.render(f"HIGH SCORE:{self.highScore}", True, (0, 0, 0)), (5, 40))

        # Health Bar
        font2 = pygame.font.SysFont("Arial", 15, "bold")
        window.blit(font2.render(f"HEALTH:{self.health}", True, (255, 255, 255)), (980, 0))
        pygame.draw.rect(window, (255, 0, 0), (980 + self.health, 20, 100 - self.health, 20))
        pygame.draw.rect(window, (0, 255, 0), (980, 20, self.health, 20))

        # Lives
        x = 900
        for i in range(self.lives):
            window.blit(self.livesImg, (x, 5))
            x -= 50

    def init(self):
        self.health = 100
        self.score = 0
        self.lives = 3

        with open("highScore.txt", "r") as f:
            self.highScore = int(f.read())


player = Player()


class Zombie:
    def __init__(self, x, y, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.isAlive = True

        # Zombie Sprites
        zombie = pygame.image.load("Zombie/zombie.png")
        self.zombie = pygame.transform.scale(zombie, (320, 320))
        deadZombie = pygame.image.load("Zombie/deadZombie.png")
        self.deadZombie = pygame.transform.scale(deadZombie, (320, 320))

    def spawn(self):
        window.blit(self.zombie, (self.x, self.y))

    def move(self, zombies):
        if self.y < 220:
            self.y += self.speed
        else:
            player.health -= self.damage
            zombies.remove(self)

    def dead(self):
        window.blit(self.deadZombie, (self.x, self.y))


class Bullet:
    def __init__(self, x, y, dest:tuple, speed, side, zombies, bullets):
        self.x = x
        self.y = y
        self.dest = dest
        self.speed = speed
        self.side = side
        self.zombies = zombies
        self.bullets = bullets

        # Bullet Sprites
        rightFacingBullet = pygame.image.load("Bullet/rightFacingBullet.png")
        self.rightFacingBullet = pygame.transform.scale(rightFacingBullet, (50, 50))
        leftFacingBullet = pygame.image.load("Bullet/leftFacingBullet.png")
        self.leftFacingBullet = pygame.transform.scale(leftFacingBullet, (50, 50))

    def spawn(self):
        if self.side == "right":
            window.blit(self.rightFacingBullet, (self.x, self.y))
        else:
            window.blit(self.leftFacingBullet, (self.x, self.y))

    def move(self):
        if not self.hasCollided():
            angle = math.atan2((self.dest[1] - self.y), (self.dest[0] - self.x))
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)

        distance = math.sqrt((self.dest[1] - self.y)**2 + (self.dest[0] - self.x)**2)
        if distance < self.speed:
            try:
                self.bullets.remove(self)
            except ValueError:
                pass

    def hasCollided(self):
        for zombie in self.zombies:
            if zombie.x <= self.x <= zombie.x+320 and zombie.y <= self.y <= zombie.y+320:
                player.score += 5
                zombie.isAlive = False
                self.bullets.remove(self)
                return True
        return False


def fillWindow():
    window.blit(bg, (0, 0))


def saveHighScore():
    with open("highScore.txt", "w") as f:
        f.write(str(player.highScore))


side = "left"
def showHands():
    if side == "left":
        window.blit(leftFacingHands, (250, 100))
        window.blit(leftFacingPistol, (250, 220))
    else:
        window.blit(rightFacingHands, (300, 100))
        window.blit(rightFacingPistol, (400, 220))


def pauseGame(clock):
    font1 = pygame.font.SysFont("Arial", 60, "bold")
    font2 = pygame.font.SysFont("Arial", 35, "bold")
    while True:
        fillWindow()

        pygame.draw.rect(window, "#9400ff", (300, 120, 520, 300))
        window.blit(font1.render("PAUSED", True, (0, 0, 0)), (430, 130))

        pygame.draw.rect(window, "#dd5aff", (325, 260, 220, 80))
        window.blit(font2.render("CONTINUE", True, (0, 0, 0)), (345, 280))

        pygame.draw.rect(window, "#dd5aff", (575, 260, 220, 80))
        window.blit(font2.render("QUIT", True, (0, 0, 0)), (635, 280))

        clock.tick(30)
        font = pygame.font.SysFont("Arial", 30, "bold")
        window.blit(font.render(f"FPS:{int(clock.get_fps())}", True, (0, 0, 0)), (5, 515))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                saveHighScore()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()

                if 325 <= mouseX <= 545 and 260 <= mouseY <= 340:
                    return

                if 575 <= mouseX <= 795 and 260 <= mouseY <= 340:
                    saveHighScore()
                    player.init()
                    menu()

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_p]:
                    return

                if keys[pygame.K_q]:
                    saveHighScore()
                    player.init()
                    menu()

        pygame.display.update()


def main():
    global side
    clock = pygame.time.Clock()
    # stores zombie objects
    zombies = []
    # stores bullet objects
    bullets = []
    # time (in milliseconds) between each zombie spawning
    spawnWait = 500
    # ms * 2
    time = 0
    # counts iterations
    count = 0
    # zombie speed
    speed = 2
    # Amount of zombies that can be displayed on screen at the same time
    zombieLimit = 10
    # Stores the player's scores
    scoresList = []
    # Zombie damage
    damage = 5
    # main game loop
    while True:
        time += 10
        count += 1
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                saveHighScore()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                gunShot = pygame.mixer.Sound("Music/GunShot.wav")
                gunShot.set_volume(0.5)
                gunShot.play()

                mouseX, mouseY = pygame.mouse.get_pos()
                if mouseX < 500:
                    side = "left"
                    x = 280
                else:
                    side = "right"
                    x = 705

                b = Bullet(x, 380, (mouseX, mouseY), 50, side, zombies, bullets)
                bullets.append(b)

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    saveHighScore()
                    player.init()
                    menu()

                if keys[pygame.K_p]:
                    pauseGame(clock)

        clock.tick(30)
        fillWindow()
        showHands()
        font = pygame.font.SysFont("Arial", 30, "bold")
        window.blit(font.render(f"FPS:{int(clock.get_fps())}", True, (0, 0, 0)), (5, 515))

        player.displayDetails()

        if (len(zombies) < zombieLimit and time >= spawnWait) or count == 1:
            time = 0
            zombieX = random.randint(50, 900)

            while 150 <= zombieX <= 500:
                zombieX = random.randint(50, 900)

            z = Zombie(zombieX, -50, speed, damage)
            zombies.append(z)

        for zombie in zombies:
            if zombie.isAlive:
                zombie.spawn()
                zombie.move(zombies)
            else:
                zombie.dead()
                pygame.display.update()
                zombies.remove(zombie)

        for bullet in bullets:
            bullet.spawn()
            bullet.move()

        scoresList.append(player.score)

        if speed >= 10 and zombieLimit >= 15 and spawnWait <= 150 and damage >= 30:
            font2 = pygame.font.SysFont("Berlin Sans FB Demi", 60, "bold")
            window.blit(font2.render("EXTREME", True, (136, 0, 21)), (400, 10))
            window.blit(font2.render("MODE", True, (136, 0, 21)), (440, 60))
        else:
            if player.score > 0 and player.score % 30 == 0:
                if scoresList[-1] != scoresList[-2]:
                    speed += 0.5
                    zombieLimit += 1
                    spawnWait -= 20
                    if damage < 30:
                        damage += 5

        pygame.display.update()


def menu():
    font = pygame.font.SysFont("cooperblack", 60)
    playLabel = font.render("PLAY", True, (0, 0, 0))
    rulesLabel = font.render("RULES", True, (0, 0, 0))

    gameMusic = pygame.mixer.Sound("Music/gameMusic.wav")
    gameMusic.play(-1)
    while True:
        window.blit(menuBg, (0, 0))
        window.blit(gameLogo, (430, 30))
        pygame.draw.rect(window, "#90000d", (420, 300, 250, 100))
        window.blit(playLabel, (455, 315))
        pygame.draw.rect(window, "#90000d", (420, 420, 250, 100))
        window.blit(rulesLabel, (440, 435))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if 420 <= mouseX <= 670 and 420 <= mouseY <= 520:
                    rules()

                if 420 <= mouseX <= 670 and 300 <= mouseY <= 400:
                    gameMusic.stop()
                    main()

        pygame.display.update()


def rules():
    window.fill((255, 255, 255))
    font = pygame.font.SysFont("comicsans", 30)
    font2 = pygame.font.SysFont("Arial MT Rounded Bold", 100, "bold")
    font3 = pygame.font.SysFont("Arial", 40, "bold")
    while True:
        y = 150

        window.blit(rulesBg, (0, 0))
        window.blit(gameControls, (800, 120))
        window.blit(font2.render("Rules", True, (0, 0, 0)), (430, 50))
        pygame.draw.rect(window, (0, 0, 255), (10, 10, 50, 50))
        window.blit(font3.render("X", True, (255, 255, 255)), (22, 12))

        with open("rules.txt", "r") as f:
            for line in f.readlines():
                window.blit(font.render(line[:-1], True, (0, 0, 0)), (40, y))
                y += 35

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if 10 <= mouseX <= 60 and 10 <= mouseY <= 60:
                    window.fill((0, 0, 0))
                    pygame.display.update()
                    return

        pygame.display.update()


def gameOver():
    saveHighScore()
    stopSound = pygame.mixer.Sound("Music/STOP.wav")
    gameOverSound = pygame.mixer.Sound("Music/GameOver.wav")
    gameOverSound.play(-1)
    hasBeenStopped = False
    font = pygame.font.SysFont("cooperblack", 60)
    font2 = pygame.font.SysFont("Arial", 30, "bold")
    while True:
        window.fill((0, 0, 0))

        gameOver = pygame.image.load("GameOver.png")
        gameOver = pygame.transform.scale(gameOver, WINDOW_SIZE)
        window.blit(gameOver, (0, 0))

        pygame.draw.rect(window, "#8800ff", (600, 350, 200, 80))
        window.blit(font.render("Menu", True, (0, 0, 0)), (620, 350))

        window.blit(font2.render(f"SCORE:{player.score}", True, (0, 0, 0)), (620, 280))

        if not hasBeenStopped:
            pygame.draw.rect(window, (255, 0, 0), (5, 5, 200, 80))
            window.blit(font.render("STOP", True, (255, 255, 255)), (20, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if not hasBeenStopped:
                    if 5 <= mouseX <= 205 and 5 <= mouseY <= 85:
                        gameOverSound.stop()
                        stopSound.play()
                        hasBeenStopped = True

                if 600 <= mouseX <= 800 and 350 <= mouseY <= 430:
                    gameOverSound.stop()
                    player.init()
                    menu()

        pygame.display.update()


if __name__ == "__main__":
    menu()
