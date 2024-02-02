from turtle import Turtle,Screen

def square():
    for _ in range(4):
        tim.forward(100)
        tim.right(90)

def dashed_line():
    for _ in range(15):
        tim.forward(10)
        tim.color("white")
        tim.forward(10)
        tim.color("black")

tim = Turtle()
tim.shape("turtle")
tim.color("green")
tim.pencolor("blue")


dashed_line()



screen = Screen()
screen.exitonclick()