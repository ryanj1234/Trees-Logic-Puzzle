import pygame
from main import build_grid
from logic import is_won


def test_not_won():
    grid = [
        [0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 5],
        [3, 1, 0, 0, 0, 5],
        [3, 3, 3, 3, 5, 5],
        [3, 3, 2, 2, 2, 4],
        [3, 3, 3, 4, 4, 4],
    ]

    pygame.init()
    _, squares = build_grid(grid)
    assert not is_won(squares)


def test_won():
    grid = [
        [0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 5],
        [3, 1, 0, 0, 0, 5],
        [3, 3, 3, 3, 5, 5],
        [3, 3, 2, 2, 2, 4],
        [3, 3, 3, 4, 4, 4],
    ]

    pygame.init()
    _, squares = build_grid(grid)

    squares[0][3].set_tree()
    squares[1][1].set_tree()
    squares[2][5].set_tree()
    squares[3][0].set_tree()
    squares[4][2].set_tree()
    squares[5][4].set_tree()

    assert is_won(squares)
