# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: graphic.py
Klassen: Graphic
Methoden: -
Autor: Ben Stuart
'''
from pyglet.gl import *
import texture


class Graphic(texture.Texture):
    graphic_cls = []

    def __init__(self, filename, reihe, spalte):
        super(Graphic, self).__init__(filename, reihe, spalte)
        self._tex_gl = 0
        self._tile_gl = 0

    @property
    def tile_gl(self):
        return self._tile_gl

    @tile_gl.setter
    def tile_gl(self, tile):
        # Erstellt ein neues Array, falls sich die Größe
        # der Liste geändert hat
        if not self._tile_gl or len(self._tile_gl) != len(tile):
            self._tile_gl = (GLfloat * len(tile))(*tile)
        else:
            for i in xrange(len(tile)):
                self._tile_gl[i] = tile[i]

    @property
    def tex_gl(self):
        return self._tex_gl

    @tex_gl.setter
    def tex_gl(self, liste):
        # Erstellt ein neues Array, falls sich die Größe
        # der Liste geändert hat
        if not self._tex_gl or len(self._tex_gl) != len(liste):
            self._tex_gl = (GLfloat * len(liste))(*liste)
        else:
            for i in xrange(len(liste)):
                self._tex_gl[i] = liste[i]

    @staticmethod
    def attach_graphic(cls, order):
        # Fügt eine Klasse in die Zeichen Methode ein
        if not cls in Graphic.graphic_cls and cls.alive:
            Graphic.graphic_cls.insert(order, cls)

    @staticmethod
    def remove_graphic(cls):
        # Entfernt eine Klasse von der Zeichen Methode
        if cls in Graphic.graphic_cls:
            Graphic.graphic_cls.remove(cls)

    @staticmethod
    def draw():
        # Zeichnet die grafische Repräsentation der Klassen
        for graphics in Graphic.graphic_cls:
            glBindTexture(GL_TEXTURE_2D, graphics.id_tex)
            glTexCoordPointer(2, GL_FLOAT, 0, graphics.tex_gl)
            glVertexPointer(2, GL_FLOAT, 0, graphics.tile_gl)
            glDrawArrays(GL_QUADS, 0, len(graphics.std_tile) / 2)
