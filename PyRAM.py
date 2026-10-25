from typing import Any
from pathlib import Path
import subprocess
import sys
import os

try:
    import psutil
    psutil_instaled = True
except(ImportError, ImportWarning):
    psutil_instaled = False

try:
    import winfspy
    winfspy_installed = True
except(ImportError, ImportWarning):
    print("Warning: winfspy not installed!\nPls download winfspy on site https://winfsp.dev/ and download library winfspy.")
    winfspy_installed = False

try:
    import ramdisk
    from ramdisk import create_hd, remove_hd
    ramdisk_installed = True
except(ImportError, ImportWarning):
    print("Warning: ramdisk not installed!\nPls download ramdisk")
    ramdisk_installed = False

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

class MemoryStorage:
    def __init__(self):
        self.disks = {}
        self.folders = {}
        self.process = {}

        for i in self.get_all_drives():
            drive: str = i.rstrip(r"\\")
            self.disks[drive] = None

        print(self.disks)

    def get_all_drives(self) -> list:
        drives = os.listdrives()
        return drives

    def create_disk_ramdisk(self, disk_name: str = "Z:", memory_mb_size: int = 2048, file_system: str = "ntfs") -> bool:
        if ramdisk_installed == False:
            raise ModuleNotFoundError("ramdisk not installed!")

        if disk_name in self.disks:
            raise RuntimeError(f"Disk: {disk_name.rstrip(":")} already exists")

        if psutil_instaled == True:
            bytes_val = psutil.virtual_memory().total
            mb_val = bytes_val / (1024 ** 2)

            if memory_mb_size > mb_val:
                raise RuntimeError("You cannot specify more RAM than you actually have!")

        elif psutil_instaled == False:
            print("Warning: psutil not installed, can not check RAM restrictions")

        success = create_hd(size_in_megabyte=memory_mb_size, drive_letter=disk_name, fs=file_system)

        self.disks[disk_name] = success

        return True if success else False

    def remove_disk_ramdisk(self, disk_name: str, forse: bool = True) -> bool:
        if ramdisk_installed == False:
            raise ModuleNotFoundError("ramdisk not installed!")

        if not disk_name in self.disks:
            raise RuntimeError(f"Disk: {disk_name.rstrip(":")} not already exists")

        success = remove_hd(drive_letter=disk_name, force=forse)

        del self.disks[disk_name]

        return True if success else False

    def get_all_disks(self) -> dict:
        return self.disks

    def get_all_folders(self) -> dict:
        return self.folders

    def get_all_processes(self) -> dict:
        return self.process

    def create_disk_winfspy(self, disk_name: str = "Z:") -> subprocess.Popen:
        if winfspy_installed == False:
            raise ModuleNotFoundError("winfspy not installed!")

        if disk_name in self.disks:
            raise RuntimeError(f"Disk: {disk_name.rstrip(":")} already exists")

        process = subprocess.Popen([
            sys.executable,
            "-m", "winfspy.memfs",
            disk_name,
        ])

        self.process[disk_name] = process

        return process

    def old_create_folder_winfspy(self, path: str) -> subprocess.Popen:
        if winfspy_installed == False:
            raise ModuleNotFoundError("winfspy not installed!")

        clead_path = Path(path)

        if clead_path in self.folders:
            raise RuntimeError(f"Folder: {path} already exists")

        process = subprocess.Popen([
            sys.executable,
            "-m", "winfspy.memfs",
            clead_path,
        ])

        self.process[clead_path] = process

        return process

    def remove_storage_winfspy(self, pointer: str) -> bool:
        if winfspy_installed == False:
            raise ModuleNotFoundError("winfspy not installed!")

        if pointer not in self.disks and pointer not in self.folders:
            raise RuntimeError(f"Process: {pointer.rstrip(":")} not already exists")

        process: subprocess.Popen = self.process.get(pointer)

        if process is None:
            return False

        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


