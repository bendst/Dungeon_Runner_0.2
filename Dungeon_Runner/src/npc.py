# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: npc.py
Klassen: NpcFactory
Methoden: -
Autor: Ben Stuart
'''
import xmlopen
import enemy
import graphic


class NpcFactory(object):
    npc = []
    dic = xmlopen.XmlEntity("spawns.xml").get_mob()

    def __init__(self, level):
        # Es werden Gegner aufgrund des Levels erstellt
        if level in NpcFactory.dic:
            if isinstance(NpcFactory.dic[level], tuple):
                mob_type = NpcFactory.dic[level][0]
                posx = NpcFactory.dic[level][1]
                posy = NpcFactory.dic[level][2]

                if mob_type == "K":
                    NpcFactory.add_entity(enemy.Knight(posx, posy))
                elif mob_type == "A":
                    NpcFactory.add_entity(enemy.Archer(posx, posy))
                elif mob_type == "T":
                    NpcFactory.add_entity(enemy.Turret(posx, posy))
                elif mob_type == "B":
                    NpcFactory.add_entity(enemy.Boss(posx, posy))

            if isinstance(NpcFactory.dic[level], list):
                dic = NpcFactory.dic[level]

                for i in xrange(0, len(dic)):
                    mob_type = dic[i][0]
                    posx = dic[i][1]
                    posy = dic[i][2]
                    if mob_type == "K":
                        NpcFactory.add_entity(enemy.Knight(posx, posy))
                    elif mob_type == "A":
                        NpcFactory.add_entity(enemy.Archer(posx, posy))
                    elif mob_type == "T":
                        NpcFactory.add_entity(enemy.Turret(posx, posy))
                    elif mob_type == "B":
                        NpcFactory.add_entity(enemy.Boss(posx, posy))

    @staticmethod
    def add_entity(mob):
        NpcFactory.npc.append(mob)

    @staticmethod
    def update_level(level):
        # Aktualisiert die npc - Liste auf der Grundlage des
        # levels
        for mobs in NpcFactory.npc:
            graphic.Graphic.remove_graphic(mobs.potion)
            graphic.Graphic.remove_graphic(mobs)

        NpcFactory.npc[:] = []
        NpcFactory(level)

    @staticmethod
    def animate_npc():
        # Führt die Animation der Gegner durch
        for mobs in NpcFactory.npc:
            if mobs.powerup["life"] > 0:
                mobs.on_animate(17, 18, 5, 6, 23, 0)

    @staticmethod
    def tick_npc(dt, collision_vertex_dict, player):
        # Aktualisiert die Gegner
        for mobs in NpcFactory.npc:
            if mobs.powerup["life"] > 0:
                mobs.get_collision(collision_vertex_dict)
                mobs.e_move(dt)
            else:
                mobs.drop_potion(collision_vertex_dict, dt)
            mobs.e_interact(player)
            mobs.update_status()

    @staticmethod
    def all_dead():
        # Überprüft ob alle Gegner in der Liste besiegt sind
        new = []
        for mob in NpcFactory.npc:
            new.append(mob.alive)

        if not filter(None, new):
            return True
        else:
            return False
