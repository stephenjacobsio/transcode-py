from abc import ABC, abstractmethod
from pathlib import Path
from src.core.media_file import MediaFile

class ITranscoder(ABC):
    """Interface for a Transcoder."""

    @abstractmethod
    def transcode(self, media_file: MediaFile, dry_run: bool = False) -> bool:
        """Transcode a media file into a standardized format.

        Args:
            media_file (MediaFile): The media file to transcode.
            dry_run (bool): If True, simulate the transcoding process without performing it.

        Returns:
            bool: True if the transcoding was successful, False otherwise.
        """
        pass

    @abstractmethod
    def generate_output_filename(self, input_file: Path) -> Path:
        """Generate the output file name based on the input file.

        Args:
            input_file (Path): The input file for which to generate the output filename.

        Returns:
            Path: The generated output file name.
        """
        pass

    @abstractmethod
    def build_ffmpeg_command(self, input_file: Path, output_file: Path) -> list:
        """Construct the FFmpeg command for transcoding.

        Args:
            input_file (Path): The input media file.
            output_file (Path): The output media file.

        Returns:
            list: The FFmpeg command as a list of arguments.
        """
        pass
