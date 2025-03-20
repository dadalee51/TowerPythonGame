import tkinter as tk
from tkinter import ttk
import random
import math

class DefenseGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Defense Game")
        self.width, self.height = 800, 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        # Load images (replace paths with your image files)
        self.tower_image = tk.PhotoImage(file="tower.png")
        self.enemy_image = tk.PhotoImage(file="pighead.png")
        self.explosion_image = tk.PhotoImage(file="explosion.png")

        self.tower = Tower(self.canvas, self.width/2, self.height/2, self.tower_image)
        self.enemies = []
        self.waves = []
        self.game_over = False

        # Game state
        self.score = 0
        self.upgrade_power = 0

        self.root.bind("<Button-1>", self.shoot)
        self.update()
        self.root.mainloop()

    def update(self):
        if not self.game_over:
            for enemy in self.enemies.copy():
                enemy.move()
                if enemy.check_collision(self.tower):
                    self.tower.health -= 1
                    enemy.destroy()
                    if self.tower.health <= 0:
                        self.end_game()
            # Spawn new enemies periodically
            if random.randint(1, 50) == 1:
                self.spawn_enemy()
            # Update waves
            for wave in self.waves.copy():
                wave.update()
                if wave.radius > 200:
                    self.waves.remove(wave)
            self.tower.draw_attack_waves(self.upgrade_power)
            self.root.after(30, self.update)

    def spawn_enemy(self):
        x = random.randint(100, self.width-100)
        y = random.randint(100, self.height-100)
        enemy = Enemy(self.canvas, x, y, self.enemy_image)
        self.enemies.append(enemy)

    def shoot(self, event):
        # This could be expanded for shooting mechanics
        pass

    def end_game(self):
        self.game_over = True
        self.tower.explosion()
        self.display_game_over()

    def display_game_over(self):
        game_over_text = self.canvas.create_text(self.width/2, self.height/2,
                                               text="Game Over",
                                               font=("Arial", 30),
                                               fill="red")

class Tower:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = image
        self.health = 10
        self.attack_radius = 100
        self.upgrade_level = 1

    def draw(self):
        self.canvas.create_image(self.x, self.y, image=self.image)

    def draw_attack_waves(self, upgrade_power):
        waves_count = int(upgrade_power) + 1
        for i in range(waves_count):
            color = f"#{int(255*(waves_count - i)/waves_count):02x}f{int(255*i/waves_count):02x}"
            radius = self.attack_radius * (i+1)
            self.canvas.create_oval(self.x - radius, self.y - radius,
                                   self.x + radius, self.y + radius,
                                   outline=color, width=2)

    def explosion(self):
        # Display explosion effect
        self.canvas.create_image(self.x, self.y, image=DefenseGame.explosion_image)

class Enemy:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image = image
        self.speed = 2

    def move(self):
        dx = (self.x - DefenseGame.tower.x) * self.speed
        dy = (self.y - DefenseGame.tower.y) * self.speed
        distance = math.hypot(dx, dy)
        if distance != 0:
            step_size = min(distance / self.speed, 5)
            self.x -= (DefenseGame.tower.x - self.x) * step_size / distance
            self.y -= (DefenseGame.tower.y - self.y) * step_size / distance

    def check_collision(self, tower):
        dx = self.x - tower.x
        dy = self.y - tower.y
        return math.hypot(dx, dy) < tower.attack_radius

    def destroy(self):
        self.canvas.delete(self.image)
        DefenseGame.score += 10
        if DefenseGame.score > 0:
            DefenseGame.upgrade_power += 1
            if DefenseGame.upgrade_power % 5 == 0:
                # Upgrade tower attack
                pass

# Replace these image paths with your actual image files
defense_game = DefenseGame()
