from random import randrange

import pygame

#
# from classes.Apple import Apple
# from classes.Snake import Snake

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 14

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый клас от которого наследуются игровые объекты"""

    def __init__(self, body_color: tuple = None):
        self.position: tuple = (320, 240)
        self.body_color: tuple = body_color

    def draw(self):
        """Абстрактный метод отрисовки"""
        pass


class Apple(GameObject):
    """Класс описывающий яблоко и действия с ним"""

    def __init__(self, body_color: tuple = (255, 0, 0)):
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        """Метод Рандомизации позиции"""

        self.position = (randrange(0, 620, 20), randrange(0, 480, 20))

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_apple_position(self):
        return self.position


class Snake(GameObject):
    """Класс логики змейки"""

    def __init__(self, position: tuple = (320, 240), body_color: tuple = (0, 255, 0)):
        super().__init__(body_color)
        self.position = position
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.last = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


    def get_head_position(self):
        return self.positions[0]

    def move(self):

        if self.positions[0] in self.positions[1:]:
            return False

        if self.next_direction:
            self.direction = self.next_direction

        new_head_x = (self.positions[0][0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (self.positions[0][1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        self.positions.insert(0, (new_head_x, new_head_y))

        self.last = self.positions[-1]

        if len(self.positions) > self.length:
            del self.positions[-1]

        return True

    def reset(self):
        self.positions = []
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)
        self.next_direction = None

    def get_positions(self):
        return self.positions

    def draw(self):

        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake((320, 240))
    apple = Apple(APPLE_COLOR)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if apple.get_apple_position() == snake.get_head_position():
            apple.randomize_position()
            snake.length += 1
        clock.tick(SPEED)
        handle_keys(snake)
        if not snake.move():
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()
            snake.reset()

        snake.draw()
        # print(snake.length)
        apple.draw()
        # apple.randomize_position()
        # print(1)

        pygame.display.update()


if __name__ == '__main__':
    main()
