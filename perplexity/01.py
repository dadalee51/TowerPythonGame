import tkinter as tk
import random
import math

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TOWER_RADIUS = 30
ENEMY_SIZE = 20
TOWER_HEALTH = 100
WAVE_RADIUS_INCREMENT = 10
UPGRADE_THRESHOLD = 10

class DefenseGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Defense Game")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack()

        self.tower_health = TOWER_HEALTH
        self.score = 0
        self.wave_radius = 50
        self.enemies = []
        self.upgrade_level = 1

        self.tower_x = WINDOW_WIDTH // 2
        self.tower_y = WINDOW_HEIGHT // 2
        self.tower = self.canvas.create_oval(
            self.tower_x - TOWER_RADIUS, 
            self.tower_y - TOWER_RADIUS,
            self.tower_x + TOWER_RADIUS,
            self.tower_y + TOWER_RADIUS,
            fill="blue"
        )

        self.health_text = self.canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 16))
        self.score_text = self.canvas.create_text(10, 40, anchor="nw", fill="white", font=("Arial", 16))
        
        self.update_health_score()
        self.spawn_enemy()
        self.update_game()

    def update_health_score(self):
        self.canvas.itemconfig(self.health_text, text=f"Health: {self.tower_health}")
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def spawn_enemy(self):
        side = random.choice(["top", "bottom", "left", "right"])
        
        if side == "top":
            x, y = random.randint(0, WINDOW_WIDTH), 0
        elif side == "bottom":
            x, y = random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT
        elif side == "left":
            x, y = 0, random.randint(0, WINDOW_HEIGHT)
        else:
            x, y = WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT)

        enemy_id = self.canvas.create_oval(
            x - ENEMY_SIZE // 2,
            y - ENEMY_SIZE // 2,
            x + ENEMY_SIZE // 2,
            y + ENEMY_SIZE // 2,
            fill="pink"
        )
        
        speed = random.uniform(1.5, 3.5)
        
        self.enemies.append({"id": enemy_id, "x": x, "y": y, "speed": speed})
        
        if self.tower_health > 0:
            spawn_time = max(500 - len(self.enemies) * 10, 200)
            self.root.after(spawn_time, self.spawn_enemy)

    def update_game(self):
        if self.tower_health <= 0:
            self.canvas.create_text(
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2,
                text="GAME OVER",
                fill="red",
                font=("Arial", 36)
            )
            return

        for enemy in list(self.enemies):  
            ex, ey = self.canvas.coords(enemy["id"])[:2]
            angle = math.atan2(self.tower_y - ey, self.tower_x - ex)
            dx = enemy["speed"] * math.cos(angle)
            dy = enemy["speed"] * math.sin(angle)
            
            self.canvas.move(enemy["id"], dx, dy)
            
            if self.distance(ex, ey, self.tower_x, self.tower_y) < TOWER_RADIUS + ENEMY_SIZE // 2:
                self.tower_health -= 10
                self.enemies.remove(enemy)
                self.canvas.delete(enemy["id"])
                self.update_health_score()
            
            elif self.distance(ex, ey, self.tower_x, self.tower_y) < self.wave_radius:
                self.enemies.remove(enemy)
                self.canvas.delete(enemy["id"])
                self.score += 1
                self.update_health_score()
                
                if self.score % UPGRADE_THRESHOLD == 0:
                    self.upgrade_level += 1
                    self.wave_radius += WAVE_RADIUS_INCREMENT
        
        self.canvas.delete("wave")
        self.canvas.create_oval(
            self.tower_x - self.wave_radius,
            self.tower_y - self.wave_radius,
            self.tower_x + self.wave_radius,
            self.tower_y + self.wave_radius,
            outline="cyan",
            width=2,
            tags="wave"
        )
        
        self.root.after(50, self.update_game)

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

if __name__ == "__main__":
    root = tk.Tk()
    game = DefenseGame(root)
    root.mainloop()
