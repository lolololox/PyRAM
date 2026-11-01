# PyRAM

A Python library for managing RAM disks on Windows. Based on ImDisk with RamDisk and WinFs with WinFsPy.
Project target it is:

1. Create more simple API than original library
2. Do more stable than original library
3. Give additional functional than original library

> [!CAUTION]
> **IMPORTANT:**
>
> 1. Early version of the library, bugs are possible
> 2. Disks may be removed with a delay
> 3. API can changes every update, please check actual documentation
> 4. Administrator privileges are required for the library to function properly
> 5. ONLY Windows
> 6. PyRAM only manages disks it created (ImDisk units 100-199) and refuses to touch others.

## Features

- Create RAM disks.
- Remove RAM disks.
- Track disks managed by a `MemoryStorage` instance.
- Simple API with minimal setup.
- Format RAM disks
- Virtual in-memory file system

## Requirements

- Windows
- Python
- ImDisk
- WinFs(Not strictly required, but necessary for the library to additional function)
- WinFsPy(Not strictly required, but necessary for the library to additional features)
- Python 3.12 and higer

RAM disk operations may require administrator privileges.

## Installation

Install ImDisk and the required Python dependencies before using PyRAM.
In short time meybe you can install PyRAM from PaPi(Pip install PyRAMObjects)

## Quick Start

```python
from PyRAM import MemoryStorage

storage = MemoryStorage()

# Create disk without parameters
storage.create_disk_ramdisk() # uses default parameters disk_name = "Z:", memory_mb_size = 2048, file_system = "ntfs"

# Create a 512 MB RAM disk
storage.create_disk_ramdisk(
    disk_name="X:",
    memory_mb_size=512,
    file_system = "ntfs"
)

# Remove the RAM disk
storage.remove_disk_ramdisk(disk_name="X:")

with MemoryStorage(cleanup_on_exit=True) as storage1: # cleaning all PyRAM disks when app closing, becouse cleanup_on_exit=True
    storage1.create_disk_imdisk(disk_name="K:", memory_mb_size=512)
```

## Usage Notes

- RAM disks use volatile memory. Data stored on them should be considered temporary.
- A drive letter must be available when creating a RAM disk.
- Creating, formatting, or removing a RAM disk may require elevated permissions.
- The library's disk registry tracks disks managed by the current `MemoryStorage` instance.

## License

MIT

## Documentation

- classes

1. MemoryObject. Just dict with dicts
2. MemoryPythonFolder. Virtual file system, where you can save only string data types
3. MemoryStorage. Class where access create folders(experimental only WinFsPy) and disks in ram and see it in explorer
4. DiskInfo. Just dataclass, has no methods

### MemoryObject methods

1. write. Save value
2. read. Get value
3. delete. delete value
4. object_sum/object_sub/object_div/object_mul/object_equal. Operations with objects

### MemoryPythonFolder methods

1. write. Save value
2. read. Get value
3. listdir. Get list of folders
4. delete. Delete value

### MemoryStorage methods

1. get_all_drives. Get all drives
2. remove_disk_imdisk. Create disk in RAM using ImDisk
3. remove_disk_imdisk. Delete disk, that created using ImDisk
4. format_ramdisk. Format disk
5. get_all_disks/get_all_folders/get_all_processes. Get all disks/folders/processes
6. create_disk_winfspy. Create disk in RAM using WinFsPy
7. create_folder_winfspy. Create folder in RAM using WinFsPy
8. remove_storage_winfspy. Remove storage, that created using WinFsPy
9. get_windows_disk. Get Windows disk
10. check_disk_formatted. Check disk formatted or not
11. get_drive_label. Get disk label
12. is_drive_readonly. Check disk read-only or not
13. get_disk_info. Get info about disk
