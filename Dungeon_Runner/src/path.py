# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Lernleistung: Dungeon Runner
Modul: path.py
Klassen: -
Methoden: get_path
Autor: Ben Stuart
'''
import os
import sys


def get_path(path):
    if sys.platform == "win32":
        relativ = os.path.abspath("../Dungeon_Runner/res")
        convert = os.path.join(relativ, path)
        return os.path.normpath(convert)

    else:
        relativ = os.path.abspath("../Dungeon_Runner/res")
        return os.path.join(relativ, path)
