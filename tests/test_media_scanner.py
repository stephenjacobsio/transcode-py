import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.core.media_scanner import MediaScanner
from src.core.media_file import MediaFile

class TestMediaScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = MediaScanner(supported_extensions=(".mp4", ".mkv"))

    @patch("os.walk")
    def test_scan_directory_empty(self, mock_os_walk):
        """Test scanning a directory with no files."""
        mock_os_walk.return_value = [("/test", [], [])]
        result = self.scanner.scan_directory(Path("/test"))
        self.assertEqual(len(result), 0)

    @patch("os.walk")
    @patch("src.core.media_scanner.MediaScanner.is_media_file")
    @patch("src.core.media_scanner.MediaScanner.get_file_size_gb")
    @patch("src.core.media_scanner.MediaScanner.probe_format")
    def test_scan_directory_with_files_count(self, mock_probe_format, mock_get_file_size_gb, mock_is_media_file, mock_os_walk):
        """Test the number of files scanned."""
        mock_os_walk.return_value = [("/test", [], ["file1.mp4", "file2.mkv"])]
        mock_is_media_file.side_effect = lambda x: x.suffix in (".mp4", ".mkv")
        mock_get_file_size_gb.side_effect = [2.5, 1.5]
        mock_probe_format.side_effect = ["mp4", "mkv"]

        result = self.scanner.scan_directory(Path("/test"))
        self.assertEqual(len(result), 2)

    @patch("os.walk")
    @patch("src.core.media_scanner.MediaScanner.is_media_file")
    @patch("src.core.media_scanner.MediaScanner.get_file_size_gb")
    @patch("src.core.media_scanner.MediaScanner.probe_format")
    def test_scan_directory_first_file(self, mock_probe_format, mock_get_file_size_gb, mock_is_media_file, mock_os_walk):
        """Test the first scanned file."""
        mock_os_walk.return_value = [("/test", [], ["file1.mp4", "file2.mkv"])]
        mock_is_media_file.side_effect = lambda x: x.suffix in (".mp4", ".mkv")
        mock_get_file_size_gb.side_effect = [2.5, 1.5]
        mock_probe_format.side_effect = ["mp4", "mkv"]

        result = self.scanner.scan_directory(Path("/test"))
        self.assertEqual(result[0], MediaFile(Path("/test/file1.mp4"), 2.5, "mp4"))

    def test_is_media_file_true(self):
        """Test if a valid media file is recognized."""
        result = self.scanner.is_media_file(Path("/test/file.mp4"))
        self.assertTrue(result)

    def test_is_media_file_false(self):
        """Test if a non-media file is not recognized."""
        result = self.scanner.is_media_file(Path("/test/file.txt"))
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()