# Import libraries
import pygame
import sys
import math
import random

# Class to represent a celestial object
class CelestialObject:
    def __init__(self, mass, x, y, vx, vy, density, color):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.density = density
        self.real_radius = self.calculate_real_radius()
        self.color = color
        self.display_radius = self.calculate_display_radius()

    def calculate_real_radius(self):
        return ((3 * self.mass) / (4 * math.pi * self.density))**(1/3)

    def calculate_display_radius(self):
        # We simply apply a transformation that reduces the real radius to a reasonable display radius
        return math.log(self.real_radius)**5//100000

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

# # Class to manage the simulation
# class Simulation:
#     def __init__(self, system, time_step):
#         self.system = GravitationalSystem(system)
#         self.time_step = time_step

#     def update_objects_positions(self):
#         for obj in self.system.objects:
#             obj.update_position(self.time_step)

# Class to manage the simulation
class Simulation:
    def __init__(self, system, time_step):
        self.system = GravitationalSystem(system)
        self.time_step = time_step

    def update_objects_positions(self):
        for i in range(len(self.system.objects)):
            obj = self.system.objects[i]
            obj.update_position(self.time_step)

            # Check for collisions with other objects
            for j in range(len(self.system.objects)):
                if i != j:
                    other_obj = self.system.objects[j]
                    distance = math.sqrt((obj.x - other_obj.x)**2 + (obj.y - other_obj.y)**2)
                    min_distance = obj.real_radius + other_obj.real_radius

                    if distance < min_distance:
                        # Collision occurred, merge the two objects
                        merged_obj = self.merge_objects(obj, other_obj)
                        self.system.objects[i] = merged_obj
                        self.system.objects.pop(j)
                        break

    def merge_objects(self, obj1, obj2):
        # Calculate the new mass and velocity after merging
        new_mass = obj1.mass + obj2.mass
        new_velocity_x = (obj1.mass * obj1.vx + obj2.mass * obj2.vx) / new_mass
        new_velocity_y = (obj1.mass * obj1.vy + obj2.mass * obj2.vy) / new_mass

        # Choose the position of the more massive object
        if obj1.mass >= obj2.mass:
            new_x, new_y = obj1.x, obj1.y
        else:
            new_x, new_y = obj2.x, obj2.y

        # Calculate the new density based on the merged mass and real radius
        new_density = (obj1.density * obj1.real_radius**3 + obj2.density * obj2.real_radius**3) / (new_mass * (new_radius**3))

        # Use the color of the more massive object
        new_color = obj1.color if obj1.mass >= obj2.mass else obj2.color

        # Create a new CelestialObject with the merged properties
        merged_obj = CelestialObject(new_mass, new_x, new_y, new_velocity_x, new_velocity_y, new_density, new_color)

        return merged_obj


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
            pygame.draw.circle(self.screen, obj.color, self.translate_coordinates(obj), obj.display_radius)

# Class to generate a system of N bodies randomly
class SystemGenerator:
    def __init__(self, num_bodies, zero_speed_initialization):
        self.num_bodies = num_bodies
        self.zero_speed_initialization = zero_speed_initialization

    def generate_system(self):
        system = []
        min_mass, max_mass = 1e20, 1e30
        min_position, max_position = -1e14, 1e14
        min_density, max_density = 500,10000
        if self.zero_speed_initialization:
            min_velocity, max_velocity = 0, 0
        else:
            min_velocity, max_velocity = -1e3, 1e3

        for _ in range(self.num_bodies):
            mass = random.uniform(min_mass, max_mass)
            x = random.uniform(min_position, max_position)
            y = random.uniform(min_position, max_position)
            vx = random.uniform(min_velocity, max_velocity)
            vy = random.uniform(min_velocity, max_velocity)
            density = random.uniform(min_density, max_density)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            system.append(CelestialObject(mass, x, y, vx, vy, density, color))
        return system


def main():

    # Window parameters
    SIZE_WIDTH = 800
    SIZE_HEIGHT = 600
    FPS = 30
    WINDOW_NAME = "Gravitational trajectory simulator"
    
    # Simulation parameters
    TIME_STEP = 100 * 86400

    # Choose either the solar system or a random system with n bodies
    use_solar_system = False

    # If use_solar_system = False
    num_bodies = 100
    zero_speed_initialization = True
    if use_solar_system:
        SCALE_FACTOR = 10e9
    else:
        SCALE_FACTOR = 10e11

    if use_solar_system:
        SYSTEM = [
            CelestialObject(mass=1.989e30, x=0, y=0, vx=0, vy=0, density=1410, color="yellow"),  # Soleil
            CelestialObject(mass=3.285e23, x=5.7e10, y=0, vx=0, vy=4.7e4, density=5427, color="gray"),  # Mercure
            CelestialObject(mass=4.867e24, x=1.1e11, y=0, vx=0, vy=3.5e4, density=5243, color="orange"),  # Venus
            CelestialObject(mass=5.972e24, x=1.5e11, y=0, vx=0, vy=2.98e4, density=5514, color="blue"),  # Terre
            CelestialObject(mass=6.39e23, x=2.2e11, y=0, vx=0, vy=2.4e4, density=3933, color="red"),  # Mars
            CelestialObject(mass=1.898e27, x=7.7e11, y=0, vx=0, vy=1.3e4, density=1326, color="orange"),  # Jupiter
            CelestialObject(mass=5.683e26, x=1.4e12, y=0, vx=0, vy=9.7e3, density=687, color="gold"),  # Saturne
            CelestialObject(mass=8.681e25, x=2.8e12, y=0, vx=0, vy=6.8e3, density=1271, color="lightblue"),  # Uranus
            CelestialObject(mass=1.024e26, x=4.5e12, y=0, vx=0, vy=5.4e3, density=1638, color="blue"),  # Neptune
            CelestialObject(mass=1.309e22, x=5.9e12, y=0, vx=0, vy=4.7e3, density=2095, color="brown"),  # Pluton
        ]

    else:
        system_generator = SystemGenerator(num_bodies, zero_speed_initialization)
        SYSTEM = system_generator.generate_system()

    # Launch the window and simulation
    main_window = MainWindow(SIZE_WIDTH, SIZE_HEIGHT, FPS, WINDOW_NAME, SYSTEM, TIME_STEP, SCALE_FACTOR)
    main_window.run()

if __name__ == "__main__":
    main()
