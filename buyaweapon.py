import kivy
from kivy.core.window import Window
from random import random
from math import sqrt, sin, cos, atan2, pi
import pickle
from time import time
# fix window size
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Rectangle

Config.set('graphics', 'resizable', False)

# to get mouse input

window_height = 768
window_width = 1366
game_height = 600
game_width = 800
Window.size = (window_width, window_height)

kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty
)
from kivy.vector import Vector
from kivy.clock import Clock


class PachinkoDropper(Widget):
    score = NumericProperty(0)
    can_bounce = BooleanProperty(True)
    moving_right = True


ball_damage = {
    'normal': 1,
    'boosted': 20
}
ball_color = {
    'normal': (1, 1, 1, 1),
    'boosted': (1, 0, 0, 1)
}


class PachinkoBall(Widget):
    maxspeed = 20
    hp_display = ObjectProperty(None)

    def __init__(self, maxhp=20, **kwargs):
        super(PachinkoBall, self).__init__(**kwargs)
        self.maxhp = maxhp
        self.hp = self.maxhp
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_bounced = None
        self.marked_for_death = False
        # self.Pachinkohp=PachinkoHP()
        # self.add_widget(self.Pachinkohp)

    def move(self):
        self.hp_display.text = str(self.hp)
        change_canvas_color(self.canvas, (150 / 256, 75 / 256, 0, 1 * (self.hp / (self.maxhp + 0.5) + 0.5)))
        self.pos = Vector(*(self.velocity_x, self.velocity_y)) + self.pos
        self.velocity_y -= 1
        self.velocity_y = min(self.velocity_y, self.maxspeed) if self.velocity_y > 0 else max(self.velocity_y,
                                                                                              -self.maxspeed)


class PurchaseButton(Widget):
    def buybuybuy(self):
        print("Pootis")
        self.parent.parent.buy_weapon()
        pass


class SaveLayoutButton(Widget):
    def save_layout(self):
        print("Spencer")
        self.parent.parent.save_layout()
        pass


class LoadLayoutButton(Widget):
    def load_layout(self):
        print("Spencer")
        self.parent.parent.load_layout()
        pass


def change_canvas_color(canvas, color):
    for i in canvas.get_group(None):
        if type(i) is Color:
            i.r, i.g, i.b, i.a = color
            return


class Weapon(Widget):
    # weapon_color= ObjectProperty(None)
    def __init__(self, weapon_type='normal', **kwargs):
        super(Weapon, self).__init__(**kwargs)
        self.has_clicked = False
        self.pin_type = weapon_type
        # while not self.has_clicked:
        #    self.move_weapon()
        # print(dir(self.canvas))
        # self.canvas.add(Color(rgba=ball_color[self.pin_type]))
        """
        for i in self.canvas.get_group(None):
            if type(i) is Color:
                print("pootis")
                i.r, i.g, i.b, i.a = ball_color[self.pin_type]
                print(i)
                break
        """
        change_canvas_color(self.canvas, ball_color[self.pin_type])

    def move_weapon(self):
        self.center = Window.mouse_pos

    def on_touch_down(self, touch):
        if not self.has_clicked:
            # weapon_color = ObjectProperty(None)
            self.has_clicked = True
            self.parent.remove_old_weapon()
            # self.center = Window.mouse_pos


class MenuGrid(GridLayout):
    pass


