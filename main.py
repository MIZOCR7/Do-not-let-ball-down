import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 60

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Do not let ball down")

collosion_line_color = (226, 155, 73)

background_img = pygame.image.load("assets/background.jpg").convert_alpha()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
pipe_image = pygame.image.load('assets/pipe.png').convert_alpha()
pipe_image = pygame.transform.scale(pipe_image, (200,300))
pipe_image = pygame.transform.flip(pipe_image, flip_x=False, flip_y=True)

box_image = pygame.image.load('assets/box.png').convert_alpha()
box_image = pygame.transform.scale(box_image, (250,150))

def draw_background(screen):
  screen.blit(background_img, (0,0))
  screen.blit(pipe_image, (50,-100))
  screen.blit(box_image, (500,370))
  pygame.draw.line(screen, collosion_line_color, (0,500), (800,500), width=1)
   

  
class Physics():
  def __init__(self):
    self.gravity = 0.75
    self.y_vel = 14
    self.direction = 1
    self.balls_list = []
    self.lines_list = []
    self.drawing = False
    self.COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (128, 128, 128),
    "light_gray": (211, 211, 211),
    "dark_gray": (64, 64, 64),

    "orange": (255, 165, 0),
    "dark_orange": (255, 140, 0),
    "coral": (255, 127, 80),
    "salmon": (250, 128, 114),
    "tomato": (255, 99, 71),

    "brown": (139, 69, 19),
    "chocolate": (210, 105, 30),
    "tan": (210, 180, 140),
    "beige": (245, 245, 220),

    "lime": (0, 255, 0),
    "dark_green": (0, 100, 0),
    "forest_green": (34, 139, 34),
    "olive": (128, 128, 0),
    "sea_green": (46, 139, 87),
    "mint": (152, 255, 152),

    "navy": (0, 0, 128),
    "royal_blue": (65, 105, 225),
    "sky_blue": (135, 206, 235),
    "light_blue": (173, 216, 230),
    "deep_sky_blue": (0, 191, 255),
    "turquoise": (64, 224, 208),
    "teal": (0, 128, 128),

    "purple": (128, 0, 128),
    "violet": (238, 130, 238),
    "indigo": (75, 0, 130),
    "lavender": (230, 230, 250),
    "plum": (221, 160, 221),

    "pink": (255, 192, 203),
    "hot_pink": (255, 105, 180),
    "deep_pink": (255, 20, 147),
    "rose": (255, 0, 127),

    "gold": (255, 215, 0),
    "goldenrod": (218, 165, 32),
    "khaki": (240, 230, 140),

    "silver": (192, 192, 192),
    "ivory": (255, 255, 240),
    "snow": (255, 250, 250),
}
  
  def making_balls(self):
    for _ in range(50):
      PIPE_X = 50
      PIPE_Y = -100
      PIPE_WIDTH = 200
      PIPE_HEIGHT = 300
      
      ball_data = {
        "x": random.randint(PIPE_X + 10, PIPE_X + PIPE_WIDTH - 10),
        "y": PIPE_Y + PIPE_HEIGHT - 5,
        "radius" : random.randint(5, 12),
        "color" : random.choice(list(self.COLORS.values())),
        'x_vel' : random.uniform(-2,3),
        "y_vel": random.uniform(0, 2)
      }
      
      self.balls_list.append(ball_data)
  
  def draw(self, screen):
    for ball in self.balls_list:
      pygame.draw.circle(screen, ball["color"], (int(ball["x"]), int(ball["y"])), ball["radius"])
    
    for line in self.lines_list:
      if len(line) > 1:
        pygame.draw.lines(screen, (0,0,0), False, line, width=5)
  
  def move(self):
    for ball in self.balls_list:
      ball["y_vel"] += self.gravity 
      ball["x"] += ball["x_vel"]     
      ball["y"] += ball["y_vel"]
      
      if ball["y"] + ball["radius"] >= 500:
        ball["y"] = 500 - ball["radius"]       
        ball["y_vel"] = -ball["y_vel"] * 0.6   
      
      if ball["x"] - ball["radius"] <= 0:
        ball["x"] = ball["radius"]             
        ball["x_vel"] = -ball["x_vel"]         
    
      elif ball["x"] + ball["radius"] >= 800:
        ball["x"] = 800 - ball["radius"]      
        ball["x_vel"] = -ball["x_vel"]


def main():
  
  physics_engine = Physics()
  physics_engine.making_balls()
  
  
  run = True
  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          run = False
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        physics_engine.drawing = True
        physics_engine.lines_list.append([mouse_pos])
      if event.type == pygame.MOUSEMOTION:
        if physics_engine.drawing:
          physics_engine.lines_list[-1].append(event.pos)
      if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          physics_engine.drawing = False
      
    physics_engine.move() 
    draw_background(screen)
    physics_engine.draw(screen)
    pygame.display.update()
  pygame.quit()

if __name__ == "__main__":
  main()
