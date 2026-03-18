#!/usr/bin/env python3
"""Debug script to test tower selector"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Capture output
import io
from contextlib import redirect_stdout, redirect_stderr

import pygame
from settings import SZELESSEG, MAGASSAG
from game import Game

# Start the game and let user click
print("Game started. Click on TOWERS ON button, then click on a tower to select image.")
print("Then click on one of the 3 images that appear.")

game = Game()

# Run for a limited time and capture output
output = io.StringIO()
for i in range(600):  # Run for 10 seconds at 60 FPS
    game.esemenyek()
    game.update()
    game.rajzol()
    game.ora.tick(60)

print("Debug test completed.")
