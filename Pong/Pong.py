import pyxel
import math


class Pong:
    def __init__(self):
        pyxel.init(120, 120)

        # inits
        self.paddle_width = 5
        self.paddle_height = 20
        self.paddle_speed = 1

        # starts at middle of screen (60px)
        self.paddle_start_height = pyxel.height / 2 - self.paddle_height / 2

        # player
        self.player_paddle = Paddle(5, self.paddle_start_height,
                                    self.paddle_width, self.paddle_height)

        # enemy
        self.enemy_paddle = Paddle(110, self.paddle_start_height,
                                   self.paddle_width, self.paddle_height)

        # ball
        # self.ball = Ball(pyxel.width/2, pyxel.height/2, 2)
        self.ball = Ball(25, 70, 2)

        # run
        pyxel.run(self.update, self.draw)

    def update(self):  # check buttons
        # player movement
        self.player_paddle.state = 0  # initializing state each update.
        if not(pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_UP)):
            if pyxel.btn(pyxel.KEY_DOWN) and self.player_paddle.y + \
                    self.paddle_height + self.paddle_speed < pyxel.height:
                # add paddle speed to paddle height to keep pixel from going
                # off screen
                self.player_paddle.y += self.paddle_speed
                self.player_paddle.state = 1
            if pyxel.btn(pyxel.KEY_UP) and self.player_paddle.y > 0:
                self.player_paddle.y -= self.paddle_speed
                self.player_paddle.state = -1

        # ball movement
        curr_x_vel = self.ball.vel_x  # total number of movements we can make
        # this tick based on the velocity
        curr_y_vel = self.ball.vel_y

        while curr_x_vel != 0 or curr_y_vel != 0:
            x_vel = 0  # number we will move
            if curr_x_vel > 0:
                curr_x_vel -= 1
                x_vel = 1
            elif curr_x_vel < 0:
                curr_x_vel += 1
                x_vel = -1

            y_vel = 0  # number we will move
            if curr_y_vel > 0:
                curr_y_vel -= 1
                y_vel = 1
            elif curr_y_vel < 0:
                curr_y_vel += 1
                y_vel = -1

            new_ball_pos = self.ball.get_next_pos(x_vel, y_vel)
            ball_x = new_ball_pos[0]
            ball_y = new_ball_pos[1]
            ball_r = self.ball.rad+1  # may need to double check

            collision_statement = "No collision"

            # check collision with bottom of screen
            if line_circle(0, pyxel.height, pyxel.width, pyxel.height,
                           ball_x, ball_y, ball_r):
                collision_statement = "bottom"
                self.ball.vel_y *= -1
                curr_y_vel *= -1

            # check collision with top of screen
            if line_circle(0, 0,
                           pyxel.width, 0,
                           ball_x, ball_y, ball_r):
                collision_statement = "top"
                self.ball.vel_y *= -1
                curr_y_vel *= -1

            # paddle collison top
            if line_circle(self.player_paddle.x, self.player_paddle.y,
                           self.player_paddle.x + self.player_paddle.width,
                           self.player_paddle.y, ball_x, ball_y, ball_r):
                collision_statement = "player paddle top"
                self.ball.vel_y *= -1
                curr_y_vel *= -1

            # paddle collison bottom
            if line_circle(self.player_paddle.x,
                           self.player_paddle.y + self.player_paddle.height,
                           self.player_paddle.x + self.player_paddle.width,
                           self.player_paddle.y + self.player_paddle.height,
                           ball_x, ball_y, ball_r):
                collision_statement = "player paddle bottom"
                self.ball.vel_y *= -1
                curr_y_vel *= -1

            # paddle collison right (top, middle, bottom)
            top_player_paddle_y1 = self.paddle_start_height
            top_player_paddle_y2 = self.paddle_start_height + \
                self.paddle_height * .2

            middle_player_paddle_y1 = top_player_paddle_y2
            middle_player_paddle_y2 = top_player_paddle_y2 + \
                self.paddle_height * .6

            bottom_player_paddle_y1 = middle_player_paddle_y2
            bottom_player_paddle_y2 = self.paddle_start_height + \
                self.player_paddle.height

            # top
            if line_circle(self.player_paddle.x + self.player_paddle.width,
                           top_player_paddle_y1,
                           self.player_paddle.x + self.player_paddle.width,
                           top_player_paddle_y2,
                           ball_x, ball_y, ball_r):
                collision_statement = "player paddle top right"
                # if self.player_paddle.state == -1:
                # self.ball.vel_x += 1
                self.ball.change_velocity(1)

                self.ball.vel_y *= -1
                curr_y_vel *= -1

            self.ball.do_move(x_vel, y_vel)
            print("Collided with", collision_statement,
                  "Current location: ", self.ball.x, ",",
                  self.ball.y, "Direction (x,y):", self.ball.vel_x,
                  self.ball.vel_y, "Paddle State: ", self.player_paddle.state,
                  file=file)

    def draw(self):
        pyxel.cls(0)
        # pyxel.rect(0,0,120,120,14)
        marker_space = 4
        marker_length = 6
        marker_width = 1
        box = marker_length + marker_space
        for i in range(pyxel.height//box):
            starting_y_pos = i * box
            starting_x_pos = pyxel.width / 2 - marker_width / 2
            pyxel.rect(starting_x_pos, starting_y_pos, marker_width,
                       marker_length, 7)
        self.player_paddle.draw()
        self.enemy_paddle.draw()
        self.ball.draw()


class Paddle:  # 5 x 20 paddle size white
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.height = h
        self.width = w
        # 0 = not moving, 1 = moving down, -1 = moving up
        self.state = 0

    def change_state(self, new_state):
        self.state = new_state

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 7)


