import pygame
from pygame.locals import *

GRID = [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 5],
    [3, 1, 0, 0, 0, 5],
    [3, 3, 3, 3, 5, 5],
    [3, 3, 2, 2, 2, 4],
    [3, 3, 3, 4, 4, 4],
]
GRID_SIZE = 6
SQUARE_WIDTH = 150
BORDER_WIDTH = 1


class Border(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Border, self).__init__()

        self.surf = pygame.Surface((SQUARE_WIDTH, SQUARE_WIDTH))

        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.position = position
        self.highlighted = False

    def toggle_highlight(self):
        if self.highlighted:
            self.surf.fill((0, 0, 0))
            self.rect = self.surf.get_rect()
        else:
            self.surf.fill((255, 0, 0))
            self.rect = self.surf.get_rect()
        self.highlighted = not self.highlighted

    def render(self, screen):
        screen.blit(self.surf, self.position)


class Square(pygame.sprite.Sprite):
    COLORS = [
        (153, 255, 255),  # 0 = blue
        (255, 153, 153),  # 1 = red
        (153, 255, 204),  # 2 = green
        (255, 204, 153),  # 3 = orange
        (255, 255, 204),  # 4 = yellow
        (229, 204, 255),  # 5 = purple
    ]

    TEXT_VALUES = [
        '',
        '-',
        'X'
    ]

    def __init__(self, color_idx, position):
        super(Square, self).__init__()
        self.color_idx = color_idx
        self.corner = position
        self.position = (position[0] + BORDER_WIDTH, position[1] + BORDER_WIDTH)

        self.surf = pygame.Surface((SQUARE_WIDTH - 2 * BORDER_WIDTH, SQUARE_WIDTH - 2 * BORDER_WIDTH))

        self.surf.fill(Square.COLORS[self.color_idx])
        self.rect = self.surf.get_rect()

        self.text_idx = 0
        self.font = pygame.font.SysFont('Corbel', 70, bold=True)
        self.text = None

    def draw(self):
        self.surf.fill(Square.COLORS[self.color_idx])
        self.rect = self.surf.get_rect()

    def render(self, screen):
        screen.blit(self.surf, self.position)
        self.text = self.font.render(Square.TEXT_VALUES[self.text_idx], True, (0, 153, 0))
        x, y, w, h = self.text.get_rect()
        x_center = self.corner[0] + SQUARE_WIDTH // 2 - w // 2
        y_center = self.corner[1] + SQUARE_WIDTH // 2 - h // 2
        screen.blit(self.text, (x_center, y_center))

    def next_text(self):
        self.text_idx += 1
        self.text_idx = self.text_idx % (len(Square.TEXT_VALUES))

    def reset_text(self):
        self.text_idx = 0

    @property
    def is_tree(self):
        return self.text_idx == 2

    def set_tree(self):
        self.text_idx = 2


def render(screen, squares, borders):
    for sq_row, bor_row in zip(squares, borders):
        for sq, bor in zip(sq_row, bor_row):
            bor.render(screen)
            sq.render(screen)


def run_game(grid):
    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE * SQUARE_WIDTH, GRID_SIZE * SQUARE_WIDTH))

    borders, squares = build_grid(grid)

    game_on = True
    render(screen, squares, borders)
    prev_highlighted = None
    while game_on:
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        obj_x = mouse_pos_x // SQUARE_WIDTH
        obj_y = mouse_pos_y // SQUARE_WIDTH

        if pygame.mouse.get_focused() == 0:
            if prev_highlighted is not None:
                prev_highlighted.toggle_highlight()
            prev_highlighted = None
        else:
            borders[obj_y][obj_x].toggle_highlight()
            if prev_highlighted is not None:
                prev_highlighted.toggle_highlight()
            prev_highlighted = borders[obj_y][obj_x]

        # for loop through the event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                game_on = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # LEFT
                    squares[obj_y][obj_x].next_text()
                elif event.button == 3:  # RIGHT
                    squares[obj_y][obj_x].reset_text()

        render(screen, squares, borders)
        pygame.display.flip()


def build_grid(grid):
    squares = []
    borders = []
    for col_idx, column in enumerate(grid):
        square_row = []
        border_row = []
        for row_idx, color in enumerate(column):
            x_coordinate = row_idx * SQUARE_WIDTH
            y_coordinate = col_idx * SQUARE_WIDTH
            square = Square(color, (x_coordinate, y_coordinate))
            border = Border((x_coordinate, y_coordinate))
            square_row.append(square)
            border_row.append(border)
        squares.append(square_row)
        borders.append(border_row)
    return borders, squares


if __name__ == '__main__':
    run_game(GRID)
