from typing import Any, Set

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


class MemoryFolder:
    def __init__(self):
        pass

