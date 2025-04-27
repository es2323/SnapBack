import pygame
import random
import time
import requests

# --- Initial Setup ---
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

# --- Instructions Message ---
screen.fill(bg_color)
msg = font.render("Click when you see the circle...", True, text_color)
screen.blit(msg, (120, 150))
pygame.display.flip()

pygame.time.set_timer(pygame.USEREVENT, delay)

# --- Main Game Loop ---
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
            reaction_time = round((time.time() - start_time) * 1000)  # Reaction time in milliseconds
            screen.fill(bg_color)
            result = font.render(f"Reaction Time: {reaction_time} ms", True, text_color)
            screen.blit(result, (150, 180))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

pygame.quit()

# --- Send Reaction Time to Flask API ---

if reaction_time is not None:
    payload = {
        "user_email": "test@example.com",   # Replace with dynamic email if needed
        "reaction_time": reaction_time
    }

    try:
        response = requests.post("http://127.0.0.1:5000/submit_score", json=payload)

        if response.status_code == 200:
            print("✅ Score submitted successfully!")
        else:
            print(f"❌ Failed to submit score. Status Code: {response.status_code}")

    except Exception as e:
        print(f"❗ Error sending data to server: {e}")
else:
    print("❗ No valid reaction time recorded.")
