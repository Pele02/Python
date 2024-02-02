from turtle import Turtle, Screen, colormode
import turtle
import random

turtle.colormode(255)
tim = Turtle()
tim.shape("turtle")
tim.speed("fastest")
my_screen = Screen()


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    color = (r, g, b)
    return color


for angle in range(0, 361, 5):
    tim.circle(100)
    tim.setheading(angle)
    tim.color(random_color())

my_screen.exitonclick()
