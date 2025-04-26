import pygame
import math
import sys
from functools import partial

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Incremental Game")

#Class Button yang mencakup rendering dan fungsinya
class Button:
    def __init__(self, x, y, w, h, text, func):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.func = func
    def draw(self):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.w, self.h))
        f = pygame.font.Font(None, 30)
        lines = self.text.split("\n")
        for i, line in enumerate(lines):
            txt = f.render(line, True, (255, 255, 255))
            # Center each line within the button
            screen.blit(txt, (self.x + (self.w - txt.get_width()) / 2, self.y + i * txt.get_height() + (self.h - len(lines) * txt.get_height()) / 2))
    def onclick(self):
        self.func()
    def update_text(self, new_text):
        self.text = new_text


#Mendefinisikan fungsi untuk mekanisme game
def get_mult():
    multiplier = 1
    global upg
    global upg_eff
    for i in range(len(upg)):
        multiplier *= upg_eff(i)
    return multiplier
def increment():
    global points
    points += 1 * get_mult()
    print(points)
def upg_eff(i):
    if i == 0:
        return 1 + (upg[0] * 0.2)
    elif i == 1:
        return 1 + (upg[1] * 0.4)
    elif i == 2:
        return 1 + (upg[2] * 0.6)
def buy_upg(i):
    global points, upg, upg_base_cost, upg_cost_inc
    c = upg_base_cost[i] * (upg_cost_inc[i] ** upg[i])
    if points >= c:
        points -= c
        upg[i] += 1
        print(f"Upgraded {i} to {upg[i]}")
def buy_factory():
    global points, factories, factory_cost
    c = factory_cost * (factory_inc ** factories)
    if points >= c:
        points -= c
        factories += 1

#Mendefinisikan variabel awal
points = 0
factories = 0
factory_cost = 2
factory_inc = 1.15
upg = [0,0,0]
upg_base_cost = [10, 100, 1000]
upg_cost_inc = [1.2, 1.5, 2]

#Objek Button
buttons = []
buttons.append(Button(100, 200, 200, 100, "Click Me!", increment))
buttons.append(Button(100, 310, 200, 100, f"Buy Upgrade 1\nCost: {upg_base_cost[0] * (upg_cost_inc[0] ** upg[0]):.2f} points", partial(buy_upg, 0)))
buttons.append(Button(100, 420, 200, 100, f"Buy Upgrade 2\nCost: {upg_base_cost[1] * (upg_cost_inc[1] ** upg[1]):.2f} points", partial(buy_upg, 1)))
buttons.append(Button(100, 530, 200, 100, f"Buy Upgrade 3\nCost: {upg_base_cost[2] * (upg_cost_inc[2] ** upg[2]):.2f} points", partial(buy_upg, 2)))
buttons.append(Button(310, 200, 200, 100, f"Buy Factory", buy_factory))

#Variabel untuk game loop
clock = pygame.time.Clock()

running = True
while running:
    #Mekanisme pertambahan poin seiring waktu
    dt = clock.tick(120) / 1000
    points += factories * get_mult() * dt

    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        #Mengatur event klik pada tombol
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for btn in buttons:
                    if btn.x <= event.pos[0] <= btn.x + btn.w and btn.y <= event.pos[1] <= btn.y + btn.h:
                        btn.onclick()
    
    #Menampilkan tombol dan teks
    buttons[1].update_text(f"Buy Upgrade 1\nCost: {upg_base_cost[0] * (upg_cost_inc[0] ** upg[0]):.2f} points")
    buttons[2].update_text(f"Buy Upgrade 2\nCost: {upg_base_cost[1] * (upg_cost_inc[1] ** upg[1]):.2f} points")
    buttons[3].update_text(f"Buy Upgrade 3\nCost: {upg_base_cost[2] * (upg_cost_inc[2] ** upg[2]):.2f} points")
    buttons[4].update_text(f"Buy Factory\nCost: {factory_cost * (factory_inc ** factories):.2f} points")
    for btn in buttons:
        btn.draw()

    #Menampilkan skor
    f = pygame.font.Font(None, 32) 
    txt = f.render(f"Score: {points:.2f}", True, (255, 255, 255))
    screen.blit(txt, (10, 10))
    pygame.display.update()

#Akhir dari game loop
pygame.quit()