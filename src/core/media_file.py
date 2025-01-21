from dataclasses import dataclass
from pathlib import Path

@dataclass
class MediaFile:
    """Data class representing a media file."""
    path: Path
    size_gb: float
    format: str