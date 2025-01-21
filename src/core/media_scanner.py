import os
from pathlib import Path
from typing import List
from src.core.media_file import MediaFile

class MediaScanner:
    def __init__(self, supported_extensions: tuple):
        self.supported_extensions = supported_extensions

    def scan_directory(self, directory: Path) -> List[MediaFile]:
        """Scan a directory for media files and return their metadata."""
        media_files = []
        for file_path in self._get_all_files(directory):
            if self.is_media_file(file_path):
                media_files.append(self._process_media_file(file_path))
        return media_files

    def _get_all_files(self, directory: Path) -> List[Path]:
        """Retrieve all files from the directory recursively."""
        for root, _, files in os.walk(directory):
            for file in files:
                yield Path(root) / file

    def is_media_file(self, file_path: Path) -> bool:
        """Check if the file has a supported media file extension."""
        return file_path.suffix.lower() in self.supported_extensions

    def _process_media_file(self, file_path: Path) -> MediaFile:
        """Generate metadata for a single media file."""
        size_gb = self.get_file_size_gb(file_path)
        fmt = self.probe_format(file_path)
        return MediaFile(path=file_path, size_gb=size_gb, format=fmt)

    @staticmethod
    def get_file_size_gb(file_path: Path) -> float:
        """Get the size of the file in gigabytes."""
        size_bytes = file_path.stat().st_size
        return size_bytes / (1024 ** 3)

    @staticmethod
    def probe_format(file_path: Path) -> str:
        """Determine the format of the media file using external tools."""
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=format_name",
                "-of", "json",
                str(file_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return data["format"].get("format_name", "Unknown")
        except Exception as e:
            logging.error(f"Failed to probe format for {file_path}: {e}")
            return "Unknown"
