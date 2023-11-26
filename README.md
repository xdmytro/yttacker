# YTTracker

YTTracker is a Python script (`youtube.py`) designed to track and record YouTube video statistics. It fetches data like view counts, like counts, and other relevant information for specified YouTube channels and videos, storing this data in a CSV file for easy analysis.

## Features

- **Data Collection**: Fetches statistics for specific videos and channels from YouTube.
- **CSV Export**: Records data in a CSV file, including video ID, channel name, view count, like count, and more.
- **Configurable**: Allows users to specify API keys, interval times, and start dates through a configuration file.

## Requirements

- Python 3.x
- `requests` library
- A valid YouTube Data API key

## Configuration

Before running the script, ensure that you have a `config.json` file set up with your YouTube API key, the interval at which the script should run (in minutes), and the start date for tracking videos.

Example `config.json`:

```json
{
    "api_key": "YOUR_API_KEY",
    "interval_minutes": 60,
    "start_date": "YYYY-MM-DD"
}
```

## Usage

1. Prepare a list of YouTube channel IDs in `channels.txt`.
2. Run `youtube.py`.
3. The script will periodically fetch the latest video data and store it in `stats.csv`.

## Files

- `youtube.py`: Main script.
- `config.json`: Configuration file for API keys and other settings.
- `channels.txt`: Text file with YouTube channel IDs.
- `videos.txt`: Text file to keep track of video IDs.
- `stats.csv`: CSV file where video data is stored.

## Error Handling

The script includes basic error handling to manage API request failures and to print stack traces for any unhandled exceptions.

## Note

Ensure you adhere to the YouTube API's usage policies and rate limits when using this script.

