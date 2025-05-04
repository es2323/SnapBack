# games/reaction_game.py
import pygame
import random
import time
import sqlite3
import sys

def run_game(user_email="test@example.com"):
    pygame.init()

    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Reaction Time Test")

    font = pygame.font.SysFont(None, 36)
    bg_color = (240, 240, 240)
    text_color = (30, 30, 30)

    circle_pos = (random.randint(100, 500), random.randint(100, 300))
    circle_shown = False
    reaction_time = None
    start_time = 0

    running = True
    waiting = True
    delay = random.randint(2000, 5000)

    screen.fill(bg_color)
    msg = font.render("Click when you see the circle...", True, text_color)
    screen.blit(msg, (120, 150))
    pygame.display.flip()
    SHOW_CIRCLE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SHOW_CIRCLE_EVENT, delay)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.USEREVENT and waiting:
                screen.fill(bg_color)
                pygame.draw.circle(screen, (100, 200, 255), circle_pos, 30)
                pygame.display.flip()
                start_time = time.time()
                circle_shown = True
                waiting = False

            elif event.type == pygame.MOUSEBUTTONDOWN and circle_shown:
                reaction_time = round((time.time() - start_time) * 1000)
                screen.fill(bg_color)
                result = font.render(f"Reaction Time: {reaction_time} ms", True, text_color)
                screen.blit(result, (150, 180))
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False

    pygame.quit()

    fatigue_score = max(0, 100 - reaction_time // 10)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO game_sessions (user_email, fatigue_score) VALUES (?, ?)", 
                   (user_email, fatigue_score))  
    conn.commit()
    conn.close()
