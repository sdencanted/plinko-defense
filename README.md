# Plinko Defence

Video - https://youtu.be/-1H2srazkdE

## Intro

You are an owner of a casino that specialises on plinko, a game where players insert steel balls into a pinball-like machine and hope that their balls reach the end for a payout. However, your machines are capable of destroying the balls before they reach the payout section! One day, a mysterious customer came who is able to insert balls of increasing strength. Upgrade your machine and prevent your casino from making huge losses!

## Instructions
Balls are served every 5 minutes, and have HP that increases with every drop. Prevent the balls from reaching the bottom of the stage by making them lose HP. The balls lose HP everytime they hit a pin. You also earn money from the balls hitting the pin. Use the money to buy upgrades! (so far there is only 1 upgrade) This upgrade increases the damage your pin deals, but also does not give you money when a ball hits it. The game ends when the balls that drop to the bottom deplete the payout of the machine.

## Code description
The game is based on kivy, with a kvlang embedded to simplify layouts.

The Window is fixed at 1366x768 pixels ( a common old widescreen monitor resolution) to avoid dealing with multiple layouts and resolutions.

The game runs on a clock that executes a function `game.update` 60 times a second. Within this function, the physics of the balls are recalculated, and values such as Money, Payout and Ball HP are also refreshed.

Ball and pin objects are created on demand, and indexed into a list for easy addition and removal. 

The pins are created on launch of the game inside `game.setup_pins`. This function will place them in a honeycomb-like pattern reminiscent of real plinko. 

The balls are created in the `game.update` function every 5 seconds. Their HP is a combination of the fixed value `20` and a value that increases with each ball `hpinc`. They start dropping from the dropper with 0 Y-velocity and a random X_velocity.

The dropper moves left and right on the top. Whether it moves left or right is controlled by the boolean `dropper.moving_right`.

The balls are checked for collision with pins in a nested for loop that `break`s once a successful collision is found. They are first filtered by minimum x-distance, then minimum y-distance, before having their diagonal distance calculated by the function `pythagoras`. If their diagonal distance is smaller than the sum of their radii, a collision has happened.

On collision, the function `collision_velocity` calulates the ball's new velocity. The ball's velocity is modified in polar coordinates. The angle of the ball's velocity is mirrored along the angle of collision. You can imagine this as the ball hitting a flat surface, where it gets deflected at an angle mirrored along the perpendicular of the flat surface. The angle is also slightly randomised so each game will not be the same.

Inter-ball collision is not considered as I am not prepared for the possibility of collision among 3 objects.