import pygame

class View:

    def __init__ (self, window_width, cell_width):
        self.window_width = window_width
        self.cell_width = cell_width
        self.padding = 50
        self.surface = pygame.display.set_mode((self.window_width, self.window_width+self.padding*2))
        pygame.init()
        pygame.display.set_caption('Sudoku')


    def redrawWindow(self, numbers, active_cell = None, message = None):
        self.surface.fill((255,255,255))
        self.drawGrid()
        self.drawNumbers(numbers)
        self.printInstructions()
        if active_cell is not None:
            self.markCell(active_cell)
        if message is not None:
            self.printMessage(message)
        pygame.display.update()


    def drawGrid(self):
        x = self.padding
        y = self.padding
        for l in range(10):
            if l % 3 == 0:
                pygame.draw.line(self.surface, (0,0,0), (x,self.padding),(x,self.window_width-self.padding), 4)
                pygame.draw.line(self.surface, (0,0,0), (self.padding,y),(self.window_width-self.padding,y), 4)
            else:
                pygame.draw.line(self.surface, (0,0,0), (x,self.padding),(x,self.window_width-self.padding))
                pygame.draw.line(self.surface, (0,0,0), (self.padding,y),(self.window_width-self.padding,y))
            x += self.cell_width
            y += self.cell_width


    def drawNumbers(self, numbers):
        font = pygame.font.SysFont('arial', 25)

        for r in range(len(numbers)):
            for c in range(len(numbers)):
                if numbers[r][c][0] > 0:
                    if numbers[r][c][1] == 'b':
                        number = font.render(str(numbers[r][c][0]), 1, (0,0,0))
                    elif numbers [r][c][1] == 'r':
                        number = font.render(str(numbers[r][c][0]), 1, (255,0,0))
                    elif numbers [r][c][1] == 'g':
                        number = font.render(str(numbers[r][c][0]), 1, (0,255,0))
                    self.surface.blit(number, (c*self.cell_width+18 + self.padding,r*self.cell_width+12 + self.padding))


    def printInstructions(self):
        font = pygame.font.SysFont('arial', 20)
        text = font.render("Click on an empty cell to activate it, ", 1, (0,0,0))
        self.surface.blit(text, (self.window_width/2-text.get_rect().width // 2,self.window_width-self.padding/2 - 5))
        text = font.render("then type a number to insert it into the cell.", 1, (0,0,0))
        self.surface.blit(text, (self.window_width/2-text.get_rect().width // 2,self.window_width-self.padding/2+15))
        text = font.render("r: create new Sudoku", 1, (0,0,0))
        self.surface.blit(text, (self.window_width/2-text.get_rect().width // 2,self.window_width-self.padding/2+40))
        text = font.render("c: check if Sudoku is still solvable", 1, (0,0,0))
        self.surface.blit(text, (self.window_width/2-text.get_rect().width // 2,self.window_width-self.padding/2+60))
        text = font.render("f: fill the whole Sudoku", 1, (0,0,0))
        self.surface.blit(text, (self.window_width/2-text.get_rect().width // 2,self.window_width-self.padding/2+80))


    """
    Draws a red line around the active cell
    """
    def markCell(self, active_cell):
        (r,c) = active_cell
        upper_left = (self.padding + c*self.cell_width, self.padding + r*self.cell_width)
        lower_left = (self.padding + c*self.cell_width, self.padding + (r+1)*self.cell_width)
        upper_right = (self.padding + (c+1)*self.cell_width, self.padding + r*self.cell_width)
        lower_right = (self.padding + (c+1)*self.cell_width, self.padding + (r+1)*self.cell_width)

        if c % 3 == 0:
            pygame.draw.line(self.surface, (255,0,0), upper_left,lower_left, 4)
        else:
            pygame.draw.line(self.surface, (255,0,0), upper_left,lower_left)

        if (c+1) % 3 == 0:
            pygame.draw.line(self.surface, (255,0,0), upper_right,lower_right, 4)
        else:
            pygame.draw.line(self.surface, (255,0,0), upper_right,lower_right)

        if r % 3 == 0:
            pygame.draw.line(self.surface, (255,0,0), upper_left,upper_right,4)
        else:
            pygame.draw.line(self.surface, (255,0,0), upper_left,upper_right)

        if (r+1) % 3 == 0:
            pygame.draw.line(self.surface, (255,0,0), lower_left,lower_right,4)
        else:
            pygame.draw.line(self.surface, (255,0,0), lower_left,lower_right)


    def printMessage(self, message):
        font = pygame.font.SysFont('arial', 20)
        (message_text, color) = message
        text = font.render(message_text, 2, color)
        self.surface.blit(text, (self.window_width/2-text.get_rect().width // 2,10))
