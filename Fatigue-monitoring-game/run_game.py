import sys
import pygame
from games import reaction_dash # Add more as needed

pygame.init()

def run_game(game_name, user_email):
    if game_name == "reaction":
        reaction_dash.run_game(user_email)
    elif game_name == "memory":
        memory_game.run_game(user_email)
    else:
        print(f"Unknown game: {game_name}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_game.py <game_name> <user_email>")
    else:
        game_name = sys.argv[1]
        user_email = sys.argv[2]
        run_game(game_name, user_email)
