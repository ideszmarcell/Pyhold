import pygame
import sys

pygame.init()
pygame.display.set_mode((1, 1))  # Dummy display

# Load the image
img = pygame.image.load("assets/images/wall.png").convert_alpha()

# Assume background is white (255,255,255), make it transparent
for x in range(img.get_width()):
    for y in range(img.get_height()):
        color = img.get_at((x, y))
        if color.r > 240 and color.g > 240 and color.b > 240:  # Near white
            img.set_at((x, y), (0, 0, 0, 0))  # Transparent

# Save the image
pygame.image.save(img, "assets/images/wall_no_bg.png")

print("Background removed and saved as wall_no_bg.png")
