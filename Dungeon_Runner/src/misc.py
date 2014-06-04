# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: misc.py
Klassen: Potion, Heartbar, Key
Methoden: -
Autor: Ben Stuart
'''
import random

import sprite


class Potion(sprite.SpriteEntity):
    def __init__(self):
        # Wird "zufällig" entschieden ob ein Gegner einen Trank fallen
        # lässt
        self.potion = random.randint(0, 1)
        self.drop = False
        super(Potion, self).__init__("life", 1, 2)
        self.hitbox.resize_box(1, 1)

        if self.potion != 0:
            self.alive = False

        self.remove_graphic(self)

    def update_spawn(self, x, y):
        # Falls der Trank "lebt" wird seine Position aktualisiert
        if self.alive:
            self.set_position(x, y)

    def potion_spawn(self):
        # Fügt den Trank zur Zeichen Methode hinzu
        self.attach_graphic(self, 1)

    def collect(self, x, y):
        # Ist der Trank am leben wird überprüft
        # ob diser aufgesammelt werden kann

        if self.alive:
            self.hitbox.set_point(self.dx, self.dy - 8)
            # wenn True wird er von der Zeichen Methode entfernt
            if self.hitbox.h_get_collision(x, y):
                self.alive = False
                self.remove_graphic(self)
                return True

    def e_move(self, dt):
        # Verhindert, dass Tränke von in der Luft besiegten Gegnern
        # hängenbleiben
        if self.drop and not self.ground:
            self.on_move(0, -150 * dt)


class Heartbar(sprite.SpriteEntity):
    def __init__(self):
        super(Heartbar, self).__init__(name="H", width=1, height=2)

    def set_status(self, life_size):
        # Aktualisiert die Anazhl der Herzen
        if len(self.std_tile) / 8 != life_size:
            self.std_tile = self.set_tile(1, 2, life_size)
            self.on_move(10, 600)
            self.tex_gl = self.tex_coord * life_size
            self.tile_gl = self.std_tile


class Key(sprite.SpriteEntity):
    def __init__(self, x, y):
        super(Key, self).__init__(name="Key", width=1, height=2)
        self.drop = False
        self.alive = False
        self.remove_graphic(self)
        self.set_position(x, y)

    def spawn(self):
        # Lässt den Schlüssel erscheinen, wenn er nicht vorhanden ist
        if not self.drop:
            self.drop = True
            self.alive = True
            self.attach_graphic(self, 1)

    def collect(self, x, y):
        if self.alive:
            self.hitbox.set_point(self.dx, self.dy - 8)
            if self.hitbox.h_get_collision(x, y):
                self.alive = False
                self.remove_graphic(self)
                print "Collect"
                return True

    def e_move(self, dt):
        if self.drop:
            if not self.ground:
                self.on_move(0, -100 * dt)
