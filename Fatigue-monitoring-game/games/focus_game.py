import pygame
import random
import time
import sqlite3
from datetime import datetime
import requests
import webbrowser

# Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Focus Game - SnapBack")

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# SnapBack Theme Colors
THEME_BG = (0, 105, 111)
TEXT_COLOR = (0, 0, 0)
SUCCESS_COLOR = (0, 200, 160)
FAIL_COLOR = (200, 0, 0)
FINAL_BG = (0, 150, 136)

def draw_words(words, positions, moving=False):
    screen.fill(THEME_BG)
    for idx, word in enumerate(words):
        x, y = positions[idx]
        if moving:
            x += random.randint(-5, 5)
        text = font.render(word, True, TEXT_COLOR)
        screen.blit(text, (x, y))
    pygame.display.flip()

def generate_words(level):
    base_words = ["Cat", "Dog", "Rat", "Bat", "Cow", "Pig", "Fox", "Hen", "Ant", "Bee"]
    common_word = random.choice(base_words)
    diff_word = random.choice([w for w in base_words if w != common_word])

    num_words = 4 + min(level, 6)
    words = [common_word for _ in range(num_words)]
    odd_index = random.randint(0, num_words - 1)
    words[odd_index] = diff_word

    spacing = 600 // (num_words + 1)
    positions = [(spacing * (i + 1) - 20, 180) for i in range(num_words)]
    return words, odd_index, positions

def save_score_to_db(user_email, score):
    conn = sqlite3.connect("main.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO game_sessions (user_email, fatigue_score, game_type, timestamp) VALUES (?, ?, ?, ?)",
        (user_email, score, "focus", datetime.now())
    )
    conn.commit()
    conn.close()

def show_instructions():
    screen.fill(THEME_BG)
    instructions = [
        "🧠 Focus Game - Instructions 🧠",
        "",
        "🔎 One word is different from the others.",
        "👆 Click the odd word out as quickly as you can.",
        "",
        "⚠️ The game gets harder with each level!",
        "",
        "Click anywhere to start..."
    ]
    y = 60
    for line in instructions:
        rendered = font.render(line, True, (255, 255, 255))
        screen.blit(rendered, (50, y))
        y += 40
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def run_game(user_email="test@example.com"):
    show_instructions()
    running = True
    level = 1
    correct_answers = 0

    while running and level <= 10:
        words, odd_index, positions = generate_words(level)
        correct = False
        clicked = False
        start_time = time.time()

        while not clicked:
            move_words = level >= 4
            draw_words(words, positions, moving=move_words)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    clicked = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for idx, (x, y) in enumerate(positions):
                        rect = pygame.Rect(x, y, 60, 40)
                        if rect.collidepoint(pos):
                            clicked = True
                            correct = (idx == odd_index)

            if level >= 5 and (time.time() - start_time > 5):
                clicked = True
                correct = False

            clock.tick(30)

        screen.fill(THEME_BG)
        if correct:
            text = font.render(f"Correct! Level {level} passed.", True, SUCCESS_COLOR)
            correct_answers += 1
            level += 1
        else:
            text = font.render(f"Wrong! Try Again from Level 1.", True, FAIL_COLOR)
            level = 1
            correct_answers = 0
        screen.blit(text, (100, 180))
        pygame.display.flip()
        time.sleep(2)

    # Game completed
    screen.fill(FINAL_BG)
    text = font.render("You beat all 10 levels! Amazing focus!", True, TEXT_COLOR)
    screen.blit(text, (60, 180))
    pygame.display.flip()
    time.sleep(3)

    # Final score and save
    fatigue_score = correct_answers * 10  # Max 100
    save_score_to_db(user_email, fatigue_score)

    # Submit to Flask backend
    payload = {
        "user_email": user_email,
        "game_type": "focus",
        "reaction_time": 1000,  # placeholder
    }
    try:
        response = requests.post("http://127.0.0.1:5000/submit_score", json=payload)
        print("Submitted:", response.status_code)
    except Exception as e:
        print("Failed to send score:", str(e))

    pygame.quit()

webbrowser.open("http://127.0.0.1:5000/results")

if __name__ == "__main__":
    run_game()
