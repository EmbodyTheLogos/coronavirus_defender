import pygame
import random

# initialize the pygame
pygame.init()

# create the screen
# set_mode(width, height)
screen = pygame.display.set_mode((800, 600))


# Title and Icon
pygame.display.set_caption("CoronaVirus Defender")
icon = pygame.image.load('coronavirus.png')
pygame.display.set_icon(icon)

# Score of the player
score_value = 0

# Displaying text
score_font = pygame.font.Font('freesansbold.ttf', 20)
end_font = pygame.font.Font('freesansbold.ttf', 40)

# Position of score on screen
textX = 10
textY = 10

# Player
playerImg = pygame.image.load('nurse.png')
playerX = 390
playerX_change = 0
playerY = 480

# Enemy
enemies = []
enemyImg = pygame.image.load('coronavirus.png')

# initialize 10 enemies:
for i in range(0, 10):
    enemyX = random.randint(0, 736)
    enemyY = random.randint(0, 150)
    enemyX_change = 0.3
    enemyY_change = 0
    enemies.append([enemyX, enemyY, enemyX_change, enemyY_change])

# Bullet
# Ready - you can't see the bullet on the screen. You are ready to fire.
# Fire - the bullet is currently moving
bulletImg = pygame.image.load('syringe.png')
bulletX = 0
bulletY = 480
bulletY_change = 1
bullet_state = 'ready'


def player(x, y):
    # draw an image of player on screen
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    # drawng an image of an enemy on screen
    # Check if an enemy is already destroyed or not. If not, then draw the enemy
    if x >= -90 and y >= -90:
        screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 16))


def isCollision(enemyX, enemyY, bulletX, bulletY, range):
    if abs(enemyX - bulletX) < range and abs(enemyY - bulletY) < range:
        return True
    else:
        return False


def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over(x, y):
    end_game = end_font.render("Game Over", True, (0, 0, 0))
    screen.blit(end_game, (x, y))


def you_win(x, y):
    winner = end_font.render("You won!", True, (0, 0, 0))
    screen.blit(winner, (x, y))


# keep track of left and right key when they are still being pressed.
left_pressed = False
right_pressed = False

# Too many components on the screen will make the game run slow. We fix it by increasing the speed of the game.
# Each time an enemy is destroyed, we decrease the scale by 0.2 to make game run slower since there are less components than before.
scale = 2

# this variable determined if the game is over or not
end = False

# Game loop
running = True
while running:
    # background color. Silver in this case
    screen.fill((192, 192, 192))

    # going through all of pygame event
    for event in pygame.event.get():
        # if somebody closes the game, then we got out of this loop.
        # if the game is not over, 'end' will still be False, thus, breaking out of this loop implies quitting the game.
        # if the game is over, then break out of this loop and let the second loop take care of the rest.
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                left_pressed = True
            if event.key == pygame.K_RIGHT:
                right_pressed = True
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_pressed = False
            if event.key == pygame.K_RIGHT:
                right_pressed = False

    # Take care of the case where one key is still pressed but another is up
    if right_pressed == True and left_pressed == False:
        playerX_change = 0.5 * scale
    if left_pressed == True and right_pressed == False:
        playerX_change = -0.5 * scale
    if left_pressed == False and right_pressed == False:
        playerX_change = 0

    # Checking for boundary of player so that it doesn't go out of bound
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    for i in range(0, len(enemies)):
        if enemies[i][0] <= 0:  # enemyX
            enemies[i][2] = +0.3 * scale  # enemyX_change
            enemies[i][1] += 20  # enemyY_change

        if enemies[i][0] >= 736:  # enemyX
            enemies[i][2] = -0.3 * scale  # enemyX_change
            enemies[i][1] += 20  # enemyY_change

        if enemies[i][0] >= -90:  # if an enemy is already destroyed
            enemies[i][0] += enemies[i][2]
        enemy(enemies[i][0], enemies[i][1])

        # Collision
        collision = isCollision(enemies[i][0], enemies[i][1], bulletX, bulletY, 32)

        if collision and bullet_state == 'fire':
            bulletY = 400
            bullet_state = 'ready'
            score_value += 1
            scale -= 0.1

            # signal that the enemy is destroyed
            enemies[i][0] = -99
            enemies[i][1] = -99

        # If an enemy collides with you, then you die and game over
        youDied = isCollision(enemies[i][0], enemies[i][1], playerX, playerY, 45)
        if youDied:
            # This is when the game is over.
            # Then you exit this loop and go to the second loop to take care of things there instead.
            running = False
            end = True

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 400
        bullet_state = 'ready'
        bulletX = 0

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY_change = 1 * scale
        bulletY -= bulletY_change

    player(playerX, playerY)

    # You Win if you destroyed all 10 enemies!
    if score_value == 10:
        you_win(320, 250)

    show_score(textX, textY)
    pygame.display.update()

# ending of the game. When you lose the game.
while end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False

    player(playerX, playerY)
    show_score(textX, textY)
    game_over(310, 250)
    pygame.display.update()