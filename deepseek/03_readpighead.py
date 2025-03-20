import tkinter as tk
import math
import random

class TowerDefense:
    def __init__(self, root):
        self.root = root
        self.root.title("Pighead Defense")
        
        # Game constants
        self.WIDTH = 800
        self.HEIGHT = 600
        self.CENTER = (self.WIDTH//2, self.HEIGHT//2)
        self.TOWER_SIZE = 40
        self.ENEMY_SPEED = 2.5
        self.SPAWN_RATE = 500
        self.WAVE_SPEED = 7
        self.MAX_WAVE_RADIUS = 300
        self.INITIAL_HEALTH = 100
        
        # Game state
        self.tower_health = self.INITIAL_HEALTH
        self.enemies = []
        self.wave_radius = 0
        self.wave_active = False
        self.kills = 0
        self.power = 0
        self.weapon_level = 1
        self.game_over = False
        
        # Setup canvas
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg='black')
        self.canvas.pack()
        
        # Draw initial elements
        self.draw_tower()
        self.draw_health_bar()
        
        # Bind controls
        self.root.bind('<space>', self.activate_wave)
        
        # Start game loops
        self.spawn_enemy_loop()
        self.game_loop()

    def draw_tower(self):
        x, y = self.CENTER
        self.tower = self.canvas.create_oval(
            x - self.TOWER_SIZE, y - self.TOWER_SIZE,
            x + self.TOWER_SIZE, y + self.TOWER_SIZE,
            fill='#404040', outline='#606060'
        )

    def draw_health_bar(self):
        x, y = self.CENTER
        self.health_bar = self.canvas.create_rectangle(
            x - self.TOWER_SIZE, y - self.TOWER_SIZE - 15,
            x + self.TOWER_SIZE, y - self.TOWER_SIZE - 5,
            fill='#00ff00', outline=''
        )

    def update_health(self):
        x, y = self.CENTER
        width = (self.tower_health / self.INITIAL_HEALTH) * (2 * self.TOWER_SIZE)
        self.canvas.coords(self.health_bar,
            x - self.TOWER_SIZE, y - self.TOWER_SIZE - 15,
            x - self.TOWER_SIZE + width, y - self.TOWER_SIZE - 5
        )
        color = '#00ff00' if self.tower_health > 50 else '#ffff00' if self.tower_health > 25 else '#ff0000'
        self.canvas.itemconfig(self.health_bar, fill=color)

    def draw_pig_head(self, x, y):
        # Main head
        head = self.canvas.create_oval(
            x-15, y-15, x+15, y+15,
            fill='#ffb3d9', outline='#ff80bf', width=2
        )
        
        # Ears
        left_ear = self.canvas.create_oval(
            x-20, y-25, x-10, y-15,
            fill='#ff80bf', outline='#ff4da6', width=1
        )
        right_ear = self.canvas.create_oval(
            x+10, y-25, x+20, y-15,
            fill='#ff80bf', outline='#ff4da6', width=1
        )
        
        # Snout
        snout = self.canvas.create_oval(
            x-10, y-5, x+10, y+10,
            fill='#ffb3d9', outline='#ff80bf', width=2
        )
        
        # Nostrils
        left_nostril = self.canvas.create_oval(
            x-7, y+3, x-3, y+7,
            fill='#ff4da6', outline=''
        )
        right_nostril = self.canvas.create_oval(
            x+3, y+3, x+7, y+7,
            fill='#ff4da6', outline=''
        )
        
        # Eyes
        left_eye = self.canvas.create_oval(
            x-12, y-12, x-8, y-8,
            fill='black', outline=''
        )
        right_eye = self.canvas.create_oval(
            x+8, y-12, x+12, y-8,
            fill='black', outline=''
        )
        
        return [head, left_ear, right_ear, snout, left_nostril, right_nostril, left_eye, right_eye]

    def spawn_enemy(self):
        angle = random.uniform(0, 2*math.pi)
        radius = max(self.WIDTH, self.HEIGHT) // 2 + 50
        x = self.CENTER[0] + radius * math.cos(angle)
        y = self.CENTER[1] + radius * math.sin(angle)
        
        pig_parts = self.draw_pig_head(x, y)
        self.enemies.append({
            'parts': pig_parts,
            'x': x,
            'y': y,
            'health': 2
        })

    def move_enemies(self):
        for enemy in list(self.enemies):
            dx = self.CENTER[0] - enemy['x']
            dy = self.CENTER[1] - enemy['y']
            dist = math.hypot(dx, dy)
            
            if dist < self.TOWER_SIZE + 10:
                self.tower_health -= 10
                for part in enemy['parts']:
                    self.canvas.delete(part)
                self.enemies.remove(enemy)
                self.update_health()
                if self.tower_health <= 0:
                    self.game_over = True
                    self.show_game_over()
                continue
                
            speed = self.ENEMY_SPEED
            enemy['x'] += dx / dist * speed
            enemy['y'] += dy / dist * speed
            
            # Move all pig parts
            for part in enemy['parts']:
                self.canvas.move(part, dx / dist * speed, dy / dist * speed)

    def activate_wave(self, event):
        if not self.wave_active and not self.game_over:
            self.wave_active = True
            self.wave_radius = 0

    def draw_wave(self):
        self.canvas.delete('wave')
        if self.wave_active:
            for i in range(0, 15):
                radius = self.wave_radius - i*15
                if radius > 0:
                    blue_shade = 255 - i*17
                    color = f'#0000{blue_shade:02x}'
                    self.canvas.create_oval(
                        self.CENTER[0]-radius, self.CENTER[1]-radius,
                        self.CENTER[0]+radius, self.CENTER[1]+radius,
                        outline=color, tags='wave'
                    )

    def update_wave(self):
        if self.wave_active:
            self.wave_radius += self.WAVE_SPEED
            max_radius = self.MAX_WAVE_RADIUS * (1 + 0.2*self.weapon_level)
            if self.wave_radius > max_radius:
                self.wave_active = False
                self.wave_radius = 0
            else:
                self.check_wave_collision()

    def check_wave_collision(self):
        for enemy in list(self.enemies):
            dx = enemy['x'] - self.CENTER[0]
            dy = enemy['y'] - self.CENTER[1]
            dist = math.hypot(dx, dy)
            
            if dist < self.wave_radius:
                enemy['health'] -= 1 * self.weapon_level
                if enemy['health'] <= 0:
                    for part in enemy['parts']:
                        self.canvas.delete(part)
                    self.enemies.remove(enemy)
                    self.kills += 1
                    self.power += 1
                    if self.power >= 3 * self.weapon_level:
                        self.weapon_level += 1
                        self.power = 0

    def show_game_over(self):
        self.canvas.create_text(
            self.WIDTH//2, self.HEIGHT//2,
            text="GAME OVER",
            font=('Arial', 48),
            fill='red',
            tags='gameover'
        )
        self.canvas.create_oval(
            self.CENTER[0]-50, self.CENTER[1]-50,
            self.CENTER[0]+50, self.CENTER[1]+50,
            fill='red', tags='explosion'
        )

    def spawn_enemy_loop(self):
        if not self.game_over:
            self.spawn_enemy()
            self.root.after(self.SPAWN_RATE, self.spawn_enemy_loop)

    def game_loop(self):
        if not self.game_over:
            self.move_enemies()
            self.update_wave()
            self.draw_wave()
            self.root.after(16, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = TowerDefense(root)
    root.mainloop()