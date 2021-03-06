# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: window.py
Klassen: GameWindow
Methoden: init_gl
Autor: Ben Stuart
'''

import sys
import pyglet
from pyglet.window import key
from pyglet.gl import *
from pyglet.font import GlyphString

from path import get_path
import world
import player
import misc
import graphic

debug = False

def init_gl():
    # Globale Zustände werden für den OpenGL Kontext
    # aktiviert:
    # 2D Texturen, der Alpha Kanal und das Zeichnen über Arrays
    # sowie wird die allgemeine Hintergrundfarbe eingestellt.
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glEnableClientState(GL_VERTEX_ARRAY)
    glClearColor(0.15, 0.15, 0.15, 1.0)


class GameWindow(pyglet.window.Window):
    def __init__(self):
        self.w_width = 864
        self.w_height = 640

        self.start = True
        self.help = False
        self.trans = 1.0
        self.trans_bool = True
        self.pos_menu = 0

        config = pyglet.gl.Config(sample_buffers=1, samples=4,
                                  double_buffer=True, debug=False)

        super(GameWindow, self).__init__(self.w_width, self.w_height,
                                         config=config, vsync=False)
        if not debug:
            self.set_fullscreen()
        self.set_caption("Dungeon Runner")
        init_gl()
        # Instanzen des Spielers, der Lebensanzeige
        # und der Spielwelt werden erstellt
        self.player = player.Player()
        self.heartbar = misc.Heartbar()
        self.level = world.Level(self.player)
        # Hintergrundbilder des Menüs werden geladen
        self.menu_start = pyglet.image.load(get_path("Start.png"))
        self.menu_help = pyglet.image.load(get_path("Hilfe.png"))
        # Font wird aus der Datei geladen
        pyglet.font.add_file(get_path("font/Cardinal.ttf"))
        cardinal_s70 = pyglet.font.load("Cardinal", size=70,
                                        bold=False, italic=False)
        cardinal_s40 = pyglet.font.load("Cardinal", size=40,
                                        bold=False, italic=False)
        # Erstellen von Unicode Strings
        text_1 = u"~ Spiel ~"
        text_2 = u"~ Hilfe ~"
        text_3 = u"~ Ende ~"
        text_win = u"Gewonnen!"
        # Setzt die die Strings auf eine bestimmte Größe
        glyph_3 = cardinal_s40.get_glyphs(text_1)
        glyph_4 = cardinal_s40.get_glyphs(text_2)
        glyph_5 = cardinal_s40.get_glyphs(text_3)
        glyph_6 = cardinal_s70.get_glyphs(text_win)
        # Strings werden zu Glypen
        # um durch OpenGL darstellbar zu werden
        self.glyph_str_3 = GlyphString(text_1, glyph_3,
                                       self.w_width / 2 - 75,
                                       self.w_height / 2 - 50)  # Start
        self.glyph_str_4 = GlyphString(text_2, glyph_4,
                                       self.w_width / 2 - 75,
                                       self.w_height / 2 - 150)  # Hilfe
        self.glyph_str_5 = GlyphString(text_3, glyph_5,
                                       self.w_width / 2 - 75,
                                       self.w_height / 2 - 250)
        self.glyph_str_6 = GlyphString(text_win, glyph_6,
                                       290, self.w_height / 2)
        # Fügt den KeyStateHandler zu den Events hinzu
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        # Setzt die Wiederholungsrate der tick Methode und Animatione
        # fest, sowie die maximale Bildwiederholungsrate
        pyglet.clock.schedule_interval(self.tick, 1 / 60.)
        pyglet.clock.schedule_interval(self.on_animate, 1 / 5.)
        pyglet.clock.set_fps_limit(60.)

    def on_key_press(self, symbol, modifiers):
        # Der Anwender kommt zurück in das Menü
        if self.keys[key.ESCAPE] and not self.start:
            self.start = True
        # Überprüft ob der Spieler an einer Tür steht
        if self.keys[key.E]:
            if self.level.check_exit():
                self.level.set_level()
                self.level.respawn()

        if self.keys[key.K]:
            self.level.player.powerup["life"] = 0
        # Aktionen im Menü werden kontrolliert
        if self.keys[key.W] and self.start\
        or self.keys[key.UP] and self.start:
            self.pos_menu -= 1
            self.trans = 0.0
            if self.pos_menu == -1:
                self.pos_menu = 2

        if self.keys[key.S] and self.start\
        or self.keys[key.DOWN] and self.start:
            self.pos_menu += 1
            self.trans = 0.0
            if self.pos_menu == 3:
                self.pos_menu = 0

        if self.keys[key.SPACE] or self.keys[key.ENTER]:
            if self.pos_menu == 0:
                self.start = False

            elif self.pos_menu == 1:
                self.help = True

            elif self.pos_menu == 2:
                if sys.platform == "win32":
                    sys.exit()
                else:
                    pyglet.app.exit()

        if self.keys[key.ESCAPE] and self.help:
            self.help = False

    def tick(self, dt):
        if self.start:
            # Ruft die Funktion für das Blinken
            # des ausgewählten Textes auf
            self.trans_animation(dt)
        else:
            # Überprüft, ob das Spiel verloren ist
            self.level.failed()
            # Aktualisiert das Spiel
            self.level.w_tick(dt, self.keys)
            # Aktualisiert die Lebensanzeige des Spielers
            self.heartbar.set_status(self.player.powerup["life"])

    def on_animate(self, dt):
        if not self.start:
            # Führt die Animation der dynamischen Spielobjekte durch
            self.level.w_animate()

    def trans_animation(self, dt):
        # Blinken des ausgewählten Textes
        # durch das Manipulieren des Alpha Wertes
        step = abs(dt)
        if self.trans_bool:
            if self.trans <= 0.0:
                self.trans_bool = False
            self.trans = self.trans - step
            return self.trans

        else:
            if self.trans >= 1.0:
                self.trans_bool = True
            self.trans = self.trans + step
            return self.trans

    def on_draw(self):
        # Der Farben Buffer wird bereinigt
        glClear(GL_COLOR_BUFFER_BIT)
        # Die Identätenmatrix wird geladen
        glLoadIdentity()
        # Setzt das Spielfenster mittig bei Vollbild
        if self.fullscreen:
            glTranslatef(self.screen.width / 2 - self.w_width / 2,
                         self.screen.height / 2 - self.w_height / 2, 0)
        # Setzt die Farbe auf Weiß
        glColor4f(1.0, 1.0, 1.0, 1.0)

        if self.start:
            if not self.help:
                # Zeichen des Menü Hintergrund
                self.menu_start.blit(0, 0)
                # Zeichnen einzelner Menüpunkte
                if self.pos_menu == 0:
                    glColor4f(0.0, 0.0, 0.0, self.trans)
                    self.glyph_str_3.draw()
                    glColor4f(0.0, 0.0, 0.0, 1.0)
                    self.glyph_str_4.draw()
                    self.glyph_str_5.draw()

                elif self.pos_menu == 1:
                    glColor4f(0.0, 0.0, 0.0, self.trans)
                    self.glyph_str_4.draw()
                    glColor4f(0.0, 0.0, 0.0, 1.0)
                    self.glyph_str_3.draw()
                    self.glyph_str_5.draw()

                elif self.pos_menu == 2:
                    glColor4f(0.0, 0.0, 0.0, self.trans)
                    self.glyph_str_5.draw()
                    glColor4f(0.0, 0.0, 0.0, 1.0)
                    self.glyph_str_4.draw()
                    self.glyph_str_3.draw()
            else:
                self.menu_help.blit(0, 0)

        else:
            # Überprüft ob das Spiel gewonnen ist
            if self.level.win():
                glColor4f(0.5, 0.5, 0.5, 1.0)
                graphic.Graphic.draw()
                glColor4f(0.0, 0.0, 0.0, 1.0)
                self.glyph_str_6.draw()
            else:
                # Ruft die Zeichen Methode auf
                graphic.Graphic.draw()

        # Bereinigt den vorderen Buffer
        # Ein Buffer Wechsel entfällt,
        # da dieser automatisch vom EventLoop aufgerufen wird
        glFlush()
