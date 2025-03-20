import math
import random
import tkinter as tk

class PigHead:
   def __init__(self, x, y, speed):
       self.x = x
       self.y = y
       self.speed = speed
       self.health = 10

   def move(self):
       self.x += self.speed * (tower.x - self.x) / math.sqrt((tower.x - self.x)**2 + (tower.y - self.y)**2)
       self.y += self.speed * (tower.y - self.y) / math.sqrt((tower.x - self.x)**2 + (tower.y - self.y)**2)

class Tower:
   def __init__(self, x, y, attack_range, attack_damage):
       self.x = x
       self.y = y
       self.attack_range = attack_range
       self.attack_damage = attack_damage

   def attack(self, pighead):
       if math.sqrt((pighead.x - self.x)**2 + (pighead.y - self.y)**2) <= self.attack_range:
           pighead.health -= self.attack_damage

   def take_damage(self, damage):
       print(f"Tower took {damage} damage!")

def create_pighead(tower_x, tower_y):
   x = random.randint(0, 100)
   y = random.randint(0, 100)
   speed = random.randint(1, 3)
   return PigHead(x, y, speed)

tower_x = 50
tower_y = 50
tower = Tower(tower_x, tower_y, 30, 5)

pigheads = []
for _ in range(3):
   pigheads.append(create_pighead(tower_x, tower_y))

def game_loop():
   for pighead in list(pigheads):
       pighead.move()

       if math.sqrt((pighead.x - tower.x)**2 + (pighead.y - self.y)**2) <= tower.attack_range:
           tower.attack(pighead)

       if pighead.health <= 0:
           pigheads.remove(pighead)

       if math.sqrt((pighead.x - tower.x)**2 + (pighead.y - tower.y)**2) <= 5:
           tower.take_damage(10)
           pigheads.remove(pighead)

   if len(pigheads) < 5:
       for _ in range(5 - len(pigheads)):
           pigheads.append(create_pighead(tower_x, tower_y))

   root.after(100, game_loop)

def upgrade_tower():
    tower.attack_damage += 5
    print(f"Tower upgraded! Attack damage: {tower.attack_damage}")

root = tk.Tk()
root.title("Pighead Defense")

upgrade_button = tk.Button(root, text="Upgrade Tower", command=upgrade_tower)
upgrade_button.pack()

game_loop()
root.mainloop()
