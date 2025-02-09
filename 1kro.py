import pygame


pygame.init()


settings = {
    "width": 800,
    "height": 600,
    "title": "Vesmírná střílečka",
    "colors": {
        "green": (0, 255, 0),
        "black": (0, 0, 0)
    },
    "player": {
        "size": 50,
        "x": 50,
        "y": 300,
        "speed": 5
    }
}

screen = pygame.display.set_mode((settings["width"], settings["height"]))
pygame.display.set_caption(settings["title"])


running = True
while running:
    screen.fill(settings["colors"]["black"])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        settings["player"]["y"] -= settings["player"]["speed"]
    if keys[pygame.K_DOWN]:
        settings["player"]["y"] += settings["player"]["speed"]
    
    pygame.draw.rect(screen, settings["colors"]["green"], (settings["player"]["x"], settings["player"]["y"], settings["player"]["size"], settings["player"]["size"]))
    
    pygame.display.flip()
    
pygame.quit()
