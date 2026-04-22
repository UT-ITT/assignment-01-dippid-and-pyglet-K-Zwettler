# Pong game

import pyglet
import time
from pyglet import window, shapes
from pyglet.gl import glClearColor
from DIPPID import SensorUDP

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
PORT = 5700

RECT_WIDTH = 10
RECT_HEIGHT = 300

# speed variables 
BASE_SPEED = 3.0
ACCCEL_FACTOR = 0.2

sensor = SensorUDP(PORT)
win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
# set background color
glClearColor(0.05, 0.08, 0.2, 1.0)

# starting time for every round
round_start = time.time()
vel_x = BASE_SPEED
vel_y = -BASE_SPEED
# counter for scoring points
counter = 0

rect_1 = shapes.Rectangle(40, 200, RECT_WIDTH, RECT_HEIGHT, (50, 153, 168))
rect_2 = shapes.Rectangle(950, 200, RECT_WIDTH, RECT_HEIGHT, (50, 153, 168))
ball = shapes.Circle(x=500, y=300, radius=30, color=(255, 255, 255))

# counter display 
points = pyglet.text.Label(str(counter),
                          font_name='Calibri',
                          font_size=36,
                          x=WINDOW_WIDTH//2, y=500,
                          anchor_x='center', anchor_y='center')

def update_rects():
    # check if sensor data is received
    if(not sensor.get_capabilities() == []):
        # Threshold for smooter operation
        if(sensor.get_value('gravity')['z'] > 1 or sensor.get_value('gravity')['z'] < -1):
            # bounding conditions
            if(rect_1.y + sensor.get_value('gravity')['z'] + RECT_HEIGHT > WINDOW_HEIGHT):
                rect_1.y = WINDOW_HEIGHT - RECT_HEIGHT
                rect_2.y = WINDOW_HEIGHT - RECT_HEIGHT
            elif(rect_1.y + sensor.get_value('gravity')['z'] < 0):
                rect_1.y = 0
                rect_2.y = 0
            # rectangles can be moved by tilting phone
            else:
                rect_1.y += sensor.get_value('gravity')['z']
                rect_2.y += sensor.get_value('gravity')['z']

def reset_game():
    global vel_x, vel_y, counter, round_start

    # reset game
    counter = 0
    ball.x = WINDOW_WIDTH / 2
    ball.y = WINDOW_HEIGHT / 2
    vel_x = BASE_SPEED
    vel_y = -BASE_SPEED
    round_start = time.time()

def update_ball():
    global vel_x, vel_y, counter, round_start

    passed_time = time.time() - round_start
    # increase speed proportional to passed time 
    speed = BASE_SPEED + ACCCEL_FACTOR * passed_time

    # set velocity
    vel_x = speed if vel_x >= 0 else -speed
    vel_y = speed if vel_y >= 0 else -speed

    # if ball is out of bounds, reset the game
    if ball.x + ball.radius < 0 or ball.x - ball.radius > WINDOW_WIDTH:
        reset_game()
   
    # let ball bounce off at bottom and top screen border
    if (ball.y - ball.radius) < 0 or (ball.y + ball.radius > WINDOW_HEIGHT):
        vel_y *= -1

    # let ball bounce off left rectangle
    if (
        # collision with rectangle 
        vel_x < 0
        and ball.x + ball.radius >= rect_1.x
        and ball.x - ball.radius <= rect_1.x + RECT_WIDTH
        and ball.y + ball.radius >= rect_1.y
        and ball.y - ball.radius <= rect_1.y + RECT_HEIGHT
    ):
        vel_x *= -1
        ball.x += 10
        # increase counter 
        counter += 1

    # let ball bounce off right rectangle
    if (
        # collision with rectangle
        vel_x > 0
        and ball.x - ball.radius <= rect_2.x + RECT_WIDTH
        and ball.x + ball.radius >= rect_2.x
        and ball.y + ball.radius >= rect_2.y
        and ball.y - ball.radius <= rect_2.y + RECT_HEIGHT
    ):
        vel_x *= -1
        ball.x -= 10
        # increase counter
        counter += 1

    # move ball   
    ball.x += vel_x
    ball.y += vel_y

@win.event
def on_draw():
    
    win.clear()

    update_rects()
    update_ball()
    # update counter display with current scroring points
    points.text = str(counter)

    rect_1.draw()
    rect_2.draw()
    ball.draw()
    points.draw()     


pyglet.app.run()