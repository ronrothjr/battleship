import json
from abc import ABCMeta, abstractmethod
from files import FilesInterface
from files import Files

class DataInterface(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return(hasattr(subclass, 'decode_records') and callable(subclass.decode_records) and
               hasattr(subclass, 'encode_records') and callable(subclass.encode_records) and
               hasattr(subclass, 'save_records') and callable(subclass.save_records) and
               hasattr(subclass, 'load_records') and callable(subclass.load_records) or
               NotImplemented)

    @property
    @abstractmethod
    def files(self) -> FilesInterface:
        raise NotImplementedError

    @abstractmethod
    def __init__(self, Files, collections=[]):
        pass

    @abstractmethod
    def decode_records(self, records_str: str) -> list:
        raise NotImplementedError

    @abstractmethod
    def encode_records(self, records: list) -> str:
        raise NotImplementedError

    @abstractmethod
    def save_records(self, collection, records) -> int:
        raise NotImplementedError

    @abstractmethod
    def load_records(self, collection) -> list:
        raise NotImplementedError

class Data(DataInterface):

    @staticmethod
    def get_object_dict(object_to_dict):
        data_dict = {}
        for k, v in dict(object_to_dict.__dict__).items():
            if isinstance(v, (int, str, dict, bool)):
                data_dict[k] = v
            elif isinstance(v, list):
                data_dict[k] = [Data.get_object_dict(item) for item in v]
            else:
                data_dict[k] = Data.get_object_dict(v)
        return data_dict

    @property
    def files(self) -> FilesInterface:
        return self._files

    @files.setter
    def files(self, value: FilesInterface):
        self._files = value

    def __init__(self, files: FilesInterface=None, collections=[]):
        self.files: FilesInterface = files or Files()
        self.collections = {}
        if collections:
            for collection in collections:
                records_str = self.files.read_file('collection')
                records = self.decode_records(records_str)
                self.collections[collection] = records

    def decode_records(self, records_str: str) -> list:
        if records_str is None:
            return []
        file_records = json.loads(records_str)
        return file_records

    def encode_records(self, records: list) -> str:
        if not records:
            return '[]'
        file_str = json.dumps(records)
        return file_str

    def save_records(self, collection, records):
        file_str = self.encode_records(records)
        file_size = self.files.write_file(collection, file_str)
        return file_size

    def load_records(self, collection) -> list:
        try:
            file_str = self.files.read_file(collection)
            file_records = self.decode_records(file_str)
            return file_records
        except:
            return []
        