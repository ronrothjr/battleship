import sys, os


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

    @staticmethod
    def get_size_at_max(pg, width, height, size=None):
        if size:
            w = size[0]
            h = size[1]
        else:
            info = pg.display.Info()
            w = info.current_w
            h = info.current_h
        current_ratio = w / h
        zoom = w / width if current_ratio < 1 else h / height
        width = int(width * zoom)
        height = int(height * zoom)
        size = (width, height)
        return size

    @staticmethod
    def center(pg, width, height, size=None):
        if size:
            w = size[0]
            h = size[1]
        else:
            info = pg.display.Info()
            w = info.current_w
            h = info.current_h
        left = int( ( w - width ) / 2 )
        top = int( ( h - height ) / 2 )
        position = (left, top)
        return position