# PyRAM

A Python library for managing RAM disks on Windows. Based on ImDisk with RamDisk and WinFs with WinFsPy.
Project target it is:

1. Create more simple API than original library
2. Do more stable than original library
3. Give additional functional than original library

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
- RamDisk
- WinFs(Not strictly required, but necessary for the library to additional function)
- WinFsPy(Not strictly required, but necessary for the library to additional features)
- Python package dependencies required by PyRAM

RAM disk operations may require administrator privileges.

## Installation

Install ImDisk with RamDisk and the required Python dependencies before using PyRAM.

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
```

## Usage Notes

- RAM disks use volatile memory. Data stored on them should be considered temporary.
- A drive letter must be available when creating a RAM disk.
- Creating, formatting, or removing a RAM disk may require elevated permissions.
- The library's disk registry tracks disks managed by the current `MemoryStorage` instance.

## License

Not specified yet.

## Documentation

- classes

1. MemoryObject. Just dict with dicts
2. MemoryPythonFolder. Virtual file system, where you can save only string data types
3. MemoryStorage. Class where access create folders and disks in ram and see it in explorer

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
2. create_disk_ramdisk. Create disk in RAM using RamDisk
3. remove_disk_ramdisk. Delete disk, that created using RamDisk
4. format_ramdisk. Format disk
5. get_all_disks/get_all_folders/get_all_processes. Get all disks/folders/processes
6. create_disk_winfspy. Create disk in RAM using WinFsPy
7. create_folder_winfspy. Create folder in RAM using WinFsPy
8. remove_storage_winfspy. Remove storage, that created using WinFsPy
