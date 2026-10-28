from exceptions import (
    PyRAMError, ComponentNotInstalledError,
    DiskAlreadyExistsError, DiskNotFoundError,
    DiskCreationError, IncorrectSymbolInPath,
    NoDiskInPath, FolderNotFile, FileNotFound,
    PathNotFound, NotEnoughRAMError,
    DiskNotAlreadyExistsError, FolderAlreadyExistsError,
    FolderNotAlreadyExistsError, ProcessAlreadyExistsError,
    ProcessNotAlreadyExistsError, WindowsDiskDeleteError,
    ZeroOrNegativeRAMError, FailedToFormatDisk,
    WindowsDiskFormatError, ForeignDiskError, ImputError
)
from typing import Any
from pathlib import Path, PureWindowsPath
import subprocess
import sys
import os
import platform
from warnings import deprecated

MARKER = ".pyram_owned"

if platform.system() != "Windows":
    raise RuntimeError("Library only for Windows")

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
            raise NoDiskInPath("Pls enter disk, for example 'C:/example/popato.txt'")
        
        path_without_disk = path.split(":")[1]
        blocked_symbol = {":", ";", ","}
        clean_path = Path(path)
        list_of_parts = clean_path.parts
        # file_name = clean_path.name

        if any(symbol in path_without_disk for symbol in blocked_symbol):
            raise IncorrectSymbolInPath("Pls do not use ':', ';', ',' in path, for example 'C:/example/popato.txt'")

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
            raise NoDiskInPath("Pls enter disk, for example 'C:/example/popato.txt'")
        
        path_without_disk = path.split(":")[1]
        blocked_symbol = {":", ";", ","}
        clean_path = Path(path)
        list_of_parts = clean_path.parts

        if any(symbol in path_without_disk for symbol in blocked_symbol):
            raise IncorrectSymbolInPath("Pls do not use ':', ';', ',' in path, for example 'C:/example/popato.txt'")

        current = self.filesystem

        for part in list_of_parts:
            try:
                current = current[part]
            except(KeyError):
                raise FileNotFound(f"File {path} not found")

        return current

    def listdir(self, path: str) -> Any:
        disk = path.split(":")[0]

        if len(disk) > 1:
            raise NoDiskInPath("Pls enter disk, for example 'C:/example/popato.txt'")
        
        path_without_disk = path.split(":")[1]
        blocked_symbol = {":", ";", ","}
        clean_path = Path(path)
        list_of_parts = clean_path.parts

        if any(symbol in path_without_disk for symbol in blocked_symbol):
            raise IncorrectSymbolInPath("Pls do not use ':', ';', ',' in path, for example 'C:/example/popato.txt'")

        current = self.filesystem

        for part in list_of_parts:
            try:
                current = current[part]
            except(KeyError):
                raise FileNotFound(f"File {path} not found")

        if isinstance(current, str):
            raise FolderNotFile("Path must end by folder, not file!")

        return list(current.keys())

    def delete(self, path: str) -> None:
        disk = path.split(":")[0]

        if len(disk) > 1:
            raise NoDiskInPath("Pls enter disk, for example 'C:/example/popato.txt'")
        
        path_without_disk = path.split(":")[1]
        blocked_symbol = {":", ";", ","}
        clean_path = Path(path)
        list_of_parts = clean_path.parts

        if any(symbol in path_without_disk for symbol in blocked_symbol):
            raise IncorrectSymbolInPath("Pls do not use ':', ';', ',' in path, for example 'C:/example/popato.txt'")

        current = self.filesystem

        for part in list_of_parts[:-1]:
            try:
                current = current[part]
            except KeyError:
                raise PathNotFound(f"Path '{path}' not found")

        try:
            del current[list_of_parts[-1]]
        except KeyError:
            raise FileNotFound(f"File '{path}' not found")

