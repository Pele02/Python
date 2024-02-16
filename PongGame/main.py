from turtle import Screen
from paddle import Paddle
# import time

RIGHT_POSITION = (375, 0)
LEFT_POSITION = (-380, 0)

game_on = True

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong Game")
screen.tracer(0)

l_paddle = Paddle(LEFT_POSITION)
r_paddle = Paddle(RIGHT_POSITION)

screen.listen()
screen.onkeypress(l_paddle.up, "w")
screen.onkeypress(l_paddle.down, "s")
screen.onkeypress(r_paddle.up, "Up")
screen.onkeypress(r_paddle.down, "Down")

while game_on:
    screen.update()
    # time.sleep(0.1)

screen.exitonclick()
