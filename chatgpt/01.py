import tkinter as tk
import random
import math

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower Defense Game")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Initial game state variables
        self.tower_health = 100
        self.power = 0
        self.enemies = []
        self.enemy_speed = 2
        self.enemy_spawn_rate = 1000  # milliseconds
        self.enemy_damage = 10

        # Tower settings
        self.tower_x = 400
        self.tower_y = 300
        self.tower_radius = 50
        self.attack_radius = 100

        # Game objects
        self.tower = self.canvas.create_oval(self.tower_x - self.tower_radius,
                                             self.tower_y - self.tower_radius,
                                             self.tower_x + self.tower_radius,
                                             self.tower_y + self.tower_radius,
                                             fill="blue")
        self.health_bar = self.canvas.create_rectangle(10, 10, 210, 30, fill="green")
        self.power_bar = self.canvas.create_rectangle(10, 40, 210, 60, fill="yellow")
        
        # Start the game loop
        self.spawn_enemy()
        self.update_game()

    def spawn_enemy(self):
        # Create a random pighead (enemy)
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        enemy = self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="red")
        self.enemies.append(enemy)
        
        # Schedule next enemy spawn
        self.root.after(self.enemy_spawn_rate, self.spawn_enemy)

    def attack_wave(self):
        # Create a wave-like gradient effect for the tower attack
        for i in range(360):
            angle = math.radians(i)
            x1 = self.tower_x + self.attack_radius * math.cos(angle)
            y1 = self.tower_y + self.attack_radius * math.sin(angle)
            x2 = self.tower_x + (self.attack_radius + 5) * math.cos(angle)
            y2 = self.tower_y + (self.attack_radius + 5) * math.sin(angle)
            
            # Check for collision with enemies
            for enemy in self.enemies:
                ex, ey = self.canvas.coords(enemy)[0] + 15, self.canvas.coords(enemy)[1] + 15
                distance = math.hypot(ex - x1, ey - y1)
                if distance < 15:
                    self.enemies.remove(enemy)
                    self.canvas.delete(enemy)
                    self.power += 5  # Increase power when an enemy is killed

    def update_game(self):
        # Move enemies towards the tower
        for enemy in self.enemies[:]:
            ex, ey, ex2, ey2 = self.canvas.coords(enemy)
            angle = math.atan2(self.tower_y - (ey + ey2) / 2, self.tower_x - (ex + ex2) / 2)
            move_x = self.enemy_speed * math.cos(angle)
            move_y = self.enemy_speed * math.sin(angle)
            self.canvas.move(enemy, move_x, move_y)

            # Check for collision with tower (if enemy hits tower, reduce health)
            if abs(self.tower_x - (ex + ex2) / 2) < self.tower_radius and abs(self.tower_y - (ey + ey2) / 2) < self.tower_radius:
                self.tower_health -= self.enemy_damage
                self.canvas.itemconfig(self.health_bar, width=2 * self.tower_health)
                self.enemies.remove(enemy)
                self.canvas.delete(enemy)

        # Attack the enemies using the wave when power is enough
        if self.power >= 50:
            self.attack_wave()
            self.power = 0  # Reset power after using the attack

        # Upgrade tower if enough power is gained
        if self.power >= 100:
            self.enemy_speed += 1
            self.attack_radius += 10
            self.power = 0  # Reset power after upgrade

        # Update power bar
        self.canvas.itemconfig(self.power_bar, width=2 * self.power)

        # Check if the tower has been destroyed
        if self.tower_health <= 0:
            self.canvas.create_text(self.tower_x, self.tower_y, text="GAME OVER", font=("Arial", 24), fill="red")
            return  # End game loop

        # Continue the game loop
        self.root.after(30, self.update_game)


# Set up the main window and run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
