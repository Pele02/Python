import colorgram
import turtle
from turtle import Turtle, Screen
import math

tim = Turtle()
my_screen = Screen()
turtle.colormode(255)
rgb_colors = []
colors = colorgram.extract('image.jpg', 35)
for color in colors:
    r = color.rgb.r
    g = color.rgb.g
    b = color.rgb.b
    new_color = (r, g, b)
    rgb_colors.append(new_color)

color_length = len(rgb_colors)
y = -166.78
tim.penup()
tim.setheading(225)
tim.forward(250)
print(tim.position())
tim.setheading(0)
tim.pendown()

for dot in range(0, color_length, 1):
    tim.color(rgb_colors[dot])
    tim.dot(20)
    tim.penup()
    tim.forward(50)
    dot += 1
    if dot % int(math.sqrt(color_length)) == 0:
        tim.home()
        tim.goto(-176.78, y)
    dot -= 1
    y += 10


my_screen.exitonclick()
