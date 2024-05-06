import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake class
class Snake:
    def __init__(self):
        self.body = [(200, 200), (210, 200), (220, 200)]
        self.direction = (GRID_SIZE, 0)

    def move(self, grow=False):
        head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, head)
        if not grow:
            self.body.pop()

    def grow(self):
        tail = (self.body[-1][0] + self.direction[0], self.body[-1][1] + self.direction[1])
        self.body.append(tail)

    def change_direction(self, direction):
        if (direction[0] != -self.direction[0]) or (direction[1] != -self.direction[1]):
            self.direction = direction

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(win, GREEN, (*segment, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(win, BLACK, (*segment, GRID_SIZE, GRID_SIZE), 1)

# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, (WIDTH-GRID_SIZE)//GRID_SIZE) * GRID_SIZE,
                         random.randint(0, (HEIGHT-GRID_SIZE)//GRID_SIZE) * GRID_SIZE)

    def respawn(self):
        self.position = (random.randint(0, (WIDTH-GRID_SIZE)//GRID_SIZE) * GRID_SIZE,
                         random.randint(0, (HEIGHT-GRID_SIZE)//GRID_SIZE) * GRID_SIZE)

    def draw(self):
        pygame.draw.rect(win, RED, (*self.position, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(win, BLACK, (*self.position, GRID_SIZE, GRID_SIZE), 1)

# Main game loop
def main():
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()

    score = 0

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction((-GRID_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((GRID_SIZE, 0))
                elif event.key == pygame.K_UP:
                    snake.change_direction((0, -GRID_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, GRID_SIZE))

        if snake.body[0] == food.position:
            snake.grow()
            food.respawn()
            score += 10
        else:
            snake.move()

        if (snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or
            snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT or
            snake.body[0] in snake.body[1:]):
            run = False

        win.fill(WHITE)
        snake.draw()
        food.draw()
        
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {score}', True, BLUE)
        win.blit(text, (10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
