# PyRAM

A Python library for managing RAM disks on Windows. Based on ImDisk with RamDisk and WinFs with WinFsPy.
Project target it is:
1. Create more simple API than original library
2. Do more stable than original library
3. Give additional functional than original library
PyRAM my first library, i will try do it good

## Features

- Create RAM disks.
- Remove RAM disks.
- Track disks managed by a `MemoryStorage` instance.
- Simple API with minimal setup.

## Requirements

- Windows
- Python
- ImDisk
- RamDisk
- WinFs(Not strictly required, but necessary for the library to additional function)
- WinFsPy(Not strictly required, but necessary for the library to additionalfunction)
- Python package dependencies required by PyRAM

RAM disk operations may require administrator privileges.

## Installation

Install ImDisk with RamDisk and the required Python dependencies before using PyRAM.

## Quick Start

```python
from PyRAM import MemoryStorage

storage = MemoryStorage()

# Create disk without parameters
storage.create_disk_ramdisk() # uses how default parameters disk_name = "Z:", memory_mb_size = 2048, file_system = "ntfs"

# Create a 512 MB RAM disk
storage.create_disk_ramdisk(
    disk_name="X:",
    memory_mb_size=512,
    file_system = "ntfs"
)

# Remove the RAM disk
storage.remove_disk_ramdisk(disk_name="X:")
# Remove disk without parameter
storage.remove_disk_ramdisk() # uses how default parameter disk_name="Z:"
```

## Usage Notes

- RAM disks use volatile memory. Data stored on them should be considered temporary.
- A drive letter must be available when creating a RAM disk.
- Creating, formatting, or removing a RAM disk may require elevated permissions.
- The library's disk registry tracks disks managed by the current `MemoryStorage` instance.

## License

Not specified yet.
