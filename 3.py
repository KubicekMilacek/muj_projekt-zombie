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

# Načtení obrázku obchodu
store_image = pygame.image.load("store.png")

# Načtení obrázku bosse (žirafy)
giraffe_boss_image = pygame.image.load("giraffe_boss.png")

# Barvy
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 100, 0)
PURPLE = (128, 0, 128)  # Fialová barva
BLACK = (0, 0, 0)  # Černá barva pro text

# Hráč
player = {
    "x": 50,
    "y": HEIGHT // 2 - 25,
    "width": 40,
    "height": 50,
    "speed": 5,
    "lives": 10,
    "fire_rate": 500,  # 0.5 sekundy cooldown
    "last_shot": 0
}

# Střely
bullets = []

# Zombíci
zombies = []
zombie_speed = 2 * (2 / 3)  # Zpomalení zombíků o třetinu

# Vlna
wave = {
    "current": 1,
    "zombies_left": 50,
    "speed_multiplier": 1.0
}

# Boss Fight
boss = None

# Obchod
store = {
    "weapon_upgrade_cost": 10,
    "money": 0,
    "fire_rate_upgrade_cost": 15,  # ✅ Cena za zrychlení střelby
    "penetration_upgrade_cost": 20,  # ✅ Cena za penetraci kulek
    "second_weapon_cost": 30,  # ✅ Cena za druhou zbraň
    "penetration_level": 0,
    "second_weapon": False
}

# Časovač
clock = pygame.time.Clock()

# Funkce pro kontrolu, jestli je pozice volná
def is_position_free(x, y):
    for zombie in zombies:
        if abs(zombie["x"] - x) < 40 and abs(zombie["y"] - y) < 50:
            return False
    return True

