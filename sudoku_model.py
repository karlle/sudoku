
from sudoku_view import View
import random
import pygame
import bisect

class Model:

    def __init__ (self, window_width, cell_width, num_blanks):
        self.view = View(window_width, cell_width)
        self.cell_width = cell_width
        self.num_blanks = num_blanks
        self.clock =  pygame.time.Clock()
        self.active_cell = None
        self.newRandomSudoku()

    """
    Creates a new random Sudoku. The class variable num_blanks specifies the
    number of blank cells created in the Sudoku.
    """

    def newRandomSudoku(self):
        self.numbers = [[(0,'b') for c in range(9)] for r in range(9)]
        self.rows = [[] for r in range(9)]
        self.cols = [[] for c in range(9)]
        self.squares = [[] for c in range(9)]
        # start with all cells blank
        self.blanks = [(i,j) for i in range(9) for j in range(9)]
        # fill a complete valid Sudoku
        self.autofillSudoku(0,visualize=False)
        # create a number of blank cells in the filled Sudoku
        self.blanks = self.createBlanks(self.num_blanks)
        self.numbers = [[(n,'b') for (n,c) in row] for row in self.numbers]
        self.view.redrawWindow(self.numbers)


    """
    Removes number from a Sudoku to create blank cells. The number of blanks
    the method creates is defined by the parameter counter.
    """

    def createBlanks(self, counter):
        blanks = []
        while counter > 0:
            r = random.randint(0,8)
            c = random.randint(0,8)
            (n,col) = self.numbers[r][c]
            if n > 0:
                self.numbers[r][c] = (0,'b')
                blanks.append((r,c))
                self.rows[r].remove(n)
                self.cols[c].remove(n)
                square_index = (r // 3) * 3 + (c // 3)
                self.squares[square_index].remove(n)
                counter -= 1
        blanks.sort()

        return blanks


    """
    Recursive backtracking algorithm used for filling a valid sudoku. Fills
    the indices specified by the class variable blanks.

    Parameters:
        index: the current index in the variable blanks which the algorithm
               tries to fill.
        visualize: if True the search for a valid solution to the Sudoku is
                   visualized.

    """

    def autofillSudoku(self, index, visualize = True):
        (r,c) = self.blanks[index]
        square_index = (r // 3) * 3 + (c // 3)
        taken_numbers = self.rows[r] + self.cols[c] + self.squares[square_index]
        possible_numbers = [i for i in range(1,10) if i not in taken_numbers]

        while possible_numbers:
            i = random.randint(0,len(possible_numbers)-1)
            n = possible_numbers[i]
            self.numbers[r][c] = (n,'r')

            if visualize:
                self.clock.tick(15)
                self.view.redrawWindow(self.numbers)

            self.rows[r].append(n)
            self.cols[c].append(n)
            self.squares[square_index].append(n)

            # if we were able to place a number in the last blank cell of the
            # sudoku, it is solved
            if index == len(self.blanks)-1:
                self.numbers[r][c] = (n,'g')
                if visualize:
                    self.clock.tick(1)
                    self.view.redrawWindow(self.numbers)
                return True

            # we have placed a number valid so far, go to next index in blanks
            # and try to place a number
            new_index = index + 1
            if self.autofillSudoku(new_index, visualize):
                self.numbers[r][c] = (n,'g')
                if visualize:
                    self.clock.tick(15)
                    if index == 0:
                        self.view.redrawWindow(self.numbers, message=("Sudoku is solved, press r to create a new one!", (20,255,20)))
                    else:
                        self.view.redrawWindow(self.numbers)

                return True

            # could not find a valid solution to the Sudoku given the currently
            # choosen number, remove it from rows, cols and sqaures and
            # possible numbers and try another one.
            else:
                self.rows[r].pop()
                self.cols[c].pop()
                self.squares[square_index].pop()
                possible_numbers.pop(i)
        # no possible numbers left, the Sudoku is not solvable
        return False



    """
    Handles mouse click for choosing which cell in the sudoku to activate.
    An activated cell can be filled with a number.
    """
    def clickedMouse(self, mouse_pos):
        (x,y) = mouse_pos
        padding = self.view.padding

        # return if click is outside of sudoku
        if x < padding or x > 9*self.cell_width + padding \
                or y < padding or y > 9*self.cell_width + padding:
                return

        # get the right cell in the sudoku
        r = (y - padding) // self.cell_width
        c = (x - padding) // self.cell_width

        # if fixed number (black color) in cell do nothing
        if self.numbers[r][c][0] > 0  and self.numbers[r][c][1] == 'b':
            return

        # if we click an already active cell, unactivate it
        if (r,c) == self.active_cell:
            self.view.redrawWindow(self.numbers)
        else:
            # else mark the clicked cell as active
            self.active_cell = (r,c)
            self.view.redrawWindow(self.numbers, (r,c))

    """
    Handles inserting numbers manually into the sudoku
    """
    def pressedNum (self,num):
        if self.active_cell is not None:
            (r,c) = self.active_cell
            square_index = (r // 3) * 3 + (c // 3)
            prev_num = self.numbers[r][c][0]

            if num > 0:
                self.rows[r].append(num)
                self.cols[c].append(num)
                self.squares[square_index].append(num)

                if prev_num == 0:
                    self.blanks.remove((r,c))

            if prev_num > 0:
                self.rows[r].remove(prev_num)
                self.cols[c].remove(prev_num)
                self.squares[square_index].remove(prev_num)

                if num == 0:
                    bisect.insort(self.blanks, (r,c))

            self.numbers[r][c] = (num,'r')
            self.active_cell = None

            self.view.redrawWindow(self.numbers)


    """
    Checks if the sudoku is solvable given the current numbers. If the sudoku is
    still solvable all red numbers (numbers which have been filled in by the user)
    are turned green.
    """
    def checkIfSolvable (self):

        self.active_cell = None

        message = ("Sudoku is not solvable", (255,0,0))

        if self.containsDuplicates():
            self.view.redrawWindow(self.numbers, message = message)
            return

        # if no duplicates and no blanks left, sudoku is solved
        if len(self.blanks) == 0:
            message = ("Sudoku is solved, press r to create a new one!", (0,255,0))
            for r in range(9):
                for c in range(9):
                    (num,col) = self.numbers[r][c]
                    if col == 'r':
                        self.numbers[r][c] = (num,'g')
            self.view.redrawWindow(self.numbers, message = message)
            return

        temp_numbers = [row[:] for row in self.numbers]
        temp_rows = [row[:] for row in self.rows]
        temp_cols = [row[:] for row in self.cols]
        temp_squares = [row[:] for row in self.squares]

        if self.autofillSudoku(0,visualize = False):
            message = ("Sudoku is solvable", (0,255,0))
            self.numbers = temp_numbers
            for r in range(9):
                for c in range(9):
                    (num,col) = self.numbers[r][c]
                    if col == 'r':
                        self.numbers[r][c] = (num,'g')

        else:
            self.numbers = temp_numbers


        self.rows = temp_rows
        self.cols = temp_cols
        self.squares = temp_squares
        self.view.redrawWindow(self.numbers, message = message)


    """
    Returns true if a duplicate number exists in a row, column or square
    of the sudoku. If no such duplicate numbers exist, returns false.
    """
    def containsDuplicates (self):
        for row in self.rows:
            if len(row) > len(set(row)):
                return True

        for col in self.cols:
            if len(col) > len(set(col)):
                return True

        for square in self.squares:
            if len(square) > len(set(square)):
                return True

        return False
