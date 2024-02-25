from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Score
import time

RIGHT_POSITION = (375, 0)
LEFT_POSITION = (-380, 0)
TIME = 0.1

game_on = True

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong Game")
screen.tracer(0)

l_paddle = Paddle(LEFT_POSITION)
score = Score()
r_paddle = Paddle(RIGHT_POSITION)
ball = Ball()


screen.listen()
screen.onkeypress(l_paddle.up, "w")
screen.onkeypress(l_paddle.down, "s")
screen.onkeypress(r_paddle.up, "Up")
screen.onkeypress(r_paddle.down, "Down")

while game_on:
    time.sleep(TIME)
    screen.update()
    ball.move_ball()

    # Detect collision with wall
    if ball.ycor() == 290 or ball.ycor() == -290:
        ball.bounce_y()

    # Detect collision with paddle
    if ball.distance(r_paddle) < 55 and ball.xcor() > 350 or ball.distance(l_paddle) < 55 and ball.xcor() < -350:
        ball.bounce_x()
        TIME /= 1.2

    # Paddle right miss the ball
    if ball.xcor() == 380:
        TIME = 0.1
        ball.reset_position()
        score.l_point()

    # Paddle left miss the ball
    if ball.xcor() == -380:
        TIME = 0.1
        ball.reset_position()
        score.r_point()


screen.exitonclick()
