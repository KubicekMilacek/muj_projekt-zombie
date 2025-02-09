import pygame

pygame.init()

settings = {
    "width": 800,
    "height": 600,
    "title": "Vesmírná střílečka",
    "colors": {
        "green": (0, 255, 0),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "blue": (0, 0, 255)
    },
    "player": {
        "size": 50,
        "x": 50,
        "y": 300,
        "speed": 5
    },
    "bullets": [],
    "bullet_speed": 10
}

screen = pygame.display.set_mode((settings["width"], settings["height"]))
pygame.display.set_caption(settings["title"])

running = True
while running:
    screen.fill(settings["colors"]["black"])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                settings["bullets"].append({
                    "x": settings["player"]["x"] + settings["player"]["size"],
                    "y": settings["player"]["y"] + settings["player"]["size"] // 2
                })
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        settings["player"]["y"] -= settings["player"]["speed"]
    if keys[pygame.K_DOWN]:
        settings["player"]["y"] += settings["player"]["speed"]
    
    for bullet in settings["bullets"]:
        bullet["x"] += settings["bullet_speed"]
    
    settings["bullets"] = [bullet for bullet in settings["bullets"] if bullet["x"] < settings["width"]]
    
    pygame.draw.rect(screen, settings["colors"]["green"], (settings["player"]["x"], settings["player"]["y"], settings["player"]["size"], settings["player"]["size"]))
    
    for bullet in settings["bullets"]:
        pygame.draw.rect(screen, settings["colors"]["blue"], (bullet["x"], bullet["y"], 10, 5))
    
    pygame.display.flip()
    
pygame.quit()
