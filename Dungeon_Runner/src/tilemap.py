# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: tilemap.py
Klassen: Tilemap
Methoden: -
Autor: Ben Stuart
'''
from pyglet.gl import *

import xmlopen
import graphic
from itertools import islice


class Tilemap(graphic.Graphic):
    def __init__(self, xmllevel, image="spsh_images/Spritesheet.png"):
        """Erstellt Tiles mit Textur anhand des Levels

        """
        self.alive = True
        self.xml = xmlopen.XmlWorld(xmllevel)

        self.img = image
        super(Tilemap, self).__init__(self.img, 8, 8)
        self.bind_tex()

        self.std_tile = self.xml.get_vertex()
        # property.setter
        self.tex_list = self.xml

        self._collision_count_list = []
        self._collision_vertex_dict = {}
        self._vertical_vertex_list = []
        self._vertical_collision_list = []
        self._collision_list = []

        # property.setter
        self.collision_list = self.xml
        # property.setter
        self.collision_vertex_list = self._collision_count_list
        # property.setter
        self.tile_gl = self.std_tile
        self.tex_gl = self.tex_list

        self.attach_graphic(self, 0)

    @property
    def tex_list(self):
        return self._tex_list

    @tex_list.setter
    def tex_list(self, filename):
        self._tex_list = []
        for i in filename:
            self._tex_list.extend(self.get_texcoords(i))

    @property
    def collision_list(self):
        return self._vertical_collision_list

    @collision_list.setter
    def collision_list(self, xml):
        count = 0
        # Es wird festgelegt für welche Texturen
        # eine Kollision stattfinden kann
        for i in xml:
            if i < 5 or i == 7 or i == 8:
                self._collision_list.append(True)

            else:
                self._collision_list.append(False)

            self._collision_count_list.append(count)
            count += 8

        for ii in xrange(0, 27):
            cl_iter = islice(self._collision_list, ii, 540, 27)
            cl_slice = [ik for ik in cl_iter]
            # Die Liste enthält 27 untergeordneten Listen, die
            # jeweils 20 boolische Werte haben
            self._vertical_collision_list.append(cl_slice)

    @property
    def collision_vertex_list(self):
        return self._vertical_vertex_list

    @collision_vertex_list.setter
    def collision_vertex_list(self, liste):
        # Reguläre Auflistung der einzelen Flächen
        self._collision_vertex_dict = {k: (self.std_tile[i],
                                           self.std_tile[i + 1])
                                       for k, i in enumerate(liste)}

        # Vertikale Sortierung
        for ii in xrange(0, 27):
            cvd_iter = islice(self._collision_vertex_dict.values(),
                              ii, 540, 27)

            cvd_slice = [ik for ik in cvd_iter]

            cl_slice = [[iv] for iv in self._vertical_collision_list[ii]]

            for iii in xrange(len(cl_slice)):

                # if cl_slice[iii][0]:
                cl_slice[iii].append(cvd_slice[iii])
            # Die Liste enthält 27 untergeordnete Listen.
            # den boolischen Werten wurden jetzt
            # noch Koordinaten zugewiesen
            self._vertical_vertex_list.append(cl_slice)

    def _clear(self):
        # Setzt die Listen zurück
        self._vertical_collision_list[:] = []
        self._collision_list[:] = []
        self._collision_count_list[:] = []
        self._vertical_vertex_list[:] = []

    def set_new_world(self, level):
        # Setzt den Level neu, es wird dazu eine neue Xxml - Datei
        # ausgelesen
        self._clear()

        self.xml = xmlopen.XmlWorld(level)

        self.collision_list = self.xml
        self.collision_vertex_list = self._collision_count_list

        self.tex_list = self.xml
        self.tex_gl = self.tex_list