# Funkce pro zobrazení obchodu
def show_store():
    screen.blit(store_image, (0, 0))
    close_button = pygame.Rect(WIDTH - 40, 10, 30, 30)  # Červený křížek pro zavření
    pygame.draw.rect(screen, RED, close_button)  # Kreslení křížku

    # Zobrazit text
    font = pygame.font.Font(None, 36)
    message = font.render("Zavřít obchod (klikněte na křížek)", True, WHITE)
    screen.blit(message, (WIDTH // 2 - 150, HEIGHT // 2))

    # Zobrazení měny
    money_text = font.render(f"Měna: {int(store['money'])}", True, WHITE)  # Zaokrouhlení měny na celé číslo
    screen.blit(money_text, (WIDTH // 2 - 50, HEIGHT // 2 - 40))

    # Vytvoření tabulky s upgrady
    upgrade_table_rect = pygame.Rect(100, HEIGHT // 2 + 50, 400, 200)
    pygame.draw.rect(screen, WHITE, upgrade_table_rect)
    pygame.draw.rect(screen, BLACK, upgrade_table_rect, 3)  # Černé ohraničení tabulky

    # Popisky pro upgrady
    upgrades = [
        ("Zrychlení střelby", store["fire_rate_upgrade_cost"], "Střelba bude rychlejší o 10%."),
        ("Penetrace kulek", store["penetration_level"], "Kulka projde až dvěma zombíky."),
        ("Druhá zbraň", store["second_weapon"], "Budeš střílet dva náboje nad sebou.")
    ]
    
    # Zobrazit upgradey
    y_offset = 70
    for upgrade_name, upgrade_level, description in upgrades:
        text = font.render(f"{upgrade_name}: {upgrade_level} - {description}", True, BLACK)
        screen.blit(text, (upgrade_table_rect.x + 10, upgrade_table_rect.y + y_offset))
        y_offset += 40

    # Tlačítka pro nákup
    buy_fire_rate_button = pygame.Rect(600, 100, 150, 50)
    pygame.draw.rect(screen, GREEN, buy_fire_rate_button)
    buy_fire_rate_text = font.render(f"Koupit zrychlení ({int(store['fire_rate_upgrade_cost'])})", True, WHITE)  # Zaokrouhlení
    screen.blit(buy_fire_rate_text, (buy_fire_rate_button.x + 10, buy_fire_rate_button.y + 10))

    buy_penetration_button = pygame.Rect(600, 170, 150, 50)
    pygame.draw.rect(screen, GREEN, buy_penetration_button)
    buy_penetration_text = font.render(f"Koupit penetraci ({int(store['penetration_upgrade_cost'])})", True, WHITE)  # Zaokrouhlení
    screen.blit(buy_penetration_text, (buy_penetration_button.x + 10, buy_penetration_button.y + 10))

    buy_second_weapon_button = pygame.Rect(600, 240, 150, 50)
    pygame.draw.rect(screen, GREEN, buy_second_weapon_button)
    buy_second_weapon_text = font.render(f"Koupit druhou zbraň ({int(store['second_weapon_cost'])})", True, WHITE)  # Zaokrouhlení
    screen.blit(buy_second_weapon_text, (buy_second_weapon_button.x + 10, buy_second_weapon_button.y + 10))

    pygame.display.flip()

    return close_button, buy_fire_rate_button, buy_penetration_button, buy_second_weapon_button

# Funkce pro začátek boss fightu
def start_boss_fight():
    global boss
    boss = {
        "x": WIDTH // 2,
        "y": HEIGHT // 4,
        "width": 100,
        "height": 150,
        "speed": 3,
        "health": 50
    }

# Hlavní smyčka
running = True
in_store = False  # Zda je hráč v obchodě
while running:
    screen.blit(background, (0, 0))
    current_time = pygame.time.get_ticks()

    # Události
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if in_store:
        # Pokud je hráč v obchodě, zobraz obchod
        close_button, buy_fire_rate_button, buy_penetration_button, buy_second_weapon_button = show_store()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    in_store = False  # Zavření obchodu
                elif buy_fire_rate_button.collidepoint(event.pos):
                    if store["money"] >= store["fire_rate_upgrade_cost"]:
                        store["money"] -= store["fire_rate_upgrade_cost"]
                        store["fire_rate_upgrade_cost"] *= 1.2  # Zvýšení ceny o 20%
                        player["fire_rate"] = int(player["fire_rate"] * 0.9)  # Zrychlení střelby o 10%
                elif buy_penetration_button.collidepoint(event.pos):
                    if store["money"] >= store["penetration_upgrade_cost"]:
                        store["money"] -= store["penetration_upgrade_cost"]
                        store["penetration_upgrade_cost"] *= 1.3  # Zvýšení ceny o 30%
                        store["penetration_level"] += 1
                elif buy_second_weapon_button.collidepoint(event.pos):
                    if store["money"] >= store["second_weapon_cost"]:
                        store["money"] -= store["second_weapon_cost"]
                        store["second_weapon"] = True
            if event.type == pygame.QUIT:
                running = False
                in_store = False

    else:
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

        # Spawn zombíků (5 fialových zombíků na vlnu)
        if wave["zombies_left"] > 0 and random.randint(1, 80) == 1:
            zombie_x = WIDTH
            zombie_y = random.randint(150, HEIGHT - 50)

            # Určíme, zda tento zombík bude fialový (5 na vlnu)
            is_purple = False
            if wave["zombies_left"] > 45 and random.randint(1, 10) <= 5:  # 5 fialových na 50 zombíků
                is_purple = True

            if is_position_free(zombie_x, zombie_y):
                zombies.append({
                    "x": zombie_x,
                    "y": zombie_y,
                    "speed": zombie_speed * wave["speed_multiplier"],
                    "is_purple": is_purple
                })
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
                    
                    # Výplata peněz
                    if zombie["is_purple"]:
                        store["money"] += 8  # Fialoví zombíci dávají více peněz
                    else:
                        store["money"] += 1  # Běžní zombíci dávají 1 peníze
                    store["money"] = round(store["money"])  # Zaokrouhlení měny na celé číslo
                    break

        # Zobrazení hráče
        pygame.draw.rect(screen, RED, (player["x"], player["y"], player["width"], player["height"]))

        # Zobrazení střel
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, (bullet["x"], bullet["y"], 10, 5))

        # Zobrazení zombíků
        for zombie in zombies:
            color = PURPLE if zombie["is_purple"] else GREEN
            pygame.draw.rect(screen, color, (zombie["x"], zombie["y"], 40, 50))

        # Zobrazení textu (životy, měna, vlna a zbývající zombíci)
        font = pygame.font.Font(None, 36)

        # Životy
        lives_text = font.render(f"Životy: {player['lives']}", True, BLACK)
        screen.blit(lives_text, (10, 10))

        # Měna
        money_text = font.render(f"Měna: {int(store['money'])}", True, BLACK)  # Zaokrouhlení
        screen.blit(money_text, (150, 10))

        # Zbývající zombíci
        remaining_zombies_text = font.render(f"Zombíci: {wave['zombies_left']}", True, BLACK)
        screen.blit(remaining_zombies_text, (WIDTH - 300, 10))

        # Vlna
        wave_text = font.render(f"Vlna: {wave['current']}", True, BLACK)
        screen.blit(wave_text, (WIDTH - 150, 10))

        # Konec vlny
        if wave["zombies_left"] <= 0 and len(zombies) == 0:
            wave["current"] += 1
            wave["zombies_left"] = 50
            wave["speed_multiplier"] *= 1.05  # Zrychlení zombíků o 5 %

            # Každých 5 levelů boss fight
            if wave["current"] % 5 == 0:
                start_boss_fight()

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
                            in_store = True
                            waiting = False
                        elif event.key == pygame.K_2:  # Pokračovat
                            waiting = False
                        elif event.key == pygame.K_3:  # Ukončit
                            running = False
                            waiting = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
