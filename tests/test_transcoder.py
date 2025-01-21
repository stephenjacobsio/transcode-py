import unittest
from unittest.mock import patch
from pathlib import Path
from src.core.transcoder import Transcoder
from src.core.media_file import MediaFile

class TestTranscoder(unittest.TestCase):
    def setUp(self):
        self.transcoder = Transcoder(threads=4, overwrite=True)

    @patch("subprocess.run")
    def test_transcode_successful(self, mock_subprocess_run):
        """Test successful transcoding."""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        media_file = MediaFile(path=Path("/test/file.mp4"), size_gb=2.5, format="mp4")

        result = self.transcoder.transcode(media_file)
        self.assertTrue(result)

    @patch("subprocess.run")
    def test_transcode_failure(self, mock_subprocess_run):
        """Test transcoding failure."""
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "ffmpeg")
        media_file = MediaFile(path=Path("/test/file.mp4"), size_gb=2.5, format="mp4")

        result = self.transcoder.transcode(media_file)
        self.assertFalse(result)

    def test_generate_output_filename(self):
        """Test output filename generation."""
        input_file = Path("/test/file.mp4")
        expected_output = Path("/test/file_transcoded.mkv")
        result = self.transcoder.generate_output_filename(input_file)
        self.assertEqual(result, expected_output)

    def test_build_ffmpeg_command(self):
        """Test FFmpeg command generation."""
        input_file = Path("/test/file.mp4")
        output_file = Path("/test/file_transcoded.mkv")
        result = self.transcoder.build_ffmpeg_command(input_file, output_file)

        expected_command = [
            "ffmpeg",
            "-i", str(input_file),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-f", "matroska",
            "-y", str(output_file)
        ]

        self.assertEqual(result, expected_command)

if __name__ == "__main__":
    unittest.main()
