import pygame, asyncio, time
from src.settings import *
from src.support import exit

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)

def updateCell(alive, neighbors):
    return neighbors == 3 or (alive and neighbors == 2)

def getNeighbors(grid, pos):
    x, y = pos
    neighboringCells = [(x - 1, y - 1), (x - 1, y + 0), (x - 1, y + 1),
                        (x + 0, y - 1),                 (x + 0, y + 1),
                        (x + 1, y - 1), (x + 1, y + 0), (x + 1, y + 1)]
    count = 0
    for x, y in neighboringCells:
        if x >= 0 and y >= 0:
            try:
                count += grid[x][y]
            except:
                pass
    return count

def newGrid(x, y):
    grid = []
    for row in range(x):
        row = []
        for col in range(y):
            row.append(0)
        grid.append(row)
    return grid

def updateGrid(grid, processing = False):
    x, y = len(grid), len(grid[0])
    newgrid = newGrid(x, y)

    for row in range(x):
        for col in range(y):
            cell = grid[row][col]
            neighbors = getNeighbors(grid, (row, col))
            color = COLORS[1] if cell == 0 else COLORS[3]

            if cell == 1:
                if neighbors < 2 or neighbors > 3:
                    if processing:
                        color = COLORS[1]

                elif 2 <= neighbors <= 3:
                    newgrid[row][col] = 1
                    if processing:
                        color = COLORS[3]
            else:
                if neighbors == 3:
                    newgrid[row][col] = 1
                    if processing:
                        color = COLORS[3]

            drawCell(row, col, color)
    return newgrid

def drawCell(x, y, aliveColor):
    x *= CELL_SIZE
    y *= CELL_SIZE
    pygame.draw.rect(screen, aliveColor, pygame.Rect((x, y), (CELL_SIZE - 1, CELL_SIZE - 1)), 0)

xLen, yLen = int(SCREEN_WIDTH / CELL_SIZE), int(SCREEN_HEIGHT / CELL_SIZE)
GRID = newGrid(int(SCREEN_WIDTH / CELL_SIZE), int(SCREEN_HEIGHT / CELL_SIZE))

async def main():
    global GRID, xLen, yLen, screen, clock
    screen.fill('black')
    updateGrid(GRID)
    # inc = 0

    running = False
    while True:

        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    updateGrid(GRID)

            if pygame.mouse.get_pressed()[0]:
                GRID[pos[0] // CELL_SIZE][pos[1] // CELL_SIZE] = 1
                updateGrid(GRID)

            if pygame.mouse.get_pressed()[2]:
                GRID[pos[0] // CELL_SIZE][pos[1] // CELL_SIZE] = 0
                updateGrid(GRID)

        if running:
            # inc += 1
            # pygame.image.save(screen, 'photos/jakester/' + str(inc) + '.png')
            GRID = updateGrid(GRID, processing = True)
            pygame.display.update()
            time.sleep(0.1)

        clock.tick(FPS)
        pygame.display.flip()
        await asyncio.sleep(0)

if __name__ == '__main__':
    asyncio.run(main())