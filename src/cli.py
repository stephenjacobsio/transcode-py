import argparse
import logging
from pathlib import Path
from src.core.media_scanner import MediaScanner
from src.core.transcoder import Transcoder
from src.config.settings import VIDEO_EXTENSIONS

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

class CLI:
    """Command-line interface for the media transcoder tool."""

    def __init__(self):
        self.args = self._parse_arguments()
        self.scanner = MediaScanner(VIDEO_EXTENSIONS)
        self.transcoder = Transcoder(threads=self.args.threads, overwrite=self.args.overwrite)

    @staticmethod
    def _parse_arguments() -> argparse.Namespace:
        """Parse command-line arguments."""
        parser = argparse.ArgumentParser(
            description=(
                "Recursively scan directories for media files, display file info, and "
                "optionally transcode those above a size threshold into H.264/AAC MKV, up to 1080p."
            )
        )
        parser.add_argument(
            "path",
            help="Path to file or directory to scan/transcode"
        )
        parser.add_argument(
            "-t", "--threads",
            type=int,
            default=2,
            help="Number of CPU threads for ffmpeg (default=2)"
        )
        parser.add_argument(
            "-y", "--overwrite",
            action="store_true",
            help="Overwrite output files if they exist without prompting."
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be transcoded without actually doing it."
        )
        parser.add_argument(
            "--size-threshold",
            type=float,
            default=6.0,
            help="Minimum file size (in GB) to consider for transcoding (default=6.0)"
        )
        return parser.parse_args()

    def run(self):
        """Execute the CLI operations."""
        target_path = Path(self.args.path)

        if not target_path.exists():
            logging.error(f"Specified path does not exist: {target_path}")
            return

        media_files = self._scan_target(target_path)
        self._display_files(media_files)

        eligible_files = [m for m in media_files if m.size_gb > self.args.size_threshold]
        if not eligible_files:
            logging.info("No media files exceed the size threshold.")
            return

        for media in eligible_files:
            self.transcoder.transcode(media, dry_run=self.args.dry_run)

    def _scan_target(self, target_path: Path):
        """Scan the specified file or directory for media files."""
        if target_path.is_file():
            return [self.scanner.scan_file(target_path)]
        return self.scanner.scan_directory(target_path)

    @staticmethod
    def _display_files(media_files):
        """Display the list of media files found during the scan."""
        if not media_files:
            logging.info("No media files found in the specified directory.")
            return

        print("Found the following media files:\n")
        for idx, media in enumerate(media_files, start=1):
            print(f"{idx}. {media.path} | Size: {media.size_gb:.2f} GB | Format: {media.format}")