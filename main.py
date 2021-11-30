import pygame,sys,random
from pygame.math import Vector2

class FRUIT:
    def __init__(self):
        self.x=random.randint(0,cell_number-1)
        self.y=random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        #pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.check = False

        self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('sound/Sound_crunch.wav')
        self.gameover = pygame.image.load('graphics/download.jfif').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else :
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                if previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                if (previous_block == Vector2(-1,0) and next_block == Vector2(0,1)) or (previous_block == Vector2(0,1) and next_block == Vector2(-1,0)):
                    screen.blit(self.body_bl,block_rect)
                if (previous_block == Vector2(1,0) and next_block == Vector2(0,1)) or (previous_block == Vector2(0,1) and next_block == Vector2(1,0)):
                    screen.blit(self.body_br,block_rect)
                if (previous_block == Vector2(0,-1) and next_block == Vector2(-1,0)) or (previous_block == Vector2(-1,0) and next_block == Vector2(0,-1)):
                    screen.blit(self.body_tl,block_rect)
                if (previous_block == Vector2(1,0) and next_block == Vector2(0,-1)) or (previous_block == Vector2(0,-1) and next_block == Vector2(1,0)):
                    screen.blit(self.body_tr,block_rect)

    def update_head_graphics(self):
        self.update_head = self.body[1] - self.body[0]
        if self.update_head == Vector2(1,0):
            self.head = self.head_left
        if self.update_head == Vector2(-1,0):
            self.head = self.head_right
        if self.update_head == Vector2(0,1):
            self.head = self.head_up
        if self.update_head == Vector2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):
        self.update_tail = self.body[len(self.body)-2] - self.body[len(self.body)-1]
        if self.update_tail == Vector2(1,0):
            self.tail = self.tail_left
        if self.update_tail == Vector2(-1,0):
            self.tail = self.tail_right
        if self.update_tail == Vector2(0,1):
            self.tail = self.tail_up
        if self.update_tail == Vector2(0,-1):
            self.tail = self.tail_down


    def move_snake(self):
        if self.check == False:
          body_copy = self.body[:-1]
          body_copy.insert(0,body_copy[0] + self.direction)
          self.body = body_copy[:]
        else :
          body_copy = self.body[:]
          body_copy.insert(0, body_copy[0] + self.direction)
          self.body = body_copy[:]
          self.check = False

    def add_block(self):
        self.check = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(10, 10),Vector2(11,10),Vector2(12,10)]
        self.direction = Vector2(0, 0)
        self.gameover_rect = self.gameover.get_rect(center = (400,400))
        screen.blit(self.gameover,self.gameover_rect)



class MAIN:
    def __init__(self):
     self.snake = SNAKE()
     self.fruit = FRUIT()

    def update(self):
     self.snake.move_snake()
     self.check_collision()

    def draw_elements(self):
     self.draw_grass()
     self.fruit.draw_fruit()
     self.snake.draw_snake()
     self.draw_score()

    def check_collision(self):
     if self.fruit.pos == self.snake.body[0]:
      self.snake.add_block()
      self.fruit.randomize()
      self.snake.play_crunch_sound()

     for block in self.snake.body[1:]:
         if block == self.fruit.pos:
             self.fruit.randomize()

    def check_fail(self):
      for block in self.snake.body[1:]:
          if block == self.snake.body[0]:
             self.snake.reset()
             self.fruit.pos = Vector2(9,10)

      if self.snake.body[0].x < 0 or self.snake.body[0].x >= cell_number:
          self.snake.reset()
          self.fruit.pos = Vector2(9, 10)

      if self.snake.body[0].y < 0 or self.snake.body[0].y >= cell_number:
          self.snake.reset()
          self.fruit.pos = Vector2(9, 10)

    def draw_grass(self):
        for row in range(cell_number):
            for col in range(cell_number):
                if row % 2 == 0:
                    if col % 2 == 0:
                        self.rectangle = pygame.Rect(row * cell_size,col * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,(167,209,61),self.rectangle)
                else:
                    if col % 2 == 1:
                        self.rectangle = pygame.Rect(row * cell_size, col * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, (167, 209, 61), self.rectangle)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 40
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size=40
cell_number=20
screen= pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
clock= pygame.time.Clock()
apple = pygame.image.load('graphics/apple.png').convert_alpha()
game_font = pygame.font.Font(None,25)

main_game = MAIN()


while True:
    for event in pygame.event.get():
     if event.type==pygame.QUIT:
        pygame.quit()
        sys.exit()
     if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_UP:
             if main_game.snake.direction.y != +1:
              main_game.snake.direction = Vector2(0,-1)
         if event.key == pygame.K_DOWN:
             if main_game.snake.direction.y != -1:
              main_game.snake.direction = Vector2(0, 1)
         if event.key == pygame.K_RIGHT:
             if main_game.snake.direction.x != -1:
              main_game.snake.direction = Vector2(1, 0)
         if event.key == pygame.K_LEFT:
             if main_game.snake.direction.x != +1:
              main_game.snake.direction = Vector2(-1, 0)
    screen.fill((175, 215, 70))
    main_game.update()
    main_game.draw_elements()
    main_game.check_fail()
    pygame.display.update()
    clock.tick(8)