import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.cli import CLI
from src.core.media_file import MediaFile

class TestCLI(unittest.TestCase):
    def setUp(self):
        """Set up mock arguments and CLI instance."""
        self.mock_args = {
            "path": "test_directory",
            "threads": 4,
            "overwrite": True,
            "dry_run": False,
            "size_threshold": 6.0
        }

    @patch("argparse.ArgumentParser.parse_args")
    @patch("src.cli.MediaScanner")
    @patch("src.cli.Transcoder")
    def test_no_media_files_message(self, mock_transcoder, mock_media_scanner, mock_parse_args):
        """Test CLI logs message when no media files are found."""
        mock_parse_args.return_value = argparse.Namespace(**self.mock_args)
        mock_scanner = mock_media_scanner.return_value
        mock_scanner.scan_directory.return_value = []

        cli = CLI()
        with patch("builtins.print") as mock_print:
            cli.run()
            mock_print.assert_called_with("No media files found in the specified directory.")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("src.cli.MediaScanner")
    @patch("src.cli.Transcoder")
    def test_transcode_calls_count(self, mock_transcoder, mock_media_scanner, mock_parse_args):
        """Test CLI calls transcode the correct number of times."""
        mock_parse_args.return_value = argparse.Namespace(**self.mock_args)
        mock_scanner = mock_media_scanner.return_value
        mock_scanner.scan_directory.return_value = [
            MediaFile(path=Path("/test/file1.mp4"), size_gb=7.0, format="mp4"),
            MediaFile(path=Path("/test/file2.mkv"), size_gb=8.0, format="mkv")
        ]
        mock_transcoder_instance = mock_transcoder.return_value

        cli = CLI()
        cli.run()

        self.assertEqual(mock_transcoder_instance.transcode.call_count, 2)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("src.cli.MediaScanner")
    @patch("src.cli.Transcoder")
    def test_transcode_first_file(self, mock_transcoder, mock_media_scanner, mock_parse_args):
        """Test CLI processes the first eligible file."""
        mock_parse_args.return_value = argparse.Namespace(**self.mock_args)
        mock_scanner = mock_media_scanner.return_value
        mock_scanner.scan_directory.return_value = [
            MediaFile(path=Path("/test/file1.mp4"), size_gb=7.0, format="mp4"),
            MediaFile(path=Path("/test/file2.mkv"), size_gb=8.0, format="mkv")
        ]
        mock_transcoder_instance = mock_transcoder.return_value

        cli = CLI()
        cli.run()

        mock_transcoder_instance.transcode.assert_any_call(
            MediaFile(path=Path("/test/file1.mp4"), size_gb=7.0, format="mp4"),
            dry_run=False
        )

    @patch("argparse.ArgumentParser.parse_args")
    @patch("src.cli.MediaScanner")
    @patch("src.cli.Transcoder")
    def test_transcode_second_file(self, mock_transcoder, mock_media_scanner, mock_parse_args):
        """Test CLI processes the second eligible file."""
        mock_parse_args.return_value = argparse.Namespace(**self.mock_args)
        mock_scanner = mock_media_scanner.return_value
        mock_scanner.scan_directory.return_value = [
            MediaFile(path=Path("/test/file1.mp4"), size_gb=7.0, format="mp4"),
            MediaFile(path=Path("/test/file2.mkv"), size_gb=8.0, format="mkv")
        ]
        mock_transcoder_instance = mock_transcoder.return_value

        cli = CLI()
        cli.run()

        mock_transcoder_instance.transcode.assert_any_call(
            MediaFile(path=Path("/test/file2.mkv"), size_gb=8.0, format="mkv"),
            dry_run=False
        )

    @patch("argparse.ArgumentParser.parse_args")
    @patch("src.cli.MediaScanner")
    @patch("src.cli.Transcoder")
    def test_dry_run_mode(self, mock_transcoder, mock_media_scanner, mock_parse_args):
        """Test CLI processes files in dry-run mode."""
        self.mock_args["dry_run"] = True
        mock_parse_args.return_value = argparse.Namespace(**self.mock_args)
        mock_scanner = mock_media_scanner.return_value
        mock_scanner.scan_directory.return_value = [
            MediaFile(path=Path("/test/file1.mp4"), size_gb=7.0, format="mp4")
        ]
        mock_transcoder_instance = mock_transcoder.return_value

        cli = CLI()
        cli.run()

        mock_transcoder_instance.transcode.assert_called_once_with(
            MediaFile(path=Path("/test/file1.mp4"), size_gb=7.0, format="mp4"),
            dry_run=True
        )

if __name__ == "__main__":
    unittest.main()