# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: texture.py
Klassen: Texture
Methoden: -
Autor: Ben Stuart
'''

from ctypes import byref

import pyglet
from pyglet.gl import *

from path import get_path


class Texture(object):
    textures = []
    files = []

    def __init__(self, filename, reihe, spalte):
        # Legt die zu öffnende Bilddatei mit Pfad fest,
        # falls diese nicht bereits im Speicher ist.
        self._file = filename
        self._open_texture(self._file)
        # Der Index der Textur wird auf 0 gesetzt
        self.texture_index = 0
        # pyglet soll ein Gitter über die gewählte Bilddatei legen und
        # es als Textur zurückgeben.
        image_grid = pyglet.image.ImageGrid(self._image, reihe, spalte)
        self.texture_grid = pyglet.image.TextureGrid(image_grid)
        # Diverse Eigentschaften einer Textur werden als Attribute erstellt..
        self.id_tex = self._get_id()
        self.pitch = self._get_pitch()
        self.pixels = self._get_pixels()
        self.width = self._get_width()
        self.height = self._get_height()

    def _open_texture(self, files):
        # Verhindert das Texturen mehrfach in den Speicher geladen
        # werden
        if files not in Texture.files:
            Texture.files.append(files)
            self._image = pyglet.image.load(get_path(files))
            Texture.textures.append(self._image)
        else:
            count = 0
            for i in Texture.files:
                if i == files:
                    self._image = Texture.textures[count]
                    break
                count += 1

    def _get_width(self):
        # Die Gesamtbreite wird zurückgegeben
        return self._image.width

    def _get_height(self):
        # Die Gesamthähe wird zurückgegeben
        return self._image.height

    def _get_texture(self, index):
        # Gibt anhand des Index einer Ausschnitt der Textur als Subtextur zurück
        return self.texture_grid[index]

    def _get_pitch(self):
        # Gibt die Breite der rohen Bilddatei zurück
        pitch = self._image.get_image_data().width
        return pitch

    def _get_pixels(self):
        # Die gesamtzahl der Pixel wird zurückgegeben
        img_data = self._image.get_image_data()
        pixels = img_data.get_data("RGBA", self.pitch * 4)
        return pixels

    def _get_id(self):
        # Legt eine einzigarte Identifikation für Textur fest
        id_tex = self._image.get_texture().id
        return id_tex

    def bind_tex(self):
        # Die Textur erhält einen einzigarten Integer
        gl_int = GLuint()
        # Die Textur wird mit dem Integer assoziert und
        # an GL_TEXTURE_2D gebunden
        glGenTextures(1, byref(gl_int))
        glBindTexture(GL_TEXTURE_2D, self.id_tex)
        # Eigenschaften der Textur werden an die Grafikkarte übermittelt
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, self.pixels)

    def get_texcoords(self, index):
        # Für den jeweiligen Index, werden Koordinatenpunkte zurückgegeben,
        # die für die Render Pipelin benötigt werden.
        tc = self._get_texture(index).tex_coords
        count = 1
        new = []

        for i in tc:
            if count == 1 or count == 2:
                new.append(i)
            else:
                count = 0
            count += 1

        return new
