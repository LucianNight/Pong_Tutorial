import pygame

#Basic Set Up
pygame.init()
clock = pygame.time.Clock()

#define screen variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Pong Tutorial")

#Game Variable
play = True

#Define colors
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)

class Player:
    def __init__(self, player, pos_x, pos_y, color):
        self.player = player
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.height = 120
        self.width = 20
        self.rect = pygame.Rect(self.pos_x,self.pos_y, self.width,self.height)
        self.color = color


    def move(self):
        vel_y = 0
        SPEED = 10
        
        key = pygame.key.get_pressed()
        #checks for which player it is first
        #then for which button is pressed and determines
        #positive and negative speed depending (top of the screen = 0)
        if self.player == 1:
            if key[pygame.K_w]:
                vel_y = -SPEED
            if key[pygame.K_s]:    
                vel_y = SPEED
        if self.player == 2:
            if key[pygame.K_UP]:
                vel_y = -SPEED
            if key[pygame.K_DOWN]:
                vel_y = SPEED
            
            
        #keeps the players within the bounds of the screen
        if self.rect.top + vel_y <= 0:
            vel_y = -self.rect.top
        if self.rect.bottom + vel_y >= SCREEN_HEIGHT:
            vel_y = SCREEN_HEIGHT - self.rect.bottom

        #updates the rectangle of the player from the velocity of y    
        self.rect.y += vel_y
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Ball:
    def __init__(self, pos_x, pos_y, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.height = 20
        self.width = 20
        self.radius = 10
        self.rect = pygame.Rect(self.pos_x - self.radius,self.pos_y - self.radius, self.width,self.height)
        self.rect.center = (self.pos_x,self.pos_y)
        self.color = color
        self.vel_x = 7
        self.vel_y = 7

    def move(self, player_one, player_two):

        #if the ball hits the bottom of the screen or the top of the screen
        #it "bounces" and changes directions
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.vel_y *= -1
        if self.rect.top <= 0:
            self.vel_y *= -1

        #Checks for collision with either of the paddles
        if self.rect.colliderect(player_one) or self.rect.colliderect(player_two):   
            self.vel_x *= -1

        #If the ball goes off the screen it resets to let the
        #losing player serve
        if self.rect.left >= SCREEN_WIDTH:
            self.pos_x = player_two.rect.left - self.radius  
            self.pos_y = player_two.rect.centery
            self.vel_x = -7 
            self.vel_y = -7

        if self.rect.right <= 0:
            self.pos_x = player_one.rect.right + self.radius
            self.pos_y = player_one.rect.centery
            self.vel_x = 7
            self.vel_y = 7
            
        #Updated the ball position x and y with the change in velocities
        self.pos_y += self.vel_y
        self.pos_x += self.vel_x

        #updates the rectangle of the ball
        self.rect.center = (self.pos_x,self.pos_y)

    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.pos_x,self.pos_y) , self.radius)

#create instances of the players and ball
player1 = Player(1, 20, SCREEN_HEIGHT / 2 - 60, RED)
player2 = Player(2, SCREEN_WIDTH - 40, SCREEN_HEIGHT / 2 - 60, RED)
ball = Ball(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, BLUE)


#main game loop
while play:

    #keeps game at 60 fps
    clock.tick(60)

    #fills background
    screen.fill(GREEN)

    #draw players and ball
    player1.draw(screen)
    player2.draw(screen)
    ball.draw(screen)

    #move players and ball
    player1.move()
    player2.move()
    ball.move(player1, player2)

    #event handler for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    #updates image for screen
    pygame.display.update()
            
pygame.quit()
