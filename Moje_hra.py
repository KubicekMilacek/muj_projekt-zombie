import pygame
import random

# Inicializace Pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 1152, 526
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")

# Načtení pozadí
background = pygame.image.load("background.png")

# Barvy
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 100, 0)

# Hráč
player = {
    "x": 50,
    "y": HEIGHT // 2 - 25,
    "width": 40,
    "height": 50,
    "speed": 5,
    "lives": 3,
    "fire_rate": 500,  # 0.5 sekundy cooldown
    "last_shot": 0
}

# Střely
bullets = []

# Zombíci
zombies = []
zombie_speed = 2

# Vlna
wave = {
    "current": 1,
    "zombies_left": 50,
    "speed_multiplier": 1.0
}

# Obchod
store = {
    "weapon_upgrade_cost": 10,
    "fire_rate_upgrade": 100,  # Snížení cooldownu střelby
    "money": 0
}

# Power-upy
powerups = []

# Časovač
clock = pygame.time.Clock()

# Hlavní smyčka
running = True
while running:
    screen.blit(background, (0, 0))
    current_time = pygame.time.get_ticks()

    # Události
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pohyb hráče
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player["y"] > 120:
        player["y"] -= player["speed"]
    if keys[pygame.K_DOWN] and player["y"] < HEIGHT - player["height"]:
        player["y"] += player["speed"]

    # Střelba
    if keys[pygame.K_SPACE] and current_time - player["last_shot"] >= player["fire_rate"]:
        bullets.append({"x": player["x"] + player["width"], "y": player["y"] + player["height"] // 2, "speed": 7})
        player["last_shot"] = current_time

    # Pohyb střel
    for bullet in bullets[:]:
        bullet["x"] += bullet["speed"]
        if bullet["x"] > WIDTH:
            bullets.remove(bullet)

    # Spawn zombíků
    if wave["zombies_left"] > 0 and random.randint(1, 40) == 1:
        zombies.append({"x": WIDTH, "y": random.randint(150, HEIGHT - 50), "speed": zombie_speed * wave["speed_multiplier"]})
        wave["zombies_left"] -= 1

    # Pohyb zombíků
    for zombie in zombies[:]:
        zombie["x"] -= zombie["speed"]
        if zombie["x"] < 70:
            player["lives"] -= 1
            zombies.remove(zombie)

    # Kolize střel a zombíků
    for bullet in bullets[:]:
        for zombie in zombies[:]:
            if zombie["x"] < bullet["x"] < zombie["x"] + 40 and zombie["y"] < bullet["y"] < zombie["y"] + 50:
                bullets.remove(bullet)
                zombies.remove(zombie)
                store["money"] += 1
                break

    # Zobrazení hráče
    pygame.draw.rect(screen, RED, (player["x"], player["y"], player["width"], player["height"]))

    # Zobrazení střel
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet["x"], bullet["y"], 10, 5))

    # Zobrazení zombíků
    for zombie in zombies:
        pygame.draw.rect(screen, GREEN, (zombie["x"], zombie["y"], 40, 50))

    # Zobrazení textu (vlna, životy, peníze)
    font = pygame.font.Font(None, 36)
    wave_text = font.render(f"Vlna: {wave['current']}", True, WHITE)
    money_text = font.render(f"Měna: {store['money']}", True, WHITE)
    lives_text = font.render(f"Životy: {player['lives']}", True, WHITE)
    
    screen.blit(wave_text, (10, 10))
    screen.blit(money_text, (10, 50))
    screen.blit(lives_text, (WIDTH - 150, 10))

    # Konec vlny
    if wave["zombies_left"] <= 0 and len(zombies) == 0:
        wave["current"] += 1
        wave["zombies_left"] = 50
        wave["speed_multiplier"] *= 1.05  # Zrychlení zombíků o 5 %

        # Nabídka po vlně
        waiting = True
        while waiting:
            screen.fill((0, 0, 0))
            message = font.render("1 = obchod, 2 = pokračovat, 3 = ukončit", True, WHITE)
            screen.blit(message, (WIDTH // 2 - 200, HEIGHT // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:  # Obchod
                        if store["money"] >= store["weapon_upgrade_cost"]:
                            store["money"] -= store["weapon_upgrade_cost"]
                            player["fire_rate"] = max(100, player["fire_rate"] - store["fire_rate_upgrade"])
                        waiting = False
                    if event.key == pygame.K_2:  # Pokračovat
                        waiting = False
                    if event.key == pygame.K_3:  # Ukončit hru
                        running = False
                        waiting = False

    # Aktualizace obrazovky
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
 