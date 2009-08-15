import unittest
from eightqueens import checker

BOARD_TOO_SMALL = ['Q' * 3 for i in range(3)]
BOARD_TOO_BIG = ['Q' * 10 for i in range(10)]
BOARD_WITH_TOO_MANY_COLS = ['Q' * 9 for i in range(8)]
BOARD_WITH_TOO_MANY_ROWS = ['Q' * 8 for i in range(9)]
BOARD_FULL_OF_QS = ['Q' * 8 for i in range(8)]
BOARD_FULL_OF_CRAP = [chr(65 + i) * 8 for i in range(8)]
BOARD_EMPTY = [' ' * 8 for i in range(8)]

BOARD_WITH_QS_IN_THE_SAME_ROW = ['Q   Q   ',
                                 '        ',
                                 '       Q',
                                 '     Q  ',
                                 '  Q     ',
                                 '      Q ',
                                 ' Q      ',
                                 '   Q    ']
BOARD_WITH_WRONG_SOLUTION = BOARD_WITH_QS_IN_THE_SAME_ROW

BOARD_WITH_QS_IN_THE_SAME_COL = ['Q       ',
                                 '    Q   ',
                                 '       Q',
                                 'Q       ',
                                 '  Q     ',
                                 '      Q ',
                                 ' Q      ',
                                 '   Q    ']

BOARD_WITH_QS_IN_THE_SAME_DIAG_1 = ['        ',
                                    '        ',
                                    '        ',
                                    '        ',
                                    '        ',
                                    '        ',
                                    'Q       ',
                                    ' Q      ']

BOARD_WITH_QS_IN_THE_SAME_DIAG_2 = ['        ',
                                    '   Q    ',
                                    '        ',
                                    '     Q  ',
                                    '        ',
                                    '        ',
                                    '        ',
                                    '        ']

BOARD_WITH_QS_IN_THE_SAME_DIAG_3 = ['        ',
                                    '      Q ',
                                    '        ',
                                    '        ',
                                    '        ',
                                    '  Q     ',
                                    '        ',
                                    '        ']


BOARD_WITH_QS_IN_THE_SAME_DIAG_4 = ['        ',
                                    '    Q   ',
                                    '        ',
                                    '        ',
                                    '        ',
                                    'Q       ',
                                    '        ',
                                    '        ']


BOARD_WITH_QS_IN_THE_SAME_DIAG_5 = ['       Q',
                                    '      Q ',
                                    '     Q  ',
                                    '    Q   ',
                                    '   Q    ',
                                    '  Q     ',
                                    ' Q      ',
                                    'Q       ']



BOARD_WITH_SOLUTION = ['Q       ',
                       '    Q   ',
                       '       Q',
                       '     Q  ',
                       '  Q     ',
                       '      Q ',
                       ' Q      ',
                       '   Q    ']


class ValidationTest(unittest.TestCase):
    def testValidateShape(self):
        def assertNotValidShape(board):
            self.assertFalse(checker._validate_shape(board))

        # Some invalid shapes:
        assertNotValidShape([])
        assertNotValidShape(BOARD_TOO_SMALL)
        assertNotValidShape(BOARD_TOO_BIG)
        assertNotValidShape(BOARD_WITH_TOO_MANY_COLS)
        assertNotValidShape(BOARD_WITH_TOO_MANY_ROWS)
        
        def assertValidShape(board):
            self.assert_(checker._validate_shape(board))

        assertValidShape(BOARD_WITH_SOLUTION)
        # Shape validation doesn't care about board contents:
        assertValidShape(BOARD_FULL_OF_QS)        
        assertValidShape(BOARD_FULL_OF_CRAP)

    def testValidateContents(self):
        # Valid content => only 'Q' and ' ' in the board
        self.assertFalse(checker._validate_contents(BOARD_FULL_OF_CRAP))
        self.assert_(checker._validate_contents(BOARD_WITH_SOLUTION))
        # Content validation doesn't care about the number of queens:
        self.assert_(checker._validate_contents(BOARD_FULL_OF_QS))


    def testValidateQueens(self):
        self.assertFalse(checker._validate_queens(BOARD_FULL_OF_QS))
        self.assertFalse(checker._validate_queens(BOARD_EMPTY))
        self.assert_(checker._validate_queens(BOARD_WITH_SOLUTION))
        self.assert_(checker._validate_queens(BOARD_WITH_WRONG_SOLUTION))
        

class PartialSolutionTest(unittest.TestCase):
    def testRowsOK(self):
        self.assert_(checker._rows_ok(BOARD_WITH_SOLUTION))
        self.assertFalse(checker._rows_ok(BOARD_WITH_QS_IN_THE_SAME_ROW))

    def testColsOK(self):
        self.assert_(checker._cols_ok(BOARD_WITH_SOLUTION))
        self.assertFalse(checker._cols_ok(BOARD_WITH_QS_IN_THE_SAME_COL))

    def testDiagonalsOK(self):
        self.assert_(checker._diagonals_ok(BOARD_WITH_SOLUTION))
        self.assertFalse(
            checker._diagonals_ok(BOARD_WITH_QS_IN_THE_SAME_DIAG_1))
        self.assertFalse(
            checker._diagonals_ok(BOARD_WITH_QS_IN_THE_SAME_DIAG_2))
        self.assertFalse(
            checker._diagonals_ok(BOARD_WITH_QS_IN_THE_SAME_DIAG_3))
        self.assertFalse(
            checker._diagonals_ok(BOARD_WITH_QS_IN_THE_SAME_DIAG_4))
        self.assertFalse(
            checker._diagonals_ok(BOARD_WITH_QS_IN_THE_SAME_DIAG_5))

class SolutionTest(unittest.TestCase):
    def testIsSolution(self):
        self.assert_(checker.is_solution(BOARD_WITH_SOLUTION))

        self.assertFalse(checker.is_solution(BOARD_WITH_QS_IN_THE_SAME_COL))
        self.assertFalse(checker.is_solution(BOARD_WITH_QS_IN_THE_SAME_ROW))
        self.assertFalse(checker.is_solution(BOARD_WITH_QS_IN_THE_SAME_DIAG_5))

        self.assertRaises(ValueError, checker.is_solution, BOARD_TOO_SMALL)
        self.assertRaises(ValueError, checker.is_solution, BOARD_FULL_OF_CRAP)
        self.assertRaises(ValueError, checker.is_solution, BOARD_EMPTY)
        
