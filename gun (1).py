from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 100

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.live -= 1
        if self.x - self.r < 0 and self.x < 0:
            self.x = self.r
            self.vx = -0.8 *self.vx

        if self.x + self.r > 800 and self.x > 0:
            self.x = 800 - self.r
            self.vx = -0.8 *self.vx

        if self.y - self.r < 0 and self.vy > 0:
           self.y = self.r
           self.vy = -0.8*self.vy

        if self.y + self.r > 600 and self.vy < 0:
            self.y = 600 - self.r
            self.vy = -0.8*self.vy

            if self.vy < 5:
                self.vy = 0.6*self.vy
            if self.vy < 0.5:
                self.vy = 0



        self.x += self.vx
        self.y -= self.vy
        self.vy -= 1
        self.vx = 0.95*self.vx
        self.vy = 0.95*self.vy
        if abs(self.vx) < 4:
        	self.vx *= 0.96

        self.set_coords()
        if self.live < 0:
            balls.pop(balls.index(self))
            canv.delete(self.id)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (obj.r + self.r) ** 2:
            return True
        else:
            return False


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7) # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y-450) / (event.x-20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self):
        self.points = 0
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()
        self.live = 1

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(20, 50)
        vx = self.vx = rnd (-4, 4)
        vy = self.vy = rnd (-4, 4)
        color = self.color = 'red'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        global sum_of_points
        canv.coords(self.id, -10, -10, -10, -10)
        sum_of_points += points
        canv.itemconfig(id_points, text = sum_of_points)

    #def set_coords(self):
     #   canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.x + self.r)

    def move_target(self):
        '''Функция описывает движенеи целей'''
        if self.x-self.r < 0 or self.x + self.r > 800:
            self.vx = -self.vx
            self.vy = self.vy
        if self.y-self.r < 0 or self.y+self.r > 600:
            self.vy = -self.vy
            self.vx = self.vx
        canv.move(self.id, self.vx, self.vy)
        self.x += self.vx
        self.y += self.vy


sum_of_points = 0
t1 = target()
t2 = target()
screen1 = canv.create_text(400, 300, text='', font='28')
id_points = canv.create_text(30, 30, text = sum_of_points, font = '28')
g1 = gun()
bullet = 0
balls = []


def new_game(event=''):
    global gun, t1, t2, screen1, balls, bullet

    t1.new_target()
    t2.new_target()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)

    z = 0.03
    t1.live = 1
    t2.live = 1
    while (t1.live or t2.live) or balls:
        if t1.live:
            t1.move_target()
        if t2.live:
            t2.move_target()
        for b in balls:
            b.move()
            if b.hittest(t1) and t1.live:
                t1.live = 0
                t1.hit()
            if b.hittest(t2) and t2.live:
                t2.live = 0
                t2.hit()
            if (t1.live == 0) and (t2.live == 0):
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    root.after(750, new_game)


new_game()

root.mainloop()
