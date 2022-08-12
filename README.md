# info-display

A simple script for displaying file information in a directory

| Item | Content |
| :-- | :-- |
| Python version | 3.9 |
| Dependencies | OpenCV, PyYAML, Tabulate |
| License | MIT |

## Usage

```bash
python {/path/to/}info_display.py [OPTIONS ...]
```

### Available options

| Option | Description | Note |
| :-- | :-- | :-- |
| -h, --help | Show help information | |
| -d, --dir | Root scan directory (Default: working directory) | Since v0.3.0 |
| -P, --pattern | Regular expression for matching certain files | |
| -e, --ext, --extension | File extensions for matching certain files | Multiple arguments supported |
| -s, --stat-dir | Directory for saving output statistic file (Will not save if not specified) | |
| -D, --show-duration | Show duration of audio and video files | Flag |
| -E, --dec, --decimal | Use decimal data units (e.g. MB, GB, TB) instead of binary ones (e.g. MiB, GiB, TiB) | Flag |
| ~~-p, --path~~ | ~~Root scan directory~~ | Until v0.3.0, <span style="color:yellow">DEPRECATED</span>, <span style="color:red;"><b>DELETED</b></span> |