class PachinkoGame(Widget):
    global ball_damage
    # ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    purchase_btn = ObjectProperty(None)
    save_layout_btn = ObjectProperty(None)
    upgrade_money_display = ObjectProperty(None)
    wall = ObjectProperty(None)
    menu_grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PachinkoGame, self).__init__(**kwargs)
        self.wallet = 90
        self.hpinc = 0
        self.last_served = time() - 10
        self.balls = []
        self.ball = None
        self.weapons = []
        self.weapon = None
        self.upgrade_money = 0
        self.min_weapon = None
        self.wall.center_x = game_width
        self.menu_grid.center_y = window_height - game_height

    def save_layout(self):
        coordinates = []
        for weapon in self.weapons:
            coordinates.append([weapon.center_x, weapon.center_y])
        with open('layout.data', 'wb') as filehandle:
            # store the data as binary data stream
            pickle.dump(coordinates, filehandle)

    def load_layout(self):
        with open('layout.data', 'rb') as filehandle:
            # store the data as binary data stream
            coordinates = pickle.load(filehandle)
        self.ball.is_bounced = None
        # remove previous obstacles
        for weapon in self.weapons:
            self.remove_widget(weapon)
        self.weapons = []

        for coordinate in coordinates:
            self.weapon = Weapon()
            self.weapons.append(self.weapon)
            self.add_widget(self.weapon)
            self.weapons[-1].center_x = coordinate[0]
            self.weapons[-1].center_y = coordinate[1]
            self.weapons[-1].has_clicked = True

    def buy_weapon(self):
        if self.upgrade_money >= 5:
            self.upgrade_money -= 5
            self.weapon = Weapon("boosted")
            self.weapons.append(self.weapon)
            self.add_widget(self.weapon)
            self.weapon.center = Window.mouse_pos

    def serve_ball(self, velx=2, vely=-1):
        self.ball.center = self.player1.center

        self.ball.velocity_x = velx
        self.ball.velocity_y = vely

    def setup_pins(self, rows=9, width=100, height=100):
        margin = 70
        for row, height in enumerate([x * height + (window_height - game_height + 30) for x in range(rows)]):
            currentx = margin + width * (row % 2) / 2
            while currentx < game_width - margin:
                self.weapon = Weapon()
                self.weapons.append(self.weapon)
                self.add_widget(self.weapon)
                self.weapons[-1].center_x = currentx
                self.weapons[-1].center_y = height
                self.weapons[-1].has_clicked = True
                currentx += width

    def remove_old_weapon(self):

        self.remove_widget(self.min_weapon)
        self.weapons.remove(self.min_weapon)

    def update(self, dt):
        #   update amount of moneys
        self.upgrade_money_display.text = "Money: "+ str(self.upgrade_money)

        # update wallet

        self.wallet_display.text = "Wallet: "+ str(self.wallet) if self.wallet>0 else "U are ded"

        #   end game if wallet is ded
        if self.wallet <= 0:
            print("your face is DIE!")
            #TODO: actually end the game

        # serve a ball every 5 seconds
        elif self.last_served + 1 < time():
            self.last_served = time()
            self.ball = PachinkoBall(maxhp=20 + self.hpinc)
            self.hpinc += 1
            self.balls.append(self.ball)
            self.add_widget(self.ball)
            self.ball.center = self.player1.center
            self.ball.velocity_x = 2
            self.ball.velocity_y = 0

        # clear balls that have dropped / deduct from wallet
        for ball in list(self.balls):
            if ball.marked_for_death or ball.hp <= 0:
                self.wallet -= (max(ball.hp, 0))
                self.remove_widget(ball)
                self.balls.remove(ball)
        """   
        for i in xrange(len(self.balls) - 1, -1, -1):
            element = somelist[i]
            do_action(element)
            if ball.marked_for_death:
                self.remove_widget(ball)
                del self.balls[i]
        """
        # move droppper
        """
        mouse_x = Window.mouse_pos[0]
        mouse_y = Window.mouse_pos[1]
        if mouse_y > self.height - 200:
            self.player1.center_x = mouse_x
        """
        if self.player1.center_x >= game_width - self.player1.width / 2:
            self.player1.moving_right = False
        elif self.player1.center_x <= self.player1.width / 2:
            self.player1.moving_right = True
        if self.player1.moving_right:
            self.player1.center_x += 2
            pass
        else:
            self.player1.center_x -= 2

        # move purchased weapon around
        if type(self.weapon) != type(None):
            if not self.weapon.has_clicked:
                # check for closest weapon
                min_dist = window_width + window_height
                for weapon in self.weapons:
                    if weapon.center_x - Window.mouse_pos[0] < min_dist and weapon.center_y - Window.mouse_pos[
                        1] < min_dist:
                        pythag_dist = pythagoras(weapon.center_x, weapon.center_y, Window.mouse_pos[0],
                                                 Window.mouse_pos[1])
                        if min_dist > pythag_dist:
                            min_dist = pythag_dist
                            self.min_weapon = weapon
                # Window.mouse_pos
                self.weapon.center = self.min_weapon.center

        # run process for each ball
        for ball in self.balls:
            # process ball movement
            ball.move()

            # mark ball to disappear on next tick when dropped into floor
            if ball.y < (window_height - game_height):
                ball.marked_for_death = True

            # bounce ball off sides
            if ball.x > game_width - ball.height:
                ball.velocity_x = -abs(ball.velocity_x)
            elif ball.x <= 0:
                ball.velocity_x = abs(ball.velocity_x)

            # ball collision
            for weapon in self.weapons:
                if is_colliding(weapon, ball):
                    if not weapon.has_clicked:
                        continue

                    # print('painis')

                    if ball.is_bounced != weapon:
                        ball.is_bounced = weapon
                        vx, vy = ball.velocity_x, ball.velocity_y
                        dy = ball.center_y - weapon.center_y
                        dx = ball.center_x - weapon.center_x
                        veltheta = atan2(vy, vx)
                        coltheta = atan2(dy, dx)
                        thetadiff = coltheta - veltheta
                        if abs(thetadiff) > pi:
                            newthetadiff = 2 * pi - abs(thetadiff)
                            newtheta = coltheta + newthetadiff * (1 if thetadiff < 0 else -1)
                        else:
                            newtheta = (coltheta + thetadiff) * (1 - (random() - 0.5) / 5)
                        newx = pythagoras(vx, vy) * cos(newtheta - pi)
                        newy = pythagoras(vx, vy) * sin(newtheta - pi)
                        bounced = Vector(newx, newy)
                        vel = bounced * 1
                        ball.velocity_x, ball.velocity_y = vel.x, vel.y * 0.7  # + offset
                        # print(vx, vy, veltheta, coltheta, newtheta)

                        # execute effects on hitting ball
                        ball.hp -= ball_damage[weapon.pin_type]
                        if weapon.pin_type == "normal":
                            self.upgrade_money += 1

                        # our ball is likely to collide with only 1 pin
                        continue
                else:
                    if ball.is_bounced == weapon:
                        ball.is_bounced = None
                    pass


def pythagoras(x1, y1, x2=0, y2=0):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def is_colliding(obj1, obj2):
    collide_dist = (obj1.height + obj2.height) / 2
    # print(collide_dist)
    if abs(obj1.center_x - obj2.center_x) <= collide_dist and abs(obj1.center_y - obj2.center_y) <= collide_dist:
        if pythagoras(obj1.center_x, obj1.center_y, obj2.center_x, obj2.center_y) <= collide_dist:
            return True
    return


def distance(center1, center2):
    xydist = [abs(a_i - b_i) for a_i, b_i in zip(center1, center2)]
    return sqrt(sum(xydist))


class WeaponApp(App):

    def build(self):
        game = PachinkoGame()
        
        game.setup_pins()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    WeaponApp().run()
