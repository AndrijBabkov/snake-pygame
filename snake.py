import pygame
import random
import sys

# --- config ---
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 10

# colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_img = pygame.image.load("assets/background.png").convert()
background_img = pygame.transform.scale(background_img, (CELL_SIZE, CELL_SIZE))
logo_img = pygame.image.load("assets/logo.png").convert_alpha()
logo_rect = logo_img.get_rect(center=(WIDTH // 2, HEIGHT // 3))

pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
snake_img = pygame.image.load("assets/snake.png").convert_alpha()
food_img = pygame.image.load("assets/food.png").convert_alpha()


food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))

def tint_image(image, color):
    tinted = image.copy()
    tint = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    tint.fill(color)
    tinted.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return tinted
snake_img = pygame.transform.scale(snake_img, (CELL_SIZE, CELL_SIZE))
snake_img = tint_image(snake_img, (200, 120, 0))  # orange/yellow



def random_position():
    x = random.randint(0, GRID_WIDTH - 1)
    y = random.randint(0, GRID_HEIGHT - 1)
    return x, y





def main():

    font = pygame.font.SysFont(None, 28)
    STATE_MENU = 0
    STATE_PLAYING = 1
    STATE_GAME_OVER = 2

    state = STATE_MENU

    while True:
        # -------- MENU --------
        while state == STATE_MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    state = STATE_PLAYING

            for x in range(GRID_WIDTH):
                for y in range(GRID_HEIGHT):
                    screen.blit(background_img, (x * CELL_SIZE, y * CELL_SIZE))

            screen.blit(logo_img, logo_rect)

            title = font.render("Press SPACE to Start", True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

            pygame.display.flip()
            clock.tick(30)

        # -------- INIT GAME STATE (ONCE) --------
        snake = [(15, 10), (14, 10), (13, 10)]
        direction = (1, 0)
        food = random_position()
        score = 0
        game_over = False

        while not game_over:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        direction = (1, 0)

            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            if (
                new_head[0] < 0 or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
                or new_head in snake
            ):
                game_over = True
                continue

            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                food = random_position()
            else:
                snake.pop()

            for x in range(GRID_WIDTH):
                for y in range(GRID_HEIGHT):
                    screen.blit(
                        background_img,
                        (x * CELL_SIZE, y * CELL_SIZE)
                    )
            for segment in snake:
                screen.blit(
                    snake_img,
                    (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE)
                )

            screen.blit(
                food_img,
                (food[0] * CELL_SIZE, food[1] * CELL_SIZE)
            )

            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()

        # --- game over screen ---
        text = font.render("Game Over - Press R to Restart", True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    state = STATE_MENU
                    waiting = False

            screen.fill(BLACK)
            screen.blit(text, rect)
            pygame.display.flip()



if __name__ == "__main__":
    main()
