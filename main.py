import pygame
import sys
import random
import math

class Food(pygame.sprite.Sprite):
    # Constructor - used to create objects of the class
    def __init__(self, x, y):
        super(Food, self).__init__()
        self.radius = random.randint(3, 7)
        # all classes inheriting from the sprite class must have an attribute self.image
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))

    def relocate(self):
        self.rect.center = (random.randint(0, 800), random.randint(0, 600))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Enemy, self).__init__()
        self.radius = 20
        # all classes inheriting from the sprite class must have an attribute self.image
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ENEMY, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
        valid_nums = list(range(-3, 0)) + list(range(1, 3))
        self.deltax = random.choice(valid_nums)
        self.deltay = random.choice(valid_nums)

    def move(self):
        if self.rect.left < -500 or self.rect.right > 1300:
            self.deltax *= -1
        if self.rect.top < -500 or self.rect.bottom > 1100:
            self.deltay *= -1

        # Adjust speed inversely proportional to size
        speed_factor = max(0.5, 100 / self.radius)
        adjusted_deltax = self.deltax * speed_factor
        adjusted_deltay = self.deltay * speed_factor

        self.rect.centerx += adjusted_deltax
        self.rect.centery += adjusted_deltay

    def collision(self, other):
        if math.dist(self.rect.center, other.rect.center) < (self.radius + other.radius):
            if self.radius >= other.radius:
                self.radius += int(other.radius * .5)
                self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(self.image, ENEMY, (self.radius, self.radius), self.radius)
                self.rect = self.image.get_rect(center=self.rect.center)
                other.kill()
            else:
                other.radius += int(self.radius * .5)
                other.image = pygame.Surface((other.radius * 2, other.radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(other.image, ENEMY, (other.radius, other.radius), other.radius)
                other.rect = other.image.get_rect(center=other.rect.center)
                self.kill()

class Player(Enemy):
    def __init__(self, x, y):
        super(Player, self).__init__(x, y)
        self.radius = 20
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PURPLE, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))

    def input(self):
        speed_factor = max(0.5, 100 / self.radius)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.centery -= 5 * speed_factor
        if keys[pygame.K_s]:
            self.rect.centery += 5 * speed_factor
        if keys[pygame.K_a]:
            self.rect.centerx -= 5 * speed_factor
        if keys[pygame.K_d]:
            self.rect.centerx += 5 * speed_factor

    def move(self):
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.rect.centerx, my - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0:
            speed_factor = max(0.5, 100 / self.radius)
            dx, dy = dx / distance, dy / distance
            self.rect.centerx += dx * speed_factor
            self.rect.centery += dy * speed_factor
        

    def collision(self, enemys):
        for enemy in enemys:
            if math.dist(self.rect.center, enemy.rect.center) < (self.radius + enemy.radius):
                if self.radius >= enemy.radius:
                    self.radius += int(enemy.radius * 0.5)
                    self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(self.image, PURPLE, (self.radius, self.radius), self.radius)
                    self.rect = self.image.get_rect(center=self.rect.center)
                    enemy.kill()
                else:
                    print("Game Over: Player was eaten!")
                    player.kill()
                    pygame.quit()
                    sys.exit()
            
# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Tutorial")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = "#800080"
RED = (255, 0, 0)
BLACK = (0, 0, 0)
ENEMY = (0, 255, 255, 100)

# Create clock to later control frame rate
clock = pygame.time.Clock()

food = pygame.sprite.Group()
for i in range(50):
    food.add(Food(random.randint(0, 800), random.randint(0, 600)))

num_players = 1
enemys = pygame.sprite.Group()
for i in range(10):
    enemys.add(Enemy(random.randint(0, 800), random.randint(0, 600)))
    num_players += 1

player = Player(screen_width // 2, screen_height // 2)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():  # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    screen.fill(WHITE)

    new_food = []
    player.move()
    player.collision(enemys)

    for enemy in enemys:
        enemy.move()
        for food_item in food:
            if math.dist(enemy.rect.center, food_item.rect.center) < (enemy.radius + food_item.radius):
                enemy.radius += 1
                enemy.image = pygame.Surface((enemy.radius * 2, enemy.radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(enemy.image, ENEMY, (enemy.radius, enemy.radius), enemy.radius)
                enemy.rect = enemy.image.get_rect(center=enemy.rect.center)
                food_item.kill()
                new_food.append(Food(random.randint(0, 800), random.randint(0, 600)))
                
        for other_enemy in enemys:
            if enemy != other_enemy:
                enemy.collision(other_enemy)
                num_players -= 1
                
    for food_item in food:
        if math.dist(player.rect.center, food_item.rect.center) < (player.radius + food_item.radius):
            player.radius += int(food_item.radius * 0.5)
            player.image = pygame.Surface((player.radius * 2, player.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(player.image, PURPLE, (player.radius, player.radius), player.radius)
            player.rect = player.image.get_rect(center=player.rect.center)
            food_item.kill()
            new_food.append(Food(random.randint(0, 800), random.randint(0, 600)))

    food.add(new_food)

    # Draw sprites on the screen
    food.draw(screen)
    enemys.draw(screen)
    screen.blit(player.image, player.rect)

    if player.radius > 400:
        print("Player Wins!")
        running = False

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

    

pygame.quit()
sys.exit()