import unittest
from pathlib import Path
from src.core.media_file import MediaFile

class TestMediaFile(unittest.TestCase):
    def test_media_file_initialization(self):
        """Test initialization of MediaFile dataclass."""
        test_path = Path("/test/file.mp4")
        test_size_gb = 2.5
        test_format = "mp4"

        media_file = MediaFile(path=test_path, size_gb=test_size_gb, format=test_format)

        self.assertEqual(media_file.path, test_path)
        self.assertEqual(media_file.size_gb, test_size_gb)
        self.assertEqual(media_file.format, test_format)

    def test_media_file_invalid_path(self):
        """Test MediaFile handles invalid paths gracefully."""
        with self.assertRaises(TypeError):
            MediaFile(path="invalid_path", size_gb=2.5, format="mp4")

    def test_media_file_negative_size(self):
        """Test MediaFile does not allow negative size values."""
        test_path = Path("/test/file.mp4")
        test_format = "mp4"

        with self.assertRaises(ValueError):
            MediaFile(path=test_path, size_gb=-1.0, format=test_format)

if __name__ == "__main__":
    unittest.main()
