import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Invaders')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define game variables
player_width, player_height = 60, 10
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 5

enemies = [{'rect': pygame.Rect(j * 50 + 20, i * 30 + 20, 40, 20), 'speed': 1, 'drop': False} for i in range(5) for j in range(10)]

# Define bunkers
bunker_matrix = {}
bunker_width, bunker_height = 50, 30
bunker_block_size = 10
for i in range(4):
    bunker_x = i * (width // 4) + (width // 8) - bunker_width // 2
    bunker_y = height - 120
    for y in range(bunker_y, bunker_y + bunker_height, bunker_block_size):
        for x in range(bunker_x, bunker_x + bunker_width, bunker_block_size):
            bunker_matrix[(x, y)] = True

bullets = []
bullet_speed = 7

clock = pygame.time.Clock()

game_over = False

# Function to reset the game
def reset_game():
    global player_x, enemies, bullets, game_over, bunker_matrix
    player_x = width // 2 - player_width // 2
    enemies = [{'rect': pygame.Rect(j * 50 + 20, i * 30 + 20, 40, 20), 'speed': 1, 'drop': False} for i in range(5) for j in range(10)]
    bullets = []
    game_over = False
    # Reset bunkers
    bunker_matrix.clear()
    for i in range(4):
        bunker_x = i * (width // 4) + (width // 8) - bunker_width // 2
        bunker_y = height - 120
        for y in range(bunker_y, bunker_y + bunker_height, bunker_block_size):
            for x in range(bunker_x, bunker_x + bunker_width, bunker_block_size):
                bunker_matrix[(x, y)] = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE] and len(bullets) < 3:
            bullets.append(pygame.Rect(player_x + player_width // 2 - 2, player_y, 4, 10))

        # Update bullet positions
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)
            else:
                # Check for bullet collision with bunkers
                bullet_hit = None
                for bunker_block in bunker_matrix.keys():
                    if bullet.colliderect(pygame.Rect(*bunker_block, bunker_block_size, bunker_block_size)):
                        bullet_hit = bunker_block
                        break
                if bullet_hit:
                    bullets.remove(bullet)
                    del bunker_matrix[bullet_hit]

        # Update enemy positions and check for collision with bullets
        for enemy in enemies[:]:
            if enemy['drop']:
                enemy['rect'].y += 10
                enemy['drop'] = False
            else:
                enemy['rect'].x += enemy['speed']
                if enemy['rect'].left < 0 or enemy['rect'].right > width:
                    enemy['speed'] *= -1
                    enemy['drop'] = True
            for bullet in bullets[:]:
                if bullet.colliderect(enemy['rect']):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

        # Check for game over conditions
        if any(enemy['rect'].y + enemy['rect'].height >= player_y for enemy in enemies):
            game_over = True

    else:
        # Display the game over message and prompt for restart
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 74)
        text = font.render('GAME OVER', True, RED)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
        restart_text = font.render('Press Space to Restart', True, WHITE)
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + text.get_height()))
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            reset_game()

    # Drawing everything
    if not game_over:
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))
        for bunker_block in bunker_matrix.keys():
            pygame.draw.rect(screen, GREEN, (*bunker_block, bunker_block_size, bunker_block_size))
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy['rect'])
        pygame.display.flip()

    clock.tick(30)  # Cap the game at 30 fps
## [@ Flames CO 2023-24 [C]]
