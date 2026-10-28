class PyRAMError(Exception):
    """A fundamental error in the PyRAM library."""

class ComponentNotInstalledError(PyRAMError):
    """A required component is not installed."""

class DiskAlreadyExistsError(PyRAMError):
    """Disk already exists."""

class DiskNotFoundError(PyRAMError):
    """Disk not found."""

class DiskCreationError(PyRAMError):
    """Failed to create disk."""

class IncorrectSymbolInPath(PyRAMError):
    """Character error in the path."""

class NoDiskInPath(PyRAMError):
    """No disk in the path."""

class FileNotFound(PyRAMError):
    """File not found."""

class FolderNotFile(PyRAMError):
    """A folder, not a file."""

class PathNotFound(PyRAMError):
    """Path not found."""

class NotEnoughRAMError(PyRAMError):
    """Not enough RAM."""

class DiskNotAlreadyExistsError(PyRAMError):
    """Disk does not exist."""

class FolderAlreadyExistsError(PyRAMError):
    """Folder already exists."""

class FolderNotAlreadyExistsError(PyRAMError):
    """Folder does not exist."""

class ProcessAlreadyExistsError(PyRAMError):
    """Process already exists."""

class ProcessNotAlreadyExistsError(PyRAMError):
    """Process does not exist."""

class WindowsDiskDeleteError(PyRAMError):
    """Windows disk deletion error"""

class WindowsDiskFormatError(PyRAMError):
    """Windows disk formattion error"""

class ZeroOrNegativeRAMError(PyRAMError):
    """Zero or negative RAM."""

class FailedToFormatDisk(PyRAMError):
    """Disk formatting error"""

class ForeignDiskError(PyRAMError):
    """Not PyRAM created"""

class ImputError(PyRAMError):
    """incorrect answer"""