from tkinter import *
import random 
import pygame 

GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 75                   # How Fast will CANVAS Update => LOWER THE NUMBER, FASTER THE GAME
SPACE_SIZE = 25              # How large the item in the game like snake's body part and food 
BODY_PART = 3                # Initial number of body parts of the snake
SNAKE_COLOR = "#00FF00"      # Color of the snake (Green)
FOOD_COLOR = "#FF0000"       # Color of the food (Red)
BACKGROUND_COLOR = "#000000" # Background color of the game (Black)

pygame.mixer.init()

class Snake:
    def __init__(self):
        self.body_size = BODY_PART
        self.coordinates = []
        self.square = []

        for i in range(BODY_PART):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.square.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.square.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()  # Create new food
    else: 
        del snake.coordinates[-1]
        canvas.delete(snake.square[-1])
        del snake.square[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction
    if new_direction == "left" and direction != "right":
        direction = "left"
    elif new_direction == "right" and direction != "left":
        direction = "right"
    elif new_direction == "up" and direction != "down":
        direction = "up"
    elif new_direction == "down" and direction != "up":
        direction = "down"


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True 
    
    for every_body_part in snake.coordinates[1:]:
        if x == every_body_part[0] and y == every_body_part[1]:
            return True
        
    return False


def start_game():
    global score, direction, snake, food

    score = 0
    direction = "down"

    label.config(text=f"Score: {score}")

    canvas.delete(ALL)

    
    pygame.mixer.music.load("up-in-my-jam-all-of-a-sudden-by-kubbi.mp3")
    pygame.mixer.music.set_volume(0.3)  # Set volume to 30% (adjust as needed)
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    
    snake = Snake()
    food = Food()
    
    next_turn(snake, food)

def game_over():
    pygame.mixer.music.stop()
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 50, text="GAME OVER", fill="white", font=("consolas", 70))
    restart_button = Button(window, text="Restart Game", font=("consolas", 20), command=start_game)
    canvas.create_window(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 50, window=restart_button) 


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"
label = Label(window, text=f"Score: {score}", font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+{x}+{y}")

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

# Start the game
start_game()

window.mainloop()