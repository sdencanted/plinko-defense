import kivy
from kivy.lang import Builder

kivy.require('1.1.1')

from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import random
from kivy.config import Config

Config.set('graphics', 'resizable', False)

from math import sqrt, sin, cos, atan2, pi
from time import time

window_height = 768
window_width = 1366
game_height = 600
game_width = 800
Window.size = (window_width, window_height)

ball_damage = {
    'normal': 1,
    'boosted': 20
}
ball_color = {
    'normal': (1, 1, 1, 1),
    'boosted': (1, 0, 0, 1)
}

# embedded kvlang
build_holder = Builder.load_string('''
#:kivy 1.0.9

<PachinkoBall>:
    hp_display:hp_display
    size: 50, 50
    canvas:
        Color:
            rgba:150/256, 75/256, 0, 1
        Ellipse:
            pos: self.pos
            size: self.size
    Label:
        id: hp_display
        font_size: 24
        center:self.parent.center
        color: 0, 0, 0, 1
        text: "" if not hasattr(self.parent, 'hp') else str(self.parent.hp)

<Weapon>:
    size: 32,32
    canvas:
        Color:
            rgba:0, 1, 0, 1
        Ellipse:
            pos: self.pos
            size: self.size
<PachinkoDropper>:
    size: 200, 25
    canvas:
        Rectangle:
            pos:self.pos
            size:self.size

<PurchaseButton>:
    Button:
        size: 200, 20
        text: 'Buy Upgrade'
        on_press: self.parent.buybuybuy()
        pos: self.parent.pos

<MenuGrid>:
    pos:0,20
    size:1366,20
    canvas:
        Rectangle:
            pos:self.pos
            size:self.size

    cols:3
    row_force_default:True
    col_force_default:True
    row_default_height:20
    padding:10
    spacing:200
    purchase_btn:purchase_button

    PurchaseButton:
        id: purchase_button


<PachinkoGame>:
    wall:wall
    dropper: player_top
    menu_grid:menu_grid
    upgrade_money_display:upgrade_money_display
    payout_left_display:payout_left_display
    Widget:
        pos: self.parent.pos
        id:wall
        canvas:
            Rectangle:
                pos: self.center_x, 0
                size: 10, self.parent.height
    MenuGrid:
        id:menu_grid


    Label:
        id:upgrade_money_display
        font_size: 70
        center_x: root.width *4/ 5
        top: root.top - 50
        text: ""

    Label:
        id:payout_left_display
        font_size: 70
        center_x: root.width *4/ 5
        top: root.top - 120
        text: ""


    PachinkoDropper:
        id: player_top
        y: root.height-self.height
        #center_x: root.center_x




''')


class PachinkoDropper(Widget):
    score = NumericProperty(0)
    can_bounce = BooleanProperty(True)
    moving_right = True


class PachinkoBall(Widget):
    max_speed = 20
    hp_display = ObjectProperty(None)

    def __init__(self, maxhp=20, **kwargs):
        super(PachinkoBall, self).__init__(**kwargs)
        self.maxhp = maxhp
        self.hp = self.maxhp
        self.velocity_x = 0
        self.velocity_y = 0
        self.last_bounced_obj = None
        self.marked_for_death = False

    def move(self):
        self.hp_display.text = str(self.hp)
        change_canvas_color(self.canvas, (150 / 256, 75 / 256, 0, 1 * (self.hp / (self.maxhp + 0.5) + 0.5)))
        self.pos = Vector(*(self.velocity_x, self.velocity_y)) + self.pos
        self.velocity_y -= 1
        self.velocity_y = (min(self.velocity_y, self.max_speed)
                           if self.velocity_y > 0
                           else
                           max(self.velocity_y, -self.max_speed))


class PurchaseButton(Widget):
    def buybuybuy(self):
        self.parent.parent.buy_weapon()
        pass


