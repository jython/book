"""
eightqueen.checker: Validates solutions for the eight queens puzzle.

Provides the function is_solution(board) to determine if a board represents a
valid solution of the puzzle.

The chess board is represented by list of 8 strings, each string of length
8. Positions occupied by a Queen are marked by the character 'Q', and empty
spaces are represented by an space character.

Here is a valid board:

>>> board = ['Q       ',
...          ' Q      ',
...          '  Q     ',
...          '   Q    ',
...          '    Q   ',
...          '     Q  ',
...          '      Q ',
...          '       Q']

Naturally, it is not a correct solution:

>>> is_solution(board)
False

Here is a correct solution:

>>> is_solution(['Q       ',
...              '    Q   ',
...              '       Q',
...              '     Q  ',
...              '  Q     ',
...              '      Q ',
...              ' Q      ',
...              '   Q    '])
True

Malformed boards are rejected and a ValueError is thrown:

>>> is_solution([])
Traceback (most recent call last):
...
ValueError: Malformed board

Only 8 x 8 boards are supported.

>>> is_solution(['Q   ',
...              ' Q  ',
...              '  Q ',
...              '   Q'])
Traceback (most recent call last):
...
ValueError: Malformed board

And they must only contains Qs and spaces:

>>> is_solution(['X       ',
...              '    X   ',
...              '       X',
...              '     X  ',
...              '  X     ',
...              '      X ',
...              ' X      ',
...              '   X    '])
Traceback (most recent call last):
...
ValueError: Malformed board

And the total number of Qs must be eight:

>>> is_solution(['QQQQQQQQ',
...              'Q       ',
...              '        ',
...              '        ',
...              '        ',
...              '        ',
...              '        ',
...              '        '])
Traceback (most recent call last):
...
ValueError: There must be exactly 8 queens in the board

>>> is_solution(['QQQQQQQ ',
...              '        ',
...              '        ',
...              '        ',
...              '        ',
...              '        ',
...              '        ',
...              '        '])
Traceback (most recent call last):
...
ValueError: There must be exactly 8 queens in the board
             
"""

def _validate_shape(board):
    return (board and
            len(board) == 8 and
            all(len(row) == 8 for row in board))

def _validate_contents(board):
    for row in board:
        for square in row:
            if square not in ('Q', ' '):
                return False
    return True

def _count_queens(row):
    n = 0
    for square in row:
        if square == 'Q':
            n += 1
    return n

def _validate_queens(board):
    n = 0
    for row in board:
        n += _count_queens(row)
    return n == 8

def _scan_ok(board, coordinates):
    queen_already_found = False
    for i, j in coordinates:
        if board[i][j] == 'Q':
            if queen_already_found:
                return False
            else:
                queen_already_found = True
    return True
        

def _rows_ok(board):
    for i in range(8):
        if not _scan_ok(board, [(i, j) for j in range(8)]):
            return False
    return True

def _cols_ok(board):
    for j in range(8):
        if not _scan_ok(board, [(i, j) for i in range(8)]):
            return False
    return True

def _diagonals_ok(board):
    for k in range(8):
        # Diagonal: (0, k), (1, k + 1), ..., (7 - k, 7)...
        if not _scan_ok(board, [(i, k + i) for i in range(8 - k)]):
            return False
        # Diagonal: (k, 0), (k + 1, 1), ..., (7, 7 - k)
        if not _scan_ok(board, [(k + j, j) for j in range(8 - k)]):
            return False

        # Diagonal: (0, k), (1, k - 1), ..., (k, 0)
        if not _scan_ok(board, [(i, k - i) for i in range(k + 1)]):
            return False        

        # Diagonal: (7, k), (6, k - 1), ..., (k, 7)
        if not _scan_ok(board, [(7 - j, k + j) for j in range(8 - k)]):
            return False
    return True

def is_solution(board):
    if not _validate_shape(board) or not _validate_contents(board):
        raise ValueError("Malformed board")
    if not _validate_queens(board):
        raise ValueError("There must be exactly 8 queens in the board")
    return _rows_ok(board) and _cols_ok(board) and _diagonals_ok(board)
