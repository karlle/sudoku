from sudoku_model import Model
import pygame

class Controller:

    def __init__ (self, window_width, num_rows, cell_width, difficulty = 'Medium'):
        num_blanks = 25
        if difficulty == 'Easy':
            num_blanks = 15
        elif difficulty == 'Hard':
            num_blanks = 40

        self.model = Model(window_width ,cell_width, num_blanks)
        self.gameLoop()

    def gameLoop(self):

        clock = pygame.time.Clock()
        flag = True
        num = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, \
               pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

        while flag:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    flag = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.model.clickedMouse(event.pos)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.model.newRandomSudoku()
                if keys[pygame.K_f]:
                    self.model.autofillSudoku(0)
                    pygame.event.clear()
                for i in range(0,len(num)):
                    if keys[num[i]]:
                        self.model.pressedNum(i)
                if keys[pygame.K_c]:
                    self.model.checkIfSolvable()



c = Controller(550,9,50,difficulty="Easy")
