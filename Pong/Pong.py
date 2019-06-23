import pyxel

class App:
    def __init__(self):
        pyxel.init(120, 120)

        self.paddle_width = 5
        self.paddle_height = 20
        self.paddle_speed = 1

        self.player_paddle = Paddle(5, 5, self.paddle_width, self.paddle_height)
        self.enemy_paddle = Paddle(110, 5, self.paddle_width, self.paddle_height)


        pyxel.run(self.update, self.draw)

    def update(self): #check buttons
        if pyxel.btn(pyxel.KEY_DOWN) and \
        self.player_paddle.y + self.paddle_height + self.paddle_speed < pyxel.height:
        # add paddle speed to paddle height to keep pixel from going off screen
            self.player_paddle.y += self.paddle_speed
        if pyxel.btn(pyxel.KEY_UP) and self.player_paddle.y > 0:
            self.player_paddle.y -= self.paddle_speed

    def draw(self):
        pyxel.cls(0)
        self.player_paddle.draw()
        self.enemy_paddle.draw()

class Paddle: #5 x 20 paddle size white
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.height = h
        self.width = w

    def draw(self):
        pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, 7)


App()
