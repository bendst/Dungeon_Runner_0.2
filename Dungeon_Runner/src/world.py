# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: wolrd.py
Klassen: Level
Methoden: -
Autor: Ben Stuart
'''
import os
import collections
import random

from path import get_path
import xmlopen
import tilemap
import npc
import misc


class Level(tilemap.Tilemap):
    def __init__(self, player):
        self.active = 0
        self.fail = False
        self.default_str = "A_LV.xml"
        self._random_list = collections.deque()
        self.reverse_order_list = collections.deque()

        ort = sorted(os.listdir(get_path("spsh_xml")))
        # Liest alle möglichen Level im Ordner aus
        # und weißt jeden eine Nummer zu
        self.level_dict = {
                           k: value for k, value in enumerate(ort)
                           if not value.startswith("s")
                           }

        self.random_level()
        super(Level, self).__init__("spsh_xml/" + self.default_str)
        self.npc = npc.NpcFactory(self.level_dict[self.active])
        self.player = player
        self.player.set_position(50, 500)
        self.key = misc.Key(400, 300)

    def set_level(self):
        # Setzt den aktuellen Level
        # Verhalten, wenn der Spieler nicht den Schlüssel hat
        if not self.player.chest_key:
            zufall = self._random_list.popleft()
            self.active = zufall

            if self.active != 10:
                # speichert die umgekehrte Reihenfolge
                self.reverse_order_list.appendleft(zufall)
            else:
                self.reverse_order_list.append(0)

            self._reload(zufall)
        else:
            level = self.reverse_order_list.popleft()

            self.active = level
            self._reload(level)

    def random_level(self):
        if self.fail:
            self._random_list.clear()
        # Ordnet die Level durch ihre Nummer zufällig an
        while True:
            if len(self._random_list) == len(self.level_dict) - 2:
                self._random_list.append(10)
                break
            else:
                r = random.randint(1, len(self.level_dict) - 2)
                if r not in self._random_list:
                    self._random_list.append(r)

        return self._random_list

    def _reload(self, zufall=0):
        # Ruft die Update Methode für den Level und die Gegner auf
        self.set_new_world("spsh_xml/" + self.level_dict[zufall])
        if self.fail:
            self.npc.update_level(self.level_dict[0])
        else:
            self.npc.update_level(self.level_dict[self.active])

    def respawn(self):
        # Wird die Spielerposition abhänig vom neu betreteten Level gesetzt
        xml = xmlopen.XmlEntity("spawns.xml").get_exit()[self.level_dict[self.active]]
        if not self.player.chest_key:
            prim = xml[0]
            self.player.set_position(xml[prim][0], xml[prim][1])
        else:
            prim = xml[0]
            self.player.set_position(xml[prim - 1][0], xml[prim - 1][1])

    def check_exit(self):
        # Aufbau des get_exit:
        # (Anzahl der Türen, (Ex1_x, Ex1_y), (Ex2_x, Ex2_y), (Spawn_x, Spawn_y))
        xml = xmlopen.XmlEntity("spawns.xml").get_exit()[self.level_dict[self.active]]
        if not self.player.chest_key:
            # Der Spieler ist noch nicht am Ende des Levels gewesen
            for i in xrange(xml[0] - 1):
                if xml[i + 1][0] <= self.player.dx + 16 <= xml[i + 1][0] + 32 \
                and xml[i + 1][1] <= self.player.dy + 10 <= xml[i + 1][1] + 32:
                    return True
        else:
            # Der Spieler ist am Ende des Level und kann nun zurücklaufen
            ex = xml[0]
            if xml[ex][0] <= self.player.dx + 10 <= xml[ex][0] + 32 \
            and xml[ex][1] <= self.player.dy + 10 <= xml[ex][1] + 32:
                return True

    def w_animate(self):
        # Animation der Spielobjekte wird durchgeführt
        self.player.on_animate(17, 18, 5, 6, 23, 0)
        self.npc.animate_npc()

    def w_tick(self, dt, keys):
        # Aktualisiert alle Spielobjekte
        self.npc.tick_npc(dt, self.collision_vertex_list, self.player)
        self.player.get_collision(self.collision_vertex_list)
        self.player.p_move(dt, keys)

        self.key.get_collision(self.collision_vertex_list)
        self.key.e_move(dt)
        # Überprüft, ob ein Schlüssel erscheinen soll
        if self.npc.all_dead() and self.level_dict[self.active] == "K_LV.xml":
            self.key.spawn()
            if self.key.collect(self.player.dx, self.player.dy):
                self.player.chest_key = True

    def win(self):
        # Die Sieg Bedingung wird festgelegt
        if self.active == 0 and self.player.chest_key:
            return True

    def failed(self):
        # Setzt das Spiel zurück
        if self.player.powerup["life"] <= 0:
            self.fail = True
            self.active = 0
            self.random_level()
            self._reload()
            self.player.powerup["life"] = 5
            self.player.set_position(0, 500)
            self.player.chest_key = False
            self.key.alive = False
            self.key.drop = False
            self.key.set_position(400, 300)
            self.fail = False