class Ball:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.rad = r

        self.vel_x = -1
        self.vel_y = -1

    def draw(self):
        pyxel.circ(self.x, self.y, self.rad, 7)

    def get_next_pos(self, x, y):
        return [self.x + x, self.y + y]

    def change_velocity(self, x, y=0):
        self.vel_x = self.get_sign(x) * (abs(self.vel_x) + x)
        self.vel_y = self.get_sign(y) * (abs(self.vel_y) + y)

    def do_move(self, x, y):
        self.x += x
        self.y += y

    def get_sign(self, num):
        return -1 if num < 0 else 1


def point_point(x1: int, y1: int, x2: int, y2: int) -> bool:
    return x1 == x2 and y1 == y2


def point_circle(px: float, py: float, cx: float, cy: float, radius: float):
    return dist(px, py, cx, cy) <= radius


def circle_circle(c1x, c1y, c1r, c2x, c2y, c2r):
    return dist(c1x, c1y, c2x, c2y) <= c1r + c2r


def point_rect(px, py, rx, ry, rw, rh):
    return px >= rx and px <= rx + rw and py >= ry and py <= ry + rh


def rect_rect(r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h):
    return r1x + r1w >= r2x and r1x <= r2x + r2w and \
            r1y + r1h >= r2y and r1y <= r2y + r2h


def circle_rect(cx, cy, cr, rx, ry, rw, rh):
    testX = cx
    testY = cy

    if cx < rx:  # left side
        testX = rx
    elif cx > rx + rw:  # right side
        testX = rx + rw

    if cy < ry:  # top side
        testY = ry
    elif cy > ry + rh:  # bottom side
        testY = ry + rh

    return dist(cx, cy, testX, testY) <= cr


def line_point(x1, y1, x2, y2, px, py):
    d1 = dist(px, py, x1, y1)
    d2 = dist(px, py, x2, y2)

    line_len = dist(x1, y1, x2, y2)

    # double check, used 0.1. may not fit our scope
    buffer = 0.01

    return d1 + d2 >= line_len - buffer and d1 + d2 <= line_len + buffer


def line_circle(x1, y1, x2, y2, cx, cy, cr):
    inside1 = point_circle(x1, y1, cx, cy, cr)
    inside2 = point_circle(x2, y2, cx, cy, cr)
    if inside1 or inside2:
        return True

    line_len = dist(x1, x2, y1, y2)

    dot = (((cx - x1) * (x2 - x1)) + (cy - y1) * (y2 - y1)) \
        / line_len**2  # closest point on the line relative to the circle

# the closest x value that may or may not be on the line segment
    closestX = x1 + (dot * (x2 - x1))
    closestY = y1 + (dot * (y2 - y1))

    onSegment = line_point(x1, y1, x2, y2, closestX, closestY)

    if not onSegment:
        return False

    return dist(closestX, closestY, cx, cy) <= cr


def dist(x1, y1, x2, y2):
    distX = x1 - x2
    distY = y1 - y2
    return math.sqrt((distX**2) + (distY**2))


if __name__ == "__main__":
    file = open("./Pong/debug.txt", "w")
    Pong()
    file.close()
