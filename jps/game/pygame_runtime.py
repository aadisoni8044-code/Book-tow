import os
import sys
import time
from typing import TextIO, Optional
import pygame

from ..runtime.environment import Environment, BoxObject


class PygameRuntime:
    """Pygame-based 2D Engine for JPS Script rendering and interactive logic."""

    def __init__(self, env: Environment, output_stream: TextIO = sys.stdout):
        self.env = env
        self.output_stream = output_stream
        self.dragging_box: Optional[BoxObject] = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def run(self):
        pygame.init()

        width, height = self.env.game_size
        flags = pygame.DOUBLEBUF

        screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption("JPS Script 2D Runtime Engine")

        clock = pygame.time.Clock()
        running = True

        print(f"[JPS Engine] 2D Window initialized ({width}x{height})", file=self.output_stream)
        self.output_stream.flush()

        # Is headless driver?
        is_headless = os.environ.get("SDL_VIDEODRIVER") == "dummy"

        # Limit frame iterations in headless test mode
        frame_count = 0
        max_frames = 10 if is_headless else float("inf")

        while running and frame_count < max_frames:
            frame_count += 1
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mx, my = event.pos
                        # Check interactive boxes (switch.box enabled or all boxes)
                        for box in reversed(self.env.boxes):
                            if box.is_switch:
                                rect = pygame.Rect(box.x, box.y, box.width, box.height)
                                if rect.collidepoint(mx, my):
                                    self.dragging_box = box
                                    self.drag_offset_x = mx - box.x
                                    self.drag_offset_y = my - box.y
                                    break

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging_box = None

                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging_box:
                        mx, my = event.pos
                        self.dragging_box.x = mx - self.drag_offset_x
                        self.dragging_box.y = my - self.drag_offset_y

            # Physics & Movement update for run.box()
            for box in self.env.boxes:
                if box.is_running and box != self.dragging_box:
                    box.x += box.dx
                    box.y += box.dy

                    # Bounce off screen boundaries
                    if box.x <= 0:
                        box.x = 0
                        box.dx *= -1
                    elif box.x + box.width >= width:
                        box.x = max(0, width - box.width)
                        box.dx *= -1

                    if box.y <= 0:
                        box.y = 0
                        box.dy *= -1
                    elif box.y + box.height >= height:
                        box.y = max(0, height - box.height)
                        box.dy *= -1

            # Render background
            screen.fill((18, 22, 32))  # Dark navy studio background

            # Draw grid lines for game environment aesthetic
            grid_color = (28, 36, 52)
            for x in range(0, width, 50):
                pygame.draw.line(screen, grid_color, (x, 0), (x, height), 1)
            for y in range(0, height, 50):
                pygame.draw.line(screen, grid_color, (0, y), (width, y), 1)

            # Draw Box Objects
            for box in self.env.boxes:
                rect = pygame.Rect(int(box.x), int(box.y), int(box.width), int(box.height))

                # Box shadow
                shadow_rect = pygame.Rect(int(box.x) + 4, int(box.y) + 4, int(box.width), int(box.height))
                pygame.draw.rect(screen, (10, 12, 18), shadow_rect, border_radius=6)

                # Box Body
                color = box.color if not box.is_running else (0, 230, 180)  # Cyan -> Mint green if active
                if box == self.dragging_box:
                    color = (255, 180, 0)  # Amber when dragging

                pygame.draw.rect(screen, color, rect, border_radius=6)
                pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=6)

                # Status label
                if pygame.font.get_init():
                    font = pygame.font.SysFont("Consolas", 14, bold=True)
                    label = f"Box #{box.id} ({int(box.width)}x{int(box.height)})"
                    text_surf = font.render(label, True, (20, 20, 20))
                    text_rect = text_surf.get_rect(center=rect.center)
                    screen.blit(text_surf, text_rect)

            pygame.display.flip()

        pygame.quit()
        print("[JPS Engine] 2D Runtime closed.", file=self.output_stream)
        self.output_stream.flush()
