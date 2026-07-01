import pygame
import random
import math

pygame.init()
pygame.font.init()

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
pipe_image = pygame.transform.scale(pipe_image, (200, 300))
pipe_image = pygame.transform.flip(pipe_image, flip_x=False, flip_y=True)

box_image = pygame.image.load('assets/box.png').convert_alpha()
box_image = pygame.transform.scale(box_image, (270, 130))

def draw_background(screen):
    screen.blit(background_img, (0, 0))
    screen.blit(pipe_image, (50, -100))
    screen.blit(box_image, (500, 372))
    pygame.draw.line(screen, collosion_line_color, (0, 500), (800, 500), width=1)

class Physics():
    def __init__(self):
        self.gravity = 0.25
        self.balls_list = []
        self.lines_list = []
        self.drawing = False

        self.game_started = False
        self.balls_to_spawn = 60
        self.spawn_delay = 14
        self.spawn_timer = 0
        self.player_won = False

        self.COLORS = {
            "white": (255, 255, 255), "red": (255, 60, 60), "green": (60, 255, 60),
            "blue": (60, 60, 255), "yellow": (255, 255, 60), "cyan": (60, 255, 255),
            "magenta": (255, 60, 255), "orange": (255, 165, 0), "coral": (255, 127, 80),
            "tomato": (255, 99, 71), "lime": (0, 255, 0), "sky_blue": (135, 206, 235),
            "pink": (255, 192, 203), "hot_pink": (255, 105, 180), "gold": (255, 215, 0)
        }

        self.box_walls = [
            ((512, 385), (512, 494)),
            ((758, 385), (758, 494)),
            ((512, 494), (758, 494))
        ]

    def spawn_single_ball(self):
        if self.balls_to_spawn <= 0:
            return
        PIPE_X = 50
        PIPE_Y = -100
        PIPE_WIDTH = 200
        PIPE_HEIGHT = 300

        ball_data = {
            "x": random.randint(PIPE_X + 25, PIPE_X + PIPE_WIDTH - 25),
            "y": PIPE_Y + PIPE_HEIGHT - 5,
            "radius": random.randint(6, 11),
            "color": random.choice(list(self.COLORS.values())),
            "x_vel": random.uniform(1.5, 3.5),
            "y_vel": random.uniform(0.1, 1.0)
        }
        self.balls_list.append(ball_data)
        self.balls_to_spawn -= 1

    def draw(self, screen):
        for line in self.lines_list:
            if len(line) > 1:
                pygame.draw.lines(screen, (40, 40, 40), False, line, width=6)

        for x in range(516, 754, 15):
            pygame.draw.line(screen, (255, 0, 0), (x, 410), (x + 8, 410), width=3)

        for ball in self.balls_list:
            pygame.draw.circle(screen, ball["color"], (int(ball["x"]), int(ball["y"])), ball["radius"])

        if self.player_won:
            font = pygame.font.SysFont("Arial", 60, bold=True)
            win_text = font.render("YOU WIN!", True, (0, 230, 0))
            shadow_text = font.render("YOU WIN!", True, (0, 40, 0))
            screen.blit(shadow_text, (WIDTH//2 - win_text.get_width()//2 + 3, HEIGHT // 2 - 50 + 3))
            screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT // 2 - 50))

    def move(self):
        if not self.game_started:
            return

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_single_ball()
            self.spawn_timer = 0

        for ball in self.balls_list:
            ball["y_vel"] += self.gravity
            ball["x"] += ball["x_vel"]
            ball["y"] += ball["y_vel"]

            if ball["y"] + ball["radius"] >= 500:
                ball["y"] = 500 - ball["radius"]
                ball["y_vel"] = -ball["y_vel"] * 0.2
                ball["x_vel"] *= 0.7

            if ball["x"] - ball["radius"] <= 0:
                ball["x"] = ball["radius"]
                ball["x_vel"] = -ball["x_vel"] * 0.5
            elif ball["x"] + ball["radius"] >= 800:
                ball["x"] = 800 - ball["radius"]
                ball["x_vel"] = -ball["x_vel"] * 0.5

            for p1, p2 in self.box_walls:
                line_dx = p2[0] - p1[0]
                line_dy = p2[1] - p1[1]
                line_len_sq = line_dx**2 + line_dy**2
                if line_len_sq == 0:
                    continue

                t = ((ball["x"] - p1[0]) * line_dx + (ball["y"] - p1[1]) * line_dy) / line_len_sq
                t = max(0, min(1, t))

                proj_x = p1[0] + t * line_dx
                proj_y = p1[1] + t * line_dy

                dist_vec_x = ball["x"] - proj_x
                dist_vec_y = ball["y"] - proj_y
                distance = math.sqrt(dist_vec_x**2 + dist_vec_y**2)

                if distance < ball["radius"] + 2:
                    if distance == 0:
                        continue
                    dist_vec_x /= distance
                    dist_vec_y /= distance

                    ball["x"] = proj_x + dist_vec_x * (ball["radius"] + 2)
                    ball["y"] = proj_y + dist_vec_y * (ball["radius"] + 2)

                    dot_product = ball["x_vel"] * dist_vec_x + ball["y_vel"] * dist_vec_y
                    ball["x_vel"] = (ball["x_vel"] - 2 * dot_product * dist_vec_x) * 0.15
                    ball["y_vel"] = (ball["y_vel"] - 2 * dot_product * dist_vec_y) * 0.15

            for line in self.lines_list:
                for idx in range(len(line) - 1):
                    p1 = line[idx]
                    p2 = line[idx+1]

                    line_dx = p2[0] - p1[0]
                    line_dy = p2[1] - p1[1]
                    line_len_sq = line_dx**2 + line_dy**2
                    if line_len_sq == 0:
                        continue

                    t = ((ball["x"] - p1[0]) * line_dx + (ball["y"] - p1[1]) * line_dy) / line_len_sq
                    t = max(0, min(1, t))

                    proj_x = p1[0] + t * line_dx
                    proj_y = p1[1] + t * line_dy

                    dist_vec_x = ball["x"] - proj_x
                    dist_vec_y = ball["y"] - proj_y
                    distance = math.sqrt(dist_vec_x**2 + dist_vec_y**2)

                    if distance < ball["radius"] + 3:
                        if distance == 0:
                            continue
                        dist_vec_x /= distance
                        dist_vec_y /= distance

                        ball["x"] = proj_x + dist_vec_x * (ball["radius"] + 3)
                        ball["y"] = proj_y + dist_vec_y * (ball["radius"] + 3)

                        dot_product = ball["x_vel"] * dist_vec_x + ball["y_vel"] * dist_vec_y
                        ball["x_vel"] = (ball["x_vel"] - 2 * dot_product * dist_vec_x) * 0.3
                        ball["y_vel"] = (ball["y_vel"] - 2 * dot_product * dist_vec_y) * 0.3
                        ball["x_vel"] += line_dx * 0.008

        for i in range(len(self.balls_list)):
            for j in range(i + 1, len(self.balls_list)):
                b1 = self.balls_list[i]
                b2 = self.balls_list[j]

                dx = b2['x'] - b1['x']
                dy = b2['y'] - b1['y']
                distance = math.sqrt(dx**2 + dy**2)
                min_dist = b1['radius'] + b2['radius']

                if distance < min_dist:
                    if distance == 0:
                        distance = 0.1
                    overlap = min_dist - distance

                    nx = dx / distance
                    ny = dy / distance

                    b1['x'] -= nx * overlap * 0.5
                    b1['y'] -= ny * overlap * 0.5
                    b2['x'] += nx * overlap * 0.5
                    b2['y'] += ny * overlap * 0.5

                    kx = b1['x_vel'] - b2['x_vel']
                    ky = b1['y_vel'] - b2['y_vel']
                    p = 2 * (nx * kx + ny * ky) / 2

                    b1['x_vel'] -= p * nx * 0.2
                    b1['y_vel'] -= p * ny * 0.2
                    b2['x_vel'] += p * nx * 0.2
                    b2['y_vel'] += p * ny * 0.2

        balls_inside_target_zone = 0
        for ball in self.balls_list:
            if 515 < ball['x'] < 755:
                if 410 < ball['y'] < 494:
                    if abs(ball['y_vel']) < 0.4 and abs(ball['x_vel']) < 0.4:
                        balls_inside_target_zone += 1

        if balls_inside_target_zone >= 12:
            self.player_won = True

def main():
    physics_engine = Physics()

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
                if event.button == 1:
                    physics_engine.drawing = True
                    physics_engine.lines_list.append([mouse_pos])
                    if not physics_engine.game_started:
                        physics_engine.game_started = True

            if event.type == pygame.MOUSEMOTION:
                if physics_engine.drawing:
                    if physics_engine.lines_list[-1][-1] != event.pos:
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
