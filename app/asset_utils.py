import sys, os
from turtle import st


class AssetUtils:

    @staticmethod
    def resource_path(*args):
        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, os.path.join(*args))

    @staticmethod
    def get_surface(pg, image_name):
        image_path = AssetUtils.resource_path('assets', 'images', image_name)
        return pg.image.load(image_path).convert()