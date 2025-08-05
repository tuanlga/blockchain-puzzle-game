
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blockchain Puzzle Game")

# Clock
clock = pygame.time.Clock()

# Grid
def create_grid():
    return [[BLACK for _ in range(COLS)] for _ in range(ROWS)]

# Draw grid
def draw_grid(grid):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Piece class
class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def valid_position(self, grid, dx=0, dy=0):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x] != BLACK):
                        return False
        return True

    def place(self, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[self.y + y][self.x + x] = self.color

# Clear full rows
def clear_rows(grid):
    new_grid = [row for row in grid if BLACK in row]
    cleared = ROWS - len(new_grid)
    for _ in range(cleared):
        new_grid.insert(0, [BLACK for _ in range(COLS)])
    return new_grid, cleared

# Main game loop
def main():
    grid = create_grid()
    piece = Piece()
    fall_time = 0
    score = 0
    running = True

    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time > 500:
            fall_time = 0
            if piece.valid_position(grid, dy=1):
                piece.y += 1
            else:
                piece.place(grid)
                grid, cleared = clear_rows(grid)
                score += cleared * 10
                piece = Piece()
                if not piece.valid_position(grid):
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and piece.valid_position(grid, dx=-1):
                    piece.x -= 1
                elif event.key == pygame.K_RIGHT and piece.valid_position(grid, dx=1):
                    piece.x += 1
                elif event.key == pygame.K_DOWN and piece.valid_position(grid, dy=1):
                    piece.y += 1
                elif event.key == pygame.K_UP:
                    piece.rotate()
                    if not piece.valid_position(grid):
                        piece.rotate()
                        piece.rotate()
                        piece.rotate()

        draw_grid(grid)
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, piece.color, ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        pygame.display.update()

    pygame.quit()
    print(f"Game Over! Your score: {score}")

if __name__ == "__main__":
    main()
