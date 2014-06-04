# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: enemy.py
Klassen: Knight, Boss, Turret, Arch
Methoden: -
Autor: Ben Stuart
'''
# Importiert das Sprite - Modul und das Modul für sonstige Objekte.
import sprite
import misc


class Knight(sprite.SpriteEntity):
    """Die Klasse stellt einen Gegner im Spiel dar, der sich bewegen
    und mit dem Spieler interagieren kann.
    """
    def __init__(self, posx, posy):
        # Übergabe der Gegnerposition
        self.dx = posx
        self.dy = posy
        # Vererben der SpriteEntity mit Parametern
        super(Knight, self).__init__("K", 1, 2)
        # Position des Gegners wird gesetzt
        self.set_position(posx, posy)
        # Leben des Gegners wird festgelegt
        self.powerup = {"life": 3}
        # Eine Instanz von der Potion - Klasse wird erstellt
        self.potion = misc.Potion()
        # Ein Zähler wird erstellt zur Steuerung der Bewegung
        self.count = 0

    def e_move(self, dt, distance=300):
        if self.move:
            # Verhalten bei rechter Ausrichtung
            if self.right:
                # Verhalten beim Auftreffen mit einer Wand
                if self.wall:
                    self.count = distance - self.count
                    self.left = True
                    self.right = False
                # Verhalten bei keiner Wand im Weg des Gegners
                else:
                    self.on_move(50 * dt, 0)
                    self.count += 1
                    # Änderung der Ausrichtung beim Erreichen
                    # der maximalen Laufdistanz
                    if self.count == distance:
                        self.count = 0
                        self.left = True
                        self.right = False
            # Verhalten bei linker Ausrichtung
            else:
                if self.wall:
                    self.count = distance - self.count
                    self.right = True
                    self.left = False

                else:
                    self.on_move(-50 * dt, 0)
                    self.count += 1
                    if self.count == distance:
                        self.count = 0
                        self.right = True
                        self.left = False
            # Verhalten bei fehlenden Untergrund
            if not self.ground:
                self.on_move(0, -150 * dt)
            # Verhindert, dass der Gegner außerhalb des Spielfenster läuft.
            if self.dx <= 3:
                self.left = False
                self.right = True

            if self.dx >= 829:
                self.left = True
                self.right = False
            # Position des Trankes wird aktualisiert
            self.potion.update_spawn(self.dx, self.dy)

    def e_interact(self, player):
        # Verhalten bei Gegnerangriff
        if self.attack:
            self.move = False
        else:
            self.move = True

        # geändertes Verhalten, wenn der Spieler innerhalb eines bestimmten
        # Bereiches ist.
        if -10 < self.dy - player.dy < 30 and self.alive:
            if 0 < self.dx - player.dx < 150:
                self.left = True
                self.right = False

            if 0 < player.dx - self.dx < 150:
                self.left = False
                self.right = True

            if 0 < self.dx - player.dx < 50 and self.allow_attack:
                self.attack = True

            elif 0 < player.dx - self.dx < 50 and self.allow_attack:
                self.attack = True

            if self.dx - player.dx > 150 or player.dx - self.dx > 150:
                self.allow_attack = True

        # Erlaubt es dem Gegner dem Spieler Schaden zu zufügen,
        # wenn es dem Gegner erlaubt ist anzugreifen.
        if self.allow_attack:
            player.allow_damage = True

        # verändert das Leben des Gegners bei durchgeüfhrten Angriff
        if self.attack and self.allow_attack:
            player.update_status(False, True)
            self.allow_attack = False

        # gegner erhält Schaden unter der Bedingung, dass der Spieler in
        # bestimmten Entfernung steht und passender Ausrichtung steht.
        if player.attack and 0 < (self.dx - player.dx) < 70:
            if -10 < self.dy - player.dy < 70 and player.right:
                self.update_status(False, True)
                self.left = False
                self.right = True

        if player.attack and 0 < (player.dx - self.dx) < 70:
            if -10 < self.dy - player.dy < 70 and player.left:
                self.update_status(False, True)
                self.left = True
                self.right = False

        # Erlaubt es dem Gegner Schaden zu erhalten,
        # wenn der Spieler nicht angreift
        # und erlaubt anzugreifen.
        if player.allow_attack and not player.attack:
            self.allow_damage = True

        # Spieler sammelt Heiltrank auf und aktualisiert sein Leben.
        if self.potion.collect(player.dx, player.dy) \
        and self.powerup["life"] <= 0:
            player.update_status(potion=True)

        # Setzt den Status zu tot, wenn das Leben gleich oder
        # geringer als 0 ist
        if self.powerup["life"] <= 0:
            self.alive = False

    def drop_potion(self, collision_list, dt):
        # Lässt einen Trank erscheinen, wenn keiner im Spiel ist
        if not self.potion.drop:
            self.potion.potion_spawn()
            self.potion.drop = True

        # Ist ein Trank im Spiel wird überprüft,
        # ob dieser am Boden oder in der Luft ist.
        if self.potion.drop:
            self.potion.get_collision(collision_list)
            self.potion.e_move(dt)


class Archer(sprite.SpriteEntity):
    """Platzhalter um die Erweiterbarkeit des Spiels zu garantieren.
    """
    def __init__(self, posx, posy):
        pass

    def e_move(self):
        pass

    def e_interact(self, player):
        pass
    pass


class Boss(sprite.SpriteEntity):
    """Platzhalter um die Erweiterbarkeit des Spiels zu garantieren.
    """
    def __init__(self, posx, posy):
        pass

    def e_move(self):
        pass

    def e_interact(self, player):
        pass
    pass


class Turret(sprite.SpriteEntity):
    """Platzhalter um die Erweiterbarkeit des Spiels zu garantieren.
    """
    def __init__(self, posx, posy):
        pass

    def e_move(self):
        pass

    def e_interact(self, player):
        pass
    pass
