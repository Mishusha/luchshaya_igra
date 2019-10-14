from tkinter import *
from random import randrange as rnd, choice, uniform
import time
from math import *
root = Tk()
root.geometry('800x600') #Задаёт размеры окна

canv = Canvas(root, bg='white') #Рисует окно
l=Label(root, bg='black', fg='white', width=20)#рисует метку для score
l.pack()
canv.pack(fill=BOTH, expand=1)

balls=[]
colors = ['red','orange','yellow','green','blue'] #Палитра цветов на выбор
score=0 #score задаёт счётчик очков
k=0
def new_ball () : #создаёт новый шарик
    global x, y, r
    #canv.delete(ALL)
    x = rnd(100, 700)
    y = rnd(100, 500)
    r = rnd(30, 50)
    vx = rnd(-3,3)
    vy = rnd(-3,3)
    oval_1 = canv.create_oval(x-r, y-r, x+r, y+r, fill=choice(colors), width=0)
    ball={'oval': oval_1, 'x' : x, 'y' : y, 'r' : r, 'vx' : vx, 'vy' : vy}
    balls.append(ball)
    root.after(800, new_ball)
    l['text'] = 'Score: ' + str(score)


def click(event): #считет очки при попадании в шарик
    global score
    for k, b in enumerate(balls):
        if (b['x']-event.x)**2+(b['y']-event.y)**2<=b['r']**2:
            score+=2
            canv.delete(b['oval'])
            del balls[k]
    score-=1
    if score<0:
        exit()

def check_coords(): #отражает шарик на рандомный угол=
    for b in balls:
        v = (b['vx'] ** 2 + b['vy'] ** 2) ** 0.5
        beta = uniform(0, pi)
        if b['x']-b['r']<0 or b['x']+b['r']>800:
            b['vx'] = - v * cos(beta) * abs(b['vx'])/b['vx']
            b['vy'] = v * sin(beta)
        if b['y']-b['r']<0 or b['y']+b['r']>600:
            b['vy'] = -v * sin(beta) * abs(b['vy'])/b['vy']
            b['vx'] = v * cos(beta)
        canv.move(b['oval'], b['vx'], b['vy'])
        b['x'] += b['vx']
        b['y'] += b['vy']
    root.after(10, check_coords)
new_ball ()
check_coords()
canv.bind('<Button-1>', click)
mainloop()
