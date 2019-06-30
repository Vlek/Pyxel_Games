import pyxel
import math


class App:
    def __init__(self):
        pyxel.init(120, 120)

        # inits
        self.paddle_width = 5
        self.paddle_height = 20
        self.paddle_speed = 1
        self.paddle_start_height = pyxel.height / 2 - self.paddle_height / 2

        # player
        self.player_paddle = Paddle(5, self.paddle_start_height,
                                    self.paddle_width, self.paddle_height)

        # enemy
        self.enemy_paddle = Paddle(110, self.paddle_start_height,
                                   self.paddle_width, self.paddle_height)

        # ball
        self.ball = Ball(pyxel.width/2, pyxel.height/2, 2)

        # run
        pyxel.run(self.update, self.draw)

    def update(self):  # check buttons
        # player movement
        if pyxel.btn(pyxel.KEY_DOWN) and self.player_paddle.y + \
                self.paddle_height + self.paddle_speed < pyxel.height:
            # add paddle speed to paddle height to keep pixel from going off
            # screen
            self.player_paddle.y += self.paddle_speed
        if pyxel.btn(pyxel.KEY_UP) and self.player_paddle.y > 0:
            self.player_paddle.y -= self.paddle_speed

        # ball movement
        curr_x_vel = self.ball.vel_x  # total number of movements we can make
        # this tick
        curr_y_vel = self.ball.vel_y

        while curr_x_vel > 0 or curr_y_vel > 0:
            new_ball_pos = self.ball.get_next_pos()
            # check collision with bottom of screen

            x_vel = 0  # number we will move
            if curr_x_vel > 0:
                curr_x_vel -= 1
                x_vel = 1

            y_vel = 0  # number we will move
            if curr_y_vel > 0:
                curr_y_vel -= 1
                y_vel = 1

            if line_circle(0 - self.ball.vel_x, pyxel.height,
                           pyxel.width + self.ball.vel_x,
                           pyxel.height + self.ball.vel_y,
                           new_ball_pos[0], new_ball_pos[1], self.ball.rad):
                self.ball.vel_y *= -1
            # check collision with top of screen
            if line_circle(0 - self.ball.vel_x, 0 - self.ball.vel_y,
                           pyxel.width + self.ball.vel_x, 0,
                           new_ball_pos[0], new_ball_pos[1], self.ball.rad):
                self.ball.vel_y *= -1

            self.ball.do_move(x_vel, y_vel)

    def draw(self):
        pyxel.cls(0)
        self.player_paddle.draw()
        self.enemy_paddle.draw()
        self.ball.draw()


class Paddle:  # 5 x 20 paddle size white
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.height = h
        self.width = w

    def draw(self):
        pyxel.rect(self.x, self.y, self.x + self.width,
                   self.y + self.height, 7)


class Ball:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.rad = r

        self.vel_x = 0
        self.vel_y = 1

    def draw(self):
        pyxel.circ(self.x, self.y, self.rad, 7)

    def get_next_pos(self):
        return [self.x + self.vel_x, self.y + self.vel_y]

    def change_velocity(self):
        pass

    def do_move(self, x, y):
        self.x += x
        self.y += y


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


def line_circle(x1, x2, y1, y2, cx, cy, cr):
    inside1 = point_circle(x1, y1, cx, cy, cr)
    inside2 = point_circle(x2, y2, cx, cy, cr)
    if inside1 or inside2:
        return True

    line_len = dist(x1, x2, y1, y2)

    dot = (((cx - x1) * (x2 - x1)) + (cy - y1) * (y2 - y1)) \
        / line_len**2

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


App()
