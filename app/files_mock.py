from files import FilesInterface

class FilesMock(FilesInterface):
    def __init__(self, files: dict={}):
        self.files = files
        self.local_path = ''
        self.path_separator = '\\'

    def path_exists(self, path: str) -> bool:
        return path in self.files

    def create_path(self, path: str) -> bool:
        if path not in self.files:
            self.files[path] = None
            return True
        return False

    def remove_path(self, path: str) -> bool:
        if path in self.files:
            del self.files[path]
            return True
        return False

    def write_file(self, file_name: str, file_data: str) -> int:
        self.files[f'{file_name}.txt'] = file_data
        return len(file_data)

    def remove_file(self, file_name: str) -> bool:
        if f'{file_name}.txt' in self.files:
            del self.files[f'{file_name}.txt']
            return True
        return False

    def read_file(self, collection: str) -> str:
        if f'{collection}.txt' in self.files:
            return self.files[f'{collection}.txt']
        return None