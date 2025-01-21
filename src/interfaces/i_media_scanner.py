from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from src.core.media_file import MediaFile

class IMediaScanner(ABC):
    """Interface for a Media Scanner."""

    @abstractmethod
    def scan_file(self, file_path: Path) -> MediaFile:
        """Scan a single media file and return its metadata."""
        pass

    @abstractmethod
    def scan_directory(self, directory: Path) -> List[MediaFile]:
        """Scan a directory for media files and return a list of their metadata."""
        pass