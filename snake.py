import pygame,sys,random
from pygame.math import Vector2
import pygame.mixer

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
    
        self.head_up=pygame.image.load('Images/head_up.png').convert_alpha()
        self.head_down=pygame.image.load('Images/head_down.png').convert_alpha()
        self.head_right=pygame.image.load('Images/head_right.png').convert_alpha()
        self.head_left=pygame.image.load('Images/head_left.png').convert_alpha()
    
        self.tail_up=pygame.image.load('Images/tail_up.png').convert_alpha()
        self.tail_down=pygame.image.load('Images/tail_down.png').convert_alpha()
        self.tail_right=pygame.image.load('Images/tail_right.png').convert_alpha()
        self.tail_left=pygame.image.load('Images/tail_left.png').convert_alpha()
    
        self.body_vertical=pygame.image.load('Images/body_vertical.png').convert_alpha()
        self.body_horizontal=pygame.image.load('Images/body_horizontal.png').convert_alpha()
    
        self.body_tr=pygame.image.load('Images/body_tr.png').convert_alpha()
        self.body_tl=pygame.image.load('Images/body_tl.png').convert_alpha()
        self.body_br=pygame.image.load('Images/body_br.png').convert_alpha()
        self.body_bl=pygame.image.load('Images/body_bl.png').convert_alpha()



    
    def draw_snake(self):

        self.update_head_images()
        self.update_tail_images()

        for index, block in enumerate (self.body):
            #1
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            #2
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x== -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                            screen.blit(self.body_tl,block_rect)
                    elif previous_block.x== -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                            screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y== -1 or previous_block.y== -1 and next_block.x == 1:
                            screen.blit(self.body_tr,block_rect)
                    elif previous_block.x== 1 and next_block.y== 1 or previous_block.y == 1 and next_block.x==1:
                            screen.blit(self.body_br,block_rect)
     


    def update_head_images(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_images(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down   



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
        fruit_image = pygame.image.load("Images/fruit.png")
        fruit_rect = fruit_image.get_rect(topleft=(self.pos.x * cell_size, self.pos.y * cell_size))
        screen.blit(fruit_image, fruit_rect)


    def randomize(self):
        self.pos = Vector2(random.randint(0, cell_number_w - 1), random.randint(0, cell_number_h - 1))


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = 0
        self.highest_score = 0
        self.background_sound = pygame.mixer.Sound("sound/SYA.wav")
        self.eat_sound = pygame.mixer.Sound("sound/tiengnhai.wav")
        self.die_sound = pygame.mixer.Sound("sound/die.wav")
        self.background_sound.play(-1)

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
        self.draw_highest_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.eat_sound.play()
            self.score += 1
            if self.score > self.highest_score: 
                self.highest_score = self.score 


    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(str(self.score), True, (255, 255, 255))
        
        fruit_image = pygame.image.load("Images/fruit.png")
        fruit_rect = fruit_image.get_rect(topleft=(10, 10))
        
        score_x = fruit_rect.right + 10
        score_y = fruit_rect.centery - score_text.get_height() // 2
             
        screen.blit(fruit_image, fruit_rect)
        screen.blit(score_text, (score_x, score_y))
 

    def draw_highest_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"{self.highest_score}", True, (255, 255, 255))
        
        trophy_image = pygame.image.load("Images/trophy.png") 
        trophy_rect = trophy_image.get_rect(topright=(770, 12)) 
        
        screen.blit(trophy_image, trophy_rect) 
        screen.blit(score_text, (width - 30, 20))


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
        self.die_sound.play()
        self.snake.reset()
        self.fruit.randomize()
        self.score = 0

          


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
die_sound = pygame.mixer.Sound("sound/die.wav")
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
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
  #  screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)

