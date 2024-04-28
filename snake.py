import pygame,sys,random
from pygame.math import Vector2
import pygame.mixer

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.has_moved = True #Kiểm soát thay đổi hướng

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
        self.has_moved = True
    def change_direction(self,new_direction):
        if self.has_moved:
            if new_direction.x * self.direction.x + new_direction.y * self.direction.y == 0:
                self.direction = new_direction
                self.has_moved = False # Cập nhật để ngăn thay đổi hướng lập tức

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_pos = (int(self.pos.x * cell_size) + cell_size // 2, int(self.pos.y * cell_size) + cell_size // 2)
        pygame.draw.circle(screen, (255, 0, 0), fruit_pos, cell_size // 2)

    def randomize(self):
        self.pos = Vector2(random.randint(0, cell_number_w - 1), random.randint(0, cell_number_h - 1))


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.fruit.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_board(self):
        for x in range(cell_number_w):
            for y in range(cell_number_h):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                if (x + y) % 2 == 0:
                    pygame.draw.rect(screen, (171,225,51), rect)
                else:
                    pygame.draw.rect(screen, (173,234,39), rect)


    def draw_elements(self):
        self.draw_board()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            eat_sound.play()
            self.score += 1

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))  

    def play_background_sound(self):
        pygame.mixer.music.load("sound/SYA.wav")
        pygame.mixer.music.play(-1)


    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number_w or not 0 <= self.snake.body[0].y < cell_number_h:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()


    def game_over(self):
        pygame.mixer.music.stop()
        self.is_game_over = True
        self.snake.reset()
        self.fruit.randomize()
        self.score = 0
        self.play_background_sound()
          


# Game Setup
pygame.init()
width = 800
height = 600
cell_size = 40
cell_number_w = width // cell_size
cell_number_h = height // cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
background_sound = pygame.mixer.Sound("sound/SYA.wav")
eat_sound = pygame.mixer.Sound("sound/tiengnhai.wav")
main_game = MAIN()

# Game Loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.change_direction(Vector2(0,-1))
            elif event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.change_direction(Vector2(1,0))
            elif event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.change_direction(Vector2(0,1))
            elif event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.change_direction(Vector2(-1,0))
            elif event.key == pygame.K_ESCAPE:  # Thêm Nút escape để thoát game khỏi mắc công click chu
                pygame.quit()
                sys.exit()
  #  screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)