class Weapon(Widget):
    # weapon_color= ObjectProperty(None)
    def __init__(self, weapon_type='normal', **kwargs):
        super(Weapon, self).__init__(**kwargs)
        self.has_clicked = False
        self.pin_type = weapon_type
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
    dropper = ObjectProperty(None)
    purchase_btn = ObjectProperty(None)
    save_layout_btn = ObjectProperty(None)
    upgrade_money_display = ObjectProperty(None)
    wall = ObjectProperty(None)
    menu_grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PachinkoGame, self).__init__(**kwargs)
        self.payout_left = 90
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

    def buy_weapon(self):
        if self.upgrade_money >= 5:
            self.upgrade_money -= 5
            self.weapon = Weapon("boosted")
            self.weapons.append(self.weapon)
            self.add_widget(self.weapon)
            self.weapon.center = Window.mouse_pos

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
        # update amount of money
        self.upgrade_money_display.text = "Money: " + str(self.upgrade_money)

        # update payout_left

        self.payout_left_display.text = "Payout left: " + str(self.payout_left) if self.payout_left > 0 else "U are ded"

        # reverse dropper direction at the sides
        if self.dropper.center_x >= game_width - self.dropper.width / 2:
            self.dropper.moving_right = False
        elif self.dropper.center_x <= self.dropper.width / 2:
            self.dropper.moving_right = True

        # move the dropper around
        self.dropper.center_x += 2 if self.dropper.moving_right else -2

        # move upgrade around
        if type(self.weapon) != type(None):
            if not self.weapon.has_clicked:

                # check for closest pin
                min_dist = window_width + window_height

                for weapon in self.weapons:
                    if (weapon.center_x - Window.mouse_pos[0] < min_dist
                            and weapon.center_y - Window.mouse_pos[1] < min_dist):
                        pythag_dist = pythagoras(weapon.center_x, weapon.center_y, Window.mouse_pos[0],
                                                 Window.mouse_pos[1])
                        if min_dist > pythag_dist:
                            min_dist = pythag_dist
                            self.min_weapon = weapon

                # snap upgrade to closest pin
                self.weapon.center = self.min_weapon.center

        # serve a ball every 5 seconds
        if self.last_served + 1 < time():
            self.last_served = time()

            # ball health increases with each drop
            self.ball = PachinkoBall(maxhp=20 + self.hpinc)
            self.hpinc += 1

            # add ball to list
            self.balls.append(self.ball)
            self.add_widget(self.ball)

            # initial ball position is at the dropper
            self.ball.center = self.dropper.center

            # initial ball velocity
            self.ball.velocity_x = 2 * random() - 1  # random
            self.ball.velocity_y = 0  # will change by gravity

        # process physics for each ball
        for ball in self.balls:
            # make ball move according to its velocity
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

                    # if the pin is actually an upgrade that hasn't been placed, skip it
                    if not weapon.has_clicked:
                        continue

                    # check that the ball did not collide with the pin recently
                    if ball.last_bounced_obj != weapon:

                        ball.last_bounced_obj = weapon

                        # calculate new velocity after collision
                        ball.velocity_x, ball.velocity_y = collision_velocity(
                            initial_v_x=ball.velocity_x,
                            initial_v_y=ball.velocity_y,
                            collision_x=ball.center_x - weapon.center_x,
                            collision_y=ball.center_y - weapon.center_y
                        )

                        # execute effects on hitting ball
                        ball.hp -= ball_damage[weapon.pin_type]
                        if weapon.pin_type == "normal":
                            self.upgrade_money += 1

                        # our ball is likely to collide with only 1 pin, skip the other pins
                        break
                else:
                    # lets the pin collide with the ball again once they are separated
                    if ball.last_bounced_obj == weapon:
                        ball.last_bounced_obj = None
                    pass

        # clear balls that have dropped to the bottom or have their HP depleted:
        for ball in list(self.balls):
            if ball.marked_for_death or ball.hp <= 0:
                self.payout_left -= (max(ball.hp, 0))  # payout will only decrease if the ball dropped with HP

                # remove dead balls from list
                self.remove_widget(ball)
                self.balls.remove(ball)


def change_canvas_color(canvas, color):
    for i in canvas.get_group(None):
        if type(i) is Color:
            i.r, i.g, i.b, i.a = color
            return


def collision_velocity(initial_v_x, initial_v_y, collision_x, collision_y):
    vel_theta = atan2(initial_v_y, initial_v_x)
    col_theta = atan2(collision_y, collision_x)
    theta_diff = col_theta - vel_theta
    if abs(theta_diff) > pi:
        new_theta_diff = 2 * pi - abs(theta_diff)
        new_theta = col_theta + new_theta_diff * (1 if theta_diff < 0 else -1)
    else:
        new_theta = (col_theta + theta_diff) * (1 - (random() - 0.5) / 5)
    new_x = pythagoras(initial_v_x, initial_v_y) * cos(new_theta - pi)
    new_y = pythagoras(initial_v_x, initial_v_y) * sin(new_theta - pi)
    return new_x, new_y * 0.7


def pythagoras(x1, y1, x2=0, y2=0):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def is_colliding(obj1, obj2):
    collide_dist = (obj1.height + obj2.height) / 2
    # print(collide_dist)
    if abs(obj1.center_x - obj2.center_x) <= collide_dist and abs(obj1.center_y - obj2.center_y) <= collide_dist:
        if pythagoras(obj1.center_x, obj1.center_y, obj2.center_x, obj2.center_y) <= collide_dist:
            return True
    return


class PlinkoApp(App):

    def build(self):
        game = PachinkoGame()

        game.setup_pins()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PlinkoApp().run()
