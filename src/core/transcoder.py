import logging
from pathlib import Path
from src.core.media_file import MediaFile
from src.interfaces.i_transcoder import ITranscoder
import subprocess
from typing import List

class Transcoder(ITranscoder):
    """Concrete implementation of ITranscoder for transcoding media files."""

    def __init__(self, threads: int, overwrite: bool):
        self.threads = threads
        self.overwrite = overwrite

    def transcode(self, media_file: MediaFile, dry_run: bool = False) -> bool:
        """Transcode a media file into a standardized format."""
        output_file = self.generate_output_filename(media_file.path)
        logging.info(f"Preparing to transcode: {media_file.path}")
        logging.info(f"Output will be saved to: {output_file}")

        if not self._can_proceed_with_transcoding(output_file, dry_run):
            return False

        command = self.build_ffmpeg_command(media_file.path, output_file)
        return self._execute_transcoding(command, media_file, output_file)

    @staticmethod
    def generate_output_filename(input_file: Path) -> Path:
        """Generate the output file name based on the input file."""
        return input_file.with_name(f"{input_file.stem}_transcoded.mkv")

    def build_ffmpeg_command(self, input_file: Path, output_file: Path) -> List[str]:
        """Construct the FFmpeg command for transcoding."""
        overwrite_flag = ["-y"] if self.overwrite else ["-n"]

        return [
            "ffmpeg",
            "-i", str(input_file),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-f", "matroska"
        ] + overwrite_flag + [str(output_file)]

    def _can_proceed_with_transcoding(self, output_file: Path, dry_run: bool) -> bool:
        """Determine if transcoding can proceed based on conditions."""
        if output_file.exists() and not self.overwrite:
            logging.warning(f"Output file already exists and overwrite is disabled: {output_file}")
            return False

        if dry_run:
            logging.info("Dry run enabled. Skipping actual transcoding.")
            return False

        return True

    @staticmethod
    def _execute_transcoding(command: List[str], media_file: MediaFile, output_file: Path) -> bool:
        """Execute the FFmpeg command and handle the process output."""
        logging.info(f"Executing FFmpeg command: {' '.join(command)}")

        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            logging.info(f"Successfully transcoded: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Transcoding failed for {media_file.path}: {e.stderr}")
            return False