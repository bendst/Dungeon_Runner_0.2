# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: player.py
Klassen: Player
Methoden: -
Autor: Ben Stuart
'''
from pyglet.window import key

import sprite


class Player(sprite.SpriteEntity):
    def __init__(self):
        super(Player, self).__init__("Spieler", 1, 2)
        self.powerup = {"life": 5}
        self.chest_key = False
        self.dm = 150
        self.distance = 0

    def p_move(self, dt, keys):
        # Verhalten bei Drücken der Taste D
        if keys[key.D]:
            if not self.wall and self.right:
                if self.dx <= 829:
                    self.on_move(self.dm * dt, 0)

            self.right = True
            self.left = False
            self.move = True

        # Verhalten bei Drücken der Taste A
        if keys[key.A]:
            if not self.wall and self.left:
                if self.dx >= 3:
                    self.on_move(-self.dm * dt, 0)
            self.left = True
            self.right = False
            self.move = True

        # Verhalten bei Drücken der Taste W
        # und der Bedingung das keine Decke berührt wird
        if keys[key.W]:
            self.jump = True
            # Legt spezielles Verhalten fest, falls eine Decke
            # berührt wird
            if self.top:
                self.jump = False
                self.distance = 40

            if self.jump and self.distance != 40:
                self.on_move(0, self.dm * dt)
                self.distance += 1

            elif self.distance == 40:
                self.jump = False

            if self.ground:
                self.distance = 0

        elif not keys[key.W]:
            self.jump = False

        if not self.ground and not self.jump:
            self.on_move(0, -150 * dt)
        # Der Spieler greift an
        if keys[key.SPACE] and self.allow_attack:
            self.attack = True

        if not keys[key.SPACE]:
            self.allow_attack = True

        # Laufanimation wird gestoppt
        if not keys[key.A] and not keys[key.D]:
            self.move = False
