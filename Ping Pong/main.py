# File: Pong/main.py
# This file is part of the Pong game project.
import turtle
import time 
import pygame

pygame.mixer.init()
bounce_sound = pygame.mixer.Sound("bounce.wav")

def setup_screen():
    wn = turtle.Screen()
    wn.title("Pong Game")
    wn.bgcolor("black")
    wn.setup(width=800, height=600)
    wn.tracer(0)  # Turns off the screen updates for better performance
   
    # Disable window resizing
    wn.getcanvas().master.resizable(False, False)
    return wn

def generate_object(x:int, y:int, shape:str, color:str, width:int, len: int ) -> turtle.Turtle:
    object = turtle.Turtle()
    object.speed(0)
    object.shape(f"{shape}")
    object.color(f"{color}")
    object.shapesize(stretch_wid=width, stretch_len=len)
    object.penup()  # Prevents drawing lines when moving
    object.goto(x, y)  # Initial position of the object
    return object

def paddle_up(paddle: turtle.Turtle):
    y = paddle.ycor()
    if y < 250:
        paddle.sety(y + 20)

def paddle_down(paddle: turtle.Turtle):
    y = paddle.ycor()
    if y > -240: 
        paddle.sety(y - 20)

def ball_movement(ball: turtle.Turtle, paddle_a: turtle.Turtle, paddle_b: turtle.Turtle
                  , score_a: int, score_b: int):
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        bounce_sound.play()

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        bounce_sound.play()

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        bounce_sound.play()

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        bounce_sound.play()

    # Paddle collision
    if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1
        bounce_sound.play()

    if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.setx(-340)
        ball.dx *= -1
        bounce_sound.play()

    return score_a, score_b

def make_pen():
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    return pen

if __name__ == "__main__":

    score_a = 0
    score_b = 0

    screen = setup_screen()

    paddle_a = generate_object(-350, 0, "square", "white", 5, 1)
    paddle_b = generate_object(350, 0, "square", "white", 5, 1)
    ball = generate_object(0, 0, "circle", "white", 1, 1)
    ball.dx = 2 # everytime the ball moves, it will move 2 pixels in the x direction
    ball.dy = 2 # everytime the ball moves, it will move 2 pixels in the y direction

    # keyboard bindings
    screen.listen()
    screen.onkeypress(lambda: paddle_up(paddle_a), "w")  # Paddle A up
    screen.onkeypress(lambda: paddle_down(paddle_a), "s")  # Paddle A down
    screen.onkeypress(lambda: paddle_up(paddle_b), "Up")  # Paddle B up
    screen.onkeypress(lambda: paddle_down(paddle_b), "Down")  # Paddle B down

    # Create the game title and instructions
    pen = make_pen()

    # Main game loop
    while True:
        screen.update()

        # Move the ball 
        score_a, score_b = ball_movement(ball, paddle_a= paddle_a, paddle_b=paddle_b, score_a=score_a, score_b=score_b)
        pen.clear()
        pen.write(f"Player A: {score_a}  Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

        time.sleep(0.01)

        # Check for exit condition
        if score_a >= 2:
            pen.clear()
            pen.write("Player A wins!", align="center", font=("Courier", 24, "normal"))
            screen.update()
            time.sleep(2)
            break
        elif score_b >= 2:
            pen.clear()
            pen.write("Player B wins!", align="center", font=("Courier", 24, "normal"))
            screen.update()
            time.sleep(2)
            break

    screen.bye()  # Close the window when the game ends