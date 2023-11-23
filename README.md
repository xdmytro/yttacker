# YTTracker

YTTracker is a Python tool designed to fetch and record statistics for YouTube videos and channels. It retrieves data such as view counts, like counts, favorite counts, and comment counts for specified YouTube videos and channels, storing this information in a CSV file for further analysis.

## Features

- Fetches video statistics from YouTube using the YouTube Data API.
- Tracks multiple videos and channels.
- Saves data to a CSV file with custom intervals.
- Easy to configure and extend.

## Setup

### Prerequisites

- Python 3.x
- `requests` library (install with `pip install requests`)

### Configuration

1. Create a `config.json` file in the root directory with the following structure:

    ```json
    {
        "api_key": "YOUR_YOUTUBE_DATA_API_KEY",
        "interval_minutes": 1
    }
    ```

    Replace `YOUR_YOUTUBE_DATA_API_KEY` with your actual YouTube Data API key.

2. Create `videos.txt` and `channels.txt` in the root directory.
   - `channels.txt`: List the YouTube channel IDs for which you want to fetch the latest videos, each on a new line.
   - `videos.txt`: List the YouTube video IDs you want to track, each on a new line.

## Usage

Run the script using Python:

```bash
python youtube.py
```

The script will start fetching data based on the configurations and intervals set in `config.json`.

To stop the script, press Ctrl+C in the terminal or command prompt.

## Output

Statistics will be saved to `stats.csv` in the following format:

- Timestamp
- Channel ID
- Channel Title
- Video ID
- Title
- View Count
- Like Count
- Favorite Count
- Comment Count

## Contributing

Contributions, issues, and feature requests are welcome!
