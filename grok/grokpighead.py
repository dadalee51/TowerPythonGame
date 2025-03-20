import tkinter as tk
import random
import math

# Window setup
root = tk.Tk()
root.title("Pighead Tower Defense")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Game variables
tower_x, tower_y = 400, 300  # Center of screen
tower_size = 20
tower_health = 100
tower_id = canvas.create_rectangle(tower_x - tower_size, tower_y - tower_size,
                                   tower_x + tower_size, tower_y + tower_size, fill="green")
health_bar = canvas.create_rectangle(350, 20, 350 + tower_health * 2, 40, fill="lime")

enemies = []
waves = []
power = 0
wave_damage = 5  # Initial damage
wave_range = 100  # Initial range
wave_speed = 3
spawn_rate = 30  # Frames between enemy spawns
spawn_counter = 0

# Enemy class (Pigheads with detailed drawing)
class Pighead:
    def __init__(self):
        # Unique tag for this pighead instance
        self.tag = f"pighead_{id(self)}"
        # Spawn at a random position on a circle 400 pixels from the tower
        angle = random.uniform(0, 2 * math.pi)
        self.x = tower_x + math.cos(angle) * 400
        self.y = tower_y + math.sin(angle) * 400
        self.speed = 2
        # Draw the pighead components
        # Head: 30px diameter oval
        self.head_id = canvas.create_oval(self.x - 15, self.y - 15, self.x + 15, self.y + 15, fill="pink", tags=self.tag)
        # Left ear
        self.ear_left_id = canvas.create_oval(self.x - 20, self.y - 20, self.x - 10, self.y - 10, fill="pink", tags=self.tag)
        # Right ear
        self.ear_right_id = canvas.create_oval(self.x + 10, self.y - 20, self.x + 20, self.y - 10, fill="pink", tags=self.tag)
        # Snout
        self.snout_id = canvas.create_oval(self.x - 5, self.y, self.x + 5, self.y + 10, fill="lightpink", tags=self.tag)
        # Left eye
        self.eye_left_id = canvas.create_oval(self.x - 7, self.y - 5, self.x - 3, self.y - 1, fill="black", tags=self.tag)
        # Right eye
        self.eye_right_id = canvas.create_oval(self.x + 3, self.y - 5, self.x + 7, self.y - 1, fill="black", tags=self.tag)

    def move(self):
        # Calculate direction towards the tower
        dx = tower_x - self.x
        dy = tower_y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        # Check collision with tower
        if dist < tower_size + 15:  # Pighead radius is ~15
            global tower_health
            tower_health -= 10
            canvas.delete(self.tag)  # Delete all pighead parts
            return False
        # Move all parts together
        move_x = (dx / dist) * self.speed
        move_y = (dy / dist) * self.speed
        canvas.move(self.tag, move_x, move_y)
        # Update center position for collision detection
        self.x += move_x
        self.y += move_y
        return True

# Wave attack class
class Wave:
    def __init__(self):
        self.radius = 0
        self.max_radius = wave_range
        self.id = canvas.create_oval(tower_x - self.radius, tower_y - self.radius,
                                     tower_x + self.radius, tower_y + self.radius,
                                     outline=self.get_gradient_color(), width=2)

    def get_gradient_color(self):
        # Simple gradient from blue to cyan
        intensity = int(255 * (self.radius / self.max_radius))
        r = min(intensity, 255)
        g = min(int(255 - intensity / 2), 255)
        b = 255
        return f"#{r:02x}{g:02x}{b:02x}"

    def expand(self):
        self.radius += wave_speed
        canvas.coords(self.id, tower_x - self.radius, tower_y - self.radius,
                      tower_x + self.radius, tower_y + self.radius)
        canvas.itemconfig(self.id, outline=self.get_gradient_color())
        if self.radius >= self.max_radius:
            canvas.delete(self.id)
            return False
        return True

    def check_collision(self):
        global power
        for enemy in enemies[:]:
            dist = math.sqrt((tower_x - enemy.x) ** 2 + (tower_y - enemy.y) ** 2)
            if abs(dist - self.radius) < 10:  # Wave hits enemy
                enemies.remove(enemy)
                canvas.delete(enemy.tag)  # Delete all pighead parts
                power += 1

# Game functions
def spawn_pighead():
    global spawn_counter
    spawn_counter += 1
    if spawn_counter >= spawn_rate:
        enemies.append(Pighead())
        spawn_counter = 0

def spawn_wave():
    waves.append(Wave())

def update_health_bar():
    canvas.coords(health_bar, 350, 20, 350 + tower_health * 2, 40)
    canvas.itemconfig(health_bar, fill="lime" if tower_health > 30 else "red")

def upgrade_wave():
    global wave_damage, wave_range, power
    if power >= 10:  # Upgrade every 10 kills
        wave_damage += 2
        wave_range += 20
        power -= 10
        canvas.create_text(400, 50, text="Wave Upgraded!", font=("Arial", 14), fill="blue", tag="upgrade")
        root.after(1000, lambda: canvas.delete("upgrade"))

def explode_tower():
    canvas.create_oval(tower_x - 50, tower_y - 50, tower_x + 50, tower_y + 50, fill="red", tag="explosion")
    canvas.delete(tower_id)
    canvas.delete(health_bar)
    canvas.create_text(400, 300, text="Game Over!", font=("Arial", 30), fill="black")
    root.after(2000, root.destroy)

def game_loop():
    global tower_health
    spawn_pighead()

    # Update enemies
    for enemy in enemies[:]:
        if not enemy.move():
            enemies.remove(enemy)

    # Spawn wave every 20 frames
    if len(waves) == 0 or waves[-1].radius > wave_range / 2:
        spawn_wave()

    # Update waves
    for wave in waves[:]:
        if not wave.expand():
            waves.remove(wave)
        else:
            wave.check_collision()

    # Update health and check game over
    update_health_bar()
    if tower_health <= 0:
        explode_tower()
        return

    # Update power display
    canvas.delete("power")
    canvas.create_text(50, 20, text=f"Power: {power}", font=("Arial", 14), tag="power")

    root.after(50, game_loop)

# Start the game
game_loop()
root.mainloop()