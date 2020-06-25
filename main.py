import pygame
import random
import time

pygame.font.init()

FRAME = 30
WIDTH = 1200
HEIGHT = 800
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Meteor properties
INITIAL_Y_LOC = 10
METEOR_MAX_SPEED = 5
INITIAL_NUM_METEOR = 8
SHIP_SPEED = 10
MAX_CYCLES = 1000
NEW_METEOR_INTERVAL = 40


class GameObject:
    def __init__(self):
        pass

    def load_image(self, filename, ship=False):
        scale = (100, 100) if ship else (30, 30)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, scale).convert()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def rect(self):
        """
        Generate a rectangle representing the object locations
        :return: pygame.rect
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        """
        draw the gamme object that x, y location
        :return:
        """
        self.game.display.blit(self.image, (self.x, self.y))


class Starship(GameObject):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.x = WIDTH / 2
        self.y = HEIGHT - 40
        self.load_image('starship.png', ship=True)

    def move_left(self):
        self.x = self.x - SHIP_SPEED
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x = self.x + SHIP_SPEED
        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width

    def move_up(self):
        self.y -= SHIP_SPEED
        if self.y < 0:
            self.y = 0

    def move_down(self):
        self.y += SHIP_SPEED
        if self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height

    def __str__(self):
        return f"Starship ({self.x}, {self.y})"


class Meteor(GameObject):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.x = random.randint(0, WIDTH)
        self. y = INITIAL_Y_LOC
        self.speed = random.randint(0, METEOR_MAX_SPEED)
        self.load_image("meteor.png")

    def move_down(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 5

    def __str__(self):
        return f"Meteor ({self.x}, {self.y})"


class Game:
    """
    represent the game itself in the while loop to play
    """
    def __init__(self):
        print("Starting game...")
        pygame.init()

        # setup the display
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invader")
        # ingame timing
        self.clock = pygame.time.Clock()
        # set up ship
        self.starship = Starship(self)
        # set up meteors
        self.meteors = [Meteor(self) for _ in range(INITIAL_NUM_METEOR)]

    def _collision_check(self):
        # result = False
        for meteor in self.meteors:
            if self.starship.rect().colliderect(meteor.rect()):
                # result = True
                # break
                return True
        return False

    def _display_message(self, message):
        font = pygame.font.SysFont("comicsansms", 48)
        text_surface = font.render(message, True, BLUE, WHITE)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (WIDTH / 2, HEIGHT / 2)
        self.display.fill(WHITE)
        self.display.blit(text_surface, text_rectangle)

    def play(self):
        run = True
        collided = False
        cycle = 0
        score = 0
        # main game loop
        while run and not collided:
            # indicates game loop
            cycle += 1

            if cycle == MAX_CYCLES:
                self._display_message("You've Won!")
                run = False

            # check events in pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                    elif event.key == pygame.K_LEFT:
                        self.starship.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.starship.move_right()
                    elif event.key == pygame.K_UP:
                        self.starship.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.starship.move_down()

            # move meteors
            for meteor in self.meteors:
                meteor.move_down()
            # clear display
            self.display.fill(BLACK)

            self.starship.draw()
            for meteor in self.meteors:
                meteor.draw()

            if self._collision_check():
                collided = True
                self._display_message(f"You lost! Score: {score}")

            if cycle % NEW_METEOR_INTERVAL == 0:
                self.meteors.append(Meteor(self))

            # display score
            score += 1 if cycle % 10 == 0 else 0
            font = pygame.font.SysFont("comicsansms", 30)
            msg = font.render(f"Score: {score}", True, BLUE)
            self.display.blit(msg, (30, 30))

            # update the display
            pygame.display.update()

            # set frame rates
            self.clock.tick(FRAME)

        time.sleep(1)
        pygame.quit()


def main():
    game = Game()
    game.play()
    print("Game Over")


if __name__ == "__main__":
    main()
