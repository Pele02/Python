import turtle
from turtle import Turtle,Screen
import random

colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]
directions = [0 , 90, 180, 270]

turtle.colormode(255)
tim = Turtle()
tim.shape("turtle")
tim.color("green")
#tim.pencolor(random.choice(colours))
tim.pensize(15)
tim.speed("fastest")

my_screen = Screen()
my_screen.screensize(20000,15000)

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    random_color = (r, g, b)
    return random_color


finish = 100


while finish != 0:
    tim.color(random_color())
    tim.forward(30)
    tim.setheading(random.choice(directions))





my_screen.exitonclick()