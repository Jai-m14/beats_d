import pygame
from config import WIDTH, HEIGHT, MARGIN, GOAL_WIDTH, GOAL_THICKNESS

class Field:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.margin = MARGIN
        self.goal_width = GOAL_WIDTH
        self.goal_thickness = GOAL_THICKNESS
        self.field_rect = pygame.Rect(MARGIN, MARGIN, WIDTH-2*MARGIN, HEIGHT-2*MARGIN)

    def draw(self, screen):
        grass_color = (30, 100, 30)
        line_color = (0, 255, 236)
        goal_color_left = (180, 180, 255)
        goal_color_right = (255, 180, 180)
        #screen.fill(grass_color)
        pygame.draw.rect(screen, line_color, self.field_rect, 5)
        pygame.draw.line(screen, line_color, (self.width//2, self.margin), (self.width//2, self.height-self.margin), 2)
        pygame.draw.circle(screen, line_color, (self.width//2, self.height//2), 60, 2)
        pygame.draw.rect(screen, line_color, (self.margin, self.height//2-self.goal_width//2-30, 48, self.goal_width+60), 2)
        pygame.draw.rect(screen, line_color, (self.width-self.margin-48, self.height//2-self.goal_width//2-30, 48, self.goal_width+60), 2)
        pygame.draw.rect(screen, goal_color_left, (self.margin, self.height//2-self.goal_width//2, self.goal_thickness, self.goal_width))
        pygame.draw.rect(screen, goal_color_right, (self.width-self.margin-self.goal_thickness, self.height//2-self.goal_width//2, self.goal_thickness, self.goal_width))

    def draw_strobe_segment(self, screen, contact_point, ball_radius):
        strobe_color = (255, 20, 50)
        thickness = 5
        x, y = contact_point
        start_pos = (x - ball_radius*0.8, y)
        end_pos = (x + ball_radius*0.8, y)
        pygame.draw.line(screen, strobe_color, start_pos, end_pos, thickness)
