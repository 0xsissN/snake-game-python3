import pygame
import time
import random
from pygame.locals import *

SIZE = 25

## Here we define the apple.
## We load the image, configure the size, show the position in which it will appear
class Apple:
    def __init__(self, parentScreen):
        self.parentScreen = parentScreen
        self.image = pygame.image.load("D:/Python/Projects/SnakeGame/Resources/apple.png").convert()
        self.x = SIZE*3
        self.y = SIZE*3
        
    def draw(self):
        self.parentScreen.blit(self.image,(self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 39) * SIZE
        self.y = random.randint(1, 31) * SIZE

## Here we define the snake
## We load the image, load the direction it is taking, show the size and increase the length
class Snake:
    def __init__(self, parentScreen):
        self.parentScreen = parentScreen
        self.image = pygame.image.load("D:/Python/Projects/SnakeGame/Resources/snake.png").convert()
        self.direction = 'right'
        self.length = 1
        self.x = [25]
        self.y = [25]

    def move_left(self):
        self.direction = 'left'
        
    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'
        
    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
            
        if self.direction == 'left':
            self.x[0] -= SIZE

        if self.direction == 'right':
            self.x[0] += SIZE

        if self.direction == 'up':
            self.y[0] -= SIZE

        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self): 
        for i in range(self.length):
            self.parentScreen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increaseLength(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

## Here we define the game.
## We configure the background, display size, define the start and end screen messages
## We define the collision, update the score
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SNAKE GAME")
        self.surface = pygame.display.set_mode((1200, 800))
        self.background = pygame.image.load("D:/Python/Projects/SnakeGame/Resources/bground.jpg").convert()
        self.background = pygame.transform.scale(self.background, (self.surface.get_width(), self.surface.get_height())) 
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def isCollision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    def isCollisionBorder(self, x, y):
        if x < 0 or x >= 1200 or y < 0 or y >= 800:
            return True
        return False

    def play(self):
        self.surface.blit(self.background, (0, 0))
        self.snake.walk()
        self.apple.draw()
        self.displayScore()
        pygame.display.flip()

        #Snake coliding with an apple
        if self.isCollision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increaseLength()
            self.apple.move()

        #Snake coliding with itself 
        for i in range(2, self.snake.length):
            if self.isCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision ocurred"

        #Snake coliding with the border 
        if self.isCollisionBorder(self.snake.x[0], self.snake.y[0]):
            raise "Collision with border occurred"

    def displayScore(self):
        font = pygame.font.SysFont('calibri', 35)
        score = font.render(f"Score: {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(score,(950, 10))
        
    def gameOver(self):
        self.surface.blit(self.background, (0, 0))
        font = pygame.font.SysFont('calibri', 30)
        line0 = font.render("Game over!", True, (0, 0, 0))
        self.surface.blit(line0, (450, 300))
        linel = font.render(f"Your score is {self.snake.length}", True, (0, 0, 0))
        self.surface.blit(linel, (435, 350))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (0, 0, 0))
        self.surface.blit(line2, (280, 400))
        pygame.display.flip()
        
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause: 
                    self.play()
            except Exception as e:
                self.gameOver()
                pause=True
                self.reset()
                
            time.sleep( 0.1 ) 
    
if __name__ == '__main__':
    game=Game()
    game.run()

## Do you know who did it?
