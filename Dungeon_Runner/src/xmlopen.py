# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: xmlopen.py
Klassen: XmlEntity, XmlWorld
Methoden: -
Autor: Ben Stuart
'''

import random
import xml.etree.ElementTree as ET

from path import get_path


class XmlEntity(object):
    def __init__(self, filename):
        # Der with Ausdruck ist unglaublich praktisch,
        # da Dateien damit automatisch geschlossen werden.
        with open(get_path(filename), 'r') as files:
            self.et = ET.parse(files)
            self.e = self.et.getroot()
        # Ausnahmebehandlung für die spawns.xml
        if filename != "spawns.xml":
            self.b = self.set_subelement()

    @property
    def get_dict(self):
        """Gibt ein Dictionary zurück mit allen Elementen
        der geöffneten XML-Datei
        """
        return self.subitem

    def get_mob(self):
        """
        @return: Dictionary key=level values=mob_type, position
        """
        # Lokale Variablen
        mob_dic = {}
        count = 0
        mob_list = []
        # Schleife iteriert über den Inhalt der spawns.xml
        for child in self.e:
            mob_count = int(child.getchildren()[0].text)
            new_key = child.attrib.values()

            if mob_count == 0:
                mob_dic[new_key[0]] = mob_count

            if mob_count == 1:
                mob_type = child.getchildren()[1].text
                spawn_x = int(child.getchildren()[2].text)
                spawn_y = int(child.getchildren()[3].text)
                mob_dic[new_key[0]] = (mob_type, spawn_x, spawn_y)

            if 2 <= mob_count < 10:
                for i in xrange(1, mob_count + 1):
                    mob_type = child.getchildren()[i + count].text
                    spawn_x = int(child.getchildren()[i + 1 + count].text)
                    spawn_y = int(child.getchildren()[i + 2 + count].text)
                    mob_list.append((mob_type, spawn_x, spawn_y))
                    mob_dic.setdefault(new_key[0], mob_list)
                    count += 2
                    if count / 2 >= mob_count:
                        count = 0
                        mob_list = []

            if mob_count == 10:
                mob_list = []
                for i in xrange(mob_count - 1):
                    mob_type = "K"
                    spawn_x = random.randint(256, 800)
                    spawn_y = 32
                    mob_list.append((mob_type, spawn_x, spawn_y))
                    mob_dic.setdefault(new_key[0], mob_list)

        return mob_dic

    def get_exit(self):
        """Liest die Ausgangspunkte im Level aus.
        Die ersten 2 Punkte sind die Exit-Points und der
        3te ist der Player-Spawn.
        """
        exit_dic = {}
        for child in self.e:
            new_key = child.attrib.values()
            if bool(child.findall("exit")):
                exit_count = int(child.find("exit").text)

                ex1 = child.getchildren()[-exit_count].text
                ex1_i = tuple((int(ex1[:3]), int(ex1[4:])))

                if exit_count == 1:
                        exit_dic.setdefault(new_key[0], (exit_count, ex1_i))

                elif exit_count == 2:
                    ex2 = child.getchildren()[-exit_count + 1].text
                    ex2_i = tuple((int(ex2[:3]), int(ex2[4:])))

                    exit_dic.setdefault(new_key[0], (exit_count, ex1_i, ex2_i))

                elif exit_count == 3:
                    ex2 = child.getchildren()[-exit_count + 1].text
                    ex2_i = tuple((int(ex2[:3]), int(ex2[4:])))

                    ex3 = child.getchildren()[-exit_count + 2].text
                    ex3_i = tuple((int(ex3[:3]), int(ex3[4:])))

                    exit_dic.setdefault(new_key[0], (exit_count, ex1_i,
                                                     ex2_i, ex3_i))

                elif exit_count == 4:
                    ex2 = child.getchildren()[-exit_count + 1].text
                    ex2_i = tuple((int(ex2[:3]), int(ex2[4:])))

                    ex3 = child.getchildren()[-exit_count + 2].text
                    ex3_i = tuple((int(ex3[:3]), int(ex3[4:])))

                    ex4 = child.getchildren()[-exit_count + 3].text
                    ex4_i = tuple((int(ex4[:3]), int(ex4[4:])))

                    exit_dic.setdefault(new_key[0], (exit_count, ex1_i,
                                                     ex2_i, ex3_i, ex4_i))

        return exit_dic

    def get_headline(self, index):
        """Gibt eine Liste mit den Inhalten der Titelleiste zurück
        #absolut unnötig
        """
        return int(self.headline[index][1])

    def set_subelement(self):
        c = self.e.getchildren()[0].getchildren()
        self.subitem = {
                        c[i].items()[0][1]: c[i].getchildren()[0].items() \
                        for i in xrange(len(c))
                        }

    def set_headline(self):
        c = self.e.items()
        self.headline = c


class XmlWorld(XmlEntity):
    def set_subelement(self):
        c = self.e.getchildren()[0]

        self.subitem = {
                        i: c.getchildren()[i].items() for i in xrange(len(c))
                        }
        return self.subitem

    def get_vertex(self):
        """
        Gibt ein Liste mit 8 Koordinatenpunkte zurück.
        """
        coords4v = []
        x1 = [
              float(self.b[i][1][1]) for i in xrange(len(self.b))
              ]
        y1 = [
              (19.0 - float(self.b[i][0][1])) for i in xrange(len(self.b))
              ]

        for i in xrange(0, len(self.b)):
            coords4v.append(x1[i] * 32)
            coords4v.append(y1[i] * 32)

            coords4v.append(x1[i] * 32 + 32)
            coords4v.append(y1[i] * 32)

            coords4v.append(x1[i] * 32 + 32)
            coords4v.append(y1[i] * 32 + 32)

            coords4v.append(x1[i] * 32)
            coords4v.append(y1[i] * 32 + 32)

        return coords4v

    def __iter__(self):
        # Iteriert über den Inhalt einer Level - Datei.
        # Dabei werden die Textur - Indexe generiert
        for i in xrange(len(self.b)):
            index = int(self.get_dict[i][4][1])
            yield index
