import pygame
import random
from datetime import datetime

pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 1400, 900
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

# Road and Lane Dimensions
ROAD_WIDTH = 180
HALF_ROAD_WIDTH = ROAD_WIDTH // 2  # 90
LANE_COUNT_PER_HALF = 2
LANE_WIDTH = HALF_ROAD_WIDTH // LANE_COUNT_PER_HALF  # 90 // 2 = 45
# Offset from road center (e.g. CENTER_X) to center of each lane
LANE_OFFSET_1 = LANE_WIDTH // 2  # 45 // 2 = 22
LANE_OFFSET_2 = LANE_WIDTH + LANE_OFFSET_1 # 45 + 22 = 67
STOP_LINE_OFFSET = 110  # How far from center cars should stop

# Colors
COLOR_GRASS = (34, 139, 34)
COLOR_ROAD = (50, 50, 50)
COLOR_LANE_LINE = (100, 100, 100)
COLOR_DASHED_LINE = (255, 255, 255)
COLOR_STOP_LINE = (255, 255, 255)

# Vehicle Specifications (Size, Speeds, Colors)
# Speeds are now [max_speed, acceleration, deceleration]
VEHICLE_SPECS = {
    "AUTO": {
        "size": (25, 40), "color": (255, 200, 0),
        "speed": [2.5, 0.08, 0.25]
    },
    "CAR": {
        "size": (30, 50), "color": random.choice([(200, 0, 0), (0, 100, 200), (100, 100, 100)]),
        "speed": [3.0, 0.1, 0.3]
    },
    "BIKE": {
        "size": (20, 35), "color": (50, 50, 50),
        "speed": [3.5, 0.12, 0.35]
    },
    "BUS": {
        "size": (35, 70), "color": (200, 50, 50),
        "speed": [2.8, 0.05, 0.2]
    },
    "TRUCK": {
        "size": (35, 65), "color": (80, 60, 40),
        "speed": [2.0, 0.04, 0.15]
    },
    "AMBULANCE": {
        "size": (30, 50), "color": (255, 255, 255),
        "speed": [4.5, 0.15, 0.4]
    }
}

# Simulation Settings
FPS = 60
GREEN_LIGHT_DURATION = 15  # seconds
YELLOW_LIGHT_DURATION = 3   # seconds
SPAWN_RATE_PER_SECOND = 0.5 # Avg vehicles per second


