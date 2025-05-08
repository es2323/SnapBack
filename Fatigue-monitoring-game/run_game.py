import sys
import traceback
# pyright: reportGeneralTypeIssues=false
import pygame


try:
    import pygame
    from games import reaction_dash, focus_game  # Add more as needed
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please install the required packages:")
    print("1. Activate your virtual environment")
    print("2. Run: python -m pip install pygame")
    sys.exit(1)

def run_game(game_name, user_email):
    try:
        pygame.init()
        if game_name == "reaction":
            reaction_dash.run_game(user_email)
        elif game_name == "focus":
            focus_game.run_game(user_email)
        else:
            print(f"Unknown game: {game_name}")
    except Exception as e:
        print(f"Game Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_game.py <game_name> <user_email>")
    else:
        run_game(sys.argv[1], sys.argv[2])
        user_email = sys.argv[2]
        run_game(game_name, user_email)