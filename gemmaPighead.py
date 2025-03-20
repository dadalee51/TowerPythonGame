import tkinter as tk
import random
import math

class PigHead:
    def __init__(self, canvas, x, y, speed, health):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.id = canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="pink")

    def move(self):
        self.y -= self.speed
        self.canvas.move(self.id, 0, -self.speed)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        self.canvas.delete(self.id)
        del self  # Important to release memory

class Tower:
    def __init__(self, canvas, x, y, damage, range_radius, attack_speed, 
health):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.damage = damage
        self.range_radius = range_radius
        self.attack_speed = attack_speed
        self.health = health
        self.last_attack_time = 0
        self.id = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, 
fill="blue")
        self.upgrade_level = 0  # Track upgrade level

    def attack(self, pig_head):
        if self.last_attack_time >= self.attack_speed:
            self.last_attack_time = 0
            pig_head.take_damage(self.damage)

    def draw_wave(self, angle_start, angle_end, wave_length):
        """Draws a wave-like attack effect."""
        num_segments = 10  # Number of segments in the wave
        for i in range(num_segments):
            angle = angle_start + (angle_end - angle_start) * i / (num_segments - 1)
            x = self.x + math.cos(angle) * self.range_radius
            y = self.y + math.sin(angle) * self.range_radius
            self.canvas.create_line(self.x, self.y, x, y, width=2, 
fill="light blue")

    def update(self, pig_heads):
        for pig_head in pig_heads:
            distance = math.sqrt((pig_head.x - self.x)**2 + (pig_head.y - 
self.y)**2)
            if distance <= self.range_radius:
                self.attack(pig_head)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.explode()

    def explode(self):
        self.canvas.delete(self.id)
        # Add explosion effects here (e.g., create circles, particles)
        print("Tower exploded!")
        # Game over logic would go here

    def upgrade(self):
        """Upgrades the tower's stats."""
        self.upgrade_level += 1
        if self.upgrade_level == 1:
            self.damage += 5
            self.range_radius += 10
            self.attack_speed /= 1.5
            print("Tower upgraded! Damage:", self.damage, "Range:", 
self.range_radius, "Attack Speed:", self.attack_speed)
        elif self.upgrade_level == 2:
            self.damage += 10
            self.range_radius += 20
            self.attack_speed /= 1.2
            print("Tower upgraded! Damage:", self.damage, "Range:", 
self.range_radius, "Attack Speed:", self.attack_speed)
        # Add more upgrade levels as needed


def main():
    root = tk.Tk()
    root.title("Pig Head Defense")

    canvas_width = 1000
    canvas_height = 800
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, 
bg="white")
    canvas.pack()

    tower_x = canvas_width // 2
    tower_y = canvas_height - 100
    tower = Tower(canvas, tower_x, tower_y, 10, 100, 1, 100)

    pig_heads = []
    score = 0
    game_over = False

    def spawn_pig_head():
        nonlocal score
        if not game_over:
            x = random.randint(0, canvas_width)
            y = 0
            speed = random.randint(3, 10)
            health = 20
            pig_head = PigHead(canvas, x, y, speed, health)
            pig_heads.append(pig_head)

            if score % 100 == 0:
                tower.upgrade()

            score += 1
            root.after(random.randint(1000, 2000), spawn_pig_head)

    def update():
        nonlocal score, game_over
        if not game_over:
            for pig_head in pig_heads:
                pig_head.move()

            tower.update(pig_heads)

            # Check for collisions (optional - for more complex interactions)
            # ...

            # Check if tower health is zero
            if tower.health <= 0:
                game_over = True
                print("Game Over! Tower destroyed.")

            root.after(30, update)  # Adjust update frequency as needed

    def draw():
        if not game_over:
            # Draw the tower
            tower.draw_wave(math.pi / 4, math.pi * 3 / 4, 50)
            tower.draw_wave(math.pi * 3 / 4, math.pi * 5 / 4, 50)
            tower.draw_wave(math.pi * 5 / 4, math.pi * 7 / 4, 50)
            tower.draw_wave(math.pi * 7 / 4, math.pi * 11 / 4, 50)

            # Draw pig heads
            for pig_head in pig_heads:
                pass  # PigHead's draw is handled by its creation

            # Display score
            canvas.create_text(50, 20, text="Score: " + str(score), 
fill="black")

    # Initial setup
    spawn_pig_head()
    update()
    draw()

    root.mainloop()

if __name__ == "__main__":
    main()
