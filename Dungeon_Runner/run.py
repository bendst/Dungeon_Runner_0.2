# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: Run.py
Klassen: -
Methoden: -
Autor: Ben Stuart
'''
import pyglet
# Schaltet die Debugging von OpenGL aus,
# um die Leistung zu verbessern
pyglet.options["debug_gl"] = False


from src import window

if __name__ == "__main__":
    # Erstellt eine ungebundene Instanz
    window.GameWindow()
    # Führt das Spiel aus
    pyglet.app.run()
