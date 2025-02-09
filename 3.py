import pygame

# Inicializace pygame
pygame.init()

# Nastavení herního okna
settings = {
    "width": 800,
    "height": 600,
    "title": "Vesmírná střílečka",
    "colors": {
        "green": (0, 255, 0),
        "black": (0, 0, 0),
        "red": (255, 0, 0)
    },
    "player": {
        "size": 50,
        "x": 50,
        "y": 300,
        "speed": 5
    },
    "zombie": {
        "x": 750,
        "y": 300,
        "speed": 2
    },
    "lives": 3,
    "boundary_x": 0  # Hranice, při jejímž překročení zombík ubere život
}

screen = pygame.display.set_mode((settings["width"], settings["height"]))
pygame.display.set_caption(settings["title"])

# Herní smyčka
running = True
while running:
    screen.fill(settings["colors"]["black"])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Pohyb hráče (chyba: hráč může vyjet mimo obrazovku)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        settings["player"]["y"] -= settings["player"]["speed"]
    if keys[pygame.K_DOWN]:
        settings["player"]["y"] += settings["player"]["speed"]
    
    # Pohyb zombíka
    settings["zombie"]["x"] -= settings["zombie"]["speed"]
    
    # Kontrola, zda zombík překročil hranici
    if settings["zombie"]["x"] <= settings["boundary_x"]:
        settings["lives"] -= 1
        settings["zombie"]["x"] = 750  # Reset pozice zombíka
        print(f"Zombík překročil hranici! Zbývající životy: {settings['lives']}")
    
    # Vykreslení hráče
    pygame.draw.rect(screen, settings["colors"]["green"], (settings["player"]["x"], settings["player"]["y"], settings["player"]["size"], settings["player"]["size"]))
    
    # Vykreslení zombíka
    pygame.draw.rect(screen, settings["colors"]["red"], (settings["zombie"]["x"], settings["zombie"]["y"], 40, 40))
    
    pygame.display.flip()
    
pygame.quit()