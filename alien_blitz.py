import turtle
import random

try:
    import playsound  # Not part of standard Library.

    SOUND = True
except ImportError:
    SOUND = False

NUM_TOWERS = 20
MAX_TOWER_HEIGHT = 10
CURSOR_SIZE = 20
PLANE_DELAY = 40
BOMB_DELAY = 40
WIDTH = 800
HEIGHT = 600
cell_colors = ["black", "dark green", "brown"]


def move_plane():
    global playing
    new_pos = (plane.xcor(), plane.ycor())
    if new_pos[0] > width // 2:
        plane.goto(- width // 2, plane.ycor() - size)
    else:
        plane.goto(plane.xcor() + 12, plane.ycor())

    if check_plane_tower_collision():
        playing = False
        restart(new_level=False)
    elif check_player_wins_level():
        restart(new_level=True)
    else:
        screen.update()
        turtle.ontimer(move_plane, PLANE_DELAY)


def check_player_wins_level():
    if score >= winning_score:
        player_wins_level()
        return True
    return False


def player_wins_level():
    update_score_display()
    if SOUND:
        playsound.playsound("victory.wav")


def check_plane_tower_collision():
    for tower in towers:
        for cell in tower:
            if plane.distance(cell) <= size / 2 + 10:  # Half cell size + half plane height
                plane_tower_collision()
                return True
    return False


def plane_tower_collision():
    bomb.hideturtle()  # If present when plane crashes
    plane.color("red")
    screen.update()
    if SOUND:
        playsound.playsound("plane_crash.wav")


def check_bomb_tower_collision():
    if playing:
        for tower in towers:
            for cell in tower:
                if bomb.distance(cell) <= size / 2 + 5:  # Half cell size + half bomb size
                    bomb_tower_collision(cell)
                    return True
        return False


def bomb_tower_collision(cell):
    global score, high_score
    if SOUND:
        playsound.playsound("bombed.wav", False)
    cell.setx(-1000)
    cell.clear()
    score += 10
    if score > high_score:
        high_score = score
    update_score_display()


def start_bomb_drop():
    # Prevent further key presses until drop is finished tp prevent event stacking.
    screen.onkey(None, "space")
    bomb.goto(plane.xcor(), plane.ycor())
    bomb.showturtle()
    __continue_bomb_drop()


def __continue_bomb_drop():
    global playing
    bomb.goto(bomb.xcor(), bomb.ycor() - 12)
    if check_bomb_tower_collision() or bomb.ycor() < - height // 2 or not playing:
        stop_bomb_drop()
    else:
        turtle.ontimer(__continue_bomb_drop, BOMB_DELAY)


def stop_bomb_drop():
    bomb.hideturtle()
    # It's now safe to allow another bomb drop, so rebind keyboard event.
    screen.onkey(start_bomb_drop, "space")


def update_score_display():
    pen.clear()
    pen.write("Score:{:2} High Score:{:2}".format(score, high_score), align="center", font=("Courier", 24, "normal"))


def get_towers():
    result = []
    for col in range(-NUM_TOWERS // 2, NUM_TOWERS // 2):
        tower = []
        for level in range(random.randrange(1, MAX_TOWER_HEIGHT + 1)):
            block = turtle.Turtle(shape="square")
            block.shapesize(size / CURSOR_SIZE)
            block.color(random.choice(cell_colors))
            block.penup()
            block.goto(col * size + offset, - height // 2 + level * size + offset)
            tower.append(block)
        result.append(tower)
    return result


def setup():
    global screen, plane, bomb, pen, high_score, size, offset, height, width, score
    # Screen
    screen = turtle.Screen()
    screen.title("Alien Blitz")
    screen.setup(WIDTH, HEIGHT)
    screen.bgcolor("dark blue")
    screen.listen()
    screen.onkey(start_bomb_drop, "space")
    screen.tracer(0)

    # MISC.
    width = screen.window_width() - 50
    height = screen.window_height() - 50
    size = width / NUM_TOWERS  # Size of tower cells in pixels
    offset = (NUM_TOWERS % 2) * size / 2 + size / 2  # Center even and odd cells

    # Plane
    plane = turtle.Turtle(shape="triangle", visible=False)
    plane.color("yellow")
    plane.shapesize(20 / CURSOR_SIZE, 40 / CURSOR_SIZE)
    plane.penup()
    plane.goto(- width // 2, height // 2)
    plane.showturtle()

    # Bomb
    bomb = turtle.Turtle(shape="circle")
    bomb.hideturtle()
    bomb.color("red")
    bomb.shapesize(0.5)
    bomb.penup()

    # Score Display
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.color("white")
    pen.penup()
    pen.goto(0, 260)

    # Initialise high score
    high_score = 0


def restart(new_level=False):
    global score, high_score, winning_score, towers, playing
    #  Towers list does not exist on first call.
    try:
        for tower in towers:
            for cell in tower:
                cell.setx(-1000)
                cell.clear()
    except NameError:
        pass
    plane.color("yellow")
    towers = get_towers()
    # Here we handle the score for different scenarios for restarting the game - crashed plane or completed level.
    if not new_level:
        score = 0
        winning_score = sum(len(row) for row in towers) * 10
    else:
        winning_score += sum(len(row) for row in towers) * 10
    update_score_display()
    plane.goto(- width // 2, height // 2)
    bomb.goto(- width // 2, height // 2)
    playing = True
    screen.update()
    move_plane()


def main():
    setup()
    restart()


if __name__ == "__main__":
    main()
    turtle.done()
