
""" Charger tous les Classe pour que le import * dans app, passe sans souci """
import os
import glob

__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py")]
