# Import libraries
import pygame
import sys
import math

# Class to represent a celestial object
class CelestialObject:
    def __init__(self, mass, x, y, vx, vy, color, radius):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius

    def update_position(self, time_step):
        self.x += self.vx * time_step
        self.y += self.vy * time_step

# Class to represent the gravitational system
class GravitationalSystem:
    def __init__(self, system):
        self.objects = system
        self.G = 6.674 * (10 ** -11)

    def calculate_gravitational_force(self, obj1, obj2):
        dx = obj2.x - obj1.x
        dy = obj2.y - obj1.y
        distance = math.sqrt(dx**2 + dy**2)
        force_magnitude = (self.G * obj1.mass * obj2.mass) / distance**2
        angle = math.atan2(dy, dx)
        force_x = force_magnitude * math.cos(angle)
        force_y = force_magnitude * math.sin(angle)
        return force_x, force_y

    def update_velocities(self, time_step):
        for i in range(len(self.objects)):
            for j in range(len(self.objects)):
                if i != j:
                    force_x, force_y = self.calculate_gravitational_force(self.objects[i], self.objects[j])
                    acceleration_x = force_x / self.objects[i].mass
                    acceleration_y = force_y / self.objects[i].mass
                    self.objects[i].vx += acceleration_x * time_step
                    self.objects[i].vy += acceleration_y * time_step

# Class to manage events
class EventManager:
    def __init__(self, scale_factor):
        self.offset_x, self.offset_y = 0, 0
        self.current_scale_factor = scale_factor
        self.mouse_button_pressed = False
        self.initial_mouse_x, self.initial_mouse_y = 0, 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_left_click()
                elif event.button == 4:
                    self.handle_scroll_up()
                elif event.button == 5:
                    self.handle_scroll_down()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.handle_left_release()

    def handle_left_click(self):
        self.initial_mouse_x, self.initial_mouse_y = pygame.mouse.get_pos()
        self.mouse_button_pressed = True

    def handle_scroll_up(self):
        self.current_scale_factor *= 1.1

    def handle_scroll_down(self):
        self.current_scale_factor /= 1.1

    def handle_left_release(self):
        self.mouse_button_pressed = False

    def handle_mouse_drag(self):
        if self.mouse_button_pressed:
            current_mouse_x, current_mouse_y = pygame.mouse.get_pos()
            self.offset_x -= current_mouse_x - self.initial_mouse_x
            self.offset_y -= current_mouse_y - self.initial_mouse_y
            self.initial_mouse_x, self.initial_mouse_y = current_mouse_x, current_mouse_y

# Class to manage the simulation
class Simulation:
    def __init__(self, system, time_step):
        self.system = GravitationalSystem(system)
        self.time_step = time_step

    def update_objects_positions(self):
        for obj in self.system.objects:
            obj.update_position(self.time_step)

# Class to manage the main window
class MainWindow:
    def __init__(self, width, height, fps, window_name, system, time_step, scale_factor):
        self.width = width
        self.height = height
        self.fps = fps
        self.window_name = window_name
        self.simulation = Simulation(system, time_step)
        self.event_manager = EventManager(scale_factor)

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.window_name)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.event_manager.handle_events()

            self.simulation.system.update_velocities(self.simulation.time_step)
            self.simulation.update_objects_positions()
            self.event_manager.handle_mouse_drag()

            self.draw_objects()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def translate_coordinates(self, obj):
        translated_x = obj.x // self.event_manager.current_scale_factor + self.width // 2 - self.event_manager.offset_x
        translated_y = obj.y // self.event_manager.current_scale_factor + self.height // 2 - self.event_manager.offset_y
        return translated_x, translated_y

    def draw_objects(self):
        self.screen.fill((0, 0, 0))
        for obj in self.simulation.system.objects:
            pygame.draw.circle(self.screen, obj.color, self.translate_coordinates(obj), obj.radius)


def main():

    # Window parameters
    SIZE_WIDTH = 800
    SIZE_HEIGHT = 600
    FPS = 30
    WINDOW_NAME = "Gravitational trajectory simulator"
    SCALE_FACTOR = 100e8

    # Simulation parameters
    TIME_STEP = 100 * 86400
    SYSTEM = [
        CelestialObject(1.989e30, 0, 0, 0, 0, (255, 255, 0), 20),
        CelestialObject(3.285e23, 5.791e10, 0, 0, 47000, (200, 200, 200), 3),
        CelestialObject(4.867e24, 1.082e11, 0, 0, 35000, (255, 165, 0), 4),
        CelestialObject(5.972e24, 1.496e11, 0, 0, 30000, (0, 0, 255), 5),
        CelestialObject(6.39e23, 2.279e11, 0, 0, 24000, (255, 0, 0), 4),
        CelestialObject(1.898e27, 7.786e11, 0, 0, 13000, (255, 69, 0), 15),
        CelestialObject(5.683e26, 1.429e12, 0, 0, 10000, (255, 215, 0), 12),
        CelestialObject(8.681e25, 2.871e12, 0, 0, 6800, (173, 216, 230), 8),
        CelestialObject(1.024e26, 4.495e12, 0, 0, 5400, (0, 0, 128), 8)
    ]

    # Launch the window and simulation
    main_window = MainWindow(SIZE_WIDTH, SIZE_HEIGHT, FPS, WINDOW_NAME, SYSTEM, TIME_STEP, SCALE_FACTOR)
    main_window.run()

if __name__ == "__main__":
    main()
