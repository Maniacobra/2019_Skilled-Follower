# -*- coding: utf-8 -*-

"""
Icone sous Windows: il faut:
=> un xxx.ico pour integration dans le exe, avec "icon=xxx.ico"
=> un xxx.png pour integration avec PyQt4 + demander la recopie avec includefiles.
"""

import sys, os
from cx_Freeze import setup, Executable

#############################################################################
# preparation des options

# chemins de recherche des modules
# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
path = sys.path

# options d'inclusion/exclusion des modules
includes = []  # nommer les modules non trouves par cx_freeze
excludes = []
packages = []  # nommer les packages utilises

# copier les fichiers non-Python et/ou repertoires et leur contenu:
includefiles = ["ressources"]

if sys.platform == "win32":
    pass
    # includefiles += [...] : ajouter les recopies specifiques à Windows
elif sys.platform == "linux2":
    pass
    # includefiles += [...] : ajouter les recopies specifiques à Linux
else:
    pass
    # includefiles += [...] : cas du Mac OSX non traite ici

# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]

# niveau d'optimisation pour la compilation en bytecodes
optimize = 0

# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = True

# construction du dictionnaire des options
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes,
           "optimize": optimize,
           "silent": silent
           }

# pour inclure sous Windows les dll system de Windows necessaires
if True:
    options["include_msvcr"] = True

#############################################################################
# preparation des cibles

if True:
    base = "Win32GUI"  # pour application graphique sous Windows
    # base = "Console" # pour application en console sous Windows

icone = None
if True:
    icone = "icon.ico"

cible_1 = Executable(
    script="SKILLED FOLLOWER.py",
    base="Win32GUI",
    icon=icone,
    )

cible_2 = Executable(
    script="LEVEL BUILDER.py",
    base="Console",
    icon=icone,
    )

#############################################################################
# creation du setup
setup(
    name="Skilled Follower",
    version="1.0.4",
    description = "",
    author="Maniacobra",
    options={"build_exe": options},
    executables=[cible_1, cible_2]
    )