# --- Vehicle Class ---
class Vehicle:
    """Represents a single vehicle in the simulation."""

    def __init__(self, vid, x, y, direction, vtype, lane):
        self.id = vid
        self.x = x
        self.y = y
        self.direction = direction
        self.type = vtype
        self.lane = lane  # 0 or 1
        self.passed = False

        # Get specs from constant
        specs = VEHICLE_SPECS[vtype]
        
        size = specs["size"] # (width across lane, length along lane)
        self.vehicle_width = size[0] # The vehicle's physical width
        self.length = size[1] # The vehicle's physical length
        self.color = specs["color"] if vtype != "CAR" else random.choice([(200, 0, 0), (0, 100, 200), (100, 100, 100)])
        
        self.max_speed, self.accel, self.decel = specs["speed"]
        self.speed = 0  # Start from stationary
        
        # Adjust dimensions for drawing based on direction
        if self.direction in ["NORTH", "SOUTH"]:
            self.width, self.height = self.vehicle_width, self.length
        else: # EAST, WEST
            self.width, self.height = self.length, self.vehicle_width

    def get_rect(self):
        """Returns the pygame.Rect for this vehicle."""
        return pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)

    def control_speed(self, signal_state, vehicle_ahead):
        """Calculates and applies acceleration or deceleration."""
        
        # Check 1: Is there a vehicle ahead and are we too close?
        stop_for_vehicle = False
        if vehicle_ahead:
            # Calculate distance to vehicle in front
            if self.direction == "NORTH":
                dist = self.y - vehicle_ahead.y - (self.height / 2) - (vehicle_ahead.height / 2)
            elif self.direction == "SOUTH":
                dist = vehicle_ahead.y - self.y - (self.height / 2) - (vehicle_ahead.height / 2)
            elif self.direction == "EAST":
                dist = vehicle_ahead.x - self.x - (self.width / 2) - (vehicle_ahead.width / 2)
            else:  # WEST
                dist = self.x - vehicle_ahead.x - (self.width / 2) - (vehicle_ahead.width / 2)
            
            # Safe stopping distance is dynamic based on speed
            safe_dist = max(10, self.speed * 10) # Simple formula: 10px + buffer for speed
            if dist < safe_dist:
                stop_for_vehicle = True

        # Check 2: Should we stop for the traffic signal?
        stop_for_signal = False
        if self.type != "AMBULANCE" and signal_state in ["RED", "YELLOW"]:
            if self.direction == "NORTH" and STOP_LINE_OFFSET + 20 < self.y - CENTER_Y < STOP_LINE_OFFSET + 80:
                stop_for_signal = True
            elif self.direction == "SOUTH" and -STOP_LINE_OFFSET - 80 < self.y - CENTER_Y < -STOP_LINE_OFFSET - 20:
                stop_for_signal = True
            elif self.direction == "EAST" and -STOP_LINE_OFFSET - 80 < self.x - CENTER_X < -STOP_LINE_OFFSET - 20:
                stop_for_signal = True
            elif self.direction == "WEST" and STOP_LINE_OFFSET + 20 < self.x - CENTER_X < STOP_LINE_OFFSET + 80:
                stop_for_signal = True

        # --- Final Speed Adjustment ---
        if stop_for_vehicle or stop_for_signal:
            # Need to stop, apply deceleration
            self.speed = max(0, self.speed - self.decel)
        else:
            # Clear to go, apply acceleration
            self.speed = min(self.max_speed, self.speed + self.accel)

    def move(self):
        """Moves the vehicle based on its current speed and direction."""
        if self.direction == "NORTH": self.y -= self.speed
        elif self.direction == "SOUTH": self.y += self.speed
        elif self.direction == "EAST": self.x += self.speed
        else: self.x -= self.speed

    def update(self, signal_state, vehicle_ahead):
        """Main update call for the vehicle."""
        self.control_speed(signal_state, vehicle_ahead)
        self.move()

    def draw(self, surface):
        """Draws the vehicle on the screen."""
        rect = self.get_rect()
        pygame.draw.rect(surface, self.color, rect, border_radius=3)
        
        # Special drawing for Ambulance
        if self.type == "AMBULANCE":
            light_color = (255, 0, 0) if (pygame.time.get_ticks() // 300) % 2 == 0 else (255, 255, 255)
            pygame.draw.circle(surface, light_color, (int(self.x), int(self.y)), 5)
        
        # Draw brake lights if stopped
        if self.speed < 0.1:
            if self.direction == "NORTH":
                pygame.draw.rect(surface, (255, 0, 0), (rect.left + 2, rect.bottom - 4, self.width - 4, 3))
            elif self.direction == "SOUTH":
                pygame.draw.rect(surface, (255, 0, 0), (rect.left + 2, rect.top + 1, self.width - 4, 3))
            elif self.direction == "EAST":
                pygame.draw.rect(surface, (255, 0, 0), (rect.left + 1, rect.top + 2, 3, self.height - 4))
            else: # WEST
                pygame.draw.rect(surface, (255, 0, 0), (rect.right - 4, rect.top + 2, 3, self.height - 4))


# --- TrafficSignal Class ---
class TrafficSignal:
    """Controls a single traffic light."""

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.state = "RED"
        self.vehicles_passed = 0
        self.vehicles_waiting = 0

    def draw(self, surface):
        """Draws the signal pole and lights."""
        pygame.draw.rect(surface, (40, 40, 40), (self.x - 12, self.y - 55, 24, 65), border_radius=4)
        colors = {"RED": (255, 0, 0), "YELLOW": (255, 255, 0), "GREEN": (0, 255, 0), "OFF": (80, 80, 0)}
        
        for i, state in enumerate(["RED", "YELLOW", "GREEN"]):
            color = colors[state] if self.state == state else \
                    (80, 0, 0) if state == "RED" else \
                    colors["OFF"] if state == "YELLOW" else (0, 80, 0)
            pygame.draw.circle(surface, color, (self.x, self.y - 40 + i * 18), 7)


# --- Intersection Class ---
class Intersection:
    """Manages the entire simulation, including signals, vehicles, and drawing."""

    def __init__(self):
        # Lane positions [Lane 0, Lane 1]
        # (Assuming Right-Hand Traffic)
        self.lane_positions = {
            "NORTH": [CENTER_X + LANE_OFFSET_1, CENTER_X + LANE_OFFSET_2], # Right side
            "SOUTH": [CENTER_X - LANE_OFFSET_1, CENTER_X - LANE_OFFSET_2], # Left side
            "EAST": [CENTER_Y + LANE_OFFSET_1, CENTER_Y + LANE_OFFSET_2],  # Bottom side
            "WEST": [CENTER_Y - LANE_OFFSET_1, CENTER_Y - LANE_OFFSET_2]   # Top side
        }
        
        # Signal positions
        self.signals = {d: TrafficSignal(x, y) for d, (x, y) in {
            "NORTH": (CENTER_X - ROAD_WIDTH / 2 - 20, CENTER_Y - ROAD_WIDTH / 2),
            "SOUTH": (CENTER_X + ROAD_WIDTH / 2 + 20, CENTER_Y + ROAD_WIDTH / 2),
            "EAST": (CENTER_X + ROAD_WIDTH / 2, CENTER_Y - ROAD_WIDTH / 2 - 20),
            "WEST": (CENTER_X - ROAD_WIDTH / 2, CENTER_Y + ROAD_WIDTH / 2 + 20)
        }.items()}
        
        self.signal_cycle = ["NORTH", "EAST", "SOUTH", "WEST"]
        self.current_signal_index = 0
        self.signal_timer = 0
        self.signal_state = "GREEN"  # Current state (GREEN, YELLOW)
        self.frame_count = 0
        
        # Vehicles stored by [direction][lane_id]
        self.vehicles = {d: {0: [], 1: []} for d in self.signal_cycle}
        self.vehicle_id_counter = 0
        
        # Statistics
        self.total_spawned = 0
        self.total_passed = 0
        self.spawn_timer = 0

    def spawn_vehicle(self, direction=None):
        """Spawns a new vehicle in a random lane for a given direction."""
        direction = direction or random.choice(self.signal_cycle)
        vtype = random.choices(["AUTO", "CAR", "BIKE", "BUS", "TRUCK", "AMBULANCE"], 
                               weights=[30, 35, 25, 5, 3, 2])[0]
        lane_id = random.choice([0, 1])
        
        # Get spawn coordinates
        if direction == "NORTH":
            x, y = self.lane_positions[direction][lane_id], HEIGHT + 100
        elif direction == "SOUTH":
            x, y = self.lane_positions[direction][lane_id], -100
        elif direction == "EAST":
            x, y = -100, self.lane_positions[direction][lane_id]
        else: # WEST
            x, y = WIDTH + 100, self.lane_positions[direction][lane_id]
        
        new_vehicle = Vehicle(self.vehicle_id_counter, x, y, direction, vtype, lane_id)
        
        # Check if spawn point is clear (prevent overlapping spawns)
        if self.vehicles[direction][lane_id]:
            last_vehicle = self.vehicles[direction][lane_id][-1]
            if direction == "NORTH" and last_vehicle.y > HEIGHT - 50: return
            if direction == "SOUTH" and last_vehicle.y < -50: return
            if direction == "EAST" and last_vehicle.x < -50: return
            if direction == "WEST" and last_vehicle.x > WIDTH + 50: return

        self.vehicles[direction][lane_id].append(new_vehicle)
        self.vehicle_id_counter += 1
        self.total_spawned += 1

    def update_signals(self):
        """Updates the state of all traffic signals based on timers."""
        self.frame_count += 1
        if self.frame_count < FPS:
            return  # Only update timer once per second
            
        self.frame_count = 0
        self.signal_timer += 1
        
        # State machine for signal cycle
        if self.signal_state == "GREEN" and self.signal_timer >= GREEN_LIGHT_DURATION:
            self.signal_state = "YELLOW"
            self.signal_timer = 0
        elif self.signal_state == "YELLOW" and self.signal_timer >= YELLOW_LIGHT_DURATION:
            self.signal_state = "GREEN"
            self.signal_timer = 0
            # Move to the next direction in the cycle
            self.current_signal_index = (self.current_signal_index + 1) % len(self.signal_cycle)
        
        # Update all signal objects
        current_green_dir = self.signal_cycle[self.current_signal_index]
        for d in self.signal_cycle:
            if d == current_green_dir:
                self.signals[d].state = self.signal_state
            else:
                self.signals[d].state = "RED"

    def update_vehicles(self):
        """Updates all vehicles on the road."""
        for direction in self.signal_cycle:
            signal_state = self.signals[direction].state
            waiting_count = 0
            
            for lane_id in [0, 1]:
                # Iterate on a copy [:] to allow safe removal
                for i, v in enumerate(self.vehicles[direction][lane_id][:]):
                    
                    # Find the vehicle directly in front
                    vehicle_ahead = self.vehicles[direction][lane_id][i - 1] if i > 0 else None
                    
                    v.update(signal_state, vehicle_ahead)
                    
                    if v.speed < 0.1 and not v.passed:
                        waiting_count += 1
                    
                    # Check if vehicle has passed the intersection
                    if not v.passed:
                        passed_checks = {
                            "NORTH": v.y < CENTER_Y - ROAD_WIDTH, "SOUTH": v.y > CENTER_Y + ROAD_WIDTH,
                            "EAST": v.x > CENTER_X + ROAD_WIDTH, "WEST": v.x < CENTER_X - ROAD_WIDTH
                        }
                        if passed_checks[direction]:
                            v.passed = True
                            self.total_passed += 1
                            self.signals[direction].vehicles_passed += 1
                    
                    # Remove vehicles that are far off-screen
                    remove_checks = {
                        "NORTH": v.y < -200, "SOUTH": v.y > HEIGHT + 200,
                        "EAST": v.x > WIDTH + 200, "WEST": v.x < -200
                    }
                    if remove_checks[direction]:
                        self.vehicles[direction][lane_id].remove(v)
                        
            self.signals[direction].vehicles_waiting = waiting_count

    def update(self):
        """Main simulation update step."""
        self.update_signals()
        self.update_vehicles()
        
        # Randomly spawn vehicles
        self.spawn_timer += 1
        if self.spawn_timer >= (FPS / SPAWN_RATE_PER_SECOND):
            self.spawn_timer = 0
            if random.random() < 0.75: # 75% chance to spawn
                self.spawn_vehicle()

    def draw_roads(self, surface):
        """Draws the grass, roads, and lane markings."""
        surface.fill(COLOR_GRASS)
        
        # Main road rects
        road_rect_v = pygame.Rect(CENTER_X - ROAD_WIDTH / 2, 0, ROAD_WIDTH, HEIGHT)
        road_rect_h = pygame.Rect(0, CENTER_Y - ROAD_WIDTH / 2, WIDTH, ROAD_WIDTH)
        pygame.draw.rect(surface, COLOR_ROAD, road_rect_v)
        pygame.draw.rect(surface, COLOR_ROAD, road_rect_h)
        
        # Lane lines (solid edge, dashed center)
        # Vertical road
        pygame.draw.line(surface, COLOR_LANE_LINE, (road_rect_v.left, 0), (road_rect_v.left, HEIGHT), 2)
        pygame.draw.line(surface, COLOR_LANE_LINE, (road_rect_v.right, 0), (road_rect_v.right, HEIGHT), 2)
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(surface, COLOR_DASHED_LINE, (CENTER_X, y), (CENTER_X, y + 20), 4)
            
        # Horizontal road
        pygame.draw.line(surface, COLOR_LANE_LINE, (0, road_rect_h.top), (WIDTH, road_rect_h.top), 2)
        pygame.draw.line(surface, COLOR_LANE_LINE, (0, road_rect_h.bottom), (WIDTH, road_rect_h.bottom), 2)
        for x in range(0, WIDTH, 40):
            pygame.draw.line(surface, COLOR_DASHED_LINE, (x, CENTER_Y), (x + 20, CENTER_Y), 4)
            
        # Draw Zebra Crossings (Stop Lines)
        crossing_width = ROAD_WIDTH / 2 - 10
        for i in range(0, int(crossing_width / 8)):
            x_off = road_rect_v.left + 5 + i * 8
            y_off = road_rect_h.top + 5 + i * 8
            # NORTH
            pygame.draw.rect(surface, COLOR_STOP_LINE, (x_off, CENTER_Y - STOP_LINE_OFFSET, 4, 15))
            # SOUTH
            pygame.draw.rect(surface, COLOR_STOP_LINE, (road_rect_v.right - 5 - 4 - i * 8, CENTER_Y + STOP_LINE_OFFSET - 15, 4, 15))
            # EAST
            pygame.draw.rect(surface, COLOR_STOP_LINE, (CENTER_X + STOP_LINE_OFFSET - 15, y_off, 15, 4))
            # WEST
            pygame.draw.rect(surface, COLOR_STOP_LINE, (CENTER_X - STOP_LINE_OFFSET, road_rect_h.bottom - 5 - 4 - i * 8, 15, 4))

    def draw_ui(self, surface):
        """Draws the statistics and info panel."""
        px, py, pw = 10, 10, 330
        
        # Create a semi-transparent surface
        ui_panel = pygame.Surface((pw, 600), pygame.SRCALPHA)
        ui_panel.fill((0, 0, 0, 180))  # Black with 180/255 transparency
        surface.blit(ui_panel, (px, py))
        
        # Border
        pygame.draw.rect(surface, (100, 100, 255), (px, py, pw, 600), 3, border_radius=5)
        
        # Fonts
        font_title = pygame.font.Font(None, 32)
        font_norm = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 20)
        
        # Title
        surface.blit(font_title.render("TRAFFIC CONTROL", True, (255, 255, 255)), (px + 50, py + 15))
        
        y = py + 55
        current_green = self.signal_cycle[self.current_signal_index]
        time_left = (GREEN_LIGHT_DURATION if self.signal_state == "GREEN" else YELLOW_LIGHT_DURATION) - self.signal_timer
        
        for text, color in [
            (f"Time: {datetime.now().strftime('%H:%M:%S')}", (200, 200, 200)),
            (f"Green: {current_green}", (0, 255, 0)),
            (f"Timer: {time_left}s", (255, 200, 0))
        ]:
            font = font_small if color == (200, 200, 200) else font_norm
            surface.blit(font.render(text, True, color), (px + 20, y))
            y += 25 if color == (200, 200, 200) else 30
        
        y += 10
        pygame.draw.line(surface, (100, 100, 255), (px + 10, y), (px + pw - 10, y), 2)
        y += 15
        
        # Per-direction stats
        for direction in self.signal_cycle:
            signal = self.signals[direction]
            color = (0, 255, 0) if signal.state == "GREEN" else \
                    (255, 255, 0) if signal.state == "YELLOW" else (255, 0, 0)
            
            surface.blit(font_norm.render(direction, True, (255, 255, 255)), (px + 20, y))
            pygame.draw.circle(surface, color, (px + 130, y + 10), 8)
            
            queue_len = len(self.vehicles[direction][0]) + len(self.vehicles[direction][1])
            surface.blit(font_small.render(f"Q:{queue_len}", True, (200, 200, 200)), (px + 20, y + 25))
            
            stat_text = f"P:{signal.vehicles_passed}" if signal.state == "GREEN" else f"W:{signal.vehicles_waiting}"
            stat_color = (0, 255, 0) if signal.state == "GREEN" else (255, 100, 100)
            surface.blit(font_small.render(stat_text, True, stat_color), (px + 170, y + 25))
            y += 55
        
        pygame.draw.line(surface, (100, 100, 255), (px + 10, y), (px + pw - 10, y), 2)
        y += 20
        surface.blit(font_norm.render("STATISTICS", True, (255, 255, 0)), (px + 90, y))
        y += 30
        
        # Global stats
        current_total = sum(len(l) for d in self.vehicles.values() for l in d.values())
        for stat in [
            f"Spawned: {self.total_spawned}",
            f"Passed: {self.total_passed}",
            f"Current: {current_total}"
        ]:
            surface.blit(font_small.render(stat, True, (200, 200, 200)), (px + 20, y))
            y += 25
            
        y += 15
        pygame.draw.line(surface, (100, 100, 255), (px + 10, y), (px + pw - 10, y), 2)
        y += 15
        surface.blit(font_small.render("SPACE-Random | N/S/E/W-Dir", True, (180, 180, 180)), (px + 20, y))

    def draw(self, surface):
        """Main draw call for the entire simulation."""
        self.draw_roads(surface)
        
        for signal in self.signals.values():
            signal.draw(surface)
            
        for direction_lanes in self.vehicles.values():
            for lane_vehicles in direction_lanes.values():
                for v in lane_vehicles:
                    v.draw(surface)
                    
        self.draw_ui(surface)


# --- Main Function ---
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Indian Traffic Signal Simulation (Enhanced)")
    clock = pygame.time.Clock()
    
    intersection = Intersection()
    running = True
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key_map = {
                    pygame.K_SPACE: None, pygame.K_n: "NORTH", pygame.K_s: "SOUTH",
                    pygame.K_e: "EAST", pygame.K_w: "WEST"
                }
                if event.key in key_map:
                    intersection.spawn_vehicle(key_map[event.key])
        
        intersection.update()
        intersection.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()

