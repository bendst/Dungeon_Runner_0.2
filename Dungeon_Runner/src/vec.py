# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: vec.py
Klassen: Hitbox, Matrix
Methoden: -
Autor: Ben Stuart
'''


class Hitbox(object):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.x2 = 32.0
        self.y2 = 32.0

    def set_point(self, x, y):
        '''Aufpunkt für die Ebene festlegen
        '''
        self.x = x * 1.0
        self.y = y * 1.0

    def resize_box(self, width=1, height=1):
        '''Größe der Vektoren ändern
        '''
        self.x2 = height * 32.0
        self.y2 = width * 32.0

    def h_get_collision(self, dx, dy):
        '''Überprüfung ob ein Punkt in der Ebene liegt
        '''
        r = (dy - self.y) / self.x2

        s = (dx - self.x) / self.y2

        if 0 <= r <= 1 and 0 <= s <= 1:
            return True
        else:
            return False


class Matrix(object):
    """    0,1----1,1        0    0
            |      |    ->   1    0
           0,0----1,0        1    1
                             0    1
    """
    def __init__(self):
        self.matrix_list = []

    def set_matrix(self, matrix):
        self.matrix_list = matrix

    def translate(self, dx, dy):
        """dx = 32, dy = 0
        set_matrix([0.0, 0.0,        0    0
                   32.0, 0.0, ->    32   0
                   32.0, 32.0,      32   32
                   0.0, 32.0,])      0    32

        nach der Manipulation
                                    32    0
                                    64    0
                                    64    32
                                    32    32
        """
        for i in xrange(0, len(self.matrix_list), 2):
            self.matrix_list[i] += dx
            self.matrix_list[i + 1] += dy

    def get_matrix(self):
        return self.matrix_list

    def clear(self):
        self.matrix_list = []
