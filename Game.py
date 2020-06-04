# I will be building a speed test for typing.

# We start off by importing all the relevant libraries

import pygame
import time
import random
import sys


# Then we create the relevant class

class Game:
    # write the an initilizer class AKA the "constructor" and all the relevant parameters for the window and the program
    def __init__(self):
        self.width = 800
        self.height = 600
        self.reset = True
        self.active = False
        self.input = ""
        self.word = ''
        self.tstart = 0
        self.total_t = 0
        self.accuracy = '0%'
        self.final_results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.words_per_minute = 0
        self.end = False
        self.Head_Color = (255, 213, 102)
        self.Text_Color = (240, 240, 240)
        self.Result_Color = (255, 70, 70)

        # After weve done that, we will call the init method on pygame and create a background and a image that opens when opening the window
        # We make sure that theyre fitted into the width and height, as well as we set the w and h for the window
        pygame.init()
        self.openimg = pygame.image.load("game_img.jpg")
        self.openimg = pygame.transform.scale(self.openimg, (self.width, self.height))

        self.background = pygame.image.load('background.jpg')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Welcome to the game")

    def run(self):
        pass


# Next, we create a helper function that will show us what is needed on the screen
    def show_text(self, screen, message, height, font_size, color):
        font = pygame.font.Font(None, font_size)
        text = font.render(message, 1, color)
        text_rect = text.get_rect(center=(self.width / 2, height))
        screen.blit(text, text_rect)


    # The user will have a randomly generated text which is picked from a wordlist txt file. We create a get sentence method
    # And return the random sentence we have split

    def read_sentence(self):
        readFile = open('sentencelist.txt').read()
        sentences = readFile.split('\n')
        sentence = random.choice(sentences)
        return sentence


    # After the game is played, a score is shown. Time elapsed is shown as well as the accuracy
    # The way accuracy is calculated is by comparing how many correct letters the user got compared to the sentence shown.
    def final_score(self, screen):
        if not self.end:
            self.total_t = time.time() - self.tstart
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input[i] == c:
                        count += 1
                except:
                    pass
                # shown in percentage
            self.accuracy = count / len(self.word) * 100

            self.words_per_minute = len(self.input) * 60 / (5 * self.total_t)
            self.end = True
            print(self.total_t)

            self.final_results = 'Time: ' + str(round(self.total_t)) + " Accuracy: " + str(
                round(self.accuracy)) + "%" + ' Word Per Minute: ' + str(round(self.words_per_minute))

            self.refresh_img = pygame.image.load('Refresh.jpg')
            self.refresh_img = pygame.transform.scale(self.refresh_img, (150, 150))
            screen.blit(self.refresh_img, (self.width / 2 - 75, self.height - 140))


            print(self.final_results)
            pygame.display.update()


    # Now we write our run method which to begin with resets the game with the reset method and starts a new game

    def run(self):
        self.reset_game()

        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.Head_Color, (50, 250, 650, 50), 2)
            self.show_text(self.screen, self.input, 274, 26, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if 50 <= x <= 650 and 250 <= y <= 300:
                        self.active = True
                        self.input = ''
                        self.tstart = time.time()
                        if x>=325 and x <= 510 and y>= 460 and self.end:
                            self.reset_game()
                            x, y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input)
                            self.final_score(self.screen)
                            print(self.final_results)
                            self.show_text(self.screen, self.final_results, 350, 28, self.Result_Color)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input = self.input[:-1]
                        else:
                            try:
                                self.input += event.unicode
                            except:
                                pass
            pygame.display.update()
        clock.tick(60)

        # We need to somehow reset all the variables, and thats what we do i the reset game method


    def reset_game(self):
        self.screen.blit(self.openimg, (0, 0))

        pygame.display.update()
        time.sleep(1)
        self.reset = False
        self.end = False
        self.input = ''
        self.word = ''
        self.tstart = 0
        self.total_t = 0
        self.words_per_minute = 0
        # Get random sentence
        self.word = self.read_sentence()
        if (not self.word): self.reset_game()

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        msg = "Typing Speed Test"
        self.show_text(self.screen, msg, 80, 80, self.Head_Color)
        # draw the rectangle for input box
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)
        # draw the sentence string
        self.show_text(self.screen, self.word, 200, 28, self.Text_Color)
        pygame.display.update()


Game().run()
