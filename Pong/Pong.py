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
        self.ball.update()

        # collision

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

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y


def line_circle_collision(x1, x2, y1, y2, circ_x, circ_y, circ_rad):
    distX = x1 - x2
    distY = y1 - y2
    line_len = math.sqrt((distX**2) + (distY**2))

    dot = (((circ_x - x1) * (x2 - x1)) + (circ_y - y1) * (y2 - y1)) \
        / line_len**2

    closestX = x1 + (dot * (x2 - x1))
    closestY = y1 + (dot * (y2 - y1))


App()
