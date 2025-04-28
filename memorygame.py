import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Setup window
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Memory Game - Basic")


font = pygame.font.SysFont(None, 36)
colors = ["RED", "GREEN", "BLUE"]
rgb_colors = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255)
}


def draw_text(text, y):
    txt = font.render(text, True, (0, 0, 0))
    screen.blit(txt, (150, y))


def show_sequence(seq):
    for color in seq:
        screen.fill(rgb_colors[color])
        pygame.display.flip()
        time.sleep(0.8)
        screen.fill((255, 255, 255))
        pygame.display.flip()
        time.sleep(0.5)


def main():
    running = True
    sequence = [random.choice(colors) for _ in range(3)]
    user_sequence = []

    screen.fill((255, 255, 255))
    draw_text("Memorize the colors!", 150)
    pygame.display.flip()
    time.sleep(2)

    show_sequence(sequence)

    
    red_button = pygame.Rect(50, 300, 100, 50)
    green_button = pygame.Rect(200, 300, 100, 50)
    blue_button = pygame.Rect(350, 300, 100, 50)

    while running:
        screen.fill((255, 255, 255))
        draw_text("Click the colors in order!", 100)
        pygame.draw.rect(screen, (255, 0, 0), red_button)
        pygame.draw.rect(screen, (0, 255, 0), green_button)
        pygame.draw.rect(screen, (0, 0, 255), blue_button)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if red_button.collidepoint(pos):
                    user_sequence.append("RED")
                elif green_button.collidepoint(pos):
                    user_sequence.append("GREEN")
                elif blue_button.collidepoint(pos):
                    user_sequence.append("BLUE")

                if len(user_sequence) == len(sequence):
                    if user_sequence == sequence:
                        screen.fill((0, 255, 0))
                        draw_text("Correct!", 180)
                    else:
                        screen.fill((255, 0, 0))
                        draw_text("Wrong! Try Again", 180)
                    pygame.display.flip()
                    time.sleep(2)
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main()

