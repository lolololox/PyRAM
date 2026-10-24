from typing import Any, Set
from pathlib import Path

class MemoryObject:
    def __init__(self):
        self.objects = {}

    def write(self, path, value) -> None:
        self.objects[path] = value

    def read(self, path) -> Any:
        try:
            return self.objects[path]
        except(KeyError):
            raise KeyError(f"Object '{path}', not found!")

    def delete(self, path) -> None:
        del self.objects[path]

    def object_sum(self, path1, path2) -> Any:
        object1 = self.read(path=path1)
        object2 = self.read(path=path2)

        try:
            return object1 + object2
        except(TypeError):
            raise TypeError(f"Can not concatenate '{object1}:{type(object1)}' and '{object2}:{type(object2)}'")

    def object_sub(self, path1, path2) -> Any:
        object1 = self.read(path=path1)
        object2 = self.read(path=path2)

        try:
            return object1 - object2
        except(TypeError):
            raise TypeError(f"Can not subtract '{object1}:{type(object1)}' and '{object2}:{type(object2)}'")

    def object_div(self, path1, path2) -> int | float | bool | complex:
        object1 = self.read(path=path1)
        object2 = self.read(path=path2)

        try:
            return object1 / object2
        except(TypeError):
            raise TypeError(f"Can not divide '{object1}:{type(object1)}' and '{object2}:{type(object2)}'")

    def object_mul(self, path1, path2) -> Any:
        object1 = self.read(path=path1)
        object2 = self.read(path=path2)

        try:
            return object1 * object2
        except(TypeError):
            raise TypeError(f"Can not multiply '{object1}:{type(object1)}' and '{object2}:{type(object2)}'")

    def object_equal(self, path1, path2) -> bool:
        object1 = self.read(path=path1)
        object2 = self.read(path=path2)

        if object1 == object2:
            return True
        elif object1 != object2:
            return False
        else:
            raise RuntimeError(f"Objects cannot be compared, {object1}:{type(object1)} and {object2}:{type(object2)}")

class MemoryPythonFolder:
    def __init__(self):
        self.filesystem = {}
        self.default_disk = "C"

    def write(self, path: str, value=None) -> None:
        disk = path.split(":")[0]

        if len(disk) > 1:
            raise RuntimeError("Pls enter disk, for example 'C:/example/popato.txt'")
        
        path_without_disk = path.split(":")[1]
        blocked_symbol = {":", ";", ","}
        clean_path = Path(path)
        list_of_parts = clean_path.parts
        # file_name = clean_path.name

        if any(symbol in path_without_disk for symbol in blocked_symbol):
            raise RuntimeError("Pls do not use ':', ';', ',' in path, for example 'C:/example/popato.txt'")

        current = self.filesystem

        for part in list_of_parts[:-1]:
            if current == part:
                current = current[part]
                continue
            current = current.setdefault(part, {})

        if list_of_parts[-1] is not None and value is not None:
            current[list_of_parts[-1]] = value
        elif list_of_parts[-1] is not None and value is None:
            current[list_of_parts[-1]] = {}

        return self.filesystem

    def read(self, path: str) -> Any:
        disk = path.split(":")[0]

        if len(disk) > 1:
            raise RuntimeError("Pls enter disk, for example 'C:/example/popato.txt'")
        
        path_without_disk = path.split(":")[1]
        blocked_symbol = {":", ";", ","}
        clean_path = Path(path)
        list_of_parts = clean_path.parts

        if any(symbol in path_without_disk for symbol in blocked_symbol):
            raise RuntimeError("Pls do not use ':', ';', ',' in path, for example 'C:/example/popato.txt'")

        current = self.filesystem

        for part in list_of_parts:
            try:
                current = current[part]
            except(KeyError):
                raise KeyError(f"File {path} not found")

        return current

    def listdir(self, path: str) -> Any:
        disk = path.split(":")[0]

        if len(disk) > 1:
            raise RuntimeError("Pls enter disk, for example 'C:/example/popato.txt'")
        
        path_without_disk = path.split(":")[1]
        blocked_symbol = {":", ";", ","}
        clean_path = Path(path)
        list_of_parts = clean_path.parts

        if any(symbol in path_without_disk for symbol in blocked_symbol):
            raise RuntimeError("Pls do not use ':', ';', ',' in path, for example 'C:/example/popato.txt'")

        current = self.filesystem

        for part in list_of_parts:
            try:
                current = current[part]
            except(KeyError):
                raise KeyError(f"File {path} not found")

        if isinstance(current, str):
            raise AttributeError("Path must end by folder, not file!")
        return list(current.keys())

    def delete(self, path: str) -> None:
        disk = path.split(":")[0]

        if len(disk) > 1:
            raise RuntimeError("Pls enter disk, for example 'C:/example/popato.txt'")
        
        path_without_disk = path.split(":")[1]
        blocked_symbol = {":", ";", ","}
        clean_path = Path(path)
        list_of_parts = clean_path.parts

        if any(symbol in path_without_disk for symbol in blocked_symbol):
            raise RuntimeError("Pls do not use ':', ';', ',' in path, for example 'C:/example/popato.txt'")

        current = self.filesystem

        for part in list_of_parts[:-1]:
            try:
                current = current[part]
            except KeyError:
                raise KeyError(f"Path '{path}' not found")

        try:
            del current[list_of_parts[-1]]
        except KeyError:
            raise KeyError(f"File '{path}' not found")

