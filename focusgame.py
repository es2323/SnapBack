import pygame
import random
import time

# Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Focus Game - Dynamic Difficulty")

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

def draw_words(words, positions, moving=False):
    screen.fill((255, 255, 255))
    for idx, word in enumerate(words):
        x, y = positions[idx]
        if moving:
            x += random.randint(-5, 5)  
        text = font.render(word, True, (0, 0, 0))
        screen.blit(text, (x, y))
    pygame.display.flip()

def generate_words(level):
    base_words = ["Cat", "Dog", "Rat", "Bat", "Cow", "Pig"]
    common_word = random.choice(base_words)
    diff_word = random.choice([w for w in base_words if w != common_word])

    num_words = 4 + min(level, 2)  
    words = [common_word for _ in range(num_words)]
    odd_index = random.randint(0, num_words - 1)
    words[odd_index] = diff_word


    spacing = 600 // (num_words + 1)
    positions = [(spacing * (i + 1) - 20, 180) for i in range(num_words)]
    return words, odd_index, positions

def main():
    running = True
    level = 1

    while running and level <= 6:
        words, odd_index, positions = generate_words(level)
        correct = False
        clicked = False

        start_time = time.time()

        while not clicked:
            move_words = True if level >= 4 else False
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
                            if idx == odd_index:
                                correct = True
                            else:
                                correct = False

            if level >= 5:
                
                elapsed = time.time() - start_time
                if elapsed > 5:
                    clicked = True
                    correct = False

            clock.tick(30)

        
        screen.fill((255, 255, 255))
        if correct:
            text = font.render(f"Correct! Level {level} passed.", True, (0, 200, 0))
            level += 1
        else:
            text = font.render(f"Wrong! Try Again from Level 1.", True, (200, 0, 0))
            level = 1
        screen.blit(text, (120, 180))
        pygame.display.flip()
        time.sleep(2)

    if level > 6:
        screen.fill((0, 255, 0))
        text = font.render("You beat all 6 levels! Great focus!", True, (0, 0, 0))
        screen.blit(text, (80, 180))
        pygame.display.flip()
        time.sleep(3)

    pygame.quit()

if __name__ == "__main__":
    main()
