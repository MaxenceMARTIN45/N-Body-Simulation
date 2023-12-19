import pygame
import sys
import math

# Constantes
G = 6.674 * (10 ** -11)  # Constante gravitationnelle
SCALE_FACTOR_LINEAR = 100e8  # Facteur d'échelle pour la simulation
SCALE_FACTOR_NONLINEAR = 20
SCALE_FACTOR_LOG = 20

# Classe pour représenter un objet céleste
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

# Fonction pour calculer la force gravitationnelle entre deux objets
def calculate_gravitational_force(obj1, obj2):
    dx = obj2.x - obj1.x
    dy = obj2.y - obj1.y
    distance = math.sqrt(dx**2 + dy**2)
    force_magnitude = (G * obj1.mass * obj2.mass) / distance**2
    angle = math.atan2(dy, dx)
    force_x = force_magnitude * math.cos(angle)
    force_y = force_magnitude * math.sin(angle)
    return force_x, force_y

# Fonction pour mettre à jour les vitesses des objets en fonction des forces gravitationnelles
def update_velocities(objects, time_step):
    for i in range(len(objects)):
        for j in range(len(objects)):
            if i != j:
                force_x, force_y = calculate_gravitational_force(objects[i], objects[j])
                acceleration_x = force_x / objects[i].mass
                acceleration_y = force_y / objects[i].mass
                objects[i].vx += acceleration_x * time_step
                objects[i].vy += acceleration_y * time_step

def cartesian_to_polar(x, y):
    """Convert Cartesian coordinates to polar coordinates."""
    radius = math.sqrt(x**2 + y**2)
    angle = math.atan2(y, x)
    return radius, angle

def polar_to_cartesian(radius, angle):
    """Convert polar coordinates to Cartesian coordinates."""
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return x, y

def translate_coordinates(obj, width, height, scale_factor = SCALE_FACTOR_LINEAR):
    """Translate object coordinates to the center of the screen."""
    translated_x = int(obj.x / scale_factor) + width // 2
    translated_y = int(obj.y / scale_factor) + height // 2
    return translated_x, translated_y

def translate_coordinates_log(obj, width, height, scale_factor = SCALE_FACTOR_LOG):
    """Translate object coordinates to the center of the screen."""
    radius,angle = cartesian_to_polar(obj.x,obj.y)
    radius = math.log10(radius + 1)
    x,y = polar_to_cartesian(radius,angle)
    translated_x = int(x * scale_factor) + width // 2
    translated_y = int(y * scale_factor) + height // 2
    return translated_x, translated_y

def nonlinear_translate_coordinates(obj, width, height, x_scale_factor=SCALE_FACTOR_NONLINEAR, y_scale_factor=SCALE_FACTOR_NONLINEAR):
    """Translate object coordinates to the center of the screen with nonlinear scaling."""
    if obj.x < 0:
        translated_x = int(-math.log10(abs(obj.x) + 1) * x_scale_factor) + width // 2
    else:
        translated_x = int(math.log10(abs(obj.x) + 1) * x_scale_factor) + width // 2
    if obj.y < 0:
        translated_y = int(-math.log10(abs(obj.y) + 1) * y_scale_factor) + height // 2
    else:
        translated_y = int(math.log10(abs(obj.y) + 1) * y_scale_factor) + height // 2
    return translated_x, translated_y

def translate_coordinates_nonlinear(obj, width, height, factor=1.0):
    """Translate object coordinates to the center of the screen with nonlinear scaling."""
    distance = math.sqrt(obj.x ** 2 + obj.y ** 2)
    scaled_distance = math.log(distance + 1) * factor
    angle = math.atan2(obj.y, obj.x)
    translated_x = int(scaled_distance * math.cos(angle)) + width // 2
    translated_y = int(scaled_distance * math.sin(angle)) + height // 2
    return translated_x, translated_y

# Fonction principale pour exécuter la simulation
def run_simulation():

    # Initialisation des objets
    sun = CelestialObject(1.989e30, 0, 0, 0, 0, (255, 255, 0), 20)
    mercury = CelestialObject(3.285e23, 5.791e10, 0, 0, 47000, (200, 200, 200), 3)
    venus = CelestialObject(4.867e24, 1.082e11, 0, 0, 35000, (255, 165, 0), 4)
    earth = CelestialObject(5.972e24, 1.496e11, 0, 0, 30000, (0, 0, 255), 5)
    mars = CelestialObject(6.39e23, 2.279e11, 0, 0, 24000, (255, 0, 0), 4)
    jupiter = CelestialObject(1.898e27, 7.786e11, 0, 0, 13000, (255, 69, 0), 15)
    saturn = CelestialObject(5.683e26, 1.429e12, 0, 0, 10000, (255, 215, 0), 12)
    uranus = CelestialObject(8.681e25, 2.871e12, 0, 0, 6800, (173, 216, 230), 8)
    neptune = CelestialObject(1.024e26, 4.495e12, 0, 0, 5400, (0, 0, 128), 8)

    # Liste des objets célestes
    list_of_celestial_objects = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    # Paramètres de la simulation
    time_step = 100*86400  # en secondes (86 400 s = 1 j)
    time_scale = 24  # échelle de temps (une heure dans la simulation = time_scale secondes)

    # Initialisation de Pygame
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Simulateur de Trajectoire Gravitationnelle")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mise à jour des positions et vitesses des objets
        update_velocities(list_of_celestial_objects, time_step)
        for obj in list_of_celestial_objects:
            obj.update_position(time_step)

        # Affichage des objets
        screen.fill((0, 0, 0))
        for object in list_of_celestial_objects:
            pygame.draw.circle(screen, object.color, translate_coordinates_log(object, width, height), object.radius)

        pygame.display.flip()
        clock.tick(30)  # Limiter la vitesse d'affichage
    
if __name__ == "__main__":
    run_simulation()
