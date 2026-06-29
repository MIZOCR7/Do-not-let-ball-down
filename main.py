import pygame

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Do not let ball down")

collosion_line_color = (226, 155, 73)

def background(screen):
  background_img = pygame.image.load("assets/background.jpg").convert_alpha()
  background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

  pipe_image = pygame.image.load('assets/pipe.png').convert_alpha()
  pipe_image = pygame.transform.scale(pipe_image, (200,300))
  pipe_image = pygame.transform.flip(pipe_image, flip_x=False, flip_y=True)
  
  box_image = pygame.image.load('assets/box.png').convert_alpha()
  box_image = pygame.transform.scale(box_image, (200,100))
  
  screen.blit(background_img, (0,0))
  screen.blit(pipe_image, (50,-100))
  screen.blit(box_image, (100,100))
  pygame.draw.line(screen, (255,0,0), (0,500), (800,500), width=1)
  pygame.display.update() 

  





def main():
  
  background(screen)
  
  run = True
  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          run = False
          
  pygame.quit()

if __name__ == "__main__":
  main()
