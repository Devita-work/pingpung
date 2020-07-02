from tkinter import *
import time
import random
from threading import Thread
from playsound import playsound 
from PIL import ImageTk, Image
import pyglet
import pygame
from os.path import abspath, dirname

BASE_PATH = abspath(dirname(__file__))
 
tk = Tk()
tk.title('Game')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=500, height=400, highlightthickness=0)
Image=ImageTk.PhotoImage(Image.open(BASE_PATH + '/bg.jpg'))
my_image = Image
canvas.create_image(0, 0, anchor=NW, image=my_image)
canvas.pack()
tk.update()
 
class Ball:
    def __init__(self, canvas, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-2, -1, 1, 2]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -2
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
 
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.score.hit()
                return True
        return False
 
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 2
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            canvas.create_text(250, 120, text='Вы проиграли', font=('Courier', 30), fill='red')
            pygame.mixer.music.stop()  
            
        if self.hit_paddle(pos) == True:
            self.y = -2
        if pos[0] <= 0:
            self.x = 2
        if pos[2] >= self.canvas_width:
            self.x = -2
 
 
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        start_1 = [40, 60, 90, 120, 150, 180, 200]
        random.shuffle(start_1)
        self.starting_point_x = start_1[0]
        self.canvas.move(self.id, self.starting_point_x, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.started = False
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)
 
    def turn_right(self, event):
        self.x = 2
 
    def turn_left(self, event):
        self.x = -2
 
    def start_game(self, event):
        self.started = True
 
    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0
 
 
class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 20, text=self.score, font=('Courier', 30), fill=color)
 
    def hit(self):
        self.score += 1
        jump.play()
        self.canvas.itemconfig(self.id, text=self.score)

def real_playsound () :
    sound = pyglet.media.load(BASE_PATH + '/1.mp3')
    sound.play()
    pyglet.app.run()

def pplaysound():
    global player_thread
    player_thread = Thread(target=real_playsound)
    player_thread.start()
 
pygame.init()

pygame.mixer.music.load(BASE_PATH + '/1.mp3')
pygame.mixer.music.set_volume(0.4)

jump = pygame.mixer.Sound(BASE_PATH + '/Jump.wav')

score = Score(canvas, 'Black')
paddle = Paddle(canvas, 'White')
ball = Ball(canvas, paddle, score, 'red')
def main():
    if ball.hit_bottom == False and paddle.started == True:
        ball.draw()
        paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)

pygame.mixer.music.play(loops=-1)
while 1:
    main()
