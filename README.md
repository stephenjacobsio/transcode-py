# PyTranscode

PyTranscode is a Python-based media transcoding tool that recursively scans directories for media files, displays metadata, and optionally transcodes files exceeding a configurable size threshold. It leverages FFmpeg for transcoding operations and follows clean architecture principles.

## Features

- **Recursive Directory Scanning**: Finds media files in specified directories.
- **Metadata Extraction**: Retrieves file size, format, and other details.
- **Configurable Transcoding**: Converts media files to H.264/AAC in MKV format.
- **Dry-Run Mode**: Simulates the transcoding process without making changes.
- **Clean Code Architecture**: Designed for maintainability and extensibility.

## Requirements

- Python 3.8+
- FFmpeg installed and available in your PATH

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pytranscode.git
   cd pytranscode
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the CLI:

```bash
python src/main.py <path> [options]
```

### Arguments

| Argument              | Description                                              |
|-----------------------|----------------------------------------------------------|
| `<path>`              | Path to the file or directory to scan/transcode.         |

### Options

| Option                | Description                                              |
|-----------------------|----------------------------------------------------------|
| `-t`, `--threads`     | Number of CPU threads for FFmpeg (default: 2).           |
| `-y`, `--overwrite`   | Overwrite output files if they already exist.            |
| `--dry-run`           | Simulate transcoding without making changes.             |
| `--size-threshold`    | Minimum file size (in GB) to consider for transcoding.   |

## Example

To scan a directory and transcode files larger than 6GB:

```bash
python src/main.py /path/to/media --threads 4 --size-threshold 6.0
```

To perform a dry run:

```bash
python src/main.py /path/to/media --dry-run
```

## Testing

Run unit tests with:

```bash
python -m unittest discover -s tests
```

## Project Structure

```plaintext
pytranscode/
├── src/
│   ├── cli.py                # Command-line interface
│   ├── config/
│   │   ├── __init__.py       # Config initialization
│   │   └── settings.py       # Configurations and constants
│   ├── core/
│   │   ├── __init__.py       # Core package initialization
│   │   ├── media_file.py     # MediaFile dataclass
│   │   ├── media_scanner.py  # Media scanning logic
│   │   └── transcoder.py     # Transcoding logic
│   ├── interfaces/
│   │   ├── __init__.py       # Interfaces initialization
│   │   ├── i_media_scanner.py # Media scanner interface
│   │   └── i_transcoder.py   # Transcoder interface
│   └── main.py               # Main entry point
├── tests/
│   ├── test_cli.py           # CLI unit tests
│   ├── test_media_file.py    # MediaFile unit tests
│   ├── test_media_scanner.py # MediaScanner unit tests
│   └── test_transcoder.py    # Transcoder unit tests
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Contributing

Contributions are welcome! Please fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Acknowledgments

- [FFmpeg](https://ffmpeg.org/) for the powerful transcoding capabilities.
- Python community for the amazing libraries and support.

---

<div style="text-align: center;">Made with ❤️ by Stephen Jacobs</div>