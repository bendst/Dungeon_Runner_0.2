# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: sprite.py
Klassen: SpriteEntity
Methoden: -
Autor: Ben Stuart
'''
import time
from pyglet.gl import *

import xmlopen
import vec
import graphic


class SpriteEntity(graphic.Graphic, vec.Matrix):
    def __init__(self, name, width, height,
                 filename="spsh_xml/spritesheet.xml"):
        # private Variablen
        self._name = name
        self._file = filename
        # Diverse Zustände des Sprites
        self.attack = False
        self.alive = True
        self.left = False
        self.right = True
        self.jump = False
        self.move = False
        self.wall = True
        self.ground = True
        self.top = False

        self.allow_attack = True
        self.allow_damage = True
        self.duration = 0

        self.dx = 0
        self.dy = 0

        # self.texture_index = 0
        self.std_tile = self.set_tile(width, height, 1)
        # Erhält die zugewiesene Bilddatei für den Sprite
        self._xml = xmlopen.XmlEntity(self._file)
        self._image = self._xml.get_dict[name][1][1]
        # Verwendeet Initialisiert das Graphic Modul und die damit verbundene
        # Texture Klasse
        super(SpriteEntity, self).__init__(self._image, 4, 8)
        self._image_index = self._xml.get_dict[name][0][1]
        # Property Setter
        self.tile_gl = self.std_tile
        self.tex_gl = self.tex_coord
        # Bindet die Textur an den Sprite
        self.bind_tex()
        # Andere vererbte Objekte werden verwendet
        vec.Matrix.__init__(self)
        self.set_matrix(self.std_tile)

        self.hitbox = vec.Hitbox()
        self.hitbox.resize_box(1, 2)

        self.attach_graphic(self, 1)

    def set_position(self, dx, dy):
        # Setzt die Spielerposition
        self.dx = dx
        self.dy = dy
        self.set_tile(1, 2, 1)
        self.set_matrix(self.std_tile)
        self.translate(dx, dy)
        # Übergabe an das graphic Modul
        self.tile_gl = self.std_tile
        self.clear()

    def get_tile(self):
        return self.std_tile

    def set_tex_tile(self, *texture_index):
        # Ermöglicht es mehrere Texturen aneinander zureihen
        # die Reihenfolge ist dabei relavant
        new = []
        for i in texture_index:
            self.texture_index = i
            new.extend(self.tex_coord)
        self.tex_gl = new

    def set_tile(self, tile_width, tile_height, size_w, default=True):
        # Ermöglicht es die Größe einer Fläche
        # sowie die Wiederholung dieser Fläche auf X - Achse
        # Beispielsweise kann dadurch aus einer Liste mit 8 Koordinatenpunkten
        # eine Liste mit 16 Koordinatenpunkten werden
        new = []
        i = 0
        n = 0
        width = tile_width * 32.0
        height = tile_height * 32.0

        while True:
            if len(new) == (size_w * 8):
                break

            if i == 0:
                new.append(width * n)
                new.append(0.0)
            elif i == 1:
                new.append(width * n + width)
                new.append(0.0)
            elif i == 2:
                new.append(width * n + width)
                new.append(height)
            elif i == 3:
                new.append(width * n)
                new.append(height)

            i += 1

            if i == 4:
                i = 0
                n += 1

        if default:
            self.std_tile = new
            return self.std_tile
        else:
            return new

    @property
    def tex_coord(self):
        return self.get_texcoords(int(self._image_index) + self.texture_index)

    def normal_reset(self):
        # Setzt den Sprite auf die Standardeinstellungen
        self.tex_gl = self.texture_index
        self.tile_gl = self.set_tile(1, 2)
        self.set_matrix(self.std_tile)

    def on_move(self, dx, dy):
        # Setzt die zu manipulierende Liste
        self.set_matrix(self.std_tile)
        # Verschiebt den Sprite in der Matrix - Klasse
        self.translate(dx, dy)
        # Übergibt den Sprite an das graphic Modul
        self.tile_gl = self.std_tile
        # Die Matrix wird zurückgesetzt
        self.clear()
        # Die öffentlichen variablen werden aktualisiert
        self.dx += dx
        self.dy += dy

    def on_animate(self, l_atk1, l_atk2, r_atk1, r_atk2, l_s, r_s):
        # Animation des Charakters während er nicht angreift
        if not self.attack:
            # Setzt die Textur neu
            if len(self.std_tile) != 8:
                if self.right:
                    self.set_tex_tile(r_s)
                else:
                    self.set_tex_tile(l_s)
            # Laufanimation zur rechten Seite hin
            if self.move and self.right:
                if self.texture_index > 3:
                    self.texture_index = 1
                self.texture_index += 1
            # Laufanimation zur linken Seite hin
            elif self.move and self.left:
                if self.texture_index < 20:
                    self.texture_index = 23
                self.texture_index -= 1
            # Der Charakter bewegt sich nicht
            # Entsprechender Textur Index wird gesetzt
            else:
                if self.right:
                    self.texture_index = 0
                else:
                    self.texture_index = 23
            # Setzt die Fläche
            self.set_tile(1, 2, 1)
            self.set_matrix(self.std_tile)
            self.translate(self.dx, self.dy)
            # Setzt die Textur
            self.set_tex_tile(self.texture_index)
            # Übergabe an das graphic Modul
            self.tile_gl = self.std_tile
            self.clear()
        # Der Sprite greift an
        else:
            # Erster Angriffstimer wird gesetzt
            if self.duration == 0:
                self.attack_time1 = time.time()
                self.duration += 1
            # Passt die Größe der Fläche an
            if len(self.std_tile) != 16:
                self.set_tile(1, 2, 2)
                if self.right:
                    # Vergrößert die sichtbare Textur
                    self.set_tex_tile(r_atk1, r_atk2)
                    self.set_matrix(self.std_tile)
                    self.translate(self.dx, self.dy)
                    # Übergibt an das graphic Modul
                    self.tile_gl = self.std_tile
                    self.clear()
                else:
                    self.set_tex_tile(l_atk1, l_atk2)
                    self.set_matrix(self.std_tile)
                    self.translate(self.dx - 32, self.dy)

                    self.tile_gl = self.std_tile
                    self.clear()
            # Zweiter Angriffstimer wird gesetzt
            if self.duration == 1:
                self.attack_time2 = time.time()

            res = self.attack_time2 - self.attack_time1
            # maximale Dauer der Angriffsanimation
            if res >= 0.005:
                self.allow_attack = False
                self.attack = False
                self.duration = 0

    def get_collision(self, vertical_collist):
        # Generelle Kollision die Sprite mit der Umgebung haben kann.
        # Bekannter Fehler:
        # Sprite bleibt mit rechter Ausrichtung an der Wand
        # während des Sprunges hängen
        x_i = int(self.dx / 32)
        self.wall = False
        self.ground = False
        self.top = False

        collision = vertical_collist[x_i]
        if x_i < 26:
            collision2 = vertical_collist[x_i + 1]
        else:
            collision2 = vertical_collist[x_i]
        if x_i != 0:
            collision3 = vertical_collist[x_i - 1]
        else:
            collision3 = vertical_collist[x_i]

        self.hitbox.set_point(self.dx, self.dy)
        # Überprüft Kollision in der Fläche der aktuellen Spielerposition
        for i in collision:
            if not i[0]:
                continue
            # Rechte obere Ecke
            if self.hitbox.h_get_collision(i[1][0] + 32, i[1][1] + 32):
                self.ground = True

            # Während des Sprungs
            if self.jump:
                # Rechte untere Ecke
                if self.hitbox.h_get_collision(i[1][0] + 32, i[1][1]):
                    self.top = True

        # überprüft die Kollision der Flächen rechts vom Spieler
        for i in collision2:
            if not i[0]:
                continue
            # Linke obere Ecke
            if self.hitbox.h_get_collision(i[1][0], i[1][1] + 32):
                self.ground = True

            # Während des Sprunges
            if self.jump:
                # Linke untere Ecke
                if self.hitbox.h_get_collision(i[1][0], i[1][1]):
                    self.top = True
            # Linke obere Ecke mit rechter Ausrichtung
            if self.hitbox.h_get_collision(i[1][0] - 7, i[1][1] + 29) \
            and self.right:
                self.wall = True

        # Überprüft die Kollision mit den Flächen links vom Spieler
        for i in collision3:
            if not i[0]:
                continue
            # Rechte obere Ecke
            if self.hitbox.h_get_collision(i[1][0] + 37, i[1][1] + 29) \
            and self.left:
                self.wall = True

    def update_status(self, potion=False, attack=False):
        # Das Leben der SpriteEntity hierdurch aktualisiert werden
        # für die diverse Situationen
        if attack and self.allow_damage:
            self.powerup["life"] -= 1
            self.allow_damage = False

        if potion:
            if self.powerup["life"] < 12:
                self.powerup["life"] += 1

        if self.powerup["life"] <= 0 and self._name != "Spieler":
            self.remove_graphic(self)
