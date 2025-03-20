import tkinter as tk
import random
import time

class DefenseGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower Defense")
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="lightblue")
        self.canvas.pack()

        self.tower_x = self.width // 2
        self.tower_y = self.height // 2
        self.tower_radius = 30
        self.tower_health = 100
        self.tower_power = 0
        self.tower_level = 1
        self.tower_damage = 10

        self.enemies = []
        self.waves = []
        self.wave_radius = 50
        self.wave_speed = 5
        self.enemy_speed = 2
        self.enemy_radius = 20
        self.enemy_health = 20

        self.create_tower()
        self.spawn_enemy()
        self.update()

    def create_tower(self):
        self.tower = self.canvas.create_oval(
            self.tower_x - self.tower_radius, self.tower_y - self.tower_radius,
            self.tower_x + self.tower_radius, self.tower_y + self.tower_radius,
            fill="gray"
        )
        self.health_text = self.canvas.create_text(
            self.tower_x, self.tower_y + self.tower_radius + 20,
            text=f"Health: {self.tower_health}", fill="black"
        )
        self.power_text = self.canvas.create_text(
            self.tower_x, self.tower_y + self.tower_radius + 40,
            text=f"Power: {self.tower_power}", fill="black"
        )
        self.level_text = self.canvas.create_text(
            self.tower_x, self.tower_y + self.tower_radius + 60,
            text=f"Level: {self.tower_level}", fill="black"
        )

    def spawn_enemy(self):
        x = random.choice([0, self.width]) if random.random() < 0.5 else random.randint(0, self.width)
        y = random.choice([0, self.height]) if x in [0, self.width] else random.choice([0, self.height])
        enemy = self.canvas.create_oval(
            x - self.enemy_radius, y - self.enemy_radius,
            x + self.enemy_radius, y + self.enemy_radius,
            fill="brown", tags="enemy"
        )
        self.enemies.append({"id": enemy, "x": x, "y": y, "health": self.enemy_health})
        self.root.after(1000, self.spawn_enemy)

    def move_enemy(self, enemy):
        dx = self.tower_x - enemy["x"]
        dy = self.tower_y - enemy["y"]
        distance = (dx**2 + dy**2)**0.5
        if distance != 0:
            dx /= distance
            dy /= distance
        enemy["x"] += dx * self.enemy_speed
        enemy["y"] += dy * self.enemy_speed
        self.canvas.coords(enemy["id"], enemy["x"] - self.enemy_radius, enemy["y"] - self.enemy_radius,
                           enemy["x"] + self.enemy_radius, enemy["y"] + self.enemy_radius)

    def attack(self):
        wave = self.canvas.create_oval(
            self.tower_x - self.wave_radius, self.tower_y - self.wave_radius,
            self.tower_x + self.wave_radius, self.tower_y + self.wave_radius,
            outline="red", width=2, tags="wave"
        )
        self.waves.append({"id": wave, "radius": self.wave_radius})

    def move_wave(self, wave):
        wave["radius"] += self.wave_speed
        self.canvas.coords(wave["id"], self.tower_x - wave["radius"], self.tower_y - wave["radius"],
                           self.tower_x + wave["radius"], self.tower_y + wave["radius"])

        enemies_to_remove = []
        for enemy in self.enemies:
            dx = enemy["x"] - self.tower_x
            dy = enemy["y"] - self.tower_y
            distance = (dx**2 + dy**2)**0.5
            if distance <= wave["radius"]:
                enemy["health"] -= self.tower_damage
                if enemy["health"] <= 0:
                    self.canvas.delete(enemy["id"])
                    enemies_to_remove.append(enemy)
                    self.tower_power += 5
                    self.canvas.itemconfig(self.power_text, text=f"Power: {self.tower_power}")

        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

        if wave["radius"] > max(self.width, self.height):
            self.canvas.delete(wave["id"])
            self.waves.remove(wave)

    def check_collision(self):
        enemies_to_remove = []
        for enemy in self.enemies:
            dx = enemy["x"] - self.tower_x
            dy = enemy["y"] - self.tower_y
            distance = (dx**2 + dy**2)**0.5
            if distance < self.tower_radius + self.enemy_radius:
                self.tower_health -= 1
                self.canvas.itemconfig(self.health_text, text=f"Health: {self.tower_health}")
                self.canvas.delete(enemy["id"])
                enemies_to_remove.append(enemy)
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

        if self.tower_health <= 0:
            self.game_over()

    def upgrade_tower(self):
        if self.tower_power >= 50:
            self.tower_level += 1
            self.tower_damage += 5
            self.tower_power -= 50
            self.canvas.itemconfig(self.power_text, text=f"Power: {self.tower_power}")
            self.canvas.itemconfig(self.level_text, text=f"Level: {self.tower_level}")

    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text="Game Over!", font=("Arial", 30), fill="red"
        )

    def update(self):
        for enemy in self.enemies[:]:
            self.move_enemy(enemy)
        for wave in self.waves[:]:
            self.move_wave(wave)

        self.check_collision()

        if random.random() < 0.01:
            self.attack()
        if self.tower_power >= 50:
            self.upgrade_tower()

        self.root.after(30, self.update)

root = tk.Tk()
game = DefenseGame(root)
root.mainloop()