class MemoryStorage:
    def __init__(self):
        self.disks = {}
        self.folders = {}
        self.process = {}

        for d in self.get_all_drives():
            drive = d.rstrip("\\")
            self.disks[drive] = "Record restored, between sessions" if self._is_owned(drive) else None

    def _is_owned(self, drive: str) -> bool:
        try:
            return os.path.isfile(os.path.join(drive + "\\", MARKER))
        except OSError:
            return False

    def check_disk_formatted(self, disk_name: str) -> bool:
        if psutil_instaled == False:
            raise ComponentNotInstalledError("Psutil not installed, please do it")

        disk_name = self.__normalizate_disk_name(disk_name)

        partitions = psutil.disk_partitions(all=True)
        
        for p in partitions:
            if p.device.startswith(disk_name) or p.mountpoint.startswith(disk_name):
                if p.fstype and p.fstype.upper() != 'RAW':
                    return True
                else:
                    return False
                    
        return False

    def __normalizate_disk_name(self, name: str) -> str:
        name = name.upper()

        if not name.endswith(":"):
            name += ":"

        return name

    def get_all_drives(self) -> list:
        drives = os.listdrives()
        return drives

    def create_disk_ramdisk(self, disk_name: str = "Z:", memory_mb_size: int = 2048, file_system: str = "ntfs") -> bool:
        disk_name = self.__normalizate_disk_name(disk_name)

        if ramdisk_installed == False:
            raise ComponentNotInstalledError("ramdisk not installed!")

        if disk_name in self.disks:
            raise DiskAlreadyExistsError(f"Disk: '{disk_name.rstrip(":")}' already exists")

        if psutil_instaled == True:
            bytes_val = psutil.virtual_memory().total
            mb_val = bytes_val / (1024 ** 2)

            if memory_mb_size > mb_val:
                raise NotEnoughRAMError("You cannot specify more RAM than you actually have!")

        elif psutil_instaled == False:
            print("Warning: psutil not installed, can not check RAM restrictions")

        if memory_mb_size <= 0:
            raise ZeroOrNegativeRAMError(f"RAM is zero or negative: '{memory_mb_size}'")

        try:
            success = create_hd(size_in_megabyte=memory_mb_size, drive_letter=disk_name, fs=file_system)
        except Exception as e:
            raise PyRAMError(f"Somethink went wrong!\n{e}")

        success_code = bool(success)

        if success_code:
            self.disks[disk_name] = success

        if not self.format_ramdisk(disk_name, file_system, forse_check=True):
            print(f"Warning: Failed to format RAM disk '{disk_name.rstrip(":")}'\nYou need to run the process as an administrator.")
        else:
            Path(disk_name + "\\", MARKER).write_text("created by PyRAM")

        return success_code

    def remove_disk_ramdisk(self, disk_name: str, force: bool = True, forse_check: bool = False) -> bool:
        disk_name = self.__normalizate_disk_name(disk_name)

        if ramdisk_installed == False:
            raise ComponentNotInstalledError("ramdisk not installed!")

        if self.disks.get(disk_name) == None:
            if not self.check_disk_formatted(disk_name=disk_name) and forse_check == False:
                accept = input(f"Disk not formatted, detele it? n | y ")
                if accept.lower() == "n":
                    return
                elif accept.lower() == "y":
                    pass
                else:
                    raise ImportError("Please input correct answer")

            else:
                raise ForeignDiskError(f"Disk {disk_name.rstrip(":")} was not created by PyRAM")

        if not disk_name in self.disks:
            raise DiskNotAlreadyExistsError(f"Disk: '{disk_name.rstrip(":")}' not already exists")

        sys_drive = os.environ.get('SystemDrive')

        if sys_drive == disk_name:
            raise WindowsDiskDeleteError("You can not delete main Windows disk")

        try:
            success = remove_hd(drive_letter=disk_name, force=force)
        except Exception as e:
            raise PyRAMError(f"Somethink went wrong!\n{e}")

        success_code = bool(success)

        if success_code:
            del self.disks[disk_name]

        return success_code

    def format_ramdisk(self, disk_name: str, file_system: str = "NTFS", forse_check: bool = False) -> bool:
        disk_name = self.__normalizate_disk_name(disk_name)

        sys_drive = os.environ.get('SystemDrive')

        if sys_drive == disk_name:
            raise WindowsDiskFormatError("You can not format main Windows disk")

        if self.disks.get(disk_name) == None:
            if not self.check_disk_formatted(disk_name=disk_name) and forse_check == False:
                accept = input(f"Disk not formatted, detele it? n | y ")
                if accept.lower() == "n":
                    return
                elif accept.lower() == "y":
                    pass
                else:
                    raise ImportError("Please input correct answer")

            else:
                raise ForeignDiskError(f"Disk {disk_name.rstrip(":")} was not created by PyRAM")

        if file_system.upper() not in {"NTFS", "FAT32", "EXFAT"}:
            raise ValueError("Unsupported file system")

        result = subprocess.run(
            [
                "format.com",
                disk_name,
                f"/FS:{file_system.upper()}",
                "/Q",
                "/Y",
            ],
            capture_output=True,
            text=True,
            timeout=60,
            shell=False,
        )

        return result.returncode == 0

    def get_all_disks(self) -> dict:
        return self.disks

    def get_all_folders(self) -> dict:
        return self.folders

    def get_all_processes(self) -> dict:
        return self.process

    @deprecated("Experimental method, not stable. Please use ramdisk methods")
    def create_disk_winfspy(self, disk_name: str = "Z:") -> subprocess.Popen:
        if winfspy_installed == False:
            raise ComponentNotInstalledError("winfspy not installed!")

        if disk_name in self.disks:
            raise DiskAlreadyExistsError(f"Disk: '{disk_name.rstrip(":")}' already exists")

        process = subprocess.Popen([
            sys.executable,
            "-m", "winfspy.memfs",
            disk_name,
        ])

        self.process[disk_name] = process

        return process

    @deprecated("Experimental method, not stable. Please use ramdisk methods")
    def create_folder_winfspy(self, path: str) -> subprocess.Popen:
        if winfspy_installed == False:
            raise ComponentNotInstalledError("winfspy not installed!")

        clead_path = Path(path)

        if clead_path in self.folders:
            raise FolderAlreadyExistsError(f"Folder: {path} already exists")

        process = subprocess.Popen([
            sys.executable,
            "-m", "winfspy.memfs",
            clead_path,
        ])

        self.process[clead_path] = process

        return process

    @deprecated("Experimental method, not stable. Please use ramdisk methods")
    def remove_storage_winfspy(self, pointer: str) -> bool:
        if len(pointer) <= 2:
            pointer = self.__normalizate_disk_name(pointer)

        if winfspy_installed == False:
            raise ComponentNotInstalledError("winfspy not installed!")

        if pointer not in self.disks and pointer not in self.folders:
            raise ProcessNotAlreadyExistsError(f"Process: {pointer.rstrip(":")} not already exists")

        process: subprocess.Popen = self.process.get(pointer)

        if process is None:
            return False

        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

        if len(pointer) >= 2:
            del self.folders[pointer]
        else:
            del self.disks[pointer]
