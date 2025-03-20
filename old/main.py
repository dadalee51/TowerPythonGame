import tkinter as tk
from tkinter import messagebox
import random
import math

# Window setup
root = tk.Tk()
root.title("Tower Defense Game")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Game variables
enemies = []
towers = []
projectiles = []
money = 100  # Player's money to buy towers
tower_cost = 50  # Cost to place a tower

# Enemy class
class Enemy:
    def __init__(self):
        self.x = 0  # Start at left edge
        self.y = random.randint(100, 500)  # Random y position
        self.speed = 2
        self.radius = 10
        self.id = canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                     self.x + self.radius, self.y + self.radius, fill="red")

    def move(self):
        self.x += self.speed
        canvas.coords(self.id, self.x - self.radius, self.y - self.radius,
                      self.x + self.radius, self.y + self.radius)
        if self.x > 800:  # Enemy reaches the end
            canvas.delete(self.id)
            return False
        return True

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100  # Attack range
        self.rate = 20  # Frames between shots
        self.cooldown = 0
        self.size = 20
        self.id = canvas.create_rectangle(self.x - self.size, self.y - self.size,
                                          self.x + self.size, self.y + self.size, fill="blue")

    def attack(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        for enemy in enemies[:]:  # Copy list to avoid modification issues
            dist = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
            if dist <= self.range:
                projectiles.append(Projectile(self.x, self.y, enemy))
                self.cooldown = self.rate
                break

# Projectile class
class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5
        self.radius = 5
        self.id = canvas.create_oval(self.x - self.radius, self.y - self.radius,
                                     self.x + self.radius, self.y + self.radius, fill="green")

    def move(self):
        if self.target not in enemies:
            canvas.delete(self.id)
            return False
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist < self.speed:  # Hit the target
            canvas.delete(self.id)
            if self.target in enemies:
                enemies.remove(self.target)
                canvas.delete(self.target.id)
            return False
        self.x += (dx / dist) * self.speed
        self.y += (dy / dist) * self.speed
        canvas.coords(self.id, self.x - self.radius, self.y - self.radius,
                      self.x + self.radius, self.y + self.radius)
        return True

# Game functions
def spawn_enemy():
    if random.randint(0, 30) == 0:  # Randomly spawn enemies
        enemies.append(Enemy())

def place_tower(event):
    global money
    if money >= tower_cost:
        towers.append(Tower(event.x, event.y))
        money -= tower_cost
        update_money_label()
    else:
        messagebox.showinfo("Insufficient Funds", "Not enough money to place a tower!")

def update_money_label():
    canvas.delete("money")
    canvas.create_text(50, 20, text=f"Money: ${money}", font=("Arial", 14), tag="money")

def game_loop():
    spawn_enemy()
    
    # Update enemies
    for enemy in enemies[:]:
        if not enemy.move():
            enemies.remove(enemy)
    
    # Update towers
    for tower in towers:
        tower.attack()
    
    # Update projectiles
    for proj in projectiles[:]:
        if not proj.move():
            projectiles.remove(proj)
    
    root.after(50, game_loop)  # Run loop every 50ms

# Bind mouse click to place towers
canvas.bind("<Button-1>", place_tower)

# Initial money display
update_money_label()

# Start the game loop
game_loop()

# Run the application
root.mainloop()