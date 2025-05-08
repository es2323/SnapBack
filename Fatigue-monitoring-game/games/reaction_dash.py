# games/reaction_game.py
# pyright: reportGeneralTypeIssues=false
import pygame
import random
import time
import sqlite3
import requests
import webbrowser

def run_game(user_email="test@example.com"):
    pygame.init()

    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Reaction Time Test")

    font = pygame.font.SysFont(None, 36)
    bg_color = (240, 240, 240)
    text_color = (30, 30, 30)

    clock = pygame.time.Clock()

    NUM_TRIALS = 10
    reaction_times = []
    trial = 1
    running = True

    while running and trial <= NUM_TRIALS:
        circle_pos = (random.randint(100, 500), random.randint(100, 300))
        circle_shown = False
        reaction_time = None
        waiting = True

        # Shorter delay for later trials (increasing difficulty)
        delay = random.randint(2000 - (trial * 100), 5000 - (trial * 150))
        delay = max(1000, delay)  # Set a lower bound

        # Instruction screen
        screen.fill(bg_color)
        msg = font.render(f"Trial {trial}: Click when you see the circle...", True, text_color)
        screen.blit(msg, (80, 150))
        pygame.display.flip()

        SHOW_CIRCLE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SHOW_CIRCLE_EVENT, delay)

        trial_running = True
        start_time = 0

        while trial_running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    trial_running = False

                elif event.type == SHOW_CIRCLE_EVENT and waiting:
                    screen.fill(bg_color)
                    pygame.draw.circle(screen, (100, 200, 255), circle_pos, 30)
                    pygame.display.flip()
                    start_time = time.time()
                    circle_shown = True
                    waiting = False

                elif event.type == pygame.MOUSEBUTTONDOWN and circle_shown:
                    reaction_time = round((time.time() - start_time) * 1000)
                    reaction_times.append(reaction_time)

                    # Display reaction time briefly
                    screen.fill(bg_color)
                    result = font.render(f"Reaction Time: {reaction_time} ms", True, text_color)
                    screen.blit(result, (150, 180))
                    pygame.display.flip()
                    pygame.time.delay(1000)

                    trial_running = False
                    trial += 1

    pygame.quit()

    # Compute average fatigue score
    if reaction_times:
        avg_reaction_time = round(sum(reaction_times) / len(reaction_times))
        fatigue_scores = [max(0, 100 - rt // 10) for rt in reaction_times]
        avg_fatigue_score = round(sum(fatigue_scores) / len(fatigue_scores))
        accuracy = 100 - (len(reaction_times) / NUM_TRIALS * 10)  # Simplified accuracy metric


                # After computing fatigue_score and reaction_time
        payload = {
        "user_email": user_email,
        "game_type": "reaction",
        "reaction_time": avg_reaction_time,
        "fatigue_score": avg_fatigue_score,
        "accuracy": accuracy,
        "errors": NUM_TRIALS - len(reaction_times),
        "completion_time": sum(reaction_times) / 1000  # Convert to seconds
        }

    try:
        response = requests.post("http://127.0.0.1:5000/submit_score", json=payload)
        if response.status_code == 200:
            print("Score submitted successfully")
            webbrowser.open("http://127.0.0.1:5000/results")
        else:
            print("Failed to submit score:", response.text)
    except Exception as e:
        print("API Error:", str(e))
        # Fallback to direct DB save if API fails
        # Save to database
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO game_sessions 
            (user_email, game_type, fatigue_score, reaction_time, accuracy, errors, completion_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_email, "reaction", avg_fatigue_score, avg_reaction_time, accuracy, 
             NUM_TRIALS - len(reaction_times), sum(reaction_times)/1000)           
        )
        conn.commit()
        conn.close()        
        webbrowser.open("http://127.0.0.1:5000/results")

